# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/qal/dataset/matrix.py
# Compiled at: 2016-04-12 13:41:36
# Size of source mod 2**32: 2805 bytes
"""
Created on Jan 8, 2012

@author: Nicklas Boerjesson
"""
from datetime import date
from qal.dal.types import DB_DB2, DB_ORACLE, DB_POSTGRESQL
from qal.sql.utils import db_specific_object_reference
from qal.dataset.custom import CustomDataset

class MatrixDataset(CustomDataset):
    __doc__ = 'The matrix dataset holds a two-dimensional array of data'

    def __init__(self):
        """
        Constructor
        """
        super(MatrixDataset, self).__init__()

    def load(self):
        """Load data. Not implemented as it is not needed in the matrix descendant"""
        pass

    def save(self):
        """Save data. Not implemented as it is not needed in the matrix descendant"""
        pass

    def as_sql(self, _db_type):
        """Generate SQL"""
        _result = []
        _add_field_names = len(self.data_table) > 0 and len(self.field_names) == len(self.data_table[0])
        for _row in self.data_table:
            _curr_row = []
            for _col_idx in range(len(_row)):
                _str_col = ''
                _col = _row[_col_idx]
                if _col is None:
                    _str_col = 'NULL'
                else:
                    if isinstance(_col, bool):
                        if _col is True:
                            if _db_type == DB_POSTGRESQL:
                                _str_col = 'TRUE'
                            else:
                                _str_col = "'1'"
                        elif _col is False:
                            if _db_type == DB_POSTGRESQL:
                                _str_col = 'FALSE'
                            else:
                                _str_col = "'0'"
                    else:
                        if isinstance(_col, int) or isinstance(_col, float):
                            _str_col = str(_col)
                        else:
                            if isinstance(_col, date) or isinstance(_col, date):
                                _str_col = "'" + _col.isoformat() + "'"
                            else:
                                _str_col = "'" + str(_col) + "'"
                if _add_field_names:
                    _curr_row.append(_str_col + ' AS ' + db_specific_object_reference(self.field_names[_col_idx], _db_type))
                else:
                    _curr_row.append(_str_col)

            _add_field_names = False
            if _db_type == DB_DB2:
                _result.append('SELECT ' + ','.join(_curr_row) + ' FROM sysibm.sysdummy1')
            else:
                if _db_type == DB_ORACLE:
                    _result.append('SELECT ' + ','.join(_curr_row) + ' FROM DUAL')
                else:
                    _result.append('SELECT ' + ','.join(_curr_row))

        return str('\nUNION\n'.join(_result))