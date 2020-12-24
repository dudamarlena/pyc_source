# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build-py2\bdist.egg\xl\sheet.py
# Compiled at: 2011-11-21 15:27:19
from xl.cache import cache_result, enable_caching
import xl._impl.com_utils as com_utils, xl._impl.table as table
from xl.range import Range, ExcelRangeError, _xlRange_from_corners, _xlRange_parse

class Worksheet(object):

    def __init__(self, xlSheet):
        self.xlWorksheet = xlSheet

    def _findOpenColumn(self):
        xlRange = self.xlWorksheet.UsedRange
        if xlRange.Count == 1:
            if self.xlWorksheet.Cells(1, 1).Value == None:
                return 1
        cs = [ c.Column for c in xlRange.Columns ]
        x = max(cs)
        return x + 1

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.xlWorksheet.Name

    @cache_result
    @enable_caching
    def _getTableColumn(self, name):
        """Search through this worksheets for the given table column
        Return a Range if found, else None."""
        for t in self.tables:
            rData = t._getTableColumn(name)
            if rData != None:
                return rData

        return

    @cache_result
    @property
    @enable_caching
    def tables(self):
        """Returns a list of all table-like things on the sheet"""
        l = []
        t = table.tableFromAutoFilter(self.xlWorksheet)
        if t != None:
            l.append(t)
        los = self.xlWorksheet.ListObjects
        for lo in los:
            t = table.tableFromListObject(lo)
            l.append(t)

        return l

    def _find_table_containing_range(self, range):
        """Search all Tables on the sheet for any that contain the given range.
        Return None if not found."""
        for t in self.tables:
            if t.rData.intersects(range):
                return t

        return


_default_workbook = None

