# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pykkelabels\exceptions.py
# Compiled at: 2015-10-29 15:45:36
# Size of source mod 2**32: 228 bytes


class PageError(Exception):

    def __init__(self, message):
        super(PageError, self).__init__(message)


class ConnError(Exception):

    def __init__(self, message):
        super(ConnError, self).__init__(message)