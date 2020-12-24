# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_local_search/lib/utils.py
# Compiled at: 2019-05-24 16:38:48
# Size of source mod 2**32: 878 bytes
from uuid import UUID
import string

def is_uuid(uuid_string, version=None):
    try:
        if version is None:
            for i in range(1, 6):
                if is_uuid(uuid_string, i):
                    return True

        else:
            uid = UUID(uuid_string, version=version)
            return uid.hex == uuid_string.replace('-', '')
    except ValueError:
        return False


class SimpleFormatter(string.Formatter):
    output_encoding = None
    output_encoding: str

    def __init__(self, output_encoding=None):
        super().__init__()
        self.output_encoding = output_encoding

    def get_value(self, key, args, kwargs):
        item = args[0]
        result = item.get(key, strict=False)
        if result is not None:
            if self.output_encoding == 'json':
                import json
                return json.dumps(result)[1:-1]
        return result