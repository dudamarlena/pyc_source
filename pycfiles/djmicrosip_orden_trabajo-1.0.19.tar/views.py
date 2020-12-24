# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_orden_trabajo\djmicrosip_orden_trabajo\views.py
# Compiled at: 2020-04-18 15:11:19
from .forms import *
from .models import *
from django.db.models import get_app, get_models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_microsip_base.libs.models_base.models import Articulo, ArticuloPrecio, ArticuloClave, Moneda, PrecioEmpresa, Registry, ClienteDireccion, Cliente, CondicionPago, Vendedor, VentasDocumento, VentasDocumentoDetalle, Almacen, ClienteClave, VentasDocumentoLiga
from django.contrib.auth.models import User
from datetime import datetime
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.list import ListView
from django.db import router, connections, connection
from django.core import management
from microsip_api.comun.sic_db import first_or_none
from storage import send_mail_orden
import time, json, os, pdb, re, io, cStringIO as StringIO
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from datetime import date, datetime, timedelta
from django.db.models import Q
from xhtml2pdf import pisa
from base64 import decodestring
from django.core.files import File
import onesignal as onesignal_sdk
from apscheduler.schedulers.background import BackgroundScheduler
app_id = 'abe73585-28d8-4b4d-9fa7-ffcd40fd980f'
app_api_key = 'Zjc3ZDZmMDctYTk0OC00ZWU1LTkwNmEtNjVlYzJiZWNkZTc3'
onesignal_client = onesignal_sdk.Client(app_auth_key=app_api_key, app_id=app_id)

