# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_mensajesdocumentos\djmicrosip_mensajesdocumentos\forms.py
# Compiled at: 2015-07-02 14:20:46
from django import forms
from .models import *
from microsip_api.apps.sms.core import SMSMasivo

class PreferenciasManageForm(forms.Form):
    empresa_nombre = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'col-md-12'}))
    apikey = forms.CharField(max_length=41, widget=forms.PasswordInput, required=False)
    VENTAS_TIPOS = (
     ('-', '--------------'),
     ('F', 'Facturas'),
     ('R', 'Remisiones'))
    ventas_tipodocumento = forms.ChoiceField(label='Enviar mensajes de documentos(Ventas) de', required=False, choices=VENTAS_TIPOS, widget=forms.Select(attrs={'class': 'form-control'}))
    PUNTOVENTA_TIPOS = (
     ('-', '--------------'),
     ('F', 'Facturas'),
     ('V', 'Ventas de mostrador'))
    puntodeventa_tipodocumento = forms.ChoiceField(label='Enviar mensajes de documentos(Punto de venta) de', required=False, choices=PUNTOVENTA_TIPOS, widget=forms.Select(attrs={'class': 'form-control'}))

    def save(self, *args, **kwargs):
        empresa_nombre = Registry.objects.get(nombre='SIC_SMS_NombreEmpresa')
        empresa_nombre.valor = self.cleaned_data['empresa_nombre']
        empresa_nombre.save()
        apikey = Registry.objects.get(nombre='SIC_SMS_ApiKey')
        apikey.valor = self.cleaned_data['apikey']
        if apikey.valor:
            apikey.save()
        ventas_tipodocumento = Registry.objects.get(nombre='SIC_MensajeDocumentos_VentasTipoDocumento')
        ventas_tipodocumento.valor = self.cleaned_data['ventas_tipodocumento']
        ventas_tipodocumento.save()
        puntodeventa_tipodocumento = Registry.objects.get(nombre='SIC_MensajeDocumentos_PuntoVentaTipoDocumento')
        puntodeventa_tipodocumento.valor = self.cleaned_data['puntodeventa_tipodocumento']
        puntodeventa_tipodocumento.save()

    def clean_apikey(self, *args, **kwargs):
        apikey = self.cleaned_data['apikey']
        if apikey:
            sms = SMSMasivo(apikey=apikey)
            if sms.credito()['estatus'] != 'ok':
                raise forms.ValidationError('Llave Invalida')
        apikey_registry = Registry.objects.get(nombre='SIC_SMS_ApiKey').valor
        if not apikey_registry and not apikey:
            raise forms.ValidationError('Campo Obligatorio')
        return apikey