# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/admin/Desktop/package_env/django_confirm_phone/phonenumber_confirmation/app_settings.py
# Compiled at: 2020-04-03 10:51:02
# Size of source mod 2**32: 201 bytes
from django.conf import settings
UNIQUE_PHONE_NUMBER = getattr(settings, 'UNIQUE_PHONE_NUMBER', True)
PHONE_CONFIRMATION_EXPIRE_MINUTES = getattr(settings, 'PHONE_CONFIRMATION_EXPIRE_MINUTES', 15)