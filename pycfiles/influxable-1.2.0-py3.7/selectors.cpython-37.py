# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/influxable/db/function/selectors.py
# Compiled at: 2019-09-20 05:34:14
# Size of source mod 2**32: 397 bytes
from . import _generate_function, _generate_function_with_param
Bottom = _generate_function_with_param('BOTTOM')
First = _generate_function('FIRST')
Last = _generate_function('LAST')
Max = _generate_function('MAX')
Min = _generate_function('MIN')
Percentile = _generate_function_with_param('PERCENTILE')
Sample = _generate_function_with_param('SAMPLE')
Top = _generate_function_with_param('TOP')