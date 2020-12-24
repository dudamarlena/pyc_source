# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build-py2\bdist.egg\xl\range.py
# Compiled at: 2011-11-21 15:27:19
import xl._impl.com_utils as com_utils
from xl.cache import CacheManager, cache_result, enable_caching
from xl._impl.collapsed_matrix import CollapsedMatrix

class ExcelRangeError(ValueError):
    """Raised when
    - a requested range / named range / table column is invalid or cannot be found
    - usage of a Range instance fails due to its dimensions, e.g. Range.set() with too many values"""
    pass


class Range(object):
    """Represents a contiguous range of cells in Excel, ex. A1:B20. The contents (in Excel) can be read and written to (see the `get`
    and `set` methods).
    
    Ranges are usually obtained using the :meth:`xl.sheet.Workbook.get` or :meth:`xl.sheet.Workbook.range` method. The returned range behaves
    according to its 'shape,' which is reflected in its type as well as the `shape` property::

        >>> type(workbook.get("A:A"))
        <class 'xl.range.ColumnVector'>

    A range's shape may be `ColumnVector`, `RowVector`, `Scalar`, or `Matrix`. The `Vector` type (a base for RowVector
    and ColumnVector) allows detection of either vector variety::

        >>> isinstance(workbook.get("A:A"), xl.Vector)
        True

    The shape subclasses differ in the rules and types involved in accessing the backing Excel data, e.g. the return
    type of `get`. See help(shape class) for specifics.

    By default, a Range excludes 'hidden' cells - those not visible in Excel due to an Excel-level filter,
    or manual hiding by the user. The `including_hidden` and `excluding_hidden` properties permit explicit
    control of this behavior::

        >>> workbook.get("A1:A3")
        <ColumnVector range object for $A$1,$A$3 (visible only)>
        >>> workbook.get("A1:A3").including_hidden
        <ColumnVector range object for $A$1:$A$3 (includes hidden)>
    
    Note that un-filtered dimensions determine shape, e.g. ``workbook.get("A1:B2")`` is a Matrix, even if column B is hidden"""

    def __init__--- This code section failed: ---

 L.  55         0  LOAD_FAST             1  'xlRange'
                3  LOAD_ATTR             0  'Areas'
                6  LOAD_ATTR             1  'Count'
                9  LOAD_CONST               1
               12  COMPARE_OP            2  ==
               15  POP_JUMP_IF_TRUE     27  'to 27'
               18  LOAD_ASSERT              AssertionError
               21  LOAD_CONST               "can't wrap a non-contiguous xlRange"
               24  RAISE_VARARGS_2       2  None

 L.  58        27  LOAD_FAST             1  'xlRange'
               30  LOAD_ATTR             3  'Cells'
               33  LOAD_FAST             0  'self'
               36  STORE_ATTR            4  '_full_xlRange'

 L.  59        39  LOAD_FAST             2  'with_hidden'
               42  LOAD_FAST             0  'self'
               45  STORE_ATTR            5  '_with_hidden'

 L.  60        48  LOAD_FAST             3  'as_matrix'
               51  LOAD_FAST             0  'self'
               54  STORE_ATTR            6  '_as_matrix'

 L.  62        57  LOAD_FAST             0  'self'
               60  LOAD_ATTR             7  '_init_shape_class'
               63  LOAD_CONST               'as_matrix'
               66  LOAD_FAST             3  'as_matrix'
               69  CALL_FUNCTION_256   256  None
               72  POP_TOP          

