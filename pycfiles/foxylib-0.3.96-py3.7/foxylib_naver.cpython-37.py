# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/socialmedia/naver/foxylib_naver.py
# Compiled at: 2020-01-15 23:57:40
# Size of source mod 2**32: 604 bytes
import os
from functools import lru_cache
from foxylib.tools.function.function_tool import FunctionTool

class FoxylibNaver:

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def client_id(cls):
        return os.environ.get('NAVER_APP_ID')

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def secret_id(cls):
        return os.environ.get('NAVER_SECRET_ID')

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def foxytrixy_auth_token(cls):
        return os.environ.get('NAVER_FOXYTRIXY_AUTH_TOKEN')