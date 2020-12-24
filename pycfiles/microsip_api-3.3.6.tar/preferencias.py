# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\django-microsip-api\microsip_api\models_base\configuracion\preferencias.py
# Compiled at: 2019-09-09 14:21:50
from django.db import models

class RegistryBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='ELEMENTO_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    tipo = models.CharField(max_length=1, db_column='TIPO')
    padre = models.ForeignKey('self', related_name='padre_a')
    valor = models.CharField(default='', blank=True, null=True, max_length=100, db_column='VALOR')

    class Meta:
        db_table = 'registry'
        abstract = True

    def __unicode__(self):
        return '%s' % self.nombre

    def get_value(self):
        if self.valor == '':
            return None
        else:
            return '%s' % self.valor