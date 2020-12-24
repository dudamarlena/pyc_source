# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dictionaryutils/json_load.py
# Compiled at: 2020-01-14 18:05:45
# Size of source mod 2**32: 1203 bytes
"""
this module serves as alternative json load that encode unicode to utf-8
from https://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-from-json/19826039
"""
import json

def json_load_byteified(file_handle):
    return _byteify(json.load(file_handle, object_hook=_byteify), ignore_dicts=True)


def json_loads_byteified(json_text):
    return _byteify(json.loads(json_text, object_hook=_byteify), ignore_dicts=True)


def _byteify(data, ignore_dicts=False):
    if isinstance(data, str):
        return data.encode('utf-8')
    else:
        if isinstance(data, list):
            return [_byteify(item, ignore_dicts=True) for item in data]
        if isinstance(data, dict):
            if not ignore_dicts:
                return {_byteify(key, ignore_dicts=True):_byteify(value, ignore_dicts=True) for key, value in data.items()}
        return data