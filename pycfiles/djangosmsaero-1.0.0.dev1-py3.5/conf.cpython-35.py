# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/smsaero/conf.py
# Compiled at: 2016-11-05 19:30:08
# Size of source mod 2**32: 242 bytes
from django.conf import settings
SMSAERO_USER = getattr(settings, 'SMSAERO_USER', '')
SMSAERO_PASSWORD = getattr(settings, 'SMSAERO_PASSWORD', '')
SMSAERO_PASSWORD_MD5 = getattr(settings, 'SMSAERO_PASSWORD_MD5', '')