@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_orden_trabajo/index.html'):
    bdatos = request.session['selected_database']
    conexion = request.session['conexion_activa']
    form_busqueda = FindFrom(request.POST or None)
    ventas_ligas = None
    ligas = []
    form = VendedorForm(request.POST or None)
    if request.method == 'POST':
        if form_busqueda.is_valid():
            page = 1
            llamada = form_busqueda.cleaned_data['llamada']
            busqueda = form_busqueda.cleaned_data['busqueda']
            inicio = form_busqueda.cleaned_data['inicio']
            fin = form_busqueda.cleaned_data['fin']
            filtro = form_busqueda.cleaned_data['filtro']
            tipo_documento = form_busqueda.cleaned_data['tipo_documento']
            inicio = datetime(inicio.year, inicio.month, inicio.day, 0, 0)
            fin = datetime(fin.year, fin.month, fin.day, 23, 59)
            pedidos_all = Pedidos_Crm.objects.all().order_by('fecha_registro')
            print filtro
            if inicio and fin:
                pedidos_all = pedidos_all.filter(fecha_registro__gte=inicio, fecha_registro__lte=fin)
            if llamada:
                pedidos_all = pedidos_all.filter(llamada=llamada)
            if filtro == 'EP':
                pedidos_all = pedidos_all.filter(progreso__in=['0', '25', '50', '75'])
            elif filtro == 'F':
                pedidos_all = pedidos_all.filter(progreso__in=['100'])
            pedidos = pedidos_all.values_list('folio').order_by('fecha_registro')
            if tipo_documento == 'F':
                ventas_surtidas = VentasDocumento.objects.filter(folio__in=pedidos, estado='S')
                ventas_ligas = VentasDocumentoLiga.objects.filter(factura__in=ventas_surtidas, devolucion__estado='F').values_list('factura__id')
                ligas = [ ven[0] for ven in ventas_ligas ]
                if ventas_ligas:
                    ventas = VentasDocumento.objects.filter(Q(estado='F', folio__in=pedidos) | Q(id__in=ventas_ligas)).exclude(estado__in=['C'])
                else:
                    ventas = VentasDocumento.objects.filter(estado='F', folio__in=pedidos).exclude(estado__in=['C'])
            elif tipo_documento == 'R':
                ventas_surtidas = VentasDocumento.objects.filter(folio__in=pedidos, estado='S')
                ventas_ligas = VentasDocumentoLiga.objects.filter(factura__in=ventas_surtidas, devolucion__estado='F').values_list('factura__id')
                ligas = [ ven[0] for ven in ventas_ligas ]
                if ventas_ligas:
                    ventas = VentasDocumento.objects.filter(folio__in=pedidos, estado='S').exclude(estado__in=['C']).exclude(id__in=ventas_ligas)
                else:
                    ventas = VentasDocumento.objects.filter(folio__in=pedidos, estado='S').exclude(estado__in=['C'])
            else:
                ventas = VentasDocumento.objects.filter(folio__in=pedidos).exclude(estado__in=['C', 'S', 'F'])
            if busqueda:
                if len(busqueda) >= 8:
                    ventas = ventas.filter(Q(cliente__nombre__icontains=busqueda) | Q(cliente__contacto1__icontains=busqueda) | Q(vendedor__nombre__icontains=busqueda))
                else:
                    ventas = ventas.filter(Q(cliente__nombre__icontains=busqueda) | Q(cliente__contacto1__icontains=busqueda) | Q(vendedor__nombre__icontains=busqueda) | Q(folio__icontains=busqueda))
            if filtro == 'PDA':
                ventas = ventas.filter(vendedor=None)
    else:
        page = request.GET.get('page')
        llamada = request.GET.get('llamada')
        busqueda = request.GET.get('busqueda')
        filtro = request.GET.get('filtro')
        tipo_documento = request.GET.get('tipo_documento')
        if request.GET.get('inicio') and request.GET.get('fin'):
            inicio = request.GET.get('inicio')
            fin = request.GET.get('fin')
            inicio = datetime.strptime(inicio, '%d/%m/%Y')
            fin = datetime.strptime(fin, '%d/%m/%Y')
            inicio = datetime(inicio.year, inicio.month, inicio.day, 0, 0)
            fin = datetime(fin.year, fin.month, fin.day, 23, 59)
            pedidos_all = Pedidos_Crm.objects.filter(fecha_registro__gte=inicio, fecha_registro__lte=fin)
        else:
            hoy = datetime.today()
            inicio = datetime(hoy.year, hoy.month, hoy.day, 0, 0)
            fin = datetime(hoy.year, hoy.month, hoy.day, 23, 59)
            pedidos_all = Pedidos_Crm.objects.filter(fecha_registro__gte=inicio, fecha_registro__lte=fin)
        if llamada:
            pedidos_all = pedidos_all.filter(llamada=llamada)
        if filtro == 'EP':
            pedidos_all = pedidos_all.filter(progreso__in=['0', '25', '50', '75'])
        else:
            if filtro == 'F':
                pedidos_all = pedidos_all.filter(progreso__in=['100'])
            pedidos = pedidos_all.values_list('folio').order_by('fecha_registro')
            if tipo_documento == 'F':
                ventas_surtidas = VentasDocumento.objects.filter(folio__in=pedidos, estado='S')
                ventas_ligas = VentasDocumentoLiga.objects.filter(factura__in=ventas_surtidas, devolucion__estado='F').values_list('factura__id')
                ligas = [ ven[0] for ven in ventas_ligas ]
                if ventas_ligas:
                    ventas = VentasDocumento.objects.filter(Q(estado='F', folio__in=pedidos) | Q(id__in=ventas_ligas)).exclude(estado__in=['C'])
                else:
                    ventas = VentasDocumento.objects.filter(estado='F', folio__in=pedidos).exclude(estado__in=['C'])
            else:
                if tipo_documento == 'R':
                    ventas_surtidas = VentasDocumento.objects.filter(folio__in=pedidos, estado='S')
                    ventas_ligas = VentasDocumentoLiga.objects.filter(factura__in=ventas_surtidas, devolucion__estado='F').values_list('factura__id')
                    ligas = [ ven[0] for ven in ventas_ligas ]
                    if ventas_ligas:
                        ventas = VentasDocumento.objects.filter(folio__in=pedidos, estado='S').exclude(estado__in=['C']).exclude(id__in=ventas_ligas)
                    else:
                        ventas = VentasDocumento.objects.filter(folio__in=pedidos, estado='S').exclude(estado__in=['C'])
                else:
                    print tipo_documento
                    ventas = VentasDocumento.objects.filter(folio__in=pedidos).exclude(estado__in=['C', 'S', 'F'])
                if busqueda:
                    if len(busqueda) >= 8:
                        ventas = ventas.filter(Q(cliente__nombre__icontains=busqueda) | Q(cliente__contacto1__icontains=busqueda) | Q(vendedor__nombre__icontains=busqueda))
                    else:
                        ventas = ventas.filter(Q(cliente__nombre__icontains=busqueda) | Q(cliente__contacto1__icontains=busqueda) | Q(vendedor__nombre__icontains=busqueda) | Q(folio__icontains=busqueda))
                if filtro == 'PDA':
                    ventas = ventas.filter(vendedor=None)
                form_initial = {'llamada': llamada, 
                   'busqueda': busqueda, 
                   'filtro': filtro, 
                   'tipo_documento': tipo_documento, 
                   'inicio': inicio, 
                   'fin': fin}
                form_busqueda = FindFrom(request.POST or None, initial=form_initial)
            ventas = ventas.order_by('-folio')
            for venta in ventas:
                for pedido in pedidos_all:
                    if pedido.folio == venta.folio:
                        folio = pedido.folio
                        pedido.folio = none_cero(folio)
                        venta.pedido = pedido

        paginator = Paginator(ventas, 20)
        try:
            ventas = paginator.page(page)
        except PageNotAnInteger:
            ventas = paginator.page(1)
        except EmptyPage:
            ventas = paginator.page(paginator.num_pages)

    context = {'form': form, 'pedidos': pedidos_all, 
       'ventas': ventas, 
       'form_busqueda': form_busqueda, 
       'ligas': ligas, 
       'llamada': llamada, 
       'busqueda': busqueda, 
       'inicio': inicio, 
       'fin': fin, 
       'filtro': filtro, 
       'tipo_documento': tipo_documento}
    return render(request, template_name, context)


