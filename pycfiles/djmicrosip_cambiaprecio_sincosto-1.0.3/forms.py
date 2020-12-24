# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_cambiaprecio_sincosto\djmicrosip_cambiaprecio_sincosto\forms.py
# Compiled at: 2015-05-30 12:59:55
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django_microsip_base.libs.models_base.models import ArticuloPrecio, Articulo
from django.db import connections
import autocomplete_light
from django.contrib.auth import authenticate
from django.db import router
from django.db import connections
from django.forms.models import inlineformset_factory

class ArticuloPrecioCompraForm(forms.ModelForm):
    costo_ultima_compra = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Articulo
        fields = ('costo_ultima_compra', )


class ArticuloPrecioForm(forms.ModelForm):
    precio = forms.DecimalField(widget=forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'precio...'}))

    class Meta:
        model = ArticuloPrecio
        exclude = ('precio_empresa', 'moneda', 'margen')


def ArticuloPrecioFormset(form, **kwargs):
    return inlineformset_factory(Articulo, ArticuloPrecio, form, **kwargs)


class ArticuloSearchForm(forms.Form):
    articulo = forms.ModelChoiceField(queryset=Articulo.objects.all(), widget=autocomplete_light.ChoiceWidget('ArticuloAutocomplete'), required=False)
    clave = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'clave...'}), required=False)

    def __init__(self, *args, **kwargs):
        super(ArticuloSearchForm, self).__init__(*args, **kwargs)
        self.fields['articulo'].widget.attrs['class'] = 'form-control'


class ArticuloForm(forms.ModelForm):

    class Meta:
        model = Articulo
        exclude = ('seguimiento', 'estatus', 'es_almacenable', 'es_juego', 'nombre',
                   'costo_ultima_compra')