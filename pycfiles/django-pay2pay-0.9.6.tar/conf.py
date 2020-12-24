# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drmartiner/projects/django-pay2pay/pay2pay/conf.py
# Compiled at: 2013-06-29 08:33:29
from django.conf import settings
PAY2PAY_MERCHANT_ID = getattr(settings, 'PAY2PAY_MERCHANT_ID')
PAY2PAY_HIDE_KEY = getattr(settings, 'PAY2PAY_HIDE_KEY')
PAY2PAY_SECRET_KEY = getattr(settings, 'PAY2PAY_SECRET_KEY')
PAY2PAY_CURRENCY = getattr(settings, 'PAY2PAY_CURRENCY', 'RUB')
PAY2PAY_SUCCESS_URL = getattr(settings, 'PAY2PAY_SUCCESS_URL')
PAY2PAY_FAIL_URL = getattr(settings, 'PAY2PAY_FAIL_URL')
PAY2PAY_RESULT_URL = getattr(settings, 'PAY2PAY_RESULT_URL')
PAY2PAY_TEST_MODE = getattr(settings, 'PAY2PAY_TEST_MODE', False)
PAY2PAY_HIDE_FORM_FIELD = getattr(settings, 'PAY2PAY_HIDE_FORM_FIELD', True)