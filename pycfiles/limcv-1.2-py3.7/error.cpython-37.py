# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/limcv/error.py
# Compiled at: 2019-12-11 09:22:26
# Size of source mod 2**32: 1217 bytes
"""
Declaration:
    Define all BaseError Classes used in aircv.
"""

class BaseError(Exception):
    __doc__ = 'Base class for exceptions in this module.'

    def __init__(self, message=''):
        self.message = message

    def __repr__(self):
        return repr(self.message)


class FileNotExistError(BaseError):
    __doc__ = 'Image does not exist.'


class TemplateInputError(BaseError):
    __doc__ = 'Resolution input is not right.'


class NoSIFTModuleError(BaseError):
    __doc__ = 'Resolution input is not right.'


class NoSiftMatchPointError(BaseError):
    __doc__ = 'Exception raised for errors 0 sift points found in the input images.'


class SiftResultCheckError(BaseError):
    __doc__ = 'Exception raised for errors 0 sift points found in the input images.'


class HomographyError(BaseError):
    __doc__ = 'In homography, find no mask, should kill points which is duplicate.'


class NoModuleError(BaseError):
    __doc__ = 'Resolution input is not right.'


class NoMatchPointError(BaseError):
    __doc__ = 'Exception raised for errors 0 keypoint found in the input images.'


class MatchResultCheckError(BaseError):
    __doc__ = 'Exception raised for errors 0 keypoint found in the input images.'