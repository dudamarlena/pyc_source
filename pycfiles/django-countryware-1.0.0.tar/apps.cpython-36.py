# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/4f/p6rdjlq11nz2jwrtdlm918l40000gn/T/pip-install-ptdu581r/django-countryware/countryware/apps.py
# Compiled at: 2018-08-21 20:41:35
# Size of source mod 2**32: 300 bytes
from django.apps import apps
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class CountrywareConfig(AppConfig):
    __doc__ = '\n    Configuration entry point for the countryware app\n    '
    label = name = 'countryware'
    verbose_name = _('countryware app')