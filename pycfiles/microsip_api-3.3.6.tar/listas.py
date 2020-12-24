# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\django-microsip-api\microsip_api\models_base\punto_de_venta\listas.py
# Compiled at: 2019-09-09 14:21:50
from django.db import models
from datetime import datetime

class CajeroBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='CAJERO_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    usuario = models.CharField(max_length=31, db_column='USUARIO')
    operar_cajas = models.CharField(max_length=1, default='T', db_column='OPERAR_CAJAS')

    class Meta:
        db_table = 'cajeros'
        abstract = True

    def __unicode__(self):
        return self.nombre


class CajaBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='CAJA_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    almacen = models.ForeignKey('Almacen', db_column='ALMACEN_ID')
    predeterminado_forma_cobro = models.ForeignKey('FormaCobro', db_column='forma_cobro_predet_id')

    class Meta:
        db_table = 'cajas'
        abstract = True

    def __unicode__(self):
        return self.nombre


class CajaFoliosManager(models.Manager):

    def get_by_natural_key(self, caja, documento_tipo, serie):
        return self.get(caja=caja, documento_tipo=documento_tipo, serie=serie)


class CajaFoliosBase(models.Model):
    DOCUMENTO_TIPOS = (
     ('V', 'Venta de mostrador'), ('O', 'Orden de venta'), ('D', 'Devolucion de ventas'), ('R', 'Retiro de caja'), ('I', 'Ingreso de caja'), ('P', 'Cobro de cuentas por cobrar'))
    objects = CajaFoliosManager()
    caja = models.ForeignKey('Caja', db_column='CAJA_ID')
    documento_tipo = models.CharField(max_length=1, choices=DOCUMENTO_TIPOS, db_column='TIPO_DOCTO')
    serie = models.CharField(max_length=3, db_column='SERIE')
    consecutivo = models.IntegerField(db_column='CONSECUTIVO')

    class Meta:
        db_table = 'FOLIOS_CAJAS'
        unique_together = (('caja', 'documento_tipo', 'serie'), )
        abstract = True

    def __unicode__(self):
        return '%s' % (self.caja, self.documento_tipo, self.serie)


class CajeroCajaManager(models.Manager):

    def get_by_natural_key(self, cajero, caja):
        return self.get(cajero=cajero, caja=caja)


class CajeroCajaBase(models.Model):
    objects = CajeroCajaManager()
    cajero = models.ForeignKey('Cajero', db_column='CAJERO_ID')
    caja = models.ForeignKey('Caja', db_column='CAJA_ID')

    class Meta:
        db_table = 'cajas_cajeros'
        unique_together = (('cajero', 'caja'), )
        abstract = True

    def __unicode__(self):
        return '%s' % (self.cajero, self.caja)


class FormaCobroBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='FORMA_COBRO_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    tipo = models.CharField(max_length=1, default='E', db_column='TIPO')

    class Meta:
        db_table = 'formas_cobro'
        abstract = True

    def __unicode__(self):
        return self.nombre


class FormaCobroReferenciaBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='FORMA_COBRO_REFER_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    forma_cobro = models.ForeignKey('FormaCobro', db_column='FORMA_COBRO_ID')

    class Meta:
        db_table = 'formas_cobro_refer'
        abstract = True

    def __unicode__(self):
        return self.nombre


class CajaMovimientoBase(models.Model):
    MOVIMIENTO_TIPOS = (
     ('A', 'Apertura'), ('C', 'Cierre'))
    CAJEROS_HABILITADOS = (('T', 'Todos los cajeros con derecho a operar la caja'), ('L', 'Los cajeros indicados en la lista'))
    id = models.AutoField(primary_key=True, db_column='movto_caja_id')
    fecha = models.DateField(db_column='fecha')
    hora = models.TimeField(db_column='hora')
    movimiento_tipo = models.CharField(max_length=1, choices=MOVIMIENTO_TIPOS, db_column='tipo_movto')
    caja = models.ForeignKey('Caja', db_column='caja_id')
    cajeros_habilitados = models.CharField(default='T', max_length=1, choices=CAJEROS_HABILITADOS, db_column='cajeros_habilitados')
    forma_emitida = models.CharField(default='N', max_length=1, db_column='forma_emitida')
    usuario_creador = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_creador')
    fechahora_creacion = models.DateTimeField(default=datetime.now, db_column='fecha_hora_creacion')
    usuario_aut_creacion = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_aut_creacion')
    usuario_ult_modif = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_ult_modif')
    fechahora_ult_modif = models.DateTimeField(auto_now=True, db_column='fecha_hora_ult_modif')
    usuario_aut_modif = models.CharField(blank=True, null=True, max_length=31, db_column='usuario_aut_modif')

    class Meta:
        db_table = 'movtos_cajas'
        abstract = True

    def __unicode__(self):
        return '%s' % self.id


class CajaMovimientoFondoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='movto_caja_fondo_id')
    caja_movimiento = models.ForeignKey('CajaMovimiento', db_column='movto_caja_id')
    forma_cobro = models.ForeignKey('FormaCobro', db_column='forma_cobro_id')
    importe = models.DecimalField(default=0, max_digits=15, decimal_places=2, db_column='IMPORTE')

    class Meta:
        db_table = 'movtos_cajas_fondo'
        abstract = True

    def __unicode__(self):
        return '%s' % self.id