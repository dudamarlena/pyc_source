# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build-py2\bdist.egg\xl\_impl\table.py
# Compiled at: 2011-11-21 15:27:19
import xl._impl.com_utils as com_utils
from xl.cache import CacheManager, cache_result, enable_caching
from xl.range import Range

class Table(object):

    def __init__(self, name, rHeader, rData, from_auto_filter=False):
        self.rHeader = rHeader
        self.rData = rData
        self._name = name
        self._from_auto_filter = from_auto_filter
        assert rHeader != None and not rHeader.intersects(rData)
        return

    @cache_result
    @enable_caching
    def _getTableColumn(self, name):
        """Returns a Range for the data in the given column name.
        None if no column."""
        if self.rHeader == None:
            return
        else:
            name = name.lower()
            for idx, header in enumerate(self.rHeader):
                if header is None:
                    continue
                if header.lower() == name:
                    return self.rData.column_vector(idx)

            return

    def getRowCount(self):
        return self.rData.num_rows

    def getVisibleRowCount(self):
        return self.rData.getVisibleRowCount()

    @property
    def data_rows(self):
        """Returns s list of data rows in the table. Each row is a list of values"""
        return self.rData.as_matrix.get()

    @cache_result
    @property
    def table_range(self):
        """The full Range of this table; encompasses headers (if any) as well as data"""
        assert self.rData is not None
        app = self.rData._full_xlRange.Application
        if self.rHeader is None:
            return self.rData
        else:
            return Range(app.Union(self.rData._full_xlRange, self.rHeader._full_xlRange), with_hidden=False)

    def Name(self):
        return self._name

    def append_empty_columns(self, num_new_cols):
        """Appends the specified number of columns to the right of this table. The columns are empty,
        except for the possibility of Excel-generated default column headers. The inserted range,
        including headers, is returned"""
        if num_new_cols == 0:
            return None
        else:
            adjacent = self._adjacent_column_range(num_new_cols)
            self._reserve_column_space(adjacent)
            adjacent = self._adjacent_column_range(num_new_cols)
            if self._from_auto_filter:
                self._convert_to_listobject_table()
            adj_header_range = Range(adjacent._full_xlRange.Rows(1), with_hidden=True)
            adj_header_range.set([' '] * num_new_cols)
            adj_header_range.set([''] * num_new_cols)
            return adjacent.excluding_hidden

    def _adjacent_column_range(self, num_cols):
        """Returns a num_cols-wide range right-adjacent to this table. The range shares the same height, incl.
        the header row if applicable. This does not modify the worksheet. The returned range includes hidden cells."""
        full_table = self.table_range.including_hidden
        last_existing_col = Range(full_table._full_xlRange.Columns(full_table.num_columns), with_hidden=True)
        first_new_col = last_existing_col._offset_unfiltered(cols=1)
        new_cols = first_new_col._adjust_unfiltered_size(cols=num_cols - 1)
        return new_cols

    def _reserve_column_space(self, range):
        """Reserve at least the requested range for new Table columns. The given range
        is assumed to be adjacent (on the right) of this Table. If unable to insert the given range,
        (e.g. because it would break a table further to the right), full (worksheet) columns are inserted instead."""
        CacheManager.invalidate_all_caches()
        try:
            range._full_xlRange.Insert(CopyOrigin=com_utils.constants.xlFormatFromLeftOrAbove, Shift=com_utils.constants.xlToRight)
        except com_utils.com_error:
            range._full_xlRange.EntireColumn.Insert(CopyOrigin=com_utils.constants.xlFormatFromLeftOrAbove, Shift=com_utils.constants.xlToRight)

    def _convert_to_listobject_table--- This code section failed: ---

 L. 136         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  '_from_auto_filter'
                6  POP_JUMP_IF_TRUE     18  'to 18'
                9  LOAD_ASSERT              AssertionError
               12  LOAD_CONST               'already a ListObject table'
               15  RAISE_VARARGS_2       2  None

 L. 137        18  LOAD_FAST             0  'self'
               21  LOAD_ATTR             2  'rData'
               24  LOAD_ATTR             3  '_full_xlRange'
               27  LOAD_ATTR             4  'Worksheet'
               30  STORE_FAST            1  'xlWorksheet'

 L. 138        33  LOAD_FAST             1  'xlWorksheet'
               36  LOAD_ATTR             5  'ListObjects'
               39  LOAD_ATTR             6  'Add'
               42  LOAD_CONST               'SourceType'
               45  LOAD_GLOBAL           7  'com_utils'
               48  LOAD_ATTR             8  'constants'
               51  LOAD_ATTR             9  'xlSrcRange'
               54  LOAD_CONST               'Source'
               57  LOAD_FAST             0  'self'
               60  LOAD_ATTR            10  'table_range'
               63  LOAD_ATTR             3  '_full_xlRange'
               66  CALL_FUNCTION_512   512  None
               69  POP_TOP          

 L. 139        70  LOAD_GLOBAL          11  'False'
               73  LOAD_FAST             0  'self'
               76  STORE_ATTR            0  '_from_auto_filter'

Parse error at or near `LOAD_FAST' instruction at offset 73


def tableFromListObject(xlListObject):
    """Given an ListObject, return a Table abstraction"""
    rHeader = Range(xlListObject.HeaderRowRange, with_hidden=False)
    rData = Range(xlListObject.DataBodyRange, with_hidden=False)
    return Table(xlListObject.Name, rHeader, rData, from_auto_filter=False)


def tableFromAutoFilter(xlSheet):
    """Each excel sheet can have 1 auto-filter. Return it if present. Else return None."""
    a = xlSheet.AutoFilter
    if a == None:
        return
    else:
        r = a.Range
        if r.ListObject != None:
            return
        r1, c1, r2, c2 = _getBounds(r)
        rHeader = Range(xlSheet.Range(xlSheet.Cells(r1, c1), xlSheet.Cells(r1, c2)), with_hidden=False)
        rData = Range(xlSheet.Range(xlSheet.Cells(r1 + 1, c1), xlSheet.Cells(r2, c2)), with_hidden=False)
        return Table('AutoFilter ' + xlSheet.Name, rHeader, rData, from_auto_filter=True)


def _getBounds(xlRange):
    x = xlRange.Columns
    c1 = x(1).Column
    c2 = x(len(x)).Column
    y = xlRange.Rows
    r1 = y(1).Row
    r2 = y(len(y)).Row
    return (
     r1, c1, r2, c2)