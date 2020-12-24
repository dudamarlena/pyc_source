# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\django-microsip-api\microsip_api\models_base\comun\proveedores.py
# Compiled at: 2019-09-09 14:21:50
from django.db import models

class ProveedorTipoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='TIPO_PROV_ID')
    nombre = models.CharField(max_length=30, db_column='NOMBRE')

    class Meta:
        db_table = 'tipos_prov'
        abstract = True

    def __unicode__(self):
        return '%s' % self.nombre


class ProveedorBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='PROVEEDOR_ID')
    nombre = models.CharField(max_length=100, db_column='NOMBRE')
    cuenta_xpagar = models.CharField(max_length=30, db_column='CUENTA_CXP', blank=True, null=True)
    cuenta_anticipos = models.CharField(max_length=9, db_column='CUENTA_ANTICIPOS', blank=True, null=True)
    moneda = models.ForeignKey('Moneda', db_column='MONEDA_ID')
    tipo = models.ForeignKey('ProveedorTipo', db_column='TIPO_PROV_ID')
    rfc_curp = models.CharField(max_length=18, db_column='RFC_CURP', blank=True, null=True)
    condicion_de_pago = models.ForeignKey('CuentasXPagarCondicionPago', db_column='COND_PAGO_ID')
    pais = models.ForeignKey('Pais', db_column='PAIS_ID', blank=True, null=True)
    estado = models.ForeignKey('Estado', db_column='ESTADO_ID', blank=True, null=True)
    ciudad = models.ForeignKey('Ciudad', db_column='CIUDAD_ID')
    TIPOS_OPERACION = (
     ('03', 'Prestacion de Servicios Profesionales'), ('06', 'Arrendamiento de Inmuebles'), ('85', 'Otros'))
    actividad_principal = models.CharField(max_length=3, choices=TIPOS_OPERACION, db_column='ACTIVIDAD_PRINCIPAL', default='85')
    EXTRANJERO = (
     ('S', 'Si'), ('N', 'No'))
    es_extranjero = models.CharField(max_length=1, choices=EXTRANJERO, db_column='EXTRANJERO', default='N')

    class Meta:
        db_table = 'proveedores'
        abstract = True

    def __unicode__(self):
        return '%s' % self.nombre