# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/apps/cms/plugins/text/cms_plugins.py
# Compiled at: 2009-10-31 23:19:40
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _
from models import Text
from cms.plugins.text.forms import TextForm
from cms.plugins.text.widgets import WYMEditor
from cms.plugins.text.utils import plugin_tags_to_user_html
from django.forms.fields import CharField

class TextPlugin(CMSPluginBase):
    model = Text
    name = _('Text')
    form = TextForm
    render_template = 'cms/plugins/text.html'

    def get_editor_widget(self, request, plugins):
        """
        Returns the Django form Widget to be used for
        the text area
        """
        return WYMEditor(installed_plugins=plugins)

    def get_form_class(self, request, plugins):
        """
        Returns a subclass of Form to be used by this plugin
        """

        class TextPluginForm(self.form):
            pass

        widget = self.get_editor_widget(request, plugins)
        TextPluginForm.declared_fields['body'] = CharField(widget=widget, required=False)
        return TextPluginForm

    def get_form(self, request, obj=None, **kwargs):
        plugins = plugin_pool.get_text_enabled_plugins(self.placeholder)
        form = self.get_form_class(request, plugins)
        kwargs['form'] = form
        return super(TextPlugin, self).get_form(request, obj, **kwargs)

    def render(self, context, instance, placeholder):
        return {'body': plugin_tags_to_user_html(instance.body, context, placeholder), 'placeholder': placeholder}


plugin_pool.register_plugin(TextPlugin)