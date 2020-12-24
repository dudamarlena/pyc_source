# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\xh\Documents\PyCharmProjects\page_screenshot\page_screenshot\config\setting.py
# Compiled at: 2019-06-25 23:08:30
# Size of source mod 2**32: 1615 bytes
import logging
LOG_LEVEL = logging.INFO
DEFAULT_IMG_SUFFIX = '.png'
TIMESTAMP_WITH_FOLDER = True
URL = 'http://huaban.com/'
IMG_SAVE_PATH = 'C:/page_screenshot'
BASE_HEIGHT = 900
SCALE_HEIGHT = 1.25
TIME_MS_SCROLL_FAST = 600
TIME_MS_SCROLL_SLOW = 900
CHROME_DRIVER_PATH = 'C:/opt/exe/chromedriver.exe'
INIT_WINDOW_POSITION_X = 800
INIT_WINDOW_POSITION_Y = 0
JS_FILE_NAME = 'return nickname + "-" + msg_title'
JS_MD5_URL = 'return md5(window.location.href)'
INIT_HEIGHT = 500
OUTER_PC_WIDTH = 1273
OUTER_PHONE_WIDTH = 643
JS_MAX_HEIGHT = '\nreturn\nMath.max(document.body.scrollHeight, document.body.offsetHeight\n, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);\n'.replace('\n', ' ')
JS_MAX_WIDTH = '\nreturn\nMath.min(document.body.scrollWidth, document.body.offsetWidth\n, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);\n'.replace('\n', ' ')
JS_WINDOW_HEIGHT = 'return document.documentElement.clientHeight'
JS_SCROLL = 'setTimeout(function(){ window.scrollTo(0, %s); }, %s);'

def init():
    """
    初始化

    :return: void
    """
    logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='[%Y-%M-%d %H:%M:%S]')


init()