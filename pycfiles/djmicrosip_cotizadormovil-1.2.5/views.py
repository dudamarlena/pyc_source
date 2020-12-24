# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Repos\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_cotizadormovil\djmicrosip_cotizadormovil\views.py
# Compiled at: 2015-06-16 13:13:17
from .forms import *
from .models import *
from datetime import datetime
from django.core import management
from django.contrib.auth.decorators import login_required
from django.db import router, connections
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from microsip_api.comun.sic_db import first_or_none, get_existencias_articulo
import json
from decimal import Decimal

def GetPrecioVentaArticulo(articulo, precio_empresa_id):
    precio_con_impuesto = 0
    precio_sin_impuesto = 0
    try:
        articuloprecio = ArticuloPrecio.objects.get(articulo__id=articulo.id, precio_empresa__id=precio_empresa_id)
    except Exception as e:
        moneda = Moneda.objects.get(es_moneda_local='S')
        precio_sin_impuesto = 0
        tipo_cambio = 1
    else:
        precio_sin_impuesto = articuloprecio.precio
        using = router.db_for_write(Articulo)
        c = connections[using].cursor()
        query = " EXECUTE PROCEDURE PRECIO_CON_IMPTO(%s, %s,'N',0,0, CURRENT_DATE,'P')"
        c.execute(query, [articulo.id, precio_sin_impuesto])
        precio_con_impuesto = c.fetchall()[0][0]
        c.close()

    return (precio_sin_impuesto, precio_con_impuesto)


@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_cotizadormovil/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def cotizacionView(request, template_name='djmicrosip_cotizadormovil/cotizacion.html'):
    monedas = Moneda.objects.all()
    dls = first_or_none(Moneda.objects.filter(es_moneda_local='N'))
    tipos_cambio = TipoCambio.objects.filter(moneda=dls).order_by('-fecha')
    tipo_cambio = tipos_cambio[0]
    tipo_cambio = tipo_cambio.tipo_cambio
    listas_precios = PrecioEmpresa.objects.all()
    DetalleFormset = CotizacionFormset(VentasDocumentoDetalleForm, extra=1, can_delete=True, can_order=False)
    formset = DetalleFormset(request.POST or None)
    context = {'formset': formset, 
       'monedas': monedas, 
       'tipo_cambio_dls': tipo_cambio, 
       'listas_precios': listas_precios}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def PreferenciasManageView(request, template_name='djmicrosip_cotizadormovil/herramientas/preferencias.html'):
    msg = ''
    initial_data = {'crear_documento': Registry.objects.get(nombre='SIC_cotizadorm_integrar').get_value(), 
       'pv_cliente': Registry.objects.get(nombre='SIC_cotizadorm_cliente_pv').get_value(), 
       'pv_almacen': Registry.objects.get(nombre='SIC_cotizadorm_almacen_pv').get_value(), 
       'pv_caja': Registry.objects.get(nombre='SIC_cotizadorm_Caja_pv').get_value(), 
       'pv_cajero': Registry.objects.get(nombre='SIC_cotizadorm_Cajero_pv').get_value(), 
       'pv_vendedor': Registry.objects.get(nombre='SIC_cotizadorm_Vendedor_pv').get_value(), 
       've_cliente': Registry.objects.get(nombre='SIC_cotizadorm_cliente_ve').get_value(), 
       've_almacen': Registry.objects.get(nombre='SIC_cotizadorm_almacen_ve').get_value(), 
       've_condicion_pago': Registry.objects.get(nombre='SIC_cotizadorm_CondicionPago_ve').get_value(), 
       've_vendedor': Registry.objects.get(nombre='SIC_cotizadorm_Vendedor_ve').get_value()}
    form = PreferenciasManageForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        form.save()
        msg = 'Datos guardados correctamente'
    c = {'form': form, 'msg': msg}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def UpdateDatabaseTable(request):
    """ Agrega campos nuevos en tablas de base de datos. """
    if request.user.is_superuser:
        padre = first_or_none(Registry.objects.filter(nombre='PreferenciasEmpresa'))
        if padre:
            if not Registry.objects.filter(nombre='SIC_cotizadorm_integrar').exists():
                Registry.objects.create(nombre='SIC_cotizadorm_integrar', tipo='V', padre=padre, valor='')
            if not Registry.objects.filter(nombre='SIC_cotizadorm_cliente_pv').exists():
                Registry.objects.create(nombre='SIC_cotizadorm_cliente_pv', tipo='V', padre=padre, valor='')
            if not Registry.objects.filter(nombre='SIC_cotizadorm_almacen_pv').exists():
                Registry.objects.create(nombre='SIC_cotizadorm_almacen_pv', tipo='V', padre=padre, valor='')
            if not Registry.objects.filter(nombre='SIC_cotizadorm_Caja_pv').exists():
                Registry.objects.create(nombre='SIC_cotizadorm_Caja_pv', tipo='V', padre=padre, valor='')
            if not Registry.objects.filter(nombre='SIC_cotizadorm_Cajero_pv').exists():
                Registry.objects.create(nombre='SIC_cotizadorm_Cajero_pv', tipo='V', padre=padre, valor='')
            if not Registry.objects.filter(nombre='SIC_cotizadorm_Vendedor_pv').exists():
                Registry.objects.create(nombre='SIC_cotizadorm_Vendedor_pv', tipo='V', padre=padre, valor='')
            if not Registry.objects.filter(nombre='SIC_cotizadorm_cliente_ve').exists():
                Registry.objects.create(nombre='SIC_cotizadorm_cliente_ve', tipo='V', padre=padre, valor='')
            if not Registry.objects.filter(nombre='SIC_cotizadorm_almacen_ve').exists():
                Registry.objects.create(nombre='SIC_cotizadorm_almacen_ve', tipo='V', padre=padre, valor='')
            if not Registry.objects.filter(nombre='SIC_cotizadorm_CondicionPago_ve').exists():
                Registry.objects.create(nombre='SIC_cotizadorm_CondicionPago_ve', tipo='V', padre=padre, valor='')
            if not Registry.objects.filter(nombre='SIC_cotizadorm_Vendedor_ve').exists():
                Registry.objects.create(nombre='SIC_cotizadorm_Vendedor_ve', tipo='V', padre=padre, valor='')
    return HttpResponseRedirect('/cotizadorm/')


