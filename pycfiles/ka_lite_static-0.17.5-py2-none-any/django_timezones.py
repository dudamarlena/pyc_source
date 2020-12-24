# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/introspection_plugins/django_timezones.py
# Compiled at: 2018-07-11 18:15:31
from south.modelsinspector import add_introspection_rules
from django.conf import settings
if 'timezones' in settings.INSTALLED_APPS:
    try:
        from timezones.fields import TimeZoneField
    except ImportError:
        pass
    else:
        rules = [
         (
          (
           TimeZoneField,), [],
          {'blank': [
                     'blank', {'default': True}], 
             'max_length': [
                          'max_length', {'default': 100}]})]
        add_introspection_rules(rules, ['^timezones\\.fields'])