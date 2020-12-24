# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_looking_glass/app_settings.py
# Compiled at: 2016-07-18 09:48:34
# Size of source mod 2**32: 768 bytes
"""
Handle app settings in a central place
"""
import datetime
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
MAX_TRANSACTIONS = getattr(settings, 'DHCPKIT_LG_MAX_TRANSACTIONS', 20)
if MAX_TRANSACTIONS:
    if not isinstance(MAX_TRANSACTIONS, int):
        raise ImproperlyConfigured('DHCPKIT_LG_MAX_TRANSACTIONS must be None or an integer')
MAX_TRANSACTION_AGE = getattr(settings, 'DHCPKIT_LG_MAX_TRANSACTION_AGE', datetime.timedelta(days=7))
if MAX_TRANSACTION_AGE:
    if not isinstance(MAX_TRANSACTION_AGE, datetime.timedelta):
        raise ImproperlyConfigured('DHCPKIT_LG_MAX_TRANSACTIONS must be None or a timedelta')