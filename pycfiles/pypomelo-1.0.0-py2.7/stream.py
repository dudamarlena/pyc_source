# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pypomelo/stream.py
# Compiled at: 2019-01-04 00:02:34
from __future__ import absolute_import, division, print_function, with_statement
import struct

class Stream(object):

    def __init__(self, data=''):
        self.index = 0
        self.data = data
        self.size = len(self.data)

    def tell(self):
        return self.index

    def seek(self, seek):
        seek = max(0, seek)
        self.index = min(self.size, seek)

    def read(self, size=None):
        if self.size <= self.index:
            return ''
        else:
            if size is None:
                size = self.size - self.index
            start = self.index
            end = min(self.size, self.index + size)
            self.index = end
            return self.data[start:end]

    def write(self, data):
        self.data += data
        self.size = len(self.data)

    def getvalue(self):
        return self.data