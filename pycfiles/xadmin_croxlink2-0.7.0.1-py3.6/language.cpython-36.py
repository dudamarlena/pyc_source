# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/xadmin/plugins/language.py
# Compiled at: 2020-02-22 03:13:29
# Size of source mod 2**32: 1022 bytes
from django.conf import settings
from django.template import loader
from django.views.i18n import set_language
from xadmin.plugins.utils import get_context_dict
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, CommAdminView, BaseAdminView

class SetLangNavPlugin(BaseAdminPlugin):

    def block_top_navmenu(self, context, nodes):
        context = get_context_dict(context)
        context['redirect_to'] = self.request.get_full_path()
        nodes.append(loader.render_to_string('xadmin/blocks/comm.top.setlang.html', context=context))


class SetLangView(BaseAdminView):

    def post(self, request, *args, **kwargs):
        if 'nav_menu' in request.session:
            del request.session['nav_menu']
        return set_language(request)


if settings.LANGUAGES:
    if settings.MIDDLEWARE:
        if 'django.middleware.locale.LocaleMiddleware' in settings.MIDDLEWARE:
            site.register_plugin(SetLangNavPlugin, CommAdminView)
            site.register_view('^i18n/setlang/$', SetLangView, 'set_language')