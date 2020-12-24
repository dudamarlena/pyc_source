# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/bookshelf/api_v2/logging_helpers.py
# Compiled at: 2016-08-21 18:37:21
# Size of source mod 2**32: 175 bytes
from fabric.colors import green, yellow, red

def log_green(msg):
    print(green(msg))


def log_yellow(msg):
    print(yellow(msg))


def log_red(msg):
    print(red(msg))