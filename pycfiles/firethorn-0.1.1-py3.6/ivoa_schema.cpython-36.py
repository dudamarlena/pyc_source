# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/models/ivoa/ivoa_schema.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 1298 bytes
"""
Created on Feb 8, 2018

@author: stelios
"""
try:
    from base.base_schema import BaseSchema
    import ivoa, json, config, logging, urllib.request
except Exception as e:
    logging.exception(e)

class IvoaSchema(BaseSchema):
    __doc__ = '\n    classdocs\n    '

    def __init__(self, ivoa_resource, json_object=None, url=None):
        """
        Constructor
        """
        super().__init__(ivoa_resource, json_object, url)

    def select_tables(self):
        table_list = []
        json_list = self.get_json(self.json_object.get('tables', ''))
        for table in json_list:
            table_list.append(ivoa.IvoaTable(json_object=table, ivoa_schema=self))

        return table_list

    def select_table_by_ident(self, ident):
        return ivoa.IvoaTable(url=ident, ivoa_schema=self)

    def select_table_by_name(self, table_name):
        response_json = {}
        try:
            response_json = self.get_json(self.url + '/tables/select', {config.ivoa_table_select_by_name_param: table_name})
        except Exception as e:
            logging.exception(e)

        return ivoa.IvoaTable(json_object=response_json, ivoa_schema=self)