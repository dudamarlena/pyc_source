# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/databricks/koalas/window.py
# Compiled at: 2020-03-11 12:47:26
# Size of source mod 2**32: 53875 bytes
from collections import OrderedDict
from functools import partial
from typing import Any
import pandas as pd
from databricks.koalas.internal import SPARK_INDEX_NAME_FORMAT
from databricks.koalas.utils import name_like_string
from pyspark.sql import Window
import pyspark.sql as F
from databricks.koalas.missing.window import _MissingPandasLikeRolling, _MissingPandasLikeRollingGroupby, _MissingPandasLikeExpanding, _MissingPandasLikeExpandingGroupby
from databricks import koalas as ks
from databricks.koalas.internal import NATURAL_ORDER_COLUMN_NAME
from databricks.koalas.utils import scol_for

class _RollingAndExpanding(object):

    def __init__(self, window, min_periods):
        self._window = window
        self._unbounded_window = Window.orderBy(NATURAL_ORDER_COLUMN_NAME).rowsBetween(Window.unboundedPreceding, Window.currentRow)
        self._min_periods = min_periods

    def _apply_as_series_or_frame(self, func):
        """
        Wraps a function that handles Spark column in order
        to support it in both Koalas Series and DataFrame.
        Note that the given `func` name should be same as the API's method name.
        """
        raise NotImplementedError('A class that inherits this class should implement this method to handle the index and columns of output.')

    def count(self):

        def count(scol):
            return F.count(scol).over(self._window)

        return self._apply_as_series_or_frame(count).astype('float64')

    def sum(self):

        def sum(scol):
            return F.when(F.row_number().over(self._unbounded_window) >= self._min_periods, F.sum(scol).over(self._window)).otherwise(F.lit(None))

        return self._apply_as_series_or_frame(sum)

    def min(self):

        def min(scol):
            return F.when(F.row_number().over(self._unbounded_window) >= self._min_periods, F.min(scol).over(self._window)).otherwise(F.lit(None))

        return self._apply_as_series_or_frame(min)

    def max(self):

        def max(scol):
            return F.when(F.row_number().over(self._unbounded_window) >= self._min_periods, F.max(scol).over(self._window)).otherwise(F.lit(None))

        return self._apply_as_series_or_frame(max)

    def mean(self):

        def mean(scol):
            return F.when(F.row_number().over(self._unbounded_window) >= self._min_periods, F.mean(scol).over(self._window)).otherwise(F.lit(None))

        return self._apply_as_series_or_frame(mean)

    def std(self):

        def std(scol):
            return F.when(F.row_number().over(self._unbounded_window) >= self._min_periods, F.stddev(scol).over(self._window)).otherwise(F.lit(None))

        return self._apply_as_series_or_frame(std)

    def var(self):

        def var(scol):
            return F.when(F.row_number().over(self._unbounded_window) >= self._min_periods, F.variance(scol).over(self._window)).otherwise(F.lit(None))

        return self._apply_as_series_or_frame(var)


class Rolling(_RollingAndExpanding):

    def __init__(self, kdf_or_kser, window, min_periods=None):
        from databricks.koalas import DataFrame, Series
        if window < 0:
            raise ValueError('window must be >= 0')
        else:
            if min_periods is not None:
                if min_periods < 0:
                    raise ValueError('min_periods must be >= 0')
            self._window_val = window
            if min_periods is not None:
                min_periods = min_periods
            else:
                min_periods = window
        self.kdf_or_kser = kdf_or_kser
        if not isinstance(kdf_or_kser, (DataFrame, Series)):
            raise TypeError('kdf_or_kser must be a series or dataframe; however, got: %s' % type(kdf_or_kser))
        window = Window.orderBy(NATURAL_ORDER_COLUMN_NAME).rowsBetween(Window.currentRow - (self._window_val - 1), Window.currentRow)
        super(Rolling, self).__init__(window, min_periods)

    def __getattr__(self, item: str) -> Any:
        if hasattr(_MissingPandasLikeRolling, item):
            property_or_func = getattr(_MissingPandasLikeRolling, item)
            if isinstance(property_or_func, property):
                return property_or_func.fget(self)
            return partial(property_or_func, self)
        raise AttributeError(item)

    def _apply_as_series_or_frame(self, func):
        return self.kdf_or_kser._apply_series_op(lambda kser: kser._with_new_scol(func(kser._scol)).rename(kser.name))

    def count(self):
        return super(Rolling, self).count()

    def sum(self):
        return super(Rolling, self).sum()

    def min(self):
        return super(Rolling, self).min()

    def max(self):
        return super(Rolling, self).max()

    def mean(self):
        return super(Rolling, self).mean()

    def std(self):
        return super(Rolling, self).std()

    def var(self):
        return super(Rolling, self).var()


