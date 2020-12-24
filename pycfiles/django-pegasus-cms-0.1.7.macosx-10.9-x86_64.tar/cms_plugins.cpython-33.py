# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/plugins/tombstone/cms_plugins.py
# Compiled at: 2015-02-18 13:07:40
# Size of source mod 2**32: 617 bytes
from __future__ import absolute_import, division
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _
from .models import TombstonePlugin

class CMSTombstonePlugin(CMSPluginBase):
    model = TombstonePlugin
    module = _('Tombstone')
    name = _('Tombstone')
    render_template = 'cms/plugins/tombstone.html'

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context


plugin_pool.register_plugin(CMSTombstonePlugin)