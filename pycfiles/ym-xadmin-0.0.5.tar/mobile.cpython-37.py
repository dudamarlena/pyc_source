# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\python\hhwork\extra_apps\xadmin\plugins\mobile.py
# Compiled at: 2019-04-17 23:57:58
# Size of source mod 2**32: 934 bytes
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, CommAdminView

class MobilePlugin(BaseAdminPlugin):

    def _test_mobile(self):
        try:
            return self.request.META['HTTP_USER_AGENT'].find('Android') >= 0 or self.request.META['HTTP_USER_AGENT'].find('iPhone') >= 0
        except Exception:
            return False

    def init_request(self, *args, **kwargs):
        return self._test_mobile()

    def get_context(self, context):
        context['is_mob'] = True
        return context

    def block_extrahead(self, context, nodes):
        nodes.append('<script>window.__admin_ismobile__ = true;</script>')


site.register_plugin(MobilePlugin, CommAdminView)