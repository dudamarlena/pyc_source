# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\samples\tetrico\status.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 705 bytes
from __future__ import division, print_function, unicode_literals
__all__ = ['status']

class Status(object):

    def __init__(self):
        self.score = 0
        self.next_piece = None
        self.level = None
        self.level_idx = None
        self.lines = 0
        self.tot_lines = 0

    def reset(self):
        self.score = 0
        self.next_piece = None
        self.level = None
        self.level_idx = None
        self.lines = 0
        self.tot_lines = 0


status = Status()