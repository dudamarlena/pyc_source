# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/json.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 1638 bytes
__doc__ = 'PyAMS_utils.json package\n\nA small utility module which provides a default JSON encoder to automatically convert\ndates and datetimes to ISO format\n\n    >>> import json as stock_json\n    >>> from datetime import datetime\n    >>> from pyams_utils import json\n    >>> from pyams_utils.timezone import GMT\n\n    >>> value = datetime.fromtimestamp(1205000000, GMT)\n    >>> stock_json.dumps(value)\n    \'"2008-03-08T18:13:20+00:00"\'\n'
import json
from datetime import date, datetime
__docformat__ = 'restructuredtext'

def default_json_encoder(obj):
    """Default JSON encoding of dates and datetimes"""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    return obj


json._default_encoder = json.JSONEncoder(skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, indent=None, separators=None, default=default_json_encoder)