# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dirstat\walker.py
# Compiled at: 2006-06-19 05:11:36
import os

class walker(object):
    __module__ = __name__

    def __init__(self, path, order=False):
        self._path = path

    def __iter__(self):
        self._result = []
        self._tmpresult = {}
        os.path.walk(self._path, walker.callback, self)
        self._index = len(self._result)
        return self

    def next(self):
        if self._index > 0:
            self._index -= 1
            return self._result[self._index]
        raise StopIteration

    def callback(self, path, files):
        dirs = []
        fileonlys = []
        for file in files:
            if os.path.isdir(os.path.join(path, file)):
                dirs.append(file)
            else:
                fileonlys.append(file)

        self._tmpresult[path] = (
         path, dirs, fileonlys)
        self._result.append((path, dirs, fileonlys))