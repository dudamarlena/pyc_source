# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/4f/p6rdjlq11nz2jwrtdlm918l40000gn/T/pip-install-o463eux1/django-toolware/toolware/apps.py
# Compiled at: 2018-06-21 10:53:48
# Size of source mod 2**32: 308 bytes
from django.apps import apps
from django.apps import AppConfig as DjangoAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(DjangoAppConfig):
    __doc__ = '\n    Configuration entry point for the toolware app\n    '
    label = name = 'toolware'
    verbose_name = _('toolware app')