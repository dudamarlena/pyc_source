# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/qal/sql/base.py
# Compiled at: 2015-04-06 11:45:43
# Size of source mod 2**32: 2393 bytes
"""
Created on Sep 12, 2013

@author: Nicklas Boerjesson
"""
from qal.sql.types import DEFAULT_ROWSEP

class ParameterBase(object):
    __doc__ = 'This class is a base class for all parameter classes.'
    row_separator = DEFAULT_ROWSEP
    _parent = None
    _base_path = None

    def __init__(self, _row_separator=None):
        super(ParameterBase, self).__init__()
        if _row_separator is not None:
            self.row_separator = _row_separator

    def _generate_sql(self, _db_type):
        """Generate SQL for specified database engine"""
        raise Exception(self.__class__.__name__ + '._generate_sql() is not implemented')

    def as_sql(self, _db_type):
        if hasattr(self, 'resource_uuid') and self.resource_uuid and self._check_need_prepare():
            return self._bring_into_context()
        else:
            return self._generate_sql(_db_type)


class SqlList(list):
    __doc__ = 'This is the base class for lists of class instances.'

    def __init__(self, _itemclasses=None):
        super(SqlList, self).__init__()
        if _itemclasses is not None:
            self._itemclasses = _itemclasses

    def as_sql(self, _db_type):
        """Generate SQL for specified database engine"""
        result = ''
        for _item in self:
            if hasattr(_item, 'as_sql'):
                result += _item.as_sql(_db_type)
            else:
                result += _item

        return result


class ParameterExpressionItem(ParameterBase):
    __doc__ = 'The superclass of all classes that can be considered part of an expression'
    operator = 'C'

    def __init__(self, _operator=None):
        super(ParameterExpressionItem, self).__init__()
        if _operator is not None:
            self.operator = _operator
        else:
            self.operator = 'C'