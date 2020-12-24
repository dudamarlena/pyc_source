# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/serialization/numpy_records.py
# Compiled at: 2019-12-06 10:13:42
# Size of source mod 2**32: 14584 bytes
import six, logging, numpy as np
from pandas import DataFrame, MultiIndex, Series, DatetimeIndex, Index
from .._config import FAST_CHECK_DF_SERIALIZABLE
from .._util import NP_OBJECT_DTYPE
from ..exceptions import ArcticException
try:
    from pandas._libs.tslib import Timestamp
    from pandas._libs.tslibs.timezones import get_timezone
except ImportError:
    try:
        from pandas._libs.tslib import Timestamp, get_timezone
    except ImportError:
        from pandas.tslib import Timestamp, get_timezone

log = logging.getLogger(__name__)
DTN64_DTYPE = 'datetime64[ns]'

def set_fast_check_df_serializable(config):
    global FAST_CHECK_DF_SERIALIZABLE
    FAST_CHECK_DF_SERIALIZABLE = bool(config)


def _to_primitive(arr, string_max_len=None, forced_dtype=None):
    if arr.dtype.hasobject:
        if len(arr) > 0:
            if isinstance(arr[0], Timestamp):
                return np.array([t.value for t in arr], dtype=DTN64_DTYPE)
        elif forced_dtype is not None:
            casted_arr = arr.astype(dtype=forced_dtype, copy=False)
        else:
            if string_max_len is not None:
                casted_arr = np.array(arr.astype('U{:d}'.format(string_max_len)))
            else:
                casted_arr = np.array(list(arr))
        if np.array_equal(arr, casted_arr):
            return casted_arr
    return arr


def _multi_index_to_records(index, empty_index):
    if not empty_index:
        ix_vals = list(map(np.array, [index.get_level_values(i) for i in range(index.nlevels)]))
    else:
        ix_vals = [np.array([]) for n in index.names]
    index_names = list(index.names)
    count = 0
    for i, n in enumerate(index_names):
        if n is None:
            index_names[i] = 'level_%d' % count
            count += 1
            log.info('Level in MultiIndex has no name, defaulting to %s' % index_names[i])

    index_tz = [get_timezone(i.tz) if isinstance(i, DatetimeIndex) else None for i in index.levels]
    return (ix_vals, index_names, index_tz)


