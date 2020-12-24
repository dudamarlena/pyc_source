# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/models/schema.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 1102 bytes
"""
Created on Nov 4, 2017

@author: stelios
"""
import models
from models.table import Table

class Schema(object):
    __doc__ = 'Column class, equivalent to a Firethorn ADQL Column\n    '

    def __init__(self, adql_schema=None):
        self._Schema__adql_schema = adql_schema

    def _get_adql_schema(self):
        return self._Schema__adql_schema

    def name(self):
        return self._Schema__adql_schema.name()

    def get_table_names(self):
        adql_tables = self._Schema__adql_schema.select_tables()
        table_name_list = [table.name() for table in adql_tables]
        return table_name_list

    def get_tables(self):
        adql_tables = self._Schema__adql_schema.select_tables()
        table_list = [Table(table) for table in adql_tables]
        return table_list

    def get_table_by_name(self, name):
        return models.table.Table(self._Schema__adql_schema.select_table_by_name(name))

    def __str__(self):
        """Get class as string
        """
        return self._Schema__adql_schema