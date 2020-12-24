# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/exceptions.py
# Compiled at: 2019-07-09 17:30:28
# Size of source mod 2**32: 1033 bytes


class ArcticException(Exception):
    pass


class NoDataFoundException(ArcticException):
    pass


class UnhandledDtypeException(ArcticException):
    pass


class LibraryNotFoundException(ArcticException):
    pass


class DuplicateSnapshotException(ArcticException):
    pass


class StoreNotInitializedException(ArcticException):
    pass


class OptimisticLockException(ArcticException):
    pass


class QuotaExceededException(ArcticException):
    pass


class UnsupportedPickleStoreVersion(ArcticException):
    pass


class DataIntegrityException(ArcticException):
    __doc__ = '\n    Base class for data integrity issues.\n    '


class ArcticSerializationException(ArcticException):
    pass


class ConcurrentModificationException(DataIntegrityException):
    pass


class UnorderedDataException(DataIntegrityException):
    pass


class OverlappingDataException(DataIntegrityException):
    pass


class AsyncArcticException(ArcticException):
    pass


class RequestDurationException(AsyncArcticException):
    pass