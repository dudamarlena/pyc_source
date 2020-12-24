# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\extra\pandas\impl.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 24350 bytes
from collections import OrderedDict, abc
from copy import copy
from typing import Any, List, Sequence, Set, Union
import attr, numpy as np, pandas
import hypothesis.extra.numpy as npst
import hypothesis.internal.conjecture.utils as cu
import hypothesis.strategies._internal.core as st
from hypothesis.control import reject
from hypothesis.errors import InvalidArgument
from hypothesis.internal.coverage import check, check_function
from hypothesis.internal.validation import check_type, check_valid_interval, check_valid_size, try_convert
from hypothesis.strategies._internal.strategies import Ex
try:
    from pandas.api.types import is_categorical_dtype
except ImportError:

    def is_categorical_dtype(dt):
        if isinstance(dt, np.dtype):
            return False
        return dt == 'category'


else:

    def dtype_for_elements_strategy(s):
        return st.shared((s.map(lambda x: pandas.Series([x]).dtype)),
          key=(
         'hypothesis.extra.pandas.dtype_for_elements_strategy', s))


    def infer_dtype_if_necessary(dtype, values, elements, draw):
        if dtype is None:
            if not values:
                return draw(dtype_for_elements_strategy(elements))
        return dtype


    @check_function
    def elements_and_dtype(elements, dtype, source=None):
        if source is None:
            prefix = ''
        else:
            prefix = '%s.' % (source,)
        if elements is not None:
            st.check_strategy(elements, '%selements' % (prefix,))
        else:
            with check('dtype is not None'):
                if dtype is None:
                    raise InvalidArgument('At least one of %(prefix)selements or %(prefix)sdtype must be provided.' % {'prefix': prefix})
        with check('is_categorical_dtype'):
            if is_categorical_dtype(dtype):
                raise InvalidArgument('%sdtype is categorical, which is currently unsupported' % (prefix,))
        dtype = try_convert(np.dtype, dtype, 'dtype')
        if elements is None:
            elements = npst.from_dtype(dtype)
        else:
            if dtype is not None:

                def convert_element--- This code section failed: ---

 L.  95         0  LOAD_STR                 'draw(%selements)'
                2  LOAD_DEREF               'prefix'
                4  BUILD_TUPLE_1         1 
                6  BINARY_MODULO    
                8  STORE_FAST               'name'

 L.  96        10  SETUP_FINALLY        34  'to 34'

 L.  97        12  LOAD_GLOBAL              np
               14  LOAD_ATTR                array
               16  LOAD_FAST                'value'
               18  BUILD_LIST_1          1 
               20  LOAD_DEREF               'dtype'
               22  LOAD_CONST               ('dtype',)
               24  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               26  LOAD_CONST               0
               28  BINARY_SUBSCR    
               30  POP_BLOCK        
               32  RETURN_VALUE     
             34_0  COME_FROM_FINALLY    10  '10'

 L.  98        34  DUP_TOP          
               36  LOAD_GLOBAL              TypeError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    80  'to 80'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.  99        48  LOAD_GLOBAL              InvalidArgument

 L. 100        50  LOAD_STR                 'Cannot convert %s=%r of type %s to dtype %s'

 L. 101        52  LOAD_FAST                'name'
               54  LOAD_FAST                'value'
               56  LOAD_GLOBAL              type
               58  LOAD_FAST                'value'
               60  CALL_FUNCTION_1       1  ''
               62  LOAD_ATTR                __name__
               64  LOAD_DEREF               'dtype'
               66  LOAD_ATTR                str
               68  BUILD_TUPLE_4         4 

 L. 100        70  BINARY_MODULO    

 L.  99        72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
               76  POP_EXCEPT       
               78  JUMP_FORWARD        120  'to 120'
             80_0  COME_FROM            40  '40'

 L. 103        80  DUP_TOP          
               82  LOAD_GLOBAL              ValueError
               84  COMPARE_OP               exception-match
               86  POP_JUMP_IF_FALSE   118  'to 118'
               88  POP_TOP          
               90  POP_TOP          
               92  POP_TOP          

 L. 104        94  LOAD_GLOBAL              InvalidArgument

 L. 105        96  LOAD_STR                 'Cannot convert %s=%r to type %s'
               98  LOAD_FAST                'name'
              100  LOAD_FAST                'value'
              102  LOAD_DEREF               'dtype'
              104  LOAD_ATTR                str
              106  BUILD_TUPLE_3         3 
              108  BINARY_MODULO    

 L. 104       110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            86  '86'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'
            120_1  COME_FROM            78  '78'

