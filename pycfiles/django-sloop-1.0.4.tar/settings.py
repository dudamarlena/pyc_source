# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/django_sloop/settings.py
# Compiled at: 2019-07-23 06:29:41
from django.conf import settings
DJANGO_SLOOP_SETTINGS = getattr(settings, 'DJANGO_SLOOP_SETTINGS', {})
DJANGO_SLOOP_SETTINGS.setdefault('AWS_REGION_NAME', None)
DJANGO_SLOOP_SETTINGS.setdefault('AWS_ACCESS_KEY_ID', None)
DJANGO_SLOOP_SETTINGS.setdefault('AWS_SECRET_ACCESS_KEY', None)
DJANGO_SLOOP_SETTINGS.setdefault('SNS_IOS_APPLICATION_ARN', None)
DJANGO_SLOOP_SETTINGS.setdefault('SNS_IOS_SANDBOX_ENABLED', False)
DJANGO_SLOOP_SETTINGS.setdefault('SNS_ANDROID_APPLICATION_ARN', None)
DJANGO_SLOOP_SETTINGS.setdefault('LOG_SENT_MESSAGES', False)
DJANGO_SLOOP_SETTINGS.setdefault('DEFAULT_SOUND', None)
DJANGO_SLOOP_SETTINGS.setdefault('DEVICE_MODEL', None)
assert DJANGO_SLOOP_SETTINGS.get('DEVICE_MODEL') or False, 'DJANGO_SLOOP_SETTINGS: DEVICE_MODEL is required.'