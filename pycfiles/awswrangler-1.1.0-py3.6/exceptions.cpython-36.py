# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/awswrangler/exceptions.py
# Compiled at: 2020-04-10 10:03:25
# Size of source mod 2**32: 1667 bytes
"""Centralized exceptions Module."""

class InvalidCompression(Exception):
    __doc__ = 'Invalid compression format.'


class InvalidArgumentValue(Exception):
    __doc__ = 'Invalid argument value.'


class InvalidArgumentType(Exception):
    __doc__ = 'Invalid argument type.'


class InvalidArgumentCombination(Exception):
    __doc__ = 'Invalid argument combination.'


class InvalidArgument(Exception):
    __doc__ = 'Invalid argument.'


class UnsupportedType(Exception):
    __doc__ = 'UnsupportedType exception.'


class UndetectedType(Exception):
    __doc__ = 'UndetectedType exception.'


class ServiceApiError(Exception):
    __doc__ = 'ServiceApiError exception.'


class InvalidTable(Exception):
    __doc__ = 'InvalidTable exception.'


class QueryFailed(Exception):
    __doc__ = 'QueryFailed exception.'


class QueryCancelled(Exception):
    __doc__ = 'QueryCancelled exception.'


class AthenaQueryError(Exception):
    __doc__ = 'AthenaQueryError exception.'


class EmptyDataFrame(Exception):
    __doc__ = 'EmptyDataFrame exception.'


class InvalidConnection(Exception):
    __doc__ = 'InvalidConnection exception.'


class InvalidDatabaseType(Exception):
    __doc__ = 'InvalidDatabaseEngine exception.'


class RedshiftLoadError(Exception):
    __doc__ = 'RedshiftLoadError exception.'


class InvalidRedshiftDiststyle(Exception):
    __doc__ = 'InvalidRedshiftDiststyle exception.'


class InvalidRedshiftDistkey(Exception):
    __doc__ = 'InvalidRedshiftDistkey exception.'


class InvalidRedshiftSortstyle(Exception):
    __doc__ = 'InvalidRedshiftSortstyle exception.'


class InvalidRedshiftSortkey(Exception):
    __doc__ = 'InvalidRedshiftSortkey exception.'


class InvalidRedshiftPrimaryKeys(Exception):
    __doc__ = 'InvalidRedshiftPrimaryKeys exception.'