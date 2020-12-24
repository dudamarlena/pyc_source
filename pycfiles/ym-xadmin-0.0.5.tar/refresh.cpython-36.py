# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: G:\python\hhwork\extra_apps\xadmin\plugins\refresh.py
# Compiled at: 2019-01-06 19:47:42
# Size of source mod 2**32: 1411 bytes
from django.template import loader
from xadmin.plugins.utils import get_context_dict
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, ListAdminView
REFRESH_VAR = '_refresh'

class RefreshPlugin(BaseAdminPlugin):
    refresh_times = []

    def get_media(self, media):
        if self.refresh_times:
            if self.request.GET.get(REFRESH_VAR):
                media = media + self.vendor('xadmin.plugin.refresh.js')
        return media

    def block_top_toolbar(self, context, nodes):
        if self.refresh_times:
            current_refresh = self.request.GET.get(REFRESH_VAR)
            context.update({'has_refresh':bool(current_refresh), 
             'clean_refresh_url':self.admin_view.get_query_string(remove=(REFRESH_VAR,)), 
             'current_refresh':current_refresh, 
             'refresh_times':[{'time':r,  'url':self.admin_view.get_query_string({REFRESH_VAR: r}),  'selected':str(r) == current_refresh} for r in self.refresh_times]})
            nodes.append(loader.render_to_string('xadmin/blocks/model_list.top_toolbar.refresh.html', get_context_dict(context)))


site.register_plugin(RefreshPlugin, ListAdminView)