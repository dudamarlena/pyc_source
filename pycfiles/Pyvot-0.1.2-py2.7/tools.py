# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build-py2\bdist.egg\xl\tools.py
# Compiled at: 2011-11-21 15:27:19
from xl.range import Range, Vector, RowVector, ColumnVector, Scalar
from xl.sheet import Workbook, Worksheet
from xl.cache import CacheManager, enable_caching, cache_result
import collections

def workbooks():
    """Returns a list of open workbooks"""
    import xl._impl.com_utils
    return [ Workbook(x) for x in xl._impl.com_utils.get_open_xlWorkbooks() ]


def view(x, name=None, to=None):
    return Workbook.default_workbook().view(x, name, to)


def get(r):
    """Returns a Range for the given table column name, named range, or Excel address (ex. A1:B4).
    `get` guesses the active workbook, and begins its search on the active sheet.
    
    See also: xl.Workbook.get and xl.Workbook.range"""
    return Workbook.default_workbook().get(r)


def selected_range():
    """Gets the currently selected range. The returned range filters
    hidden cells by default"""
    wb = Workbook.default_workbook()
    xlApp = wb.xlWorkbook.Application
    return Range(xlApp.Selection, with_hidden=False).normalize()


def selected_value():
    """Gets the values in the currently selected range. See xl.selected_range()"""
    return selected_range().get()


def filter(func, range):
    """Filters rows or columns by applying `func` to the given range.
    `func` is called for each value in the range. If it returns False,
    the corresponding row / column is hidden. Otherwise, the row / column is
    made visible.

    `range` must be a row or column vector. If it is a row vector, columns are hidden, and vice versa.
    
    Note that, to unhide rows / columns, `range` must include hidden cells. For example, to unhide a range:
       xl.filter(lambda v: True, some_vector.including_hidden)"""
    if range.shape not in (Scalar, RowVector, ColumnVector):
        raise ValueError('range must be a vector or scalar')
    hide_dim = range._vector_dim.other
    with CacheManager.caching_disabled():
        for cell in range.itercells():
            assert cell.shape is Scalar
            visible = bool(func(cell.get()))
            hide_dim.entire(cell._full_xlRange).Hidden = not visible


def map(func, *rangeIn):
    """Excel equivalent to the built-in map().

    ColumnVector ranges as well as Python iterables are accepted.
    The result list is written back to Excel as a column. A ColumnVector
    representing the stored results is returned"""
    import __builtin__
    xs = (_to_value(r) for r in rangeIn)
    name = getattr(func, '__name__', '<callable>')
    y = __builtin__.map(func, *xs)
    r = _dest_for_source_ranges(rangeIn)
    return view(y, name, to=r)


def apply(func, *rangeIn):
    """Excel equivalent to the built-in apply().

    Ranges as well as Python iterables are accepted. Ranges
    are converted to lists of Python values (with Range.get()).
    
    The value returned by `func` is then passed to xl.view"""
    import __builtin__
    xs = (_to_value(r) for r in rangeIn)
    name = getattr(func, '__name__', '<callable>')
    y = __builtin__.apply(func, xs)
    r = _dest_for_source_ranges(rangeIn)
    return view(y, name, to=r)


def _to_value(obj):
    r = _tryToRange(obj)
    if r is not None:
        return r.get()
    else:
        if isinstance(obj, collections.Sequence):
            return obj
        raise ValueError('Expected range or value')
        return


def _tryToRange(obj):
    if obj is None:
        raise ValueError("range object can't be None")
    if isinstance(obj, Range):
        return obj
    else:
        t = type(obj)
        if t is str:
            return get(obj)
        return


def _toRange(obj):
    r = _tryToRange(obj)
    if r is None:
        raise ValueError('Unrecognized range object:%s' % str(obj))
    return r


def _dest_for_source_ranges(ranges):
    """Given a set of source ranges/values (for map or apply), attempts to find a sensible target range
    If a source is found that is both a range and part of a table, returns a new column range in that table
    If no such range exists, None is returned"""
    rs = [ r for r in ranges if r is not None and isinstance(r, Range) and r.containing_table is not None
         ]
    if rs:
        r = rs[0]
        dest_col = r.containing_table.append_empty_columns(1)
        dest_col = dest_col.with_filter(include_hidden_cells=r.includes_hidden_cells)
        return dest_col
    else:
        return
        return


