# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/models/table.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 1839 bytes
"""
Created on Nov 4, 2017

@author: stelios
"""
try:
    import simplejson as json
except ImportError:
    import json

import warnings
from models.column import Column
from astropy.utils.exceptions import AstropyWarning
warnings.simplefilter('ignore', category=AstropyWarning)

class Table(object):
    __doc__ = 'Table class, equivalent to a Firethorn ADQL Table\n    '

    def __init__(self, adql_table=None):
        self._Table__adql_table = adql_table

    def name(self):
        return self._Table__adql_table.name()

    def get_column_names(self):
        adql_columns = self._Table__adql_table.select_columns()
        column_name_list = [col.name() for col in adql_columns]
        return column_name_list

    def get_columns(self):
        adql_columns = self._Table__adql_table.select_columns()
        column_list = [Column(col) for col in adql_columns]
        return column_list

    def get_column_by_name(self, name):
        return Column(self._Table__adql_table.select_column_by_name(name))

    def as_astropy(self, limit=True):
        """Get Astropy table
                             
        Returns
        -------
        astropy_table: Astropy.Table
            Table as Astropy table 
        """
        if self._Table__adql_table != None:
            return self._Table__adql_table.as_astropy()
        else:
            return

    def rowcount(self):
        """Get Row count
        
        Returns
        -------
        rowcount: integer
            Count of rows  
        """
        if self._Table__adql_table != None:
            return self._Table__adql_table.count()
        else:
            return

    def __str__(self):
        """Get class as string
        """
        return self._Table__adql_table