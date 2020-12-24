# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/framework/Json.py
# Compiled at: 2016-12-16 14:55:45
"""Better support to convert our objects to JSON."""
from datetime import datetime
import json

class SkytapJsonEncoder(json.JSONEncoder):
    """Convert a few additional types into JSON."""

    def default(self, o):
        """Convert datetime and our custom objects to JSON.

        Our objects all have a .json() function available to them,
        so we can just try using that if it's available.
        """
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)

        if isinstance(o, datetime):
            return o.isoformat()
        try:
            ret = json.loads(o.json())
        except AttributeError:
            raise
        else:
            return ret

        return json.JSONEncoder.default(self, o)