def join--- This code section failed: ---

 L. 147         0  LOAD_GLOBAL           0  '_join_map'
                3  LOAD_FAST             1  'key_range_b'
                6  CALL_FUNCTION_1       1  None
                9  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST            2  'b_headers'
               15  STORE_FAST            3  'b_key_map'

 L. 148        18  LOAD_FAST             2  'b_headers'
               21  LOAD_CONST               None
               24  COMPARE_OP            9  is-not
               27  POP_JUMP_IF_TRUE     39  'to 39'
               30  LOAD_ASSERT              AssertionError
               33  LOAD_CONST               'Headerless tables not supported yet'
               36  RAISE_VARARGS_2       2  None

 L. 151        39  LOAD_GLOBAL           3  'len'
               42  LOAD_FAST             2  'b_headers'
               45  CALL_FUNCTION_1       1  None
               48  STORE_FAST            4  'num_joined_cols'

 L. 152        51  LOAD_FAST             4  'num_joined_cols'
               54  LOAD_CONST               0
               57  COMPARE_OP            2  ==
               60  POP_JUMP_IF_FALSE    78  'to 78'

 L. 153        63  LOAD_GLOBAL           4  'ValueError'
               66  LOAD_CONST               'key_range_b indicates the source table; there must be at least one value column in addition to the key column'
               69  CALL_FUNCTION_1       1  None
               72  RAISE_VARARGS_1       1  None
               75  JUMP_FORWARD          0  'to 78'
             78_0  COME_FROM            75  '75'

 L. 155        78  LOAD_FAST             2  'b_headers'
               81  BUILD_LIST_1          1 
               84  STORE_FAST            5  'new_rows'

 L. 156        87  SETUP_LOOP           73  'to 163'
               90  LOAD_FAST             0  'key_range_a'
               93  GET_ITER         
               94  FOR_ITER             65  'to 162'
               97  STORE_FAST            6  'a_key'

 L. 157       100  LOAD_FAST             3  'b_key_map'
              103  LOAD_ATTR             5  'get'
              106  LOAD_FAST             6  'a_key'
              109  LOAD_CONST               ('',)
              112  LOAD_FAST             4  'num_joined_cols'
              115  BINARY_MULTIPLY  
              116  CALL_FUNCTION_2       2  None
              119  STORE_FAST            7  'v'

 L. 158       122  LOAD_GLOBAL           3  'len'
              125  LOAD_FAST             7  'v'
              128  CALL_FUNCTION_1       1  None
              131  LOAD_FAST             4  'num_joined_cols'
              134  COMPARE_OP            2  ==
              137  POP_JUMP_IF_TRUE    146  'to 146'
              140  LOAD_ASSERT              AssertionError
              143  RAISE_VARARGS_1       1  None

 L. 159       146  LOAD_FAST             5  'new_rows'
              149  LOAD_ATTR             6  'append'
              152  LOAD_FAST             7  'v'
              155  CALL_FUNCTION_1       1  None
              158  POP_TOP          
              159  JUMP_BACK            94  'to 94'
              162  POP_BLOCK        
            163_0  COME_FROM            87  '87'

 L. 161       163  LOAD_GLOBAL           7  'Worksheet'
              166  LOAD_FAST             0  'key_range_a'
              169  LOAD_ATTR             8  '_full_xlRange'
              172  LOAD_ATTR             7  'Worksheet'
              175  CALL_FUNCTION_1       1  None
              178  STORE_FAST            8  'ws_a'

 L. 162       181  LOAD_FAST             8  'ws_a'
              184  LOAD_ATTR             9  '_find_table_containing_range'
              187  LOAD_FAST             0  'key_range_a'
              190  CALL_FUNCTION_1       1  None
              193  STORE_FAST            9  'tb_a'

 L. 164       196  LOAD_FAST             9  'tb_a'
              199  LOAD_ATTR            10  'append_empty_columns'
              202  LOAD_FAST             4  'num_joined_cols'
              205  CALL_FUNCTION_1       1  None
              208  STORE_FAST           10  'joined_cols'

 L. 167       211  LOAD_FAST            10  'joined_cols'
              214  LOAD_ATTR            11  'as_matrix'
              217  LOAD_ATTR            12  'set'
              220  LOAD_FAST             5  'new_rows'
              223  CALL_FUNCTION_1       1  None
              226  POP_TOP          
              227  LOAD_CONST               None
              230  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 227


