# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/configmaster/exc.py
# Compiled at: 2015-08-17 15:21:11


class LoaderException(Exception):
    pass


class WriterException(Exception):
    pass


class FiletypeNotSupportedException(Exception):
    pass


class NetworkedFileException(Exception):
    pass