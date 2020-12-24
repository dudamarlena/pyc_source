# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\dtypes.py
# Compiled at: 2018-01-16 00:06:36
# Size of source mod 2**32: 331 bytes
from strategycontainer.utils.numpy_utils import bool_dtype, datetime64ns_dtype, float64_dtype, int64_dtype, object_dtype
CLASSIFIER_DTYPES = frozenset({object_dtype, int64_dtype})
FACTOR_DTYPES = frozenset({datetime64ns_dtype, float64_dtype, int64_dtype})
FILTER_DTYPES = frozenset({bool_dtype})