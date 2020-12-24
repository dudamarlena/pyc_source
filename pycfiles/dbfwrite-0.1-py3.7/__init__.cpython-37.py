# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dbfwrite\__init__.py
# Compiled at: 2020-01-12 23:25:10
# Size of source mod 2**32: 354 bytes
"""
Created on Thu Jan  9 13:44:33 2020

@author: vane
"""
import struct, datetime, pandas as pd
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_datetime64_dtype
from pandas.api.types import is_bool_dtype
from pandas.api.types import is_float_dtype
from io import BytesIO