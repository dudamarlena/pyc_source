# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/databricks/koalas/indexing.py
# Compiled at: 2019-10-15 08:52:53
# Size of source mod 2**32: 28368 bytes
"""
A loc indexer for Koalas DataFrame/Series.
"""
from functools import reduce
import pandas as pd
from pandas.api.types import is_list_like
from pyspark import sql as spark
import pyspark.sql as F
from pyspark.sql.types import BooleanType
from pyspark.sql.utils import AnalysisException
from databricks.koalas.internal import _InternalFrame
from databricks.koalas.exceptions import SparkPandasIndexingError, SparkPandasNotImplementedError
from databricks.koalas.utils import column_index_level

def _make_col(c):
    from databricks.koalas.series import Series
    if isinstance(c, Series):
        return c._scol
    if isinstance(c, str):
        return F.col('`{}`'.format(c))
    raise SparkPandasNotImplementedError(description='Can only convert a string to a column type.')


def _unfold(key, kseries):
    """ Return row selection and column selection pair.

    If kseries parameter is not None, the key should be row selection and the column selection will
    be the kseries parameter.

    >>> s = ks.Series([1, 2, 3], name='a')
    >>> _unfold(slice(1, 2), s)
    (slice(1, 2, None), 0    1
    1    2
    2    3
    Name: a, dtype: int64)

    >>> _unfold((slice(1, 2), slice(None)), None)
    (slice(1, 2, None), slice(None, None, None))

    >>> _unfold((slice(1, 2), s), None)
    (slice(1, 2, None), 0    1
    1    2
    2    3
    Name: a, dtype: int64)

    >>> _unfold((slice(1, 2), 'col'), None)
    (slice(1, 2, None), 'col')
    """
    if kseries is not None:
        if isinstance(key, tuple):
            if len(key) > 1:
                raise SparkPandasIndexingError('Too many indexers')
            key = key[0]
        rows_sel = key
        cols_sel = kseries
    else:
        if isinstance(key, tuple):
            if len(key) != 2:
                raise SparkPandasIndexingError('Only accepts pairs of candidates')
            rows_sel, cols_sel = key
        else:
            rows_sel = key
            cols_sel = None
    return (
     rows_sel, cols_sel)


class AtIndexer(object):
    __doc__ = "\n    Access a single value for a row/column label pair.\n    If the index is not unique, all matching pairs are returned as an array.\n    Similar to ``loc``, in that both provide label-based lookups. Use ``at`` if you only need to\n    get a single value in a DataFrame or Series.\n\n    .. note:: Unlike pandas, Koalas only allows using ``at`` to get values but not to set them.\n\n    .. note:: Warning: If ``row_index`` matches a lot of rows, large amounts of data will be\n        fetched, potentially causing your machine to run out of memory.\n\n    Raises\n    ------\n    KeyError\n        When label does not exist in DataFrame\n\n    Examples\n    --------\n    >>> kdf = ks.DataFrame([[0, 2, 3], [0, 4, 1], [10, 20, 30]],\n    ...                    index=[4, 5, 5], columns=['A', 'B', 'C'])\n    >>> kdf\n        A   B   C\n    4   0   2   3\n    5   0   4   1\n    5  10  20  30\n\n    Get value at specified row/column pair\n\n    >>> kdf.at[4, 'B']\n    2\n\n    Get array if an index occurs multiple times\n\n    >>> kdf.at[5, 'B']\n    array([ 4, 20])\n    "

    def __init__(self, df_or_s):
        from databricks.koalas.frame import DataFrame
        from databricks.koalas.series import Series
        if not isinstance(df_or_s, (DataFrame, Series)):
            raise AssertionError('unexpected argument type: {}'.format(type(df_or_s)))
        elif isinstance(df_or_s, DataFrame):
            self._kdf = df_or_s
            self._ks = None
        else:
            self._kdf = df_or_s._kdf
            self._ks = df_or_s

    def __getitem__(self, key):
        if self._ks is None:
            if isinstance(key, tuple):
                if len(key) != 2:
                    raise TypeError('Use DataFrame.at like .at[row_index, column_name]')
            elif self._ks is not None:
                if not isinstance(key, str):
                    if len(key) != 1:
                        raise TypeError('Use Series.at like .at[row_index]')
            if len(self._kdf._internal.index_columns) != 1:
                raise ValueError("'.at' only supports indices with level 1 right now")
            if self._ks is None:
                if self._kdf._internal.column_index_level > 1:
                    column = dict(zip(self._kdf._internal.column_index, self._kdf._internal.data_columns)).get(key[1], None)
                    if column is None:
                        raise KeyError(key[1])
                else:
                    column = key[1]
            else:
                column = self._ks.name
        elif column is not None and column not in self._kdf._internal.data_columns:
            raise KeyError(column)
        sdf = self._ks._kdf._sdf if self._ks is not None else self._kdf._sdf
        row = key[0] if self._ks is None else key
        pdf = sdf.where(self._kdf._internal.index_scols[0] == row).select(_make_col(column)).toPandas()
        if len(pdf) < 1:
            raise KeyError(row)
        values = pdf.iloc[:, 0].values
        if len(values) == 1:
            return values[0]
        return values


