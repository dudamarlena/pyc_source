# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/schemamanager.py
# Compiled at: 2007-12-02 16:26:58
from salamoia.h2o.decorators import lazymethod
__all__ = ['SchemaManager']

class SchemaManager(object):
    """
    The schema manager keeps track of registered schemas
    """
    __module__ = __name__

    @classmethod
    @lazymethod
    def defaultManager(cls):
        """
        Returns the global bundle manager
        """
        return SchemaManager()

    def __init__(self):
        self.schemaByName = {}

    def registerSchemaDescription(self, schema):
        """
        """
        self.schemaByName[schema.name] = schema

    def schemaDescriptionNamed(self, name):
        return self.schemaByName[name]


from salamoia.tests import *
runDocTests()