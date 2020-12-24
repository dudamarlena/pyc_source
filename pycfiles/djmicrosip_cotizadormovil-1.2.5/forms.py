# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Repos\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_cotizadormovil\djmicrosip_cotizadormovil\forms.py
# Compiled at: 2015-05-19 12:21:31
from .models import *
from django import forms
from django.forms.models import inlineformset_factory
import autocomplete_light

class VentasDocumentoDetalleForm(forms.ModelForm):
    articulo = forms.ModelChoiceField(queryset=Articulo.objects.all(), widget=autocomplete_light.ChoiceWidget('ArticuloAutocomplete'), required=False)

    def __init__(self, *args, **kwargs):
        super(VentasDocumentoDetalleForm, self).__init__(*args, **kwargs)
        self.fields['unidades'].widget = forms.TextInput(attrs={'class': 'form-control text-right'})
        self.fields['precio_unitario'].widget = forms.TextInput(attrs={'class': 'form-control text-right'})
        self.fields['descuento_porcentaje'].widget = forms.TextInput(attrs={'class': 'form-control text-right'})
        self.fields['precio_total_neto'].widget = forms.TextInput(attrs={'class': 'form-control text-right'})

    class Meta:
        model = VentasDocumentoDetalle
        fields = ('articulo', 'unidades', 'precio_unitario', 'descuento_porcentaje',
                  'precio_total_neto')


def CotizacionFormset(form, **kwargs):
    return inlineformset_factory(VentasDocumento, VentasDocumentoDetalle, form, **kwargs)


class PreferenciasManageForm(forms.Form):
    CHOICES = (
     ('N', 'No integrar'),
     ('V', 'Ventas'),
     ('P', 'Punto de Venta'))
    crear_documento = forms.ChoiceField(required=True, choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    pv_cliente = forms.ModelChoiceField(Cliente.objects.all(), widget=autocomplete_light.ChoiceWidget('ClienteAutocomplete'), required=True)
    pv_almacen = forms.ModelChoiceField(queryset=Almacen.objects.all(), required=True)
    pv_caja = forms.ModelChoiceField(queryset=Caja.objects.all(), required=True)
    pv_cajero = forms.ModelChoiceField(queryset=Cajero.objects.all(), required=True)
    pv_vendedor = forms.ModelChoiceField(queryset=Vendedor.objects.all(), required=True)
    ve_cliente = forms.ModelChoiceField(Cliente.objects.all(), widget=autocomplete_light.ChoiceWidget('ClienteAutocomplete'), required=True)
    ve_almacen = forms.ModelChoiceField(queryset=Almacen.objects.all(), required=True)
    ve_condicion_pago = forms.ModelChoiceField(queryset=CondicionPago.objects.all(), required=True)
    ve_vendedor = forms.ModelChoiceField(queryset=Vendedor.objects.all(), required=True)

    def save(self, *args, **kwargs):
        using = kwargs.get('using', None)
        crear_documento = Registry.objects.get(nombre='SIC_cotizadorm_integrar')
        if crear_documento.valor != self.cleaned_data['crear_documento']:
            crear_documento.valor = self.cleaned_data['crear_documento']
            crear_documento.save()
        pv_cliente = Registry.objects.get(nombre='SIC_cotizadorm_cliente_pv')
        if pv_cliente.valor != self.cleaned_data['pv_cliente']:
            pv_cliente.valor = self.cleaned_data['pv_cliente']
            pv_cliente.save()
        pv_almacen = Registry.objects.get(nombre='SIC_cotizadorm_almacen_pv')
        if pv_almacen.valor != self.cleaned_data['pv_almacen']:
            pv_almacen.valor = self.cleaned_data['pv_almacen']
            pv_almacen.save()
        pv_caja = Registry.objects.get(nombre='SIC_cotizadorm_Caja_pv')
        if pv_caja.valor != self.cleaned_data['pv_caja']:
            pv_caja.valor = self.cleaned_data['pv_caja']
            pv_caja.save()
        pv_cajero = Registry.objects.get(nombre='SIC_cotizadorm_Cajero_pv')
        if pv_cajero.valor != self.cleaned_data['pv_cajero']:
            pv_cajero.valor = self.cleaned_data['pv_cajero']
            pv_cajero.save()
        pv_vendedor = Registry.objects.get(nombre='SIC_cotizadorm_Vendedor_pv')
        if pv_vendedor.valor != self.cleaned_data['pv_vendedor']:
            pv_vendedor.valor = self.cleaned_data['pv_vendedor']
            pv_vendedor.save()
        ve_cliente = Registry.objects.get(nombre='SIC_cotizadorm_cliente_ve')
        if ve_cliente.valor != self.cleaned_data['ve_cliente']:
            ve_cliente.valor = self.cleaned_data['ve_cliente']
            ve_cliente.save()
        ve_almacen = Registry.objects.get(nombre='SIC_cotizadorm_almacen_ve')
        if ve_almacen.valor != self.cleaned_data['ve_almacen']:
            ve_almacen.valor = self.cleaned_data['ve_almacen']
            ve_almacen.save()
        ve_condicion_pago = Registry.objects.get(nombre='SIC_cotizadorm_CondicionPago_ve')
        if ve_condicion_pago.valor != self.cleaned_data['ve_condicion_pago']:
            ve_condicion_pago.valor = self.cleaned_data['ve_condicion_pago']
            ve_condicion_pago.save()
        ve_vendedor = Registry.objects.get(nombre='SIC_cotizadorm_Vendedor_ve')
        if ve_vendedor.valor != self.cleaned_data['ve_vendedor']:
            ve_vendedor.valor = self.cleaned_data['ve_vendedor']
            ve_vendedor.save()
        return