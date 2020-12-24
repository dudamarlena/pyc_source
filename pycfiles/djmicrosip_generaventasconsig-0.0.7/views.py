# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_generaventasconsig\djmicrosip_generaventasconsig\views.py
# Compiled at: 2015-02-17 17:11:05
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import csv
from django.http import HttpResponse
from django.views.generic.list import ListView
from microsip_api.comun.sic_db import first_or_none
from datetime import datetime
from django.http import HttpResponseRedirect
import json
from datetime import datetime
from django.db import router, connections
from decimal import Decimal
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist

def GetPrecioCostoArticulo(articulo, incremento_porcentaje, decimals_round=18):
    precio_con_impuesto = 0
    precio_sin_impto_mn = 0
    costo_ultima_compra = articulo.costo_ultima_compra
    if not costo_ultima_compra:
        costo_ultima_compra = 0
    precio_sin_impto_mn = costo_ultima_compra * (incremento_porcentaje / 100 + 1)
    using = router.db_for_write(Articulo)
    c = connections[using].cursor()
    query = " EXECUTE PROCEDURE PRECIO_CON_IMPTO(%s, %s,'N',0,0, CURRENT_DATE,'P')"
    c.execute(query, [articulo.id, precio_sin_impto_mn])
    precio_con_impuesto = c.fetchall()[0][0]
    c.close()
    return {'con_impuesto': Decimal(round(precio_con_impuesto, decimals_round)), 
       'sin_impuesto': Decimal(round(precio_sin_impto_mn, decimals_round))}


@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_generaventasconsig/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def preferencias(request, template_name='djmicrosip_generaventasconsig/preferencias.html'):
    initial = {'busqueda_fecha_inicio': Registry.objects.get(nombre='SIC_generaVentasConsig_fechaInicio').get_value(), 
       'busqueda_database': Registry.objects.get(nombre='SIC_generaVentasConsig_empresa').get_value(), 
       'ventas_cliente': Registry.objects.get(nombre='SIC_generaVentasConsig_cliente').get_value(), 
       'ventas_cajero': Registry.objects.get(nombre='SIC_generaVentasConsig_cajero').get_value(), 
       'ventas_caja': Registry.objects.get(nombre='SIC_generaVentasConsig_caja').get_value(), 
       'ventas_vendedor': Registry.objects.get(nombre='SIC_generaVentasConsig_vendedor').get_value(), 
       'incremento_precio': Registry.objects.get(nombre='SIC_generaVentasConsig_incrementoPrecio').get_value()}
    form = PreferenciasManageForm(request.POST or None, initial=initial)
    if form.is_valid():
        form.save()
    c = {'form': form}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def PrepararAplicacion(request):
    """ Prepara aplicacion para su uso. """
    if request.user.is_superuser:
        padre = first_or_none(Registry.objects.filter(nombre='PreferenciasEmpresa'))
        if not Registry.objects.filter(nombre='SIC_generaVentasConsig_fechaInicio').exists():
            Registry.objects.create(nombre='SIC_generaVentasConsig_fechaInicio', tipo='V', padre=padre, valor=datetime.now())
        if not Registry.objects.filter(nombre='SIC_generaVentasConsig_empresa').exists():
            Registry.objects.create(nombre='SIC_generaVentasConsig_empresa', tipo='V', padre=padre, valor='')
        if not Registry.objects.filter(nombre='SIC_generaVentasConsig_cliente').exists():
            Registry.objects.create(nombre='SIC_generaVentasConsig_cliente', tipo='V', padre=padre, valor='')
        if not Registry.objects.filter(nombre='SIC_generaVentasConsig_cajero').exists():
            Registry.objects.create(nombre='SIC_generaVentasConsig_cajero', tipo='V', padre=padre, valor='')
        if not Registry.objects.filter(nombre='SIC_generaVentasConsig_caja').exists():
            Registry.objects.create(nombre='SIC_generaVentasConsig_caja', tipo='V', padre=padre, valor='')
        if not Registry.objects.filter(nombre='SIC_generaVentasConsig_vendedor').exists():
            Registry.objects.create(nombre='SIC_generaVentasConsig_vendedor', tipo='V', padre=padre, valor='')
        if not Registry.objects.filter(nombre='SIC_generaVentasConsig_incrementoPrecio').exists():
            Registry.objects.create(nombre='SIC_generaVentasConsig_incrementoPrecio', tipo='V', padre=padre, valor='')
    return HttpResponseRedirect('/generaventasconsig/')


