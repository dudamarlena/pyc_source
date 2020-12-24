# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rmartins/Desenvolvimento/Django/Apps/wagtaildemo/smart_selects/form_fields.py
# Compiled at: 2016-01-06 07:19:32
try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model

from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.forms import ChoiceField
from smart_selects.widgets import ChainedSelect, ChainedSelectMultiple
from django.utils.encoding import force_text
import traceback

class ChainedModelChoiceField(ModelChoiceField):

    def __init__(self, to_app_name, to_model_name, chained_field, chained_model_field, foreign_key_app_name, foreign_key_model_name, foreign_key_field_name, show_all, auto_choose, manager=None, initial=None, view_name=None, *args, **kwargs):
        defaults = {'widget': ChainedSelect(to_app_name, to_model_name, chained_field, chained_model_field, foreign_key_app_name, foreign_key_model_name, foreign_key_field_name, show_all, auto_choose, manager, view_name)}
        defaults.update(kwargs)
        if 'queryset' not in kwargs:
            queryset = get_model(to_app_name, to_model_name).objects.all()
            super(ChainedModelChoiceField, self).__init__(queryset=queryset, initial=initial, *args, **defaults)
        else:
            super(ChainedModelChoiceField, self).__init__(initial=initial, *args, **defaults)

    def _get_choices(self):
        self.widget.queryset = self.queryset
        choices = super(ChainedModelChoiceField, self)._get_choices()
        return choices

    choices = property(_get_choices, ChoiceField._set_choices)


class ChainedManyToManyField(ModelMultipleChoiceField):

    def __init__(self, to_app_name, to_model_name, chain_field, chained_model_field, foreign_key_app_name, foreign_key_model_name, foreign_key_field_name, auto_choose, manager=None, initial=None, *args, **kwargs):
        defaults = {'widget': ChainedSelectMultiple(to_app_name, to_model_name, chain_field, chained_model_field, foreign_key_app_name, foreign_key_model_name, foreign_key_field_name, auto_choose, manager)}
        defaults.update(kwargs)
        if 'queryset' not in kwargs:
            queryset = get_model(to_app_name, to_model_name).objects.all()
            super(ChainedManyToManyField, self).__init__(queryset=queryset, initial=initial, *args, **defaults)
        else:
            super(ChainedManyToManyField, self).__init__(initial=initial, *args, **defaults)


class GroupedModelSelect(ModelChoiceField):

    def __init__(self, queryset, order_field, *args, **kwargs):
        self.order_field = order_field
        super(GroupedModelSelect, self).__init__(queryset, *args, **kwargs)

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        group_indexes = {}
        choices = [
         (
          '', self.empty_label or '---------')]
        i = len(choices)
        for item in self.queryset:
            order_field = getattr(item, self.order_field)
            group_index = order_field.pk
            if group_index not in group_indexes:
                group_indexes[group_index] = i
                choices.append([force_text(order_field), []])
                i += 1
            choice_index = group_indexes[group_index]
            choices[choice_index][1].append(self.make_choice(item))

        return choices

    def make_choice(self, obj):
        return (
         obj.pk, '   ' + self.label_from_instance(obj))

    choices = property(_get_choices, ChoiceField._set_choices)