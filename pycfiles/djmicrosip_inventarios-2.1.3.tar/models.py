# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_inventarios\djmicrosip_inventarios\models.py
# Compiled at: 2019-09-17 20:13:05
from django.db import models
from django_microsip_base.libs.models_base.models import Articulo, ImpuestosArticulo, ArticuloPrecio, ArticuloClave, ConexionDB, LineaArticulos, InventariosConcepto, InventariosDocumento, InventariosDocumentoDetalle, Almacen, InventariosDocumentoIF, InventariosDocumentoIFDetalle, ArticuloDiscreto, Registry

class LogInventario(models.Model):
    almacen = models.ForeignKey(Almacen)
    apertura_fechahora = models.DateTimeField(auto_now_add=True)
    cierre_fechahora = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'SIC_LOGINVENTARIO'
        app_label = 'models_base'

    def __unicode__(self):
        return '%s' % self.id


class LogInventarioDetalle(models.Model):
    log_inventario = models.ForeignKey(LogInventario)
    articulo = models.ForeignKey(Articulo)
    unidades = models.DecimalField(max_digits=18, decimal_places=5)
    costo_unitario = models.DecimalField(default=0, max_digits=18, decimal_places=5)
    TIPO = (('N', 'Normal'), ('S', 'Serie'), ('L', 'Lote'))
    seguimiento_tipo = models.CharField(default='N', max_length=1, choices=TIPO)
    clave = models.CharField(max_length=20)
    AJUSTADO = (('S', 'Si'), ('N', 'No'))
    serie_ajustada = models.CharField(default='N', max_length=1, choices=AJUSTADO)
    usuario = models.CharField(max_length=20)
    ubicacion = models.CharField(max_length=20)
    fechahora = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'SIC_LOGINVENTARIO_DETALLE'
        app_label = 'models_base'

    def __unicode__(self):
        return '%s' % self.id


class LogInventarioValorInicial(models.Model):
    log_inventario = models.ForeignKey(LogInventario)
    articulo = models.ForeignKey(Articulo)
    existencia = models.DecimalField(max_digits=18, decimal_places=5)
    costo = models.DecimalField(default=0, max_digits=18, decimal_places=5)
    existencia_final = models.DecimalField(blank=True, null=True, max_digits=18, decimal_places=5)

    class Meta:
        db_table = 'SIC_LOGINVENTARIO_VALOR_INICIAL'
        app_label = 'models_base'

    def __unicode__(self):
        return '%s' % self.id