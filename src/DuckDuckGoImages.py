import re
import io
import os
import json
import uuid
import shutil
import random
import requests
from PIL import Image
from joblib import Parallel, delayed

class Images:
    URL = "https://duckduckgo.com/"

    def __init__(self):
        pass
    
    def download(self, query, folder='.', max_urls=None, thumbnails=False, parallel=False, shuffle=False, remove_folder=False):
        if thumbnails:
            urls = self.get_image_thumbnails_search_urls(query)
        else:
            urls = self.get_image_search_urls(query)
        
        if shuffle:
            random.shuffle(urls)
        
        if max_urls is not None and len(urls) > max_urls:
            urls = urls[:max_urls]
            
        if remove_folder:
            self.remove_folder(folder)
        
        self.create_folder(folder)
        if parallel:
            return self.parallel_download_urls(urls, folder)
        else:
            return self.download_urls(urls, folder)

    def _download(self, url, folder):
            try:
                filename = str(uuid.uuid4().hex)
                while os.path.exists("{}/{}.jpg".format(folder, filename)):
                    filename = str(uuid.uuid4().hex)
                response = requests.get(url, stream=True, timeout=1.0, allow_redirects=True)
                with Image.open(io.BytesIO(response.content)) as im:
                    with open("{}/{}.jpg".format(folder, filename), 'wb') as out_file:
                        im.save(out_file)
                        return True
            except:
                return False
    
    def download_urls(self, urls, folder):
        downloaded = 0
        for url in urls:
            if self._download(url, folder):
                downloaded += 1
        return downloaded

    def parallel_download_urls(self, urls, folder):
        downloaded = 0
        with Parallel(n_jobs=os.cpu_count()) as parallel:
            results = parallel(delayed(self._download)(url, folder) for url in urls)
            for result in results:
                if result:
                    downloaded += 1
        return downloaded


    def get_image_search_urls(self, query):
        token = self.fetch_token(query)
        return self.fetch_search_urls(query, token)
    
    def get_image_thumbnails_search_urls(self, query):
        token = self.fetch_token(query)
        return self.fetch_search_urls(query, token, what="thumbnail")
    
    def fetch_token(self, query):
        res = requests.post(self.URL, data={'q': query})
        if res.status_code != 200:
            return ""
        match = re.search(r"vqd='([\d-]+)'", res.text, re.M|re.I)
        if match is None:
            return ""
        return match.group(1)
    
    def fetch_search_urls(self, query, token, what="image"):
        query = {
            "vqd": token,
            "q": query,
            "l": "wt-wt",
            "o": "json",
            "f": ",,,",
            "p": "2"
        }
        urls = []

        res = requests.get(self.URL+"i.js", params=query)
        if res.status_code != 200:
            return urls

        data = json.loads(res.text)
        for result in data["results"]:
            urls.append(result[what])

        while "next" in data:
            res = requests.get(self.URL+data["next"], params=query)
            if res.status_code != 200:
                return urls
            data = json.loads(res.text)
            for result in data["results"]:
                urls.append(result[what])
        return urls
    
    def remove_folder(self, folder):
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
            
    def create_folder(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)