# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_msp_controldeacceso\django_msp_controldeacceso\models.py
# Compiled at: 2016-02-15 12:30:53
from django.db import models
from django_microsip_base.libs.models_base.models import Cliente, ClienteClave, Registry

class RegistroAcceso(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.IntegerField()
    acceso = models.CharField(max_length=1)
    fecha = models.DateField()
    hora = models.TimeField()

    class Meta:
        db_table = 'SIC_REGISTRO_ACCESOS'
        app_label = 'models_base'

    def __unicode__(self):
        return '%s' % self.id


class ImagenSlide(models.Model):
    id = models.AutoField(primary_key=True)
    imagen = models.ImageField(blank=True, null=True, upload_to='clientes')

    class Meta:
        db_table = 'SIC_CONTROLDEACCESO_IMAGEN'
        app_label = 'models_base'

    def __unicode__(self):
        return '%s' % self.id