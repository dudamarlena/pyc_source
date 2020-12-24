# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/serialization/numpy_arrays.py
# Compiled at: 2019-07-09 17:30:49
# Size of source mod 2**32: 7457 bytes
import logging, numpy as np
import numpy.ma as ma
import pandas as pd
from bson import Binary, SON
from .._compression import compress, decompress, compress_array
from ._serializer import Serializer
try:
    from pandas.api.types import infer_dtype
except ImportError:
    from pandas.lib import infer_dtype

try:
    from pandas._libs.writers import max_len_string_array
except ImportError:
    try:
        from pandas._libs.lib import max_len_string_array
    except ImportError:
        from pandas.lib import max_len_string_array

if int(pd.__version__.split('.')[1]) > 22:
    from functools import partial
    pd.concat = partial((pd.concat), sort=False)
DATA = 'd'
MASK = 'm'
TYPE = 't'
DTYPE = 'dt'
COLUMNS = 'c'
INDEX = 'i'
METADATA = 'md'
LENGTHS = 'ln'

class FrameConverter(object):
    __doc__ = "\n    Converts a Pandas Dataframe to and from PyMongo SON representation:\n\n        {\n          METADATA: {\n                      COLUMNS: [col1, col2, ...]             list of str\n                      MASKS: {col1: mask, col2: mask, ...}   dict of str: Binary\n                      INDEX: [idx1, idx2, ...]               list of str\n                      TYPE: 'series' or 'dataframe'\n                      LENGTHS: {col1: len, col2: len, ...}   dict of str: int\n                    }\n          DATA: BINARY(....)      Compressed columns concatenated together\n        }\n    "

    def _convert_types(self, a):
        """
        Converts object arrays of strings to numpy string arrays
        """
        if a.dtype != 'object':
            return (
             a, None)
            if len(a) == 0:
                return (
                 a.astype('U1'), None)
        else:
            mask = pd.isnull(a)
            if mask.sum() > 0:
                a = a.copy()
                np.putmask(a, mask, '')
            else:
                mask = None
            if infer_dtype(a, skipna=False) == 'mixed':
                try:
                    a = np.array([s.encode('ascii') for s in a])
                    a = a.astype('O')
                except:
                    raise ValueError("Column of type 'mixed' cannot be converted to string")

        type_ = infer_dtype(a, skipna=False)
        if type_ in ('unicode', 'string'):
            max_len = max_len_string_array(a)
            return (a.astype('U{:d}'.format(max_len)), mask)
        raise ValueError('Cannot store arrays with {} dtype'.format(type_))

    def docify(self, df):
        """
        Convert a Pandas DataFrame to SON.

        Parameters
        ----------
        df:  DataFrame
            The Pandas DataFrame to encode
        """
        dtypes = {}
        masks = {}
        lengths = {}
        columns = []
        data = Binary(b'')
        start = 0
        arrays = []
        for c in df:
            try:
                columns.append(str(c))
                arr, mask = self._convert_types(df[c].values)
                dtypes[str(c)] = arr.dtype.str
                if mask is not None:
                    masks[str(c)] = Binary(compress(mask.tostring()))
                arrays.append(arr.tostring())
            except Exception as e:
                try:
                    typ = infer_dtype((df[c]), skipna=False)
                    msg = "Column '{}' type is {}".format(str(c), typ)
                    logging.warning(msg)
                    raise e
                finally:
                    e = None
                    del e

        arrays = compress_array(arrays)
        for index, c in enumerate(df):
            d = Binary(arrays[index])
            lengths[str(c)] = (start, start + len(d) - 1)
            start += len(d)
            data += d

        doc = SON({DATA: data, METADATA: {}})
        doc[METADATA] = {COLUMNS: columns, 
         MASK: masks, 
         LENGTHS: lengths, 
         DTYPE: dtypes}
        return doc

    def objify(self, doc, columns=None):
        """
        Decode a Pymongo SON object into an Pandas DataFrame
        """
        cols = columns or doc[METADATA][COLUMNS]
        data = {}
        for col in cols:
            if col not in doc[METADATA][LENGTHS]:
                d = [
                 np.nan]
            else:
                d = decompress(doc[DATA][doc[METADATA][LENGTHS][col][0]:doc[METADATA][LENGTHS][col][1] + 1])
                d = np.frombuffer(d, doc[METADATA][DTYPE][col])
                if MASK in doc[METADATA]:
                    if col in doc[METADATA][MASK]:
                        mask_data = decompress(doc[METADATA][MASK][col])
                        mask = np.frombuffer(mask_data, 'bool')
                        d = ma.masked_array(d, mask)
            data[col] = d

        return pd.DataFrame(data, columns=cols, copy=True)[cols]


class FrametoArraySerializer(Serializer):
    TYPE = 'FrameToArray'

    def __init__(self):
        self.converter = FrameConverter()

    def serialize(self, df):
        if isinstance(df, pd.Series):
            dtype = 'series'
            df = df.to_frame()
        else:
            dtype = 'dataframe'
        if not (len(df.index.names) > 1 and None in df.index.names):
            if None in list(df.columns.values):
                raise Exception('All columns and indexes must be named')
            if df.index.names != [None]:
                index = df.index.names
                df = df.reset_index()
                ret = self.converter.docify(df)
                ret[METADATA][INDEX] = index
                ret[METADATA][TYPE] = dtype
                return ret
        ret = self.converter.docify(df)
        ret[METADATA][TYPE] = dtype
        return ret

    def deserialize(self, data, columns=None):
        """
        Deserializes SON to a DataFrame

        Parameters
        ----------
        data: SON data
        columns: None, or list of strings
            optionally you can deserialize a subset of the data in the SON. Index
            columns are ALWAYS deserialized, and should not be specified

        Returns
        -------
        pandas dataframe or series
        """
        if not data:
            return pd.DataFrame()
        else:
            meta = data[0][METADATA] if isinstance(data, list) else data[METADATA]
            index = INDEX in meta
            if columns:
                if index:
                    columns = columns[:]
                    columns.extend(meta[INDEX])
                if len(columns) > len(set(columns)):
                    raise Exception('Duplicate columns specified, cannot de-serialize')
            if not isinstance(data, list):
                df = self.converter.objify(data, columns)
            else:
                df = pd.concat([self.converter.objify(d, columns) for d in data], ignore_index=(not index))
        if index:
            df = df.set_index(meta[INDEX])
        if meta[TYPE] == 'series':
            return df[df.columns[0]]
        return df

    def combine(self, a, b):
        if a.index.names != [None]:
            return pd.concat([a, b]).sort_index()
        return pd.concat([a, b])