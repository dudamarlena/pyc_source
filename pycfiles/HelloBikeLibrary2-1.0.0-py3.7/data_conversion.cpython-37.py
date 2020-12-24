# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/HelloBikeLibrary2/data_conversion.py
# Compiled at: 2020-03-13 04:56:30
# Size of source mod 2**32: 1550 bytes
import datetime, json as _json
ISO8601_10_DIGITS = '%Y-%m-%d'
ISO8601_17_DIGITS = '%Y-%m-%dT%H%M%S'
ISO8601_17_DIGITS_V2 = '%Y-%m-%d %H%M%S'
ISO8601_19_DIGITS = '%Y-%m-%dT%H:%M:%S'
ISO8601_19_DIGITS_V2 = '%Y-%m-%d %H:%M:%S'
ISO8601_20_DIGITS = '%Y-%m-%dT%H:%M:%SZ'
ISO8601_20_DIGITS_V2 = '%Y-%m-%d %H:%M:%SZ'
JsonParseError = ValueError
dumps_skipkeys = False
dumps_ensure_ascii = True
dumps_check_circular = True
dumps_allow_nan = True
dumps_cls = None
dumps_indent = None
dumps_separators = None
dumps_encoding = 'utf-8'
dumps_default = None
dumps_sort_keys = False
loads_encoding = None
loads_cls = None
loads_object_hook = None
loads_parse_float = None
loads_parse_int = None
loads_parse_constant = None
loads_object_pairs_hook = None

def soa_loads(data_struct):

    def my_json_obj_hook(data):

        def check_json(input_str):
            try:
                _json.loads(input_str)
                return True
            except:
                return False

        for key, values in data.items():
            if check_json(values):
                data[key] = _json.loads(values)

        return data

    return _json.loads(data_struct, object_hook=my_json_obj_hook)