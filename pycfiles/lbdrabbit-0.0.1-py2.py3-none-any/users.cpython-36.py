# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/lbdrabbit-project/lbdrabbit/tests/handlers/rest/users.py
# Compiled at: 2019-09-30 22:00:37
# Size of source mod 2**32: 421 bytes
from lbdrabbit.tests.auto_inherit_config import LbdFuncConfig
__lbd_func_config__ = LbdFuncConfig(timeout=30,
  alias='users')

def get(event, context):
    pass


get.__lbd_func_config__ = LbdFuncConfig(alias='rest.users.get')

def post(event, context):
    pass


post.__lbd_func_config__ = LbdFuncConfig(timeout=60,
  alias='rest.users.post')

def any_(event, context):
    pass