class LocIndexer(object):
    __doc__ = "\n    Access a group of rows and columns by label(s) or a boolean Series.\n\n    ``.loc[]`` is primarily label based, but may also be used with a\n    conditional boolean Series derived from the DataFrame or Series.\n\n    Allowed inputs are:\n\n    - A single label, e.g. ``5`` or ``'a'``, (note that ``5`` is\n      interpreted as a *label* of the index, and **never** as an\n      integer position along the index) for column selection.\n\n    - A list or array of labels, e.g. ``['a', 'b', 'c']``.\n\n    - A slice object with labels, e.g. ``'a':'f'``.\n\n    - A conditional boolean Series derived from the DataFrame or Series\n\n    Not allowed inputs which pandas allows are:\n\n    - A boolean array of the same length as the axis being sliced,\n      e.g. ``[True, False, True]``.\n    - A ``callable`` function with one argument (the calling Series, DataFrame\n      or Panel) and that returns valid output for indexing (one of the above)\n\n    .. note:: MultiIndex is not supported yet.\n\n    .. note:: Note that contrary to usual python slices, **both** the\n        start and the stop are included, and the step of the slice is not allowed.\n        In addition, with a slice, Koalas works as a filter between the range.\n\n    .. note:: With a list or array of labels for row selection,\n        Koalas behaves as a filter without reordering by the labels.\n\n    See Also\n    --------\n    Series.loc : Access group of values using labels.\n\n    Examples\n    --------\n    **Getting values**\n\n    >>> df = ks.DataFrame([[1, 2], [4, 5], [7, 8]],\n    ...                   index=['cobra', 'viper', 'sidewinder'],\n    ...                   columns=['max_speed', 'shield'])\n    >>> df\n                max_speed  shield\n    cobra               1       2\n    viper               4       5\n    sidewinder          7       8\n\n    A single label for row selection is not allowed.\n\n    >>> df.loc['viper']\n    Traceback (most recent call last):\n     ...\n    databricks.koalas.exceptions.SparkPandasNotImplementedError: ...\n\n    List of labels. Note using ``[[]]`` returns a DataFrame.\n    Also note that Koalas behaves just a filter without reordering by the labels.\n\n    >>> df.loc[['viper', 'sidewinder']]\n                max_speed  shield\n    viper               4       5\n    sidewinder          7       8\n\n    >>> df.loc[['sidewinder', 'viper']]\n                max_speed  shield\n    viper               4       5\n    sidewinder          7       8\n\n    Single label for column\n\n    >>> df.loc[['cobra'], 'shield']\n    cobra    2\n    Name: shield, dtype: int64\n\n    List of labels for column. Note using list returns a DataFrame.\n\n    >>> df.loc[['cobra'], ['shield']]\n           shield\n    cobra       2\n\n    Slice with labels for row and single label for column. As mentioned\n    above, note that both the start and stop of the slice are included.\n\n    Also note that the row for 'sidewinder' is included since 'sidewinder'\n    is between 'cobra' and 'viper'.\n\n    >>> df.loc['cobra':'viper', 'max_speed']\n    cobra         1\n    viper         4\n    sidewinder    7\n    Name: max_speed, dtype: int64\n\n    Conditional that returns a boolean Series\n\n    >>> df.loc[df['shield'] > 6]\n                max_speed  shield\n    sidewinder          7       8\n\n    Conditional that returns a boolean Series with column labels specified\n\n    >>> df.loc[df['shield'] > 6, ['max_speed']]\n                max_speed\n    sidewinder          7\n\n    **Setting values**\n\n    Setting value for all items matching the list of labels.\n\n    >>> df.loc[['viper', 'sidewinder'], ['shield']] = 50\n    >>> df\n                max_speed  shield\n    cobra               1       2\n    viper               4      50\n    sidewinder          7      50\n\n    Setting value for an entire row is not allowed\n\n    >>> df.loc['cobra'] = 10\n    Traceback (most recent call last):\n     ...\n    databricks.koalas.exceptions.SparkPandasNotImplementedError: ...\n\n    Set value for an entire column\n\n    >>> df.loc[:, 'max_speed'] = 30\n    >>> df\n                max_speed  shield\n    cobra              30       2\n    viper              30      50\n    sidewinder         30      50\n\n    Set value for an entire list of columns\n\n    >>> df.loc[:, ['max_speed', 'shield']] = 100\n    >>> df\n                max_speed  shield\n    cobra             100     100\n    viper             100     100\n    sidewinder        100     100\n\n    Set value with Series\n\n    >>> df.loc[:, 'shield'] = df['shield'] * 2\n    >>> df\n                max_speed  shield\n    cobra             100     200\n    viper             100     200\n    sidewinder        100     200\n\n    **Getting values on a DataFrame with an index that has integer labels**\n\n    Another example using integers for the index\n\n    >>> df = ks.DataFrame([[1, 2], [4, 5], [7, 8]],\n    ...                   index=[7, 8, 9],\n    ...                   columns=['max_speed', 'shield'])\n    >>> df\n       max_speed  shield\n    7          1       2\n    8          4       5\n    9          7       8\n\n    Slice with integer labels for rows. As mentioned above, note that both\n    the start and stop of the slice are included.\n\n    >>> df.loc[7:9]\n       max_speed  shield\n    7          1       2\n    8          4       5\n    9          7       8\n    "

    def __init__(self, df_or_s):
        from databricks.koalas.frame import DataFrame
        from databricks.koalas.series import Series
        if not isinstance(df_or_s, (DataFrame, Series)):
            raise AssertionError('unexpected argument type: {}'.format(type(df_or_s)))
        elif isinstance(df_or_s, DataFrame):
            self._kdf = df_or_s
            self._ks = None
        else:
            self._kdf = df_or_s._kdf
            self._ks = df_or_s

    def __getitem__(self, key):
        from databricks.koalas.frame import DataFrame
        from databricks.koalas.series import Series

        def raiseNotImplemented(description):
            raise SparkPandasNotImplementedError(description=description,
              pandas_function='.loc[..., ...]',
              spark_target_function='select, where')

        rows_sel, cols_sel = _unfold(key, self._ks)
        sdf = self._kdf._sdf
        if isinstance(rows_sel, Series):
            sdf_for_check_schema = sdf.select(rows_sel._scol)
            assert isinstance(sdf_for_check_schema.schema.fields[0].dataType, BooleanType), (
             str(sdf_for_check_schema), sdf_for_check_schema.schema.fields[0].dataType)
            sdf = sdf.where(rows_sel._scol)
        else:
            if isinstance(rows_sel, slice):
                if not len(self._kdf._internal.index_columns) > 0:
                    raise AssertionError
                elif rows_sel.step is not None:
                    raiseNotImplemented('Cannot use step with Spark.')
                elif rows_sel == slice(None):
                    pass
                elif len(self._kdf._internal.index_columns) == 1:
                    start = rows_sel.start
                    stop = rows_sel.stop
                    index_column = self._kdf.index.to_series()
                    index_data_type = index_column.schema[0].dataType
                    cond = []
                    if start is not None:
                        cond.append(index_column._scol >= F.lit(start).cast(index_data_type))
                    if stop is not None:
                        cond.append(index_column._scol <= F.lit(stop).cast(index_data_type))
                    if len(cond) > 0:
                        sdf = sdf.where(reduce(lambda x, y: x & y, cond))
                else:
                    raiseNotImplemented('Cannot use slice for MultiIndex with Spark.')
            else:
                if isinstance(rows_sel, str):
                    raiseNotImplemented('Cannot use a scalar value for row selection with Spark.')
                else:
                    try:
                        rows_sel = list(rows_sel)
                    except TypeError:
                        raiseNotImplemented('Cannot use a scalar value for row selection with Spark.')

                    if len(rows_sel) == 0:
                        sdf = sdf.where(F.lit(False))
                    else:
                        if len(self._kdf._internal.index_columns) == 1:
                            index_column = self._kdf.index.to_series()
                            index_data_type = index_column.schema[0].dataType
                            if len(rows_sel) == 1:
                                sdf = sdf.where(index_column._scol == F.lit(rows_sel[0]).cast(index_data_type))
                            else:
                                sdf = sdf.where(index_column._scol.isin([F.lit(r).cast(index_data_type) for r in rows_sel]))
                        else:
                            raiseNotImplemented('Cannot select with MultiIndex with Spark.')
        column_index = self._kdf._internal.column_index
        if isinstance(cols_sel, str):
            kdf = DataFrame(self._kdf._internal.copy(sdf=sdf))
            return kdf._get_from_multiindex_column((cols_sel,))
        if isinstance(cols_sel, Series):
            cols_sel = _make_col(cols_sel)
        else:
            if isinstance(cols_sel, slice) and cols_sel != slice(None):
                raise raiseNotImplemented('Can only select columns either by name or reference or all')
            else:
                if isinstance(cols_sel, slice):
                    if cols_sel == slice(None):
                        cols_sel = None
        if cols_sel is None:
            columns = self._kdf._internal.data_scols
        else:
            if isinstance(cols_sel, spark.Column):
                columns = [
                 cols_sel]
                column_index = None
            else:
                if all((isinstance(key, Series) for key in cols_sel)):
                    columns = [_make_col(key) for key in cols_sel]
                    column_index = [key._internal.column_index[0] for key in cols_sel]
                else:
                    if all((isinstance(key, spark.Column) for key in cols_sel)):
                        columns = cols_sel
                        column_index = None
                    else:
                        if any((isinstance(key, str) for key in cols_sel)) and any((isinstance(key, tuple) for key in cols_sel)):
                            raise TypeError('Expected tuple, got str')
                        else:
                            if all((isinstance(key, tuple) for key in cols_sel)):
                                level = self._kdf._internal.column_index_level
                                if any((len(key) != level for key in cols_sel)):
                                    raise ValueError('All the key level should be the same as column index level.')
                                column_to_index = list(zip(self._kdf._internal.data_columns, self._kdf._internal.column_index))
                                columns = []
                                column_index = []
                                for key in cols_sel:
                                    found = False
                                    for column, idx in column_to_index:
                                        if not idx == key:
                                            if idx[0] == key:
                                                pass
                                            columns.append(_make_col(column))
                                            column_index.append(idx)
                                            found = True

                                    if not found:
                                        raise KeyError("['{}'] not in index".format(key))

                            else:
                                try:
                                    sdf = sdf.select(self._kdf._internal.index_scols + columns)
                                    index_columns = self._kdf._internal.index_columns
                                    data_columns = [column for column in sdf.columns if column not in index_columns]
                                    internal = _InternalFrame(sdf=sdf,
                                      data_columns=data_columns,
                                      index_map=(self._kdf._internal.index_map),
                                      column_index=column_index)
                                    kdf = DataFrame(internal)
                                except AnalysisException:
                                    raise KeyError("[{}] don't exist in columns".format([col._jc.toString() for col in columns]))

                            if cols_sel is not None:
                                if isinstance(cols_sel, spark.Column):
                                    from databricks.koalas.series import _col
                                    return _col(kdf)
                            return kdf

    def __setitem__(self, key, value):
        from databricks.koalas.frame import DataFrame
        from databricks.koalas.series import Series, _col
        if not isinstance(key, tuple) or len(key) != 2:
            raise SparkPandasNotImplementedError(description='Only accepts pairs of candidates',
              pandas_function='.loc[..., ...] = ...',
              spark_target_function='withColumn, select')
        rows_sel, cols_sel = key
        if isinstance(rows_sel, slice):
            if rows_sel != slice(None):
                if isinstance(rows_sel, list):
                    if isinstance(cols_sel, str):
                        cols_sel = [
                         cols_sel]
                    kdf = self._kdf.copy()
                    for col_sel in cols_sel:
                        kdf['__indexing_temp_col__'] = value
                        new_col = kdf['__indexing_temp_col__']._scol
                        kdf[col_sel] = Series(kdf[col_sel]._internal.copy(scol=(F.when(kdf._internal.index_scols[0].isin(rows_sel), new_col).otherwise(kdf[col_sel]._scol))),
                          anchor=kdf)
                        kdf = kdf.drop(labels=['__indexing_temp_col__'])

                    self._kdf._internal = kdf._internal.copy()
                else:
                    raise SparkPandasNotImplementedError(description='Can only assign value to the whole dataframe, the row index\n                    has to be `slice(None)` or `:`',
                      pandas_function='.loc[..., ...] = ...',
                      spark_target_function='withColumn, select')
            if not isinstance(cols_sel, (str, list)):
                raise ValueError('only column names or list of column names can be assigned')
            if isinstance(value, DataFrame):
                if len(value.columns) == 1:
                    self._kdf[cols_sel] = _col(value)
            else:
                raise ValueError('Only a dataframe with one column can be assigned')
        else:
            if isinstance(cols_sel, str):
                cols_sel = [
                 cols_sel]
        if not isinstance(rows_sel, list):
            if isinstance(cols_sel, list):
                for col_sel in cols_sel:
                    self._kdf[col_sel] = value


