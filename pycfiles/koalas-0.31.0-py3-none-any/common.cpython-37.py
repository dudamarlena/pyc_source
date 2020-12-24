# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/databricks/koalas/missing/common.py
# Compiled at: 2020-02-26 21:14:38
# Size of source mod 2**32: 1887 bytes
memory_usage = lambda f: f('memory_usage',
  reason="Unlike pandas, most DataFrames are not materialized in memory in Spark (and Koalas), and as a result memory_usage() does not do what you intend it to do. Use Spark's web UI to monitor disk and memory usage of your application.")
array = lambda f: f('array',
  reason="If you want to collect your data as an NumPy array, use 'to_numpy()' instead.")
to_pickle = lambda f: f('to_pickle',
  reason='For storage, we encourage you to use Delta or Parquet, instead of Python pickle format.')
to_xarray = lambda f: f('to_xarray',
  reason="If you want to collect your data as an NumPy array, use 'to_numpy()' instead.")
to_list = lambda f: f('to_list',
  reason="If you want to collect your data as an NumPy array, use 'to_numpy()' instead.")
tolist = lambda f: f('tolist',
  reason="If you want to collect your data as an NumPy array, use 'to_numpy()' instead.")
__iter__ = lambda f: f('__iter__',
  reason="If you want to collect your data as an NumPy array, use 'to_numpy()' instead.")
duplicated = lambda f: f('duplicated',
  reason="'duplicated' API returns np.ndarray and the data size is too large.You can just use DataFrame.deduplicated instead")