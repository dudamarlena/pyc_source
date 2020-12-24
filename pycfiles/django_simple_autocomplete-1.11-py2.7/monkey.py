# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/simple_autocomplete/monkey.py
# Compiled at: 2016-11-08 09:30:37
import pickle, hashlib
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.conf import settings
from django.forms.fields import Field
_simple_autocomplete_queryset_cache = {}
from simple_autocomplete.widgets import AutoCompleteWidget, AutoCompleteMultipleWidget

def ModelChoiceField__init__(self, queryset, empty_label='---------', required=True, widget=None, label=None, initial=None, help_text='', to_field_name=None, limit_choices_to=None, *args, **kwargs):
    if required and initial is not None:
        self.empty_label = None
    else:
        self.empty_label = empty_label
    if widget is None and self.__class__ in (ModelChoiceField, ModelMultipleChoiceField):
        meta = queryset.model._meta
        key = '%s.%s' % (meta.app_label, meta.model_name)
        models = getattr(settings, 'SIMPLE_AUTOCOMPLETE_MODELS', getattr(settings, 'SIMPLE_AUTOCOMPLETE', {}).keys())
        if key in models:
            pickled = pickle.dumps((
             queryset.model._meta.app_label,
             queryset.model._meta.model_name,
             queryset.query))
            token = hashlib.md5(pickled).hexdigest()
            _simple_autocomplete_queryset_cache[token] = pickled
            if self.__class__ == ModelChoiceField:
                widget = AutoCompleteWidget(token=token, model=queryset.model)
            else:
                widget = AutoCompleteMultipleWidget(token=token, model=queryset.model)
    Field.__init__(self, required, widget, label, initial, help_text, *args, **kwargs)
    self.queryset = queryset
    self.limit_choices_to = limit_choices_to
    self.to_field_name = to_field_name
    return


ModelChoiceField.__init__ = ModelChoiceField__init__

def clean_decorator(func):

    def new(self, value):
        qs = func(self, value)
        li = [ o for o in qs ]
        li.sort(lambda a, b: cmp(value.index(str(a.pk)), value.index(str(b.pk))))
        return li

    return new


ModelMultipleChoiceField.clean = clean_decorator(ModelMultipleChoiceField.clean)