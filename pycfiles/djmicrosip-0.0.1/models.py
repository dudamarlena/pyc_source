# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Admin\Documents\GitHub\djmicrosip\djmicrosip\ventas\ventas_documentos\models.py
# Compiled at: 2015-01-28 22:14:31
from django.db import models
from datetime import datetime
from django.db import router
from djmicrosip.core.db import next_id
import django_dynamic_models as dymodels
app_label = 'djmicrosip.ventas.ventas_documentos'
from djmicrosip.comun.impuestos.models import Impuesto
from djmicrosip.comun.clientes.models import Cliente, ClienteDireccion, CondicionPago
from djmicrosip.comun.articulos.models import Almacen, Articulo
from djmicrosip.comun.listas.models import Vendedor
from djmicrosip.comun.general.models import ViaEmbarque, Moneda
from djmicrosip.comun.impuestos.models import Impuesto

class VentasDocumentoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='DOCTO_VE_ID')
    tipo = models.CharField(max_length=1, db_column='TIPO_DOCTO')
    subtipo = models.CharField(max_length=1, blank=True, null=True, db_column='SUBTIPO_DOCTO')
    folio = models.CharField(max_length=9, db_column='FOLIO')
    fecha = models.DateField(db_column='FECHA')
    cliente = models.ForeignKey(Cliente, db_column='CLIENTE_ID')
    cliente_clave = models.CharField(max_length=20, blank=True, null=True, db_column='CLAVE_CLIENTE')
    cliente_direccion = models.ForeignKey(ClienteDireccion, db_column='DIR_CLI_ID', related_name='direccion_cliente')
    direccion_consignatario = models.ForeignKey(ClienteDireccion, db_column='DIR_CONSIG_ID', related_name='direccion_consignatario')
    almacen = models.ForeignKey(Almacen, db_column='ALMACEN_ID')
    moneda = models.ForeignKey(Moneda, db_column='MONEDA_ID')
    tipo_cambio = models.DecimalField(default=1, max_digits=18, decimal_places=6, db_column='TIPO_CAMBIO')
    descuento_tipo = models.CharField(default='P', max_length=1, db_column='TIPO_DSCTO')
    descuento_porcentaje = models.DecimalField(default=0, max_digits=9, decimal_places=6, db_column='DSCTO_PCTJE')
    descuento_importe = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='DSCTO_IMPORTE')
    estado = models.CharField(max_length=1, db_column='ESTATUS')
    aplicado = models.CharField(default='S', max_length=1, db_column='APLICADO')
    vigencia_entrega_fecha = models.DateField(blank=True, null=True, db_column='FECHA_VIGENCIA_ENTREGA')
    orden_compra = models.CharField(max_length=35, blank=True, null=True, db_column='ORDEN_COMPRA')
    orden_compra_fecha = models.CharField(max_length=35, blank=True, null=True, db_column='FECHA_ORDEN_COMPRA')
    recibo_mercancia_folio = models.CharField(max_length=35, blank=True, null=True, db_column='FOLIO_RECIBO_MERCANCIA')
    recibo_mercancia_fecha = models.CharField(max_length=35, blank=True, null=True, db_column='FECHA_RECIBO_MERCANCIA')
    descripcion = models.CharField(blank=True, null=True, max_length=200, db_column='DESCRIPCION')
    importe_neto = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='IMPORTE_NETO')
    fletes = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='FLETES')
    otros_cargos = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='OTROS_CARGOS')
    impuestos_total = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='TOTAL_IMPUESTOS')
    retenciones_total = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='TOTAL_RETENCIONES')
    fpgc_total = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='TOTAL_FPGC')
    peso_enbarque = models.DecimalField(default=0, max_digits=12, decimal_places=3, db_column='PESO_EMBARQUE')
    SI_O_NO = (('S', 'Si'), ('N', 'No'))
    forma_emitida = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='FORMA_EMITIDA')
    contabilizado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='CONTABILIZADO')
    acreditar_cuentasxcobrar = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='ACREDITAR_CXC')
    sistema_origen = models.CharField(max_length=2, db_column='SISTEMA_ORIGEN')
    condicion_pago = models.ForeignKey(CondicionPago, db_column='COND_PAGO_ID')
    descuentoxprontopago_fecha = models.DateField(blank=True, null=True, db_column='FECHA_DSCTO_PPAG')
    descuentoxprontopago_porcentaje = models.DecimalField(default=0, max_digits=9, decimal_places=6, db_column='PCTJE_DSCTO_PPAG')
    vendedor = models.ForeignKey(Vendedor, blank=True, null=True, db_column='VENDEDOR_ID')
    comisiones_porcentaje = models.DecimalField(default=0, max_digits=9, decimal_places=6, db_column='PCTJE_COMIS')
    via_embarque = models.ForeignKey(ViaEmbarque, blank=True, null=True, db_column='VIA_EMBARQUE_ID')
    cobro_importe = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='IMPORTE_COBRO')
    cobro_descripcion = models.CharField(blank=True, null=True, max_length=200, db_column='DESCRIPCION_COBRO')
    impuesto_sustituido = models.ForeignKey(Impuesto, on_delete=models.SET_NULL, blank=True, null=True, db_column='IMPUESTO_SUSTITUIDO_ID', related_name='impuesto_sustituido_re')
    impuesto_sustituto = models.ForeignKey(Impuesto, on_delete=models.SET_NULL, blank=True, null=True, db_column='IMPUESTO_SUSTITUTO_ID', related_name='impuesto_sustituto_re')
    es_cfd = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='ES_CFD')
    modalidad_facturacion = models.CharField(max_length=10, db_column='MODALIDAD_FACTURACION')
    envio_enviado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='ENVIADO')
    envio_email = models.EmailField(blank=True, null=True, db_column='EMAIL_ENVIO')
    envio_fechahora = models.DateTimeField(default=datetime.now(), blank=True, null=True, db_column='FECHA_HORA_ENVIO')
    cfd_envio_especial = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='CFD_ENVIO_ESPECIAL')
    cfd_certificado = models.CharField(default='N', max_length=1, choices=SI_O_NO, db_column='CFDI_CERTIFICADO')
    cargar_sun = models.CharField(default='S', max_length=1, db_column='CARGAR_SUN')
    creacion_usuario = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_CREADOR')
    creacion_fechahora = models.DateTimeField(default=datetime.now().replace(hour=0), db_column='FECHA_HORA_CREACION')
    creacion_usuario_aut = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_CREACION')
    modificacion_usuario = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_ULT_MODIF')
    modificacion_fechahora = models.DateTimeField(auto_now=True, db_column='FECHA_HORA_ULT_MODIF')
    modificacion_usuario_aut = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_MODIF')
    cancelacion_usuario = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_CANCELACION')
    cancelacion_fechahora = models.DateTimeField(blank=True, null=True, db_column='FECHA_HORA_CANCELACION')
    cancelacion_usuario_aut = models.CharField(blank=True, null=True, max_length=31, db_column='USUARIO_AUT_CANCELACION')

    class Meta:
        db_table = 'doctos_ve'
        abstract = True

    def __unicode__(self):
        return '%s' % self.folio

    def _get_importe_total(self):
        return self.importe_neto + self.impuestos_total - self.retenciones_total

    importe_total = property(_get_importe_total)

    def save(self, *args, **kwargs):
        if not self.id:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(VentasDocumentoBase, instance=self)
            self.id = next_id('ID_DOCTOS', using)
        super(VentasDocumentoBase, self).save(*args, **kwargs)
        return


