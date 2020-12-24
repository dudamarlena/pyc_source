# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_puntos\djmicrosip_puntos\forms.py
# Compiled at: 2015-07-09 14:41:15
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.db import connections
import autocomplete_light
from django.contrib.auth import authenticate
from django.db import router
from django.db import connections

def BooleanTo01(value):
    if value:
        return 1
    return 0


class InicializarPuntosArticulosForm(forms.Form):
    sysdba_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password de SYSDBA...'}))

    def clean_sysdba_password(self, *args, **kwargs):
        sysdba_password = self.cleaned_data['sysdba_password']
        usuario = authenticate(username='SYSDBA', password=sysdba_password)
        if not usuario:
            raise forms.ValidationError('contraseña invalida')
        return sysdba_password


class ArticuloSearchForm(forms.Form):
    articulo = forms.ModelChoiceField(queryset=Articulo.objects.all(), widget=autocomplete_light.ChoiceWidget('ArticuloAutocomplete'), required=False)
    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nombre...'}), required=False)
    clave = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'clave...'}), required=False)

    def __init__(self, *args, **kwargs):
        super(ArticuloSearchForm, self).__init__(*args, **kwargs)
        self.fields['articulo'].widget.attrs['class'] = 'form-control'


class ClienteClaveSearchForm(forms.Form):
    cliente = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autofocus': ''}), required=True)


class ClienteSearchForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), widget=autocomplete_light.ChoiceWidget('ClienteAutocomplete'), required=False)
    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nombre...'}), required=False)
    clave = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'clave...'}), required=False)

    def __init__(self, *args, **kwargs):
        super(ClienteSearchForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].widget.attrs['class'] = 'form-control'


class articulos_form(forms.ModelForm):

    class Meta:
        model = Articulo
        exclude = ('seguimiento', 'estatus', 'es_almacenable', 'es_juego', 'nombre',
                   'costo_ultima_compra', 'es_importado')


class LineaArticulosForm(forms.ModelForm):

    class Meta:
        model = LineaArticulos
        exclude = ('cuenta_ventas', 'nombre')


class GrupoLineasForm(forms.ModelForm):

    class Meta:
        model = GrupoLineas
        exclude = ('cuenta_ventas', 'nombre')


class ClienteTipoForm(forms.ModelForm):

    class Meta:
        model = ClienteTipo
        exclude = ('nombre', )


class ClienteManageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClienteManageForm, self).__init__(*args, **kwargs)
        self.fields['hereda_puntos_a'].widget = autocomplete_light.ChoiceWidget('ClienteAutocomplete')
        self.fields['vigencia_fecha_inicio'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['vigencia_fecha_fin'].widget = forms.TextInput(attrs={'class': 'form-control'})

    class Meta:
        model = Cliente
        exclude = ('cuenta_xcobrar', 'estatus', 'tipo_cliente', 'condicion_de_pago',
                   'emir_estado_cuenta', 'cobrar_impuestos', 'moneda', 'nombre',
                   'generar_interereses')


from datetime import datetime

class PreferenciasPuntosManageForm(forms.Form):
    FRECUENCIA_TIPOS = (
     ('D', 'Dias'),
     ('S', 'Semanas'),
     ('M', 'Meses'),
     ('A', 'Años'))
    vigencia_inicio_periodo = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    vigencia_fin_periodo = forms.DateField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    vigencia_frecuencia_tipo = forms.ChoiceField(required=False, choices=FRECUENCIA_TIPOS, widget=forms.Select(attrs={'class': 'form-control'}))
    vigencia_frecuencia = forms.IntegerField(min_value=0, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    triggers_activos = forms.BooleanField(required=False)
    precio_con_impuestos = forms.BooleanField(required=False)
    porcentaje_menos_credito = forms.DecimalField(min_value=0, max_value=100)
    articulo_dinero_electronico = forms.DecimalField(min_value=0, max_value=100)
    condicion_de_pago_contado = forms.ModelChoiceField(queryset=CondicionPago.objects.all())
    cajero_general = forms.ModelChoiceField(queryset=Cajero.objects.exclude(operar_cajas='N'))
    caja_general = forms.ModelChoiceField(queryset=Caja.objects.all())
    cliente_eventual_pv = forms.ModelChoiceField(queryset=Cliente.objects.all(), widget=autocomplete_light.ChoiceWidget('ClienteAutocomplete'))
    articulo_general = forms.ModelChoiceField(queryset=Articulo.objects.filter(es_almacenable='N', es_juego='N'), widget=autocomplete_light.ChoiceWidget('ArticuloAutocomplete'))
    dar_dinero_alpagar = forms.BooleanField(required=False)
    limite_gastarporventa = forms.DecimalField(min_value=0, max_value=100)

    def clean_caja_general(self, *args, **kwargs):
        caja_general = self.cleaned_data['caja_general']
        if not caja_general:
            raise forms.ValidationError('Campo obligatorio.')
        return caja_general

    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data
        cajero = cleaned_data.get('cajero_general')
        caja = cleaned_data.get('caja_general')
        vigencia_inicio_dia = cleaned_data.get('vigencia_inicio_dia')
        vigencia_inicio_mes = cleaned_data.get('vigencia_inicio_mes')
        vigencia_inicio_anio = cleaned_data.get('vigencia_inicio_anio')
        if cajero and not cajero.operar_cajas == 'T' and not CajeroCaja.objects.filter(cajero=cajero, caja=caja).exists():
            raise forms.ValidationError('La caja [%s] no puede ser operada por el cajero [%s]' % (caja, cajero))
        return cleaned_data

    def save(self, *args, **kwargs):
        using = kwargs.get('using', None)
        vigencia_inicio_periodo_obj = Registry.objects.get(nombre='SIC_Puntos_VigenciaInicioPeriodoFecha')
        if vigencia_inicio_periodo_obj.valor != self.cleaned_data['vigencia_inicio_periodo']:
            vigencia_inicio_periodo_obj.valor = self.cleaned_data['vigencia_inicio_periodo']
            vigencia_inicio_periodo_obj.save()
        vigencia_fin_periodo_obj = Registry.objects.get(nombre='SIC_Puntos_VigenciaFinPeriodoFecha')
        if vigencia_fin_periodo_obj.valor != self.cleaned_data['vigencia_fin_periodo']:
            vigencia_fin_periodo_obj.valor = self.cleaned_data['vigencia_fin_periodo']
            vigencia_fin_periodo_obj.save()
        vigencia_frecuencia_tipo_obj = Registry.objects.get(nombre='SIC_Puntos_VigenciaFrecuenciaTipo')
        if vigencia_frecuencia_tipo_obj.valor != self.cleaned_data['vigencia_frecuencia_tipo']:
            vigencia_frecuencia_tipo_obj.valor = self.cleaned_data['vigencia_frecuencia_tipo']
            vigencia_frecuencia_tipo_obj.save()
        vigencia_frecuencia_obj = Registry.objects.get(nombre='SIC_Puntos_VigenciaFrecuencia')
        if vigencia_frecuencia_obj.valor != self.cleaned_data['vigencia_frecuencia']:
            vigencia_frecuencia_obj.valor = self.cleaned_data['vigencia_frecuencia']
            vigencia_frecuencia_obj.save()
        from custom_db.punto_venta import sql_queries as pv_sql_queries
        if self.cleaned_data['triggers_activos']:
            for trigger in pv_sql_queries.triggers_activate:
                c = connections[using].cursor()
                c.execute(pv_sql_queries.triggers_activate[trigger])
                c.close()

        else:
            triggers_activate_keys = pv_sql_queries.triggers_activate.keys()
            triggers_activate_keys += ['SIC_PUNTOS_PV_CLIENTES_BU', 'SIC_PUNTOS_PV_DOCTOSPVDET_AD', 'SIC_PUNTOS_PV_DOCTOSPVDET_BU']
            c = connections[using].cursor()
            for trigger_key in triggers_activate_keys:
                sql = 'drop trigger %s;' % trigger_key
                try:
                    c.execute(sql)
                except:
                    pass

            c.close()
        articulo_puntos_obj = Registry.objects.get(nombre='SIC_PUNTOS_ARTICULO_PUNTOS_PREDET')
        articulo_dinero_electronico_obj = Registry.objects.get(nombre='SIC_PUNTOS_ARTICULO_DINERO_ELECT_PREDET')
        articulo_dinero_electronico_obj.valor = self.cleaned_data['articulo_dinero_electronico']
        articulo_dinero_electronico_obj.save()
        caja_general_obj = Registry.objects.get(nombre='SIC_PUNTOS_CAJA_GRAL')
        caja_general_obj.valor = self.cleaned_data['caja_general']
        caja_general_obj.save()
        cajero_general_obj = Registry.objects.get(nombre='SIC_PUNTOS_CAJERO_GRAL')
        cajero_general_obj.valor = self.cleaned_data['cajero_general']
        cajero_general_obj.save()
        condicion_pago_contado_obj = Registry.objects.get(nombre='SIC_CONDICION_PAGO_CONTADO')
        condicion_pago_contado_obj.valor = self.cleaned_data['condicion_de_pago_contado']
        condicion_pago_contado_obj.save()
        cliente_eventual_id = Registry.objects.get(nombre='CLIENTE_EVENTUAL_PV_ID').get_value()
        cliente_eventual_pv_obj = Registry.objects.get(nombre='CLIENTE_EVENTUAL_PV_ID')
        cliente_eventual_pv_obj.valor = self.cleaned_data['cliente_eventual_pv']
        cliente_eventual_pv_obj.save()
        articulo_general_obj = Registry.objects.get(nombre='ARTICULO_VENTAS_FG_PV_ID')
        articulo_general_obj.valor = self.cleaned_data['articulo_general']
        articulo_general_obj.save()
        articulo_general_obj = Registry.objects.get(nombre='SIC_Puntos_DarDineroEnPagos')
        articulo_general_obj.valor = BooleanTo01(self.cleaned_data['dar_dinero_alpagar'])
        articulo_general_obj.save()
        articulo_general_obj = Registry.objects.get(nombre='SIC_Puntos_LimiteAGastarPorVenta')
        articulo_general_obj.valor = self.cleaned_data['limite_gastarporventa']
        articulo_general_obj.save()
        precio_con_impuestos = self.cleaned_data['precio_con_impuestos']
        if precio_con_impuestos:
            precio_con_impuestos = 1
        else:
            precio_con_impuestos = 0
        precio_con_impuestos_obj = Registry.objects.get(nombre='SIC_Puntos_PrecioConImpuestos')
        precio_con_impuestos_obj.valor = precio_con_impuestos
        precio_con_impuestos_obj.save()
        porcentaje_menos_credito_obj = Registry.objects.get(nombre='SIC_Puntos_PorcentajeMenosCredito')
        porcentaje_menos_credito_obj.valor = self.cleaned_data['porcentaje_menos_credito']
        porcentaje_menos_credito_obj.save()
        return


class DarDineroForm(forms.Form):
    dinero_electronico = forms.DecimalField(initial=0, max_value=2000, decimal_places=2, widget=forms.TextInput(attrs={'class': 'input-mini form-control'}), required=False)
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), widget=autocomplete_light.ChoiceWidget('ClienteAutocomplete'))
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
        using = router.db_for_write(Caja)
        caja = Registry.objects.get(nombre='SIC_PUNTOS_CAJA_GRAL').get_value()
        if caja:
            caja = Caja.objects.get(pk=caja)
            c = connections[using].cursor()
            c.execute('EXECUTE PROCEDURE GET_ESTATUS_CAJA (%s)' % caja.id)
            estatus_caja = c.fetchall()
            estatus_caja = estatus_caja[0][1]
            c.close()
            if estatus_caja == 'A':
                raise forms.ValidationError('la caja [%s] se encuentra abierta, es nesesario cerrar la caja para generar las tarjetas.' % caja.nombre)
        else:
            raise forms.ValidationError('Por favor define primero la caja general en [ Herramientas > Preferencias]. ')
        if not Registry.objects.get(nombre='ARTICULO_VENTAS_FG_PV_ID').get_value():
            raise forms.ValidationError('Por favor define primero el articulo general en preferencias de empresa de microsip')
        if not Registry.objects.get(nombre='CLIENTE_EVENTUAL_PV_ID').get_value():
            raise forms.ValidationError('Por favor define primero el cliente eventual en preferencias de empresa de microsip')
        return cleaned_data


