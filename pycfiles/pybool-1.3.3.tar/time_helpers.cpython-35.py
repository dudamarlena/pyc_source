# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.5/site-packages/bookshelf/api_v2/time_helpers.py
# Compiled at: 2016-08-21 18:37:21
# Size of source mod 2**32: 132 bytes
from time import sleep

def sleep_for_one_minute():
    sleep(60)