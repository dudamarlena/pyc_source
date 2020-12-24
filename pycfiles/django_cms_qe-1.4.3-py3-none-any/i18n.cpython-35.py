# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/settings/base/i18n.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 357 bytes
"""
Internationalization settings for Django app.
"""
from django.utils.translation import ugettext_lazy as _
LANGUAGE_CODE = 'en'
LANGUAGES = (
 (
  'en', _('English')),)
LOCALE_PATHS = ('locale', )
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True