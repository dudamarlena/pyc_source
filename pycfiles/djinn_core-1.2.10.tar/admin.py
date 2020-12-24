# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/projects/pythonunited/provgroningen/buildout/src/djinn_core/djinn_core/views/admin.py
# Compiled at: 2014-08-05 04:26:20
import pkg_resources
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

class AdminMixin(object):
    """ Mixin for admin views """

    def list_tools(self):
        tools = []
        for entrypoint in pkg_resources.iter_entry_points(group='djinn.tool', name='info'):
            tool = entrypoint.load()()
            tool['url'] = reverse(tool['url'])
            tools.append(tool)

        return tools


class AdminView(TemplateView, AdminMixin):
    template_name = 'djinn_core/admin.html'