Parse error at or near `CALL_FUNCTION_256' instruction at offset 69

    def _init_shape_class(self, as_matrix):
        """Updates __class__ based on the unfiltered (contiguous) dimensions. After this call,
        the instance is a subclass of Range, such as Matrix."""
        r, c = self._unfiltered_dimensions
        if as_matrix:
            self.__class__ = Matrix
        elif (r == 1) + (c == 1) == 1:
            if r == 1:
                self.__class__ = RowVector
            else:
                self.__class__ = ColumnVector
        elif r == 1 and c == 1:
            self.__class__ = Scalar
        elif r > 1 and c > 1:
            self.__class__ = Matrix
        else:
            assert False
        assert isinstance(self, Range)

    @property
    def shape(self):
        """Returns the shape class of this range (e.g. RowVector). Equivalent to type(self)"""
        assert type(self) is not Range
        return type(self)

    @cache_result
    @property
    def as_matrix(self):
        """Returns a version of this range that is always a Matrix (even if shaped differently).
        This is useful for utility functions that wish to avoid a special case per range shape"""
        if self._as_matrix:
            return self
        return Range(self._full_xlRange, with_hidden=self._with_hidden, as_matrix=True)

    @cache_result
    @property
    def _effective_xlRange(self):
        """The xlRange from which we should draw data; filtered cells are removed, if applicable"""
        return self._apply_filter_to(self._full_xlRange)

    def _apply_filter_to(self, xlRange):
        """Given an xlRange, returns a subset which passes the configured filters.
        A filter may remove entire rows and columns, but NOT arbitrary cells"""
        if self.includes_hidden_cells:
            return xlRange
        else:
            assert not self._with_hidden
            if xlRange.Cells.Count == 1:
                assert not (xlRange.EntireRow.Hidden or xlRange.EntireColumn.Hidden)
                return xlRange
            return xlRange.SpecialCells(com_utils.constants.xlCellTypeVisible)

    @cache_result
    def with_filter(self, include_hidden_cells):
        """Returns a range with the specified inclusion / exclusion of hidden cells.
        See the including_hidden / excluding_hidden properties for less verbose shortcuts"""
        if self.includes_hidden_cells == include_hidden_cells:
            return self
        return Range(self._full_xlRange, with_hidden=include_hidden_cells, as_matrix=self._as_matrix)

    @property
    def includes_hidden_cells(self):
        return self._with_hidden

    @property
    def excluding_hidden(self):
        """Returns a new Range identical this one, but with hidden cells filtered away.
        This is reversible, e.g. range.exluding_hidden.including_hidden"""
        return self.with_filter(include_hidden_cells=False)

    @property
    def including_hidden(self):
        """Returns a new Range identical this one, but with hidden cells included.
        This is reversible, e.g. range.including_hidden.excluding_hidden"""
        return self.with_filter(include_hidden_cells=True)

    def _with_xlRange(self, xlRange):
        """Returns a Range with the same filtering / shape override, but the specified xlRange"""
        if _xlRanges_equivalent(xlRange, self._full_xlRange):
            return self
        else:
            return Range(xlRange, with_hidden=self._with_hidden, as_matrix=self._as_matrix)

    def __repr__(self):
        try:
            addr = str(self._effective_xlRange.Address)
        except com_utils.com_error:
            addr = '<error getting address from excel>'

        hidden_descr = 'visible only' if not self._with_hidden else 'includes hidden'
        return '<%s range object for %s (%s)>' % (type(self).__name__, addr, hidden_descr)

    @cache_result
    @property
    def _trimmed(self):
        trimmedXlRange = _trim_xlRange(self._full_xlRange)
        return self._with_xlRange(trimmedXlRange)

    @cache_result
    @enable_caching
    def _get_2D(self):
        cd = self._trimmed._get_collapsed_matrix(populate_values=True).collapsed_data
        return [ [ com_utils.unmarshal_from_excel_value(c) for c in row ] for row in cd ]

    @enable_caching
    def _set_2d(self, data):
        """Sets the range's cells using the 2D (list-of-lists) `data` parameter. `data` may be smaller
        than the range"""
        num_rows, num_cols = self.dimensions
        data = list(data)
        num_data_rows = len(data)
        num_data_cols = len(data[0]) if data else 0
        if num_data_rows > num_rows:
            raise ExcelRangeError('Range has %d rows; too many (%d) given' % (num_rows, num_data_rows))
        if num_data_cols > num_cols:
            raise ExcelRangeError('Range has %d columns; too many (%d) given' % (num_cols, num_data_cols))
        if num_data_rows < num_rows or num_data_cols < num_cols:
            matrix = self._get_collapsed_matrix(populate_values=False, row_limit=num_data_rows, column_limit=num_data_cols)
        else:
            matrix = self._get_collapsed_matrix(populate_values=False)
        marshalled_data = []
        for row in data:
            if len(row) != num_data_cols:
                raise ExcelRangeError('All rows must be the same size')
            marshalled_data.append([ com_utils.marshal_to_excel_value(v) for v in row ])

        matrix.collapsed_data = marshalled_data
        self._set_from_collapsed_matrix(matrix)

    def _set_from_collapsed_matrix(self, matrix):
        """Sets this range's cell values to reflect the contents of `matrix.` The matrix is sliced
        with the range's sheet-wide indices (not relative to the range). In other words,
        if this range contains sheet cell (r, c), and matrix[r, c] is a valid index,
        the cell (r, c) is set to matrix[r, c]"""
        for area, bounds in self._area_bounds:
            (row_start, row_stop), (col_start, col_stop) = bounds
            val_2d = matrix[row_start:row_stop + 1, col_start:col_stop + 1]
            val_2d_rows = len(val_2d)
            if not val_2d_rows:
                continue
            val_2d_cols = len(val_2d[0])
            if not val_2d_cols:
                continue
            if val_2d_rows < row_stop - row_start + 1 or val_2d_cols < col_stop - col_start + 1:
                area = area.GetResize(val_2d_rows, val_2d_cols)
            CacheManager.invalidate_all_caches()
            area.Value = val_2d

    def itercells(self):
        """Returns a generator yielding the single cell ranges comprising this scalar / vector.
        Thus, range.get() == [c.get() for c in range.itercells()]"""
        if not (self.shape is Matrix and False):
            raise AssertionError, '2D itercells not supported'
        trimmedXlRange = _trim_xlRange(self._full_xlRange)
        trimmedRange = self._with_xlRange(trimmedXlRange)
        for c in trimmedRange._effective_xlRange:
            yield self._with_xlRange(c)

    def _dim_vector_index_in_sheet(self, dim, idx):
        """Maps relative (effective) indices on a given dimension to sheetwide indices.

        For example, _dim_vector_index_in_sheet(_RowDimension, 0) returns a value i such
        that xlWorksheet.Rows(i) is the sheet-row containing the first row of the effective range"""
        if dim is _RowDimension:
            m = self._get_collapsed_matrix(populate_values=False, column_limit=1)
            ind = m.row_indices
        elif dim is _ColumnDimension:
            m = self._get_collapsed_matrix(populate_values=False, row_limit=1)
            ind = m.column_indices
        return ind[idx]

    @cache_result
    def _get_dim_vector(self, dim, idx):
        """Returns a Range object for a row or column vector comprising the effective xlRange,
        by zero-based index.
        
        For example, _get_dim_vector(_RowDimension, 0) returns a RowVector for the
        first non-filtered row."""
        ws = self._full_xlRange.Worksheet
        app = ws.Application
        idx_sheet = self._dim_vector_index_in_sheet(dim, idx)
        vec_sheet = dim.of(ws)(idx_sheet)
        vec = app.Intersect(vec_sheet, self._full_xlRange)
        return self._with_xlRange(vec)

    def row_vector(self, idx):
        """Returns one of the row-vectors comprising this Range
        by index, i.e. row_vector(0) gives the first row"""
        return self._get_dim_vector(_RowDimension, idx)

    def column_vector(self, idx):
        """Returns one of the column-vectors comprising this Range
        by index, i.e. column_vector(0) gives the first column"""
        return self._get_dim_vector(_ColumnDimension, idx)

    @cache_result
    @property
    def _areas(self):
        """Returns a list of contigous sub-areas (rows / cols may be missing from the effective range)"""
        return list(self._effective_xlRange.Areas)

    @cache_result
    @property
    def _area_bounds(self):
        """Returns a tuple (contiguous xlRange, ((first row, last row), (first col, last col))) per contiguous sub-area"""
        return [ (a, self._single_area_bounds(a)) for a in self._areas ]

    def _single_area_bounds(self, xlArea):
        """Returns ((first row, last row), (first column, last column)) for the given xlArea"""
        r, c = xlArea.Row, xlArea.Column
        return ((r, r + xlArea.Rows.Count - 1), (c, c + xlArea.Columns.Count - 1))

    def _limit_index_pairs(self, pairs, count_limit):
        """Given a list of pairs (start, stop) (indicating a range of indices, inclusive),
        returns a list containing at most count_limit indices. The highest indices are dropped as needed.
            list( self._limit_index_pairs([(10,19), (30, 40)], 15)) ->  [(10, 19), (30, 34)]"""
        count = 0
        current_index = None
        for start, stop in sorted(pairs):
            assert stop >= start
            if current_index is None or start > current_index:
                current_index = start
            contained = stop - current_index + 1
            if contained > 0:
                if count + contained < count_limit:
                    count += contained
                else:
                    stop = count_limit - count + current_index - 1
                    assert count + stop - current_index + 1 == count_limit
                    count = count_limit
            current_index = stop + 1
            yield (start, stop)
            if count == count_limit:
                break

        return

    @cache_result
    @enable_caching
    def _get_collapsed_matrix--- This code section failed: ---

 L. 335         0  LOAD_GENEXPR             '<code_object <genexpr>>'
                3  MAKE_FUNCTION_0       0  None
                6  LOAD_FAST             0  'self'
                9  LOAD_ATTR             0  '_area_bounds'
               12  GET_ITER         
               13  CALL_FUNCTION_1       1  None
               16  STORE_FAST            4  'row_pairs'

 L. 336        19  LOAD_GENEXPR             '<code_object <genexpr>>'
               22  MAKE_FUNCTION_0       0  None
               25  LOAD_FAST             0  'self'
               28  LOAD_ATTR             0  '_area_bounds'
               31  GET_ITER         
               32  CALL_FUNCTION_1       1  None
               35  STORE_FAST            5  'col_pairs'

 L. 337        38  LOAD_FAST             2  'row_limit'
               41  LOAD_CONST               None
               44  COMPARE_OP            9  is-not
               47  POP_JUMP_IF_FALSE    71  'to 71'
               50  LOAD_FAST             0  'self'
               53  LOAD_ATTR             2  '_limit_index_pairs'
               56  LOAD_FAST             4  'row_pairs'
               59  LOAD_FAST             2  'row_limit'
               62  CALL_FUNCTION_2       2  None
               65  STORE_FAST            4  'row_pairs'
               68  JUMP_FORWARD          0  'to 71'
             71_0  COME_FROM            68  '68'

 L. 338        71  LOAD_FAST             3  'column_limit'
               74  LOAD_CONST               None
               77  COMPARE_OP            9  is-not
               80  POP_JUMP_IF_FALSE   104  'to 104'
               83  LOAD_FAST             0  'self'
               86  LOAD_ATTR             2  '_limit_index_pairs'
               89  LOAD_FAST             5  'col_pairs'
               92  LOAD_FAST             3  'column_limit'
               95  CALL_FUNCTION_2       2  None
               98  STORE_FAST            5  'col_pairs'
              101  JUMP_FORWARD          0  'to 104'
            104_0  COME_FROM           101  '101'

 L. 340       104  LOAD_GLOBAL           3  'CollapsedMatrix'
              107  LOAD_FAST             4  'row_pairs'
              110  LOAD_FAST             5  'col_pairs'
              113  CALL_FUNCTION_2       2  None
              116  STORE_FAST            6  'm'

 L. 342       119  LOAD_FAST             1  'populate_values'
              122  POP_JUMP_IF_FALSE   309  'to 309'

 L. 343       125  LOAD_FAST             2  'row_limit'
              128  LOAD_CONST               None
              131  COMPARE_OP            8  is
              134  POP_JUMP_IF_FALSE   149  'to 149'
              137  LOAD_FAST             3  'column_limit'
              140  LOAD_CONST               None
              143  COMPARE_OP            8  is
            146_0  COME_FROM           134  '134'
              146  POP_JUMP_IF_TRUE    158  'to 158'
              149  LOAD_ASSERT              AssertionError
              152  LOAD_CONST               'size limits only allowed when populate_values=False'
              155  RAISE_VARARGS_2       2  None

 L. 344       158  SETUP_LOOP          148  'to 309'
              161  LOAD_FAST             0  'self'
              164  LOAD_ATTR             0  '_area_bounds'
              167  GET_ITER         
              168  FOR_ITER            134  'to 305'
              171  UNPACK_SEQUENCE_2     2 
              174  STORE_FAST            7  'area'
              177  UNPACK_SEQUENCE_2     2 
              180  STORE_FAST            8  'row_bounds'
              183  STORE_FAST            9  'col_bounds'

 L. 345       186  LOAD_FAST             7  'area'
              189  LOAD_ATTR             5  'Value'
              192  STORE_FAST           10  'v'

 L. 347       195  LOAD_FAST             8  'row_bounds'
              198  LOAD_CONST               0
              201  BINARY_SUBSCR    
              202  LOAD_FAST             8  'row_bounds'
              205  LOAD_CONST               1
              208  BINARY_SUBSCR    
              209  COMPARE_OP            2  ==
              212  POP_JUMP_IF_FALSE   250  'to 250'
              215  LOAD_FAST             9  'col_bounds'
              218  LOAD_CONST               0
              221  BINARY_SUBSCR    
              222  LOAD_FAST             9  'col_bounds'
              225  LOAD_CONST               1
              228  BINARY_SUBSCR    
              229  COMPARE_OP            2  ==
            232_0  COME_FROM           212  '212'
              232  POP_JUMP_IF_FALSE   250  'to 250'

 L. 348       235  LOAD_FAST            10  'v'
              238  BUILD_LIST_1          1 
              241  BUILD_LIST_1          1 
              244  STORE_FAST           10  'v'
              247  JUMP_FORWARD          0  'to 250'
            250_0  COME_FROM           247  '247'

 L. 349       250  LOAD_FAST            10  'v'
              253  LOAD_FAST             6  'm'
              256  LOAD_FAST             8  'row_bounds'
              259  LOAD_CONST               0
              262  BINARY_SUBSCR    
              263  LOAD_FAST             8  'row_bounds'
              266  LOAD_CONST               1
              269  BINARY_SUBSCR    
              270  LOAD_CONST               1
              273  BINARY_ADD       
              274  BUILD_SLICE_2         2 
              277  LOAD_FAST             9  'col_bounds'
              280  LOAD_CONST               0
              283  BINARY_SUBSCR    
              284  LOAD_FAST             9  'col_bounds'
              287  LOAD_CONST               1
              290  BINARY_SUBSCR    
              291  LOAD_CONST               1
              294  BINARY_ADD       
              295  BUILD_SLICE_2         2 
              298  BUILD_TUPLE_2         2 
              301  STORE_SUBSCR     
              302  JUMP_BACK           168  'to 168'
              305  POP_BLOCK        
            306_0  COME_FROM           158  '158'
              306  JUMP_FORWARD          0  'to 309'
            309_0  COME_FROM           158  '158'

 L. 350       309  LOAD_FAST             6  'm'
              312  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 309

    def intersects(self, rangeOther):
        app = self._full_xlRange.Application
        return app.Intersect(self._full_xlRange, rangeOther._full_xlRange) != None

    @property
    @enable_caching
    def dimensions(self):
        """Gives the tuple (num rows, num columns). If applicable for this range, hidden cells are excluded"""
        return (
         self.num_rows, self.num_columns)

    @property
    def _unfiltered_dimensions(self):
        assert self._full_xlRange.Areas.Count == 1
        return (self._full_xlRange.Rows.Count, self._full_xlRange.Columns.Count)

    @property
    def num_rows(self):
        return self._get_collapsed_matrix(populate_values=False).num_rows

    @property
    def num_columns(self):
        return self._get_collapsed_matrix(populate_values=False).num_columns

    @cache_result
    def normalize(self):
        """Return a normalized version of this range. The returned range is reduced to
        encompass only in-use areas of the worksheet, and (if applicable) the data area of its table"""
        from xl.sheet import Worksheet
        normalized = _trim_xlRange(self._full_xlRange)
        s = Worksheet(self._full_xlRange.Worksheet)
        t = s._find_table_containing_range(self)
        if t != None:
            normalized = self._full_xlRange.Application.Intersect(normalized, t.rData._full_xlRange)
        return self._with_xlRange(normalized)

    def _with_unfiltered_size(self, rows=0, cols=0):
        assert rows > 0 and cols > 0
        r1, c1 = self._full_xlRange.Row, self._full_xlRange.Column
        r2 = r1 + int(rows) - 1
        c2 = c1 + int(cols) - 1
        ws = self._full_xlRange.Worksheet
        return self._with_xlRange(_xlRange_from_corners(ws, r1, c1, r2, c2))

    def _adjust_unfiltered_size(self, rows=0, cols=0):
        return self._with_unfiltered_size(self._full_xlRange.Rows.Count + rows, self._full_xlRange.Columns.Count + cols)

    def _offset_unfiltered(self, rows=0, cols=0):
        fr = self._full_xlRange
        size_r, size_c = fr.Rows.Count, fr.Columns.Count
        r1, c1 = fr.Row + rows, fr.Column + cols
        r2 = r1 + size_r - 1
        c2 = c1 + size_c - 1
        ws = self._full_xlRange.Worksheet
        return self._with_xlRange(_xlRange_from_corners(ws, r1, c1, r2, c2))

    @property
    def row(self):
        """Returns the sheet-wide row index of the top-most unfiltered cells"""
        return self._get_collapsed_matrix(populate_values=False, row_limit=1, column_limit=1).row_indices[0]

    @property
    def column(self):
        """Returns the sheet-wide column index of the left-most unfiltered cells"""
        return self._get_collapsed_matrix(populate_values=False, row_limit=1, column_limit=1).column_indices[0]

    @cache_result
    @property
    def containing_table(self):
        """If this range is partially or fully contained in a Table, returns the table
        Otherwise, returns None"""
        from xl.sheet import Worksheet
        ws = Worksheet(self._full_xlRange.Worksheet)
        return ws._find_table_containing_range(self)

    def __setitem__(self, index, value):
        raise NotImplementedError('setting ranges')

    def __len__(self):
        return self._effective_xlRange.Count


class _Dimension(object):
    pass


class _RowDimension(_Dimension):

    def position(self, xlRange):
        return xlRange.Row

    def of(self, xlRange):
        return xlRange.Rows

    def entire(self, xlRange):
        return xlRange.EntireRow

    @property
    def other(self):
        return _ColumnDimension


_RowDimension = _RowDimension()

class _ColumnDimension(_Dimension):

    def position(self, xlRange):
        return xlRange.Column

    def of(self, xlRange):
        return xlRange.Columns

    def entire(self, xlRange):
        return xlRange.EntireColumn

    @property
    def other(self):
        return _RowDimension


_ColumnDimension = _ColumnDimension()

class Vector(Range):

    @enable_caching
    def set(self, data):
        """Updates this vector's cells. The `data` parameter should be an iterable returning cell values.
        Not all cells need to be specified. Values are filled in from the top-left of the vector, and
        additional cells are left unmodified. For example::

            workbook.get("A:A").set([1,2,3])

        sets the first 3 values of column A"""
        if isinstance(data, basestring):
            raise ValueError('Vector-shaped Range requires a list of values (was given a string)')
        is_row_vector = self.num_rows == 1
        if is_row_vector:
            vec_data = [data]
        else:
            vec_data = [ [v] for v in data ]
        self._set_2d(vec_data)

    def get(self):
        """Returns a list representation of this vector's values (containing values for low indices first)

        The number of elements returned may be less than num_rows / num_columns; the fetch is clipped to the 'used range' of the worksheet"""
        vals_2d = self._get_2D()
        if len(vals_2d) == 1:
            return vals_2d[0]
        else:
            return [ v for v, in vals_2d ]

    def __getitem__(self, index):
        if not CacheManager.is_caching_enabled:
            raise Exception('Repeatedly indexing into a vector has severe performance implications when caching is disabled. ' + 'Enable caching while indexing the vector (see CacheManager), or consider using get() instead')
        return self.get()[index]

    def __iter__(self):
        return iter(self.get())


class RowVector(Vector):
    _vector_dim = _RowDimension


class ColumnVector(Vector):
    _vector_dim = _ColumnDimension


class Scalar(Range):

    def set(self, data):
        """Updates this scalar range's cell. The `data` parameter
        may be a single value, or a (non-string) iterable that returns one item."""
        if not isinstance(data, basestring):
            try:
                l = list(data)
                if len(l) != 1:
                    raise ValueError('set() for a scalar Range must be given a scalar value, or an iterable giving one value')
                data = l[0]
            except TypeError:
                pass

        self._set_2d([[data]])

    def get--- This code section failed: ---

 L. 526         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  '_get_2D'
                6  CALL_FUNCTION_0       0  None
                9  STORE_FAST            1  'vals_2d'

 L. 527        12  LOAD_GLOBAL           1  'len'
               15  LOAD_FAST             1  'vals_2d'
               18  CALL_FUNCTION_1       1  None
               21  LOAD_CONST               0
               24  COMPARE_OP            2  ==
               27  UNARY_NOT        
               28  POP_JUMP_IF_TRUE     40  'to 40'
               31  LOAD_ASSERT              AssertionError
               34  LOAD_CONST               'Scalar range has no value. Filtered?'
               37  RAISE_VARARGS_2       2  None

 L. 528        40  LOAD_GLOBAL           1  'len'
               43  LOAD_FAST             1  'vals_2d'
               46  CALL_FUNCTION_1       1  None
               49  LOAD_CONST               1
               52  COMPARE_OP            2  ==
               55  POP_JUMP_IF_FALSE    80  'to 80'
               58  LOAD_GLOBAL           1  'len'
               61  LOAD_FAST             1  'vals_2d'
               64  LOAD_CONST               0
               67  BINARY_SUBSCR    
               68  CALL_FUNCTION_1       1  None
               71  LOAD_CONST               1
               74  COMPARE_OP            2  ==
             77_0  COME_FROM            55  '55'
               77  POP_JUMP_IF_TRUE     86  'to 86'
               80  LOAD_ASSERT              AssertionError
               83  RAISE_VARARGS_1       1  None

 L. 529        86  LOAD_FAST             1  'vals_2d'
               89  LOAD_CONST               0
               92  BINARY_SUBSCR    
               93  LOAD_CONST               0
               96  BINARY_SUBSCR    
               97  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 97

    def __getitem__(self, index):
        if not index == 0:
            raise IndexError('Scalar range. Only index 0 is allowed')
        return self.get()

    def __iter__(self):
        """Returns an iterator yielding a single value (that of the single cell)"""
        return iter([self.get()])


class Matrix(Range):

    def set(self, data):
        """Updates the matrix's cells. `data` should be of the form::

            [[row values, ...], [row values,...], ...]
        
        Not all rows and columns need to be specified; the given values fill
        the top-left corner of the matrix, and the remaining cells are unchanged. For example::

            workbook.get("A:C").set([[1,2], [3,4]])

        only modifies A1:B2"""
        self._set_2d(data)

    def get(self):
        """Returns a list-of-lists representation in the form::

            [[row values,...], [row values,...], ...]

        All row lists have the same length. The number of rows / columns returned may be less than num_rows / num_columns;
        the fetch is clipped to the 'used range' of the worksheet"""
        return self._get_2D()

    def __getitem__(self, index):
        """Not supported for Matrix"""
        raise NotImplementedError('2D indexing is not supported. Call get() instead')

    def __iter__(self):
        """Not supported for Matrix"""
        raise NotImplementedError('2D iteration is not supported. Call get() instead')


def _trim_xlRange(xlRange):
    """Trim an xlRange to be within the range actually used. This prevents, for example, a range such as A:A
    from including empty cells down to the row limit
    
    A new xlRange is returned"""
    xlApp = xlRange.Application
    xlRangeUsed = xlRange.Worksheet.UsedRange
    xlRange = xlApp.Intersect(xlRange, xlRangeUsed)
    if xlRange == None:
        raise ExcelRangeError('Range is completely outside the used ranged')
    return xlRange


def _xlRange_from_corners(xlWorksheet, r1, c1, r2, c2):
    """Get excel Range for (row1,column1) to (row2, column2), inclusive."""
    return xlWorksheet.Range(xlWorksheet.Cells(r1, c1), xlWorksheet.Cells(r2, c2))


def _xlRange_parse--- This code section failed: ---

 L. 598         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             1  'obj'
                6  LOAD_GLOBAL           1  'basestring'
                9  CALL_FUNCTION_2       2  None
               12  POP_JUMP_IF_TRUE     24  'to 24'
               15  LOAD_ASSERT              AssertionError
               18  LOAD_CONST               'Expected a range string'
               21  RAISE_VARARGS_2       2  None

 L. 599        24  SETUP_EXCEPT         17  'to 44'

 L. 600        27  LOAD_FAST             0  'xlWorksheet'
               30  LOAD_ATTR             3  'Range'
               33  LOAD_FAST             1  'obj'
               36  CALL_FUNCTION_1       1  None
               39  RETURN_VALUE     
               40  POP_BLOCK        
               41  JUMP_FORWARD         44  'to 88'
             44_0  COME_FROM            24  '24'

 L. 601        44  DUP_TOP          
               45  LOAD_GLOBAL           4  'com_utils'
               48  LOAD_ATTR             5  'com_error'
               51  COMPARE_OP           10  exception-match
               54  POP_JUMP_IF_FALSE    87  'to 87'
               57  POP_TOP          
               58  STORE_FAST            2  'e'
               61  POP_TOP          

 L. 603        62  LOAD_GLOBAL           6  'ExcelRangeError'
               65  LOAD_CONST               'failed to find range: '
               68  LOAD_GLOBAL           7  'str'
               71  LOAD_FAST             1  'obj'
               74  CALL_FUNCTION_1       1  None
               77  BINARY_ADD       
               78  CALL_FUNCTION_1       1  None
               81  RAISE_VARARGS_1       1  None
               84  JUMP_FORWARD          1  'to 88'
               87  END_FINALLY      
             88_0  COME_FROM            87  '87'
             88_1  COME_FROM            41  '41'

Parse error at or near `COME_FROM' instruction at offset 88_0


def _xlRanges_equivalent(xlRange_a, xlRange_b):
    if xlRange_a.Count != xlRange_b.Count:
        return False
    else:
        inter = xlRange_a.Application.Intersect(xlRange_a, xlRange_b)
        if inter is None:
            return False
        return inter.Count == xlRange_a.Count