def none_cero(folio):
    indice_inicio = 0
    indice_fin = 0
    x = 0
    while indice_inicio == 0:
        if folio[x] == '0':
            indice_inicio = x
        x = x + 1

    x = indice_inicio
    while indice_fin == 0:
        if folio[x] != '0':
            indice_fin = x
        x = x + 1

    remplazar = folio[indice_inicio:indice_fin]
    folio_nuevo = folio.replace(remplazar, '')
    return folio_nuevo


@login_required(login_url='/login/')
def add_pedido(request, id):
    id_articulo = Registry.objects.get(nombre='SIC_Pedidos_Crm_Articulo_predeterminado').get_value()
    articulo = Articulo.objects.get(id=id_articulo)
    clave_articulo = ArticuloClave.objects.filter(articulo__id=id_articulo)
    if settings.MICROSIP_VERSION >= 2020:
        using = router.db_for_write(Articulo)
        c = connections[using].cursor()
        query = "select sucursal_id from sucursales where nombre='Matriz'"
        c.execute(query)
        sucursal_id = c.fetchall()[0][0]
        print sucursal_id
    if clave_articulo:
        clave_articulo = clave_articulo[0].clave
    else:
        clave_articulo = None
    form_initial = [
     {'articulo': articulo, 
        'unidades': 1, 
        'precio_unitario': 0, 
        'descuento_porcentaje': 0, 
        'precio_total_neto': 0, 
        'notas': None, 
        'articulo_clave': clave_articulo}]
    if id != '0':
        pedido = Pedidos_Crm.objects.get(id=id)
        print ('-----------', pedido)
    else:
        pedido = None
    if pedido:
        venta = VentasDocumento.objects.get(folio=pedido.folio)
        venta_fecha = VentasDocumento.objects.filter(folio=pedido.folio)[0]
        form = PedidoAddForm(request.POST or None, instance=venta)
        DetalleFormSet = inlineformset_factory(VentasDocumento, VentasDocumentoDetalle, VentasDetalleDocumentoForm, extra=1)
        formset = DetalleFormSet(request.POST or None, instance=venta)
        form_crm = PedidoCrmForm(request.POST or None, instance=pedido)
    else:
        venta = None
        form = PedidoAddForm(request.POST or None)
        DetalleFormSet = inlineformset_factory(VentasDocumento, VentasDocumentoDetalle, VentasDetalleDocumentoForm, extra=2)
        formset = DetalleFormSet(request.POST or None, initial=form_initial)
        form_crm = PedidoCrmForm(request.POST or None)
    print ('frist', pedido)
    usuario = request.user
    bdatos = request.session['selected_database']
    conexion = request.session['conexion_activa']
    if request.method == 'POST':
        if form.is_valid():
            form.instance.estado = 'P'
            form.instance.sistema_origen = 'VE'
            form.instance.modalidad_facturacion = None
            form.instance.metodo_pago_sat = None
            form.instance.modalidad_facturacion = None
            form.instance.metodo_pago_sat = None
            form.instance.uso_cfdi = None
            form.instance.sucursal_id = sucursal_id
            if not venta:
                form.instance.fecha = date.today()
                form.instance.creacion_usuario = usuario
            else:
                form.instance.fecha = venta_fecha.fecha
                form.instance.vendedor = venta_fecha.vendedor
                form.instance.creacion_usuario = venta_fecha.creacion_usuario
            if formset.is_valid():
                if form_crm.is_valid():
                    descripcion_venta = form.instance.descripcion
                    remplazo = form_crm.instance.descripcion_general
                    if remplazo:
                        sin_hadware = descripcion_venta.replace(remplazo, '')
                    else:
                        sin_hadware = form.instance.descripcion
                    objetos = form_crm.instance.hardware
                    hardware = ''
                    if objetos:
                        hardware = ' se recibio '
                        for objeto in objetos:
                            if objeto == 'OTROS':
                                hardware = hardware + form_crm.instance.descripcion_otros.upper() + ', '
                            else:
                                hardware = hardware + objeto + ', '

                    form.instance.descripcion = sin_hadware + hardware
                    hard = form_crm.cleaned_data['hardware']
                    precio_aproximado = form_crm.cleaned_data['precio_aproximado']
                    tipo_servicio = form_crm.cleaned_data['tipo_servicio']
                    tipo_llamada = form_crm.cleaned_data['tipo_llamada']
                    llamada = form_crm.cleaned_data['llamada']
                    preprogramado = form_crm.cleaned_data['preprogramado']
                    if form_crm.cleaned_data['fecha_registro']:
                        fecha_registro = form_crm.cleaned_data['fecha_registro']
                    else:
                        fecha_registro = datetime.now()
                    if llamada:
                        form.instance.tipo = 'P'
                    else:
                        form.instance.tipo = 'R'
                    if preprogramado:
                        date_ = date(fecha_registro.year, fecha_registro.month, fecha_registro.day)
                        form.instance.fecha = date_
                    object_save = form.save()
                    if not venta:
                        formset.instance = object_save
                    formset.save()
                    player_ids = []
                    if pedido:
                        form_crm.save()
                        return redirect('/pedidos/pedido/' + str(form_crm.instance.id) + '/')
                    nombre_cliente = form.instance.cliente.nombre.encode('UTF-8')
                    content = {'en': 'Orden de trabajo de ' + str(nombre_cliente) + ', click para mas detalles', 'es': 'Orden de trabajo de ' + str(nombre_cliente) + ', click para mas detalles'}
                    headings = {'en': 'Hay unan nueva orden de trabajo', 'es': 'Hay unan nueva orden de trabajo'}
                    usuarios = Usuario_notificacion.objects.all().values_list('id_onesignal')
                    for usuario in usuarios:
                        player_ids.append(str(usuario[0]))

                    url = 'http://sic.no-ip.org:8001/pedidos/'
                    push = send_push_notification(content=content, headings=headings, url=url, player_ids=player_ids)
                    print push.status_code
                    print push.json()
                    pedido_crm = Pedidos_Crm.objects.get_or_create(folio=object_save.folio, bdatos=bdatos, conexion=conexion, hardware=hard, descripcion_general=hardware, precio_aproximado=precio_aproximado, tipo_servicio=tipo_servicio, tipo_llamada=tipo_llamada, llamada=llamada, fecha_registro=fecha_registro, preprogramado=preprogramado)
                    return redirect('/pedidos/pedido/' + str(pedido_crm[0].id) + '/')
    context = {'form': form, 
       'formset': formset, 
       'form_crm': form_crm}
    return render(request, 'djmicrosip_orden_trabajo/add_pedido.html', context)


