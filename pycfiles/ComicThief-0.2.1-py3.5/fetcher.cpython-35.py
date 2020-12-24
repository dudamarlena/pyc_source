# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComicThief/fetcher.py
# Compiled at: 2017-02-05 15:00:28
# Size of source mod 2**32: 1630 bytes
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import os
from urllib.parse import urlparse
import requests
from tqdm import tqdm
from .config import WithConfig

class Fetcher(WithConfig):

    def __init__(self):
        super().__init__()
        self.headers = {'user-agent': self.config['SETTINGS'].get('useragent', 'ComicThief')}

    def fetch_comic_list_page(self, service='default'):
        return requests.get(self.config['COMICS_LIST'].get(service))

    def fetch_subpage(self, url):
        return requests.get(url)

    def prepare_ordered_filename(self, remote_path, order):
        file_name = os.path.split(remote_path)[(-1)]
        return '{}.{}'.format(str(order), file_name.split('.')[1])

    def download_image(self, url, local_path, name):
        download_path = Path(local_path, name)
        with download_path.open('wb') as (f):
            f.write(requests.get(url).content)
            return download_path

    def download_images_list(self, local_path, images_list, threads=2):
        local_path.mkdir(parents=True, exist_ok=True)
        pool = ThreadPoolExecutor(threads)
        futures = []
        for order, image_url in enumerate(images_list):
            remote_path = urlparse(image_url).path
            file_name = self.prepare_ordered_filename(remote_path, order)
            futures.append(pool.submit(self.download_image, image_url, local_path, file_name))

        total = len(futures)
        for _ in tqdm(as_completed(futures), total=total):
            pass