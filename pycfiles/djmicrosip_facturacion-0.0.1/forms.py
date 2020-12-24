# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_facturacion\djmicrosip_facturacion\forms.py
# Compiled at: 2017-09-18 14:36:36
from django import forms
from .models import *
from microsip_api.comun.comun_functions import split_letranumero, get_long_folio
from django.db import connections, router

class RFCSearchForm(forms.Form):
    rfc = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'RFC', 'autocomplete': 'off', 'class': 'form-control'}))

    def clean_rfc(self):
        rfc = self.cleaned_data['rfc']
        clientes = ClienteDireccion.objects.filter(rfc_curp=rfc)
        if len(clientes) == 0:
            raise forms.ValidationError('No hay clientes con este RFC Intente con otro')
        elif len(clientes) > 1:
            raise forms.ValidationError('Hay mas de un cliente Registrado con este RFC')
        return self.cleaned_data['rfc']


class FacturarForm(forms.Form):
    folio_ticket = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Ticket', 'autocomplete': 'off', 'class': 'form-control'}))

    def clean(self):
        if self.cleaned_data:
            using = router.db_for_write(PuntoVentaDocumento)
            c = connections[using].cursor()
            ticket = self.cleaned_data['folio_ticket'].capitalize()
            folio, serie = split_letranumero(ticket)
            folio_largo = get_long_folio(folio, serie)
            venta = PuntoVentaDocumento.objects.filter(folio=folio_largo, tipo='V')
            if not venta:
                raise forms.ValidationError('No existe el ticket indicado')
            else:
                venta = venta[0]
                if venta.estado == 'C':
                    raise forms.ValidationError('El ticket se encuentra Cancelado.')
                elif venta.estado == 'D':
                    raise forms.ValidationError('El ticket se encuentra Devuelto.')
                else:
                    c.execute("select coalesce(folio,'%s') from get_folio_factura_pv(%s,'%s') ;" % ('xx', venta.id, 'F'))
                    factura = c.fetchall()[0][0]
                    if factura.strip() != 'xx':
                        raise forms.ValidationError('El ticket ya ha sido facturado.')
        return self.cleaned_data


class DireccionForm(forms.ModelForm):

    class Meta:
        model = ClienteDireccion