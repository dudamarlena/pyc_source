# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: G:\python\hhwork\extra_apps\xadmin\plugins\sitemenu.py
# Compiled at: 2019-01-06 19:47:42
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, CommAdminView
BUILDIN_STYLES = {'default': 'xadmin/includes/sitemenu_default.html', 
   'accordion': 'xadmin/includes/sitemenu_accordion.html'}

class SiteMenuStylePlugin(BaseAdminPlugin):
    menu_style = None

    def init_request(self, *args, **kwargs):
        return bool(self.menu_style) and self.menu_style in BUILDIN_STYLES

    def get_context(self, context):
        context['menu_template'] = BUILDIN_STYLES[self.menu_style]
        return context


site.register_plugin(SiteMenuStylePlugin, CommAdminView)