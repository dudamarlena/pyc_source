# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/th13f/dev/pretty_form_errors/dcf_pretty_form_errors/form_mixins.py
# Compiled at: 2016-01-14 09:44:14
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class PrettyFormMixin(object):

    def __init__(self, *args, **kwargs):
        super(PrettyFormMixin, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        helper.error_text_inline = True
        helper._help_text_inline = True
        helper.allow_auto_tooltip_placement = True
        helper.field_template = 'pretty_forms/bootstrap3/field.html'

    class Media:
        css = {'all': ('pretty_forms/css/bootstrap-tooltip.css', 'pretty_forms/css/form-pretty-errors.css',
 'pretty_forms/fonts/question-font/style.css')}
        js = ('pretty_forms/js/jquery_extensions.js', 'pretty_forms/js/bootstrap-tooltip.js',
              'pretty_forms/js/enable-form-tooltips.js')


class PrettyFormPlaceholdersMixin(PrettyFormMixin):

    def __init__(self, *args, **kwargs):
        super(PrettyFormPlaceholdersMixin, self).__init__(*args, **kwargs)
        helper = self.helper
        layout = helper.layout = Layout()
        for field_name in self.fields:
            field = self.fields[field_name]
            label = field.label if field.label else field_name.capitalize()
            layout.append(Field(field_name, placeholder=label + (' *' if field.required else ''), template=helper.field_template, css_class='pretty_field'))

        helper.form_show_labels = False