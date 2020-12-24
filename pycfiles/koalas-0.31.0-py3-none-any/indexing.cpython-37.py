# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/databricks/koalas/indexing.py
# Compiled at: 2020-04-01 17:55:58
# Size of source mod 2**32: 44638 bytes
"""
A loc indexer for Koalas DataFrame/Series.
"""
from collections import OrderedDict, Iterable
from functools import reduce
from pandas.api.types import is_list_like
from pyspark import sql as spark
import pyspark.sql as F
from pyspark.sql.types import BooleanType, LongType
from pyspark.sql.utils import AnalysisException
import numpy as np
from databricks.koalas.internal import _InternalFrame, NATURAL_ORDER_COLUMN_NAME
from databricks.koalas.exceptions import SparkPandasIndexingError, SparkPandasNotImplementedError
from databricks.koalas.utils import lazy_property, name_like_string, verify_temp_column_name, scol_for

class _IndexerLike(object):

    def __init__(self, kdf_or_kser):
        from databricks.koalas.frame import DataFrame
        from databricks.koalas.series import Series
        assert isinstance(kdf_or_kser, (DataFrame, Series)), 'unexpected argument type: {}'.format(type(kdf_or_kser))
        self._kdf_or_kser = kdf_or_kser

    @property
    def _is_df(self):
        from databricks.koalas.frame import DataFrame
        return isinstance(self._kdf_or_kser, DataFrame)

    @property
    def _is_series(self):
        from databricks.koalas.series import Series
        return isinstance(self._kdf_or_kser, Series)

    @property
    def _internal(self):
        return self._kdf_or_kser._internal


class AtIndexer(_IndexerLike):
    __doc__ = "\n    Access a single value for a row/column label pair.\n    If the index is not unique, all matching pairs are returned as an array.\n    Similar to ``loc``, in that both provide label-based lookups. Use ``at`` if you only need to\n    get a single value in a DataFrame or Series.\n\n    .. note:: Unlike pandas, Koalas only allows using ``at`` to get values but not to set them.\n\n    .. note:: Warning: If ``row_index`` matches a lot of rows, large amounts of data will be\n        fetched, potentially causing your machine to run out of memory.\n\n    Raises\n    ------\n    KeyError\n        When label does not exist in DataFrame\n\n    Examples\n    --------\n    >>> kdf = ks.DataFrame([[0, 2, 3], [0, 4, 1], [10, 20, 30]],\n    ...                    index=[4, 5, 5], columns=['A', 'B', 'C'])\n    >>> kdf\n        A   B   C\n    4   0   2   3\n    5   0   4   1\n    5  10  20  30\n\n    Get value at specified row/column pair\n\n    >>> kdf.at[4, 'B']\n    2\n\n    Get array if an index occurs multiple times\n\n    >>> kdf.at[5, 'B']\n    array([ 4, 20])\n    "

    def __getitem__(self, key):
        if self._is_df:
            if not isinstance(key, tuple) or len(key) != 2:
                raise TypeError('Use DataFrame.at like .at[row_index, column_name]')
            row_sel, col_sel = key
        else:
            assert self._is_series, type(self._kdf_or_kser)
            if isinstance(key, tuple):
                if len(key) != 1:
                    raise TypeError('Use Series.at like .at[row_index]')
            row_sel = key
            col_sel = self._internal.column_labels[0]
        if len(self._internal.index_map) == 1:
            if is_list_like(row_sel):
                raise ValueError('At based indexing on a single index can only have a single value')
            row_sel = (
             row_sel,)
        else:
            if not isinstance(row_sel, tuple):
                raise ValueError('At based indexing on multi-index can only have tuple values')
            elif not isinstance(col_sel, str):
                raise isinstance(col_sel, tuple) and all((isinstance(col, str) for col in col_sel)) or ValueError('At based indexing on multi-index can only have tuple values')
            if isinstance(col_sel, str):
                col_sel = (
                 col_sel,)
            cond = reduce(lambda x, y: x & y, [scol == row for scol, row in zip(self._internal.index_spark_columns, row_sel)])
            pdf = self._internal.spark_frame.drop(NATURAL_ORDER_COLUMN_NAME).filter(cond).select(self._internal.spark_column_for(col_sel)).toPandas()
            if len(pdf) < 1:
                raise KeyError(name_like_string(row_sel))
            values = pdf.iloc[:, 0].values
            if len(row_sel) < len(self._internal.index_map) or len(values) > 1:
                return values
            return values[0]


