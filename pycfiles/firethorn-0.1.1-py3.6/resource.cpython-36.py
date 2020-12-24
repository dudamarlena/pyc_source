# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/models/resource.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 2495 bytes
import logging
from models.query import Query
import urllib, json
from models.adql import adql_resource
from models.schema import Schema

class Resource(object):
    __doc__ = '\n    Resource client class\n         \n    Attributes\n    ----------\n      \n    adql_resource: AdqlResource, optional\n        The AdqlResource behind the Resource object\n    \n    url: String, optional\n        A String representing the URL of the resource\n        \n\n    '

    def __init__(self, adql_resource=None, url=None):
        self.url = url
        self._Resource__adql_resource = adql_resource

    def add_schema(self, schema=None, schema_name=None):
        """
        Add a Schema into the resource
        """
        if schema == None:
            schema = self._Resource__adql_resource.select_schema_by_name(schema_name)
        else:
            schema = schema._get_adql_schema()
        self._Resource__adql_resource.import_adql_schema(schema, schema_name)

    def get_schema_by_name(self, schema_name=None):
        """
        Get a copy of the schema by name
        """
        adql_schema = self._Resource__adql_resource.select_schema_by_name(schema_name)
        return Schema(adql_schema=adql_schema)

    def query(self, query='', mode='SYNC'):
        """        
        Run a query on the imported resources
        
        Parameters
        ----------
        query : str, required
            The query string
            
        Returns
        -------
        query : `Query`
            The created Query
        """
        adql_query = self._Resource__adql_resource.create_query(query)
        return Query(adql_query=adql_query, mode=mode)

    def get_schemas(self):
        """Get list of schemas in a resource
        """
        schemas = []
        try:
            adql_schemas = self._Resource__adql_resource.select_schemas()
            for adql_schema in adql_schemas:
                schemas.append(Schema(adql_schema=adql_schema))

        except Exception as e:
            logging.exception(e)

        return schemas

    def get_schema_names(self):
        """Get list of schemas in a resource
        """
        schemas = []
        try:
            adql_schemas = self._Resource__adql_resource.select_schemas()
            schemas = [adql_schema.name() for adql_schema in adql_schemas]
        except Exception as e:
            logging.exception(e)

        return schemas