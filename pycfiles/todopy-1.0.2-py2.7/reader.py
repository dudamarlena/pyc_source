# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\todopy\reader.py
# Compiled at: 2011-12-15 09:19:07
import os.path
from model import Model
import codecs

class FileReader(object):

    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):

        class Iter(object):

            def __init__(self, f):
                self.f = f

            def __iter__(self):
                return self

            def next(self):
                try:
                    return self.f.next().strip()
                except StopIteration:
                    self.f.close()
                    raise StopIteration()

        if os.path.exists(self.filename):
            return Iter(codecs.open(self.filename, mode='r', encoding='utf-8'))
        return iter([])