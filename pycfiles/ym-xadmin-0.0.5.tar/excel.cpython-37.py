# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\python\hhwork\extra_apps\xadmin\plugins\excel.py
# Compiled at: 2019-04-17 23:57:58
# Size of source mod 2**32: 882 bytes
from django.template import loader
import xadmin
from xadmin.plugins.utils import get_context_dict
from xadmin.views import BaseAdminPlugin, ListAdminView

class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', get_context_dict(context)))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)