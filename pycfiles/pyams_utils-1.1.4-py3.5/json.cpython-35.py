# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/json.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 1638 bytes
"""PyAMS_utils.json package

A small utility module which provides a default JSON encoder to automatically convert
dates and datetimes to ISO format

    >>> import json as stock_json
    >>> from datetime import datetime
    >>> from pyams_utils import json
    >>> from pyams_utils.timezone import GMT

    >>> value = datetime.fromtimestamp(1205000000, GMT)
    >>> stock_json.dumps(value)
    '"2008-03-08T18:13:20+00:00"'
"""
import json
from datetime import date, datetime
__docformat__ = 'restructuredtext'

def default_json_encoder(obj):
    """Default JSON encoding of dates and datetimes"""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    return obj


json._default_encoder = json.JSONEncoder(skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, indent=None, separators=None, default=default_json_encoder)