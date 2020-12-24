# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/django_unsaved_changes/templatetags/unsaved_changes_tags.py
# Compiled at: 2017-12-19 19:02:17
import json
from django import template
from django.conf import settings
register = template.Library()

@register.simple_tag()
def get_unsaved_changes_settings():
    config = {'use_persistant_storage': getattr(settings, 'UNSAVED_CHANGES_PERSISTANT_STORAGE', False), 
       'use_unsaved_changes_alert': getattr(settings, 'UNSAVED_CHANGES_UNSAVED_CHANGES_ALERT', False), 
       'use_submitted_alert': getattr(settings, 'UNSAVED_CHANGES_SUMBITTED_ALERT', False), 
       'use_submitted_overlay': getattr(settings, 'UNSAVED_CHANGES_SUBMITTED_OVERLAY', False), 
       'show_unsaved_changes_visuals': getattr(settings, 'UNSAVED_CHANGES_UNSAVED_CHANGES_VISUALS', False), 
       'keyboard_shortcut_save': getattr(settings, 'UNSAVED_CHANGES_KEYBOARD_SHORTCUT_SAVE', False), 
       'debug': getattr(settings, 'DEBUG', False)}
    return json.dumps(config)