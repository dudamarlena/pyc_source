# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/takumakanari/.pyenv/versions/japanese-numbers-py3/lib/python3.8/site-packages/japanese_numbers/result.py
# Compiled at: 2017-12-20 18:27:05
# Size of source mod 2**32: 500 bytes
from __future__ import absolute_import, unicode_literals

class ParsedResult(object):

    def __init__(self, text=None, number=None, type=int, index=-1):
        self.text = text
        self.number = number
        self.type = type
        self.index = index

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<{0} {1[number]} : "{1[text]}" index={1[index]}>'.format(self.__class__.__name__, self.__dict__).encode('utf8')