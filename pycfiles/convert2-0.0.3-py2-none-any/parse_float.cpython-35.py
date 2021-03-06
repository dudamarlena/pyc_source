# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = "Parse anything to float\n\n    The logic:\n\n    - for int:\n    - for float:\n    - for str:\n    - for datetime: it's utc timestamp\n    - for date: it's days from ordinary\n    - for timedelta: its total seconds\n    "
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