class InitialConfiguration(object):

    def __init__(self):
        self.errors = []

    def is_valid(self):
        self.errors = []
        valid = True
        try:
            Registry.objects.get(nombre='SIC_generaVentasConsig_incrementoPrecio').get_value()
        except ObjectDoesNotExist:
            self.errors.append('Por favor inicializa la configuracion de la aplicacion en herramientas > preparar_aplicacion ')

        if not self.errors:
            caja_id = Registry.objects.get(nombre='SIC_generaVentasConsig_caja').get_value()
            caja = Caja.objects.get(pk=caja_id)
            apertura_ultima = first_or_none(CajaMovimiento.objects.filter(caja=caja, movimiento_tipo='A').order_by('-fecha', '-hora'))
            cierre = None
            if apertura_ultima:
                cierre = first_or_none(CajaMovimiento.objects.filter(caja=caja, movimiento_tipo='C', fecha__gte=apertura_ultima.fecha, hora__gt=apertura_ultima.hora.strftime('%H:%M:%S')))
            if not apertura_ultima or cierre:
                self.errors.append('la caja %s no esta abierta por favor abrela para continuar.' % caja.nombre)
        if not self.errors == []:
            valid = False
        return valid


@login_required(login_url='/login/')
def generar_ventas(request, template_name='djmicrosip_generaventasconsig/generar_ventas.html'):
    initial_configuration = InitialConfiguration()
    initial_configuration.is_valid()
    errors = initial_configuration.errors
    if not errors:
        fecha_inicio_str = Registry.objects.get(nombre='SIC_generaVentasConsig_fechaInicio').valor
        empresa = Registry.objects.get(nombre='SIC_generaVentasConsig_empresa').get_value()
        cliente = Cliente.objects.get(pk=Registry.objects.get(nombre='SIC_generaVentasConsig_cliente').valor)
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        documentos = PuntoVentaDocumento.objects.using(empresa).exclude(descripcion__contains='SIC_VENTA_TRASPASADA').filter(tipo='F', estado='N', fecha__gte=fecha_inicio).order_by('-fecha')
        context = {'documentos': documentos, 
           'empresa': empresa.split('-')[1], 
           'cliente': cliente, 
           'fecha_inicio': fecha_inicio_str}
    else:
        context = {'errors': errors}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def GenerarVentasSeleccionadas(request):
    """ Para traspasar las facturas a la otra empresa como ventas
    """
    documentos_ids = request.GET.getlist('documentos_ids')[0].split(',')
    documentos_ids = tuple(map(lambda x: int(x), documentos_ids))
    documentos_ids_str = str(documentos_ids)
    if len(documentos_ids) == 1:
        documentos_ids_str = '(%s)' % documentos_ids[0]
    initial_configuration = InitialConfiguration()
    errors = []
    msg = ''
    if initial_configuration.is_valid():
        empresa = Registry.objects.get(nombre='SIC_generaVentasConsig_empresa').get_value()
        empresa_nombre = empresa.split('-')[1]
        c = connections[empresa].cursor()
        query = 'select sum(unidades), a.nombre from doctos_pv_det dd inner join articulos a on dd.articulo_id = a.articulo_id where docto_pv_id in %s group by a.nombre' % documentos_ids_str
        c.execute(query)
        articulos = c.fetchall()
        c.close()
        articulos_list = []
        incremento_precio = Decimal(Registry.objects.get(nombre='SIC_generaVentasConsig_incrementoPrecio').valor)
        folios = PuntoVentaDocumento.objects.using(empresa).filter(id__in=documentos_ids).values_list('folio', flat=True)
        folios = (',').join(folios)
        for articulo in articulos:
            articulo_unidades = articulo[0]
            articulo_nombre = articulo[1]
            articulo = first_or_none(Articulo.objects.filter(nombre=articulo_nombre))
            decimals_round = 2
            if articulo:
                precio = GetPrecioCostoArticulo(articulo, incremento_precio, decimals_round)
                if articulo.seguimiento == 'N':
                    articulos_list.append((articulo.id, articulo_unidades, precio))
                else:
                    errors.append(('Seguimiento de articulo no soportado', articulo.nombre))
            else:
                errors.append(('Articulo no encontrado', articulo_nombre, '\n'))

        if not errors:
            moneda = Moneda.objects.get(es_moneda_local='S')
            cliente_id = Registry.objects.get(nombre='SIC_generaVentasConsig_cliente').get_value()
            cliente = Cliente.objects.get(pk=cliente_id)
            cliente_clave = first_or_none(ClienteClave.objects.filter(cliente=cliente))
            caja_id = Registry.objects.get(nombre='SIC_generaVentasConsig_caja').get_value()
            caja = Caja.objects.get(pk=caja_id)
            almacen = caja.almacen
            cajero_id = Registry.objects.get(nombre='SIC_generaVentasConsig_cajero').get_value()
            cajero = Cajero.objects.get(pk=cajero_id)
            ventas_vendedor_id = Registry.objects.get(nombre='SIC_generaVentasConsig_vendedor').get_value()
            vendedor = Vendedor.objects.get(pk=ventas_vendedor_id)
            documento = PuntoVentaDocumento(id=-1, caja=caja, cajero=cajero, cliente=cliente, clave_cliente=cliente_clave, vendedor=vendedor, descripcion=('Venta(as) = ' + folios + ' de ' + empresa_nombre)[0:200], almacen=almacen, moneda=moneda, tipo='V', tipo_cambio=1, aplicado='N', fecha=datetime.now(), hora=datetime.now().strftime('%H:%M:%S'), importe_neto=0, total_impuestos=0, importe_donativo=0, total_fpgc=0, sistema_origen='PV', usuario_creador=request.user.username, tipo_gen_fac=None, fecha_envio=datetime.now())
            documento.save()
            importe_total = 0
            for articulo_list in articulos_list:
                articulo_id = articulo_list[0]
                articulo_unidades = articulo_list[1]
                articulo_precio = articulo_list[2]
                articulo = Articulo.objects.get(pk=articulo_id)
                precio_total_neto = articulo_precio['con_impuesto'] * articulo_unidades
                articulo_clave = first_or_none(ArticuloClave.objects.filter(rol__es_ppal='S', articulo=articulo))
                detalle = PuntoVentaDocumentoDetalle.objects.create(id=-1, documento_pv=documento, clave_articulo=articulo_clave, articulo=articulo, unidades=articulo_unidades, unidades_dev=0, precio_unitario=articulo_precio['sin_impuesto'], precio_unitario_impto=articulo_precio['con_impuesto'], fpgc_unitario=0, porcentaje_descuento=0, precio_total_neto=precio_total_neto, porcentaje_comis=0, rol='N', posicion=-1)
                importe_total += detalle.precio_total_neto

            PuntoVentaCobro.objects.create(id=-1, tipo='C', documento_pv=documento, forma_cobro=caja.predeterminado_forma_cobro, importe=importe_total, tipo_cambio=1, importe_mon_doc=importe_total)
            documento.importe_neto = importe_total
            documento.aplicado = 'S'
            documento.save(update_fields=['importe_neto', 'aplicado'])
            msg = 'Venta Generada Correctamente (' + documento.folio + ')'
            documentos_empresa_orig = PuntoVentaDocumento.objects.using(empresa).filter(id__in=documentos_ids).update(descripcion='%s SIC_VENTA_TRASPASADA' % F('descripcion'))
    else:
        errors = initial_configuration.errors
    datos = {'msg': msg, 
       'documentos_ids': documentos_ids, 
       'errors': errors}
    data = json.dumps(datos)
    return HttpResponse(data, mimetype='application/json')