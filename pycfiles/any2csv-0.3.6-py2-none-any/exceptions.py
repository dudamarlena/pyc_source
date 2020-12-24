# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/any2/exceptions.py
# Compiled at: 2015-07-28 10:41:14


class Any2Error(Exception):
    pass


class ColumnMappingError(Any2Error):
    pass


class TransformationError(Any2Error):
    pass