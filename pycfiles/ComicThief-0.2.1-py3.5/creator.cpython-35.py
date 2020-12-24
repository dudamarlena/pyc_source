# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComicThief/creator.py
# Compiled at: 2017-02-05 15:39:49
# Size of source mod 2**32: 1113 bytes
from pathlib import Path
import os
from zipfile import ZipFile
from .config import WithConfig

def name_fits(search_phrase, key):
    if key:
        return search_phrase.lower() in key.lower()


class Creator(WithConfig):

    def create(self):
        raise NotImplementedError

    def make_comics_dict(self, hrefs):
        return {item.text:item.attrib.get('href') for item in hrefs}

    def search_comics_dict(self, search_phrase, comics_dict):
        return {key:value for key, value in comics_dict.items() if name_fits(search_phrase, key)}

    def exact_search_comics_dict(self, search_phrase, comics_dict):
        return {key:value for key, value in comics_dict.items() if search_phrase == key}


class CreatorCbz(Creator):

    def zip_directory(self, path, img_dir, name):
        with ZipFile(str(Path(path, '{}.cbz'.format(name))), 'w') as (zip_file):
            for file in os.listdir(str(Path(path, img_dir))):
                zip_file.write(str(Path(path, img_dir, file)))

    def create(self, path, img_dir, name):
        self.zip_directory(path, img_dir, name)