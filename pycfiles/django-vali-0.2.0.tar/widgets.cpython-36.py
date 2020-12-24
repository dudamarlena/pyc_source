# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/anyi/workspace/django-vali/vali/widgets.py
# Compiled at: 2018-06-22 05:50:33
# Size of source mod 2**32: 2165 bytes
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper, FilteredSelectMultiple
from django.forms.widgets import CheckboxSelectMultiple
from django.conf import settings
from django import forms

class ValiDashboardWidget(forms.Widget):

    def render(self, name, value, attrs=None, renderer=None):
        return 'render'


class ValiDateWidget(forms.Widget):

    def render(self, name, value, attrs=None, renderer=None):
        return 'dateinput'


class ValiDateTimeWidget(forms.Widget):

    def render(self, name, value, attrs=None, renderer=None):
        return 'datetimeinput'


class ValiFilteredSelectMultiple(FilteredSelectMultiple):
    __doc__ = ' customize FilteredSelectMultiple, not used for now '

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'selectfilter'
        if self.is_stacked:
            context['widget']['attrs']['class'] += 'stacked'
        context['widget']['attrs']['data-field-name'] = self.verbose_name
        context['widget']['attrs']['data-is-stacked'] = int(self.is_stacked)
        return context


class ValiCheckboxSelectMultiple(CheckboxSelectMultiple):

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'vali-multicheckbox list-group'
        return context


class ValiRelatedFieldWidgetWrapper(RelatedFieldWidgetWrapper):
    __doc__ = ' customize ValiRelatedFieldWidgetWrapper, display auth.user.permissions in multiple checkbox '

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.widget = ValiCheckboxSelectMultiple(attrs=(self.widget.attrs), choices=(self.widget.choices))