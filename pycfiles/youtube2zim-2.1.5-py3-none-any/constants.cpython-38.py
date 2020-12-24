# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/youtube/youtube2zim/constants.py
# Compiled at: 2020-04-21 13:30:02
# Size of source mod 2**32: 734 bytes
import pathlib, logging
from zimscraperlib.logging import getLogger
ROOT_DIR = pathlib.Path(__file__).parent
NAME = ROOT_DIR.name
with open(ROOT_DIR.joinpath('VERSION'), 'r') as (fh):
    VERSION = fh.read().strip()
ENCODER_VERSION = 'v1'
SCRAPER = f"{NAME} {VERSION}"
CHANNEL = 'channel'
PLAYLIST = 'playlist'
USER = 'user'
logger = getLogger(NAME, level=(logging.DEBUG))

class Youtube(object):

    def __init__(self):
        self.build_dir = None
        self.cache_dir = None
        self.api_key = None

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


YOUTUBE = Youtube()