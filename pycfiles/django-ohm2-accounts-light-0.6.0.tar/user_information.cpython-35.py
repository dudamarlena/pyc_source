# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/entwicklung/ohm2-dev-light/webapp/backend/apps/ohm2_accounts_light/pipelines/signup/user_information.py
# Compiled at: 2017-10-03 15:48:00
# Size of source mod 2**32: 522 bytes
from ohm2_handlers_light import utils as h_utils
from ohm2_accounts_light import utils as ohm2_accounts_light_utils

def user_information(request, user, previous_outputs, *args, **kwargs):
    output = {}
    user_information = kwargs.get('ohm2_user_information', {})
    if user_information:
        first_name, last_name = user_information['first_name'], user_information['last_name']
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()
    return (user, output)