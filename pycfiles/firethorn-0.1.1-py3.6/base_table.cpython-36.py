# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/models/base/base_table.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 622 bytes
"""
Created on Feb 8, 2018

@author: stelios
"""
from base.base_object import BaseObject

class BaseTable(BaseObject):
    __doc__ = '\n    classdocs\n    '

    def __init__(self, parent, json_object=None, url=None):
        """
        Constructor
        """
        self.parent = parent
        super().__init__(account=(self.parent.account), json_object=json_object, url=url)

    def resource(self):
        return self.parent.resource()

    def schema(self):
        return self.parent

    def select_columns(self):
        return self.get_json(self.json_object.get('columns', ''))