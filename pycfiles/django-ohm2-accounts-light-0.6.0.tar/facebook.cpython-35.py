# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/ohm2-dev-light/backend/webapp/backend/apps/ohm2_accounts_light/pipelines/social/facebook.py
# Compiled at: 2018-08-20 19:55:37
# Size of source mod 2**32: 371 bytes
from ohm2_accounts_light import utils as ohm2_accounts_light_utils

def login(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        pipeline_options = {'facebook': {'response': response, 
                      'kwargs': kwargs}}
        ohm2_accounts_light_utils.run_signup_pipeline(backend.strategy.request, user, **pipeline_options)
    return {}