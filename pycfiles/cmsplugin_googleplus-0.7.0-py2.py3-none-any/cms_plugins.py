# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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