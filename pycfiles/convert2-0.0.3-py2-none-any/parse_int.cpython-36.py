# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/parse_int.py
# Compiled at: 2018-01-23 13:51:20
# Size of source mod 2**32: 3945 bytes
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

class RoundMethod:
    round = 'round'
    floor = 'floor'
    ceiling = 'ceiling'


class Anything2Int(object):
    __doc__ = 'Parse anything to ``int``.\n\n    The logic:\n\n    - for int: force to be generic int type.\n    - for float: round.\n    - for str: extract int from string, for exmplae: "you have 5 dollar" -> 5\n        if there is more than 1 integer, "You got 3, he got 4", raise ValueError\n    - for datetime: it\'s utc timestamp. Ignore milliseconds.\n    - for date: it\'s days from ordinary.\n    - for timedelta: its total seconds, Ignore milliseconds.\n    '
    ROUND_FLOAT_METHOD = RoundMethod.round
    EXTRACT_NUMBER_FROM_TEXT = True

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
                    return int(value)
            except:
                pass

            if type(value).__name__.startswith('float'):
                return int(round(value))
            if isinstance(value, string_types):
                try:
                    return int(value)
                except ValueError:
                    pass

                try:
                    float_ = float(value)
                    return self(float_)
                except ValueError:
                    pass

                if self.EXTRACT_NUMBER_FROM_TEXT:
                    result = extract_number_from_string(value)
                    if len(result) == 1:
                        return self(float(result[0]))
                    raise ValueError('%r is not int parsable!' % value)
            if isinstance(value, pd.Timestamp):
                try:
                    return self((value - pd.Timestamp('1970-01-01 00:00:00Z')).total_seconds())
                except:
                    raise ValueError('%r is not int parsable!' % value)

            if isinstance(value, np.datetime64):
                try:
                    return self(rolex.to_utctimestamp(value.astype(datetime)))
                except:
                    raise ValueError('%r is not int parsable!' % value)

            if isinstance(value, datetime):
                try:
                    return self(rolex.to_utctimestamp(value))
                except:
                    raise ValueError('%r is not int parsable!' % value)

            if isinstance(value, date):
                try:
                    return rolex.to_ordinal(value)
                except Exception as e:
                    raise ValueError('%r is not int parsable!' % value)

            if isinstance(value, timedelta):
                try:
                    return self(value.total_seconds())
                except Exception as e:
                    raise ValueError('%r is not int parsable!' % value)

            try:
                return int(value)
            except:
                raise ValueError('%r is not int parsable!' % value)


any2int = Anything2Int()