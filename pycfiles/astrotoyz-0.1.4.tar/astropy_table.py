# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/data-beta/users/fmooleka/git_projects/astro-toyz/astrotoyz/data_types/astropy_table.py
# Compiled at: 2015-08-06 16:42:10
"""
Data Types for astrotoyz
"""
from __future__ import division, print_function
from toyz.utils.sources import DataSource
from toyz.utils.errors import ToyzError

class AstroDataError(ToyzError):
    pass


class AstropyTable(DataSource):

    def __init__(self, *args, **kwargs):
        DataSource.__init__(self, *args, **kwargs)

    def name_columns(self, columns=None):
        print('entered name columns!!!!!!!!!!!!!!!!!!!!!!')
        if columns is not None:
            table_cols = self.data.colnames
            if len(columns) != len(table_cols):
                raise AstroDataError('Number of new columns does not match number of table columns')
            for n, col in enumerate(columns):
                self.data.rename_column(table_cols[n], col)

            self.columns = columns
        else:
            self.columns = self.data.colnames
        return self.data.colnames

    def check_instance(self, data, data_kwargs={}):
        from astropy.table import Table
        if isinstance(data, Table):
            self.data = Table(data, **data_kwargs)
            self.data_type = 'astropy.table.table.Table'
            return True
        return False

    def to_dict(self, columns=None):
        import numpy as np

        def isnan(x):
            if np.isnan(x):
                return 'NaN'
            else:
                return x

        if columns is None:
            columns = self.columns
        data_dict = {col:map(isnan, np.array(self.data[col]).tolist()) for col in columns}
        return data_dict

    def remove_rows(self, points):
        self.data.remove_rows(points)