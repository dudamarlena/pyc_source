# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev-light/application/backend/apps/ohm2_accounts_light/pipelines/signup/default.py
# Compiled at: 2017-07-25 18:35:08
# Size of source mod 2**32: 239 bytes
from ohm2_accounts_light import utils as ohm2_accounts_light

def default(request, user, previous_outputs, *args, **kwargs):
    output = {}
    output['authtoken'] = ohm2_accounts_light.get_or_create_authtoken(user)
    return (
     user, output)