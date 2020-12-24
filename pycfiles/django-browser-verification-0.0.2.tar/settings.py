# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/paparazziaccessories-com/venv-paparazzi/src/django-browser-verification/browser_verification/settings.py
# Compiled at: 2016-06-22 17:42:29
from django.conf import settings as django_settings
MIN_BROWSER_VERSIONS = getattr(django_settings, 'MIN_BROWSER_VERSIONS', {'Chrome': 49.0, 
   'Firefox': 45.0, 
   'IE': 11.0, 
   'Edge': 12, 
   'Safari': 8})