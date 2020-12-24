# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/any2/exceptions.py
# Compiled at: 2015-07-28 10:41:14


class Any2Error(Exception):
    pass


class ColumnMappingError(Any2Error):
    pass


class TransformationError(Any2Error):
    pass