# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/xwaves_errs.py
# Compiled at: 2007-10-30 16:40:50
"""Errors for reading label (typically speech transcription) files.
"""

class Error(Exception):

    def __init__(self, *x):
        Exception.__init__(self, *x)


class NoSuchFileError(IOError, Error):

    def __init__(self, *x):
        IOError.__init__(self, *x)
        Error.__init__(self, *x)


class BadFileFormatError(Error):

    def __init__(self, *x):
        Error.__init__(self, *x)


class DataError(Error):

    def __init__(self, *x):
        Error.__init__(self, *x)


class DataOutOfOrderError(DataError):

    def __init__(self, *s):
        DataError.__init__(self, *s)