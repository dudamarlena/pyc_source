# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_cotizador\djmicrosip_cotizador\models.py
# Compiled at: 2015-02-13 17:45:27
from django.db import models
from django_microsip_base.libs.models_base.models import *

class EstructuraCotizacion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    imagen = models.imagen = models.ImageField(blank=True, null=True, upload_to='estructuras')
    carpeta_base = models.ForeignKey('Carpeta')

    class Meta:
        db_table = 'SIC_ESTRUCTURA_COTIZACION'
        app_label = 'models_base'

    def __unicode__(self):
        return '%s' % self.nombre


class DetalleEstructuraCotizacion(models.Model):
    id = models.AutoField(primary_key=True)
    estructura = models.ForeignKey('EstructuraCotizacion', blank=True, null=True)
    carpeta = models.ForeignKey('Carpeta', blank=True)
    cantidad = models.IntegerField()

    class Meta:
        db_table = 'SIC_ESTRUCTURA_COTIZACION_DET'
        app_label = 'models_base'

    def __unicode__(self):
        return '%s' % self.estructura