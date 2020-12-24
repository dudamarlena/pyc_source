# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stalk/develop/django_affiliate/django-affiliate/affiliate/app_settings.py
# Compiled at: 2016-05-23 16:26:25
from django.conf import settings
from decimal import Decimal as D
AFFILIATE_MODEL = settings.AFFILIATE_AFFILIATE_MODEL
PARAM_NAME = getattr(settings, 'AFFILIATE_PARAM_NAME', 'aid')
REWARD_AMOUNT = getattr(settings, 'AFFILIATE_REWARD_AMOUNT', D('10.0'))
REWARD_PERCENTAGE = getattr(settings, 'AFFILIATE_REWARD_PERCENTAGE', True)
SAVE_IN_SESSION = getattr(settings, 'AFFILIATE_SAVE_IN_SESSION', True)
SESSION_AGE = getattr(settings, 'AFFILIATE_SESSION_AGE', 432000)
DEFAULT_LINK = getattr(settings, 'AFFILIATE_DEFAULT_LINK', '/')
REMOVE_PARAM_AND_REDIRECT = getattr(settings, 'AFFILIATE_REMOVE_PARAM_AND_REDIRECT', False)
BANNER_FOLDER = getattr(settings, 'AFFILIATE_BANNER_PATH', 'affiliate')
START_AID = getattr(settings, 'AFFILIATE_START_AID', '1000')
DEFAULT_CURRENCY = getattr(settings, 'AFFILIATE_DEFAULT_CURRENCY', 'USD')
MIN_REQUEST_AMOUNT = getattr(settings, 'AFFILIATE_MIN_BALANCE_FOR_REQUEST', D('1.0'))