# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_microsip_consultaprecio\django_microsip_consultaprecio\models.py
# Compiled at: 2015-11-13 19:01:52
from django.db import models
from django_microsip_base.libs.models_base.models import *

class ImagenSlideChecador(models.Model):
    id = models.AutoField(primary_key=True)
    imagen = models.ImageField(blank=True, null=True, upload_to='control_de_acceso')

    class Meta:
        db_table = 'SIC_CHECADOR_IMAGEN'
        app_label = 'models_base'

    def __unicode__(self):
        return '%s' % self.id