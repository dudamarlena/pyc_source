# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apacheconfig/reader.py
# Compiled at: 2020-01-09 16:01:59
import io, os

class LocalHostReader(object):

    def __init__(self):
        self._os = os
        self._environ = self._os.environ
        self._path = self._os.path

    @property
    def environ(self):
        return self._environ

    def exists(self, filepath):
        return self._path.exists(filepath)

    def isdir(self, filepath):
        return self._path.isdir(filepath)

    def listdir(self, filepath):
        return self._os.listdir(filepath)

    def open(self, filename, mode='r', encoding='utf-8', bufsize=-1):
        return io.open(filename, mode, bufsize, encoding=encoding)