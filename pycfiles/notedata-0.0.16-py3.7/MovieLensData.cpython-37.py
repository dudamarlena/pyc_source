# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notedata/dataset/MovieLensData.py
# Compiled at: 2019-06-13 02:40:33
# Size of source mod 2**32: 1291 bytes
import logging, os
from ..utils import data_root
from ..utils import download_file
logger = logging.getLogger(__name__)

class MovieLensData:

    def __init__(self, size='1m'):
        self.path_root = data_root + '/data/movielens/'
        if size not in ('1m', '10m', '20m'):
            raise Exception('参数有误，1m,10m,20m')
        self.size = size
        self.zip_name = 'ml-' + size + '.zip'
        self.zip_path = self.path_root + self.zip_name
        self.file_path = self.path_root + 'ml-' + size + '/'
        self.data_users = self.file_path + 'users.dat'
        self.data_movies = self.file_path + 'movies.dat'
        self.data_ratings = self.file_path + 'ratings.dat'

    def download_raw_0(self, overwrite=False):
        download_file(url=('http://files.grouplens.org/datasets/movielens/' + self.zip_name), path=(self.zip_path), overwrite=overwrite)
        cmd1 = 'cd ' + self.path_root + ' && unzip ' + self.zip_name
        os.system(cmd1)

    def init_data(self, overwrite=False):
        self.download_raw_0(overwrite=overwrite)