class iAtIndexer(_IndexerLike):
    __doc__ = "\n    Access a single value for a row/column pair by integer position.\n\n    Similar to ``iloc``, in that both provide integer-based lookups. Use\n    ``iat`` if you only need to get or set a single value in a DataFrame\n    or Series.\n\n    Raises\n    ------\n    KeyError\n        When label does not exist in DataFrame\n\n    Examples\n    --------\n    >>> df = ks.DataFrame([[0, 2, 3], [0, 4, 1], [10, 20, 30]],\n    ...                   columns=['A', 'B', 'C'])\n    >>> df\n        A   B   C\n    0   0   2   3\n    1   0   4   1\n    2  10  20  30\n\n    Get value at specified row/column pair\n\n    >>> df.iat[1, 2]\n    1\n\n    Get value within a series\n\n    >>> kser = ks.Series([1, 2, 3], index=[10, 20, 30])\n    >>> kser\n    10    1\n    20    2\n    30    3\n    Name: 0, dtype: int64\n\n    >>> kser.iat[1]\n    2\n    "

    def __getitem__(self, key):
        if self._is_df:
            if not isinstance(key, tuple) or len(key) != 2:
                raise TypeError('Use DataFrame.iat like .iat[row_integer_position, column_integer_position]')
            row_sel, col_sel = key
            if not (isinstance(row_sel, int) and isinstance(col_sel, int)):
                raise ValueError('iAt based indexing can only have integer indexers')
            return self._kdf_or_kser.iloc[(row_sel, col_sel)]
            if not self._is_series:
                raise AssertionError(type(self._kdf_or_kser))
        else:
            if not isinstance(key, int):
                if len(key) != 1:
                    raise TypeError('Use Series.iat like .iat[row_integer_position]')
            assert isinstance(key, int), 'iAt based indexing can only have integer indexers'
        return self._kdf_or_kser.iloc[key]


class _LocIndexerLike(_IndexerLike):

    def __getitem__(self, key):
        from databricks.koalas.frame import DataFrame
        from databricks.koalas.series import Series
        if self._is_series:
            if isinstance(key, Series):
                if key._kdf is not self._kdf_or_kser._kdf:
                    kdf = self._kdf_or_kser.to_frame()
                    kdf['__temp_col__'] = key
                    return type(self)(kdf[self._kdf_or_kser.name])[kdf['__temp_col__']]
                else:
                    cond, limit, remaining_index = self._select_rows(key)
                    if cond is None and limit is None:
                        return self._kdf_or_kser
                column_labels = self._internal.column_labels
                data_spark_columns = self._internal.data_spark_columns
                returns_series = True
            else:
                pass
        if not self._is_df:
            raise AssertionError
        else:
            if isinstance(key, tuple):
                if len(key) != 2:
                    raise SparkPandasIndexingError('Only accepts pairs of candidates')
                rows_sel, cols_sel = key
            else:
                rows_sel = key
                cols_sel = None
            if isinstance(rows_sel, Series):
                if rows_sel._kdf is not self._kdf_or_kser:
                    kdf = self._kdf_or_kser.copy()
                    kdf['__temp_col__'] = rows_sel
                    return type(self)(kdf)[(kdf['__temp_col__'], cols_sel)][list(self._kdf_or_kser.columns)]
            cond, limit, remaining_index = self._select_rows(rows_sel)
            column_labels, data_spark_columns, returns_series = self._select_cols(cols_sel)
            if cond is None:
                if limit is None:
                    if returns_series:
                        return self._kdf_or_kser._kser_for(column_labels[0])
                    else:
                        if remaining_index is not None:
                            index_scols = self._internal.index_spark_columns[-remaining_index:]
                            index_map = OrderedDict(list(self._internal.index_map.items())[-remaining_index:])
                        else:
                            index_scols = self._internal.index_spark_columns
                            index_map = self._internal.index_map
                        if len(column_labels) > 0:
                            column_labels = column_labels.copy()
                            column_labels_level = max(((len(label) if label is not None else 1) for label in column_labels))
                            none_column = 0
                            for i, label in enumerate(column_labels):
                                if label is None:
                                    label = (
                                     str(none_column),)
                                    none_column += 1
                                if len(label) < column_labels_level:
                                    label = tuple(list(label) + [''] * (column_labels_level - len(label)))
                                column_labels[i] = label

                            if self._internal.column_label_names is None:
                                column_label_names = None
                            else:
                                column_label_names = self._internal.column_label_names[-column_labels_level:]
                        else:
                            column_label_names = None
                        try:
                            sdf = self._internal._sdf
                            if cond is not None:
                                sdf = sdf.drop(NATURAL_ORDER_COLUMN_NAME).filter(cond)
                            if limit is not None:
                                if limit >= 0:
                                    sdf = sdf.limit(limit)
                                else:
                                    sdf = sdf.limit(sdf.count() + limit)
                            data_columns = sdf.select(data_spark_columns).columns
                            sdf = sdf.select(index_scols + data_spark_columns)
                        except AnalysisException:
                            raise KeyError("[{}] don't exist in columns".format([col._jc.toString() for col in data_spark_columns]))

                        internal = _InternalFrame(spark_frame=sdf,
                          index_map=index_map,
                          column_labels=column_labels,
                          data_spark_columns=[scol_for(sdf, col) for col in data_columns],
                          column_label_names=column_label_names)
                        kdf = DataFrame(internal)
                        if returns_series:
                            kdf_or_kser = Series(kdf._internal.copy(spark_column=(kdf._internal.data_spark_columns[0])),
                              anchor=kdf)
                        else:
                            kdf_or_kser = kdf
                    if remaining_index is not None and remaining_index == 0:
                        pdf_or_pser = kdf_or_kser.head(2).to_pandas()
                        length = len(pdf_or_pser)
                        if length == 0:
                            raise KeyError(name_like_string(key))
                else:
                    if length == 1:
                        return pdf_or_pser.iloc[0]
                    return kdf_or_kser
            else:
                return kdf_or_kser

    def __setitem__(self, key, value):
        from databricks.koalas.series import Series
        if self._is_series:
            cond, limit, remaining_index = self._select_rows(key)
            if cond is None:
                cond = F.lit(True)
            else:
                if limit is not None:
                    cond = cond & (self._internal.spark_frame[self._sequence_col] < F.lit(limit))
                if isinstance(value, Series):
                    if remaining_index is not None:
                        if remaining_index == 0:
                            raise ValueError('No axis named {} for object type {}'.format(key, type(value)))
                    value = value._scol
                else:
                    value = F.lit(value)
            scol = F.when(cond, value).otherwise(self._internal.spark_column).alias(name_like_string(self._kdf_or_kser.name or '0'))
            internal = self._internal.copy(spark_column=scol)
            self._kdf_or_kser._internal = internal
        else:
            assert self._is_df
            raise SparkPandasNotImplementedError(description='Assignment to DataFrame with the iloc indexer is not supported yet',
              pandas_function=('.{}[..., ...] = ...'.format(type(self).__name__[:-7].lower())),
              spark_target_function='withColumn, select')


