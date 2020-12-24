# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/template/settings.py
# Compiled at: 2015-05-19 08:43:44
# Size of source mod 2**32: 402 bytes
from django.conf import settings
JINJA2_ENVIRONMENT_OPTIONS = getattr(settings, 'JINJA2_ENVIRONMENT_OPTIONS', {})
JINJA2_EXTENSIONS = getattr(settings, 'JINJA2_EXTENSIONS', [])
JINJA2_AUTOESCAPE = getattr(settings, 'JINJA2_AUTOESCAPE', True)
JINJA2_NEWSTYLE_GETTEXT = getattr(settings, 'JINJA2_NEWSTYLE_GETTEXT', True)
JINJA2_EXCLUDED_FOLDERS = getattr(settings, 'JINJA2_EXCLUDED_FOLDERS', ())