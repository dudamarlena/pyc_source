# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_microsip_consultaprecio\django_microsip_consultaprecio\forms.py
# Compiled at: 2015-11-13 19:01:52
from django import forms
from .models import *
import autocomplete_light

class ArticuloSearchForm(forms.Form):
    clave = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escanea Tu Articulo...', 'autocomplete': 'off'}))


class PreferenciasManageForm(forms.Form):
    empresa_nombre = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'col-md-12'}))
    empresa_slogan = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'col-md-12'}), required=False)
    cliente_eventual = forms.ModelChoiceField(queryset=Cliente.objects.all(), widget=autocomplete_light.ChoiceWidget('ClienteAutocomplete'))

    def save(self, *args, **kwargs):
        empresa_nombre = Registry.objects.get(nombre='SIC_ConsultaPrecio_NombreEmpresa')
        empresa_nombre.valor = self.cleaned_data['empresa_nombre']
        empresa_nombre.save()
        empresa_slogan = Registry.objects.get(nombre='SIC_ConsultaPrecio_Slogan')
        empresa_slogan.valor = self.cleaned_data['empresa_slogan']
        empresa_slogan.save()
        cliente_eventual = Registry.objects.get(nombre='SIC_ConsultaPrecio_Cliente')
        cliente_eventual.valor = self.cleaned_data['cliente_eventual']
        cliente_eventual.save()


class ImagenManageForm(forms.ModelForm):

    class Meta:
        model = ImagenSlideChecador