@login_required(login_url='/login/')
def info_cliente(request):
    id_cliente = request.GET['id']
    if id_cliente:
        direcciones_cliente = ClienteDireccion.objects.filter(cliente_id=id_cliente)
        cliente_clave = ClienteClave.objects.filter(cliente__id=id_cliente)
        cliente = Cliente.objects.filter(id=id_cliente)[0]
        moneda = cliente.moneda
        condicion_de_pago = cliente.condicion_de_pago
        print direcciones_cliente
    if cliente_clave:
        clave_cliente = cliente_clave[0].clave
    else:
        clave_cliente = ''
    lista_direccion = {}
    direccion = {}
    for direccion_cliente in direcciones_cliente:
        direccion['id'] = direccion_cliente.pk
        direccion['calle'] = direccion_cliente.calle
        direccion['es_ppal'] = direccion_cliente.es_ppal
        lista_direccion[direccion_cliente.pk] = direccion

    data = {'lista_direccion': lista_direccion, 'clave': clave_cliente, 
       'moneda': moneda.id, 
       'condicion_de_pago': condicion_de_pago.id}
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/login/')
def vendedor_asignar(request):
    id_vendedor = request.GET['id_vendedor']
    id_crm = request.GET['id_crm']
    player_ids = []
    pedido = Pedidos_Crm.objects.filter(id=id_crm)[0]
    venta = VentasDocumento.objects.filter(folio=pedido.folio)[0]
    if venta:
        vendedor = Vendedor.objects.filter(id=id_vendedor)[0]
        venta.vendedor = vendedor
        venta.save()
        mensaje = vendedor.nombre
        data = {'mensaje': mensaje}
        nombre_cliente = venta.cliente.nombre.encode('UTF-8')
        content = {'en': 'Has recibido una asignacion para ' + nombre_cliente + ', click para mas detalles', 'es': 'Has recibido una asignacion para ' + nombre_cliente + ', click para mas detalles'}
        headings = {'en': 'Asignacion de orden de trabajo', 'es': 'Asignacion de orden de trabajo'}
        usuarios = Usuario_notificacion.objects.filter(vendedor=vendedor).values_list('id_onesignal')
        for usuario in usuarios:
            player_ids.append(str(usuario[0]))

        url = 'http://sic.no-ip.org:8001/pedidos/pedido/' + str(id_crm) + '/'
        push = send_push_notification(content=content, headings=headings, url=url, player_ids=player_ids)
        print push.status_code
        print push.json()
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        mensaje = ''
        data = {'mensaje': mensaje}
        return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/login/')
def get_detalles(request):
    id_doc = request.GET['id_doc']
    detalles_venta = VentasDocumentoDetalle.objects.filter(documento__id=id_doc)
    lista_detalle = []
    for detalle in detalles_venta:
        detalles = {}
        detalles['articulo'] = detalle.articulo.nombre
        detalles['unidades'] = str(detalle.unidades)
        detalles['notas'] = detalle.notas
        lista_detalle.append(detalles)

    return HttpResponse(json.dumps(lista_detalle), content_type='application/json')


