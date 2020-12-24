# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jgorset/code/python/libraries/respite/respite/settings.py
# Compiled at: 2012-09-28 03:36:32
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
DEFAULT_FORMAT = getattr(settings, 'RESPITE_DEFAULT_FORMAT', 'html')