class PandasSerializer(object):

    def _index_to_records(self, df):
        metadata = {}
        index = df.index
        index_tz = None
        if isinstance(index, MultiIndex):
            ix_vals, index_names, index_tz = _multi_index_to_records(index, len(df) == 0)
        else:
            ix_vals = [
             index.values]
            index_names = list(index.names)
            if index_names[0] is None:
                index_names = [
                 'index']
                log.info("Index has no name, defaulting to 'index'")
            if isinstance(index, DatetimeIndex):
                if index.tz is not None:
                    index_tz = get_timezone(index.tz)
        if index_tz is not None:
            metadata['index_tz'] = index_tz
        metadata['index'] = index_names
        return (
         index_names, ix_vals, metadata)

    def _index_from_records(self, recarr):
        index = recarr.dtype.metadata['index']
        if len(index) == 1:
            rtn = Index((np.copy(recarr[str(index[0])])), name=(index[0]))
            if isinstance(rtn, DatetimeIndex):
                if 'index_tz' in recarr.dtype.metadata:
                    rtn = rtn.tz_localize('UTC').tz_convert(recarr.dtype.metadata['index_tz'])
        else:
            level_arrays = []
            index_tz = recarr.dtype.metadata.get('index_tz', [])
            for level_no, index_name in enumerate(index):
                level = Index(np.copy(recarr[str(index_name)]))
                if level_no < len(index_tz):
                    tz = index_tz[level_no]
                    if tz is not None:
                        if (isinstance(level, DatetimeIndex) or len(level)) == 0:
                            level = DatetimeIndex([], tz=tz)
                        else:
                            level = level.tz_localize('UTC').tz_convert(tz)
                level_arrays.append(level)

            rtn = MultiIndex.from_arrays(level_arrays, names=index)
        return rtn

    def _to_records(self, df, string_max_len=None, forced_dtype=None):
        """
        Similar to DataFrame.to_records()
        Differences:
            Attempt type conversion for pandas columns stored as objects (e.g. strings),
            as we can only store primitives in the ndarray.
            Use dtype metadata to store column and index names.

        string_max_len: integer - enforces a string size on the dtype, if any
                                  strings exist in the record
        """
        index_names, ix_vals, metadata = self._index_to_records(df)
        columns, column_vals, multi_column = self._column_data(df)
        if '' in columns:
            raise ArcticException('Cannot use empty string as a column name.')
        else:
            if multi_column is not None:
                metadata['multi_column'] = multi_column
            metadata['columns'] = columns
            names = index_names + columns
            arrays = []
            for arr, name in zip(ix_vals + column_vals, index_names + columns):
                arrays.append(_to_primitive(arr, string_max_len, forced_dtype=(None if forced_dtype is None else forced_dtype[name])))

            if forced_dtype is None:
                dtype = np.dtype([(str(x), v.dtype) if len(v.shape) == 1 else (str(x), v.dtype, v.shape[1]) for x, v in zip(names, arrays)],
                  metadata=metadata)
            else:
                dtype = forced_dtype
        rtn = np.rec.fromarrays(arrays, dtype=dtype, names=names)
        return (
         rtn, dtype)

    def fast_check_serializable--- This code section failed: ---

 L. 177         0  LOAD_FAST                'df'
                2  LOAD_ATTR                index
                4  LOAD_ATTR                dtype
                6  LOAD_FAST                'df'
                8  LOAD_ATTR                dtypes
               10  ROT_TWO          
               12  STORE_FAST               'i_dtype'
               14  STORE_DEREF              'f_dtypes'

 L. 178        16  LOAD_FAST                'df'
               18  LOAD_ATTR                index
               20  LOAD_ATTR                dtype
               22  LOAD_GLOBAL              NP_OBJECT_DTYPE
               24  COMPARE_OP               is
               26  STORE_FAST               'index_has_object'

 L. 179        28  LOAD_CLOSURE             'f_dtypes'
               30  BUILD_TUPLE_1         1 
               32  LOAD_LISTCOMP            '<code_object <listcomp>>'
               34  LOAD_STR                 'PandasSerializer.fast_check_serializable.<locals>.<listcomp>'
               36  MAKE_FUNCTION_8          'closure'
               38  LOAD_FAST                'df'
               40  LOAD_ATTR                columns
               42  GET_ITER         
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  STORE_FAST               'fields_with_object'

 L. 180        48  LOAD_FAST                'df'
               50  LOAD_ATTR                empty
               52  POP_JUMP_IF_TRUE     62  'to 62'
               54  LOAD_FAST                'index_has_object'
               56  POP_JUMP_IF_TRUE     94  'to 94'
               58  LOAD_FAST                'fields_with_object'
               60  POP_JUMP_IF_TRUE     94  'to 94'
             62_0  COME_FROM            52  '52'

 L. 181        62  LOAD_FAST                'self'
               64  LOAD_METHOD              _to_records
               66  LOAD_FAST                'df'
               68  LOAD_ATTR                iloc
               70  LOAD_CONST               None
               72  LOAD_CONST               10
               74  BUILD_SLICE_2         2 
               76  BINARY_SUBSCR    
               78  CALL_METHOD_1         1  '1 positional argument'
               80  UNPACK_SEQUENCE_2     2 
               82  STORE_FAST               'arr'
               84  STORE_FAST               '_'

 L. 182        86  LOAD_FAST                'arr'
               88  BUILD_MAP_0           0 
               90  BUILD_TUPLE_2         2 
               92  RETURN_VALUE     
             94_0  COME_FROM            60  '60'
             94_1  COME_FROM            56  '56'

 L. 185        94  LOAD_FAST                'df'
               96  LOAD_FAST                'fields_with_object'
               98  POP_JUMP_IF_FALSE   104  'to 104'
              100  LOAD_FAST                'fields_with_object'
              102  JUMP_FORWARD        116  'to 116'
            104_0  COME_FROM            98  '98'
              104  LOAD_FAST                'df'
              106  LOAD_ATTR                columns
              108  LOAD_CONST               None
              110  LOAD_CONST               2
              112  BUILD_SLICE_2         2 
              114  BINARY_SUBSCR    
            116_0  COME_FROM           102  '102'
              116  BINARY_SUBSCR    
              118  STORE_FAST               'df_objects_only'

 L. 187       120  LOAD_FAST                'self'
              122  LOAD_METHOD              _to_records
              124  LOAD_FAST                'df_objects_only'
              126  CALL_METHOD_1         1  '1 positional argument'
              128  UNPACK_SEQUENCE_2     2 
              130  STORE_FAST               'arr'
              132  STORE_DEREF              'dtype'

 L. 188       134  LOAD_FAST                'arr'
              136  LOAD_CLOSURE             'dtype'
              138  BUILD_TUPLE_1         1 
              140  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              142  LOAD_STR                 'PandasSerializer.fast_check_serializable.<locals>.<dictcomp>'
              144  MAKE_FUNCTION_8          'closure'
              146  LOAD_DEREF               'dtype'
              148  LOAD_ATTR                names
              150  GET_ITER         
              152  CALL_FUNCTION_1       1  '1 positional argument'
              154  BUILD_TUPLE_2         2 
              156  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 156

    def can_convert_to_records_without_objects(self, df, symbol):
        try:
            if FAST_CHECK_DF_SERIALIZABLE:
                arr, _ = self.fast_check_serializable(df)
            else:
                arr, _ = self._to_records(df)
        except Exception as e:
            try:
                log.warning('Pandas dataframe %s caused exception "%s" when attempting to convert to records. Saving as Blob.' % (
                 symbol, repr(e)))
                return False
            finally:
                e = None
                del e

        else:
            if arr.dtype.hasobject:
                log.warning('Pandas dataframe %s contains Objects, saving as Blob' % symbol)
                return False
            if any([len(x[0].shape) for x in arr.dtype.fields.values()]):
                log.warning('Pandas dataframe %s contains >1 dimensional arrays, saving as Blob' % symbol)
                return False
            return True

    def serialize(self, item, string_max_len=None, forced_dtype=None):
        raise NotImplementedError

    def deserialize(self, item, force_bytes_to_unicode=False):
        raise NotImplementedError


