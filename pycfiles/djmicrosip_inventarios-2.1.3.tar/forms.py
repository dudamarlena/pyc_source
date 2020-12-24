# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_inventarios\djmicrosip_inventarios\inventarios_fisicos\forms.py
# Compiled at: 2019-09-17 20:13:05
from django import forms
from .models import *

class AlmacenInventariadoForm(forms.ModelForm):

    class Meta:
        model = Almacen
        exclude = ('nombre', 'inventariando')


class EntradaInventarioForm(forms.Form):
    linea = forms.ModelChoiceField(LineaArticulos.objects.all(), required=False)
    clave_articulo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'clave...'}), required=False)
    articulo = forms.ModelChoiceField(Articulo.objects.filter(seguimiento='N'), widget=autocomplete_light.ChoiceWidget('ArticuloNormalAutocomplete'))
    articulo_serie = forms.ModelChoiceField(Articulo.objects.filter(seguimiento='S'), widget=autocomplete_light.ChoiceWidget('ArticuloSerieAutocomplete'))
    ubicacion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-lg-1', 'placeholder': 'Ubicacion...'}), required=False)