# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/accounts/pipelines/signup/user_keys.py
# Compiled at: 2017-01-24 21:51:09
# Size of source mod 2**32: 313 bytes
from ohm2_handlers.accounts import utils as accounts_utils
import os

def user_keys(user, request, previous_outputs, *args, **kwargs):
    output = {}
    keys = accounts_utils.get_or_none_keys(user=user)
    if keys is None:
        keys = accounts_utils.create_keys(user)
    output['keys'] = keys
    return (
     user, output)