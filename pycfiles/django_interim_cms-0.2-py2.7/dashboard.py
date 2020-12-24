# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/interim_cms/dashboard.py
# Compiled at: 2015-06-10 02:57:48
from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard import modules, Dashboard
from interim_cms.modules import ExampleModule, StaticModule

class LeftDashboard(Dashboard):

    def init_with_context(self, context):
        self.children = []
        self.children.append(modules.AppList(column=1, title='Administration'))


class CenterDashboard(Dashboard):

    def init_with_context(self, context):
        self.children = []
        self.children.append(StaticModule(title='Welcome', collapsible=False, template='interim_cms/welcome.html'))


class RightDashboard(Dashboard):

    class Media:
        js = ('interim_cms/js/cms.js', 'interim_cms/js/Chart.min.js', 'interim_cms/js/jquery.cookie.js')
        css = {'all': ('interim_cms/css/cms.css', 'interim_cms/css/skin.css')}

    def init_with_context(self, context):
        self.children = []
        if 'empty' in context['request'].GET:
            return
        self.children.append(modules.RecentActions(_('Recent Actions'), limit=5, collapsible=False, column=1))
        if context['request'].user.is_authenticated():
            self.children.append(ExampleModule(title='Foo'))