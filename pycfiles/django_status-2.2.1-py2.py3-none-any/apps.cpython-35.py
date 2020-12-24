# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/perdy/Development/django-status/demo/status/apps.py
# Compiled at: 2016-08-31 05:54:13
# Size of source mod 2**32: 234 bytes
"""Django application config module.
"""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class Status(AppConfig):
    name = 'status'
    verbose_name = _('Status')