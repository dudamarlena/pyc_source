# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\python\hhwork\extra_apps\xadmin\apps.py
# Compiled at: 2019-04-17 23:57:58
# Size of source mod 2**32: 409 bytes
from django.apps import AppConfig
from django.core import checks
import django.utils.translation as _
import xadmin

class XAdminConfig(AppConfig):
    __doc__ = 'Simple AppConfig which does not do automatic discovery.'
    name = 'xadmin'
    verbose_name = _('Administration')

    def ready(self):
        self.module.autodiscover()
        setattr(xadmin, 'site', xadmin.site)