def _join_map--- This code section failed: ---

 L. 170         0  LOAD_GLOBAL           0  'Worksheet'
                3  LOAD_FAST             0  'r'
                6  LOAD_ATTR             1  '_full_xlRange'
                9  LOAD_ATTR             0  'Worksheet'
               12  CALL_FUNCTION_1       1  None
               15  STORE_FAST            1  'ws'

 L. 171        18  LOAD_FAST             1  'ws'
               21  LOAD_ATTR             2  '_find_table_containing_range'
               24  LOAD_FAST             0  'r'
               27  CALL_FUNCTION_1       1  None
               30  STORE_FAST            2  'tb'

 L. 173        33  LOAD_FAST             0  'r'
               36  LOAD_ATTR             3  'column'
               39  LOAD_FAST             2  'tb'
               42  LOAD_ATTR             4  'rData'
               45  LOAD_ATTR             3  'column'
               48  BINARY_SUBTRACT  
               49  STORE_FAST            3  'key_col_idx'

 L. 174        52  LOAD_CONST               None
               55  STORE_FAST            4  'headers'

 L. 175        58  LOAD_FAST             2  'tb'
               61  LOAD_ATTR             6  'rHeader'
               64  POP_JUMP_IF_FALSE   122  'to 122'

 L. 176        67  LOAD_FAST             2  'tb'
               70  LOAD_ATTR             6  'rHeader'
               73  LOAD_ATTR             7  'shape'
               76  LOAD_GLOBAL           8  'Scalar'
               79  COMPARE_OP            9  is-not
               82  POP_JUMP_IF_TRUE     91  'to 91'
               85  LOAD_ASSERT              AssertionError
               88  RAISE_VARARGS_1       1  None

 L. 177        91  LOAD_GLOBAL          10  'list'
               94  LOAD_FAST             2  'tb'
               97  LOAD_ATTR             6  'rHeader'
              100  LOAD_ATTR            11  'get'
              103  CALL_FUNCTION_0       0  None
              106  CALL_FUNCTION_1       1  None
              109  STORE_FAST            4  'headers'

 L. 178       112  LOAD_FAST             4  'headers'
              115  LOAD_FAST             3  'key_col_idx'
              118  DELETE_SUBSCR    
              119  JUMP_FORWARD          0  'to 122'
            122_0  COME_FROM           119  '119'

 L. 180       122  BUILD_MAP_0           0  None
              125  STORE_FAST            5  'm'

 L. 181       128  SETUP_LOOP           72  'to 203'
              131  LOAD_FAST             2  'tb'
              134  LOAD_ATTR            12  'data_rows'
              137  GET_ITER         
              138  FOR_ITER             61  'to 202'
              141  STORE_FAST            0  'r'

 L. 182       144  LOAD_FAST             0  'r'
              147  LOAD_FAST             3  'key_col_idx'
              150  BINARY_SUBSCR    
              151  LOAD_FAST             5  'm'
              154  COMPARE_OP            7  not-in
              157  POP_JUMP_IF_TRUE    169  'to 169'
              160  LOAD_ASSERT              AssertionError
              163  LOAD_CONST               'Duplicate key during join'
              166  RAISE_VARARGS_2       2  None

 L. 183       169  LOAD_FAST             0  'r'
              172  LOAD_FAST             3  'key_col_idx'
              175  SLICE+2          
              176  LOAD_FAST             0  'r'
              179  LOAD_FAST             3  'key_col_idx'
              182  LOAD_CONST               1
              185  BINARY_ADD       
              186  SLICE+1          
              187  BINARY_ADD       
              188  LOAD_FAST             5  'm'
              191  LOAD_FAST             0  'r'
              194  LOAD_FAST             3  'key_col_idx'
              197  BINARY_SUBSCR    
              198  STORE_SUBSCR     
              199  JUMP_BACK           138  'to 138'
              202  POP_BLOCK        
            203_0  COME_FROM           128  '128'

 L. 185       203  LOAD_FAST             4  'headers'
              206  LOAD_FAST             5  'm'
              209  BUILD_TUPLE_2         2 
              212  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 202


def tool_map(func):
    return func


def tool_apply(func):
    return func


def tool_workbook(func):
    return func