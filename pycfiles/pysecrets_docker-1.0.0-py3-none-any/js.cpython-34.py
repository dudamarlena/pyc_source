# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pysecret-project/pysecret/js.py
# Compiled at: 2019-04-10 22:56:44
# Size of source mod 2**32: 994 bytes
import os
from superjson import json
from .helper import HOME
from .singleton import CachedSpam
from .js_helper import create_json_if_not_exists, set_value, get_value, del_key
DEFAULT_JSON_SECRET_FILE = os.path.join(HOME, '.pysecret.json')

class JsonSecret(CachedSpam):
    """JsonSecret"""
    settings_uuid_field = 'secret_file'

    def __real_init__(self, secret_file=DEFAULT_JSON_SECRET_FILE):
        self.secret_file = secret_file
        create_json_if_not_exists(self.secret_file)
        with open(self.secret_file, 'rb') as (f):
            self.data = json.loads(f.read().decode('utf-8'))

    def set(self, json_path, value):
        set_value(self.data, json_path, value)
        json.dump(self.data, self.secret_file, pretty=True, ensure_ascii=False, overwrite=True, verbose=False)

    def get(self, json_path):
        return get_value(self.data, json_path)

    def unset(self, json_path):
        return del_key(self.data, json_path)