# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/models/jdbc/jdbc_column.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 1340 bytes
"""
Created on Feb 8, 2018

@author: stelios
"""
from base.base_column import BaseColumn
import jdbc

class JdbcColumn(BaseColumn):
    __doc__ = '\n    classdocs\n    '

    def __init__(self, jdbc_table, json_object=None, url=None):
        """
        Constructor
        """
        super().__init__(jdbc_table, json_object, url)

    def type(self):
        if self.json_object.get('meta', '') != '':
            if self.json_object.get('meta').get('jdbc', '') != '':
                return self.json_object.get('meta').get('jdbc').get('type', '')

    def size(self):
        if self.json_object.get('meta', '') != '':
            if self.json_object.get('meta').get('adql', '') != '':
                return self.json_object.get('meta').get('jdbc').get('size', '')

    def ucd(self):
        if self.json_object.get('meta', '') != '':
            if self.json_object.get('meta').get('adql', '') != '':
                return self.json_object.get('meta').get('adql').get('ucd', 'test')
        return 'test'

    def utype(self):
        if self.json_object.get('meta', '') != '':
            if self.json_object.get('meta').get('adql', '') != '':
                return self.json_object.get('meta').get('adql').get('utype', '')