# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_reorden\djmicrosip_reorden\views.py
# Compiled at: 2016-02-03 18:00:54
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core import management
from django.db import connections, router
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from microsip_api.comun.sic_db import first_or_none
import json
from datetime import datetime
from django.conf import settings
if 'djmicrosip_tareas' in settings.EXTRA_MODULES:
    from djmicrosip_tareas.models import ProgrammedTask
    from djmicrosip_tareas.models import PendingTask

@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_reorden/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def preferencias_view(request, template_name='djmicrosip_reorden/preferencias.html'):
    c = {'errors': []}
    almacenes_ids = []
    almacenes_ids_str = Registry.objects.get(nombre='SIC_REORDEN_almacenes_id').get_value()
    if almacenes_ids_str:
        almacenes_ids = almacenes_ids_str.split(',')
    almacenes = Almacen.objects.filter(ALMACEN_ID__in=almacenes_ids)
    if 'djmicrosip_tareas' in settings.EXTRA_MODULES:
        from djmicrosip_tareas.models import ProgrammedTask
        form_initial = {'almacenes': almacenes, 'estatus': Registry.objects.get(nombre='SIC_REORDEN_estatus').get_value(), 
           'nivel': Registry.objects.get(nombre='SIC_REORDEN_nivel').get_value()}
        task = first_or_none(ProgrammedTask.objects.filter(description='Generacion de Ordenes de Compra')) or ProgrammedTask()
        form = ProgrammedTaskForm(request.POST or None, initial=form_initial, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            if not task.id:
                task.description = 'Generacion de Pedido por Ventas'
                task.command_type = 'http'
                task.command = 'http://127.0.0.1:8001/reorden/generar_auto/'
            form.save()
            c['msg'] = 'Informacion actualizada'
        c['form'] = form
    else:
        c['errors'].append('Por favor instalarla para poder configurar esta opción')
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def UpdateDatabaseTable(request):
    if request.user.is_superuser:
        using = router.db_for_write(Registry)
        management.call_command('syncdb', database=using, interactive=False)
        from custom_db import sql_queries
        c = connections[using].cursor()
        for query in sql_queries.triggers_activate:
            c.execute(sql_queries.triggers_activate[query])

        c.close()
        from config import configuration_registers
        for register in configuration_registers:
            padre = first_or_none(Registry.objects.filter(nombre='PreferenciasEmpresa'))
            if padre:
                if not Registry.objects.filter(nombre=register).exists():
                    Registry.objects.create(nombre=register, tipo='V', padre=padre, valor='')

        using = router.db_for_write(Articulo)
        c.execute('grant ALL ON sic_pendingtask TO USUARIO_MICROSIP;')
        management.call_command('syncdb', database=using, interactive=False)
    return HttpResponseRedirect('/reorden/preferencias/')


@permission_required('reorden.can_view_generate_url', login_url='/')
@login_required(login_url='/login/')
def genera_view(request, template_name='djmicrosip_reorden/generar.html'):
    msg = None
    proveedores = []
    articulos_dic = {}
    almacen_id = 0
    form = GeneraOrdenForm(request.POST or None)
    if form.is_valid():
        almacen_id = form.cleaned_data['almacen'].ALMACEN_ID
        nivel = form.cleaned_data['nivel']
        estatus = form.cleaned_data['estatus']
        msg = 'a'
        proveedores, articulos_dic = get_articulos_pedido(almacen_id, nivel, estatus)
    context = {'msg': msg, 'form': form, 
       'articulos_dic': articulos_dic, 
       'proveedores': proveedores, 
       'almacen_id': almacen_id}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def get_articulos_pedido(almacen_id, nivel, estatus):
    articulos_dic = {}
    proveedores = []
    row = []
    using = router.db_for_write(Articulo)
    c = connections[using].cursor()
    articulos = Articulo.objects.filter(seguimiento='N', estatus='A', es_almacenable='S')
    for articulo in articulos:
        query = "select * from sugcom_alms_art(%s,%s,'%s','%s')" % (articulo.id, almacen_id, estatus, nivel)
        c.execute(query)
        result = c.fetchall()
        if result:
            row = result[0]
            if row[6] > 0:
                row = (
                 articulo,) + row
            c.execute('select first 1 pr.proveedor_id,pr.nombre from precios_compra pc\n                join precios_compra_det pcd  on pcd.precio_compra_id = pc.precio_compra_id\n                join proveedores pr on pr.proveedor_id = pc.proveedor_id\n                where pc.articulo_id = %s\n                order by pc.fecha_hora_creacion desc' % articulo.id)
            proveedor = c.fetchall()
            if proveedor:
                row += (proveedor[0][1], proveedor[0][0])
                if proveedor[0][1] not in articulos_dic:
                    articulos_dic[proveedor[0][1]] = []
                articulos_dic[proveedor[0][1]].append(row)
            else:
                row += ('', '')
                if 'Sin Proveedor' not in articulos_dic:
                    articulos_dic['Sin Proveedor'] = []
                articulos_dic['Sin Proveedor'].append(row)
            c.close()
            proveedores = Proveedor.objects.filter(nombre__in=articulos_dic.keys)

    return (
     proveedores, articulos_dic)


def crea_documento_function(proveedor_id, almacen_id, detalles, request):
    proveedor = Proveedor.objects.get(id=proveedor_id)
    almacen = Almacen.objects.get(ALMACEN_ID=almacen_id)
    documento = ComprasDocumento.objects.create(tipo='O', subtipo='N', proveedor=proveedor, almacen=almacen, tipo_cambio=1, condicion_pago=proveedor.condicion_de_pago, descripcion='APLICACION REORDEN', importe_neto=0, estado='P', usuario_creador=request.user.username)
    for detalle in detalles:
        articulo = Articulo.objects.get(id=detalle['articulo_id'])
        clave_articulo = first_or_none(ArticuloClave.objects.filter(articulo=articulo))
        if clave_articulo:
            clave_articulo = clave_articulo.clave
        else:
            clave_articulo = ''
        unidades = detalle['unidades']
        ComprasDocumentoDetalle.objects.create(documento=documento, clave_articulo=clave_articulo, articulo=articulo, unidades=unidades, precio_unitario=articulo.costo_ultima_compra, precio_total_neto=articulo.costo_ultima_compra * unidades, posicion=-1)

    using = router.db_for_write(Articulo)
    c = connections[using].cursor()
    c.execute("execute procedure CALC_TOTALES_DOCTO_CM(%s, 'N')" % documento.id)
    c.close()
    management.call_command('syncdb', database=using, interactive=False)


def crea_documento_view(request):
    proveedor_id = request.GET['proveedor']
    almacen_id = request.GET['almacen_id']
    detalles = json.loads(request.GET['detalles'])
    crea_documento_function(proveedor_id, almacen_id, detalles, request)
    data = json.dumps({})
    return HttpResponse(data, mimetype='application/json')


def genera_auto_view(request):
    almacenes_ids = []
    almacenes_ids_str = Registry.objects.get(nombre='SIC_REORDEN_almacenes_id').get_value()
    if almacenes_ids_str:
        almacenes_ids = almacenes_ids_str.split(',')
    almacenes = Almacen.objects.filter(ALMACEN_ID__in=almacenes_ids)
    for almacen in almacenes:
        nivel = Registry.objects.get(nombre='SIC_REORDEN_nivel').get_value()
        estatus = Registry.objects.get(nombre='SIC_REORDEN_estatus').get_value()
        proveedores, articulos_dic = get_articulos_pedido(almacen.ALMACEN_ID, nivel, estatus)
        for proveedor in proveedores:
            detalles = []
            articulos = articulos_dic[proveedor.nombre]
            for articulo in articulos:
                detalles.append({'articulo_id': articulo[0].id, 'unidades': articulo[7]})

            crea_documento_function(proveedor.id, almacen.ALMACEN_ID, detalles, request)

    return HttpResponse()


@login_required(login_url='/login/')
def entradas_automaticas_view(request, template_name='djmicrosip_reorden/entradas_automaticas.html'):
    c = {'errors': []}
    if 'djmicrosip_tareas' in settings.EXTRA_MODULES:
        from djmicrosip_tareas.models import ProgrammedTask
        form_initial = {'empresas': Registry.objects.get(nombre='SIC_REORDEN_empresa').get_value()}
        task = first_or_none(ProgrammedTask.objects.filter(description='Generacion de Entradas por Remisiones')) or ProgrammedTask()
        form = ProgrammedTaskInForm(request.POST or None, initial=form_initial, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            if not task.id:
                task.description = 'Generacion de Entradas por Remisiones'
                task.command_type = 'http'
                task.command = 'http://127.0.0.1:8001/reorden/generar_entradas/'
            form.save()
            c['msg'] = 'Informacion actualizada'
        c['form'] = form
    else:
        c['errors'].append('Por favor instalarla para poder configurar esta opción')
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def generaentrada_view(request):
    using = router.db_for_write(Registry)
    c = connections[using].cursor()
    empresa = Registry.objects.get(nombre='SIC_REORDEN_empresa').get_value()
    almacen_nombre = 'ALMACEN CEDIS'
    pendientes = PendingTask.objects.filter(app='REORDEN')
    for pendiente in pendientes:
        try:
            dic = json.loads(pendiente.parameters)
            folio = dic['FOLIO']
            tipo = dic['TIPO_DOCUMENTO']
            movto = dic['MOVTO']
            if movto == 'I':
                documento = first_or_none(VentasDocumento.objects.filter(tipo=tipo, folio=folio))
                detalles = VentasDocumentoDetalle.objects.filter(documento=documento)
                query = 'select la.valor_desplegado from libres_rem_ve dp join\n                    listas_atributos la on la.lista_atrib_id = dp.almacen\n                    where dp.docto_ve_id = %s' % documento.id
                c.execute(query)
                almacen_nombre = c.fetchall()[0][0]
                c.close()
                almacen = Almacen.objects.using(empresa).get(nombre=almacen_nombre)
                concepto = InventariosConcepto.objects.using(empresa).get(nombre_abrev='ENTRADA CEDIS')
                entrada = InventariosDocumento.objects.using(empresa).create(id=None, almacen=almacen, descripcion='Remision Cedis: ' + documento.folio, concepto=concepto, naturaleza_concepto='E', fecha=documento.fecha, cancelado='N', aplicado='S', forma_emitida='N', sistema_origen='IN')
                for detalle in detalles:
                    articulo = first_or_none(Articulo.objects.using(empresa).filter(nombre=detalle.articulo.nombre))
                    InventariosDocumentoDetalle.objects.using(empresa).create(id=None, doctosIn=entrada, almacen=almacen, concepto=concepto, claveArticulo=detalle.articulo_clave, articulo=articulo, tipo_movto='E', unidades=detalle.unidades, costo_unitario=detalle.precio_unitario, costo_total=detalle.unidades * detalle.precio_unitario, fecha=documento.fecha)

                c2 = connections[empresa].cursor()
                query = 'EXECUTE PROCEDURE aplica_docto_in(%s); ' % entrada.id
                c2.execute(query)
                c2.close()
            elif movto == 'C':
                documento = first_or_none(InventariosDocumento.objects.using(empresa).filter(naturaleza_concepto='E', descripcion__contains=folio))
                if documento:
                    documento.cancelado = 'S'
                    documento.save(using=empresa)
        except Exception as e:
            pendiente.intents = pendiente.intents + 1
            pendiente.save()
        else:
            pendiente.delete()

    return HttpResponse()


def salidas_automaticas_view(request, template_name='djmicrosip_reorden/salidas_automaticas.html'):
    c = {'errors': []}
    if 'djmicrosip_tareas' in settings.EXTRA_MODULES:
        from djmicrosip_tareas.models import ProgrammedTask
        form_initial = {'empresas': Registry.objects.get(nombre='SIC_REORDEN_empresa').get_value()}
        task = first_or_none(ProgrammedTask.objects.filter(description='Reorden Entradas Automaticas')) or ProgrammedTask()
        form = ProgrammedTaskOutForm(request.POST or None, initial=form_initial, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            if not task.id:
                task.description = 'Generacion de Pedidos por Ventas'
                task.command_type = 'http'
                task.command = 'http://127.0.0.1:8001/reorden/generar_pedido/'
            form.save()
            c['msg'] = 'Informacion actualizada'
        c['form'] = form
    else:
        c['errors'].append('Por favor instalarla para poder configurar esta opción')
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def generapedido_view(request, template_name='djmicrosip_reorden/pedidos.html'):
    lista = []
    using = router.db_for_write(Registry)
    c = connections[using].cursor()
    query = 'select distinct articulo_id from doctos_pv_det dpd join\n        doctos_pv dp on dp.docto_pv_id = dpd.docto_pv_id\n        where dp.fecha = current_date'
    c.execute(query)
    articulos_ids = c.fetchall()
    articulos_ids = map(lambda x: x[0], articulos_ids)
    c.close()
    articulos = Articulo.objects.filter(id__in=articulos_ids)
    almacen = first_or_none(Almacen.objects.filter(nombre='ALMACEN CEDIS'))
    almacen_desc = first_or_none(Almacen.objects.filter(es_predet='S'))
    if almacen_desc:
        almacen_desc = almacen_desc.nombre
    for articulo in articulos:
        query = "SELECT articulo_id,venta_unid as unidades\n            FROM orsp_pv_ventas_art(%s,current_date,current_date,'N','N');" % articulo.id
        c.execute(query)
        result = c.fetchall()
        lista.append(result[0])

    if len(lista) > 0:
        cliente_id = Registry.objects.get(nombre='CLIENTE_EVENTUAL_PV_ID').get_value()
        cliente = Cliente.objects.get(id=cliente_id)
        cliente_clave = ClienteClave.objects.get(rol__es_ppal='S', cliente=cliente)
        cliente_direccion = ClienteDireccion.objects.get(es_ppal='S', cliente=cliente)
        moneda = Moneda.objects.get(es_moneda_local='S')
        condicion_pago = cliente.condicion_de_pago
        if not VentasDocumento.objects.filter(descripcion__contains='Pedido Ventas diarias de', fecha=datetime.now()).exists():
            pedido = VentasDocumento.objects.create(tipo='P', subtipo='N', fecha=datetime.now(), cliente=cliente, cliente_clave=cliente_clave, cliente_direccion=cliente_direccion, direccion_consignatario=cliente_direccion, almacen=almacen, moneda=moneda, estado='N', aplicado='S', descripcion='Pedido Ventas diarias de ' + almacen_desc, sistema_origen='VE', condicion_pago=condicion_pago, modalidad_facturacion=None)
            for detalle in lista:
                articulo = Articulo.objects.get(id=detalle[0])
                articulo_clave = first_or_none(ArticuloClave.objects.filter(rol__es_ppal='S', articulo=articulo))
                if articulo_clave:
                    articulo_clave = articulo_clave.clave
                unidades = detalle[1]
                query = 'select precio_unitario from get_precio_art(%s,43,0,current_date,43);' % articulo.id
                c.execute(query)
                precio_unitario = c.fetchall()[0][0]
                c.close()
                if unidades > 0:
                    VentasDocumentoDetalle.objects.create(documento=pedido, articulo_clave=articulo_clave, articulo=articulo, unidades=unidades, unidades_comprometidas=0, unidades_surtidas_devueltas=0, unidades_a_surtir=0, precio_unitario=precio_unitario, precio_total_neto=unidades * precio_unitario)

            query = 'EXECUTE PROCEDURE aplica_docto_ve(%s); ' % pedido.id
            c.execute(query)
            c.close()
            query = "execute procedure calc_totales_docto_ve(%s,'N'); " % pedido.id
            c.execute(query)
            c.close()
            management.call_command('syncdb', database=using, interactive=False)
    return render_to_response(template_name, {}, context_instance=RequestContext(request))