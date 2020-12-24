# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/influxable/db/function/aggregations.py
# Compiled at: 2019-09-20 05:34:14
# Size of source mod 2**32: 368 bytes
from . import _generate_function
Count = _generate_function('COUNT')
Distinct = _generate_function('DISTINCT')
Integral = _generate_function('INTEGRAL')
Mean = _generate_function('MEAN')
Median = _generate_function('MEDIAN')
Mode = _generate_function('MODE')
Spread = _generate_function('SPREAD')
StdDev = _generate_function('STDDEV')
Sum = _generate_function('SUM')