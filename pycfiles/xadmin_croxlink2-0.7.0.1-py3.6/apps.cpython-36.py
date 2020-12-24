# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/xadmin/apps.py
# Compiled at: 2018-01-28 08:42:20
# Size of source mod 2**32: 394 bytes
from django.apps import AppConfig
from django.core import checks
from django.utils.translation import ugettext_lazy as _
import xadmin

class XAdminConfig(AppConfig):
    __doc__ = 'Simple AppConfig which does not do automatic discovery.'
    name = 'xadmin'
    verbose_name = _('Administration')

    def ready(self):
        self.module.autodiscover()
        setattr(xadmin, 'site', xadmin.site)