def GetPrecioArticulo(request):
    articulo_id = request.GET['articulo_id']
    lista_precios_id = request.GET['lista_precios_id']
    articulo_precio = None
    precio = 0
    moneda_id = None
    es_moneda_local = None
    articulo = Articulo.objects.get(id=articulo_id)
    precio_empresa = PrecioEmpresa.objects.filter(id=lista_precios_id)
    articulo_precio = ArticuloPrecio.objects.filter(articulo=articulo, precio_empresa=precio_empresa)
    if articulo_precio:
        precio = articulo_precio[0].precio
        moneda_id = articulo_precio[0].moneda.id
        es_moneda_local = articulo_precio[0].moneda.es_moneda_local
        precio = GetPrecioVentaArticulo(articulo, precio_empresa[0].id)[1]
    using = router.db_for_write(Articulo)
    existencia = get_existencias_articulo(articulo_id=articulo_id, connection_name=using, fecha_inicio=datetime.now().strftime('01/01/%Y'), almacen='CONSOLIDADO')
    data = {'precio': str(precio), 
       'moneda_id': moneda_id, 
       'es_moneda_local': es_moneda_local, 
       'existencia': str(existencia)}
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')


def GetArticulobyClave(request):
    clave = request.GET['clave']
    articulo_id = None
    articulo_nombre = None
    articulo_clave = ArticuloClave.objects.filter(clave=clave)
    if articulo_clave:
        articulo_id = articulo_clave[0].articulo.id
        articulo_nombre = articulo_clave[0].articulo.nombre
    data = {'articulo_id': articulo_id, 
       'articulo_nombre': articulo_nombre}
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')