@login_required(login_url='/login/')
def get_tiempos(request):
    id_crm = request.GET['id_crm']
    pedido = Pedidos_Crm.objects.filter(id=id_crm)[0]
    data = {}
    if pedido.fecha_inicio:
        tiempo_espera = pedido.fecha_inicio - pedido.fecha_registro
        data['tiempo_espera'] = formato_tiempo(tiempo_espera)
    if pedido.fecha_fin:
        tiempo_fin = pedido.fecha_fin - pedido.fecha_inicio
        data['tiempo_fin'] = formato_tiempo(tiempo_fin)
    if pedido.fecha_aviso:
        tiempo_aviso = pedido.fecha_aviso - pedido.fecha_fin
        data['tiempo_aviso'] = formato_tiempo(tiempo_aviso)
    if pedido.fecha_entrega:
        tiempo_entrega = pedido.fecha_entrega - pedido.fecha_aviso
        data['tiempo_entrega'] = formato_tiempo(tiempo_entrega)
    return HttpResponse(json.dumps(data), content_type='application/json')


def formato_tiempo(time):
    print time
    seconds = time.total_seconds()
    dias = seconds / 86400
    horas = seconds / 3600
    tiempo = ('{0:.2f} hora(s)').format(horas)
    if horas < 1:
        minutos = seconds / 60
        tiempo = ('{0:.2f} minuto(s)').format(minutos)
    elif horas > 24:
        tiempo = ('{0:.2f} dia(s)').format(dias)
    return tiempo


@login_required(login_url='/login/')
def fin_progress(request):
    id_crm = request.GET['id_crm']
    pedido = Pedidos_Crm.objects.filter(id=id_crm)[0]
    if pedido:
        pedido.fecha_inicio = pedido.fecha_registro
        pedido.fecha_fin = pedido.fecha_registro
        pedido.fecha_aviso = pedido.fecha_registro
        print pedido.fecha_aviso
        pedido.progreso = '100'
        pedido.fecha_entrega = datetime.now()
    pedido.save()
    return HttpResponse(json.dumps(pedido.progreso), content_type='application/json')


@login_required(login_url='/login/')
def change_progress(request):
    id_crm = request.GET['id_crm']
    pedido = Pedidos_Crm.objects.filter(id=id_crm)[0]
    if pedido.progreso == '0':
        pedido.progreso = '25'
        pedido.fecha_inicio = datetime.now()
    elif pedido.progreso == '25':
        pedido.progreso = '50'
        pedido.fecha_fin = datetime.now()
    elif pedido.progreso == '50':
        pedido.progreso = '75'
        pedido.fecha_aviso = datetime.now()
    elif pedido.progreso == '75':
        pedido.progreso = '100'
        pedido.fecha_entrega = datetime.now()
    pedido.save()
    return HttpResponse(json.dumps(pedido.progreso), content_type='application/json')


@login_required(login_url='/login/')
def return_progress(request):
    id_crm = request.GET['id_crm']
    pedido = Pedidos_Crm.objects.filter(id=id_crm)[0]
    if pedido.progreso == '25':
        pedido.progreso = '0'
        pedido.fecha_inicio = None
    elif pedido.progreso == '50':
        pedido.progreso = '25'
        pedido.fecha_fin = None
    elif pedido.progreso == '75':
        pedido.progreso = '50'
        pedido.fecha_aviso = None
    elif pedido.progreso == '100':
        pedido.progreso = '75'
        pedido.fecha_entrega = None
    pedido.save()
    return HttpResponse(json.dumps(pedido.progreso), content_type='application/json')


@login_required(login_url='/login/')
def inf_articulo(request):
    id_articulo = request.GET['id']
    id_cliente = request.GET['id_cliente']
    id_almacen = request.GET['id_almacen']
    data_articulo = GetArticulo(id_articulo, id_cliente, id_almacen)
    precio_articulo = 0
    if id_articulo:
        articulo = ArticuloPrecio.objects.filter(articulo__id=id_articulo)
        clave_articulo = ArticuloClave.objects.filter(articulo__id=id_articulo)
        if articulo:
            precio_articulo = articulo[0].precio
        else:
            precio_articulo = 0
        if clave_articulo:
            clave = clave_articulo[0].clave
        else:
            clave = ''
    data = {'precio_articulo': str(precio_articulo), 
       'clave': clave, 
       'existencia': data_articulo['existencia'], 
       'descuento': data_articulo['descuento']}
    return HttpResponse(json.dumps(data), content_type='application/json')


def GetArticulo(articulo_id, cliente_id, id_almacen):
    try:
        using = router.db_for_write(Articulo)
        c = connections[using].cursor()
        c.execute('EXECUTE PROCEDURE CALC_EXIS_ARTALM %s,%s,CURRENT_DATE;' % (articulo_id, id_almacen))
        existencia = c.fetchall()[0][0]
        c.execute('SELECT * FROM GET_POLS_DSCTO_ARTCLI (%s,%s,CURRENT_DATE) where descuento>0;' % (articulo_id, cliente_id))
        descuento = c.fetchall()[0][1]
        data = {'existencia': str(existencia), 
           'descuento': str(descuento)}
        c.close()
    except Exception as e:
        print e

    return data


