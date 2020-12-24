# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/models/base/base_schema.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 854 bytes
"""
Created on Feb 8, 2018

@author: stelios
"""
from base.base_object import BaseObject

class BaseSchema(BaseObject):
    __doc__ = '\n    classdocs\n    '

    def __init__(self, parent, json_object=None, url=None):
        """
        Constructor
        """
        self.parent = parent
        super().__init__(parent.account, json_object, url)

    def resource(self):
        return self.parent

    def name(self):
        return self.schema_name()

    def schema_name(self):
        if self.json_object != None:
            return self.json_object.get('fullname', '')
        else:
            return

    def select_tables(self):
        pass

    def select_table_by_ident(self, ident):
        pass

    def select_table_by_name(self, table_name):
        pass