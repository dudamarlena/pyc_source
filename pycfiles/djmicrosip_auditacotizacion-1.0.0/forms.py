# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_auditacotizacion\djmicrosip_auditacotizacion\forms.py
# Compiled at: 2015-12-05 14:34:44
from django import forms
from .models import *
from django.forms.models import inlineformset_factory
import autocomplete_light

class AuuditoriaForm(forms.Form):
    clave = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clave...'}))


class VentasDocumentoDetalleForm(forms.ModelForm):
    articulo = forms.ModelChoiceField(queryset=Articulo.objects.all(), widget=autocomplete_light.ChoiceWidget('ArticuloAutocomplete'), required=False)

    def __init__(self, *args, **kwargs):
        super(VentasDocumentoDetalleForm, self).__init__(*args, **kwargs)
        self.fields['unidades'].widget = forms.TextInput(attrs={'class': 'form-control text-right'})

    class Meta:
        model = VentasDocumentoDetalle
        fields = ('articulo', 'unidades')


def CotizacionFormset(form, **kwargs):
    return inlineformset_factory(VentasDocumento, VentasDocumentoDetalle, form, **kwargs)