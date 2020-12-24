# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anderson/src/django-searchable-select/searchableselect/widgets.py
# Compiled at: 2017-04-18 07:21:57
from django import forms
try:
    from django.db.models.loading import get_model
except ImportError:
    from django.apps import apps
    get_model = apps.get_model

from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDict
try:
    from django.utils.datastructures import MergeDict
    DICT_TYPES = (
     MultiValueDict, MergeDict)
except:
    DICT_TYPES = (
     MultiValueDict,)

class SearchableSelect(forms.CheckboxSelectMultiple):

    class Media:
        css = {'all': ('searchableselect/main.css', )}
        js = ('searchableselect/jquery-2.2.4.min.js', 'searchableselect/bloodhound.min.js',
              'searchableselect/typeahead.jquery.min.js', 'searchableselect/main.js')

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        self.search_field = kwargs.pop('search_field')
        self.many = kwargs.pop('many', True)
        self.limit = int(kwargs.pop('limit', 10))
        super(SearchableSelect, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        if not isinstance(value, (list, tuple)):
            value = [value]
        else:
            self.many = False
        values = get_model(self.model).objects.filter(pk__in=value)
        try:
            final_attrs = self.build_attrs(attrs, name=name)
        except TypeError as e:
            final_attrs = self.build_attrs(attrs, extra_attrs={'name': name})

        return render_to_string('searchableselect/select.html', dict(field_id=final_attrs['id'], field_name=final_attrs['name'], values=values, model=self.model, search_field=self.search_field, limit=self.limit, many=self.many))

    def value_from_datadict(self, data, files, name):
        if self.many and isinstance(data, DICT_TYPES):
            return data.getlist(name)
        else:
            return data.get(name, None)