VentasDocumento = dymodels.change.load('VentasDocumento', VentasDocumentoBase, app_label)

class VentasDocumentoVencimientoBase(models.Model):
    documento = models.ForeignKey('VentasDocumento', unique_for_date='fecha', db_column='DOCTO_VE_ID')
    fecha = models.DateField(db_column='FECHA_VENCIMIENTO')
    porcentaje_de_venta = models.PositiveSmallIntegerField(db_column='PCTJE_VEN')

    class Meta:
        db_table = 'vencimientos_cargos_ve'
        abstract = True


VentasDocumentoVencimiento = dymodels.change.load('VentasDocumentoVencimiento', VentasDocumentoVencimientoBase, app_label)

class VentasDocumentoImpuestoManager(models.Manager):

    def get_by_natural_key(self, documento, impuesto):
        return self.get(documento_pv=documento, impuesto=impuesto)


class VentasDocumentoImpuestoBase(models.Model):
    objects = VentasDocumentoImpuestoManager()
    documento = models.ForeignKey('VentasDocumento', db_column='DOCTO_VE_ID')
    impuesto = models.ForeignKey(Impuesto, db_column='IMPUESTO_ID')
    venta_neta = models.DecimalField(max_digits=15, decimal_places=2, db_column='VENTA_NETA')
    otros = models.DecimalField(max_digits=15, decimal_places=2, db_column='OTROS_IMPUESTOS')
    porcentaje = models.DecimalField(max_digits=9, decimal_places=6, db_column='PCTJE_IMPUESTO')
    importe = models.DecimalField(max_digits=15, decimal_places=2, db_column='IMPORTE_IMPUESTO')
    unidades = models.DecimalField(max_digits=15, decimal_places=2, db_column='UNIDADES_IMPUESTO')
    importe_unitario = models.DecimalField(max_digits=15, decimal_places=2, db_column='IMPORTE_UNITARIO_IMPUESTO')

    class Meta:
        db_table = 'impuestos_doctos_ve'
        unique_together = (('documento', 'impuesto'), )
        abstract = True


