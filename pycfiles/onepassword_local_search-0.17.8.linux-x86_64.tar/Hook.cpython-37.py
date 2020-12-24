# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_local_search/exceptions/Hook.py
# Compiled at: 2019-05-24 16:38:48
# Size of source mod 2**32: 262 bytes
from os import environ
from sys import excepthook, stderr

def exception_handler(exception_type, exception, traceback):
    if environ.get('DEBUG'):
        excepthook(exception_type, exception, traceback)
    else:
        print(('%s' % exception), file=stderr)