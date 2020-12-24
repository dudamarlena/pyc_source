# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """Anything2Datetime"""

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