# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/cmsplugin_googleform/cms_plugins.py
# Compiled at: 2012-06-05 11:16:37
from django.utils.translation import ugettext as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cmsplugin_googleform.models import GoogleFormsPlugin

class CMSGoogleFormsPlugin(CMSPluginBase):
    model = GoogleFormsPlugin
    name = _('Google Form')
    render_template = 'cms/plugins/googleform/googleform.html'

    def render(self, context, instance, placeholder):
        context.update({'form_key': instance.form_id, 'form_width': instance.width, 
           'form_height': instance.height})
        return context


plugin_pool.register_plugin(CMSGoogleFormsPlugin)