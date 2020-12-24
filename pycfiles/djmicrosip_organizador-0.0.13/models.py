# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_organizador\djmicrosip_organizador\models.py
# Compiled at: 2015-02-07 15:36:52
from django.db import models
from django_microsip_base.libs.models_base.models import Carpeta, Articulo, Registry, ArticuloPrecio, GrupoLineas, LineaArticulos

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=100)

    class Meta:
        db_table = 'SIC_TAG'
        app_label = 'models_base'

    def __unicode__(self):
        return '%s' % self.tag


class TagArticulo(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.ForeignKey('Tag', blank=True, null=True)
    articulo = models.ForeignKey('Articulo', blank=True)

    class Meta:
        db_table = 'SIC_TAG_ARTICULO'
        app_label = 'models_base'

    def __unicode__(self):
        return '%s' % self.id