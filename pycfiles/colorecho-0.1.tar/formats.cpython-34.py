# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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