class SeriesSerializer(PandasSerializer):
    TYPE = 'series'

    def _column_data(self, s):
        if s.name is None:
            log.info("Series has no name, defaulting to 'values'")
        columns = [
         s.name if s.name else 'values']
        column_vals = [s.values]
        return (columns, column_vals, None)

    def deserialize(self, item, force_bytes_to_unicode=False):
        index = self._index_from_records(item)
        name = item.dtype.names[(-1)]
        data = item[name]
        if force_bytes_to_unicode:
            if six.PY2:
                if isinstance(name, (bytes, str)):
                    name = name.decode('utf-8')
            if len(data):
                if isinstance(data[0], bytes):
                    data = data.astype('unicode')
            if isinstance(index, MultiIndex):
                unicode_indexes = []
                for level in range(len(index.levels)):
                    _index = index.get_level_values(level)
                    if isinstance(_index[0], bytes):
                        _index = _index.astype('unicode')
                    unicode_indexes.append(_index)

                index = unicode_indexes
            else:
                if len(index):
                    if type(index[0]) == bytes:
                        index = index.astype('unicode')
        return Series.from_array(data, index=index, name=name)

    def serialize(self, item, string_max_len=None, forced_dtype=None):
        return self._to_records(item, string_max_len, forced_dtype)


class DataFrameSerializer(PandasSerializer):
    TYPE = 'df'

    def _column_data(self, df):
        columns = list(map(str, df.columns))
        if columns != list(df.columns):
            log.info('Dataframe column names converted to strings')
        column_vals = [df[c].values for c in df.columns]
        if isinstance(df.columns, MultiIndex):
            ix_vals, ix_names, _ = _multi_index_to_records(df.columns, False)
            vals = [list(val) for val in ix_vals]
            str_vals = [list(map(str, val)) for val in ix_vals]
            if vals != str_vals:
                log.info('Dataframe column names converted to strings')
            return (
             columns, column_vals, {'names':list(ix_names),  'values':str_vals})
        return (columns, column_vals, None)

    def deserialize(self, item, force_bytes_to_unicode=False):
        index = self._index_from_records(item)
        column_fields = [x for x in item.dtype.names if x not in item.dtype.metadata['index']]
        multi_column = item.dtype.metadata.get('multi_column')
        if len(item) == 0:
            rdata = item[column_fields] if len(column_fields) > 0 else None
            if multi_column is not None:
                columns = MultiIndex.from_arrays((multi_column['values']), names=(multi_column['names']))
                return DataFrame(rdata, index=index, columns=columns)
            return DataFrame(rdata, index=index)
            columns = item.dtype.metadata['columns']
            df = DataFrame(data=(item[column_fields]), index=index, columns=columns)
            if multi_column is not None:
                df.columns = MultiIndex.from_arrays((multi_column['values']), names=(multi_column['names']))
            if force_bytes_to_unicode:
                for c in df.select_dtypes(object):
                    if type(df[c].iloc[0]) == bytes:
                        df[c] = df[c].str.decode('utf-8')

                if isinstance(df.index, MultiIndex):
                    unicode_indexes = []
                    for level in range(len(df.index.levels)):
                        _index = df.index.get_level_values(level)
                        if isinstance(_index[0], bytes):
                            _index = _index.astype('unicode')
                        unicode_indexes.append(_index)

                    df.index = unicode_indexes
        elif type(df.index[0]) == bytes:
            df.index = df.index.astype('unicode')
        if not df.columns.empty:
            if type(df.columns[0]) == bytes:
                df.columns = df.columns.astype('unicode')
        return df

    def serialize(self, item, string_max_len=None, forced_dtype=None):
        return self._to_records(item, string_max_len, forced_dtype)