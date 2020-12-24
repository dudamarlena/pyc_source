# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/douban_client/api/music.py
# Compiled at: 2013-12-18 08:08:58
from .subject import Subject

class Music(Subject):
    target = 'music'

    def __repr__(self):
        return '<DoubanAPI Music>'