def actualiza_base_datos(request):
    using = router.db_for_write(Pedidos_Crm)
    fields_exist = []
    bandera = False
    data = {}
    app = get_app('djmicrosip_orden_trabajo')
    for field in Pedidos_Crm._meta.fields:
        fields_exist.append(field.get_attname_column()[1])
        data[field.get_attname_column()[1]] = {'campo': field.db_type(connections[using]), 'null': field.null, 'default': field.default}

    try:
        col_names = []
        management.call_command('syncdb', database=using, interactive=False)
        c = connections[using].cursor()
        c.execute('SELECT * FROM SIC_PEDIDOS_CRM')
        for desc in enumerate(c.description):
            col_names.append(desc[1][0])

        diferencia = list(set(fields_exist) - set(col_names))
        dif_contraria = list(set(col_names) - set(fields_exist))
        campos_add = ''
        if diferencia:
            for campo in diferencia:
                print campo
                if data[campo]['null']:
                    campos_add = campos_add + ' ADD ' + campo + ' ' + data[campo]['campo'] + ','
                elif data[campo]['campo'] == 'smallint':
                    campos_add = campos_add + ' ADD ' + campo + ' ' + data[campo]['campo'] + ','
                else:
                    campos_add = campos_add + ' ADD ' + campo + ' ' + data[campo]['campo'] + ' NOT NULL,'

            temp = len(campos_add)
            campos_add = campos_add[:temp - 1]
            if campos_add:
                consulta = 'ALTER TABLE SIC_PEDIDOS_CRM ' + campos_add + ';'
                c.execute(consulta)
                connections[using].commit()
        if dif_contraria:
            print dif_contraria
            for campo in dif_contraria:
                print campo
                if campo == 'DOCTOS_VE_ID':
                    c.execute('DROP INDEX SIC_PEDIDOS_CRM_9D1423F5')
                    c.execute('ALTER TABLE SIC_PEDIDOS_CRM DROP CONSTRAINT DOCTOS_VE_ID_REFS_DOCTO_VE_3CD6')
                consulta_ = 'ALTER TABLE SIC_PEDIDOS_CRM DROP ' + campo + ';'
                print consulta_
                c.execute(consulta_)
                connections[using].commit()

        c.close()
    except Exception as e:
        c.close()
        print e

    padre = first_or_none(Registry.objects.filter(nombre='PreferenciasEmpresa'))
    if not Registry.objects.filter(nombre='SIC_Pedidos_Crm_Articulo_predeterminado').exists():
        Registry.objects.create(nombre='SIC_Pedidos_Crm_Articulo_predeterminado', tipo='V', padre=padre, valor='')
    if not Registry.objects.filter(nombre='SIC_Pedidos_Crm_Logo').exists():
        Registry.objects.create(nombre='SIC_Pedidos_Crm_Logo', tipo='V', padre=padre, valor='')
    if not Registry.objects.filter(nombre='SIC_Pedidos_Crm_Imagen_extra').exists():
        Registry.objects.create(nombre='SIC_Pedidos_Crm_Imagen_extra', tipo='V', padre=padre, valor='')
    if not Registry.objects.filter(nombre='SIC_Pedidos_Crm_Url_Pdf_Destino').exists():
        Registry.objects.create(nombre='SIC_Pedidos_Crm_Url_Pdf_Destino', tipo='V', padre=padre, valor='')
    if not Registry.objects.filter(nombre='SIC_Pedidos_Crm_Email').exists():
        Registry.objects.create(nombre='SIC_Pedidos_Crm_Email', tipo='V', padre=padre, valor='')
    if not Registry.objects.filter(nombre='SIC_Pedidos_Crm_Password').exists():
        Registry.objects.create(nombre='SIC_Pedidos_Crm_Password', tipo='V', padre=padre, valor='')
    if not Registry.objects.filter(nombre='SIC_Pedidos_Crm_Servidro_Correo').exists():
        Registry.objects.create(nombre='SIC_Pedidos_Crm_Servidro_Correo', tipo='V', padre=padre, valor='')
    if not Registry.objects.filter(nombre='SIC_Pedidos_Crm_Puerto').exists():
        Registry.objects.create(nombre='SIC_Pedidos_Crm_Puerto', tipo='V', padre=padre, valor='')
    return redirect('/pedidos/preferencias/')


