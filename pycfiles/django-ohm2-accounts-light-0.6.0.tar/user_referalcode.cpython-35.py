# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/accounts/pipelines/signup/user_referalcode.py
# Compiled at: 2017-01-24 21:50:30
# Size of source mod 2**32: 450 bytes
from ohm2_handlers.accounts import utils as accounts_utils
import os

def user_referalcode(user, request, previous_outputs, *args, **kwargs):
    output = {}
    referalcodes = accounts_utils.get_referalcodes(user=user)
    if len(referalcodes) == 0:
        referalcode = accounts_utils.create_referalcode(user)
        output['referalcodes'] = accounts_utils.get_referalcodes(user=user)
    else:
        output['referalcodes'] = referalcodes
    return (user, output)