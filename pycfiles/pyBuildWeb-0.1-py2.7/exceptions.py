# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pyBuildWeb\_utils\exceptions.py
# Compiled at: 2018-02-16 03:58:40
__author__ = 'rramchandani'

class BuildError(BaseException):
    pass


class BuildNotFound(BaseException):
    pass


class BuildDownloadError(BaseException):
    pass