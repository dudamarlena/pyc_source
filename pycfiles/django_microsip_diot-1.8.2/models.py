# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_microsip_diot\django_microsip_diot\models.py
# Compiled at: 2015-11-24 14:59:04
from django.db import models
from django_microsip_base.libs.models_base.models import Proveedor, ContabilidadDocumentoDetalle, ContabilidadCuentaContable, ContabilidadDocumento, Pais, ClaveGeneral, Ciudad, Registry, RepositorioCFDI, Estado, Moneda, CondicionPago, CuentasXPagarCondicionPago

class CapturaManual(models.Model):
    id = models.AutoField(primary_key=True)
    folio = models.CharField(max_length=20)
    fecha = models.DateField()
    proveedor = models.ForeignKey('Proveedor', db_column='PROVEEDOR_ID')
    importe = models.DecimalField(max_digits=18, decimal_places=6)
    subtotal = models.DecimalField(max_digits=18, decimal_places=6)
    iva = models.DecimalField(max_digits=18, decimal_places=6)
    iva_no_acreditable = models.DecimalField(max_digits=18, decimal_places=6)
    iva_retenido = models.DecimalField(max_digits=18, decimal_places=6)
    iva_descuentos = models.DecimalField(max_digits=18, decimal_places=6)
    mostrar = models.CharField(default='S', max_length=1)

    class Meta:
        db_table = 'SIC_DIOT_CAPTURAS'
        app_label = 'models_base'

    def __unicode__(self):
        return '%s' % self.folio