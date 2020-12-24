# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/util/encoder.py
# Compiled at: 2020-04-15 23:36:42
# Size of source mod 2**32: 498 bytes
import json
from datetime import datetime
from bson import ObjectId

class DTEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return list(obj.timetuple())[0:6]
        return json.JSONEncoder.default(self, obj)


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)