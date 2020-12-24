# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Jesus\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_faexist\djmicrosip_faexist\views.py
# Compiled at: 2015-02-05 13:24:38
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import PuntoVentaDocumentoForm, PreferenciasManageForm, ArticuloSearchForm
import csv
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.db import router, connections
from datetime import datetime
from microsip_api.comun.sic_db import first_or_none
from django.db.models import Q
import json
from datetime import datetime
from django.core import management
from django.http import HttpResponseRedirect
from procedures import procedures as procedures_sic
from decimal import Decimal

class ArticuloListView(ListView):
    context_object_name = 'articulos'
    model = Articulo
    template_name = 'djmicrosip_faexist/articulos/articulos.html'
    paginate_by = 50

    def dispatch(self, *args, **kwargs):
        return super(ArticuloListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        documentos = []
        get_dict = self.request.GET
        form = ArticuloSearchForm(self.request.GET)
        articulos = Articulo.objects.all()
        if form.is_valid():
            articulo = form.cleaned_data['articulo']
            nombre = form.cleaned_data['nombre']
            clave = form.cleaned_data['clave']
            linea = form.cleaned_data['linea']
            mostrar_articulos = form.cleaned_data['mostrar_articulos']
            if mostrar_articulos == 'I':
                articulos = articulos.filter(facturaexistencia_ignorar=True)
            elif mostrar_articulos == 'SI':
                articulos = articulos.filter(Q(facturaexistencia_ignorar=False) | Q(facturaexistencia_ignorar=None))
            if nombre:
                articulos = articulos.filter(nombre__contains=nombre)
            if clave:
                claves = ArticuloClave.objects.filter(clave=clave)
                if claves:
                    articulos = Articulo.objects.filter(pk=claves[0].articulo.id)
            if articulo:
                articulos = Articulo.objects.filter(pk=articulo.id)
            if linea:
                articulos = articulos.filter(linea=linea)
        return articulos

    def get_context_data(self, **kwargs):
        context = super(ArticuloListView, self).get_context_data(**kwargs)
        context['form'] = ArticuloSearchForm(self.request.GET or None)
        return context


def GetPrecioVentaArticulo(articulo):
    precio_con_impuesto = 0
    precio_sin_impto_mn = 0
    try:
        articuloprecio = ArticuloPrecio.objects.get(articulo__id=articulo.id, precio_empresa__id=42)
    except Exception as e:
        moneda = Moneda.objects.get(es_moneda_local='S')
        precio = 0
        tipo_cambio = 1
    else:
        precio = articuloprecio.precio
        moneda = articuloprecio.moneda
        if not moneda.es_moneda_local == 'S':
            tipo_cambio = first_or_none(TipoCambio.objects.filter(moneda=moneda).order_by('-fecha'))
            if tipo_cambio:
                tipo_cambio = tipo_cambio.tipo_cambio
            else:
                tipo_cambio = 1
        else:
            tipo_cambio = 1
        precio_sin_impto_mn = precio * tipo_cambio
        using = router.db_for_write(Articulo)
        c = connections[using].cursor()
        query = " EXECUTE PROCEDURE PRECIO_CON_IMPTO(%s, %s,'N',0,0, CURRENT_DATE,'P')"
        c.execute(query, [articulo.id, precio_sin_impto_mn])
        precio_con_impuesto = c.fetchall()[0][0]
        c.close()

    return {'con_impuesto': precio_con_impuesto, 
       'sin_impuesto': precio_sin_impto_mn}


def GetPrecioCostoArticulo(articulo, incremento_porcentaje):
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
    return {'con_impuesto': precio_con_impuesto, 
       'sin_impuesto': precio_sin_impto_mn}


def GetSeriesArticulo(articulo):
    """
    Obtiene los numero de serie con existencia de un articulo dado.
    """
    series = []
    if articulo.seguimiento == 'S':
        series = ArticuloDiscretoExistencia.objects.filter(articulo_discreto__articulo=articulo, existencia__gt=0, articulo_discreto__tipo='S').values_list('articulo_discreto__clave', flat=True)
    return series


@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_faexist/index.html'):
    moneda = Moneda.objects.get(es_moneda_local='S')
    form = PuntoVentaDocumentoForm(request.POST or None)
    existencias_list = []
    errors = []
    messages = []
    using = router.db_for_write(Articulo)
    initial_configuration = InitialConfiguration(using)
    c = {}
    if initial_configuration.is_valid():
        if form.is_valid():
            cleaned_data = form.cleaned_data
            linea = cleaned_data['linea']
            cliente = cleaned_data['cliente']
            cliente_clave = first_or_none(ClienteClave.objects.filter(cliente=cliente))
            cliente_direccion = first_or_none(ClienteDireccion.objects.filter(cliente=cliente, es_ppal='N'))
            caja_id = Registry.objects.get(nombre='SIC_factExist_ventasCaja').get_value()
            caja = Caja.objects.get(pk=caja_id)
            almacen = caja.almacen
            cajero_id = Registry.objects.get(nombre='SIC_factExist_ventasCajero').get_value()
            cajero = Cajero.objects.get(pk=cajero_id)
            ventas_vendedor_id = Registry.objects.get(nombre='SIC_factExist_ventasVendedor').get_value()
            vendedor = Vendedor.objects.get(pk=ventas_vendedor_id)
            articulos_ids = Articulo.objects.filter(linea=linea, es_almacenable='S').values_list('id', flat=True)
            errors = []
            for id in articulos_ids:
                articulo = Articulo.objects.get(pk=id)
                if articulo.facturaexistencia_ignorar != True:
                    existencia = articulo.get_existencia(almacen_nombre=almacen.nombre)
                    incremento_porcentaje = Decimal(Registry.objects.get(nombre='SIC_factExist_margenPrecioCosto').get_value() or '0')
                    precio = GetPrecioCostoArticulo(articulo=articulo, incremento_porcentaje=incremento_porcentaje)
                    if existencia > 0:
                        articulos_discretos = []
                        if articulo.seguimiento == 'S':
                            articulos_discretos = ArticuloDiscretoExistencia.objects.filter(articulo_discreto__articulo=articulo, existencia__gt=0, articulo_discreto__tipo='S').values_list('articulo_discreto', flat=True)
                            if existencia == len(articulos_discretos):
                                existencias_list.append((id, existencia, precio, articulos_discretos))
                            else:
                                errors.append('series incorrectas', articulo.nombre)
                        else:
                            existencias_list.append((id, existencia, precio))

            if not errors and existencias_list:
                documento = PuntoVentaDocumento(id=-1, caja=caja, cajero=cajero, cliente=cliente, clave_cliente=cliente_clave, vendedor=vendedor, almacen=almacen, moneda=moneda, tipo='V', tipo_cambio=1, aplicado='N', fecha=datetime.now(), hora=datetime.now().strftime('%H:%M:%S'), importe_neto=0, total_impuestos=0, importe_donativo=0, total_fpgc=0, sistema_origen='PV', descripcion='VENTA DE LINEA %s, SIC_GENERA_COMPRA' % linea.nombre, usuario_creador=request.user.username, tipo_gen_fac=None, fecha_envio=datetime.now())
                documento.save()
                messages.append('Venta Generada Correctamente')
                importe_total = 0
                for articulo_list in existencias_list:
                    articulo_id = articulo_list[0]
                    articulo_existencia = articulo_list[1]
                    articulo_precio = articulo_list[2]
                    articulo = Articulo.objects.get(pk=articulo_id)
                    precio_total_neto = articulo_precio['con_impuesto'] * articulo_existencia
                    articulo_clave = first_or_none(ArticuloClave.objects.filter(rol__es_ppal='S', articulo=articulo))
                    detalle = PuntoVentaDocumentoDetalle.objects.create(id=-1, documento_pv=documento, clave_articulo=articulo_clave, articulo=articulo, unidades=articulo_existencia, unidades_dev=0, precio_unitario=articulo_precio['sin_impuesto'], precio_unitario_impto=articulo_precio['con_impuesto'], fpgc_unitario=0, porcentaje_descuento=0, precio_total_neto=precio_total_neto, porcentaje_comis=0, rol='N', posicion=-1)
                    if articulo.seguimiento == 'S':
                        articulos_discretos = articulo_list[3]
                        for articulo_discreto_id in articulos_discretos:
                            articulo_discreto = ArticuloDiscreto.objects.get(pk=articulo_discreto_id)
                            PuntoVentaArticuloDiscreto.objects.create(id=-1, detalle=detalle, articulo_discreto=articulo_discreto)

                    importe_total += precio_total_neto

                PuntoVentaCobro.objects.create(id=-1, tipo='C', documento_pv=documento, forma_cobro=caja.predeterminado_forma_cobro, importe=importe_total, tipo_cambio=1, importe_mon_doc=importe_total)
                documento.importe_neto = importe_total
                documento.aplicado = 'S'
                documento.save(update_fields=['importe_neto', 'aplicado'])
            if not existencias_list and request.POST:
                errors.append(('No hay articulos por vender de la linea indicada',
                               ''))
        c = {'form': form, 'errors': errors, 
           'messages': messages}
    else:
        c['errors'] = initial_configuration.errors
    return render_to_response(template_name, c, context_instance=RequestContext(request))


class InitialConfiguration(object):

    def __init__(self, using):
        self.errors = []
        self.using = using

    def is_valid(self):
        self.errors = []
        valid = True
        try:
            Registry.objects.get(nombre='SIC_facExist_fechaInicio').get_value()
        except ObjectDoesNotExist:
            self.errors.append('Por favor inicializa la configuracion de la aplicacion dando  <a href="/djmicrosip_faexist/preferencias/actualizar_tablas/">click aqui</a>')

        if not self.errors == []:
            valid = False
        return valid


@login_required(login_url='/login/')
def exporta_factura(request, template_name='djmicrosip_faexist/exporta_factura.html'):
    periodo_fecha_inicio = Registry.objects.get(nombre='SIC_facExist_fechaInicio').get_value()
    periodo_fecha_inicio = datetime.strptime(periodo_fecha_inicio, '%d/%m/%Y')
    cliente = Registry.objects.get(nombre='SIC_factExist_cliente').get_value()
    cliente = Cliente.objects.get(pk=cliente)
    database = Registry.objects.get(nombre='SIC_facExist_EmpresaCompras').get_value()
    proveedor_id = Registry.objects.get(nombre='SIC_facExist_ProveedorCompras').get_value()
    proveedor = Proveedor.objects.using(database).get(pk=proveedor_id)
    database_name = database.split('-')[1]
    documentos = PuntoVentaDocumento.objects.exclude(Q(descripcion__contains='FACTURA EXPORTADA')).filter(tipo='F', estado='N', cliente=cliente, fecha__gte=periodo_fecha_inicio).order_by('-fecha')
    c = {'documentos': documentos, 
       'database': database_name, 
       'cliente': cliente, 
       'proveedor': proveedor}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def preferencias(request, template_name='djmicrosip_faexist/preferencias.html'):
    initial = {'periodo_fecha_inicio': Registry.objects.get(nombre='SIC_facExist_fechaInicio').get_value(), 
       'cliente': Registry.objects.get(nombre='SIC_factExist_cliente').get_value(), 
       'database': Registry.objects.get(nombre='SIC_facExist_EmpresaCompras').get_value(), 
       'proveedor': Registry.objects.get(nombre='SIC_facExist_ProveedorCompras').get_value(), 
       'almacen': Registry.objects.get(nombre='SIC_facExist_almacenCompras').get_value(), 
       'ventas_caja': Registry.objects.get(nombre='SIC_factExist_ventasCaja').get_value(), 
       'ventas_cajero': Registry.objects.get(nombre='SIC_factExist_ventasCajero').get_value(), 
       'ventas_vendedor': Registry.objects.get(nombre='SIC_factExist_ventasVendedor').get_value(), 
       'margen_precio_lista': Registry.objects.get(nombre='SIC_factExist_margenPrecioLista').get_value(), 
       'margen_precio_costo': Registry.objects.get(nombre='SIC_factExist_margenPrecioCosto').get_value()}
    form = PreferenciasManageForm(request.POST or None, initial=initial)
    c = {'form': form}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


def GetProveedoresByEmpresa(request):
    """ Para obterner existencia de un articulo segun id del articulo """
    empresa_conexion = request.GET['empresa_conexion']
    proveedores = Proveedor.objects.using(empresa_conexion).all().order_by('nombre').values('id', 'nombre')
    datos = {'proveedores': list(proveedores)}
    data = json.dumps(datos)
    return HttpResponse(data, mimetype='application/json')


def GetAlmacenesByEmpresa(request):
    """ Para obterner existencia de un articulo segun id del articulo """
    empresa_conexion = request.GET['empresa_conexion']
    almacenes = Almacen.objects.using(empresa_conexion).all().order_by('nombre').values('ALMACEN_ID', 'nombre')
    datos = {'almacenes': list(almacenes)}
    data = json.dumps(datos)
    return HttpResponse(data, mimetype='application/json')


def GuardarPreferencias(request):
    """ Para obterner existencia de un articulo segun id del articulo """
    using = router.db_for_write(Articulo)
    busqueda_fecha_inicio = request.GET['busqueda_fecha_inicio']
    busqueda_facturas_cliente_id = request.GET['busqueda_cliente_facturas_id']
    compras_empresa_id = request.GET['compras_empresa_id']
    compras_proveedor_id = request.GET['compras_proveedor_id']
    compras_almacen_id = request.GET['compras_almacen_id']
    ventas_caja = request.GET['ventas_caja']
    ventas_cajero = request.GET['ventas_cajero']
    ventas_vendedor = request.GET['ventas_vendedor']
    margen_precio_lista = request.GET['margen_precio_lista']
    margen_precio_costo = request.GET['margen_precio_costo']
    registry = Registry.objects.get(nombre='SIC_facExist_fechaInicio')
    registry.valor = busqueda_fecha_inicio
    registry.save(update_fields=('valor', ))
    registry = Registry.objects.get(nombre='SIC_factExist_cliente')
    registry.valor = busqueda_facturas_cliente_id
    registry.save(update_fields=('valor', ))
    registry = Registry.objects.get(nombre='SIC_facExist_EmpresaCompras')
    registry.valor = compras_empresa_id
    registry.save(update_fields=('valor', ))
    registry = Registry.objects.get(nombre='SIC_facExist_ProveedorCompras')
    registry.valor = compras_proveedor_id
    registry.save(update_fields=('valor', ))
    registry = Registry.objects.get(nombre='SIC_facExist_almacenCompras')
    registry.valor = compras_almacen_id
    registry.save(update_fields=('valor', ))
    registry = Registry.objects.get(nombre='SIC_factExist_ventasCaja')
    registry.valor = ventas_caja
    registry.save(update_fields=('valor', ))
    registry = Registry.objects.get(nombre='SIC_factExist_ventasCajero')
    registry.valor = ventas_cajero
    registry.save(update_fields=('valor', ))
    registry = Registry.objects.get(nombre='SIC_factExist_ventasVendedor')
    registry.valor = ventas_vendedor
    registry.save(update_fields=('valor', ))
    registry = Registry.objects.get(nombre='SIC_factExist_margenPrecioLista')
    registry.valor = margen_precio_lista
    registry.save(update_fields=('valor', ))
    registry = Registry.objects.get(nombre='SIC_factExist_margenPrecioCosto')
    registry.valor = margen_precio_costo
    registry.save(update_fields=('valor', ))
    datos = {'msg': 'datos guardados'}
    data = json.dumps(datos)
    return HttpResponse(data, mimetype='application/json')


def GenerarCompras(request):
    """ Para obterner existencia de un articulo segun id del articulo 
        Pendiente checar 
        * fletes
        * otros_cargos
        * total_retenciones
        * gastos_aduanales
        * otros_gastos

    """
    documentos_ids = request.GET.getlist('documentos_ids')
    proveedor_id = Registry.objects.get(nombre='SIC_facExist_ProveedorCompras').get_value()
    empresa = Registry.objects.get(nombre='SIC_facExist_EmpresaCompras').get_value()
    proveedor = Proveedor.objects.using(empresa).get(pk=proveedor_id)
    almacen_id = Registry.objects.get(nombre='SIC_facExist_almacenCompras').get_value()
    margen_precio_lista = Decimal(Registry.objects.get(nombre='SIC_factExist_margenPrecioLista').get_value())
    almacen = Almacen.objects.using(empresa).get(ALMACEN_ID=almacen_id)
    errors = []
    c = connections[empresa].cursor()
    query = 'SELECT cond_pago_Id FROM PROVEEDORES WHERE proveedor_id = %s' % proveedor.id
    c.execute(query)
    condicion_pago_id = c.fetchall()[0][0]
    c.close()
    condicion_pago = CuentasXPagarCondicionPago.objects.using(empresa).get(id=condicion_pago_id)
    compras_documentos = []
    msg = ''
    for documento_id in documentos_ids:
        factura = PuntoVentaDocumento.objects.get(pk=documento_id)
        factura_detalles = PuntoVentaDocumentoDetalle.objects.filter(documento_pv=factura)
        articulos_no_existen = []
        for detalle in factura_detalles:
            if not Articulo.objects.using(empresa).filter(nombre=detalle.articulo.nombre).exists():
                articulos_no_existen.append(detalle.articulo.nombre)

        if articulos_no_existen == []:
            compras_documento = ComprasDocumento.objects.using(empresa).create(tipo='C', subtipo='N', proveedor_clave='', proveedor=proveedor, proveedor_folio=factura.folio, almacen=almacen, moneda=proveedor.moneda, tipo_cambio=factura.tipo_cambio, aplicado='N', importe_neto=factura.importe_neto, total_impuestos=factura.total_impuestos, total_fpgc=factura.total_fpgc, sistema_origen='CM', condicion_pago=condicion_pago, cargar_sun=factura.cargar_sun, usuario_creador='SYSDBA')
            c = connections[empresa].cursor()
            query = 'INSERT INTO vencimientos_cargos_cm (docto_cm_id, fecha_vencimiento, pctje_ven)                 VALUES (%s, CURRENT_DATE, 100)'
            c.execute(query, [compras_documento.id])
            c.close()
            management.call_command('syncdb', database=empresa, interactive=False)
            for factura_detalle in factura_detalles:
                compra_articulo = Articulo.objects.using(empresa).get(nombre=factura_detalle.articulo.nombre)
                compra_articulo_clave = first_or_none(ArticuloClave.objects.using(empresa).filter(articulo=compra_articulo))
                if compra_articulo_clave:
                    compra_articulo_clave = compra_articulo_clave.clave
                else:
                    compra_articulo_clave = ''
                ComprasDocumentoDetalle.objects.using(empresa).create(documento=compras_documento, clave_articulo=compra_articulo_clave, articulo=compra_articulo, unidades=factura_detalle.unidades, precio_unitario=factura_detalle.precio_unitario, fpgc_unitario=factura_detalle.fpgc_unitario, porcentaje_descuento=factura_detalle.porcentaje_descuento, precio_total_neto=factura_detalle.precio_total_neto, notas=factura_detalle.notas, posicion=factura_detalle.posicion)
                compra_articuloprecio = first_or_none(ArticuloPrecio.objects.using(empresa).filter(articulo__id=compra_articulo.id, precio_empresa__id=42))
                if compra_articuloprecio:
                    compra_articuloprecio.margen = margen_precio_lista
                    compra_articuloprecio.precio = factura_detalle.precio_unitario * (margen_precio_lista / 100 + 1)
                    compra_articuloprecio.save(using=empresa, update_fields=('margen',
                                                                             'precio'))

            compras_documentos.append(compras_documento.id)
            c = connections[empresa].cursor()
            query = "update DOCTOS_CM set aplicado='S' WHERE docto_cm_id = %s"
            c.execute(query, [compras_documento.id])
            c.close()
            factura.descripcion += 'FACTURA EXPORTADA'
            factura.save(update_fields=('descripcion', ))
            msg = 'Compras generadas correctamente'
        else:
            msg = 'Error en documento(s) No se encontaron articulos'
            errors = articulos_no_existen

    management.call_command('syncdb', database=empresa, interactive=False)
    datos = {'compras_documentos': compras_documentos, 
       'msg': msg, 
       'errors': errors}
    data = json.dumps(datos)
    return HttpResponse(data, mimetype='application/json')


@login_required(login_url='/login/')
def UpdateDatabaseTable(request):
    """ Agrega campos nuevos en tablas de base de datos. """
    if request.user.is_superuser:
        using = router.db_for_write(Articulo)
        padre = first_or_none(Registry.objects.filter(nombre='PreferenciasEmpresa'))
        if not Registry.objects.filter(nombre='SIC_facExist_fechaInicio').exists():
            Registry.objects.create(nombre='SIC_facExist_fechaInicio', tipo='V', padre=padre, valor=datetime.now())
        if not Registry.objects.filter(nombre='SIC_facExist_EmpresaCompras').exists():
            Registry.objects.create(nombre='SIC_facExist_EmpresaCompras', tipo='V', padre=padre)
        if not Registry.objects.filter(nombre='SIC_facExist_almacenCompras').exists():
            Registry.objects.create(nombre='SIC_facExist_almacenCompras', tipo='V', padre=padre)
        if not Registry.objects.filter(nombre='SIC_facExist_ProveedorCompras').exists():
            Registry.objects.create(nombre='SIC_facExist_ProveedorCompras', tipo='V', padre=padre)
        if not Registry.objects.filter(nombre='SIC_factExist_cliente').exists():
            Registry.objects.create(nombre='SIC_factExist_cliente', tipo='V', padre=padre)
        if not Registry.objects.filter(nombre='SIC_factExist_ventasCaja').exists():
            Registry.objects.create(nombre='SIC_factExist_ventasCaja', tipo='V', padre=padre)
        if not Registry.objects.filter(nombre='SIC_factExist_ventasCajero').exists():
            Registry.objects.create(nombre='SIC_factExist_ventasCajero', tipo='V', padre=padre)
        if not Registry.objects.filter(nombre='SIC_factExist_ventasVendedor').exists():
            Registry.objects.create(nombre='SIC_factExist_ventasVendedor', tipo='V', padre=padre)
        if not Registry.objects.filter(nombre='SIC_factExist_margenPrecioLista').exists():
            Registry.objects.create(nombre='SIC_factExist_margenPrecioLista', tipo='V', padre=padre)
        if not Registry.objects.filter(nombre='SIC_factExist_margenPrecioCosto').exists():
            Registry.objects.create(nombre='SIC_factExist_margenPrecioCosto', tipo='V', padre=padre)
        padre = first_or_none(Registry.objects.filter(nombre='PreferenciasEmpresa'))
        if request.user.is_superuser and padre:
            using = router.db_for_write(Registry)
            for procedure in procedures_sic:
                c = connections[using].cursor()
                c.execute(procedures_sic[procedure])
                c.execute('EXECUTE PROCEDURE %s;' % procedure)
                c.execute('DROP PROCEDURE %s;' % procedure)
                c.close()

        management.call_command('syncdb', database=using, interactive=False)
    else:
        return HttpResponseRedirect('/djmicrosip_faexist/')
    return HttpResponseRedirect('/djmicrosip_faexist/preferencias/')


def ignorar_articulos(request):
    """
    Ignorar articulos
    """
    error = ''
    factura_id = 0
    reporte_id = 0
    articulos_ids = request.GET.getlist('articulos_ids')
    ignorar = request.GET.getlist('ignorar')[0] == 'true'
    for articulo_id in articulos_ids:
        articulo = Articulo.objects.get(pk=articulo_id)
        articulo.facturaexistencia_ignorar = ignorar
        articulo.save(update_fields=('facturaexistencia_ignorar', ))

    data = {'msg': 'Datos guradados'}
    return HttpResponse(json.dumps(data), mimetype='application/json')