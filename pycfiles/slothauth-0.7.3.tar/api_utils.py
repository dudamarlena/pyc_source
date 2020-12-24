# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/slothauth/tests/api_utils.py
# Compiled at: 2016-02-01 18:16:07
from .utils import verify_json_object, is_int, is_array, is_float, is_none_or, is_str, is_bool

def is_user_me(obj):
    return verify_json_object(obj, TestDictionaries.user_me)


class TestDictionaries(object):
    user_me = {'id': is_int, 
       'first_name': is_str, 
       'last_name': is_str, 
       'email': is_str, 
       'auth_token': is_str}