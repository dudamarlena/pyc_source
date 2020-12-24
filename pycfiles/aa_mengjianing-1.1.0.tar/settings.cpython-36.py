# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./../aa_airtable/settings.py
# Compiled at: 2017-06-21 21:50:37
# Size of source mod 2**32: 2541 bytes
__doc__ = '\nSettings for Airtable are all namespaced in the AIRTABLE setting. For example your project"s "settings.py" file\nmight look like this:\n\nAIRTABLE = {\n\n}\n\nTo simplify overriding those settings they have a flat structure.\n\nThis code is based on Django Rest Framework"s settings.\n'
from django.conf import settings
from django.test.signals import setting_changed
DEFAULTS = {'API_KEY':'', 
 'DATABASES':{},  'ENDPOINT_URL':'https://api.airtable.com/v0/', 
 'DATA_DIRECTORY':'airtable-data', 
 'FILES_DIRECTORY':'airtable-files', 
 'SAVE_FILES':True}

class AirtableSettings(object):
    """AirtableSettings"""

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