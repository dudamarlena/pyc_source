# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/parse_str.py
# Compiled at: 2018-01-23 13:51:24
import numpy as np
try:
    from .pkg import chardet
    from .pkg.six import binary_type
except:
    from convert2.pkg import chardet
    from convert2.pkg.six import binary_type

class Anything2Str(object):
    """Parse anything to ``str``

    The logic:

    - bytes: auto detect encoding and then decode
    - other: stringlize it
    """

    def __call__(self, value):
        if value is None:
            return
        else:
            try:
                if np.isnan(value):
                    return
            except:
                pass

            if isinstance(value, binary_type):
                result = chardet.detect(value)
                return value.decode(result['encoding'])
            try:
                return str(value)
            except:
                raise ValueError('%r is not str parsable!' % value)

            return


any2str = Anything2Str()