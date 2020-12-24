# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/json.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 2170 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from datetime import datetime, date
import json, numpy as np

def json_ser(obj):
    """json serializer that deals with dates.

    usage: json.dumps(object, default=utils.json.json_ser)
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()


class AirflowJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            if isinstance(obj, date):
                return obj.strftime('%Y-%m-%d')
            else:
                if type(obj) in (np.int_, np.intc, np.intp, np.int8, np.int16,
                 np.int32, np.int64, np.uint8, np.uint16,
                 np.uint32, np.uint64):
                    return int(obj)
                if type(obj) in (np.bool_,):
                    return bool(obj)
                if type(obj) in (np.float_, np.float16, np.float32, np.float64,
                 np.complex_, np.complex64, np.complex128):
                    return float(obj)
            return json.JSONEncoder.default(self, obj)