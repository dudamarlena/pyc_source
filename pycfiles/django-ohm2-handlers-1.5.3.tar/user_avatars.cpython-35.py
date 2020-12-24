# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/accounts/pipelines/user_avatars.py
# Compiled at: 2017-01-24 21:51:29
# Size of source mod 2**32: 365 bytes
from ohm2_handlers.accounts import utils as accounts_utils
import os

def user_avatars(user, request, previous_outputs, *args, **kwargs):
    output = {}
    avatars = accounts_utils.get_or_none_avatars(user=user)
    if avatars is None:
        tmp_sett = {}
        avatars = accounts_utils.create_avatars(user, **tmp_sett)
    output['avatars'] = avatars
    return (
     user, output)