class RollingGroupby(Rolling):

    def __init__(self, groupby, groupkeys, window, min_periods=None):
        from databricks.koalas.groupby import SeriesGroupBy
        from databricks.koalas.groupby import DataFrameGroupBy
        if isinstance(groupby, SeriesGroupBy):
            kdf = groupby._kser.to_frame()
        else:
            if isinstance(groupby, DataFrameGroupBy):
                kdf = groupby._kdf
            else:
                raise TypeError('groupby must be a SeriesGroupBy or DataFrameGroupBy; however, got: %s' % type(groupby))
        super(RollingGroupby, self).__init__(kdf, window, min_periods)
        self._groupby = groupby
        self._window = (self._window.partitionBy)(*[F.col(name_like_string(ser.name)) for ser in groupkeys])
        self._unbounded_window = (self._unbounded_window.partitionBy)(*[F.col(name_like_string(ser.name)) for ser in groupkeys])
        self._groupkeys = groupkeys
        self.kdf = self.kdf_or_kser

    def __getattr__(self, item: str) -> Any:
        if hasattr(_MissingPandasLikeRollingGroupby, item):
            property_or_func = getattr(_MissingPandasLikeRollingGroupby, item)
            if isinstance(property_or_func, property):
                return property_or_func.fget(self)
            return partial(property_or_func, self)
        raise AttributeError(item)

    def _apply_as_series_or_frame(self, func):
        """
        Wraps a function that handles Spark column in order
        to support it in both Koalas Series and DataFrame.
        Note that the given `func` name should be same as the API's method name.
        """
        from databricks.koalas import DataFrame
        from databricks.koalas.series import _col
        from databricks.koalas.groupby import SeriesGroupBy
        kdf = self.kdf
        sdf = self.kdf._sdf
        new_index_scols = []
        new_index_map = OrderedDict()
        for groupkey in self._groupkeys:
            new_index_scols.append(F.col(name_like_string(groupkey.name)).alias(SPARK_INDEX_NAME_FORMAT(len(new_index_scols))))
            new_index_map[SPARK_INDEX_NAME_FORMAT(len(new_index_map))] = groupkey._internal.column_labels[0]

        for new_index_scol, index_name in zip(kdf._internal.index_spark_columns, kdf._internal.index_names):
            new_index_scols.append(new_index_scol.alias(SPARK_INDEX_NAME_FORMAT(len(new_index_scols))))
            new_index_map[SPARK_INDEX_NAME_FORMAT(len(new_index_map))] = index_name

        applied = []
        for column in kdf.columns:
            applied.append(kdf[column]._with_new_scol(func(kdf[column]._scol)).rename(kdf[column].name))

        cond = self._groupkeys[0]._scol.isNotNull()
        for c in self._groupkeys:
            cond = cond | c._scol.isNotNull()

        sdf = sdf.select(new_index_scols + [c._scol for c in applied]).filter(cond)
        internal = kdf._internal.copy(spark_frame=sdf,
          index_map=new_index_map,
          column_labels=[c._internal.column_labels[0] for c in applied],
          data_spark_columns=[scol_for(sdf, c._internal.data_spark_column_names[0]) for c in applied])
        ret = DataFrame(internal)
        if isinstance(self._groupby, SeriesGroupBy):
            return _col(ret)
        return ret

    def count(self):
        return super(RollingGroupby, self).count()

    def sum(self):
        return super(RollingGroupby, self).sum()

    def min(self):
        return super(RollingGroupby, self).min()

    def max(self):
        return super(RollingGroupby, self).max()

    def mean(self):
        return super(RollingGroupby, self).mean()

    def std(self):
        return super(RollingGroupby, self).std()

    def var(self):
        return super(RollingGroupby, self).var()


