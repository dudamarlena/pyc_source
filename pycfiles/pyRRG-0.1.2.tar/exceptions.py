# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyrrd\exceptions.py
# Compiled at: 2013-08-12 02:05:53


class PyRRDError(Exception):
    pass


class ExternalCommandError(PyRRDError):
    pass