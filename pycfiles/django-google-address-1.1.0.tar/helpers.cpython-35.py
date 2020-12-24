# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/projects/cpmd/server/api/django-google-address/google_address/helpers.py
# Compiled at: 2017-04-17 18:57:52
# Size of source mod 2**32: 168 bytes
from django.conf import settings
from django.utils.translation import ugettext as _

def get_settings(string='GOOGLE_ADDRESS'):
    return getattr(settings, string, {})