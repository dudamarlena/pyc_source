# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/databricks/koalas/indexes.py
# Compiled at: 2019-10-04 00:12:44
# Size of source mod 2**32: 15256 bytes
"""
Wrappers for Indexes to behave similar to pandas Index, MultiIndex.
"""
from functools import partial
from typing import Any, List, Optional, Tuple, Union
import pandas as pd
from pandas.api.types import is_list_like, is_interval_dtype, is_bool_dtype, is_categorical_dtype, is_integer_dtype, is_float_dtype, is_numeric_dtype, is_object_dtype
from pyspark import sql as spark
import pyspark.sql as F
from databricks import koalas as ks
from databricks.koalas.config import get_option
from databricks.koalas.exceptions import PandasNotImplementedError
from databricks.koalas.base import IndexOpsMixin
from databricks.koalas.frame import DataFrame
from databricks.koalas.missing.indexes import _MissingPandasLikeIndex, _MissingPandasLikeMultiIndex
from databricks.koalas.series import Series

class Index(IndexOpsMixin):
    __doc__ = "\n    Koalas Index that corresponds to Pandas Index logically. This might hold Spark Column\n    internally.\n\n    :ivar _kdf: The parent dataframe\n    :type _kdf: DataFrame\n    :ivar _scol: Spark Column instance\n    :type _scol: pyspark.Column\n\n    See Also\n    --------\n    MultiIndex : A multi-level, or hierarchical, Index.\n\n    Examples\n    --------\n    >>> ks.DataFrame({'a': ['a', 'b', 'c']}, index=[1, 2, 3]).index\n    Int64Index([1, 2, 3], dtype='int64')\n\n    >>> ks.DataFrame({'a': [1, 2, 3]}, index=list('abc')).index\n    Index(['a', 'b', 'c'], dtype='object')\n    "

    def __init__(self, kdf: DataFrame, scol: Optional[spark.Column]=None) -> None:
        if scol is None:
            scol = kdf._internal.index_scols[0]
        internal = kdf._internal.copy(scol=scol, data_columns=(kdf._internal.index_columns),
          column_index=(kdf._internal.index_names),
          column_index_names=None)
        IndexOpsMixin.__init__(self, internal, kdf)

    def _with_new_scol(self, scol: spark.Column) -> 'Index':
        """
        Copy Koalas Index with the new Spark Column.

        :param scol: the new Spark Column
        :return: the copied Index
        """
        return Index(self._kdf, scol)

    @property
    def size(self) -> int:
        """
        Return an int representing the number of elements in this object.

        Examples
        --------
        >>> df = ks.DataFrame([(.2, .3), (.0, .6), (.6, .0), (.2, .1)],
        ...                   columns=['dogs', 'cats'],
        ...                   index=list('abcd'))
        >>> df.index.size
        4

        >>> df.set_index('dogs', append=True).index.size
        4
        """
        return len(self._kdf)

    def to_pandas(self) -> pd.Index:
        """
        Return a pandas Index.

        .. note:: This method should only be used if the resulting Pandas object is expected
                  to be small, as all the data is loaded into the driver's memory.

        Examples
        --------
        >>> df = ks.DataFrame([(.2, .3), (.0, .6), (.6, .0), (.2, .1)],
        ...                   columns=['dogs', 'cats'],
        ...                   index=list('abcd'))
        >>> df['dogs'].index.to_pandas()
        Index(['a', 'b', 'c', 'd'], dtype='object')
        """
        sdf = self._kdf._sdf.select(self._scol)
        internal = self._kdf._internal.copy(sdf=sdf,
          index_map=[
         (
          sdf.schema[0].name, self._kdf._internal.index_names[0])],
          data_columns=[],
          column_index=[],
          column_index_names=None)
        return DataFrame(internal)._to_internal_pandas().index

    toPandas = to_pandas

    @property
    def spark_type(self):
        """ Returns the data type as defined by Spark, as a Spark DataType object."""
        return self.to_series().spark_type

    @property
    def name(self) -> Union[(str, Tuple[(str, ...)])]:
        """Return name of the Index."""
        return self.names[0]

    @name.setter
    def name(self, name: Union[(str, Tuple[(str, ...)])]) -> None:
        self.names = [name]

    @property
    def names(self) -> List[Union[(str, Tuple[(str, ...)])]]:
        """Return names of the Index."""
        return [name if (name is None or len(name) > 1) else (name[0]) for name in self._kdf._internal.index_names]

    @names.setter
    def names(self, names: List[Union[(str, Tuple[(str, ...)])]]) -> None:
        if not is_list_like(names):
            raise ValueError('Names must be a list-like')
        internal = self._kdf._internal
        if len(internal.index_map) != len(names):
            raise ValueError('Length of new names must be {}, got {}'.format(len(internal.index_map), len(names)))
        names = [name if isinstance(name, tuple) else (name,) for name in names]
        self._kdf._internal = internal.copy(index_map=(list(zip(internal.index_columns, names))))

    def rename(self, name: Union[(str, Tuple[(str, ...)])], inplace: bool=False):
        """
        Alter Index name.
        Able to set new names without level. Defaults to returning new index.

        Parameters
        ----------
        name : label or list of labels
            Name(s) to set.
        inplace : boolean, default False
            Modifies the object directly, instead of creating a new Index.

        Returns
        -------
        Index
            The same type as the caller or None if inplace is True.

        Examples
        --------
        >>> df = ks.DataFrame({'a': ['A', 'C'], 'b': ['A', 'B']}, columns=['a', 'b'])
        >>> df.index.rename("c")
        Int64Index([0, 1], dtype='int64', name='c')

        >>> df.set_index("a", inplace=True)
        >>> df.index.rename("d")
        Index(['A', 'C'], dtype='object', name='d')

        You can also change the index name in place.

        >>> df.index.rename("e", inplace=True)
        Index(['A', 'C'], dtype='object', name='e')

        >>> df  # doctest: +NORMALIZE_WHITESPACE
           b
        e
        A  A
        C  B
        """
        index_columns = self._kdf._internal.index_columns
        assert len(index_columns) == 1
        if isinstance(name, str):
            name = (
             name,)
        internal = self._kdf._internal.copy(index_map=[(index_columns[0], name)])
        if inplace:
            self._kdf._internal = internal
            return self
        return Index(DataFrame(internal), self._scol)

    def to_series(self, name: Union[(str, Tuple[(str, ...)])]=None) -> Series:
        """
        Create a Series with both index and values equal to the index keys
        useful with map for returning an indexer based on an index.

        Parameters
        ----------
        name : string, optional
            name of resulting Series. If None, defaults to name of original
            index

        Returns
        -------
        Series : dtype will be based on the type of the Index values.

        Examples
        --------
        >>> df = ks.DataFrame([(.2, .3), (.0, .6), (.6, .0), (.2, .1)],
        ...                   columns=['dogs', 'cats'],
        ...                   index=list('abcd'))
        >>> df['dogs'].index.to_series()
        a    a
        b    b
        c    c
        d    d
        Name: 0, dtype: object
        """
        kdf = self._kdf
        scol = self._scol
        if name is not None:
            scol = scol.alias(str(name))
        column_index = [None] if len(kdf._internal.index_map) > 1 else kdf._internal.index_names
        return Series(kdf._internal.copy(scol=scol, column_index=column_index,
          column_index_names=None),
          anchor=kdf)

    def is_boolean(self):
        """
        Return if the current index type is a boolean type.

        Examples
        --------
        >>> ks.DataFrame({'a': [1]}, index=[True]).index.is_boolean()
        True
        """
        return is_bool_dtype(self.dtype)

    def is_categorical(self):
        """
        Return if the current index type is a categorical type.

        Examples
        --------
        >>> ks.DataFrame({'a': [1]}, index=[1]).index.is_categorical()
        False
        """
        return is_categorical_dtype(self.dtype)

    def is_floating(self):
        """
        Return if the current index type is a floating type.

        Examples
        --------
        >>> ks.DataFrame({'a': [1]}, index=[1]).index.is_floating()
        False
        """
        return is_float_dtype(self.dtype)

    def is_integer(self):
        """
        Return if the current index type is a integer type.

        Examples
        --------
        >>> ks.DataFrame({'a': [1]}, index=[1]).index.is_integer()
        True
        """
        return is_integer_dtype(self.dtype)

    def is_interval(self):
        """
        Return if the current index type is an interval type.

        Examples
        --------
        >>> ks.DataFrame({'a': [1]}, index=[1]).index.is_interval()
        False
        """
        return is_interval_dtype(self.dtype)

    def is_numeric(self):
        """
        Return if the current index type is a numeric type.

        Examples
        --------
        >>> ks.DataFrame({'a': [1]}, index=[1]).index.is_numeric()
        True
        """
        return is_numeric_dtype(self.dtype)

    def is_object(self):
        """
        Return if the current index type is a object type.

        Examples
        --------
        >>> ks.DataFrame({'a': [1]}, index=["a"]).index.is_object()
        True
        """
        return is_object_dtype(self.dtype)

    def __getattr__(self, item: str) -> Any:
        if hasattr(_MissingPandasLikeIndex, item):
            property_or_func = getattr(_MissingPandasLikeIndex, item)
            if isinstance(property_or_func, property):
                return property_or_func.fget(self)
            return partial(property_or_func, self)
        raise AttributeError("'Index' object has no attribute '{}'".format(item))

    def __repr__(self):
        max_display_count = get_option('display.max_rows')
        if max_display_count is None:
            return repr(self.to_pandas())
        pindex = self._kdf.head(max_display_count + 1).index._with_new_scol(self._scol).to_pandas()
        pindex_length = len(pindex)
        repr_string = repr(pindex[:max_display_count])
        if pindex_length > max_display_count:
            footer = '\nShowing only the first {}'.format(max_display_count)
            return repr_string + footer
        return repr_string

    def __iter__(self):
        return _MissingPandasLikeIndex.__iter__(self)


