# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/parse_datetime.py
# Compiled at: 2018-01-23 13:53:55
# Size of source mod 2**32: 2076 bytes
from datetime import datetime
import numpy as np, pandas as pd
try:
    from .pkg import rolex
except:
    from convert2.pkg import rolex

class Anything2Datetime(object):
    __doc__ = "Parse anything to ``datetime.datetime``.\n\n    The logic:\n\n    - for int, it's the ``datetime.from_utctimestamp(value)``\n    - for float, it's the ``datetime.from_utctimestamp(value)``\n    - for str, try to parse ``datetime``\n    - for datetime type, it's itself\n    - for date type, it's the time at 00:00:00\n    "

    def __call__(self, value):
        if value is None:
            return
        else:
            try:
                if np.isnan(value):
                    return
            except:
                pass

            try:
                if int(value) == value:
                    try:
                        return rolex.from_utctimestamp(int(value))
                    except:
                        raise ValueError('%r is not datetime parsable!' % value)

            except:
                pass

            if type(value).__name__.startswith('float'):
                try:
                    return rolex.from_utctimestamp(float(value))
                except:
                    raise ValueError('%r is not datetime parsable!' % value)

            if isinstance(value, pd.Timestamp):
                try:
                    return value.to_pydatetime()
                except:
                    raise ValueError('%r is not datetime parsable!' % value)

            if isinstance(value, np.datetime64):
                try:
                    return value.astype(datetime)
                except:
                    raise ValueError('%r is not datetime parsable!' % value)

            try:
                return rolex.parse_datetime(value)
            except:
                raise ValueError('%r is not datetime parsable!' % value)


any2datetime = Anything2Datetime()