class LocIndexer(_LocIndexerLike):
    __doc__ = "\n    Access a group of rows and columns by label(s) or a boolean Series.\n\n    ``.loc[]`` is primarily label based, but may also be used with a\n    conditional boolean Series derived from the DataFrame or Series.\n\n    Allowed inputs are:\n\n    - A single label, e.g. ``5`` or ``'a'``, (note that ``5`` is\n      interpreted as a *label* of the index, and **never** as an\n      integer position along the index) for column selection.\n\n    - A list or array of labels, e.g. ``['a', 'b', 'c']``.\n\n    - A slice object with labels, e.g. ``'a':'f'``.\n\n    - A conditional boolean Series derived from the DataFrame or Series\n\n    Not allowed inputs which pandas allows are:\n\n    - A boolean array of the same length as the axis being sliced,\n      e.g. ``[True, False, True]``.\n    - A ``callable`` function with one argument (the calling Series, DataFrame\n      or Panel) and that returns valid output for indexing (one of the above)\n\n    .. note:: MultiIndex is not supported yet.\n\n    .. note:: Note that contrary to usual python slices, **both** the\n        start and the stop are included, and the step of the slice is not allowed.\n\n    .. note:: With a list or array of labels for row selection,\n        Koalas behaves as a filter without reordering by the labels.\n\n    See Also\n    --------\n    Series.loc : Access group of values using labels.\n\n    Examples\n    --------\n    **Getting values**\n\n    >>> df = ks.DataFrame([[1, 2], [4, 5], [7, 8]],\n    ...                   index=['cobra', 'viper', 'sidewinder'],\n    ...                   columns=['max_speed', 'shield'])\n    >>> df\n                max_speed  shield\n    cobra               1       2\n    viper               4       5\n    sidewinder          7       8\n\n    Single label. Note this returns the row as a Series.\n\n    >>> df.loc['viper']\n    max_speed    4\n    shield       5\n    Name: viper, dtype: int64\n\n    List of labels. Note using ``[[]]`` returns a DataFrame.\n    Also note that Koalas behaves just a filter without reordering by the labels.\n\n    >>> df.loc[['viper', 'sidewinder']]\n                max_speed  shield\n    viper               4       5\n    sidewinder          7       8\n\n    >>> df.loc[['sidewinder', 'viper']]\n                max_speed  shield\n    viper               4       5\n    sidewinder          7       8\n\n    Single label for column.\n\n    >>> df.loc['cobra', 'shield']\n    2\n\n    List of labels for row.\n\n    >>> df.loc[['cobra'], 'shield']\n    cobra    2\n    Name: shield, dtype: int64\n\n    List of labels for column.\n\n    >>> df.loc['cobra', ['shield']]\n    shield    2\n    Name: cobra, dtype: int64\n\n    List of labels for both row and column.\n\n    >>> df.loc[['cobra'], ['shield']]\n           shield\n    cobra       2\n\n    Slice with labels for row and single label for column. As mentioned\n    above, note that both the start and stop of the slice are included.\n\n    >>> df.loc['cobra':'viper', 'max_speed']\n    cobra    1\n    viper    4\n    Name: max_speed, dtype: int64\n\n    Conditional that returns a boolean Series\n\n    >>> df.loc[df['shield'] > 6]\n                max_speed  shield\n    sidewinder          7       8\n\n    Conditional that returns a boolean Series with column labels specified\n\n    >>> df.loc[df['shield'] > 6, ['max_speed']]\n                max_speed\n    sidewinder          7\n\n    **Setting values**\n\n    Setting value for all items matching the list of labels.\n\n    >>> df.loc[['viper', 'sidewinder'], ['shield']] = 50\n    >>> df\n                max_speed  shield\n    cobra               1       2\n    viper               4      50\n    sidewinder          7      50\n\n    Setting value for an entire row is not allowed\n\n    >>> df.loc['cobra'] = 10\n    Traceback (most recent call last):\n     ...\n    databricks.koalas.exceptions.SparkPandasNotImplementedError: ...\n\n    Set value for an entire column\n\n    >>> df.loc[:, 'max_speed'] = 30\n    >>> df\n                max_speed  shield\n    cobra              30       2\n    viper              30      50\n    sidewinder         30      50\n\n    Set value for an entire list of columns\n\n    >>> df.loc[:, ['max_speed', 'shield']] = 100\n    >>> df\n                max_speed  shield\n    cobra             100     100\n    viper             100     100\n    sidewinder        100     100\n\n    Set value with Series\n\n    >>> df.loc[:, 'shield'] = df['shield'] * 2\n    >>> df\n                max_speed  shield\n    cobra             100     200\n    viper             100     200\n    sidewinder        100     200\n\n    **Getting values on a DataFrame with an index that has integer labels**\n\n    Another example using integers for the index\n\n    >>> df = ks.DataFrame([[1, 2], [4, 5], [7, 8]],\n    ...                   index=[7, 8, 9],\n    ...                   columns=['max_speed', 'shield'])\n    >>> df\n       max_speed  shield\n    7          1       2\n    8          4       5\n    9          7       8\n\n    Slice with integer labels for rows. As mentioned above, note that both\n    the start and stop of the slice are included.\n\n    >>> df.loc[7:9]\n       max_speed  shield\n    7          1       2\n    8          4       5\n    9          7       8\n    "

    @staticmethod
    def _raiseNotImplemented(description):
        raise SparkPandasNotImplementedError(description=description,
          pandas_function='.loc[..., ...]',
          spark_target_function='select, where')

    def _select_rows(self, rows_sel):
        from databricks.koalas.indexes import MultiIndex
        from databricks.koalas.series import Series
        if isinstance(rows_sel, Series):
            assert isinstance(rows_sel.spark_type, BooleanType), rows_sel.spark_type
            return (rows_sel._scol, None, None)
        if isinstance(rows_sel, slice):
            if not len(self._internal.index_spark_column_names) > 0:
                raise AssertionError
            else:
                if rows_sel.step is not None:
                    LocIndexer._raiseNotImplemented('Cannot use step with Spark.')
                else:
                    if rows_sel == slice(None):
                        return (None, None, None)
                        if len(self._internal.index_spark_column_names) == 1:
                            sdf = self._internal.spark_frame
                            index = self._kdf_or_kser.index
                            index_column = index.to_series()
                            index_data_type = index_column.spark_type
                            start = rows_sel.start
                            stop = rows_sel.stop
                            start_and_stop = sdf.select(index_column._scol, NATURAL_ORDER_COLUMN_NAME).where((index_column._scol == F.lit(start).cast(index_data_type)) | (index_column._scol == F.lit(stop).cast(index_data_type))).collect()
                            start = [row[1] for row in start_and_stop if row[0] == start]
                            start = start[0] if len(start) > 0 else None
                            stop = [row[1] for row in start_and_stop if row[0] == stop]
                            stop = stop[(-1)] if len(stop) > 0 else None
                            cond = []
                            if start is not None:
                                cond.append(F.col(NATURAL_ORDER_COLUMN_NAME) >= F.lit(start).cast(LongType()))
                            if stop is not None:
                                cond.append(F.col(NATURAL_ORDER_COLUMN_NAME) <= F.lit(stop).cast(LongType()))
                            if not (start is None and rows_sel.start is not None):
                                if not stop is None or rows_sel.stop is not None:
                                    inc = index_column.is_monotonic_increasing
                                    if inc is False:
                                        dec = index_column.is_monotonic_decreasing
                                    if start is None and rows_sel.start is not None:
                                        start = rows_sel.start
                                        if inc is not False:
                                            cond.append(index_column._scol >= F.lit(start).cast(index_data_type))
                        elif dec is not False:
                            cond.append(index_column._scol <= F.lit(start).cast(index_data_type))
                        else:
                            raise KeyError(rows_sel.start)
                    else:
                        if stop is None:
                            if rows_sel.stop is not None:
                                stop = rows_sel.stop
                                if inc is not False:
                                    cond.append(index_column._scol <= F.lit(stop).cast(index_data_type))
                                else:
                                    if dec is not False:
                                        cond.append(index_column._scol >= F.lit(stop).cast(index_data_type))
                                    else:
                                        raise KeyError(rows_sel.stop)
                        return (
                         reduce(lambda x, y: x & y, cond), None, None)
                    index = self._kdf_or_kser.index
                    index_data_type = [f.dataType for f in index.to_series().spark_type]
                    start = rows_sel.start
                    if start is not None:
                        if not isinstance(start, tuple):
                            start = (
                             start,)
                        if len(start) == 0:
                            start = None
                stop = rows_sel.stop
                if stop is not None:
                    if not isinstance(stop, tuple):
                        stop = (
                         stop,)
                    if len(stop) == 0:
                        stop = None
            depth = max(len(start) if start is not None else 0, len(stop) if stop is not None else 0)
            if depth == 0:
                return (None, None, None)
                if not (depth > len(self._internal.index_map) or index.droplevel(list(range(len(self._internal.index_map))[depth:])).is_monotonic):
                    raise KeyError('Key length ({}) was greater than MultiIndex sort depth'.format(depth))
                conds = []
                if start is not None:
                    cond = F.lit(True)
                    for scol, value, dt in list(zip(self._internal.index_spark_columns, start, index_data_type))[::-1]:
                        compare = MultiIndex._comparator_for_monotonic_increasing(dt)
                        cond = F.when(scol.eqNullSafe(F.lit(value).cast(dt)), cond).otherwise(compare(scol, F.lit(value).cast(dt), spark.Column.__gt__))

                    conds.append(cond)
                if stop is not None:
                    cond = F.lit(True)
                    for scol, value, dt in list(zip(self._internal.index_spark_columns, stop, index_data_type))[::-1]:
                        compare = MultiIndex._comparator_for_monotonic_increasing(dt)
                        cond = F.when(scol.eqNullSafe(F.lit(value).cast(dt)), cond).otherwise(compare(scol, F.lit(value).cast(dt), spark.Column.__lt__))

                    conds.append(cond)
                return (reduce(lambda x, y: x & y, conds), None, None)
            else:
                pass
        if is_list_like(rows_sel) and not isinstance(rows_sel, tuple):
            rows_sel = list(rows_sel)
            if len(rows_sel) == 0:
                return (
                 F.lit(False), None, None)
            if len(self._internal.index_spark_column_names) == 1:
                index_column = self._kdf_or_kser.index.to_series()
                index_data_type = index_column.spark_type
                if len(rows_sel) == 1:
                    return (index_column._scol == F.lit(rows_sel[0]).cast(index_data_type),
                     None,
                     None)
                    return (
                     index_column._scol.isin([F.lit(r).cast(index_data_type) for r in rows_sel]),
                     None,
                     None)
                else:
                    LocIndexer._raiseNotImplemented('Cannot select with MultiIndex with Spark.')
            else:
                if not isinstance(rows_sel, tuple):
                    rows_sel = (
                     rows_sel,)
                if len(rows_sel) > len(self._internal.index_map):
                    raise SparkPandasIndexingError('Too many indexers')
                rows = [scol == value for scol, value in zip(self._internal.index_spark_columns, rows_sel)]
                return (
                 reduce(lambda x, y: x & y, rows),
                 None,
                 len(self._internal.index_map) - len(rows_sel))

    def _get_from_multiindex_column(self, key, labels=None):
        """ Select columns from multi-index columns.

        :param key: the multi-index column keys represented by tuple
        :return: DataFrame or Series
        """
        if not isinstance(key, tuple):
            raise AssertionError
        else:
            if labels is None:
                labels = [(label, label) for label in self._internal.column_labels]
            for k in key:
                labels = [(label, lbl[1:]) for label, lbl in labels if lbl[0] == k]
                if len(labels) == 0:
                    raise KeyError(k)

            if all((len(lbl) > 0 and lbl[0] == '' for _, lbl in labels)):
                labels = [(label, tuple([str(key), *lbl[1:]])) for i, (label, lbl) in enumerate(labels)]
                return self._get_from_multiindex_column((str(key),), labels)
                returns_series = all((len(lbl) == 0 for _, lbl in labels))
                if returns_series:
                    labels = set((label for label, _ in labels))
                    assert len(labels) == 1
                    label = list(labels)[0]
                    column_labels = [label]
                    data_spark_columns = [self._internal.spark_column_for(label)]
            else:
                column_labels = [lbl for _, lbl in labels]
            data_spark_columns = [self._internal.spark_column_for(label) for label, _ in labels]
        return (
         column_labels, data_spark_columns, returns_series)

    def _select_cols(self, cols_sel):
        from databricks.koalas.series import Series
        returns_series = False
        if isinstance(cols_sel, (Series, spark.Column)):
            returns_series = True
            cols_sel = [cols_sel]
        elif cols_sel is None or cols_sel == slice(None):
            column_labels = self._internal.column_labels
            data_spark_columns = self._internal.data_spark_columns
        else:
            if isinstance(cols_sel, slice):
                start, stop = self._kdf_or_kser.columns.slice_locs(start=(cols_sel.start),
                  end=(cols_sel.stop))
                column_labels = self._internal.column_labels[start:stop]
                data_spark_columns = self._internal.data_spark_columns[start:stop]
            else:
                if isinstance(cols_sel, (str, tuple)):
                    if isinstance(cols_sel, str):
                        cols_sel = (
                         cols_sel,)
                    return self._get_from_multiindex_column(cols_sel)
                    if all((isinstance(key, Series) for key in cols_sel)):
                        column_labels = [key._internal.column_labels[0] for key in cols_sel]
                        data_spark_columns = [key._scol for key in cols_sel]
                elif all((isinstance(key, spark.Column) for key in cols_sel)):
                    column_labels = [(self._internal.spark_frame.select(col).columns[0],) for col in cols_sel]
                    data_spark_columns = cols_sel
                else:
                    if any((isinstance(key, str) for key in cols_sel)) and any((isinstance(key, tuple) for key in cols_sel)):
                        raise TypeError('Expected tuple, got str')
                    else:
                        if all((isinstance(key, tuple) for key in cols_sel)):
                            level = self._internal.column_labels_level
                            if any((len(key) != level for key in cols_sel)):
                                raise ValueError('All the key level should be the same as column index level.')
                        column_labels = []
                        data_spark_columns = []
                        for key in cols_sel:
                            found = False
                            for label in self._internal.column_labels:
                                if not label == key:
                                    if label[0] == key:
                                        pass
                                    column_labels.append(label)
                                    data_spark_columns.append(self._internal.spark_column_for(label))
                                    found = True

                            if not found:
                                raise KeyError("['{}'] not in index".format(name_like_string(key)))

        return (
         column_labels, data_spark_columns, returns_series)

    def __setitem__(self, key, value):
        from databricks.koalas.frame import DataFrame
        from databricks.koalas.series import Series, _col
        if self._is_series:
            super(LocIndexer, self).__setitem__(key, value)
            return
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
                    kdf = self._kdf_or_kser.copy()
                    for col_sel in cols_sel:
                        kdf['__indexing_temp_col__'] = value
                        new_col = kdf['__indexing_temp_col__']._scol
                        kdf[col_sel] = Series(kdf[col_sel]._internal.copy(spark_column=(F.when(kdf._internal.index_spark_columns[0].isin(rows_sel), new_col).otherwise(kdf[col_sel]._scol))),
                          anchor=kdf)
                        kdf = kdf.drop(labels=['__indexing_temp_col__'])

                    self._kdf_or_kser._internal = kdf._internal.copy()
                else:
                    raise SparkPandasNotImplementedError(description='Can only assign value to the whole dataframe, the row index\n                    has to be `slice(None)` or `:`',
                      pandas_function='.loc[..., ...] = ...',
                      spark_target_function='withColumn, select')
            if not isinstance(cols_sel, (str, list)):
                raise ValueError('only column names or list of column names can be assigned')
            if isinstance(value, DataFrame):
                if len(value.columns) == 1:
                    self._kdf_or_kser[cols_sel] = _col(value)
            else:
                raise ValueError('Only a dataframe with one column can be assigned')
        else:
            if isinstance(cols_sel, str):
                cols_sel = [
                 cols_sel]
        if not isinstance(rows_sel, list):
            if isinstance(cols_sel, list):
                for col_sel in cols_sel:
                    self._kdf_or_kser[col_sel] = value


