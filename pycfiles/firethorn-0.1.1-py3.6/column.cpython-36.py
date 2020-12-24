# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/models/column.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 639 bytes
"""
Created on Nov 4, 2017

@author: stelios
"""

class Column(object):
    __doc__ = 'Column class, equivalent to a Firethorn ADQL Column\n    '

    def __init__(self, adql_column=None):
        self._Column__adql_column = adql_column

    def name(self):
        return self._Column__adql_column.name()

    def type(self):
        return self._Column__adql_column.type()

    def ucd(self):
        return self._Column__adql_column.ucd()

    def utype(self):
        return self._Column__adql_column.utype()

    def __str__(self):
        """Get class as string
        """
        return self._Column__adql_column