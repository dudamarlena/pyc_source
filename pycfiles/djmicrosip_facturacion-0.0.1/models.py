# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_facturacion\djmicrosip_facturacion\models.py
# Compiled at: 2017-09-18 13:09:25
from django.db import models
from django_microsip_base.libs.models_base.models import Cliente, ClienteDireccion, PuntoVentaDocumento, PuntoVentaDocumentoDetalle, PuntoVentaDocumentoLiga, PuntoVentaDocumentoLigaDetalle, Registry
from django.db import connections
from django.core import management

class BookmarkReporteManager(models.Manager):

    def get_by_natural_key(self, reporte_id, objeto_id):
        return self.get(reporte_id=reporte_id, objeto_id=objeto_id)

    def create_manual(self, *args, **kwargs):
        using = kwargs.get('using', None)
        reporte_id = kwargs.get('reporte_id', None)
        objeto_id = kwargs.get('objeto_id', None)
        fecha = kwargs.get('fecha', None)
        c = connections[using].cursor()
        query = 'INSERT INTO BOOKMARKS_REPORTES (reporte_id, objeto_id, fecha) VALUES (%s, %s, %s)'
        c.execute(query, [reporte_id, objeto_id, fecha])
        c.close()
        management.call_command('syncdb', database=using, interactive=False)
        return


class BookmarkReporte(models.Model):
    objects = BookmarkReporteManager()
    reporte_id = models.IntegerField(db_column='reporte_id')
    objeto_id = models.IntegerField(db_column='objeto_id')
    fecha = models.DateField(db_column='fecha')
    orden_seleccion = models.IntegerField(db_column='orden_seleccion')

    class Meta:
        db_table = 'bookmarks_reportes'
        unique_together = (('reporte_id', 'objeto_id'), )
        app_label = 'models_base'

    def __unicode__(self):
        return '%s' % (self.documento_liga, self.detalle_fuente)