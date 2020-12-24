# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """DataIntegrityException"""
    pass


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