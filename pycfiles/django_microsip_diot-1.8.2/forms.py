# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_microsip_diot\django_microsip_diot\forms.py
# Compiled at: 2015-11-24 14:59:04
from django import forms
from .models import *
import autocomplete_light
from django.contrib.auth import authenticate

class ProveedorSearchForm(forms.Form):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), widget=autocomplete_light.ChoiceWidget('ProveedorAutocomplete'), required=False)
    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre...'}), required=False)

    def __init__(self, *args, **kwargs):
        super(ProveedorSearchForm, self).__init__(*args, **kwargs)
        self.fields['proveedor'].widget.attrs['class'] = 'form-control'


class ProveedorForm(forms.ModelForm):
    cuenta_por_pagar = forms.ModelChoiceField(ContabilidadCuentaContable.objects.all(), widget=autocomplete_light.ChoiceWidget('ContabilidadCuentaContableAutocomplete'), required=False)

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
        self.fields['pais'].widget = autocomplete_light.ChoiceWidget('PaisAutocomplete')
        if 'instance' in kwargs:
            self.id = kwargs['instance'].id

    def clean(self, *args, **kwargs):
        cuenta_por_pagar_obj = self.cleaned_data['cuenta_por_pagar']
        if cuenta_por_pagar_obj:
            cuenta_xpagar = cuenta_por_pagar_obj.cuenta
        else:
            cuenta_xpagar = ''
        if cuenta_xpagar and Proveedor.objects.exclude(id=self.id).filter(cuenta_xpagar=cuenta_xpagar).exists():
            raise forms.ValidationError('La cuenta contable %s ya existe con otro proveedor' % cuenta_xpagar)
        self.cleaned_data['cuenta_xpagar'] = cuenta_xpagar
        return self.cleaned_data

    class Meta:
        model = Proveedor
        exclude = ('estado', 'ciudad', 'tipo')


class GeneraDiotForm(forms.Form):
    fecha_inicio = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    fecha_fin = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    inicio_ext = forms.DateField(widget=forms.TextInput(attrs={'class': 'input-small'}), required=False)
    repos_ext = forms.BooleanField(initial=False, required=False)

    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        inicio_ext = cleaned_data.get('inicio_ext')
        if fecha_inicio and fecha_fin:
            if fecha_inicio > fecha_fin:
                raise forms.ValidationError('La fecha de inicio no puede ser mayor que la fecha de fin')
            if fecha_inicio.month != fecha_fin.month:
                raise forms.ValidationError('Las fechas deben ser del mismo mes')
            elif fecha_inicio.year != fecha_fin.year:
                raise forms.ValidationError('Las fechas deben ser del mismo año')
        return cleaned_data


class PreferenciasManageForm(forms.Form):
    IMPUESTOS = (
     ('0', 'IVA AL 0'), ('E', 'EXENTO'))
    impuesto_default = forms.ChoiceField(widget=forms.RadioSelect, choices=IMPUESTOS)
    rfc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    integrar_contabilidad = forms.BooleanField(required=False)

    def save(self, *args, **kwargs):
        impuesto_default = self.cleaned_data['impuesto_default']
        tasa_no_iva_default = Registry.objects.get(nombre='SIC_DIOT_tasaNoIVADefault')
        tasa_no_iva_default.valor = impuesto_default
        tasa_no_iva_default.save()
        rfc_cd = self.cleaned_data['rfc']
        rfc = Registry.objects.get(nombre='Rfc')
        rfc.valor = rfc_cd
        rfc.save()
        integrar_contabilidad_cd = self.cleaned_data['integrar_contabilidad']
        integrar_contabilidad = Registry.objects.get(nombre='SIC_DIOT_integrar_contabilidad')
        integrar_contabilidad.valor = integrar_contabilidad_cd
        integrar_contabilidad.save()


class ManualForm(forms.Form):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), widget=autocomplete_light.ChoiceWidget('ProveedorAutocomplete'), required=False)
    fecha_manual = forms.DateField(widget=forms.TextInput(attrs={'class': 'input-small'}))


class InicializarPagosForm(forms.Form):
    ANIOS = (
     ('2001', '2001'),
     ('2002', '2002'),
     ('2003', '2003'),
     ('2004', '2004'),
     ('2005', '2005'),
     ('2006', '2006'),
     ('2007', '2007'),
     ('2008', '2008'),
     ('2009', '2009'),
     ('2010', '2010'),
     ('2011', '2011'),
     ('2012', '2012'),
     ('2013', '2013'),
     ('2014', '2014'),
     ('2015', '2015'),
     ('2016', '2016'),
     ('2017', '2017'),
     ('2018', '2018'),
     ('2019', '2019'),
     ('2020', '2020'),
     ('2021', '2021'),
     ('2022', '2022'),
     ('2023', '2023'),
     ('2024', '2024'),
     ('2025', '2025'),
     ('2026', '2026'),
     ('2027', '2027'),
     ('2028', '2028'),
     ('2029', '2029'),
     ('2030', '2030'))
    MESES = (
     ('01', 'Enero'),
     ('02', 'Febrero'),
     ('03', 'Marzo'),
     ('04', 'Abril'),
     ('05', 'Mayo'),
     ('06', 'Junio'),
     ('07', 'Julio'),
     ('08', 'Agosto'),
     ('09', 'Septiembre'),
     ('10', 'Octubre'),
     ('11', 'Noviembre'),
     ('12', 'Diciembre'))
    anio = forms.ChoiceField(required=False, choices=ANIOS, widget=forms.Select(attrs={'class': 'form-control'}))
    mes = forms.ChoiceField(required=False, choices=MESES, widget=forms.Select(attrs={'class': 'form-control'}))
    total = forms.BooleanField(initial=False, required=False)
    sysdba_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password de SYSDBA...'}))

    def clean_sysdba_password(self, *args, **kwargs):
        sysdba_password = self.cleaned_data['sysdba_password']
        usuario = authenticate(username='SYSDBA', password=sysdba_password)
        if not usuario:
            raise forms.ValidationError('contraseña invalida')
        return sysdba_password

    def clean_dinero_electronico(self):
        dinero_electronico = self.cleaned_data['dinero_electronico']
        if not dinero_electronico:
            raise forms.ValidationError('Campo obligatorio.')
        return dinero_electronico

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data