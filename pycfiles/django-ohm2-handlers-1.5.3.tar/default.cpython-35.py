# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/accounts/pipelines/logout/default.py
# Compiled at: 2017-01-24 23:31:06
# Size of source mod 2**32: 197 bytes
from ohm2_handlers.accounts import utils as accounts_utils
import os

def default(request, previous_outputs, *args, **kwargs):
    output = {}
    accounts_utils.user_logout(request)
    return output