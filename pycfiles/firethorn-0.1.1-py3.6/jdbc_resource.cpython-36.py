# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/models/jdbc/jdbc_resource.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 1355 bytes
"""
Created on Feb 8, 2018

@author: stelios
"""
from base.base_resource import BaseResource
import urllib, config, json, logging, jdbc

class JdbcResource(BaseResource):
    __doc__ = '\n    classdocs\n    '

    def __init__(self, account, json_object=None, url=None):
        """
        Constructor    
        """
        super().__init__(account, json_object, url)

    def select_schemas(self):
        schema_list = []
        json_list = self.get_json(self.url + '/schemas/select')
        for schema in json_list:
            schema_list.append(jdbc.JdbcSchema(json_object=schema, jdbc_resource=self))

        return schema_list

    def select_schema_by_ident(self, ident):
        return jdbc.JdbcSchema(url=ident, jdbc_resource=self)

    def select_schema_by_name(self, catalog_name, schema_name):
        response_json = {}
        try:
            response_json = self.get_json(self.url + '/schemas/select', {config.jdbc_schema_catalog: catalog_name, config.jdbc_schema_schema: schema_name})
        except Exception as e:
            logging.exception(e)

        return jdbc.JdbcSchema(json_object=response_json, jdbc_resource=self)

    def create_schema(self, catalog_name, schema_name):
        pass