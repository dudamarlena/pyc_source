# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dynamodb_meta_store/exceptions.py
# Compiled at: 2020-03-21 06:23:49
# Size of source mod 2**32: 367 bytes


class TableNotReadyException(Exception):
    __doc__ = ' Exception thrown if the table is not in ACTIVE or UPDATING state '


class MisconfiguredSchemaException(Exception):
    __doc__ = ' Exception thrown if the table does not match the configuration '


class ItemNotFound(Exception):
    __doc__ = ' Exception thrown if the item does not exist in table '