# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pykkelabels\exceptions.py
# Compiled at: 2015-10-29 15:45:36
# Size of source mod 2**32: 228 bytes


class PageError(Exception):

    def __init__(self, message):
        super(PageError, self).__init__(message)


class ConnError(Exception):

    def __init__(self, message):
        super(ConnError, self).__init__(message)