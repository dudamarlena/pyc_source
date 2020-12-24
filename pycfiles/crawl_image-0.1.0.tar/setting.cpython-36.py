# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\xh\Documents\github-xh\crawl_image\crawl_image\config\setting.py
# Compiled at: 2019-06-12 04:44:40
# Size of source mod 2**32: 538 bytes
import logging
LOG_LEVEL = logging.INFO
DO_MULTI = True
TIMESTAMP_WITH_FOLDER = True
URL = 'http://huaban.com/'
IMG_SAVE_PATH = 'D:/crawl/image'
DEFAULT_IMG_SUFFIX = 'jpg'
IMG_INCLUDE_SUFFIX = ['png', 'jpg']
IMG_EXCLUDE_SUFFIX = ['gif']

def init():
    logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='[%Y-%M-%d %H:%M:%S]')


init()