# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\django_msp_facturaglobal\django_msp_facturaglobal\views.py
# Compiled at: 2014-12-10 18:43:00
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import csv, json
from django.views.generic.list import ListView, View
from microsip_api.comun.sic_db import first_or_none
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from datetime import datetime
from django.db import connections, transaction, router
from django.core import management
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic.edit import View, FormView

@login_required(login_url='/login/')
def index(request, template_name='django_msp_facturaglobal/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


class ListViewFilterMixin(object):
    """
    Filter a list view by date range.
    """
    form = None

    def get_queryset(self):
        queryset = super(ListViewFilterMixin, self).get_queryset()
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)
        cliente_eventual = Registry.objects.get(nombre='CLIENTE_EVENTUAL_PV_ID').valor
        cliente = Cliente.objects.get(id=cliente_eventual)
        form_initial = {'cliente': cliente}
        form = DateRangeForm(self.request.GET or None, initial=form_initial)
        if form.is_valid() and start_date and end_date:
            cliente_eventual = self.request.GET.get('cliente', None)
            cur_month = datetime.now().month
            cur_year = datetime.now().year
            ventas_sin_facturar = PuntoVentaDocumento.objects.filter(tipo='V', estado='N', cliente__id=cliente_eventual, fecha__gte=start_date, fecha__lte=end_date)
            ventas_facturadas = PuntoVentaDocumentoLiga.objects.filter(docto_pv_fuente__in=ventas_sin_facturar).values_list('docto_pv_fuente', flat=True)
            queryset = ventas_sin_facturar.exclude(pk__in=ventas_facturadas)
        else:
            queryset = PuntoVentaDocumentoLiga.objects.none()
        self.form = form
        return queryset


class VentasPorFacturarList(ListViewFilterMixin, ListView):
    """
        Muestra las ventas que estan pendientes de facturar del cliente generico
    """
    template_name = 'django_msp_facturaglobal/facturas/facturas.html'
    context_object_name = 'ventas'
    model = PuntoVentaDocumento

    def get_context_data(self, **kwargs):
        cliente_eventual = Registry.objects.get(nombre='CLIENTE_EVENTUAL_PV_ID').valor
        cliente = Cliente.objects.get(id=cliente_eventual)
        context = super(VentasPorFacturarList, self).get_context_data(**kwargs)
        context['cliente'] = cliente.nombre
        cur_month = datetime.now().month
        mes = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        cur_year = datetime.now().year
        context['fecha'] = 'Del mes de ' + str(mes[(cur_month - 1)]) + ' de ' + str(cur_year) + ''
        context['microsip_version'] = settings.MICROSIP_VERSION
        context['form'] = self.form
        return context


def generar_factura_global(request):
    """
    Genera el documento de la factura global para posteriormente agregar ventas a esta factura con vitsa "generar_venta_factura"
    """
    error = ''
    factura_id = 0
    reporte_id = 0
    documentos_ids = request.GET.getlist('documentos')
    documentos = PuntoVentaDocumento.objects.filter(id__in=documentos_ids).order_by('fecha')
    if documentos:
        using = router.db_for_write(Articulo)
        modalidad_facturacion = Registry.objects.get(nombre='MODALIDAD_FACTURACION_PV').valor
        fecha_inicio = documentos[0].fecha
        fecha_fin = documentos[(len(documentos) - 1)].fecha
        documento1 = documentos[0]
        cliente = documento1.cliente
        cliente_clave = documento1.clave_cliente
        cliente_direccion = first_or_none(ClienteDireccion.objects.filter(cliente=cliente, es_ppal='N'))
        caja = first_or_none(Caja.objects.all())
        moneda = Moneda.objects.get(pk=1)
        factura_tipo = 'C'
        if cliente_direccion:
            factura = PuntoVentaDocumento(id=-1, caja=caja, clave_cliente=cliente_clave, cliente=cliente, clave_cliente_fac=cliente_clave, cliente_fac=cliente, direccion_cliente=cliente_direccion, moneda=moneda, tipo='F', aplicado='S', fecha=datetime.now(), hora=datetime.now().strftime('%H:%M:%S'), impuesto_incluido='N', tipo_cambio=1, unidad_comprom='N', tipo_descuento='I', tipo_gen_fac='C', es_fac_global='N', porcentaje_descuento=0, importe_descuento=0, importe_neto=0, total_impuestos=0, importe_donativo=0, total_fpgc=0, sistema_origen='PV', usuario_creador=request.user.username, es_cfd='S', modalidad_facturacion=modalidad_facturacion)
            factura.save()
            c = connections[using].cursor()
            c.execute('EXECUTE PROCEDURE GET_REPORTE_ID')
            reporte_id = c.fetchall()[0][0]
            c.close()
            for documento in documentos:
                BookmarkReporte.objects.create_manual(using=using, reporte_id=reporte_id, objeto_id=documento.id, fecha=datetime.now())

            print factura.id
            print reporte_id
            factura_id = factura.id
        else:
            error = 'No se ha encontrado consignatario en el cliente eventual'
    data = {'factura_id': factura_id, 
       'reporte_id': reporte_id, 
       'error': error}
    return HttpResponse(json.dumps(data), mimetype='application/json')


def generar_venta_factura(request):
    """ 
        Genera la factura global dependiendo de el reporte dado
    """
    factura_id = request.GET['factura_id']
    reporte_id = request.GET['reporte_id']
    using = router.db_for_write(Articulo)
    c = connections[using].cursor()
    query = "EXECUTE PROCEDURE COPIA_TICKETS_A_FAC_PV('L',null," + str(factura_id) + ",'C'," + str(reporte_id) + ')'
    c.execute(query)
    c.close()
    management.call_command('syncdb', database=using, interactive=False)
    return HttpResponse(json.dumps(data), mimetype='application/json')