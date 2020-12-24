# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_orden_trabajo\djmicrosip_orden_trabajo\models.py
# Compiled at: 2020-01-13 20:04:32
from django.db import models
from datetime import datetime
from multiselectfield import MultiSelectField
from storage import OverwriteStorage
from django_microsip_base.libs.models_base.models import VentasDocumento, VendedorBase

class Pedidos_Crm(models.Model):
    id = models.AutoField(primary_key=True, db_column='CRM_ID')
    folio = models.CharField(max_length=9, db_column='FOLIO', null=True)
    fecha_registro = models.DateTimeField(db_column='FECHA_HORA_REGISTRO')
    fecha_inicio = models.DateTimeField(null=True, db_column='FECHA_HORA_INICIO')
    PROGRESS_CHOICES = (
     ('0', 'Recibido'),
     ('25', 'Inicio'),
     ('50', 'Finalizado'),
     ('75', 'Aviso cliente'),
     ('100', 'Entregado'))
    progreso = models.CharField(max_length=3, default='0', choices=PROGRESS_CHOICES, db_column='PROGRESO')
    fecha_meta = models.DateTimeField(null=True, db_column='FECHA_META')
    fecha_mod = models.DateTimeField(null=True, db_column='FECHA_MODIFICACION')
    fecha_aviso = models.DateTimeField(null=True, db_column='FECHA_AVISO')
    fecha_fin = models.DateTimeField(null=True, db_column='FECHA_FIN')
    fecha_entrega = models.DateTimeField(null=True, db_column='FECHA_ENTREGA')
    nota = models.TextField(null=True, blank=True, db_column='NOTA')
    bdatos = models.CharField(max_length=250, db_column='BASE_DATOS')
    conexion = models.CharField(max_length=10, db_column='CONEXION')
    HARDWARE_CHOICES = (
     ('CPU', 'CPU'),
     ('LAPTOP', 'LAPTOP'),
     ('CABLE', 'CABLE'),
     ('MONITOR', 'MONITOR'),
     ('IMPRESORA', 'IMPRESORA'),
     ('CARGADOR', 'CARGADOR'),
     ('OTROS', 'OTROS'))
    hardware = MultiSelectField(choices=HARDWARE_CHOICES, db_column='HARDWARE')
    descripcion_otros = models.TextField(null=True, db_column='DESC_OTROS')
    precio_aproximado = models.FloatField(default=0, null=True, blank=True, db_column='PRECIO_APROXIMADO')
    descripcion_general = models.TextField(null=True, db_column='DESC_GENERAL')
    firma = models.ImageField(blank=True, null=True, upload_to='pedidos_crm', db_column='SIC_FIRMA_URL', storage=OverwriteStorage())
    TIPO_SERVICIO_CHOICES = (
     ('PRESENCIAL', 'PRESENCIAL'),
     ('REMOTO', 'REMOTO'))
    tipo_servicio = models.CharField(null=True, max_length=50, default='PRESENCIAL', choices=TIPO_SERVICIO_CHOICES, db_column='TIPO_SERVICIO')
    llamada = models.BooleanField(default=False, db_column='LLAMADA')
    TIPO_LLAMADA_CHOICES = (
     ('PENDIENTE', 'PENDIENTE'),
     ('ATENDIDA', 'ATENDIDA'))
    tipo_llamada = models.CharField(null=True, max_length=50, default='ATENDIDA', choices=TIPO_LLAMADA_CHOICES, db_column='TIPO_LLAMADA')
    envio_correo = models.BooleanField(default=False, db_column='ENVIO_CORREO')
    preprogramado = models.BooleanField(default=False, db_column='PREPROGRAMADO')

    class Meta:
        db_table = 'SIC_PEDIDOS_CRM'
        app_label = 'models_base'

    def image_path(instance, filename):
        return os.path.join('some_dir', str(instance.some_identifier), 'filename.ext')


class Usuario_notificacion(models.Model):
    user_id = models.AutoField(primary_key=True, db_column='USER_ID')
    vendedor = models.ForeignKey('Vendedor', blank=True, null=True, db_column='VENDEDOR_ID')
    id_onesignal = models.CharField(max_length=200, db_column='ID_ONESIGNAL', null=True)
    administrador = models.BooleanField(default=False, db_column='ADMINISTRADOR')
    usuario_microsipd = models.IntegerField(blank=True, null=True, db_column='USUARIO_MICROSIP')

    class Meta:
        db_table = 'SIC_USUARIO_NOTIFICACION'
        app_label = 'models_base'