# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/basketball_reference_web_scraper/json_encoders.py
# Compiled at: 2020-02-10 09:35:28
# Size of source mod 2**32: 441 bytes
from datetime import datetime, date
from enum import Enum
from json import JSONEncoder

class BasketballReferenceJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)