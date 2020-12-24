# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pyBuildWeb\_utils\exceptions.py
# Compiled at: 2018-02-16 03:58:40
__author__ = 'rramchandani'

class BuildError(BaseException):
    pass


class BuildNotFound(BaseException):
    pass


class BuildDownloadError(BaseException):
    pass