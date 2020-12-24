# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/app/tcrudge/utils/json.py
# Compiled at: 2016-12-08 09:48:39
# Size of source mod 2**32: 535 bytes
import datetime, uuid

def json_serial(obj):
    """
    JSON serializer for objects not serializable by default json code.

    :param obj: object to serialize
    :type obj: date, datetime or UUID

    :return: formatted and serialized object
    :rtype: str
    """
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return obj.isoformat()
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError('Type %s not serializable' % type(obj))