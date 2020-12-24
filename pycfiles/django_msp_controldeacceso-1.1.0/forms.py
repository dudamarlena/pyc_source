# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_msp_controldeacceso\django_msp_controldeacceso\forms.py
# Compiled at: 2016-02-15 12:30:53
from .models import *
from django import forms
import autocomplete_light

class LogSearch(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), widget=autocomplete_light.ChoiceWidget('ClienteAutocomplete'), required=False)
    fecha = forms.DateField(widget=forms.TextInput(attrs={'class': 'input-small'}), required=False)


class ClienteClaveSearchForm(forms.Form):
    clave = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escanea Tu clave...', 'autocomplete': 'off'}), required=False)


class ClienteManageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClienteManageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Cliente
        exclude = 'condicion_de_pago, estatus, emir_estado_cuenta, cobrar_impuestos, cuenta_xcobrar, nombre, moneda, generar_interereses, '


class PreferenciasManageForm(forms.Form):
    enterprise_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'col-md-12'}))

    def save(self, *args, **kwargs):
        enterprise_name = Registry.objects.get(nombre='SIC_Controldeacceso_NombreEmpresa')
        enterprise_name.valor = self.cleaned_data['enterprise_name']
        enterprise_name.save()


class ImagenManageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ImagenManageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ImagenSlide