# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/mass_post_office/settings.py
# Compiled at: 2015-03-06 05:08:58
from django.conf import settings
SECRET_KEY = getattr(settings, 'SECRET_KEY', 'some secret key')
EMAIL_TEMPLATES_SHOULD_BE_OVERRIDED = getattr(settings, 'EMAIL_TEMPLATES_SHOULD_BE_OVERRIDED', [])