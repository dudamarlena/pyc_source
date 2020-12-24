# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chunkypandas\core\base.py
# Compiled at: 2019-12-23 19:06:13
# Size of source mod 2**32: 10195 bytes
"""
base.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""
from chunkypandas.utilities import get_named_tempfile
from abc import ABC
import numpy as np, os, pandas as pd
from typelike import ListLike

class ChunkyBase(ABC):
    __doc__ = '\n    Base class for Chunky objects. Not meant to be directly used.\n    '

    def __init__(self, path, ext, chunksize, index_col):
        self.path = path
        self.ext = _get_ext(path, ext)
        self.chunksize = chunksize
        self.index_col = index_col

    def __add__(self, other):
        return self.add(other)

    def __repr__(self):
        return self.to_pandas().__repr__()

    def _get_chunks(self):
        """
        Get chunks by reading file through pandas
        """
        if self.ext == 'csv':
            chunks = pd.read_csv((self.path), chunksize=(self.chunksize), index_col=(self.index_col), header=0)
        else:
            raise AttributeError('cannot read extension {}'.format(self.ext))
        if self.chunksize is not None:
            return chunks
        return [chunks]

    def add(self, other):
        """
        Add to the ChunkySeries

        Currently supported are constant values and other ChunkySeries instances

        Parameters
        ----------
        other : NumberLike or ChunkySeries
            Something to add to this instance of ChunkySeries

        Returns
        -------
        ChunkySeries
            This instance added to *other*
        """
        return self.compute_combine_reduce(compute='add', combine='concat', other=other)

    def compute_combine_reduce(self, compute='skip', combine='skip', reduce='skip', other=None):
        """
        Compute, combine, and reduce chunks

        Pre-defined functions include:
        * **add** : adds two things together
        * **concat** : concatenates LikeLike objects
        * **empty** : returns None for step
        * **skip** : returns input for step
        * **sub** : subtracts first thing by second thing

        Parameters
        ----------
        compute : callable or str
            Function applied to pandas DataFrame or Series chunks, or string used to represent pre-defined functions.
            (Default: 'skip', i.e., no operation is performed on pandas objects).
        combine : callable or str
            Function used to combine chunks, or string used to represent pre-defined functions. (Default: 'skip', i.e.,
            chunks are not combined and the last chunk will be returned).
        reduce : callable or str
            Function used to provide final transformation, or string used to represented pre-defined functions.
            (Default: 'skip', i.e., the result of all the combines is returned).
        other : NumberLike or child of ChunkyBase
            Some compute functions perform mathematical operations involved an `other` thing

        Returns
        -------
        result
        """
        compute = _define_compute_combine_reduce(compute)
        combine = _define_compute_combine_reduce(combine)
        reduce = _define_compute_combine_reduce(reduce)
        chunks = self._get_chunks()
        result = None
        if isinstance(other, ChunkyBase):
            for chunk1, chunk2 in zip(chunks, other._get_chunks()):
                if not np.array_equal(chunk1.index.values, chunk2.index.values):
                    raise AttributeError('indices between chunks should match')
                _result = compute(chunk1, chunk2)
                if result is None:
                    result = _result
                else:
                    result = combine(result, _result)

        else:
            if other is not None:
                for chunk in chunks:
                    _result = compute(chunk, other)
                    if result is None:
                        result = _result
                    else:
                        result = combine(result, _result)

            else:
                for chunk in chunks:
                    _result = compute(chunk)
                    if result is None:
                        result = _result
                    else:
                        result = combine(result, _result)

        return reduce(result)

    def count(self):
        return self.compute_combine_reduce(compute='count', combine='add')

    def head(self, n=10):
        old_chunksize = self.chunksize
        self.chunksize = n
        result = self.compute_combine_reduce()
        self.chunksize = old_chunksize
        return result

    def mean(self):
        """
        Compute mean
        """

        def _compute(chunk):
            return (
             chunk.sum(), chunk.count())

        def _reduce(result):
            return result[0] / result[1]

        return self.compute_combine_reduce(compute=_compute, combine='add', reduce=_reduce)

    def from_pandas(self, pandas_object, chunksize=1000):
        """
        Convert `pandas` to `chunkypandas`

        Parameters
        ----------
        pandas_object : pandas.DataFrame or pandas.Series
            Pandas object to convert
        chunksize : int
            Size of chunks to process for new Chunky object

        Returns
        -------
        ChunkyDataFrame or ChunkySeries
            Pandas object converted to Chunky object
        """
        path = get_named_tempfile()
        pandas_object.to_csv(path, index=True, header=True)
        self.__init__(path, ext='csv', chunksize=chunksize, index_col=0)
        return self

    def to_pandas(self):
        """
        Convert `chunkypandas` to `pandas`

        Returns
        -------
        pandas.DataFrame or pandas.Series
            Pandas DataFrame or Series depending if ChunkyDataFrame or ChunkySeries
        """
        return self.compute_combine_reduce(combine='concat')


def _add(x, y):
    if isinstance(x, (pd.DataFrame, pd.Series)):
        result = x.add(y)
    else:
        if isinstance(x, ListLike) and isinstance(y, ListLike):
            print(x, y)
            assert len(x) == len(y)
            result = []
            for i in range(len(x)):
                result.append(x[i] + y[i])

        else:
            result = x + y
    return result


def _count(x, y=None):
    if isinstance(x, (pd.DataFrame, pd.Series)):
        result = x.count()
    else:
        result = len(x)
    return result


def _get_ext(path, ext):
    if path is not None:
        if ext is None:
            ext = os.path.splitext(path)[1][1:]
    if isinstance(ext, str):
        ext = ext.lower()
    return ext


def _concat(x, y):
    return pd.concat([x, y], ignore_index=True, axis=0)


def _empty(x, y=None):
    pass


def _define_compute_combine_reduce(thing):
    functions = {'add':_add, 
     'concat':_concat, 
     'count':_count, 
     'empty':_empty, 
     'skip':_skip, 
     'sub':_sub}
    if callable(thing):
        result = thing
    else:
        if isinstance(thing, str):
            result = functions[thing]
        else:
            raise AttributeError('unexpected type {}'.format(type(thing)))
    return result


def _skip(x, y=None):
    return x


def _sub(x, y):
    if isinstance(x, (pd.DataFrame, pd.Series)):
        result = x.sub(y)
    else:
        result = x - y
    return result


def _empty_combine(x, y):
    pass


def _empty_reduce(result):
    pass


def _skip_compute(chunk):
    return chunk


def _skip_combine(result, _result):
    return _result


def _skip_reduce(result):
    return result


def _sub(x, y):
    return x - y