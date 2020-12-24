# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/img_downloader.py
# Compiled at: 2020-04-18 14:24:17
# Size of source mod 2**32: 1982 bytes
import requests, os
from tqdm import tqdm
from urllib.parse import urlparse
try:
    from bs4 import BeautifulSoup as bs
except ImportError:
    raise Exception('Please install bs4 package')
else:

    def is_valid(url):
        """
    Checks whether `url` is a valid URL.
    """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)


    def get_all_images(url):
        """
    Returns all image URLs on a single `url`
    """
        soup = bs(requests.get(url).content, 'html.parser')
        filenames = [x.attrs.get('href') for x in soup.find_all('a') if x.attrs.get('href').__contains__('bmp')]
        urls = [os.path.join(url, filename) for filename in filenames]
        return urls


    def download_file(url, pathname):
        """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
        if not os.path.isdir(pathname):
            os.makedirs(pathname)
        response = requests.get(url, stream=True)
        file_size = int(response.headers.get('Content-Length', 0))
        filename = os.path.join(pathname, url.split('/')[(-1)])
        progress = tqdm((response.iter_content(1024)), f"Downloading {filename}", total=file_size, unit='B', unit_scale=True, unit_divisor=1024)
        with open(filename, 'wb') as (f):
            for data in progress:
                f.write(data)
                progress.update(len(data))


    def download_stack(url, path):
        imgs = get_all_images(url)
        for img in imgs:
            download_file(img, path)


    if __name__ == '__main__':
        download_stack('https://www.math.purdue.edu/~lucier/PHOTO_CD/BMP_IMAGES/', os.path.join(os.getcwd(), 'data'))