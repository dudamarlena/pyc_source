# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/douban_client/api/guess.py
# Compiled at: 2013-12-18 08:08:58
from .base import DoubanAPIBase, DEFAULT_START, DEFAULT_COUNT

class Guess(DoubanAPIBase):

    def __repr__(self):
        return '<DoubanAPI Guess>'