def preferencias(request):
    id_articulo = Registry.objects.get(nombre='SIC_Pedidos_Crm_Articulo_predeterminado').get_value()
    logo = Registry.objects.get(nombre='SIC_Pedidos_Crm_Logo').get_value()
    imagen_extra = Registry.objects.get(nombre='SIC_Pedidos_Crm_Imagen_extra').get_value()
    url_pdf_destino = Registry.objects.get(nombre='SIC_Pedidos_Crm_Url_Pdf_Destino').get_value()
    email = Registry.objects.get(nombre='SIC_Pedidos_Crm_Email').get_value()
    password = Registry.objects.get(nombre='SIC_Pedidos_Crm_Password').get_value()
    servidor_correo = Registry.objects.get(nombre='SIC_Pedidos_Crm_Servidro_Correo').get_value()
    puerto = Registry.objects.get(nombre='SIC_Pedidos_Crm_Puerto').get_value()
    articulo = Articulo.objects.filter(id=id_articulo)
    form_initial = None
    if articulo:
        form_initial = {'articulo': articulo[0], 'logo': logo, 
           'imagen_extra': imagen_extra, 
           'url_pdf_destino': url_pdf_destino, 
           'email': email, 
           'password': password, 
           'servidor_correo': servidor_correo, 
           'puerto': puerto}
    form = PreferenciasManageForm(request.POST or None, initial=form_initial)
    if form.is_valid():
        form.save()
    context = {'form': form}
    return render(request, 'djmicrosip_orden_trabajo/preferencias.html', context)


def create_pdf(id_doc):
    venta = first_or_none(VentasDocumento.objects.filter(id=id_doc))
    logo = Registry.objects.get(nombre='SIC_Pedidos_Crm_Logo').get_value()
    imagen_extra = Registry.objects.get(nombre='SIC_Pedidos_Crm_Imagen_extra').get_value()
    pedido = first_or_none(Pedidos_Crm.objects.filter(folio=venta.folio))
    folio = venta.folio
    venta.folio = none_cero(folio)
    datos_empresa = Registry.objects.get(nombre='DatosEmpresa')
    datos_empresa = Registry.objects.filter(padre=datos_empresa)
    nombre = datos_empresa.get(nombre='Nombre').get_value()
    calle = datos_empresa.get(nombre='NombreCalle').get_value()
    num_ext = datos_empresa.get(nombre='NumExterior').get_value()
    colonia = datos_empresa.get(nombre='Colonia').get_value()
    telefono1 = datos_empresa.get(nombre='Telefono1').get_value()
    telefono2 = datos_empresa.get(nombre='Telefono2').get_value()
    rfc = datos_empresa.get(nombre='Rfc').get_value()
    curp = datos_empresa.get(nombre='CurpEmpresa').get_value()
    if not telefono2:
        telefono2 = ''
    email = datos_empresa.get(nombre='Email').get_value()
    poblacion = datos_empresa.get(nombre='Poblacion').get_value()
    empresa = {'nombre': nombre, 
       'calle': calle, 
       'num_ext': num_ext, 
       'colonia': colonia, 
       'telefono1': telefono1, 
       'telefono2': telefono2, 
       'email': email, 
       'poblacion': poblacion, 
       'rfc': rfc, 
       'curp': curp}
    if venta:
        venta_detalles = VentasDocumentoDetalle.objects.filter(documento__id=id_doc)
    else:
        venta_detalles = None
    context = {'venta': venta, 'venta_detalles': venta_detalles, 
       'empresa': empresa, 
       'pedido': pedido, 
       'MEDIA_URL': settings.MEDIA_URL, 
       'logo': logo, 
       'imagen_extra': imagen_extra}
    nombre = venta.folio + '.pdf'
    template_path = 'djmicrosip_orden_trabajo/nota_pedido.html'
    template = get_template(template_path)
    html = template.render(Context(context))
    destination = Registry.objects.get(nombre='SIC_Pedidos_Crm_Url_Pdf_Destino').get_value()
    file = open(destination + '\\' + nombre, 'w+b')
    pisaStatus = pisa.CreatePDF(StringIO.StringIO(html.encode('ISO-8859-1')), dest=file, encoding='UTF-8')
    file.seek(0)
    pdf = file.read()
    file.close()
    return pdf


def nota_pedido(request, id_doc):
    pdf = create_pdf(id_doc)
    return HttpResponse(pdf, content_type='application/pdf')


def firma(request, id_crm):
    pedido = Pedidos_Crm.objects.get(id=id_crm)
    form = FirmaForm(request.POST, request.FILES, instance=pedido)
    if request.method == 'POST':
        if form.is_valid():
            if request.POST.get('data_image'):
                data_url_pattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
                signature_url = request.POST.get('data_image')
                signature_data = data_url_pattern.match(signature_url).group(2)
                signature_data = bytes(signature_data)
                signature_data = decodestring(signature_data)
                img_io = io.BytesIO(signature_data)
                url = str(pedido.firma).replace('pedidos_crm/', '')
                if pedido.firma:
                    pedido.firma.save(url, File(img_io))
                else:
                    form.instance.firma.save('firma' + none_cero(pedido.folio) + '.png', File(img_io))
                return redirect('/pedidos/')
    context = {'form': form, 
       'pedido': pedido}
    return render(request, 'djmicrosip_orden_trabajo/firma.html', context)


