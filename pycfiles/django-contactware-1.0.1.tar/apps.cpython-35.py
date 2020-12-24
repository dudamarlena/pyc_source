# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/bizdir/apps/django-contactware/contactware/apps.py
# Compiled at: 2016-08-11 12:49:02
# Size of source mod 2**32: 317 bytes
from django.apps import apps
from django.apps import AppConfig as DjangoAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(DjangoAppConfig):
    __doc__ = '\n    Configuration entry point for the contactware app\n    '
    label = name = 'contactware'
    verbose_name = _('contactware app')