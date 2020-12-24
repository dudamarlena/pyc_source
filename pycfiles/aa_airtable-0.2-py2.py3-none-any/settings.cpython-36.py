# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./../aa_airtable/settings.py
# Compiled at: 2017-06-21 21:50:37
# Size of source mod 2**32: 2541 bytes
"""
Settings for Airtable are all namespaced in the AIRTABLE setting. For example your project"s "settings.py" file
might look like this:

AIRTABLE = {

}

To simplify overriding those settings they have a flat structure.

This code is based on Django Rest Framework"s settings.
"""
from django.conf import settings
from django.test.signals import setting_changed
DEFAULTS = {'API_KEY':'', 
 'DATABASES':{},  'ENDPOINT_URL':'https://api.airtable.com/v0/', 
 'DATA_DIRECTORY':'airtable-data', 
 'FILES_DIRECTORY':'airtable-files', 
 'SAVE_FILES':True}

class AirtableSettings(object):
    __doc__ = '\n    A settings object, that allows settings to be accessed as properties.\n    For example:\n\n        from aa_airtable.settings import airtable_settings\n        print(airtable_settings.API_KEY)\n\n    Any setting with string import paths will be automatically resolved\n    and return the class, rather than the string literal.\n    '

    def __init__(self, user_settings=None):
        if user_settings:
            self._user_settings = self._AirtableSettings__check_user_settings(user_settings)

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'AIRTABLE_SETTINGS', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in DEFAULTS:
            raise AttributeError('Invalid setting: {}'.format(attr))
        try:
            val = self.user_settings[attr]
        except KeyError:
            val = DEFAULTS[attr]

        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        for setting in user_settings:
            if setting not in DEFAULTS:
                raise RuntimeError('The %s is incorrect. Please check settings.DEFAULTS for the available options')

        return user_settings


class AirtableSettingOutter(object):

    def __init__(self, settings_inner):
        self.settings_inner = settings_inner

    def __getattr__(self, attr):
        return getattr(self.settings_inner, attr)


airtable_settings = AirtableSettingOutter(AirtableSettings())

def reload_airtable_settings(*args, **kwargs):
    global airtable_settings
    setting, value = kwargs['setting'], kwargs['value']
    if setting == 'AIRTABLE_SETTINGS':
        airtable_settings.settings_inner = AirtableSettings(value)


setting_changed.connect(reload_airtable_settings)