def enviar_correo(request):
    id_crm = request.GET['id']
    pedido = Pedidos_Crm.objects.get(id=id_crm)
    venta = VentasDocumento.objects.get(folio=pedido.folio)
    cliente = ClienteDireccion.objects.get(cliente=venta.cliente)
    destinatarios = cliente.email.split(';')
    email = Registry.objects.get(nombre='SIC_Pedidos_Crm_Email').get_value()
    password = Registry.objects.get(nombre='SIC_Pedidos_Crm_Password').get_value()
    servidor_correo = Registry.objects.get(nombre='SIC_Pedidos_Crm_Servidro_Correo').get_value()
    puerto = Registry.objects.get(nombre='SIC_Pedidos_Crm_Puerto').get_value()
    nombre = none_cero(venta.folio) + '.pdf'
    pdf = create_pdf(venta.id)
    destination = Registry.objects.get(nombre='SIC_Pedidos_Crm_Url_Pdf_Destino').get_value()
    file = destination + '\\' + nombre
    data = {}
    bandera = send_mail_orden(servidor_correo, puerto, email, password, destinatarios, 'Nota de servicio', '<p>Servicios de Ingenieria</p>', file, nombre)
    if bandera:
        pedido.envio_correo = 1
        print pedido.envio_correo
        pedido.save()
        data['mensaje'] = 'Correo Enviado'
        print data
    else:
        data['mensaje'] = 'Hubo un error al enviar el correo'
        print data
    return HttpResponse(json.dumps(data), content_type='application/json')


def lista_vendedores(request):
    vendedores = Vendedor.objects.all()
    context = {'vendedores': vendedores}
    return render(request, 'djmicrosip_orden_trabajo/lista_vendedores.html', context)


def configuracion_usuarios_onesignal(request, id_vendedor):
    vendedor = Vendedor.objects.get(id=id_vendedor)
    UsuarioFormSet = inlineformset_factory(Vendedor, Usuario_notificacion, extra=1)
    usuarios = Usuario_notificacion.objects.all().values_list('id_onesignal')
    print usuarios
    print vendedor
    if vendedor:
        formset = UsuarioFormSet(request.POST or None, instance=vendedor)
    else:
        formset = UsuarioFormSet(request.POST or None)
    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
    context = {'vendedor': vendedor, 'formset': formset}
    return render(request, 'djmicrosip_orden_trabajo/configuracion.html', context)


def search_id(request):
    id_onesignal = request.GET['id']
    print id_onesignal
    usuario = Usuario_notificacion.objects.filter(id_onesignal=id_onesignal)
    if usuario:
        mensaje = 'El id de este dispositivo ya esta siendo usado por otro usuario'
    else:
        mensaje = 'Disponible'
    return HttpResponse(json.dumps(mensaje), content_type='application/json')


def send_push_notification(content, headings, url, player_ids):
    print '---------------'
    print player_ids
    new_notification = onesignal_sdk.Notification(post_body={'contents': content, 
       'include_player_ids': player_ids, 
       'headings': headings, 
       'url': url})
    onesignal_response = onesignal_client.send_notification(new_notification)
    return onesignal_response


def send_notifications_preprogramadas(request):
    hoy = datetime.today()
    ahora = datetime.now()
    inicio = datetime(hoy.year, hoy.month, hoy.day, 0, 0)
    fin = datetime(hoy.year, hoy.month, hoy.day, 23, 59)
    ordenes_trabajo = Pedidos_Crm.objects.filter(preprogramado=True, fecha_registro__gte=inicio, fecha_registro__lte=fin)
    for orden in ordenes_trabajo:
        time_orden = orden.fecha_registro - timedelta(hours=1)
        if ahora >= time_orden:
            if ahora < orden.fecha_registro:
                player_ids = []
                tiempo_restante = orden.fecha_registro - ahora
                venta = VentasDocumento.objects.get(folio=orden.folio)
                nombre_cliente = venta.cliente.nombre.encode('UTF-8')
                print 'Orden de trabajo preprogramada de ' + nombre_cliente + ' faltan ' + formato_tiempo(tiempo_restante) + ' '
                content = {'en': 'Orden de trabajo preprogramada de ' + nombre_cliente + ' faltan ' + formato_tiempo(tiempo_restante) + ' ', 'es': 'Orden de trabajo preprogramada de ' + nombre_cliente + ' faltan ' + formato_tiempo(tiempo_restante) + ' '}
                if venta.vendedor:
                    headings = {'en': 'Recordatorio', 'es': 'Recordatorio'}
                    usuarios = Usuario_notificacion.objects.filter(vendedor=venta.vendedor).values_list('id_onesignal')
                else:
                    headings = {'en': 'Recordatorio(orden no asignada)', 'es': 'Recordatorio(orden no asignada)'}
                    usuarios = Usuario_notificacion.objects.all().values_list('id_onesignal')
                print headings
                for usuario in usuarios:
                    player_ids.append(str(usuario[0]))

                url = 'http://sic.no-ip.org:8001/pedidos/pedido/' + str(orden.id) + '/'
                print url
                push = send_push_notification(content=content, headings=headings, url=url, player_ids=player_ids)
                print push.status_code
                print push.json()

    return HttpResponse()