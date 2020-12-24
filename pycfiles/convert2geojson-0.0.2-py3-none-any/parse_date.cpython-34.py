# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """Anything2Date"""

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