VentasDocumentoImpuesto = dymodels.change.load('VentasDocumentoImpuesto', VentasDocumentoImpuestoBase, app_label)

class VentasDocumentoDetalleBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='DOCTO_VE_DET_ID')
    documento = models.ForeignKey('VentasDocumento', on_delete=models.SET_NULL, blank=True, null=True, db_column='DOCTO_VE_ID')
    articulo_clave = models.CharField(max_length=20, blank=True, null=True, db_column='CLAVE_ARTICULO')
    articulo = models.ForeignKey(Articulo, on_delete=models.SET_NULL, blank=True, null=True, db_column='ARTICULO_ID')
    unidades = models.DecimalField(default=0, max_digits=18, decimal_places=5, db_column='UNIDADES')
    unidades_comprometidas = models.DecimalField(default=0, max_digits=18, decimal_places=5, db_column='UNIDADES_COMPROM')
    unidades_surtidas_devueltas = models.DecimalField(default=0, max_digits=18, decimal_places=5, db_column='UNIDADES_SURT_DEV')
    unidades_a_surtir = models.DecimalField(default=0, max_digits=18, decimal_places=5, db_column='UNIDADES_A_SURTIR')
    precio_unitario = models.DecimalField(default=0, max_digits=18, decimal_places=6, db_column='PRECIO_UNITARIO')
    fpgc_unitario = models.DecimalField(default=0, max_digits=18, decimal_places=6, db_column='FPGC_UNITARIO')
    descuento_porcentaje = models.DecimalField(default=0, max_digits=9, decimal_places=6, db_column='PCTJE_DSCTO')
    descuento_porcentaje_cli = models.DecimalField(default=0, max_digits=9, decimal_places=6, db_column='PCTJE_DSCTO_CLI')
    descuento_porcentaje_vol = models.DecimalField(default=0, max_digits=9, decimal_places=6, db_column='PCTJE_DSCTO_VOL')
    descuento_porcentaje_promo = models.DecimalField(default=0, max_digits=9, decimal_places=6, db_column='PCTJE_DSCTO_PROMO')
    precio_total_neto = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='PRECIO_TOTAL_NETO')
    comisiones_porcentaje = models.DecimalField(default=0, max_digits=9, decimal_places=6, db_column='PCTJE_COMIS')
    rol = models.CharField(default='N', max_length=1, db_column='ROL')
    notas = models.CharField(blank=True, null=True, max_length=80, db_column='NOTAS')
    posicion = models.SmallIntegerField(default=-1, db_column='POSICION')

    class Meta:
        db_table = 'doctos_ve_det'
        abstract = True

    def __unicode__(self):
        return '%s(%s)' % (self.id, self.documento_pv)

    def save(self, *args, **kwargs):
        if not self.id:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(VentasDocumentoDetalleBase, instance=self)
            self.id = next_id('ID_DOCTOS', using)
        super(VentasDocumentoDetalleBase, self).save(*args, **kwargs)
        return


VentasDocumentoDetalle = dymodels.change.load('VentasDocumentoDetalle', VentasDocumentoDetalleBase, app_label)

class VentasDocumentoLigaBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='DOCTO_VE_LIGA_ID')
    factura = models.ForeignKey('VentasDocumento', db_column='DOCTO_VE_FTE_ID', related_name='factura')
    devolucion = models.ForeignKey('VentasDocumento', db_column='DOCTO_VE_DEST_ID', related_name='devolucion')

    class Meta:
        db_table = 'doctos_ve_ligas'
        abstract = True


VentasDocumentoLiga = dymodels.change.load('VentasDocumentoLiga', VentasDocumentoLigaBase, app_label)

class VentasDocumentoFacturaLibresBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='DOCTO_VE_ID')

    class Meta:
        db_table = 'libres_fac_ve'
        abstract = True

    def __unicode__(self):
        return '%s' % self.id


VentasDocumentoFacturaLibres = dymodels.change.load('VentasDocumentoFacturaLibres', VentasDocumentoFacturaLibresBase, app_label)

class VentasDocumentoFacturaDevLibresBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='DOCTO_VE_ID')

    class Meta:
        db_table = 'libres_devfac_ve'
        abstract = True

    def __unicode__(self):
        return '%s' % self.id


VentasDocumentoFacturaDevLibres = dymodels.change.load('VentasDocumentoFacturaDevLibres', VentasDocumentoFacturaDevLibresBase, app_label)