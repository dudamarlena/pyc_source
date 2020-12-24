# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/databricks/koalas/selection.py
# Compiled at: 2019-04-23 07:44:26
# Size of source mod 2**32: 8716 bytes
"""
A locator for PandasLikeDataFrame.
"""
from functools import reduce
from pyspark import sql as spark
from pyspark.sql.types import BooleanType
from pyspark.sql.utils import AnalysisException
from databricks.koalas.dask.compatibility import string_types
from databricks.koalas.exceptions import SparkPandasIndexingError, SparkPandasNotImplementedError

def _make_col(c):
    from databricks.koalas.series import Series
    if isinstance(c, Series):
        return c._scol
    if isinstance(c, str):
        from pyspark.sql.functions import col
        return col(c)
    raise SparkPandasNotImplementedError(description='Can only convert a string to a column type.')


def _unfold(key, col):
    """ Return row selection and column selection pair.

    If col parameter is not None, the key should be row selection and the column selection will be
    the col parameter itself. Otherwise check the key contains column selection, and the selection
    is acceptable.
    """
    from databricks.koalas.series import Series
    if col is not None:
        if isinstance(key, tuple):
            if len(key) > 1:
                raise SparkPandasIndexingError('Too many indexers')
            key = key[0]
        rows_sel = key
        cols_sel = col._scol
    else:
        if isinstance(key, tuple):
            if len(key) != 2:
                raise SparkPandasIndexingError('Only accepts pairs of candidates')
            rows_sel, cols_sel = key
            if isinstance(cols_sel, (str, Series)):
                cols_sel = _make_col(cols_sel)
            elif isinstance(cols_sel, slice) and cols_sel != slice(None):
                raise SparkPandasNotImplementedError(description='Can only select columns either by name or reference or all',
                  pandas_function='loc',
                  spark_target_function='select, where, withColumn')
            elif isinstance(cols_sel, slice) and cols_sel == slice(None):
                cols_sel = None
        else:
            rows_sel = key
            cols_sel = None
    return (
     rows_sel, cols_sel)


class SparkDataFrameLocator(object):
    __doc__ = '\n    A locator to slice a group of rows and columns by conditional and label(s).\n\n    Allowed inputs are a slice with all indices or conditional for rows, and string(s) or\n    :class:`Column`(s) for cols.\n    '

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
        from pyspark.sql.functions import lit
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
                if rows_sel.step is not None:
                    raiseNotImplemented('Cannot use step with Spark.')
                elif rows_sel == slice(None):
                    pass
                elif len(self._kdf._index_columns) == 0:
                    raiseNotImplemented('Cannot use slice for Spark if no index provided.')
                else:
                    if len(self._kdf._index_columns) == 1:
                        start = rows_sel.start
                        stop = rows_sel.stop
                        index_column = self._kdf.index
                        index_data_type = index_column.schema[0].dataType
                        cond = []
                        if start is not None:
                            cond.append(index_column._scol >= lit(start).cast(index_data_type))
                        if stop is not None:
                            cond.append(index_column._scol <= lit(stop).cast(index_data_type))
                        if len(cond) > 0:
                            sdf = sdf.where(reduce(lambda x, y: x & y, cond))
                    else:
                        raiseNotImplemented('Cannot use slice for MultiIndex with Spark.')
            else:
                if isinstance(rows_sel, string_types):
                    raiseNotImplemented('Cannot use a scalar value for row selection with Spark.')
                else:
                    try:
                        rows_sel = list(rows_sel)
                    except TypeError:
                        raiseNotImplemented('Cannot use a scalar value for row selection with Spark.')

                    if len(rows_sel) == 0:
                        sdf = sdf.where(lit(False))
                    else:
                        if len(self._kdf._index_columns) == 1:
                            index_column = self._kdf.index
                            index_data_type = index_column.schema[0].dataType
                            if len(rows_sel) == 1:
                                sdf = sdf.where(index_column._scol == lit(rows_sel[0]).cast(index_data_type))
                            else:
                                sdf = sdf.where(index_column._scol.isin([lit(r).cast(index_data_type) for r in rows_sel]))
                        else:
                            raiseNotImplemented('Cannot select with MultiIndex with Spark.')
        if cols_sel is None:
            columns = [_make_col(c) for c in self._kdf._metadata.column_fields]
        else:
            if isinstance(cols_sel, spark.Column):
                columns = [
                 cols_sel]
            else:
                columns = [_make_col(c) for c in cols_sel]
        try:
            kdf = DataFrame(sdf.select(self._kdf._metadata.index_fields + columns))
        except AnalysisException:
            raise KeyError("[{}] don't exist in columns".format([col._jc.toString() for col in columns]))

        kdf._metadata = self._kdf._metadata.copy(column_fields=(kdf._metadata.column_fields[-len(columns):]))
        if cols_sel is not None:
            if isinstance(cols_sel, spark.Column):
                from databricks.koalas.series import _col
                return _col(kdf)
        return kdf

    def __setitem__(self, key, value):
        from databricks.koalas.frame import DataFrame
        from databricks.koalas.series import Series
        if not isinstance(key, tuple) or len(key) != 2:
            raise NotImplementedError('Only accepts pairs of candidates')
        rows_sel, cols_sel = key
        if not isinstance(rows_sel, slice) or rows_sel != slice(None):
            raise SparkPandasNotImplementedError(description='Can only assign value to the whole dataframe, the row index\n                has to be `slice(None)` or `:`',
              pandas_function='.loc[..., ...] = ...',
              spark_target_function='withColumn, select')
        if not isinstance(cols_sel, str):
            raise ValueError('only column names can be assigned')
        elif isinstance(value, Series):
            self._kdf[cols_sel] = value
        else:
            if isinstance(value, DataFrame) and len(value.columns) == 1:
                from pyspark.sql.functions import _spark_col
                self._kdf[cols_sel] = _spark_col(value.columns[0])
            else:
                if isinstance(value, DataFrame) and len(value.columns) != 1:
                    raise ValueError('Only a dataframe with one column can be assigned')
                else:
                    raise ValueError('Only a column or dataframe with single column can be assigned')