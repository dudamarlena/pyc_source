# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/parse_float.py
# Compiled at: 2018-01-23 13:51:17
# Size of source mod 2**32: 3253 bytes
import numpy as np, pandas as pd
from datetime import datetime, date, timedelta
try:
    from .pkg import chardet
    from .pkg import rolex
    from .pkg.six import string_types, binary_type
    from .util import extract_number_from_string
except:
    from convert2.pkg import chardet
    from convert2.pkg.rolex import rolex
    from convert2.pkg.six import string_types, binary_type
    from convert2.util import extract_number_from_string

class Anything2Float(object):
    """Anything2Float"""
    EXTRACT_NUMBER_FROM_TEXT = True

    def __call__(self, value):
        if value is None:
            return
        try:
            if np.isnan(value):
                return
        except:
            pass

        try:
            return float(value)
        except:
            pass

        if isinstance(value, string_types):
            try:
                return float(value)
            except ValueError:
                pass

            if self.EXTRACT_NUMBER_FROM_TEXT:
                result = extract_number_from_string(value)
                if len(result) == 1:
                    return float(result[0])
                raise ValueError('%r is not float parsable!' % value)
        if isinstance(value, pd.Timestamp):
            try:
                return self((value - pd.Timestamp('1970-01-01 00:00:00Z')).total_seconds())
            except:
                raise ValueError('%r is not float parsable!' % value)

        if isinstance(value, np.datetime64):
            try:
                return self(rolex.to_utctimestamp(value.astype(datetime)))
            except:
                raise ValueError('%r is not float parsable!' % value)

        if isinstance(value, datetime):
            try:
                return self(rolex.to_utctimestamp(value))
            except:
                raise ValueError('%r is not float parsable!' % value)

        if isinstance(value, date):
            try:
                return float(rolex.to_ordinal(value))
            except Exception as e:
                raise ValueError('%r is not float parsable!' % value)

        if isinstance(value, timedelta):
            try:
                return self(value.total_seconds())
            except Exception as e:
                raise ValueError('%r is not float parsable!' % value)

        try:
            return int(value)
        except:
            raise ValueError('%r is not float parsable!' % value)


any2float = Anything2Float()