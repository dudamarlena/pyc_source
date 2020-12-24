# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/snipsskills/utils/cache.py
# Compiled at: 2017-09-29 08:24:39
""" Simple caching. """
import os
from .os_helpers import write_text_file, read_file, create_dir, remove_file
from .. import SNIPS_CACHE_DIR

class Cache:
    STORE_FILE = os.path.join(SNIPS_CACHE_DIR, 'token_store')

    @staticmethod
    def get_login_token():
        return read_file(Cache.STORE_FILE)

    @staticmethod
    def save_login_token(token):
        write_text_file(Cache.STORE_FILE, token)

    @staticmethod
    def clear_login_token():
        remove_file(Cache.STORE_FILE)