Parse error at or near `POP_TOP' instruction at offset 44

                elements = elements.map(convert_element)
        assert elements is not None
        return (
         elements, dtype)


    class ValueIndexStrategy(st.SearchStrategy):

        def __init__(self, elements, dtype, min_size, max_size, unique):
            super().__init__()
            self.elements = elements
            self.dtype = dtype
            self.min_size = min_size
            self.max_size = max_size
            self.unique = unique

        def do_draw(self, data):
            result = []
            seen = set()
            iterator = cu.many(data,
              min_size=(self.min_size),
              max_size=(self.max_size),
              average_size=((self.min_size + self.max_size) / 2))
            while iterator.more():
                elt = data.draw(self.elements)
                if self.unique:
                    if elt in seen:
                        iterator.reject()
                    else:
                        seen.add(elt)
                result.append(elt)

            dtype = infer_dtype_if_necessary(dtype=(self.dtype),
              values=result,
              elements=(self.elements),
              draw=(data.draw))
            return pandas.Index(result, dtype=dtype, tupleize_cols=False)


    DEFAULT_MAX_SIZE = 10

    @st.cacheable
    @st.defines_strategy
    def range_indexes(min_size: int=0, max_size: int=None) -> st.SearchStrategy[pandas.RangeIndex]:
        """Provides a strategy which generates an :class:`~pandas.Index` whose
    values are 0, 1, ..., n for some n.

    Arguments:

    * min_size is the smallest number of elements the index can have.
    * max_size is the largest number of elements the index can have. If None
      it will default to some suitable value based on min_size.
    """
        check_valid_size(min_size, 'min_size')
        check_valid_size(max_size, 'max_size')
        if max_size is None:
            max_size = min([min_size + DEFAULT_MAX_SIZE, 9223372036854775807])
        check_valid_interval(min_size, max_size, 'min_size', 'max_size')
        return st.integers(min_size, max_size).map(pandas.RangeIndex)


    @st.cacheable
    @st.defines_strategy
    def indexes(elements: st.SearchStrategy[Ex]=None, dtype: Any=None, min_size: int=0, max_size: int=None, unique: bool=True) -> st.SearchStrategy[pandas.Index]:
        """Provides a strategy for producing a :class:`pandas.Index`.

    Arguments:

    * elements is a strategy which will be used to generate the individual
      values of the index. If None, it will be inferred from the dtype. Note:
      even if the elements strategy produces tuples, the generated value
      will not be a MultiIndex, but instead be a normal index whose elements
      are tuples.
    * dtype is the dtype of the resulting index. If None, it will be inferred
      from the elements strategy. At least one of dtype or elements must be
      provided.
    * min_size is the minimum number of elements in the index.
    * max_size is the maximum number of elements in the index. If None then it
      will default to a suitable small size. If you want larger indexes you
      should pass a max_size explicitly.
    * unique specifies whether all of the elements in the resulting index
      should be distinct.
    """
        check_valid_size(min_size, 'min_size')
        check_valid_size(max_size, 'max_size')
        check_valid_interval(min_size, max_size, 'min_size', 'max_size')
        check_type(bool, unique, 'unique')
        elements, dtype = elements_and_dtype(elements, dtype)
        if max_size is None:
            max_size = min_size + DEFAULT_MAX_SIZE
        return ValueIndexStrategy(elements, dtype, min_size, max_size, unique)


    @st.defines_strategy
    def series(elements: st.SearchStrategy[Ex]=None, dtype: Any=None, index: st.SearchStrategy[Union[(Sequence, pandas.Index)]]=None, fill: st.SearchStrategy[Ex]=None, unique: bool=False) -> st.SearchStrategy[pandas.Series]:
        """Provides a strategy for producing a :class:`pandas.Series`.

    Arguments:

    * elements: a strategy that will be used to generate the individual
      values in the series. If None, we will attempt to infer a suitable
      default from the dtype.

    * dtype: the dtype of the resulting series and may be any value
      that can be passed to :class:`numpy.dtype`. If None, will use
      pandas's standard behaviour to infer it from the type of the elements
      values. Note that if the type of values that comes out of your
      elements strategy varies, then so will the resulting dtype of the
      series.

    * index: If not None, a strategy for generating indexes for the
      resulting Series. This can generate either :class:`pandas.Index`
      objects or any sequence of values (which will be passed to the
      Index constructor).

      You will probably find it most convenient to use the
      :func:`~hypothesis.extra.pandas.indexes` or
      :func:`~hypothesis.extra.pandas.range_indexes` function to produce
      values for this argument.

    Usage:

    .. code-block:: pycon

        >>> series(dtype=int).example()
        0   -2001747478
        1    1153062837
    """
        if index is None:
            index = range_indexes()
        else:
            st.check_strategy(index)
        elements, dtype = elements_and_dtype(elements, dtype)
        index_strategy = index

        @st.composite
        def result(draw):
            index = draw(index_strategy)
            if len(index) > 0:
                if dtype is not None:
                    result_data = draw(npst.arrays(dtype=dtype,
                      elements=elements,
                      shape=(len(index)),
                      fill=fill,
                      unique=unique))
                else:
                    result_data = list(draw(npst.arrays(dtype=object,
                      elements=elements,
                      shape=(len(index)),
                      fill=fill,
                      unique=unique)))
                return pandas.Series(result_data, index=index, dtype=dtype)
            return pandas.Series((),
              index=index,
              dtype=(dtype if dtype is not None else draw(dtype_for_elements_strategy(elements))))

        return result()


    @attr.s(slots=True)
    class column:
        __doc__ = 'Data object for describing a column in a DataFrame.\n\n    Arguments:\n\n    * name: the column name, or None to default to the column position. Must\n      be hashable, but can otherwise be any value supported as a pandas column\n      name.\n    * elements: the strategy for generating values in this column, or None\n      to infer it from the dtype.\n    * dtype: the dtype of the column, or None to infer it from the element\n      strategy. At least one of dtype or elements must be provided.\n    * fill: A default value for elements of the column. See\n      :func:`~hypothesis.extra.numpy.arrays` for a full explanation.\n    * unique: If all values in this column should be distinct.\n    '
        name = attr.ib(default=None)
        elements = attr.ib(default=None)
        dtype = attr.ib(default=None)
        fill = attr.ib(default=None)
        unique = attr.ib(default=False)


    def columns(names_or_number: Union[(int, Sequence[str])], dtype: Any=None, elements: st.SearchStrategy[Ex]=None, fill: st.SearchStrategy[Ex]=None, unique: bool=False) -> List[column]:
        """A convenience function for producing a list of :class:`column` objects
    of the same general shape.

    The names_or_number argument is either a sequence of values, the
    elements of which will be used as the name for individual column
    objects, or a number, in which case that many unnamed columns will
    be created. All other arguments are passed through verbatim to
    create the columns.
    """
        if isinstance(names_or_number, (int, float)):
            names = [
             None] * names_or_number
        else:
            names = list(names_or_number)
        return [column(name=n, dtype=dtype, elements=elements, fill=fill, unique=unique) for n in names]


    @st.defines_strategy
    def data_frames(columns: Sequence[column]=None, rows: st.SearchStrategy[Union[(dict, Sequence[Any])]]=None, index: st.SearchStrategy[Ex]=None) -> st.SearchStrategy[pandas.DataFrame]:
        """Provides a strategy for producing a :class:`pandas.DataFrame`.

    Arguments:

    * columns: An iterable of :class:`column` objects describing the shape
      of the generated DataFrame.

    * rows: A strategy for generating a row object. Should generate
      either dicts mapping column names to values or a sequence mapping
      column position to the value in that position (note that unlike the
      :class:`pandas.DataFrame` constructor, single values are not allowed
      here. Passing e.g. an integer is an error, even if there is only one
      column).

      At least one of rows and columns must be provided. If both are
      provided then the generated rows will be validated against the
      columns and an error will be raised if they don't match.

      Caveats on using rows:

      * In general you should prefer using columns to rows, and only use
        rows if the columns interface is insufficiently flexible to
        describe what you need - you will get better performance and
        example quality that way.
      * If you provide rows and not columns, then the shape and dtype of
        the resulting DataFrame may vary. e.g. if you have a mix of int
        and float in the values for one column in your row entries, the
        column will sometimes have an integral dtype and sometimes a float.

    * index: If not None, a strategy for generating indexes for the
      resulting DataFrame. This can generate either :class:`pandas.Index`
      objects or any sequence of values (which will be passed to the
      Index constructor).

      You will probably find it most convenient to use the
      :func:`~hypothesis.extra.pandas.indexes` or
      :func:`~hypothesis.extra.pandas.range_indexes` function to produce
      values for this argument.

    Usage:

    The expected usage pattern is that you use :class:`column` and
    :func:`columns` to specify a fixed shape of the DataFrame you want as
    follows. For example the following gives a two column data frame:

    .. code-block:: pycon

        >>> from hypothesis.extra.pandas import column, data_frames
        >>> data_frames([
        ... column('A', dtype=int), column('B', dtype=float)]).example()
                    A              B
        0  2021915903  1.793898e+232
        1  1146643993            inf
        2 -2096165693   1.000000e+07

    If you want the values in different columns to interact in some way you
    can use the rows argument. For example the following gives a two column
    DataFrame where the value in the first column is always at most the value
    in the second:

    .. code-block:: pycon

        >>> from hypothesis.extra.pandas import column, data_frames
        >>> import hypothesis.strategies as st
        >>> data_frames(
        ...     rows=st.tuples(st.floats(allow_nan=False),
        ...                    st.floats(allow_nan=False)).map(sorted)
        ... ).example()
                       0             1
        0  -3.402823e+38  9.007199e+15
        1 -1.562796e-298  5.000000e-01

    You can also combine the two:

    .. code-block:: pycon

        >>> from hypothesis.extra.pandas import columns, data_frames
        >>> import hypothesis.strategies as st
        >>> data_frames(
        ...     columns=columns(["lo", "hi"], dtype=float),
        ...     rows=st.tuples(st.floats(allow_nan=False),
        ...                    st.floats(allow_nan=False)).map(sorted)
        ... ).example()
                 lo            hi
        0   9.314723e-49  4.353037e+45
        1  -9.999900e-01  1.000000e+07
        2 -2.152861e+134 -1.069317e-73

    (Note that the column dtype must still be specified and will not be
    inferred from the rows. This restriction may be lifted in future).

    Combining rows and columns has the following behaviour:

    * The column names and dtypes will be used.
    * If the column is required to be unique, this will be enforced.
    * Any values missing from the generated rows will be provided using the
      column's fill.
    * Any values in the row not present in the column specification (if
      dicts are passed, if there are keys with no corresponding column name,
      if sequences are passed if there are too many items) will result in
      InvalidArgument being raised.
    """
        if index is None:
            index = range_indexes()
        else:
            st.check_strategy(index)
        index_strategy = index
        if columns is None:
            if rows is None:
                raise InvalidArgument('At least one of rows and columns must be provided')
            else:

                @st.composite
                def rows_only(draw):
                    index = draw(index_strategy)

                    @check_function
                    def row():
                        result = draw(rows)
                        check_type(abc.Iterable, result, 'draw(row)')
                        return result

                    if len(index) > 0:
                        return pandas.DataFrame([row() for _ in index], index=index)
                    base = pandas.DataFrame([row()])
                    return base.drop(0)

                return rows_only()
        assert columns is not None
        cols = try_convert(tuple, columns, 'columns')
        rewritten_columns = []
        column_names = set()
        for i, c in enumerate(cols):
            check_type(column, c, 'columns[%d]' % (i,))
            c = copy(c)
            if c.name is None:
                label = 'columns[%d]' % (i,)
                c.name = i
            else:
                label = c.name
            try:
                hash(c.name)
            except TypeError:
                raise InvalidArgument('Column names must be hashable, but columns[%d].name was %r of type %s, which cannot be hashed.' % (
                 i, c.name, type(c.name).__name__))
            else:
                if c.name in column_names:
                    raise InvalidArgument('duplicate definition of column name %r' % (c.name,))
                column_names.add(c.name)
                c.elements, c.dtype = elements_and_dtype(c.elements, c.dtype, label)
                if c.dtype is None:
                    if rows is not None:
                        raise InvalidArgument('Must specify a dtype for all columns when combining rows with columns.')
                c.fill = npst.fill_for(fill=(c.fill),
                  elements=(c.elements),
                  unique=(c.unique),
                  name=label)
                rewritten_columns.append(c)
        else:
            if rows is None:

                @st.composite
                def just_draw_columns(draw):
                    index = draw(index_strategy)
                    local_index_strategy = st.just(index)
                    data = OrderedDict(((c.name, None) for c in rewritten_columns))
                    columns_without_fill = [c for c in rewritten_columns if c.fill.is_empty]
                    if columns_without_fill:
                        for c in columns_without_fill:
                            data[c.name] = pandas.Series(np.zeros(shape=(len(index)), dtype=(c.dtype)),
                              index=index)
                        else:
                            seen = {set():c.name for c in columns_without_fill if c.unique if c.unique}
                            for i in range(len(index)):
                                for c in columns_without_fill:
                                    if c.unique:
                                        for _ in range(5):
                                            value = draw(c.elements)
                                            if value not in seen[c.name]:
                                                seen[c.name].add(value)
                                                break
                                        else:
                                            reject()

                                    else:
                                        value = draw(c.elements)
                                    data[c.name][i] = value

                    for c in rewritten_columns:
                        if not c.fill.is_empty:
                            data[c.name] = draw(series(index=local_index_strategy,
                              dtype=(c.dtype),
                              elements=(c.elements),
                              fill=(c.fill),
                              unique=(c.unique)))
                        return pandas.DataFrame(data, index=index)

                return just_draw_columns()

            @st.composite
            def assign_rows--- This code section failed: ---

 L. 604         0  LOAD_FAST                'draw'
                2  LOAD_DEREF               'index_strategy'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_DEREF              'index'

 L. 606         8  LOAD_GLOBAL              pandas
               10  LOAD_ATTR                DataFrame

 L. 607        12  LOAD_GLOBAL              OrderedDict
               14  LOAD_CLOSURE             'index'
               16  BUILD_TUPLE_1         1 
               18  LOAD_GENEXPR             '<code_object <genexpr>>'
               20  LOAD_STR                 'data_frames.<locals>.assign_rows.<locals>.<genexpr>'
               22  MAKE_FUNCTION_8          'closure'

 L. 614        24  LOAD_DEREF               'rewritten_columns'

 L. 607        26  GET_ITER         
               28  CALL_FUNCTION_1       1  ''
               30  CALL_FUNCTION_1       1  ''

 L. 616        32  LOAD_DEREF               'index'

 L. 606        34  LOAD_CONST               ('index',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  STORE_FAST               'result'

 L. 619        40  BUILD_MAP_0           0 
               42  STORE_FAST               'fills'

 L. 621        44  LOAD_GLOBAL              any
               46  LOAD_GENEXPR             '<code_object <genexpr>>'
               48  LOAD_STR                 'data_frames.<locals>.assign_rows.<locals>.<genexpr>'
               50  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               52  LOAD_DEREF               'rewritten_columns'
               54  GET_ITER         
               56  CALL_FUNCTION_1       1  ''
               58  CALL_FUNCTION_1       1  ''
               60  STORE_FAST               'any_unique'

 L. 623        62  LOAD_FAST                'any_unique'
               64  POP_JUMP_IF_FALSE   102  'to 102'

 L. 624        66  LOAD_LISTCOMP            '<code_object <listcomp>>'
               68  LOAD_STR                 'data_frames.<locals>.assign_rows.<locals>.<listcomp>'
               70  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               72  LOAD_DEREF               'rewritten_columns'
               74  GET_ITER         
               76  CALL_FUNCTION_1       1  ''
               78  STORE_FAST               'all_seen'

 L. 625        80  LOAD_FAST                'all_seen'
               82  LOAD_CONST               -1
               84  BINARY_SUBSCR    
               86  LOAD_CONST               None
               88  COMPARE_OP               is
               90  POP_JUMP_IF_FALSE   102  'to 102'

 L. 626        92  LOAD_FAST                'all_seen'
               94  LOAD_METHOD              pop
               96  CALL_METHOD_0         0  ''
               98  POP_TOP          
              100  JUMP_BACK            80  'to 80'
            102_0  COME_FROM            90  '90'
            102_1  COME_FROM            64  '64'

 L. 628       102  LOAD_GLOBAL              range
              104  LOAD_GLOBAL              len
              106  LOAD_DEREF               'index'
              108  CALL_FUNCTION_1       1  ''
              110  CALL_FUNCTION_1       1  ''
              112  GET_ITER         
          114_116  FOR_ITER            566  'to 566'
              118  STORE_FAST               'row_index'

 L. 629       120  LOAD_GLOBAL              range
              122  LOAD_CONST               5
              124  CALL_FUNCTION_1       1  ''
              126  GET_ITER         
          128_130  FOR_ITER            558  'to 558'
              132  STORE_FAST               '_'

 L. 630       134  LOAD_FAST                'draw'
              136  LOAD_DEREF               'rows'
              138  CALL_FUNCTION_1       1  ''
              140  STORE_FAST               'original_row'

 L. 631       142  LOAD_FAST                'original_row'
              144  STORE_FAST               'row'

 L. 632       146  LOAD_GLOBAL              isinstance
              148  LOAD_FAST                'row'
              150  LOAD_GLOBAL              dict
              152  CALL_FUNCTION_2       2  ''
          154_156  POP_JUMP_IF_FALSE   352  'to 352'

 L. 633       158  LOAD_CONST               None
              160  BUILD_LIST_1          1 
              162  LOAD_GLOBAL              len
              164  LOAD_DEREF               'rewritten_columns'
              166  CALL_FUNCTION_1       1  ''
              168  BINARY_MULTIPLY  
              170  STORE_FAST               'as_list'

 L. 634       172  LOAD_GLOBAL              enumerate
              174  LOAD_DEREF               'rewritten_columns'
              176  CALL_FUNCTION_1       1  ''
              178  GET_ITER         
              180  FOR_ITER            298  'to 298'
              182  UNPACK_SEQUENCE_2     2 
              184  STORE_FAST               'i'
              186  STORE_FAST               'c'

 L. 635       188  SETUP_FINALLY       208  'to 208'

 L. 636       190  LOAD_FAST                'row'
              192  LOAD_FAST                'c'
              194  LOAD_ATTR                name
              196  BINARY_SUBSCR    
              198  LOAD_FAST                'as_list'
              200  LOAD_FAST                'i'
              202  STORE_SUBSCR     
              204  POP_BLOCK        
              206  JUMP_BACK           180  'to 180'
            208_0  COME_FROM_FINALLY   188  '188'

 L. 637       208  DUP_TOP          
              210  LOAD_GLOBAL              KeyError
              212  COMPARE_OP               exception-match
          214_216  POP_JUMP_IF_FALSE   294  'to 294'
              218  POP_TOP          
              220  POP_TOP          
              222  POP_TOP          

 L. 638       224  SETUP_FINALLY       242  'to 242'

 L. 639       226  LOAD_FAST                'fills'
              228  LOAD_FAST                'i'
              230  BINARY_SUBSCR    
              232  LOAD_FAST                'as_list'
              234  LOAD_FAST                'i'
              236  STORE_SUBSCR     
              238  POP_BLOCK        
              240  JUMP_FORWARD        290  'to 290'
            242_0  COME_FROM_FINALLY   224  '224'

 L. 640       242  DUP_TOP          
              244  LOAD_GLOBAL              KeyError
              246  COMPARE_OP               exception-match
          248_250  POP_JUMP_IF_FALSE   288  'to 288'
              252  POP_TOP          
              254  POP_TOP          
              256  POP_TOP          

 L. 641       258  LOAD_FAST                'draw'
              260  LOAD_FAST                'c'
              262  LOAD_ATTR                fill
              264  CALL_FUNCTION_1       1  ''
              266  LOAD_FAST                'fills'
              268  LOAD_FAST                'i'
              270  STORE_SUBSCR     

 L. 642       272  LOAD_FAST                'fills'
              274  LOAD_FAST                'i'
              276  BINARY_SUBSCR    
              278  LOAD_FAST                'as_list'
              280  LOAD_FAST                'i'
              282  STORE_SUBSCR     
              284  POP_EXCEPT       
              286  JUMP_FORWARD        290  'to 290'
            288_0  COME_FROM           248  '248'
              288  END_FINALLY      
            290_0  COME_FROM           286  '286'
            290_1  COME_FROM           240  '240'
              290  POP_EXCEPT       
              292  JUMP_BACK           180  'to 180'
            294_0  COME_FROM           214  '214'
              294  END_FINALLY      
              296  JUMP_BACK           180  'to 180'

 L. 643       298  LOAD_FAST                'row'
              300  GET_ITER         
            302_0  COME_FROM           312  '312'
              302  FOR_ITER            348  'to 348'
              304  STORE_FAST               'k'

 L. 644       306  LOAD_FAST                'k'
              308  LOAD_DEREF               'column_names'
              310  COMPARE_OP               not-in
          312_314  POP_JUMP_IF_FALSE   302  'to 302'

 L. 645       316  LOAD_GLOBAL              InvalidArgument

 L. 646       318  LOAD_STR                 'Row %r contains column %r not in columns %r)'

 L. 647       320  LOAD_FAST                'row'
              322  LOAD_FAST                'k'
              324  LOAD_LISTCOMP            '<code_object <listcomp>>'
              326  LOAD_STR                 'data_frames.<locals>.assign_rows.<locals>.<listcomp>'
              328  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              330  LOAD_DEREF               'rewritten_columns'
              332  GET_ITER         
              334  CALL_FUNCTION_1       1  ''
              336  BUILD_TUPLE_3         3 

 L. 646       338  BINARY_MODULO    

 L. 645       340  CALL_FUNCTION_1       1  ''
              342  RAISE_VARARGS_1       1  'exception instance'
          344_346  JUMP_BACK           302  'to 302'

 L. 649       348  LOAD_FAST                'as_list'
              350  STORE_FAST               'row'
            352_0  COME_FROM           154  '154'

 L. 650       352  LOAD_FAST                'any_unique'
          354_356  POP_JUMP_IF_FALSE   436  'to 436'

 L. 651       358  LOAD_CONST               False
              360  STORE_FAST               'has_duplicate'

 L. 652       362  LOAD_GLOBAL              zip
              364  LOAD_FAST                'all_seen'
              366  LOAD_FAST                'row'
              368  CALL_FUNCTION_2       2  ''
              370  GET_ITER         
              372  FOR_ITER            428  'to 428'
              374  UNPACK_SEQUENCE_2     2 
              376  STORE_FAST               'seen'
              378  STORE_FAST               'value'

 L. 653       380  LOAD_FAST                'seen'
              382  LOAD_CONST               None
              384  COMPARE_OP               is
          386_388  POP_JUMP_IF_FALSE   394  'to 394'

 L. 654   390_392  JUMP_BACK           372  'to 372'
            394_0  COME_FROM           386  '386'

 L. 655       394  LOAD_FAST                'value'
              396  LOAD_FAST                'seen'
              398  COMPARE_OP               in
          400_402  POP_JUMP_IF_FALSE   414  'to 414'

 L. 656       404  LOAD_CONST               True
              406  STORE_FAST               'has_duplicate'

 L. 657       408  POP_TOP          
          410_412  BREAK_LOOP          428  'to 428'
            414_0  COME_FROM           400  '400'

 L. 658       414  LOAD_FAST                'seen'
              416  LOAD_METHOD              add
              418  LOAD_FAST                'value'
              420  CALL_METHOD_1         1  ''
              422  POP_TOP          
          424_426  JUMP_BACK           372  'to 372'

 L. 659       428  LOAD_FAST                'has_duplicate'
          430_432  POP_JUMP_IF_FALSE   436  'to 436'

 L. 660       434  JUMP_BACK           128  'to 128'
            436_0  COME_FROM           430  '430'
            436_1  COME_FROM           354  '354'

 L. 661       436  LOAD_GLOBAL              list
              438  LOAD_GLOBAL              try_convert
              440  LOAD_GLOBAL              tuple
              442  LOAD_FAST                'row'
              444  LOAD_STR                 'draw(rows)'
              446  CALL_FUNCTION_3       3  ''
              448  CALL_FUNCTION_1       1  ''
              450  STORE_FAST               'row'

 L. 663       452  LOAD_GLOBAL              len
              454  LOAD_FAST                'row'
              456  CALL_FUNCTION_1       1  ''
              458  LOAD_GLOBAL              len
              460  LOAD_DEREF               'rewritten_columns'
              462  CALL_FUNCTION_1       1  ''
              464  COMPARE_OP               >
          466_468  POP_JUMP_IF_FALSE   496  'to 496'

 L. 664       470  LOAD_GLOBAL              InvalidArgument

 L. 666       472  LOAD_STR                 'Row %r contains too many entries. Has %d but expected at most %d'

 L. 669       474  LOAD_FAST                'original_row'
              476  LOAD_GLOBAL              len
              478  LOAD_FAST                'row'
              480  CALL_FUNCTION_1       1  ''
              482  LOAD_GLOBAL              len
              484  LOAD_DEREF               'rewritten_columns'
              486  CALL_FUNCTION_1       1  ''
              488  BUILD_TUPLE_3         3 

 L. 665       490  BINARY_MODULO    

 L. 664       492  CALL_FUNCTION_1       1  ''
              494  RAISE_VARARGS_1       1  'exception instance'
            496_0  COME_FROM           466  '466'

 L. 671       496  LOAD_GLOBAL              len
              498  LOAD_FAST                'row'
              500  CALL_FUNCTION_1       1  ''
              502  LOAD_GLOBAL              len
              504  LOAD_DEREF               'rewritten_columns'
              506  CALL_FUNCTION_1       1  ''
              508  COMPARE_OP               <
          510_512  POP_JUMP_IF_FALSE   542  'to 542'

 L. 672       514  LOAD_FAST                'row'
              516  LOAD_METHOD              append
              518  LOAD_FAST                'draw'
              520  LOAD_DEREF               'rewritten_columns'
              522  LOAD_GLOBAL              len
              524  LOAD_FAST                'row'
              526  CALL_FUNCTION_1       1  ''
              528  BINARY_SUBSCR    
              530  LOAD_ATTR                fill
              532  CALL_FUNCTION_1       1  ''
              534  CALL_METHOD_1         1  ''
              536  POP_TOP          
          538_540  JUMP_BACK           496  'to 496'
            542_0  COME_FROM           510  '510'

 L. 673       542  LOAD_FAST                'row'
              544  LOAD_FAST                'result'
              546  LOAD_ATTR                iloc
              548  LOAD_FAST                'row_index'
              550  STORE_SUBSCR     

 L. 674       552  POP_TOP          
              554  CONTINUE            114  'to 114'
              556  JUMP_BACK           128  'to 128'

 L. 676       558  LOAD_GLOBAL              reject
              560  CALL_FUNCTION_0       0  ''
              562  POP_TOP          
              564  JUMP_BACK           114  'to 114'

 L. 677       566  LOAD_FAST                'result'
              568  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 554

            return assign_rows()