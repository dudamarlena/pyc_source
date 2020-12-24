# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mongotail/jsondec.py
# Compiled at: 2020-04-09 10:59:11
# Size of source mod 2**32: 3718 bytes
import re, json
from bson import ObjectId, DBRef, regex
try:
    from bson.decimal128 import Decimal128
except ImportError:
    pass

from bson.timestamp import Timestamp
from datetime import datetime
from uuid import UUID
import base64
REGEX_TYPE = type(re.compile(''))

class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return 'ObjectId(%sObjectId)' % str(o)
        else:
            if isinstance(o, UUID):
                return 'UUID(%sUUID)' % str(o)
            if isinstance(o, DBRef):
                return 'DBRef(Field(%sField), ObjectId(%sObjectId)DBRef)' % (o.collection, str(o.id))
            if isinstance(o, datetime):
                try:
                    return 'ISODate(' + o.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'ZISODate)'
                except ValueError:
                    return 'ISODate(' + o.isoformat()[:-3] + 'ZISODate)'

            if isinstance(o, Timestamp):
                return 'Timestamp(%s, %sTimestamp)' % (o.time, o.inc)
            if isinstance(o, (REGEX_TYPE, regex.Regex)):
                return {'$regex': o.pattern}
            if Decimal128 and isinstance(o, Decimal128):
                return 'NumberDecimal(' + str(o) + 'NumberDecimal)'
        if isinstance(o, bytes):
            return 'BinData(0,' + base64.b64encode(o).decode('utf-8') + 'BinData)'
        return json.JSONEncoder.default(self, o)

    def encode(self, o):
        result = super(JSONEncoder, self).encode(o)
        result = result.replace('Field(', '"')
        result = result.replace('Field)', '"')
        result = result.replace('ObjectId(', 'ObjectId("')
        result = result.replace('"ObjectId(', 'ObjectId(')
        result = result.replace('ObjectId)"', '")')
        result = result.replace('ObjectId)', '")')
        result = result.replace('"DBRef(', 'DBRef(')
        result = result.replace('DBRef)"', ')')
        result = result.replace('"ISODate(', 'ISODate("')
        result = result.replace('ISODate)"', '")')
        result = result.replace('"Timestamp(', 'Timestamp(')
        result = result.replace('Timestamp)"', ')')
        result = result.replace('"UUID(', 'UUID("')
        result = result.replace('UUID)"', '")')
        result = result.replace('"NumberDecimal(', 'NumberDecimal("')
        result = result.replace('NumberDecimal)"', '")')
        result = result.replace('"BinData(0,', 'BinData(0,"')
        result = result.replace('BinData)"', '")')
        return result

    def encode_number(self, num):
        """
        For some reason, the profiler store integers as float,
        eg. limit and skip arguments
        """
        if isinstance(num, float):
            if num.is_integer():
                return str(int(num))
        return str(num)