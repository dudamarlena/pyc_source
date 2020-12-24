# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\apps\plugins\django_microsip_catalogoarticulos\django_microsip_catalogoarticulos\forms.py
# Compiled at: 2014-10-24 12:41:24
from django import forms
from .models import *
import autocomplete_light

class ArticuloForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ArticuloForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Articulo
        exclude = ('estatus', 'costo_ultima_compra', 'seguimiento', 'es_almacenable',
                   'linea', 'es_juego')


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


class TagSearchForm(forms.Form):
    tag = forms.CharField(widget=autocomplete_light.ChoiceWidget('TagAutocomplete'))


class ArticuloSearchForm(forms.Form):
    articulo = forms.ModelChoiceField(queryset=Articulo.objects.all(), widget=autocomplete_light.ChoiceWidget('ArticuloAutocomplete'), required=False)
    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nombre...'}), required=False)
    clave = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'clave...'}), required=False)
    tag = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tag...'}), required=False)

    def __init__(self, *args, **kwargs):
        super(ArticuloSearchForm, self).__init__(*args, **kwargs)
        self.fields['articulo'].widget.attrs['class'] = 'form-control'