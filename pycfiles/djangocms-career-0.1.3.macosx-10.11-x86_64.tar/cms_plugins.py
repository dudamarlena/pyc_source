# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dominicmonn/Documents/Private/cms-sample/dev_packages/djangocms-career/djangocms_career/cms_plugins.py
# Compiled at: 2016-04-18 07:22:06
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .models import Post

class CareerPlugin(CMSPluginBase):
    module = 'Career'


class CareerContainer(CareerPlugin):
    """
    Container to hold position entries
    """
    name = _('Career Plugin Container')
    render_template = 'djangocms_career/career_plugin.html'
    allow_children = True
    child_classes = ['PositionObject']

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


class PositionObject(CareerPlugin):
    """
    Position Entries, being held by CareerContainer
    """
    name = _('Position')
    render_template = 'djangocms_career/position_object.html'
    require_parent = True
    parent_classes = ['CareerContainer']
    model = Post

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


plugin_pool.register_plugin(CareerContainer)
plugin_pool.register_plugin(PositionObject)