def SearchArticulos(request):
    arts = None
    moneda_nombre = ''
    using = router.db_for_write(Articulo)
    lista_precios_id = request.GET['lista_precios_id']
    tipo_cambio = request.GET['tipo_cambio']
    nombre = request.GET['nombre']
    clave_get = request.GET['clave']
    clave = ''
    nombre_moneda = ''
    if nombre:
        arts = list(Articulo.objects.filter(nombre__icontains=nombre).order_by('nombre').values_list('id', 'nombre'))
    else:
        if clave_get:
            arts = list(ArticuloClave.objects.filter(clave=clave_get))
            if not arts:
                arts = list(ArticuloClave.objects.filter(clave__icontains=clave_get))
            arts = map(lambda art: (art.articulo.id, art.articulo.nombre), arts)
        articulos = []
        for a in arts:
            articulo_id = a[0]
            articulo = Articulo.objects.get(id=articulo_id)
            articulo_clave = first_or_none(ArticuloClave.objects.filter(articulo=articulo))
            if articulo_clave:
                clave = articulo_clave.clave
            existencia = get_existencias_articulo(articulo_id=articulo_id, connection_name=using, fecha_inicio=datetime.now().strftime('01/01/%Y'), almacen='CONSOLIDADO')
            try:
                articulo_precio = ArticuloPrecio.objects.get(articulo=articulo, precio_empresa__id=lista_precios_id)
                nombre_moneda = articulo_precio.moneda.nombre
                if articulo_precio.moneda.es_moneda_local == 'S':
                    precio_original = GetPrecioVentaArticulo(articulo, lista_precios_id)[1]
                    precio_conv = ''
                else:
                    precio_original = GetPrecioVentaArticulo(articulo, lista_precios_id)[1]
                    precio_conv = GetPrecioVentaArticulo(articulo, lista_precios_id)[1] * Decimal(tipo_cambio)
            except Exception as e:
                precio_original = 0
                precio_conv = ''

            a += (clave, str(precio_original), str(existencia), str(precio_conv), nombre_moneda)
            articulos.append(a)

    data = {'articulos': articulos}
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')


