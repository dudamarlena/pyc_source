# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Sites/senpilic.com.tr/senpilic/utils/cms_plugins.py
# Compiled at: 2012-11-19 10:50:40
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin

class HeaderPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _('Global Header')
    render_template = 'utils/_header.html'
    module = _('Utils')

    def render(self, context, instance, placeholder):
        return context


plugin_pool.register_plugin(HeaderPlugin)

class FooterPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _('Global Footer')
    render_template = 'utils/_footer.html'
    module = _('Utils')

    def render(self, context, instance, placeholder):
        return context


plugin_pool.register_plugin(FooterPlugin)

class BreadcrumbPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _('Breadcrumb')
    render_template = 'utils/breadcrumb.html'
    module = _('Utils')

    def render(self, context, instance, placeholder):
        return context


plugin_pool.register_plugin(BreadcrumbPlugin)

class SubmenuPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _('Submenu')
    render_template = 'utils/submenu.html'
    module = _('Utils')

    def render(self, context, instance, placeholder):
        return context


plugin_pool.register_plugin(SubmenuPlugin)