class GenerarTarjetasForm(forms.Form):
    prefijo = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'class': 'input-mini'}))
    iniciar_en = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'input-mini'}))
    cantidad = forms.IntegerField(max_value=6000, widget=forms.TextInput(attrs={'class': 'input-mini'}))
    TIPOS_TARJETA = (('D', 'Dinero Electronico'), )
    tipo_tarjeta = forms.ChoiceField(choices=TIPOS_TARJETA)
    puntos = forms.IntegerField(initial=0, widget=forms.TextInput(attrs={'class': 'input-mini'}), required=False)
    dinero_electronico = forms.DecimalField(initial=0, max_value=2000, decimal_places=2, widget=forms.TextInput(attrs={'class': 'input-mini'}), required=False)
    valor_puntos = forms.DecimalField(initial=1, max_digits=15, decimal_places=2, widget=forms.TextInput(attrs={'class': 'input-mini'}), required=False)
    sysdba_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password de SYSDBA...'}))

    def clean_sysdba_password(self, *args, **kwargs):
        sysdba_password = self.cleaned_data['sysdba_password']
        usuario = authenticate(username='SYSDBA', password=sysdba_password)
        if not usuario:
            raise forms.ValidationError('contraseña invalida')
        return sysdba_password

    def clean_iniciar_en(self):
        iniciar_en = self.cleaned_data['iniciar_en']
        if not iniciar_en:
            raise forms.ValidationError('Campo obligatorio.')
        return iniciar_en

    def clean(self):
        cleaned_data = self.cleaned_data
        prefijo = cleaned_data.get('prefijo')
        using = router.db_for_write(Caja)
        caja = Registry.objects.get(nombre='SIC_PUNTOS_CAJA_GRAL').get_value()
        if caja:
            caja = Caja.objects.get(pk=caja)
            c = connections[using].cursor()
            c.execute('EXECUTE PROCEDURE GET_ESTATUS_CAJA (%s)' % caja.id)
            estatus_caja = c.fetchall()
            estatus_caja = estatus_caja[0][1]
            c.close()
            if estatus_caja == 'A':
                raise forms.ValidationError('la caja [%s] se encuentra abierta, es nesesario cerrar la caja para generar las tarjetas.' % caja.nombre)
        else:
            raise forms.ValidationError('Por favor define primero la caja general en [ Herramientas > Preferencias]. ')
        tipo_tarjeta = cleaned_data.get('tipo_tarjeta')
        valor_puntos = cleaned_data.get('valor_puntos')
        puntos = cleaned_data.get('puntos')
        dinero_electronico = cleaned_data.get('dinero_electronico')
        iniciar_en = cleaned_data.get('iniciar_en')
        cantidad = cleaned_data.get('cantidad')
        if tipo_tarjeta == 'P' and puntos == None:
            raise forms.ValidationError('Por favor define los puntos de las tarjetas')
        if tipo_tarjeta == 'P' and valor_puntos == None:
            raise forms.ValidationError('Por favor define el valor en $ dinero de cada punto')
        if tipo_tarjeta == 'D' and dinero_electronico == None:
            raise forms.ValidationError('Por favor define el dinero electronico de las tarjetas')
        if not Registry.objects.get(nombre='ARTICULO_VENTAS_FG_PV_ID').get_value():
            raise forms.ValidationError('Por favor define primero el articulo general en preferencias de empresa de microsip')
        if not Registry.objects.get(nombre='CLIENTE_EVENTUAL_PV_ID').get_value():
            raise forms.ValidationError('Por favor define primero el cliente eventual en preferencias de empresa de microsip')
        if iniciar_en != None and cantidad != None:
            claves = []
            for numero in range(iniciar_en, iniciar_en + cantidad):
                claves.append('%s%s' % (prefijo, '%09d' % numero))

            if ClienteClave.objects.filter(clave__in=claves).exists():
                raise forms.ValidationError('Ya Existe una o mas claves en este rango')
        return cleaned_data