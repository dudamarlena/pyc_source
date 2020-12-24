# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomislav/dev/seveno_pyutil/build/lib/seveno_pyutil/string_utilities.py
# Compiled at: 2019-03-13 06:22:26
# Size of source mod 2**32: 660 bytes
from datetime import date, datetime
from typing import AnyStr, Iterable, Union
try:
    import simplejson as json
except Exception:
    import json

def is_blank(obj: Union[(AnyStr, Iterable, None)]):
    """
    True if line is empty string, None, string that contains only spaces and
    space like characters, or line is iterable that contains only these kinds
    of strings/objects
    """
    if not obj:
        return True
    else:
        if isinstance(obj, (str, bytes)):
            return not obj.strip()
        retv = False
        try:
            retv = all(is_blank(x) for x in obj)
        except TypeError:
            retv = False

        return retv