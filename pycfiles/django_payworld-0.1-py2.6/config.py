# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/django_payworld/config.py
# Compiled at: 2012-02-15 01:02:40
from django.conf import settings

def get(key, default):
    return getattr(settings, key, default)


TEST_PAYMENT_URL = get('PAYWORLD_TEST_PAYMENT_URL', 'https://pay-world.ru/paymentsystem/enter-test/')
REAL_PAYMENT_URL = get('PAYWORLD_REAL_PAYMENT_URL', 'https://pay-world.ru/paymentsystem/enter/')
TEST_MODE = get('PAYWORLD_TEST_MODE', True)
if TEST_MODE:
    PAYMENT_URL = REAL_PAYMENT_URL
else:
    PAYMENT_URL = TEST_PAYMENT_URL