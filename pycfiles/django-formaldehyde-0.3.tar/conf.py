# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kraken/Projects/websites/django-formaldehyde/formaldehyde/formaldehyde/conf.py
# Compiled at: 2015-01-30 04:54:36
import sys
from django.conf import settings as django_settings
from django.utils.functional import cached_property as settings_property
if 'test' in sys.argv:
    settings_property = property

class LazySettingsDict(object):
    """ Internal properties """

    @settings_property
    def settings(self):
        return getattr(django_settings, 'FORMALDEHYDE_SETTINGS', {})

    def get_property(self, name, default):
        return self.settings.get(name, default)

    def get_property_fallback(self, name, default):
        return self.settings.get(name, getattr(django_settings, name, default))

    @settings_property
    def GRID_COLUMN_NUMBER(self):
        return self.get_property('GRID_COLUMN_NUMBER', 12)

    @settings_property
    def LABEL_COLUMN_SIZE(self):
        return self.get_property('LABEL_COLUMN_SIZE', 1)

    @settings_property
    def FIRST_LABEL_COLUMN_SIZE(self):
        return self.get_property('FIRST_LABEL_COLUMN_SIZE', 2)


settings = LazySettingsDict()