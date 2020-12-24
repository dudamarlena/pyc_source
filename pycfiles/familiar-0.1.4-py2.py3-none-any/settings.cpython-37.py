# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jeffsalisbury/Documents/Code/Python_Code/familiar/familiar_tools/settings.py
# Compiled at: 2020-03-23 14:06:03
# Size of source mod 2**32: 357 bytes
from django.conf import settings
from rest_framework.settings import APISettings
settings.configure()
USER_SETTINGS = getattr(settings, 'FAMILIAR', None)
DEFAULTS = {'VERSION': '3.5'}
IMPORT_STRINGS = ('VERSION', )
api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)