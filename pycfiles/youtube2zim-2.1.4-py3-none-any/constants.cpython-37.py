# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/youtube/youtube2zim/constants.py
# Compiled at: 2019-09-02 05:49:49
# Size of source mod 2**32: 672 bytes
import pathlib, logging
NAME = pathlib.Path(__file__).parent.name
VERSION = '2.0'
SCRAPER = f"{NAME} {VERSION}"
CHANNEL = 'channel'
PLAYLIST = 'playlist'
USER = 'user'
ROOT_DIR = pathlib.Path(__file__).parent
logging.basicConfig(format='%(levelname)s:%(message)s')
logger = logging.getLogger('youtube-scraper')

class Youtube(object):

    def __init__(self):
        self.build_dir = None
        self.cache_dir = None
        self.api_key = None

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


YOUTUBE = Youtube()