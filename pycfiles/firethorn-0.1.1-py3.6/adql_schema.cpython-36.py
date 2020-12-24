# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/models/adql/adql_schema.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 1905 bytes
"""
Created on Feb 8, 2018

@author: stelios
"""
from base.base_schema import BaseSchema
import adql, logging
from adql import adql_resource

class AdqlSchema(BaseSchema):
    __doc__ = '\n    classdocs\n    '

    def __init__(self, adql_resource, json_object=None, url=None):
        """
        Constructor
        """
        super().__init__(adql_resource, json_object, url)

    def select_tables(self):
        table_list = []
        json_list = self.get_json(self.json_object.get('tables', ''))
        for table in json_list:
            table_list.append(adql.AdqlTable(json_object=table, adql_schema=self))

        return table_list

    def select_table_by_ident(self, ident):
        return adql.AdqlTable(adql_schema=self, url=ident)

    def select_table_by_name(self, table_name):
        """Get table by name
        
        Parameters
        ----------
        table_name: string, required
            The name of the Table being searched
         
        Returns
        -------
        table_list: list
            List of table names
        """
        response_json = {}
        try:
            response_json = self.get_json(self.url + '/tables/select', {'adql.table.name': table_name})
        except Exception as e:
            logging.exception(e)

        return adql.AdqlTable(json_object=response_json, adql_schema=self)

    def create_table(self, table_name):
        pass

    def import_ivoa_table(self, IvoaTable, table_name=None):
        pass

    def import_jdbc_table(self, JdbcTable, table_name=None):
        pass

    def import_adql_table(self, AdqlTable, table_name=None):
        pass

    def create_adql_table(self, table_name=None):
        pass