# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/parse_date.py
# Compiled at: 2018-01-23 13:51:09
# Size of source mod 2**32: 1543 bytes
import numpy as np
try:
    from .pkg import rolex
    from .parse_datetime import any2datetime
except:
    from convert2.pkg.rolex import rolex
    from convert2.parse_datetime import any2datetime

class Anything2Date(object):
    __doc__ = "Parse anything to ``datetime.date``.\n\n    The logic:\n\n    - for int, it's the ``datetime.fromordinal(value)``\n    - for float, it's a invalid input\n    - for str, try to parse ``date``\n    - for datetime type, it's the date part\n    - for date type, it's itself\n    "

    def __call__(self, value):
        if value is None:
            return
            try:
                if np.isnan(value):
                    return
            except:
                pass

            try:
                if int(value) == value:
                    try:
                        return rolex.from_ordinal(value)
                    except:
                        raise ValueError('%r is not date parsable!' % value)

            except:
                pass

            if type(value).__name__.startswith('float'):
                raise ValueError('%r is not date parsable!' % value)
            try:
                return any2datetime(value).date()
            except:
                raise ValueError('%r is not date parsable!' % value)


any2date = Anything2Date()