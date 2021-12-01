
 ## DuckDuckGoImages

## Instalation

To install run the following:

```python
pip install DuckDuckGoImages
```

## Usage

import using the following:

```python
import DuckDuckGoImages as ddg
```

and then you can search and download images from DuckDuckGo using:

```python
ddg.download('kittens')
```

The above command will search for the query phrase `kittens`, and then will try to download the list of image urls into the current folder.

Each downloaded image will have a randomic UUIDv4 name.

## Options

When downloading images you can pass `download` the next list of parameters to achieve different results:

- `folder`: The path where the downloaded images are saved. Default is current directory.
- `max_urls`: If set to a number, then only that amount of images will be downloaded. Note that the available images to download could be less than `max_urls`. Default `None`, so all search results will try to be downloaded.
- `thumbnails`: If set to `True`, the image thumbnails will be downloaded instead of the actual image. This should avoid broken links, but it will also download a smaller image in most cases. Default `None`.
- `parallel`: If set to true, then N jobs will be created to download the list of images faster, the number of jobs is the number of cpu procesors on the machine. Default `False`.
- `shuffle`: If set to true, the list of images will be shuffled randomly before download. Default `False`.
- `remove_folder`: If set to true, then the folder where the images will be downloaded is deleted before the download. Default `False`.
- `licence`: If set to a value the result search will only retrieve images that have the specified licence. Usable values are defined as constants inside the package, so for use you should do something like `ddg.download('kittens', licence=ddg.ALL)`, valid licence types are:
    - ALL: retrieve all images, this is the default behaviour.
    - CREATIVE_COMMONS: This will only retrieve images that have the Creative Commons licence.
    - PUBLIC_DOMAIN: This will only retrieve images that are on the public domain.
    - SHARE_AND_USE: This will only retrieve images that can be shared and used.
    - SHARE_AND_USE_COMMECIALLY: This will only retrieve images that can be shared and used commercially. 
    - MODIFY_SHARE_AND_USE: This will only retrieve images that can be modified, shared and used.
    - MODIFY_SHARE_AND_USE_COMMERCIALLY: This will only retrieve images that can be modified, shared and used commercially.