class iLocIndexer(_LocIndexerLike):
    __doc__ = "\n    Purely integer-location based indexing for selection by position.\n\n    ``.iloc[]`` is primarily integer position based (from ``0`` to\n    ``length-1`` of the axis), but may also be used with a conditional boolean Series.\n\n    Allowed inputs are:\n\n    - An integer for column selection, e.g. ``5``.\n    - A list or array of integers for row selection with distinct index values,\n      e.g. ``[3, 4, 0]``\n    - A list or array of integers for column selection, e.g. ``[4, 3, 0]``.\n    - A boolean array for column selection.\n    - A slice object with ints for row and column selection, e.g. ``1:7``.\n\n    Not allowed inputs which pandas allows are:\n\n    - A list or array of integers for row selection with duplicated indexes,\n      e.g. ``[4, 4, 0]``.\n    - A boolean array for row selection.\n    - A ``callable`` function with one argument (the calling Series, DataFrame\n      or Panel) and that returns valid output for indexing (one of the above).\n      This is useful in method chains, when you don't have a reference to the\n      calling object, but would like to base your selection on some value.\n\n    ``.iloc`` will raise ``IndexError`` if a requested indexer is\n    out-of-bounds, except *slice* indexers which allow out-of-bounds\n    indexing (this conforms with python/numpy *slice* semantics).\n\n    See Also\n    --------\n    DataFrame.loc : Purely label-location based indexer for selection by label.\n    Series.iloc : Purely integer-location based indexing for\n                   selection by position.\n\n    Examples\n    --------\n\n    >>> mydict = [{'a': 1, 'b': 2, 'c': 3, 'd': 4},\n    ...           {'a': 100, 'b': 200, 'c': 300, 'd': 400},\n    ...           {'a': 1000, 'b': 2000, 'c': 3000, 'd': 4000 }]\n    >>> df = ks.DataFrame(mydict, columns=['a', 'b', 'c', 'd'])\n    >>> df\n          a     b     c     d\n    0     1     2     3     4\n    1   100   200   300   400\n    2  1000  2000  3000  4000\n\n    **Indexing just the rows**\n\n    A scalar integer for row selection.\n\n    >>> df.iloc[0]\n    a    1\n    b    2\n    c    3\n    d    4\n    Name: 0, dtype: int64\n\n    >>> df.iloc[[0]]\n       a  b  c  d\n    0  1  2  3  4\n\n    With a `slice` object.\n\n    >>> df.iloc[:3]\n          a     b     c     d\n    0     1     2     3     4\n    1   100   200   300   400\n    2  1000  2000  3000  4000\n\n    **Indexing both axes**\n\n    You can mix the indexer types for the index and columns. Use ``:`` to\n    select the entire axis.\n\n    With scalar integers.\n\n    >>> df.iloc[:1, 1]\n    0    2\n    Name: b, dtype: int64\n\n    With lists of integers.\n\n    >>> df.iloc[:2, [1, 3]]\n         b    d\n    0    2    4\n    1  200  400\n\n    With `slice` objects.\n\n    >>> df.iloc[:2, 0:3]\n         a    b    c\n    0    1    2    3\n    1  100  200  300\n\n    With a boolean array whose length matches the columns.\n\n    >>> df.iloc[:, [True, False, True, False]]\n          a     c\n    0     1     3\n    1   100   300\n    2  1000  3000\n    "

    @staticmethod
    def _raiseNotImplemented(description):
        raise SparkPandasNotImplementedError(description=description,
          pandas_function='.iloc[..., ...]',
          spark_target_function='select, where')

    @lazy_property
    def _internal(self):
        internal = super(iLocIndexer, self)._internal
        if self._is_series:
            sdf = internal.spark_frame.select(internal.index_spark_columns + [internal.spark_column])
            scol = scol_for(sdf, internal.data_spark_column_names[0])
        else:
            sdf = internal.spark_frame
            scol = None
        sdf = _InternalFrame.attach_distributed_sequence_column(sdf, column_name=(self._sequence_col))
        return internal.copy(spark_frame=(sdf.orderBy(NATURAL_ORDER_COLUMN_NAME)), spark_column=scol)

    @lazy_property
    def _sequence_col(self):
        internal = super(iLocIndexer, self)._internal
        return verify_temp_column_name(internal.spark_frame, '__distributed_sequence_column__')

    def _select_rows(self, rows_sel):
        from databricks.koalas.indexes import Index
        if isinstance(rows_sel, tuple) and len(rows_sel) > 1:
            raise SparkPandasIndexingError('Too many indexers')
        else:
            if isinstance(rows_sel, Index):
                if not isinstance(rows_sel.spark_type, BooleanType):
                    raise AssertionError(rows_sel.spark_type)
                else:
                    return (
                     rows_sel._scol, None, None)
                    if isinstance(rows_sel, slice):

                        def verify_type(i):
                            if not isinstance(i, int):
                                raise TypeError('cannot do slice indexing with these indexers [{}] of {}'.format(i, type(i)))

                        has_negative = False
                        start = rows_sel.start
                        if start is not None:
                            verify_type(start)
                            if start == 0:
                                start = None
                    elif start < 0:
                        has_negative = True
                    stop = rows_sel.stop
                    if stop is not None:
                        verify_type(stop)
                        if stop == 0:
                            stop = None
                        else:
                            if stop < 0:
                                has_negative = True
                    else:
                        step = rows_sel.step
                        if step is not None:
                            verify_type(step)
                            if step == 0:
                                raise ValueError('slice step cannot be zero')
                        else:
                            step = 1
                    if start is None and step == 1:
                        return (
                         None, stop, None)
                sdf = self._internal.spark_frame
                sequence_scol = sdf[self._sequence_col]
                if not has_negative:
                    if step < 0:
                        if start is None:
                            cnt = sdf.count()
            else:
                cond = []
                if start is not None:
                    if start < 0:
                        start = start + cnt
                    elif step >= 0:
                        cond.append(sequence_scol >= F.lit(start).cast(LongType()))
                    else:
                        cond.append(sequence_scol <= F.lit(start).cast(LongType()))
                else:
                    if stop is not None:
                        if stop < 0:
                            stop = stop + cnt
                        elif step >= 0:
                            cond.append(sequence_scol < F.lit(stop).cast(LongType()))
                        else:
                            cond.append(sequence_scol > F.lit(stop).cast(LongType()))
                    if step != 1:
                        if step > 0:
                            start = start or 0
                        else:
                            start = start or cnt - 1
                        cond.append((sequence_scol - start) % F.lit(step).cast(LongType()) == F.lit(0))
                    return (reduce(lambda x, y: x & y, cond), None, None)
                    if isinstance(rows_sel, int):
                        sdf = self._internal.spark_frame
                        return (sdf[self._sequence_col] == rows_sel, None, 0)
                        if isinstance(rows_sel, Iterable):
                            sdf = self._internal.spark_frame
                            if any((isinstance(key, (int, np.int, np.int64, np.int32)) and key < 0 for key in rows_sel)):
                                offset = sdf.count()
                    else:
                        offset = 0
                new_rows_sel = []
                for key in list(rows_sel):
                    if not isinstance(key, (int, np.int, np.int64, np.int32)):
                        raise TypeError('cannot do positional indexing with these indexers [{}] of {}'.format(key, type(key)))
                    if key < 0:
                        key = key + offset
                    new_rows_sel.append(key)

                if len(new_rows_sel) != len(set(new_rows_sel)):
                    raise NotImplementedError('Duplicated row selection is not currently supported; however, normalised index was [%s]' % new_rows_sel)
                sequence_scol = sdf[self._sequence_col]
                cond = []
                for key in new_rows_sel:
                    cond.append(sequence_scol == F.lit(int(key)).cast(LongType()))

                if len(cond) == 0:
                    cond = [
                     F.lit(False)]
                return (
                 reduce(lambda x, y: x | y, cond), None, None)
            iLocIndexer._raiseNotImplemented('.iloc requires numeric slice, conditional boolean Index or a sequence of positions as int, got {}'.format(type(rows_sel)))

    def _select_cols(self, cols_sel):
        from databricks.koalas.series import Series
        returns_series = cols_sel is not None and isinstance(cols_sel, (Series, int))
        if isinstance(cols_sel, Series) and cols_sel._equals(self._kdf_or_kser):
            column_labels = cols_sel._internal.column_labels
            data_spark_columns = cols_sel._internal.data_spark_columns
        else:
            if isinstance(cols_sel, int):
                if cols_sel > len(self._internal.column_labels):
                    raise KeyError(cols_sel)
                column_labels = [
                 self._internal.column_labels[cols_sel]]
                data_spark_columns = [self._internal.data_spark_columns[cols_sel]]
            else:
                if cols_sel is None or cols_sel == slice(None):
                    column_labels = self._internal.column_labels
                    data_spark_columns = self._internal.data_spark_columns
                else:
                    if isinstance(cols_sel, slice):
                        if all((s is None or isinstance(s, int) for s in (cols_sel.start, cols_sel.stop, cols_sel.step))):
                            column_labels = self._internal.column_labels[cols_sel]
                            data_spark_columns = self._internal.data_spark_columns[cols_sel]
                        else:
                            not_none = cols_sel.start if cols_sel.start is not None else cols_sel.stop if cols_sel.stop is not None else cols_sel.step
                            raise TypeError('cannot do slice indexing with these indexers {} of {}'.format(not_none, type(not_none)))
                    else:
                        if is_list_like(cols_sel):
                            if all((isinstance(s, bool) for s in cols_sel)):
                                cols_sel = [i for i, s in enumerate(cols_sel) if s]
                            elif all((isinstance(s, int) for s in cols_sel)):
                                column_labels = [self._internal.column_labels[s] for s in cols_sel]
                                data_spark_columns = [self._internal.data_spark_columns[s] for s in cols_sel]
                            else:
                                raise TypeError('cannot perform reduce with flexible type')
                        else:
                            raise ValueError('Location based indexing can only have [integer, integer slice, listlike of integers, boolean array] types, got {}'.format(cols_sel))
        return (
         column_labels, data_spark_columns, returns_series)

    def __setitem__(self, key, value):
        from databricks.koalas.frame import DataFrame
        from databricks.koalas.series import _col
        super(iLocIndexer, self).__setitem__(key, value)
        if self._is_series:
            internal = self._kdf_or_kser._internal
            sdf = internal.spark_frame.select(internal.index_spark_columns + [internal.spark_column])
            internal = internal.copy(spark_frame=sdf,
              column_labels=[
             internal.column_labels[0] or ('0', )],
              data_spark_columns=[
             scol_for(sdf, internal.data_spark_column_names[0])],
              spark_column=None)
            kser = _col(DataFrame(internal))
            self._kdf_or_kser._internal = kser._internal
            self._kdf_or_kser._kdf = kser._kdf
        else:
            assert self._is_df
        delattr(self, '_lazy__internal')
        delattr(self, '_lazy__sequence_col')