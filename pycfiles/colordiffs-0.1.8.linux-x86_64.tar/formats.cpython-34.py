# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/.virtualenvs/temp3/lib/python3.4/site-packages/colordiffs/formats.py
# Compiled at: 2015-06-20 22:17:55
# Size of source mod 2**32: 238 bytes
from pygments.console import ansiformat

def green_bg(text):
    return ansiformat('green', text)


def red_bg(text):
    return ansiformat('red', text)


def discreet(text):
    return ansiformat('faint', ansiformat('lightgray', text))