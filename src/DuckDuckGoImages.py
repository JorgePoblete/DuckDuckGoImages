import re
import io
import os
import json
import uuid
import shutil
import random
import requests
from PIL import Image
from urllib import parse
import joblib
import contextlib
from tqdm.auto import tqdm


ALL = None
CREATIVE_COMMONS = "Any"
PUBLIC_DOMAIN = "Public"
SHARE_AND_USE = "Share"
SHARE_AND_USE_COMMECIALLY = "ShareCommercially"
MODIFY_SHARE_AND_USE = "Modify"
MODIFY_SHARE_AND_USE_COMMERCIALLY = "ModifyCommercially"

_licenses = [
    ALL,
    CREATIVE_COMMONS,
    PUBLIC_DOMAIN,
    SHARE_AND_USE,
    SHARE_AND_USE_COMMECIALLY,
    MODIFY_SHARE_AND_USE,
    MODIFY_SHARE_AND_USE_COMMERCIALLY
]

@contextlib.contextmanager
def tqdm_parallel(tqdm_object):
    """Context manager to patch joblib to display tqdm progress bar"""

    def tqdm_print_progress(self):
        if self.n_completed_tasks > tqdm_object.n:
            n_completed = self.n_completed_tasks - tqdm_object.n
            tqdm_object.update(n=n_completed)

    original_print_progress = joblib.parallel.Parallel.print_progress
    joblib.parallel.Parallel.print_progress = tqdm_print_progress

    try:
        yield tqdm_object
    finally:
        joblib.parallel.Parallel.print_progress = original_print_progress
        tqdm_object.close()


def download(query, folder='.', max_urls=None, thumbnails=False, parallel=False, shuffle=False, remove_folder=False, license=ALL):
    if thumbnails:
        urls = get_image_thumbnails_urls(query, license)
    else:
        urls = get_image_urls(query, license)

    if shuffle:
        random.shuffle(urls)

    if max_urls is not None and len(urls) > max_urls:
        urls = urls[:max_urls]

    if remove_folder:
        _remove_folder(folder)

    _create_folder(folder)
    if parallel:
        return _parallel_download_urls(urls, folder)
    else:
        return _download_urls(urls, folder)

def _download(url, folder):
        try:
            filename = str(uuid.uuid4().hex)
            while os.path.exists("{}/{}.jpg".format(folder, filename)):
                filename = str(uuid.uuid4().hex)
            response = requests.get(url, stream=True, timeout=5.0, allow_redirects=True)
            with Image.open(io.BytesIO(response.content)) as im:
                with open("{}/{}.jpg".format(folder, filename), 'wb') as out_file:
                    im.save(out_file)
                    return True
        except:
            return False

def _download_urls(urls, folder):
    downloaded = 0
    for url in tqdm(urls):
        if _download(url, folder):
            downloaded += 1
    return downloaded

def _parallel_download_urls(urls, folder):
    downloaded = 0
    with tqdm_parallel(tqdm(total=len(urls))):
        with joblib.Parallel(n_jobs=os.cpu_count()) as parallel:
            results = parallel(joblib.delayed(_download)(url, folder) for url in urls)
            for result in results:
                if result:
                    downloaded += 1
    return downloaded

def get_image_urls(query, license):
    token = _fetch_token(query)
    return _fetch_search_urls(query, token, license)

def get_image_thumbnails_urls(query, license):
    token = _fetch_token(query)
    return _fetch_search_urls(query, token, license, what="thumbnail")

def _fetch_token(query, URL="https://duckduckgo.com/"):
    res = requests.post(URL, data={'q': query})
    if res.status_code != 200:
        return ""
    match = re.search(r"vqd='([\d-]+)'", res.text, re.M|re.I)
    if match is None:
        return ""
    return match.group(1)

def _fetch_search_urls(q, token, license, URL="https://duckduckgo.com/", what="image"):
    query = {
        "vqd": token,
        "q": q,
        "l": "us-en",
        "o": "json",
        "f": ",,,,,",
        "p": "1",
        "s": "100",
        "u": "bing"
    }
    if license is not None and license in _licenses:
        query["f"] = f",,,,,license:{license}"

    urls = []
    _urls, next = _get_urls(f"{URL}i.js", query, what) 
    urls.extend(_urls)
    while next is not None:
        query.update(parse.parse_qs(parse.urlsplit(next).query))
        _urls, next = _get_urls(f"{URL}i.js", query, what) 
        urls.extend(_urls)
    return urls

def _get_urls(URL, query, what):
    urls = []
    res = requests.get(
        URL,
        params=query,
        headers={
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36"
        }
    )
    if res.status_code != 200:
        return urls

    data = json.loads(res.text)
    for result in data["results"]:
        urls.append(result[what])
    return urls, data["next"] if "next" in data else None

def _remove_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)

def _create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
