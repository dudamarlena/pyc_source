# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/growlf/django/apps/django-testimony/testimony/settings.py
# Compiled at: 2013-04-29 14:46:27
from django.conf import settings
gettext = lambda s: s
TESTIMONY_TEMPLATES = getattr(settings, 'TESTIMONY_TEMPLATES', (
 (
  'testimony/list_default.html', gettext('Default list (stationary)')),
 (
  'testimony/rotator.html', gettext('Continuous scroll (animated)')),
 (
  'testimony/vticker.html', gettext('Scroll and pause (animated)'))))