class Workbook(object):

    def __init__--- This code section failed: ---

 L.  87         0  LOAD_CONST               -1
                3  LOAD_CONST               None
                6  IMPORT_NAME           0  'win32com.client'
                9  LOAD_ATTR             1  'client'
               12  STORE_FAST            2  'win32'

 L.  88        15  LOAD_GLOBAL           2  'com_utils'
               18  LOAD_ATTR             3  'ensure_excel_dispatch_support'
               21  CALL_FUNCTION_0       0  None
               24  POP_TOP          

 L.  89        25  LOAD_GLOBAL           4  'len'
               28  LOAD_FAST             1  'args'
               31  CALL_FUNCTION_1       1  None
               34  LOAD_CONST               0
               37  COMPARE_OP            2  ==
               40  POP_JUMP_IF_FALSE   112  'to 112'

 L.  91        43  LOAD_FAST             2  'win32'
               46  LOAD_ATTR             5  'gencache'
               49  LOAD_ATTR             6  'EnsureDispatch'
               52  LOAD_CONST               'Excel.Application'
               55  CALL_FUNCTION_1       1  None
               58  STORE_FAST            3  'excel'

 L.  92        61  LOAD_GLOBAL           7  'True'
               64  LOAD_FAST             3  'excel'
               67  STORE_ATTR            8  'Visible'

 L.  93        70  LOAD_FAST             3  'excel'
               73  LOAD_ATTR             9  'Workbooks'
               76  LOAD_ATTR            10  'Add'
               79  CALL_FUNCTION_0       0  None
               82  LOAD_FAST             0  'self'
               85  STORE_ATTR           11  'xlWorkbook'

 L.  94        88  LOAD_FAST             0  'self'
               91  LOAD_ATTR            11  'xlWorkbook'
               94  LOAD_CONST               None
               97  COMPARE_OP            9  is-not
              100  POP_JUMP_IF_TRUE    260  'to 260'
              103  LOAD_ASSERT              AssertionError
              106  RAISE_VARARGS_1       1  None
              109  JUMP_FORWARD        148  'to 260'

 L.  95       112  LOAD_GLOBAL           4  'len'
              115  LOAD_FAST             1  'args'
              118  CALL_FUNCTION_1       1  None
              121  LOAD_CONST               1
              124  COMPARE_OP            2  ==
              127  POP_JUMP_IF_FALSE   260  'to 260'

 L.  96       130  LOAD_GLOBAL          14  'isinstance'
              133  LOAD_FAST             1  'args'
              136  LOAD_CONST               0
              139  BINARY_SUBSCR    
              140  LOAD_GLOBAL          15  'basestring'
              143  CALL_FUNCTION_2       2  None
              146  POP_JUMP_IF_FALSE   216  'to 216'

 L.  97       149  LOAD_FAST             1  'args'
              152  LOAD_CONST               0
              155  BINARY_SUBSCR    
              156  STORE_FAST            4  'filename'

 L.  98       159  LOAD_GLOBAL           2  'com_utils'
              162  LOAD_ATTR            16  'get_running_xlWorkbook_for_filename'
              165  LOAD_FAST             4  'filename'
              168  CALL_FUNCTION_1       1  None
              171  LOAD_FAST             0  'self'
              174  STORE_ATTR           11  'xlWorkbook'

 L.  99       177  LOAD_FAST             0  'self'
              180  LOAD_ATTR            11  'xlWorkbook'
              183  LOAD_CONST               None
              186  COMPARE_OP            2  ==
              189  POP_JUMP_IF_FALSE   257  'to 257'

 L. 100       192  LOAD_GLOBAL           2  'com_utils'
              195  LOAD_ATTR            17  'open_xlWorkbook'
              198  LOAD_FAST             4  'filename'
              201  CALL_FUNCTION_1       1  None
              204  LOAD_FAST             0  'self'
              207  STORE_ATTR           11  'xlWorkbook'
              210  JUMP_ABSOLUTE       257  'to 257'
              213  JUMP_ABSOLUTE       260  'to 260'

 L. 102       216  LOAD_GLOBAL          18  'hasattr'
              219  LOAD_FAST             1  'args'
              222  LOAD_CONST               0
              225  BINARY_SUBSCR    
              226  LOAD_CONST               'CLSID'
              229  CALL_FUNCTION_2       2  None
              232  POP_JUMP_IF_TRUE    244  'to 244'
              235  LOAD_ASSERT              AssertionError
              238  LOAD_CONST               'Expected workbook name or xlWorkbook'
              241  RAISE_VARARGS_2       2  None

 L. 103       244  LOAD_FAST             1  'args'
              247  LOAD_CONST               0
              250  BINARY_SUBSCR    
              251  LOAD_FAST             0  'self'
              254  STORE_ATTR           11  'xlWorkbook'
              257  JUMP_FORWARD          0  'to 260'
            260_0  COME_FROM           257  '257'
            260_1  COME_FROM           109  '109'

 L. 105       260  LOAD_FAST             0  'self'
              263  LOAD_ATTR            19  'set_default_workbook'
              266  LOAD_FAST             0  'self'
              269  CALL_FUNCTION_1       1  None
              272  POP_TOP          
              273  LOAD_CONST               None
              276  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 273

    @classmethod
    def default_workbook(cls):
        global _default_workbook
        if _default_workbook == None:
            cls.set_default_workbook(Workbook())
        return _default_workbook

    @classmethod
    def set_default_workbook(cls, workbook):
        global _default_workbook
        if workbook == None:
            raise ValueError("Can't set active workbook instance to None")
        _default_workbook = workbook
        return

    @cache_result
    @property
    def active_sheet(self):
        return Worksheet(self.xlWorkbook.ActiveSheet)

    @cache_result
    @property
    def worksheets(self):
        return [ Worksheet(xlSheet) for xlSheet in self.xlWorkbook.Worksheets ]

    def view(self, obj, name=None, to=None):
        """Writes a Python iterable to an available location in the workbook, with an optional header (name).
        The optional `to` argument specifies a location hint. 
        
        If None, the values are written to an empty column on the active sheet.
        If `to` is a Range, the values are written to it (like Range.set, but with the header prepended)
        If `to` is a Table, the values are written to a new column in the table."""
        if to is None:
            ws = self.active_sheet
            c = Range(ws.xlWorksheet.Columns(ws._findOpenColumn()), with_hidden=False)
        elif isinstance(to, table.Table):
            c = to.append_empty_columns(num_new_cols=1)
        elif isinstance(to, Range):
            c = to
        else:
            raise ValueError("'to' argument must be a Range, Table, or None")
        if name == None:
            name = 'values'
        if isinstance(obj, basestring):
            obj = [
             obj]
        obj = list(obj)
        vals = [name] + obj
        c.set(vals)
        data_only = c._adjust_unfiltered_size(rows=-1)._offset_unfiltered(rows=1)
        return data_only

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Workbook(%s)' % repr(self.name)

    @property
    def name(self):
        return self.xlWorkbook.Name

    @cache_result
    @enable_caching
    def get(self, object):
        """Returns a Range for the requested table column, named Excel range, or Excel address (ex. A1:B20)

        The returned Range has been normalized (see Range.normalize()); if possible, it is clipped to an overlapping table's data area,
        as well as the worksheet's `used range`."""
        if type(object) is str:
            r = self._getTableColumn(object)
            if r != None:
                return r
        try:
            r = self.range(object)
        except ExcelRangeError:
            msg = 'failed to find range or table column: %s. ' + 'Note that table columns must be part of an AutoFilter or Table (Ctrl+T) in Excel in order to be found.'
            msg = msg % str(object)
            raise ExcelRangeError(msg)

        return r.normalize()

    @cache_result
    @enable_caching
    def range(self, object):
        """Returns a Range for the requested named Excel range or Excel address.

        The returned range is not normalized, e.g. range("A:A") returns a Range containing ~1mil rows,
        rather than clipping to the 'used range' / table areas. See also `get`"""
        r = self._get_named_range(object)
        if r != None:
            return r
        else:
            xlSheet = self.xlWorkbook.ActiveSheet
            xlRange = _xlRange_parse(xlSheet, object)
            return Range(xlRange, with_hidden=False)

    def _get_named_range(self, name):
        name = name.lower()
        for n in self.xlWorkbook.Names:
            if n.Name.lower() == name:
                r = n.RefersToRange
                if r == None:
                    raise NotImplementedError('Name ' + name + ' is not backed by a range')
                return Range(r, with_hidden=False)

        return

    @property
    def named_ranges(self):
        return [ n.Name for n in self.xlWorkbook.Names ]

    def _getTableColumn(self, name):
        """Search through all worksheets for the given column
        Return a Range if found, else None."""
        active = self.active_sheet
        r = active._getTableColumn(name)
        if r != None:
            return r
        else:
            for s in self.worksheets:
                r = s._getTableColumn(name)
                if r != None:
                    return r

            return