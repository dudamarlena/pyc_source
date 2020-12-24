# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/antonio/Projects/ipkiss_manager/ipkiss_manager/im_exception.py
# Compiled at: 2013-01-22 06:56:22


class TimeoutError(BaseException):
    pass


class UnsolvableError(BaseException):
    pass


class ReferenceFileError(BaseException):
    pass


class DownloadError(BaseException):
    pass


class ShapelyNotInstalled(BaseException):
    pass


class DependencyError(BaseException):
    pass


class VersionError(BaseException):
    pass


class RemoveError(BaseException):
    """
        Errors on removing IPKISS
    """
    pass


class RemoveByVersionError(RemoveError):
    pass


class RemoveByPathError(RemoveError):
    pass


class PermissionError(BaseException):
    pass


class UnkowIpkissRelease(BaseException):
    pass