# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmusilek/github/django-fido/django_fido/settings.py
# Compiled at: 2020-03-12 10:55:09
# Size of source mod 2**32: 684 bytes
"""Django settings specific for django_fido."""
from __future__ import unicode_literals
from appsettings import AppSettings, BooleanSetting, CallablePathSetting, NestedListSetting, StringSetting

class DjangoFidoSettings(AppSettings):
    __doc__ = 'Application specific settings.'
    authentication_backends = NestedListSetting(inner_setting=(CallablePathSetting()),
      default=('django.contrib.auth.backends.ModelBackend', ),
      transform_default=True)
    rp_name = StringSetting(default=None)
    two_step_auth = BooleanSetting(default=True)

    class Meta:
        __doc__ = 'Meta class.'
        setting_prefix = 'django_fido_'


SETTINGS = DjangoFidoSettings()