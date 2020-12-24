# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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