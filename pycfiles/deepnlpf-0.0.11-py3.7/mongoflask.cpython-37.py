# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/mongoflask.py
# Compiled at: 2020-03-16 10:47:21
# Size of source mod 2**32: 616 bytes
from datetime import datetime, date
import isodate as iso
from bson import ObjectId
from flask.json import JSONEncoder
from werkzeug.routing import BaseConverter

class MongoJSONEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, (datetime, date)):
            return iso.datetime_isoformat(o)
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


class ObjectIdConverter(BaseConverter):

    def to_python(self, value):
        return ObjectId(value)

    def to_url(self, value):
        return str(value)