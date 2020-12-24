# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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