# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robin/projects/gap/.venv/lib/python2.7/site-packages/gap/templates/src/config.py
# Compiled at: 2013-10-11 03:16:02
import os
ROOT_PATH = os.path.dirname(__file__)
TEMPLATES_PATH = (
 os.path.join(ROOT_PATH, 'templates'),)
STATIC_PATH = os.path.join(ROOT_PATH, 'static')
STATIC_URL = '/static'
DEFAULT_SETTINGS = {'DEBUG': True}