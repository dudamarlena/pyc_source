# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\django-microsip-api\microsip_api\models_base\inventarios\otros.py
# Compiled at: 2019-09-09 14:21:50
from django.db import models

class InventariosDesgloseEnDiscretosBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='DESGLOSE_DISCRETO_ID')
    docto_in_det = models.ForeignKey('InventariosDocumentoDetalle', db_column='DOCTO_IN_DET_ID')
    art_discreto = models.ForeignKey('ArticuloDiscreto', db_column='ART_DISCRETO_ID')
    unidades = models.IntegerField(default=0, blank=True, null=True, db_column='UNIDADES')

    class Meta:
        db_table = 'desglose_en_discretos'
        abstract = True

    def __unicode__(self):
        return '%s' % self.id


class InventariosDesgloseEnDiscretosIFBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='DESGL_DISCRETO_INVFIS_ID')
    docto_invfis_det = models.ForeignKey('InventariosDocumentoIFDetalle', db_column='DOCTO_INVFIS_DET_ID')
    art_discreto = models.ForeignKey('ArticuloDiscreto', db_column='ART_DISCRETO_ID')
    unidades = models.IntegerField(default=0, blank=True, null=True, db_column='UNIDADES')

    class Meta:
        db_table = 'desglose_en_discretos_invfis'
        abstract = True

    def __unicode__(self):
        return '%s' % self.id