class Expanding(_RollingAndExpanding):

    def __init__(self, kdf_or_kser, min_periods=1):
        from databricks.koalas import DataFrame, Series
        if min_periods < 0:
            raise ValueError('min_periods must be >= 0')
        self.kdf_or_kser = kdf_or_kser
        if not isinstance(kdf_or_kser, (DataFrame, Series)):
            raise TypeError('kdf_or_kser must be a series or dataframe; however, got: %s' % type(kdf_or_kser))
        window = Window.orderBy(NATURAL_ORDER_COLUMN_NAME).rowsBetween(Window.unboundedPreceding, Window.currentRow)
        super(Expanding, self).__init__(window, min_periods)

    def __getattr__(self, item: str) -> Any:
        if hasattr(_MissingPandasLikeExpanding, item):
            property_or_func = getattr(_MissingPandasLikeExpanding, item)
            if isinstance(property_or_func, property):
                return property_or_func.fget(self)
            return partial(property_or_func, self)
        raise AttributeError(item)

    def __repr__(self):
        return 'Expanding [min_periods={}]'.format(self._min_periods)

    _apply_as_series_or_frame = Rolling._apply_as_series_or_frame

    def count(self):
        """
        The expanding count of any non-NaN observations inside the window.

        .. note:: the current implementation of this API uses Spark's Window without
            specifying partition specification. This leads to move all data into
            single partition in single machine and could cause serious
            performance degradation. Avoid this method against very large dataset.

        Returns
        -------
        Series or DataFrame
            Returned object type is determined by the caller of the expanding
            calculation.

        See Also
        --------
        Series.expanding : Calling object with Series data.
        DataFrame.expanding : Calling object with DataFrames.
        Series.count : Count of the full Series.
        DataFrame.count : Count of the full DataFrame.

        Examples
        --------
        >>> s = ks.Series([2, 3, float("nan"), 10])
        >>> s.expanding().count()
        0    1.0
        1    2.0
        2    2.0
        3    3.0
        Name: 0, dtype: float64

        >>> s.to_frame().expanding().count()
             0
        0  1.0
        1  2.0
        2  2.0
        3  3.0
        """

        def count(scol):
            return F.when(F.row_number().over(self._unbounded_window) >= self._min_periods, F.count(scol).over(self._window)).otherwise(F.lit(None))

        return self._apply_as_series_or_frame(count).astype('float64')

    def sum(self):
        return super(Expanding, self).sum()

    def min(self):
        return super(Expanding, self).min()

    def max(self):
        return super(Expanding, self).max()

    def mean(self):
        return super(Expanding, self).mean()

    def std(self):
        return super(Expanding, self).std()

    def var(self):
        return super(Expanding, self).var()


class ExpandingGroupby(Expanding):

    def __init__(self, groupby, groupkeys, min_periods=1):
        from databricks.koalas.groupby import SeriesGroupBy
        from databricks.koalas.groupby import DataFrameGroupBy
        if isinstance(groupby, SeriesGroupBy):
            kdf = groupby._kser.to_frame()
        else:
            if isinstance(groupby, DataFrameGroupBy):
                kdf = groupby._kdf
            else:
                raise TypeError('groupby must be a SeriesGroupBy or DataFrameGroupBy; however, got: %s' % type(groupby))
        super(ExpandingGroupby, self).__init__(kdf, min_periods)
        self._groupby = groupby
        self._window = (self._window.partitionBy)(*[F.col(name_like_string(ser.name)) for ser in groupkeys])
        self._unbounded_window = (self._window.partitionBy)(*[F.col(name_like_string(ser.name)) for ser in groupkeys])
        self._groupkeys = groupkeys
        self.kdf = self.kdf_or_kser

    def __getattr__(self, item: str) -> Any:
        if hasattr(_MissingPandasLikeExpandingGroupby, item):
            property_or_func = getattr(_MissingPandasLikeExpandingGroupby, item)
            if isinstance(property_or_func, property):
                return property_or_func.fget(self)
            return partial(property_or_func, self)
        raise AttributeError(item)

    _apply_as_series_or_frame = RollingGroupby._apply_as_series_or_frame

    def count(self):
        return super(ExpandingGroupby, self).count()

    def sum(self):
        return super(ExpandingGroupby, self).sum()

    def min(self):
        return super(ExpandingGroupby, self).min()

    def max(self):
        return super(ExpandingGroupby, self).max()

    def mean(self):
        return super(ExpandingGroupby, self).mean()

    def std(self):
        return super(ExpandingGroupby, self).std()

    def var(self):
        return super(ExpandingGroupby, self).var()