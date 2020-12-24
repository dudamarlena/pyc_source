# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/accounts/pipelines/signup/user_crypto.py
# Compiled at: 2017-01-24 21:44:45
# Size of source mod 2**32: 332 bytes
from ohm2_handlers.accounts import utils as accounts_utils
import os

def user_crypto(user, request, previous_outputs, *args, **kwargs):
    output = {}
    crypto = accounts_utils.get_or_none_crypto(user=user)
    if crypto is None:
        crypto = accounts_utils.create_crypto(user)
    output['crypto'] = crypto
    return (
     user, output)