class MultiIndex(Index):
    __doc__ = "\n    Koalas MultiIndex that corresponds to Pandas MultiIndex logically. This might hold Spark Column\n    internally.\n\n    :ivar _kdf: The parent dataframe\n    :type _kdf: DataFrame\n    :ivar _scol: Spark Column instance\n    :type _scol: pyspark.Column\n\n    See Also\n    --------\n    Index : A single-level Index.\n\n    Examples\n    --------\n    >>> ks.DataFrame({'a': ['a', 'b', 'c']}, index=[[1, 2, 3], [4, 5, 6]]).index  # doctest: +SKIP\n    MultiIndex([(1, 4),\n                (2, 5),\n                (3, 6)],\n               )\n\n    >>> ks.DataFrame({'a': [1, 2, 3]}, index=[list('abc'), list('def')]).index  # doctest: +SKIP\n    MultiIndex([('a', 'd'),\n                ('b', 'e'),\n                ('c', 'f')],\n               )\n    "

    def __init__(self, kdf: DataFrame):
        assert len(kdf._internal._index_map) > 1
        scol = F.struct(kdf._internal.index_scols)
        data_columns = kdf._sdf.select(scol).columns
        internal = kdf._internal.copy(scol=scol, column_index=[(col, None) for col in data_columns],
          column_index_names=None)
        IndexOpsMixin.__init__(self, internal, kdf)

    def any(self, *args, **kwargs):
        raise TypeError('cannot perform any with this index type: MultiIndex')

    def all(self, *args, **kwargs):
        raise TypeError('cannot perform all with this index type: MultiIndex')

    @property
    def name(self) -> str:
        raise PandasNotImplementedError(class_name='pd.MultiIndex', property_name='name')

    @name.setter
    def name(self, name: str) -> None:
        raise PandasNotImplementedError(class_name='pd.MultiIndex', property_name='name')

    def to_pandas(self) -> pd.MultiIndex:
        """
        Return a pandas MultiIndex.

        .. note:: This method should only be used if the resulting Pandas object is expected
                  to be small, as all the data is loaded into the driver's memory.

        Examples
        --------
        >>> df = ks.DataFrame([(.2, .3), (.0, .6), (.6, .0), (.2, .1)],
        ...                   columns=['dogs', 'cats'],
        ...                   index=[list('abcd'), list('efgh')])
        >>> df['dogs'].index.to_pandas()  # doctest: +SKIP
        MultiIndex([('a', 'e'),
                    ('b', 'f'),
                    ('c', 'g'),
                    ('d', 'h')],
                   )
        """
        return self._kdf[[]]._to_internal_pandas().index

    toPandas = to_pandas

    def __getattr__(self, item: str) -> Any:
        if hasattr(_MissingPandasLikeMultiIndex, item):
            property_or_func = getattr(_MissingPandasLikeMultiIndex, item)
            if isinstance(property_or_func, property):
                return property_or_func.fget(self)
            return partial(property_or_func, self)
        raise AttributeError("'MultiIndex' object has no attribute '{}'".format(item))

    def rename(self, name, inplace=False):
        raise NotImplementedError()

    def __repr__(self):
        max_display_count = get_option('display.max_rows')
        if max_display_count is None:
            return repr(self.to_pandas())
        pindex = self._kdf.head(max_display_count + 1).index.to_pandas()
        pindex_length = len(pindex)
        repr_string = repr(pindex[:max_display_count])
        if pindex_length > max_display_count:
            footer = '\nShowing only the first {}'.format(max_display_count)
            return repr_string + footer
        return repr_string

    def __iter__(self):
        return _MissingPandasLikeMultiIndex.__iter__(self)