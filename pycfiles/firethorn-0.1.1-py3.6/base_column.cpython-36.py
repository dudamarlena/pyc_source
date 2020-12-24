# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/models/base/base_column.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 1709 bytes
"""
Created on Feb 8, 2018

@author: stelios
"""
from base.base_object import BaseObject

class BaseColumn(BaseObject):
    __doc__ = '\n    classdocs\n    '

    def __init__(self, parent, json_object=None, url=None):
        """
        Constructor
        """
        self.parent = parent
        super().__init__(parent.account, json_object, url)

    def resource(self):
        if self.json_object != None:
            return self.table().resource()
        else:
            return

    def schema(self):
        if self.json_object != None:
            return self.table().schema()
        else:
            return

    def table(self):
        return self.parent

    def type(self):
        if self.json_object.get('meta', '') != '':
            if self.json_object.get('meta').get('jdbc', '') != '':
                return self.json_object.get('meta').get('jdbc').get('type', '')

    def arraysize(self):
        if self.json_object.get('meta', '') != '':
            if self.json_object.get('meta').get('adql', '') != '':
                return self.json_object.get('meta').get('adql').get('arraysize', '')

    def ucd(self):
        if self.json_object.get('meta', '') != '':
            if self.json_object.get('meta').get('adql', '') != '':
                return self.json_object.get('meta').get('adql').get('ucd', '')
        return ''

    def utype(self):
        if self.json_object.get('meta', '') != '':
            if self.json_object.get('meta').get('adql', '') != '':
                return self.json_object.get('meta').get('adql').get('utype', '')