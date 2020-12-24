# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/ycollections/table.py
# Compiled at: 2016-03-30 08:43:32
import os

def simple_table(row, col, cell_factory):
    """
    Create and return a simple table, like: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [ [ cell_factory(i, j) for j in range(col) ] for i in range(row)
           ]


class BaseTable(object):

    def __init__(self, row, col):
        self.height = row
        self.width = col

    @property
    def rows(self):
        return ([ self[(i, j)] for i in range(self.width) ] for j in range(self.height))

    @property
    def cols(self):
        return ([ self[(i, j)] for i in range(self.height) ] for j in range(self.width))


class Table(BaseTable):

    def __init__(self, row, col, init_val=None):
        self.table = [ [ init_val for j in range(col) ] for i in range(row)
                     ]
        super(Table, self).__init__(row, col)

    def __getitem__(self, idx):
        row, col = idx
        return self.table[row][col]

    def __setitem__(self, idx, val):
        row, col = idx
        self.table[row][col] = val


class SparseTable(BaseTable):

    def __init__(self, row, col, init_val=None):
        self.init_val = init_val
        self.table = {}
        super(SparseTable, self).__init__(row, col)

    def __getitem__(self, idx):
        r, c = idx
        row = self.table.get(r)
        if row is None:
            return self.init_val
        else:
            return row.get(c, self.init_val)

    def __setitem__(self, idx, val):
        r, c = idx
        row = self.table.get(r)
        if row is None:
            row = self.table[r] = {}
        row[c] = val
        return