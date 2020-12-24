# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/json_encoders/SimpleJSONEncoder.py
# Compiled at: 2020-05-11 10:02:35
# Size of source mod 2**32: 565 bytes
import json
from enum import Enum
from .utils import is_elemental, is_collection, is_custom_class

class SimpleJSONEncoder(json.JSONEncoder):
    remove_none_fields = True

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, Enum):
            return obj.value
        if is_custom_class(obj):
            if SimpleJSONEncoder.remove_none_fields:
                return {k:v for k, v in obj.__dict__.items() if v is not None if v is not None}
            return obj.__dict__
        return obj