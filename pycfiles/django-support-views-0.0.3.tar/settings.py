# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/paparazziaccessories-com/venv-paparazzi/src/support-views/support_views/settings.py
# Compiled at: 2017-11-17 15:28:05
from django.conf import settings as django_settings
SUPPORT_EXTRA_CONTEXT = getattr(django_settings, 'SUPPORT_EXTRA_CONTEXT', lambda r: {})