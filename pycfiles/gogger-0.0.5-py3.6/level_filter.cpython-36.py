# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/gogger/level_filter.py
# Compiled at: 2018-11-20 23:27:50
# Size of source mod 2**32: 165 bytes


class LevelFilter(object):

    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level