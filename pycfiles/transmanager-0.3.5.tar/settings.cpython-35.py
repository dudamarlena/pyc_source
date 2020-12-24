# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/transmanager/transmanager/settings.py
# Compiled at: 2017-07-27 04:31:57
# Size of source mod 2**32: 753 bytes
"""
Settings for TransManager app
"""
from django.conf import settings
TM_API_URL = getattr(settings, 'TM_API_URL', '/transmanager/api/task/')
TM_DEFAULT_LANGUAGE_CODE = getattr(settings, 'TM_DEFAULT_LANGUAGE_CODE', 'es')
TM_DEFAULT_ENABLED_ATTRIBUTE_NAME = getattr(settings, 'TM_DEFAULT_ENABLED_ATTRIBUTE_NAME', 'enabled')
TM_BRAND_LOGO_URL = getattr(settings, 'TM_BRAND_LOGO_URL', 'transmanager/img/logo.png')
TM_ORIGINAL_VALUE_CHARS_NUMBER = getattr(settings, 'TM_ORIGINAL_VALUE_CHARS_NUMBER', 100)
TM_HAYSTACK_SUGGESTIONS_MAX_NUMBER = getattr(settings, 'TM_HAYSTACK_SUGGESTIONS_MAX_NUMBER', 20)
TM_HAYSTACK_DISABLED = getattr(settings, 'TM_HAYSTACK_DISABLED', False)
TM_DISABLED = getattr(settings, 'TM_DISABLED', False)