# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: backstage/settings/venue_settings.py
# Compiled at: 2014-06-27 19:07:27
import os, sys
venue_DB = 'enterprise'
SITE_ID = 1
ADMINS = ()
MANAGERS = ADMINS
USE_TZ = True
TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
SECRET_KEY = '0p3ffc)q#f-4rv23&amp;yqp-f_p04p(lp(i!&amp;wljvvnk690=!0wo$'
EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
INTERNAL_IPS = ('127.0.0.1', )
venue_TEMPLATE_DIRS = [
 'venue/templates']
venue_TEMPLATE_CONTEXT_PROCESSORS = [
 'backstage.utils.context_processors.settings_constants']
UNDERSCORIFY = True