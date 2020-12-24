# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\apps\plugins\django_microsip_catalogoarticulos\django_microsip_catalogoarticulos\views.py
# Compiled at: 2014-10-24 12:41:32
from microsip_api.comun.sic_db import get_conecctionname, first_or_none
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db import connections, router
from custom_db.procedures import procedures as sql_procedures
from django.db.models.query import QuerySet
from django.core import management
from collections import Counter
from .models import *
from decimal import *
import csv
from django.http import HttpResponse
from django.views.generic.list import ListView
from .forms import *
import json

@login_required(login_url='/login/')
def index(request, template_name='django_microsip_catalogoarticulos/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def ArticulosView(request, template_name='django_microsip_catalogoarticulos/articulos.html'):
    form = ArticuloSearchForm(request.GET)
    if form.is_valid():
        articulo = form.cleaned_data['articulo']
        tags = form.cleaned_data['tag'].split(' ')
        nombre = form.cleaned_data['nombre']
        clave = form.cleaned_data['clave']
        articulos = Articulo.objects.exclude(es_juego='S').order_by('id')
        if nombre:
            articulos = articulos.filter(nombre__contains=nombre)
        if clave:
            claves = ArticuloClave.objects.filter(clave=clave)
            if claves:
                articulos = Articulo.objects.filter(pk=claves[0].articulo.id)
        if articulo:
            articulos = Articulo.objects.filter(pk=articulo.id)
        if tags != ['']:
            articulos = []
            articulos_ids = []
            tagsarticulos = TagArticulo.objects.all()
            for tag in tags:
                tagsarticulos = TagArticulo.objects.filter(tag__tag__contains=tag)
                for tagarticulo in tagsarticulos:
                    articulos_ids.append(tagarticulo.articulo)

            cuentas = Counter(articulos_ids)
            objects.jhv
            for cuenta in cuentas.items():
                if cuenta[1] == len(tags):
                    articulos.append(cuenta[0])

    try:
        res = Tag.objects.all().exists()
    except:
        error = 'Inicializa la Configuracion <a href="/catalogo/inicializar/">Aqui</a>'
        c = {'error': error}
    else:
        p = None
        cliente_eventual = Registry.objects.get(nombre='CLIENTE_EVENTUAL_PV_ID').valor
        if not cliente_eventual:
            cliente_eventual = 1
        articulos_precios = []
        precios = {'original': 0, 'descuento': 0, 'actual': 0, 'ahorro': 0, 'articulo': None}
        p = Paginator(articulos, 24)
        page = request.GET.get('page')
        try:
            articulos = p.page(page)
        except PageNotAnInteger:
            articulos = p.page(1)
        except EmptyPage:
            articulos = p.page(p.num_pages)

        for articulo in articulos:
            precios = {'original': 0, 'descuento': 0, 'actual': 0, 'ahorro': 0, 'articulo': None}
            try:
                precios['original'] = ArticuloPrecio.objects.get(articulo=articulo, precio_empresa__id=42).precio
            except Exception as e:
                precios['original'] = 0
                precios['actual'] = 0
            else:
                precios['descuento'] = articulo.get_descuento_total(cliente_id=cliente_eventual, unidades=1)

            if precios['descuento'] != 0:
                precios['actual'] = precios['original'] - precios['original'] * precios['descuento'] / 100
                precios['ahorro'] = precios['original'] - precios['actual']
                precios['actual'] = '%.2f' % precios['actual']
            else:
                precios['actual'] = '%.2f' % precios['original']
            precios['ahorro'] = '%.2f' % precios['ahorro']
            precios['original'] = '%.2f' % precios['original']
            precios['descuento'] = '%.0f' % precios['descuento']
            precios['articulo'] = articulo
            if precios['original'] != '0.00':
                articulos_precios.append(precios)

        c = {'articulos_precios': articulos_precios, 'articulos': articulos, 'form': form}

    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def ArticuloManageView(request, id=None, template_name='django_microsip_catalogoarticulos/articulo.html'):
    tags = []
    if id:
        articulo = get_object_or_404(Articulo, pk=id)
    else:
        articulo = Articulo()
    if request.POST:
        form = ArticuloForm(request.POST or None, request.FILES, instance=articulo)
    else:
        form = ArticuloForm(instance=articulo)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/catalogo/articulos/')
    else:
        tag_search_form = TagSearchForm()
        tags = TagArticulo.objects.filter(articulo=articulo)
        c = {'form': form, 'Articulo': articulo, 'tag_search_form': tag_search_form, 'tags': tags}
        return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def TagsView(request, template_name='django_microsip_catalogoarticulos/tags.html'):
    tags = Tag.objects.all().order_by('id')
    c = {'tags': tags}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def TagsManageView(request, id=None, template_name='django_microsip_catalogoarticulos/tag.html'):
    if id:
        tag = get_object_or_404(Tag, pk=id)
    else:
        tag = Tag()
    if request.POST:
        form = TagForm(request.POST or None, instance=tag)
    else:
        form = TagForm(instance=tag)
    if form.is_valid():
        tag.save()
        return HttpResponseRedirect('/catalogo/tags/')
    else:
        c = {'form': form, 'Tag': tag}
        return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def AgregarTagArticulo(request):
    tag_id = request.GET['tag_id']
    articulo_id = request.GET['articulo_id']
    tag = Tag.objects.get(id=tag_id)
    articulo = Articulo.objects.get(id=articulo_id)
    tagarticulo = TagArticulo(tag=tag, articulo=articulo)
    tagarticulo.save()
    tagarticulo = TagArticulo.objects.get(tag=tag, articulo=articulo)
    data = {'tag_id': tag_id, 
       'articulo_id': articulo_id, 
       'tag_name': tag.tag, 
       'tagarticulo': tagarticulo.id}
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')


@login_required(login_url='/login/')
def EliminarTagArticulo(request):
    tag_id = request.GET['tag_id']
    tag_name = request.GET['tag_name']
    a_eliminar = TagArticulo.objects.filter(id=tag_id)
    TagArticulo.objects.filter(id=tag_id).delete()
    data = {'tag_id': tag_id}
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')


@login_required(login_url='/login/')
def UpdateDatabaseTable(request):
    """ Agrega campos nuevos en tablas de base de datos. """
    if request.user.is_superuser:
        using = router.db_for_write(Articulo)
        c = connections[using].cursor()
        c.execute(sql_procedures['SIC_ARTICULOS_CATALOGO'])
        c.execute('EXECUTE PROCEDURE SIC_ARTICULOS_CATALOGO;')
        c.execute('DROP PROCEDURE SIC_ARTICULOS_CATALOGO;')
        c.close()
        management.call_command('syncdb', database=using, interactive=False)
    return HttpResponseRedirect('/catalogo/')