# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/models/base/base_resource.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 531 bytes
"""
Created on Feb 8, 2018

@author: stelios
"""
from base.base_object import BaseObject

class BaseResource(BaseObject):
    __doc__ = '\n    classdocs\n    '

    def __init__(self, account, json_object=None, url=None):
        """
        Constructor    
        """
        super().__init__(account, json_object, url)

    def select_schemas(self):
        pass

    def select_schema_by_ident(self, ident):
        pass

    def select_schema_by_name(self, catalog_name, schema_name):
        pass