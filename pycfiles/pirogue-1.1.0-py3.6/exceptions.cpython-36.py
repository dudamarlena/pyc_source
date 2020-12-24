# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pirogue/exceptions.py
# Compiled at: 2019-11-29 08:49:00
# Size of source mod 2**32: 300 bytes


class TableHasNoPrimaryKey(Exception):
    pass


class NoReferenceFound(Exception):
    pass


class InvalidSkipColumns(Exception):
    pass


class VariableError(Exception):
    pass


class InvalidDefinition(Exception):
    pass


class InvalidColumn(Exception):
    pass