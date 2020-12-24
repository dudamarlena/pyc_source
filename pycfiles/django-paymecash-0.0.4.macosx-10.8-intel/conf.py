# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drmartiner/projects/django-paymecash/paymecash/conf.py
# Compiled at: 2013-09-11 01:20:11
from django.conf import settings
PAYMECASH_WALLET_ID = getattr(settings, 'PAYMECASH_WALLET_ID')
PAYMECASH_DEFAULT_CURRENCY = getattr(settings, 'PAYMECASH_DEFAULT_CURRENCY', 'RUB')
PAYMECASH_SECRET_KEY = getattr(settings, 'PAYMECASH_SECRET_KEY')
PAYMECASH_PAYMENT_URL = getattr(settings, 'PAYMECASH_PAYMENT_URL', 'https://paymecash.me/api/payment')
PAYMECASH_HIDE_FORM = getattr(settings, 'PAYMECASH_HIDE_FORM', True)