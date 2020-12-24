# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/widgets.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 3635 bytes
import logging
from django.forms.fields import ChoiceField, Field
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect, Select, TextInput
logger = logging.getLogger(__name__)

def conditional_id(choice):
    pk = choice.get('pk')
    return f"choice_{pk}"


def options_as_choices(data):
    return [(option.get('pk'), option.get('text')) for option in data.get('options', [])]


def conditional_field_from_choice(choice):
    if choice.get('options'):
        return ConditionalField.dropdown(choice)
    if choice.get('extra_info_text'):
        return ConditionalField.textinfo(choice)


class ConditionalField(object):

    @classmethod
    def dropdown(cls, choice):
        attrs = {'class':'extra-widget extra-widget-dropdown', 
         'style':'display: none;'}
        return ChoiceField(required=False,
          choices=(options_as_choices(choice)),
          widget=Select(attrs=attrs))

    @classmethod
    def textinfo(cls, choice):
        attrs = {'placeholder':choice.get('extra_info_text'), 
         'class':'extra-widget extra-widget-text', 
         'style':'display: none;'}
        return Field(required=False, widget=TextInput(attrs=attrs))


class ConditionalGenerator(object):
    __doc__ = '\n        generates the "context" data needed to render a conditional\n    '
    dropdown_var = 'extra_dropdown_widget_context'
    text_var = 'extra_text_widget_context'

    @classmethod
    def generate_context(cls, choice, querydict):
        self = cls()
        self.choice = choice
        self.querydict = querydict
        return self.context_from_conditional_type()

    def context_from_conditional_type(self):
        if self.choice.get('options'):
            field = ConditionalField.dropdown(self.choice)
            return {self.dropdown_var: self.context_from_field(field)}
        else:
            if self.choice.get('extra_info_text'):
                field = ConditionalField.textinfo(self.choice)
                return {self.text_var: self.context_from_field(field)}
            return {}

    def context_from_field(self, field):
        name = conditional_id(self.choice)
        value = field.widget.value_from_datadict(self.querydict, None, name)
        return field.widget.get_context(name, value, {})


class ConditionalSelectMixin:
    __doc__ = '\n        hooks into a Select widget, and adds conditionals to certain choices\n    '
    option_template_name = 'wizard_builder/input_option_extra.html'

    def value_from_datadict(self, data, files, name):
        self.querydict = data
        return super().value_from_datadict(data, files, name)

    def create_option(self, *args, **kwargs):
        option = (super().create_option)(*args, **kwargs)
        conditional_context = ConditionalGenerator.generate_context(choice=(self.choice_datas[int(option['index'])]),
          querydict=(self.querydict))
        option.update(conditional_context)
        return option


class ConditionalSelect(ConditionalSelectMixin, Select):
    __doc__ = '\n        A dropdown with conditional fields\n    '


class RadioConditionalSelect(ConditionalSelectMixin, RadioSelect):
    __doc__ = '\n        A radio button series with conditional fields\n    '


class CheckboxConditionalSelectMultiple(ConditionalSelectMixin, CheckboxSelectMultiple):
    __doc__ = '\n        A checkbox series with conditional fields\n    '