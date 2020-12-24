# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_organizador\djmicrosip_organizador\forms.py
# Compiled at: 2015-02-07 15:36:52
from django import forms
from .models import *
import autocomplete_light
from django.forms.models import BaseInlineFormSet, inlineformset_factory, modelformset_factory

class ArticuloForm(forms.ModelForm):

    class Meta:
        model = Articulo
        exclude = ('seguimiento', 'estatus', 'es_almacenable', 'es_juego', 'costo_ultima_compra')


class TagSearchForm(forms.Form):
    tag = forms.CharField(widget=autocomplete_light.ChoiceWidget('TagAutocomplete'))


class TagForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.id = kwargs['instance'].id

    def clean_tag(self, *args, **kwargs):
        tag = self.cleaned_data['tag']
        if Tag.objects.exclude(id=self.id).filter(tag=tag).exists():
            raise forms.ValidationError('El tag %s ya existe' % tag)
        return tag

    class Meta:
        model = Tag


class TagArticuloForm(forms.ModelForm):
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), widget=autocomplete_light.ChoiceWidget('TagAutocomplete'))

    class Meta:
        widgets = autocomplete_light.get_widgets_dict(TagArticulo)
        model = TagArticulo


def articulotags_formset(form, **kwargs):
    return inlineformset_factory(Articulo, TagArticulo, form, **kwargs)