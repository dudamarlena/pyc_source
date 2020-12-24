# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/transdb/widgets.py
# Compiled at: 2010-11-15 07:25:19
from django.forms.widgets import Widget
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.forms.util import flatatt

class TransCharWidget(Widget):
    """
    Widget that shows many labeled inputs
    Can be subclassed to change the type of input to display (overwritting "get_input()" method) 
    """

    def get_input(self, name, value, lang, attrs, id=None):
        attrs = self.build_attrs(attrs, type='text', name='%s_%s' % (name, lang), id='id_%s' % name, value=force_unicode(value))
        return '<input%s />' % flatatt(attrs)

    def render(self, name, value, attrs=None):
        if isinstance(value, dict) and value.has_key(settings.LANGUAGE_CODE):
            value_dict = value
        elif value and hasattr(value, 'raw_data'):
            value_dict = value.raw_data
        else:
            value_dict = {}
        output = []
        for (lang_code, lang_name) in settings.LANGUAGES:
            value_for_lang = ''
            if value_dict.has_key(lang_code):
                value_for_lang = value_dict[lang_code]
            if lang_code == settings.LANGUAGE_CODE:
                input = self.get_input(name, value_for_lang, lang_code, attrs, True)
            else:
                input = self.get_input(name, value_for_lang, lang_code, attrs)
            output.append('<li style="list-style-type: none; float: left; margin-right: 1em;"><span style="display: block;">%s:</span>%s</li>' % (force_unicode(lang_name), input))

        return mark_safe('<ul>%s</ul>' % ('').join(output))

    def value_from_datadict(self, data, files, name):
        value = {}
        for (lang_code, lang_name) in settings.LANGUAGES:
            value[lang_code] = data.get('%s_%s' % (name, lang_code))

        return value


class TransTextWidget(TransCharWidget):
    """
    Subclasses TransCharField to use textarea insted of input
    """

    def __init__(self, attrs=None):
        self.attrs = {'cols': '40', 'rows': '10'}
        if attrs:
            self.attrs.update(attrs)

    def get_input(self, name, value, lang, attrs, id=None):
        attrs = self.build_attrs(attrs, name='%s_%s' % (name, lang), id='id_%s' % name)
        return '<textarea%s>%s</textarea>' % (flatatt(attrs), conditional_escape(force_unicode(value)))