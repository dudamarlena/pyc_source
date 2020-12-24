# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ojcrawler/crawlers/config.py
# Compiled at: 2018-12-27 10:28:29
from __future__ import absolute_import, division, print_function
from logging.handlers import RotatingFileHandler
import os
from six.moves import urllib
import logging
logFile = 'crawler.log'
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5242880, backupCount=2, encoding=None, delay=0)
formatter = logging.Formatter('%(name)s: %(asctime)s [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s')
my_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s', datefmt='%m-%d %H:%M', filename='judge.log', filemode='w')
logging.getLogger('').addHandler(my_handler)
DEBUG = True
if DEBUG:
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
logger = logging
HTTP_METHOD_TIMEOUT = os.getenv('HTTP_METHOD_TIMEOUT', 10)
RESULT_COUNT = os.getenv('RESULT_COUNT', 20)
RESULT_INTERVAL = os.getenv('RESULT_INTERVAL', 2)
STATIC_OJ_ROOT = os.getenv('STATIC_OJ_ROOT', '/home/')
STATIC_OJ_URL = os.getenv('STATIC_OJ_URL', 'localhost:8000/statics/')

def save_image(image_url, oj_name):
    file_name = image_url.split('/')[(-1)]
    image_folder = os.path.join(STATIC_OJ_ROOT, oj_name)
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    path = os.path.join(image_folder, file_name)
    if os.path.exists(path):
        return STATIC_OJ_URL + oj_name + '/' + file_name
    req = urllib.request.Request(image_url)
    resp = urllib.request.urlopen(req)
    data = resp.read()
    with open(path, 'wb') as (fp):
        fp.write(data)
    return STATIC_OJ_URL + oj_name + '/' + file_name