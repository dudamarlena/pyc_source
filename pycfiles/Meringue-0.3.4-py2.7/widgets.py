# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/meringue/widgets.py
# Compiled at: 2015-08-17 17:37:49
from django import forms
from django.db import models
from django.utils.encoding import force_text
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from meringue.utils.thumbnails import get_thumbnail

class PreviewImageFileInput(forms.widgets.FileInput):
    """
    TO-DO:
        информация о изображении
        изображение при инициализации
        при загрузке изображения сразу же его выводить в превью (js)
    """
    initial_text = _('Currently')
    input_text = _('Change')
    clear_checkbox_label = _('Clear')
    preview = '<img src="%(src)s" data-src="%(data_src)s" >'
    template_with_initial = '<p class="file-upload">%(preview)s<br />        %(initial_text)s: %(initial)s %(clear_template)s<br />        %(input_text)s: %(input)s</p>'
    template_with_clear = '<span class="clearable-file-input">        %(clear)s <label for="%(clear_checkbox_id)s">        %(clear_checkbox_label)s</label></span>'
    url_markup_template = '<a href="{0}">{1}</a>'

    def clear_checkbox_name(self, name):
        """
        Given the name of the file input, return the name of the clear
        checkbox input.
        """
        return name + '-clear'

    def clear_checkbox_id(self, name):
        """
        Given the name of the clear checkbox input, return the HTML id
        for it.
        """
        return name + '_id'

    def get_preview(self, value, size):
        if value:
            data = {'src': get_thumbnail(value.path, [
                     's:%dx%d' % size,
                     'resize',
                     'crop']), 
               'data_src': value.url}
        else:
            data = {'src': '', 
               'data_src': ''}
        return self.preview % data

    def render(self, name, value, size=(100, 100), attrs=None):
        substitutions = {'initial_text': self.initial_text, 
           'preview': self.get_preview(value, size), 
           'input_text': self.input_text, 
           'clear_template': '', 
           'clear_checkbox_label': self.clear_checkbox_label}
        template = '%(input)s'
        substitutions['input'] = super(PreviewImageFileInput, self).render(name, value, attrs)
        if value and hasattr(value, 'url'):
            template = self.template_with_initial
            substitutions['initial'] = format_html(self.url_markup_template, value.url, force_text(value))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = forms.CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions
        return mark_safe(template % substitutions)