def CreaDocumento(request):
    moneda_id = request.GET['moneda_id']
    descuento_porcentaje = float(request.GET['descuento_porcentaje'])
    tipo_cambio = 1
    lista = json.loads(request.GET['lista'])
    moneda = Moneda.objects.get(id=moneda_id)
    if not moneda.es_moneda_local == 'S':
        tipo_cambio = float(request.GET['tipo_cambio'])
    using = router.db_for_write(Articulo)
    c = connections[using].cursor()
    crear_documento = Registry.objects.get(nombre='SIC_cotizadorm_integrar').get_value()
    documento = None
    if crear_documento == 'P':
        cliente_id = Registry.objects.get(nombre='SIC_cotizadorm_cliente_pv').get_value()
        almacen_id = Registry.objects.get(nombre='SIC_cotizadorm_almacen_pv').get_value()
        caja_id = Registry.objects.get(nombre='SIC_cotizadorm_Caja_pv').get_value()
        cajero_id = Registry.objects.get(nombre='SIC_cotizadorm_Cajero_pv').get_value()
        vendedor_id = Registry.objects.get(nombre='SIC_cotizadorm_Vendedor_pv').get_value()
        cliente = Cliente.objects.get(id=cliente_id)
        almacen = Almacen.objects.get(ALMACEN_ID=almacen_id)
        caja = Caja.objects.get(id=caja_id)
        cajero = Cajero.objects.get(id=cajero_id)
        vendedor = Vendedor.objects.get(id=vendedor_id)
        cliente_clave = first_or_none(ClienteClave.objects.filter(cliente=cliente))
        documento = PuntoVentaDocumento(id=-1, caja=caja, cajero=cajero, cliente=cliente, clave_cliente=cliente_clave, vendedor=vendedor, almacen=almacen, moneda=moneda, tipo='O', tipo_cambio=tipo_cambio, aplicado='N', fecha=datetime.now(), hora=datetime.now().strftime('%H:%M:%S'), importe_neto=0, porcentaje_descuento=descuento_porcentaje, total_impuestos=0, importe_donativo=0, total_fpgc=0, sistema_origen='PV', descripcion='', usuario_creador=request.user.username, tipo_gen_fac=None, fecha_envio=datetime.now())
        documento.save()
        for detalle in lista:
            articulo_id = int(detalle[0])
            precio_con_impuesto = float(detalle[1])
            porcentaje_descuento = float(detalle[2])
            precio_total_neto = float(detalle[3])
            unidades = float(detalle[4])
            articulo = Articulo.objects.get(id=articulo_id)
            articulo_clave = first_or_none(ArticuloClave.objects.filter(rol__es_ppal='S', articulo=articulo))
            query = " EXECUTE PROCEDURE PRECIO_CON_IMPTO(%s, %s,'N',0,0, CURRENT_DATE,'Q')"
            c.execute(query, [articulo.id, precio_con_impuesto])
            precio_sin_impuesto = c.fetchall()[0][0]
            c.close()
            detalle_doc = PuntoVentaDocumentoDetalle.objects.create(id=-1, documento_pv=documento, clave_articulo=articulo_clave, articulo=articulo, unidades=unidades, unidades_dev=0, precio_unitario=precio_sin_impuesto, precio_unitario_impto=precio_con_impuesto, fpgc_unitario=0, porcentaje_descuento=porcentaje_descuento, precio_total_neto=precio_total_neto, porcentaje_comis=0, rol='N', posicion=-1)

        c.execute("execute procedure calc_totales_docto_pv(%s,'N','S',0)" % documento.id)
        management.call_command('syncdb', database=using, interactive=False)
    elif crear_documento == 'V':
        cliente_id = Registry.objects.get(nombre='SIC_cotizadorm_cliente_ve').get_value()
        almacen_id = Registry.objects.get(nombre='SIC_cotizadorm_almacen_ve').get_value()
        condicion_pago_id = Registry.objects.get(nombre='SIC_cotizadorm_CondicionPago_ve').get_value()
        vendedor_id = Registry.objects.get(nombre='SIC_cotizadorm_Vendedor_ve').get_value()
        cliente = Cliente.objects.get(id=cliente_id)
        cliente_direccion = first_or_none(ClienteDireccion.objects.filter(cliente=cliente))
        almacen = Almacen.objects.get(ALMACEN_ID=almacen_id)
        condicion_pago = CondicionPago.objects.get(id=condicion_pago_id)
        vendedor = Vendedor.objects.get(id=vendedor_id)
        cliente_clave = first_or_none(ClienteClave.objects.filter(cliente=cliente))
        documento = VentasDocumento(tipo='P', subtipo='N', fecha=datetime.now(), cliente=cliente, cliente_clave=cliente_clave, cliente_direccion=cliente_direccion, direccion_consignatario=cliente_direccion, almacen=almacen, descuento_tipo='P', descuento_importe=0, descuento_porcentaje=descuento_porcentaje, estado='P', moneda=moneda, tipo_cambio=tipo_cambio, condicion_pago=condicion_pago, vendedor=vendedor, modalidad_facturacion=None, sistema_origen='VE')
        documento.save()
        for detalle in lista:
            articulo_id = int(detalle[0])
            precio_con_impuesto = float(detalle[1])
            porcentaje_descuento = float(detalle[2])
            precio_total_neto = float(detalle[3])
            unidades = float(detalle[4])
            articulo = Articulo.objects.get(id=articulo_id)
            articulo_clave = first_or_none(ArticuloClave.objects.filter(rol__es_ppal='S', articulo=articulo))
            query = " EXECUTE PROCEDURE PRECIO_CON_IMPTO(%s, %s,'N',0,0, CURRENT_DATE,'Q')"
            c.execute(query, [articulo.id, precio_con_impuesto])
            precio_sin_impuesto = c.fetchall()[0][0]
            c.close()
            detalle_doc = VentasDocumentoDetalle.objects.create(id=-1, documento=documento, articulo_clave=articulo_clave, articulo=articulo, unidades=unidades, precio_unitario=precio_sin_impuesto, descuento_porcentaje=porcentaje_descuento, precio_total_neto=0, posicion=-1)

        c.execute("execute procedure calc_totales_docto_ve(%s,'N')" % documento.id)
        management.call_command('syncdb', database=using, interactive=False)
    if documento:
        documento_folio = documento.folio
    else:
        documento_folio = '-'
    if crear_documento == 'V':
        modulo = 'Ventas'
    elif crear_documento == 'P':
        modulo = 'Punto de Venta'
    else:
        modulo = ''
    data = {'documento_folio': documento_folio, 
       'modulo': modulo}
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')