# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bfschott/Source/cmsplugin-newsplus/cmsplugin_newsplus/forms.py
# Compiled at: 2016-06-07 17:28:14
from __future__ import absolute_import
from django import forms
from cms.plugin_pool import plugin_pool
from djangocms_text_ckeditor.widgets import TextEditorWidget
from cmsplugin_newsplus.models import News

class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = '__all__'

    def _get_widget(self):
        plugins = plugin_pool.get_text_enabled_plugins(placeholder=None, page=None)
        return TextEditorWidget(installed_plugins=plugins)

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        widget = self._get_widget()
        self.fields['excerpt'].widget = widget
        self.fields['content'].widget = widget