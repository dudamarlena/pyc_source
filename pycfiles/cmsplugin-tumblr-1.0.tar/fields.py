# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jrief/Workspace/virtualenvs/gfg/src/cmsplugin-text-wrapper/cmsplugin_text_wrapper/fields.py
# Compiled at: 2013-07-23 13:35:52
from django import forms
from django.db import models
from django.utils.text import capfirst
from django.core import exceptions

class MultiSelectFormField(forms.MultipleChoiceField):
    widget = forms.CheckboxSelectMultiple

    def __init__(self, *args, **kwargs):
        self.max_choices = kwargs.pop('max_choices', 0)
        super(MultiSelectFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        return value


class MultiSelectField(models.Field):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return 'CharField'

    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def _get_FIELD_display(self, field):
        value = getattr(self, field.attname)
        choicedict = dict(field.choices)

    def formfield(self, **kwargs):
        defaults = {'required': not self.blank, 'label': capfirst(self.verbose_name), 'help_text': self.help_text, 
           'choices': self.choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_prep_value(self, value):
        return value

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if isinstance(value, basestring):
            return value
        if isinstance(value, list):
            return (',').join(value)

    def to_python(self, value):
        if value is not None:
            if isinstance(value, list):
                return value
            return value.split(',')
        else:
            return ''

    def contribute_to_class(self, cls, name):
        super(MultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            func = lambda self, fieldname=name, choicedict=dict(self.choices): (',').join([ choicedict.get(value, value) for value in getattr(self, fieldname) ])
            setattr(cls, 'get_%s_display' % self.name, func)

    def validate(self, value, model_instance):
        arr_choices = self.get_choices_selected(self.get_choices_default())
        for opt_select in value:
            if int(opt_select) not in arr_choices:
                raise exceptions.ValidationError(self.error_messages['invalid_choice'] % value)

    def get_choices_selected(self, arr_choices=''):
        if not arr_choices:
            return False
        choices = []
        for choice_selected in arr_choices:
            choices.append(choice_selected[0])

        return choices

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ['^cmsplugin_text_wrapper\\.fields\\.MultiSelectField'])