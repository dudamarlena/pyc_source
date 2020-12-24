# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_clasificadores\djmicrosip_clasificadores\models.py
# Compiled at: 2020-04-01 15:34:47
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django_microsip_base.libs.models_base.models import Articulo, Cliente

class ClasificadorAsignacion(models.Model):
    clasificador_padre = models.IntegerField(blank=True, null=True, db_column='CLASIFICADOR_PADRE')
    clasificador_padre_valor = models.IntegerField(blank=True, null=True, db_column='CLASIFICADOR_PADRE_VALOR')
    clasificador_asignado = models.IntegerField(blank=True, null=True, db_column='CLASIFICADOR_ASIGNADO')

    class Meta:
        db_table = 'SIC_CLASIFICADOR_ASIGNACION'
        app_label = 'models_base'


class ArticulosCompatibilidad(models.Model):
    id = models.AutoField(primary_key=True, db_column='ARTICULOS_COMPATIBILIDAD_ID')
    articulo = models.ForeignKey('Articulo', blank=True, null=True, db_column='ARTICULO_ID')
    articulo_compatible = models.IntegerField(blank=True, null=True, db_column='ARTICULO_COMPATIBLE')

    class Meta:
        db_table = 'SIC_ARTICULOS_COMPATIBILIDAD'
        app_label = 'models_base'


class ClienteUsuario(models.Model):
    id = models.AutoField(primary_key=True, db_column='CLIENTE_USUARIO_ID')
    cliente = models.ForeignKey('Cliente', blank=True, null=True, db_column='CLIENTE_ID')
    usuario = models.IntegerField(blank=True, null=True, db_column='USUARIO_ID')

    class Meta:
        db_table = 'SIC_CLIENTE_USUARIO'
        app_label = 'models_base'