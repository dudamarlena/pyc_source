# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_i18n/djinn_i18n/views/module.py
# Compiled at: 2014-08-05 04:27:36
from django.views.generic import TemplateView
from djinn_i18n.tool import TOOL
from djinn_core.views.admin import AdminMixin

class ModuleView(TemplateView, AdminMixin):
    template_name = 'djinn_i18n/module.html'

    @property
    def module(self):
        return self.kwargs.get('module')

    @property
    def locale(self):
        return self.kwargs.get('locale')

    def list_entries(self):
        return TOOL.list_entries(self.module, self.locale)