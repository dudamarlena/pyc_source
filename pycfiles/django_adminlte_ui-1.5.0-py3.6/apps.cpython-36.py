# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/adminlteui/apps.py
# Compiled at: 2020-01-21 04:26:45
# Size of source mod 2**32: 297 bytes
from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
__all__ = [
 'AdminlteUIConfig']

class AdminlteUIConfig(AppConfig):
    name = 'adminlteui'
    label = 'django_admin_settings'
    verbose_name = _('AdminSettings')