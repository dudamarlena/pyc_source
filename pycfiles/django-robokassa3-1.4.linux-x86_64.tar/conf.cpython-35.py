# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mikhail/.virtualenvs/django-robokassa/lib/python3.5/site-packages/robokassa/conf.py
# Compiled at: 2018-04-26 06:41:03
# Size of source mod 2**32: 1202 bytes
from __future__ import unicode_literals
from django.conf import settings
LOGIN = settings.ROBOKASSA_LOGIN
PASSWORD1 = settings.ROBOKASSA_PASSWORD1
PASSWORD2 = getattr(settings, 'ROBOKASSA_PASSWORD2', None)
USE_POST = getattr(settings, 'ROBOKASSA_USE_POST', True)
STRICT_CHECK = getattr(settings, 'ROBOKASSA_STRICT_CHECK', True)
TEST_MODE = getattr(settings, 'ROBOKASSA_TEST_MODE', False)
FORM_TARGET = 'https://merchant.roboxchange.com/Index.aspx'
if TEST_MODE:
    FORM_TARGET = getattr(settings, 'ROBOKASSA_TEST_FORM_TARGET', 'https://auth.robokassa.ru/Merchant/Index.aspx')
EXTRA_PARAMS = sorted(getattr(settings, 'ROBOKASSA_EXTRA_PARAMS', []))