# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/echelon/forms.py
# Compiled at: 2011-09-24 06:25:11
from django.forms import ModelForm
from echelon.models import Category, Page, SiteSettings, SiteVariable
from django.forms import HiddenInput, TypedChoiceField

class CategoryForm(ModelForm):

    class Meta:
        model = Category
        exclude = ('order', 'created', 'updated')


class PageForm(ModelForm):

    class Meta:
        model = Page
        exclude = ('created', 'updated')


class CategoryOrderForm(ModelForm):

    class Meta:
        model = Category
        fields = ['order']
        widgets = {'order': HiddenInput()}


class PageOrderForm(ModelForm):

    class Meta:
        model = Page
        fields = ['order']
        widgets = {'order': HiddenInput()}


class SiteSettingsForm(ModelForm):

    class Meta:
        model = SiteSettings


class SiteVariableForm(ModelForm):
    delete = TypedChoiceField(coerce=bool, choices=(
     (
      True, 'Yes'), ('', 'No')), required=False)

    class Meta:
        model = SiteVariable
        exclude = ('site', )