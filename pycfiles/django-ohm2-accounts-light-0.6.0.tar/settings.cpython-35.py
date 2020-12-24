# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/entwicklung/ohm2-dev-light/webapp/backend/apps/ohm2_accounts_light/api/v1/settings.py
# Compiled at: 2017-11-08 15:32:15
# Size of source mod 2**32: 409 bytes
from ohm2_accounts_light import settings as ohm2_accounts_light_settings
FACEBOOK_LOGIN = getattr(ohm2_accounts_light_settings, 'FACEBOOK_LOGIN', False)
GOOGLE_PLUS_LOGIN = getattr(ohm2_accounts_light_settings, 'GOOGLE_PLUS_LOGIN', False)
ENABLE_SOCIAL_LOGIN = getattr(ohm2_accounts_light_settings, 'ENABLE_SOCIAL_LOGIN')
INCLUDE_PATCHED_URLS = getattr(ohm2_accounts_light_settings, 'INCLUDE_PATCHED_URLS')