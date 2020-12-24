# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cmsplugin_twitter/cms_plugins.py
# Compiled at: 2019-07-23 02:11:51
# Size of source mod 2**32: 545 bytes
from __future__ import absolute_import
import django.utils.translation as _
from cms.plugin_base import CMSPluginBase
import cms.plugin_pool as plugin_pool
from .models import Twitter

class TwitterPlugin(CMSPluginBase):
    model = Twitter
    name = _('Twitter feed Plugin')
    render_template = 'cmsplugin_twitter/plugin.html'

    def render(self, context, instance, placeholder):
        context.update({'object': instance})
        return context


plugin_pool.register_plugin(TwitterPlugin)