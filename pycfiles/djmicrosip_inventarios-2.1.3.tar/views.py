# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_inventarios\djmicrosip_inventarios\views.py
# Compiled at: 2019-11-21 18:58:38
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from microsip_api.comun.sic_db import next_id, get_existencias_articulo, first_or_none, runsql_rows
from microsip_api.comun.comun_functions import split_seq, split_letranumero
from django.db import router
from .models import *
import datetime
from . import app_label
from . import config

@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_inventarios/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def ayuda(request, template_name='djmicrosip_inventarios/ayuda.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


def ajustar_existencias(**kwargs):
    """ Para ajustar un articulo a las unidades indicadas sin importar su existencia actual """
    articulo_id = kwargs.get('articulo_id', None)
    ajustar_a = kwargs.get('ajustar_a', None)
    connection_name = kwargs.get('connection_name', None)
    inv_fin = get_existencias_articulo(articulo_id=articulo_id, connection_name=connection_name, fecha_inicio=datetime.datetime.now().strftime('01/01/%Y'), almacen=almacen)
    unidades_a_insertar = -inv_fin + ajustar_a
    return unidades_a_insertar


def add_articulos_sincontar(**kwargs):
    """ Agrega articulos almacenables de la linea indicada faltantes en los documentos de ajustes indicados.
    - Se INGORAN articulos importados
    """
    request_username = kwargs.get('request_username', None)
    using = router.db_for_write(Almacen)
    linea = kwargs.get('linea', None)
    loginventario = kwargs.get('loginventario', None)
    almacen = loginventario.almacen
    message = ''
    sql = ' select distinct articulo_id from sic_loginventario_detalle where log_inventario_id = %s order by fechahora desc' % loginventario.id
    articulos_endocumentos = map(lambda elemento: elemento[0], runsql_rows(sql, using))
    print sql
    inventario_descripcion = ''
    if linea:
        if InventariosDocumentoIF.objects.filter(descripcion='ARTICULOS SIN CONTAR', aplicado='N', almacen=almacen).exists():
            message = 'Ya se genero anteriormente un documento con articulos sin contar de todos los articulos, OPERACION RECHAZADA!!'
            return {'articulos_agregados': 0, 'articulo_pendientes': 0, 'message': message}
        inventario_descripcion = 'ARTICULOS SIN CONTAR LINEA(%s)' % linea.nombre
        articulos_all = list(set(Articulo.objects.exclude(estatus='B', es_importado='S').filter(es_almacenable='S', linea=linea).order_by('-id').values_list('id', flat=True)))
    else:
        inventario_descripcion = 'ARTICULOS SIN CONTAR'
        articulos_all = list(set(Articulo.objects.exclude(estatus='B', es_importado='S').filter(es_almacenable='S').order_by('-id').values_list('id', flat=True)))
    inventarios_fisicos = InventariosDocumentoIF.objects.filter(descripcion__contains=inventario_descripcion, aplicado='N', almacen=almacen)
    for inventario_fisico in inventarios_fisicos:
        articulos_endocumentosinv = list(set(InventariosDocumentoIFDetalle.objects.filter(docto_invfis=inventario_fisico).order_by('-articulo').values_list('articulo__id', flat=True)))
        articulos_endocumentos = articulos_endocumentos + articulos_endocumentosinv

    articulos_sincontar = [ n for n in articulos_all if n not in articulos_endocumentos ]
    articulos_sincontar_con_existencia = list(articulos_sincontar)
    for articulo_id in articulos_sincontar:
        articulo = Articulo.objects.get(pk=articulo_id)
        articulo_existencia = articulo.get_existencia(almacen_nombre=almacen.nombre)
        if articulo_existencia == 0:
            articulos_sincontar_con_existencia.remove(articulo_id)

    articulos_sincontar = articulos_sincontar_con_existencia
    total_articulos_sincontar = len(articulos_sincontar_con_existencia)
    articulos_sincontar_con_existencia = articulos_sincontar_con_existencia[0:9000]
    articulos_sincontar_list = split_seq(articulos_sincontar_con_existencia, 2000)
    articulos_agregados = 0
    ultimofolio = Registry.objects.filter(nombre='SIG_FOLIO_INVFIS')
    if total_articulos_sincontar <= 0:
        message = 'No hay articulos por agregar!!'
        return {'articulos_agregados': 0, 'articulo_pendientes': 0, 'message': message}
    else:
        if not ultimofolio.exists():
            message = 'Para poder crear un inventario es nesesario Asignarles folios automaticos a los inventarios fisicos, OPERACION RECHAZADA!!'
            return {'articulos_agregados': 0, 'articulo_pendientes': 0, 'message': message}
        inventario = InventariosDocumentoIF.objects.create(id=next_id('ID_DOCTOS', using), folio=inventario_getnew_folio(), fecha=datetime.datetime.now(), almacen=almacen, descripcion=inventario_descripcion, usuario_creador=request_username, usuario_aut_creacion='SYSDBA', usuario_ult_modif=request_username, usuario_aut_modif='SYSDBA')
        for articulos_sincontar_sublist in articulos_sincontar_list:
            detalles_en_ceros = 0
            for articulo_id in articulos_sincontar_sublist:
                articulo = Articulo.objects.get(pk=articulo_id)
                InventariosDocumentoIFDetalle.objects.create(id=-1, docto_invfis=inventario, clave=first_or_none(ArticuloClave.objects.filter(articulo=articulo)), articulo=articulo, unidades=0)
                detalles_en_ceros = detalles_en_ceros + 1

            articulos_agregados = articulos_agregados + detalles_en_ceros

        articulos_pendientes = total_articulos_sincontar - articulos_agregados
        return {'articulos_agregados': articulos_agregados, 'articulo_pendientes': articulos_pendientes, 'message': message}


def inventario_getnew_folio():
    registro_folioinventario = Registry.objects.get(nombre='SIG_FOLIO_INVFIS')
    folio = registro_folioinventario.valor
    serie, consecutivo = split_letranumero(folio)
    consecutivo = int(consecutivo) + 1
    siguiente_folio = '%s%s' % (serie, ('%09d' % consecutivo)[len(serie):])
    registro_folioinventario.valor = siguiente_folio
    registro_folioinventario.save()
    return folio


def close_inventario_byalmacen_view(request):
    """ Para agregar existencia a un articulo por ajuste"""
    almacen_id = request.GET['almacen_id']
    almacen = Almacen.objects.get(pk=almacen_id)
    almacen.inventariando = False
    almacen.inventario_conajustes = False
    almacen.inventario_modifcostos = False
    almacen.save()
    loginventario = first_or_none(LogInventario.objects.filter(apertura_fechahora__lte=datetime.datetime.now(), almacen=almacen, cierre_fechahora=None))
    if loginventario:
        loginventario.cierre_fechahora = datetime.datetime.now()
        loginventario.save(update_fields=['cierre_fechahora'])
    InventariosDocumento.objects.filter(almacen__ALMACEN_ID=almacen_id, descripcion='ES INVENTARIO', fechahora_creacion__gte=loginventario.apertura_fechahora).update(descripcion='INVENTARIO CERRADO', sistema_origen='IN')
    data = json.dumps({'mensaje': 'Inventario cerrado'})
    return HttpResponse(data, mimetype='application/json')


def getlogs_ini(request):
    """ Para agregar existencia a un articulo por ajuste"""
    almacen_id = request.GET['almacen_id']
    almacen = Almacen.objects.get(pk=almacen_id)
    loginventario = first_or_none(LogInventario.objects.filter(apertura_fechahora__lte=datetime.datetime.now(), almacen=almacen, cierre_fechahora=None))
    logsinventariodetallearticulos = LogInventarioValorInicial.objects.filter(log_inventario=loginventario).values_list('id', flat=True)
    logsinventariodetallearticulos = map(str, logsinventariodetallearticulos)
    data = json.dumps({'logs_ini_ids': logsinventariodetallearticulos})
    return HttpResponse(data, mimetype='application/json')


def setlogs_ini(request):
    """ Para guardar las existencias finales"""
    id = request.GET['id']
    logsinventario_valor_inicial = LogInventarioValorInicial.objects.get(id=id)
    almacen = logsinventario_valor_inicial.log_inventario.almacen
    existencia_final = logsinventario_valor_inicial.articulo.get_existencia(almacen_nombre=almacen.nombre)
    logsinventario_valor_inicial.existencia_final = existencia_final
    logsinventario_valor_inicial.save(update_fields=['existencia_final'])
    data = json.dumps({})
    return HttpResponse(data, mimetype='application/json')


def add_articulossinexistencia(request):
    """ Agrega articulos almacenables de la linea indicada faltantes en los documentos de ajustes indicados.  """
    connection_name = router.db_for_write(Almacen)
    almacen_id = request.GET['almacen_id']
    almacen = Almacen.objects.get(pk=almacen_id)
    loginventario = first_or_none(LogInventario.objects.filter(apertura_fechahora__lte=datetime.datetime.now(), almacen=almacen, cierre_fechahora=None))
    result = add_articulos_sincontar(request_username=request.user.username, connection_name=connection_name, loginventario=loginventario)
    data = json.dumps(result)
    return HttpResponse(data, mimetype='application/json')


def add_articulossinexistencia_bylinea(request):
    """ Agrega articulos almacenables de la linea indicada faltantes en los documentos de ajustes indicados.  """
    connection_name = router.db_for_write(Almacen)
    ubicacion = request.GET['ubicacion']
    linea_id = request.GET['linea_id']
    almacen_id = request.GET['almacen_id']
    linea = LineaArticulos.objects.get(pk=linea_id)
    almacen = Almacen.objects.get(pk=almacen_id)
    loginventario = first_or_none(LogInventario.objects.filter(apertura_fechahora__lte=datetime.datetime.now(), almacen=almacen, cierre_fechahora=None))
    result = add_articulos_sincontar(request_username=request.user.username, connection_name=connection_name, ubicacion=ubicacion, linea=linea, loginventario=loginventario)
    data = json.dumps(result)
    return HttpResponse(data, mimetype='application/json')