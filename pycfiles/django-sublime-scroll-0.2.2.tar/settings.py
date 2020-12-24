# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/arnar/git/django-sublime-scroll/sublime_scroll/settings.py
# Compiled at: 2013-03-09 15:37:11
from django.conf import settings
SUBLIME_SCROLL_WKHTMLTOIMAGE_PATH = getattr(settings, 'SUBLIME_SCROLL_WKHTMLTOIMAGE_PATH', 'wkhtmltoimage')
SUBLIME_SCROLL_SETTINGS = getattr(settings, 'SUBLIME_SCROLL_SETTINGS', {'scroll_width': 150})