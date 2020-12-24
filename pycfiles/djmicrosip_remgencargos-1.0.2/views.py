# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_remgencargos\djmicrosip_remgencargos\views.py
# Compiled at: 2015-02-27 17:35:49
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.db import connections
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *
from microsip_api.comun.sic_db import get_conecctionname
from django.views.generic.list import ListView
from django.db.utils import DatabaseError
import django_filters

class InitialConfiguration(object):

    def __init__(self):
        self.errors = []

    def is_valid(self):
        self.errors = []
        valid = True
        if Registry.objects.get(nombre='INTEG_CC').get_value() == 'S':
            self.errors.append('Es nesesario desabilitar la integracion con cuentas por cobrar en el modulo de ventas. ')
            valid = False
        try:
            concepto = CuentasXCobrarConcepto.objects.get(tipo='V', nombre='Remision')
        except:
            self.errors.append('Por favor genera un concepto en microsip - cuentas por cobrar [ nombre="Remision", tipo="Ventas"]')
            valid = False

        return valid


class VentasDocumentoRemisionesListView(ListView):
    context_object_name = 'documentos'
    model = VentasDocumento
    template_name = 'ventas/documentos/djmicrosip_remgencargos/remisiones.html'
    paginate_by = 20
    initial_configuration = InitialConfiguration()

    def get_queryset(self):
        documentos = []
        if self.initial_configuration.is_valid():
            get_dict = self.request.GET
            form = SearchForm(self.request.GET)
            documentos = VentasDocumento.objects.filter(tipo='R', estado='P').order_by('-id')
            if form.is_valid():
                if 'inicio' in get_dict:
                    if get_dict['inicio']:
                        inicio = datetime.strptime(get_dict['inicio'], '%d/%m/%Y')
                        documentos = documentos.filter(fecha__gte=inicio)
                if 'fin' in get_dict:
                    if get_dict['fin']:
                        fin = datetime.strptime(get_dict['fin'], '%d/%m/%Y')
                        documentos = documentos.filter(fecha__lte=fin)
                if 'cliente' in get_dict:
                    documentos = documentos.filter(cliente__id=get_dict['cliente'])
            documentos = documentos.order_by('-folio')
        return documentos

    def get_context_data(self, **kwargs):
        context = super(VentasDocumentoRemisionesListView, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET or None)
        if not self.initial_configuration.is_valid():
            context['errors'] = self.initial_configuration.errors
        return context


from django.core import serializers
import json
from django.db.models import Q

class generar_cargosbyremisionesview(TemplateView):
    """ Genera un cargo en cuentas por pagar de las remisiones dadas."""

    def get(self, request, *args, **kwargs):
        connection_name = get_conecctionname(request.session)
        errors, remisiones_cargadas = [], []
        ids = request.GET['ids']
        ids = map(int, ids[:len(ids) - 1].split(','))
        documentos = VentasDocumento.objects.filter(pk__in=ids).exclude(descripcion='cargo_generado')
        concepto = CuentasXCobrarConcepto.objects.get(tipo='V', nombre='Remision')
        for documento in documentos:
            descripcion = ''
            if not CuentasXCobrarDocumento.objects.filter(folio=documento.folio, concepto=concepto).exists():
                cxc_documento = CuentasXCobrarDocumento.objects.create(concepto=concepto, folio=documento.folio, fecha=documento.fecha, cliente=documento.cliente, descripcion=descripcion, cliente_clave=documento.cliente_clave, tipo_cambio=documento.tipo_cambio, condicion_pago=documento.condicion_pago, descuentoxprontopago_fecha=documento.descuentoxprontopago_fecha, descuentoxprontopago_porcentaje=documento.descuentoxprontopago_porcentaje, creacion_usuario=request.user.username, modificacion_usuario=request.user.username)
                impuestos_importes = VentasDocumentoImpuesto.objects.filter(documento=documento).values_list('venta_neta', 'impuesto', 'importe', 'porcentaje', 'otros')
                iva_retenido, isr_retenido = (0, 0)
                importe = 0
                for impuesto_importes in impuestos_importes:
                    impuesto = Impuesto.objects.get(pk=impuesto_importes[1])
                    tipo_impuesto = impuesto.tipoImpuesto
                    if tipo_impuesto.tipo == 'I':
                        importe += impuesto_importes[0] + impuesto_importes[4]
                    if tipo_impuesto.tipo == 'R':
                        if tipo_impuesto.id_interno == 'I':
                            iva_retenido += impuesto_importes[2]
                        elif tipo_impuesto.id_interno == 'S':
                            isr_retenido += impuesto_importes[2]

                importe_cxc = CuentasXCobrarDocumentoImportes.objects.create(docto_cc=cxc_documento, doocumento_acr=cxc_documento, importe=importe, total_impuestos=documento.impuestos_total, iva_retenido=iva_retenido, isr_retenido=isr_retenido)
                for impuesto_importes in impuestos_importes:
                    impuesto = Impuesto.objects.get(pk=impuesto_importes[1])
                    tipo_impuesto = impuesto.tipoImpuesto
                    if tipo_impuesto.tipo == 'I' and tipo_impuesto.id_interno == 'V':
                        CuentasXCobrarDocumentoImportesImpuesto.objects.create(id=-1, importe=importe_cxc, importe_venta_neta=impuesto_importes[0] + impuesto_importes[4], impuesto=impuesto, impuesto_importe=impuesto_importes[2], impuesto_porcentaje=impuesto_importes[3])

                plazos = CondicionPagoPlazo.objects.filter(condicion_de_pago=documento.condicion_pago)
                c = connections[connection_name].cursor()
                for plazo in plazos:
                    plazo_fecha = cxc_documento.fecha + timedelta(days=plazo.dias)
                    query = 'INSERT INTO "VENCIMIENTOS_CARGOS_CC" ("DOCTO_CC_ID", "FECHA_VENCIMIENTO", "PCTJE_VEN") VALUES (%s, %s, %s)'
                    c.execute(query, [cxc_documento.id, plazo_fecha, plazo.porcentaje_de_venta])

                c.close()
                cxc_documento.aplicado = 'S'
                cxc_documento.save(update_fields=('aplicado', ))
                remisiones_cargadas.append(documento.id)
                documento.descripcion = 'cargo_generado'
                documento.save(update_fields=('descripcion', ))

        data = {'remisiones_cargadas': remisiones_cargadas, 'errors': errors}
        data = json.dumps(data)
        return HttpResponse(data, mimetype='application/json')