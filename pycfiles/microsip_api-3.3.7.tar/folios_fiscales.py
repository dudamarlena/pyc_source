# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\django-microsip-api\microsip_api\models_base\configuracion\folios_fiscales.py
# Compiled at: 2019-09-09 14:21:50
from django.db import models
from django.db import router
from microsip_api.comun.sic_db import next_id
from django.conf import settings

class ConfiguracionFolioFiscalBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='FOLIOS_FISCALES_ID')
    serie = models.CharField(max_length=3, db_column='SERIE')
    folio_ini = models.IntegerField(db_column='FOLIO_INI')
    folio_fin = models.IntegerField(db_column='FOLIO_FIN')
    ultimo_utilizado = models.IntegerField(db_column='ULTIMO_UTILIZADO')
    num_aprobacion = models.CharField(max_length=14, db_column='NUM_APROBACION')
    ano_aprobacion = models.IntegerField(db_column='ANO_APROBACION')
    modalidad_facturacion = models.CharField(max_length=10, db_column='MODALIDAD_FACTURACION')
    fecha_aprobacion = models.DateField(db_column='FECHA_APROBACION', blank=True, null=True)
    fecha_vencimiento = models.DateField(db_column='FECHA_VENCIMIENTO', blank=True, null=True)

    class Meta:
        db_table = 'folios_fiscales'
        abstract = True

    def __str__(self):
        return '%s' % self.id

    def save(self, *args, **kwargs):
        if not self.id:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(ConfiguracionFolioFiscalBase, instance=self)
            self.id = next_id('ID_DOCTOS', using)
        super(ConfiguracionFolioFiscalBase, self).save(*args, **kwargs)
        return


class ConfiguracionFolioFiscalUsoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='USO_FOLIO_ID')
    folios_fiscales = models.ForeignKey('ConfiguracionFolioFiscal', db_column='FOLIOS_FISCALES_ID')
    folio = models.IntegerField(db_column='FOLIO')
    fecha = models.DateField(db_column='FECHA')
    sistema = models.CharField(max_length=2, db_column='SISTEMA')
    documento = models.IntegerField(db_column='DOCTO_ID')
    xml = models.TextField(db_column='XML')
    prov_cert = models.CharField(max_length=20, db_column='PROV_CERT')
    fechahora_timbrado = models.CharField(max_length=25, db_column='FECHA_HORA_TIMBRADO')
    uuid = models.CharField(max_length=45, db_column='UUID')
    if settings.MICROSIP_VERSION >= 2016:
        cfdi = models.IntegerField(db_column='CFDI_ID')

    class Meta:
        db_table = 'usos_folios_fiscales'
        abstract = True

    def __str__(self):
        return '%s' % self.id

    def save(self, *args, **kwargs):
        if self.id == -1:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(ConfiguracionFolioFiscalUsoBase, instance=self)
            self.id = next_id('ID_DOCTOS', using)
        super(ConfiguracionFolioFiscalUsoBase, self).save(*args, **kwargs)
        return