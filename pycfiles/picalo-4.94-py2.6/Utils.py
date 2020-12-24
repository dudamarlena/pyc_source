# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/lib/pyExcelerator/Utils.py
# Compiled at: 2008-03-17 12:58:00
"""pyXLWriter.utilites

Utilities for work with reference to cells

"""
__rev_id__ = '$Id: Utils.py,v 1.1 2005/08/11 08:53:48 rvk Exp $'
import re
from struct import pack
from ExcelMagic import MAX_ROW, MAX_COL
_re_cell_ex = re.compile('(\\$?)([A-I]?[A-Z])(\\$?)(\\d+)')
_re_row_range = re.compile('\\$?(\\d+):\\$?(\\d+)')
_re_col_range = re.compile('\\$?([A-I]?[A-Z]):\\$?([A-I]?[A-Z])')
_re_cell_range = re.compile('\\$?([A-I]?[A-Z]\\$?\\d+):\\$?([A-I]?[A-Z]\\$?\\d+)')
_re_cell_ref = re.compile('\\$?([A-I]?[A-Z]\\$?\\d+)')

def col_by_name(colname):
    """
    """
    col = 0
    pow = 1
    for i in xrange(len(colname) - 1, -1, -1):
        ch = colname[i]
        col += (ord(ch) - ord('A') + 1) * pow
        pow *= 26

    return col - 1


def cell_to_rowcol(cell):
    """Convert an Excel cell reference string in A1 notation
    to numeric row/col notation.
  
    Returns: row, col, row_abs, col_abs
 
    """
    m = _re_cell_ex.match(cell)
    if not m:
        raise Exception('Error in cell format')
    (col_abs, col, row_abs, row) = m.groups()
    row_abs = bool(row_abs)
    col_abs = bool(col_abs)
    row = int(row) - 1
    col = col_by_name(col)
    return (row, col, row_abs, col_abs)


def cell_to_rowcol2(cell):
    """Convert an Excel cell reference string in A1 notation
    to numeric row/col notation.
  
    Returns: row, col
    
    """
    m = _re_cell_ex.match(cell)
    if not m:
        raise Exception('Error in cell format')
    (col_abs, col, row_abs, row) = m.groups()
    row = int(row) - 1
    col = col_by_name(col)
    return (row, col)


def rowcol_to_cell(row, col, row_abs=False, col_abs=False):
    """Convert numeric row/col notation to an Excel cell reference string in
    A1 notation.
 
    """
    d = col // 26
    m = col % 26
    chr1 = ''
    if row_abs:
        row_abs = '$'
    else:
        row_abs = ''
    if col_abs:
        col_abs = '$'
    else:
        col_abs = ''
    if d > 0:
        chr1 = chr(ord('A') + d - 1)
    chr2 = chr(ord('A') + m)
    return col_abs + chr1 + chr2 + row_abs + str(row + 1)


def cellrange_to_rowcol_pair(cellrange):
    """Convert cell range string in A1 notation to numeric row/col 
    pair.

    Returns: row1, col1, row2, col2
    
    """
    cellrange = cellrange.upper()
    res = _re_row_range.match(cellrange)
    if res:
        row1 = int(res.group(1)) - 1
        col1 = 0
        row2 = int(res.group(2)) - 1
        col2 = -1
        return (
         row1, col1, row2, col2)
    res = _re_col_range.match(cellrange)
    if res:
        col1 = col_by_name(res.group(1))
        row1 = 0
        col2 = col_by_name(res.group(2))
        row2 = -1
        return (
         row1, col1, row2, col2)
    res = _re_cell_range.match(cellrange)
    if res:
        (row1, col1) = cell_to_rowcol2(res.group(1))
        (row2, col2) = cell_to_rowcol2(res.group(2))
        return (
         row1, col1, row2, col2)
    res = _re_cell_ref.match(cellrange)
    if res:
        (row1, col1) = cell_to_rowcol2(res.group(1))
        return (
         row1, col1, row1, col1)
    raise Exception('Unknown cell reference %s' % cell)


def cell_to_packed_rowcol(cell):
    """ pack row and column into the required 4 byte format """
    (row, col, row_abs, col_abs) = cell_to_rowcol(cell)
    if col >= MAX_COL:
        raise Exception('Column %s greater than IV in formula' % cell)
    if row >= MAX_ROW:
        raise Exception('Row %s greater than %d in formula' % (cell, MAX_ROW))
    col |= int(not row_abs) << 15
    col |= int(not col_abs) << 14
    return (row, col)