class ILocIndexer(object):
    __doc__ = "\n    Purely integer-location based indexing for selection by position.\n\n    ``.iloc[]`` is primarily integer position based (from ``0`` to\n    ``length-1`` of the axis), but may also be used with a conditional boolean Series.\n\n    Allowed inputs are:\n\n    - An integer for column selection, e.g. ``5``.\n    - A list or array of integers for column selection, e.g. ``[4, 3, 0]``.\n    - A boolean array for column selection.\n    - A slice object with ints for column selection, e.g. ``1:7``.\n    - A slice object with ints without start and step for row selection, e.g. ``:7``.\n    - A conditional boolean Index for row selection.\n\n    Not allowed inputs which pandas allows are:\n\n    - An integer for row selection, e.g. ``5``.\n    - A list or array of integers for row selection, e.g. ``[4, 3, 0]``.\n    - A boolean array for row selection.\n    - A ``callable`` function with one argument (the calling Series, DataFrame\n      or Panel) and that returns valid output for indexing (one of the above).\n      This is useful in method chains, when you don't have a reference to the\n      calling object, but would like to base your selection on some value.\n\n    ``.iloc`` will raise ``IndexError`` if a requested indexer is\n    out-of-bounds, except *slice* indexers which allow out-of-bounds\n    indexing (this conforms with python/numpy *slice* semantics).\n\n    See Also\n    --------\n    DataFrame.loc : Purely label-location based indexer for selection by label.\n    Series.iloc : Purely integer-location based indexing for\n                   selection by position.\n\n    Examples\n    --------\n\n    >>> mydict = [{'a': 1, 'b': 2, 'c': 3, 'd': 4},\n    ...           {'a': 100, 'b': 200, 'c': 300, 'd': 400},\n    ...           {'a': 1000, 'b': 2000, 'c': 3000, 'd': 4000 }]\n    >>> df = ks.DataFrame(mydict, columns=['a', 'b', 'c', 'd'])\n    >>> df\n          a     b     c     d\n    0     1     2     3     4\n    1   100   200   300   400\n    2  1000  2000  3000  4000\n\n    **Indexing just the rows**\n\n    A scalar integer for row selection is not allowed.\n\n    >>> df.iloc[0]\n    Traceback (most recent call last):\n     ...\n    databricks.koalas.exceptions.SparkPandasNotImplementedError: ...\n\n    A list of integers for row selection is not allowed.\n\n    >>> df.iloc[[0]]\n    Traceback (most recent call last):\n     ...\n    databricks.koalas.exceptions.SparkPandasNotImplementedError: ...\n\n    With a `slice` object.\n\n    >>> df.iloc[:3]\n          a     b     c     d\n    0     1     2     3     4\n    1   100   200   300   400\n    2  1000  2000  3000  4000\n\n    Conditional that returns a boolean Series\n\n    >>> df.iloc[df.index % 2 == 0]\n          a     b     c     d\n    0     1     2     3     4\n    2  1000  2000  3000  4000\n\n    **Indexing both axes**\n\n    You can mix the indexer types for the index and columns. Use ``:`` to\n    select the entire axis.\n\n    With scalar integers.\n\n    >>> df.iloc[:1, 1]\n    0    2\n    Name: b, dtype: int64\n\n    With lists of integers.\n\n    >>> df.iloc[:2, [1, 3]]\n         b    d\n    0    2    4\n    1  200  400\n\n    With `slice` objects.\n\n    >>> df.iloc[:2, 0:3]\n         a    b    c\n    0    1    2    3\n    1  100  200  300\n\n    With a boolean array whose length matches the columns.\n\n    >>> df.iloc[:, [True, False, True, False]]\n          a     c\n    0     1     3\n    1   100   300\n    2  1000  3000\n    "

    def __init__(self, df_or_s):
        from databricks.koalas.frame import DataFrame
        from databricks.koalas.series import Series
        if not isinstance(df_or_s, (DataFrame, Series)):
            raise AssertionError('unexpected argument type: {}'.format(type(df_or_s)))
        elif isinstance(df_or_s, DataFrame):
            self._kdf = df_or_s
            self._ks = None
        else:
            self._kdf = df_or_s._kdf
            self._ks = df_or_s

    def __getitem__(self, key):
        from databricks.koalas.frame import DataFrame
        from databricks.koalas.indexes import Index
        from databricks.koalas.series import Series

        def raiseNotImplemented(description):
            raise SparkPandasNotImplementedError(description=description,
              pandas_function='.iloc[..., ...]',
              spark_target_function='select, where')

        rows_sel, cols_sel = _unfold(key, self._ks)
        sdf = self._kdf._sdf
        if isinstance(rows_sel, Index):
            sdf_for_check_schema = sdf.select(rows_sel._scol)
            assert isinstance(sdf_for_check_schema.schema.fields[0].dataType, BooleanType), (
             str(sdf_for_check_schema), sdf_for_check_schema.schema.fields[0].dataType)
            sdf = sdf.where(rows_sel._scol)
        else:
            if isinstance(rows_sel, slice):
                if rows_sel == slice(None):
                    pass
                elif rows_sel.start is not None or rows_sel.step is not None:
                    raiseNotImplemented('Cannot use start or step with Spark.')
                else:
                    if not isinstance(rows_sel.stop, int):
                        raise TypeError('cannot do slice indexing with these indexers [{}] of {}'.format(rows_sel.stop, type(rows_sel.stop)))
                    else:
                        if rows_sel.stop >= 0:
                            sdf = sdf.limit(rows_sel.stop)
                        else:
                            sdf = sdf.limit(sdf.count() + rows_sel.stop)
            else:
                raiseNotImplemented('.iloc requires numeric slice or conditional boolean Index, got {}'.format(rows_sel))
        if isinstance(cols_sel, Series):
            columns = [
             cols_sel._scol]
        else:
            if isinstance(cols_sel, int):
                columns = [
                 self._kdf._internal.data_scols[cols_sel]]
            else:
                if cols_sel is None or cols_sel == slice(None):
                    columns = self._kdf._internal.data_scols
                else:
                    if isinstance(cols_sel, slice):
                        if all((s is None or isinstance(s, int) for s in (cols_sel.start, cols_sel.stop, cols_sel.step))):
                            columns = self._kdf._internal.data_scols[cols_sel]
                        else:
                            not_none = cols_sel.start if cols_sel.start is not None else cols_sel.stop if cols_sel.stop is not None else cols_sel.step
                            raise TypeError('cannot do slice indexing with these indexers {} of {}'.format(not_none, type(not_none)))
                    else:
                        if is_list_like(cols_sel):
                            if all((isinstance(s, int) for s in cols_sel)):
                                columns = [self._kdf._internal.scol_for(col) for col in self._kdf.columns[cols_sel]]
                            else:
                                raise TypeError('cannot perform reduce with flexible type')
                        else:
                            raise ValueError('Location based indexing can only have [integer, integer slice, listlike of integers, boolean array] types, got {}'.format(cols_sel))
        try:
            sdf = sdf.select(self._kdf._internal.index_scols + columns)
            index_columns = self._kdf._internal.index_columns
            data_columns = [column for column in sdf.columns if column not in index_columns]
            internal = _InternalFrame(sdf=sdf,
              data_columns=data_columns,
              index_map=(self._kdf._internal.index_map))
            kdf = DataFrame(internal)
        except AnalysisException:
            raise KeyError("[{}] don't exist in columns".format([col._jc.toString() for col in columns]))

        column_index = self._kdf._internal.column_index
        if cols_sel is not None:
            if isinstance(cols_sel, (Series, int)):
                column_index = None
            else:
                column_index = pd.MultiIndex.from_tuples(self._kdf._internal.column_index)[cols_sel].tolist()
        kdf = DataFrame(kdf._internal.copy(column_index=column_index))
        if cols_sel is not None:
            if isinstance(cols_sel, (Series, int)):
                from databricks.koalas.series import _col
                return _col(kdf)
        return kdf