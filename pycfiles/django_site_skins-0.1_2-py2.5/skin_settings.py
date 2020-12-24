# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skins/skin_settings.py
# Compiled at: 2010-03-20 20:08:48
"""A central mechanism for settings with defaults.
"""
from django.conf import settings
import os
skin_settings_defaults = {'DEFAULT_SKIN': 'default', 
   'SKIN_DIRS': (
               os.path.join(settings.MEDIA_ROOT, 'skins'),)}

def add_setting_defaults(newdefaults):
    """
    This method can be used by other applications to define their
    default values.

    newdefaults has to be a dictionary containing name -> value of
    the settings.
    """
    skin_settings_defaults.update(newdefaults)


def set_skin_setting(name, value):
    if not hasattr(settings, 'SKIN_SETTINGS'):
        settings.SKIN_SETTINGS = {}
    settings.SKIN_SETTINGS[name] = value


def get_skin_setting(name, default_value=None):
    if not hasattr(settings, 'SKIN_SETTINGS'):
        return skin_settings_defaults.get(name, default_value)
    return settings.SKIN_SETTINGS.get(name, skin_settings_defaults.get(name, default_value))