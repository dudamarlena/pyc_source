# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_organizador\djmicrosip_organizador\views.py
# Compiled at: 2015-03-11 16:55:15
from .forms import *
from .models import *
from collections import Counter
from custom_db.procedures import procedures as sql_procedures
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core import management
from django.core.paginator import Paginator
from django.db import router, connections
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.list import ListView
from microsip_api.comun.sic_db import get_existencias_articulo, next_id, first_or_none
import csv, json

@login_required(login_url='/login/')
def updateDatabaseView(request):
    return HttpResponseRedirect('/organizador/')


def saveSearchOptions(request):
    busqueda_anidada = request.GET['busqueda_anidada']
    data = {}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_organizador/index.html'):
    c = {}
    raiz = Carpeta.objects.filter(nombre='/')
    if not raiz:
        pass
    return render_to_response(template_name, c, context_instance=RequestContext(request))


class Children(list):

    def __init__(self, parent):
        self.get_children(parent)

    def get_children(self, parent):
        children = Carpeta.objects.filter(carpeta_padre=parent)
        if children:
            for child in children:
                self.append(child)
                data_child = self.get_children(child)


def structure_lineas():
    raiz = Carpeta.objects.create(nombre='/', carpeta_padre=None)
    grupos = GrupoLineas.objects.all()
    if grupos:
        for grupo in grupos:
            nombre = grupo.nombre
            carpeta_grupo = Carpeta.objects.create(nombre=grupo.nombre, carpeta_padre=raiz)
            lineas = LineaArticulos.objects.filter(grupo=grupo)
            for linea in lineas:
                carpeta_linea = Carpeta.objects.create(nombre=linea.nombre, carpeta_padre=carpeta_grupo)

    else:
        lineas = LineaArticulos.objects.all()
        for linea in lineas:
            carpeta_linea = Carpeta.objects.create(nombre=linea.nombre, carpeta_padre=raiz)

        articulos = Articulo.objects.filter(linea=None)
        for articulo in articulos:
            articulo.carpeta = raiz
            articulo.save()

    return


def get_estructura_carpetas(request):
    ids = []
    raiz = Carpeta.objects.filter(nombre='/')
    if not raiz:
        structure_lineas()
        ids = list(Articulo.objects.exclude(linea=None).values_list('id', flat=True))
    raiz = Carpeta.objects.get(nombre='/')
    folders = Children(raiz)
    folders.append(raiz)
    data = []
    for folder in folders:
        if not folder.carpeta_padre:
            parent = '#'
        else:
            parent = folder.carpeta_padre.id
        node = {'id': folder.id, 
           'parent': parent, 
           'text': folder.nombre}
        data.append(node)

    data = {'data': data, 'ids': ids}
    return HttpResponse(json.dumps(data), mimetype='application/json')


def set_article_in_folder(request):
    articulos_ids = request.GET.getlist('articulos_ids')[0].split(',')
    articulos_ids = map(lambda id: int(id), articulos_ids)
    for articulo_id in articulos_ids:
        articulo = Articulo.objects.get(id=articulo_id)
        linea = articulo.linea
        carpeta_linea = first_or_none(Carpeta.objects.filter(nombre=linea.nombre))
        articulo.carpeta = carpeta_linea
        articulo.save()

    data = {'result': 1}
    return HttpResponse(json.dumps(data), mimetype='application/json')


class ArticuloListView(ListView):
    context_object_name = 'articulos'
    model = Articulo
    template_name = 'djmicrosip_organizador/articulos.html'
    paginate_by = 5

    def get_queryset(self):
        return Articulo.objects.all().order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super(ArticuloListView, self).get_context_data(**kwargs)
        context['form'] = TagSearchForm(self.request.GET or None)
        return context


@login_required(login_url='/login/')
def ArticuloManageView(request, id=None, template_name='djmicrosip_organizador/articulos/articulo.html'):
    """ Modificacion de tags de articulo"""
    if id:
        articulo = get_object_or_404(Articulo, pk=id)
    else:
        articulo = Articulo()
    tags_items = articulotags_formset(ArticuloForm, extra=1, can_delete=True)
    Tagarticuloformset = tags_items(request.POST or None, instance=articulo)
    if Tagarticuloformset.is_valid():
        Tagarticuloformset.save()
    c = {'formset': Tagarticuloformset, 'articulo_nombre': articulo.nombre}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


class TagListView(ListView):
    context_object_name = 'tags'
    model = Tag
    template_name = 'djmicrosip_organizador/tags/tags.html'
    paginate_by = 100

    def get_queryset(self):
        return Tag.objects.all().order_by('tag')


def EliminarTag(request, id=None):
    data = {}
    id_a = id
    tag_a_eliminar = Tag.objects.get(id=id_a)
    tag_a_eliminar.delete()
    return HttpResponseRedirect('/organizador/tags/')


def agregar_tag_articulo(request):
    tag_id = request.GET['tag_id']
    articles_ids = request.GET['articulos_ids'].split(',')
    tag = Tag.objects.get(id=tag_id)
    for article_id in articles_ids:
        article = Articulo.objects.get(id=article_id)
        if not TagArticulo.objects.filter(tag=tag, articulo=article).exists():
            TagArticulo.objects.create(tag=tag, articulo=article)

    data = {}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/login/')
def TagsManageView(request, id=None, template_name='djmicrosip_organizador/tags/tag.html'):
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
        return HttpResponseRedirect('/organizador/tags/')
    else:
        c = {'form': form, 'Tag': tag}
        return render_to_response(template_name, c, context_instance=RequestContext(request))


def move_articles(request):
    article_id = request.GET['value']
    selected = request.GET['selected']
    folder = Carpeta.objects.get(id=selected)
    article = Articulo.objects.get(id=article_id)
    article.carpeta = folder
    article.save()
    data = {}
    return HttpResponse(json.dumps(data), mimetype='application/json')


def get_articles_in_folder_all(request):
    cliente_eventual = Registry.objects.get(nombre='CLIENTE_EVENTUAL_PV_ID').valor
    using = router.db_for_write(Articulo)
    data = []
    articulos_lista = []
    articulos = []
    page = request.GET['page']
    search_text = request.GET['search_text']
    carpeta_id = request.GET['selected']
    busqueda_anidada = request.GET['busqueda_anidada'] == 'true'
    tags = search_text.split(',')
    tags = map(lambda tag: tag.rstrip().lstrip(), tags)
    padre = Carpeta.objects.get(id=carpeta_id)
    folders = []
    if busqueda_anidada:
        folders = Children(padre)
    folders.append(padre)
    if tags != ['']:
        for tag in tags:
            tagsarticulos = list(Articulo.objects.filter(Q(tagarticulo__tag__tag__contains=tag) | Q(nombre__icontains=tag), carpeta__in=folders).order_by('nombre').values_list('id', 'nombre'))
            for tagarticulo in tagsarticulos:
                articulos_lista.append(tagarticulo)

        cuentas = Counter(articulos_lista)
        articulos_lista = []
        for cuenta in cuentas.items():
            if cuenta[1] >= len(tags):
                articulos_lista.append(cuenta[0])

    data = []
    for a in articulos_lista:
        articulo_id = a[0]
        articulo = Articulo.objects.get(id=articulo_id)
        existencia = get_existencias_articulo(articulo_id=articulo_id, connection_name=using, fecha_inicio=datetime.now().strftime('01/01/%Y'), almacen='CONSOLIDADO')
        try:
            precio = ArticuloPrecio.objects.get(articulo=articulo, precio_empresa__id=42).precio
        except Exception as e:
            precio = 0

        a += ('%.2f' % precio,)
        a += (str(existencia),)
        data.append(a)

    articulos_lista = []
    p = Paginator(data, 50)
    num_pages = p.num_pages
    if num_pages < int(page):
        data = None
    else:
        page1 = p.page(page)
        data = page1.object_list
    data = {'data': data, 
       'pages': num_pages}
    return HttpResponse(json.dumps(data), mimetype='application/json')


def get_articles_in_folder(request):
    using = router.db_for_write(Articulo)
    carpeta_id = request.GET['selected']
    page = request.GET['page']
    data = []
    arts = []
    arts = list(Articulo.objects.filter(carpeta__id=int(carpeta_id)).order_by('nombre').values_list('id', 'nombre'))
    data = arts
    p = Paginator(data, 50)
    num_pages = p.num_pages
    page1 = p.page(page)
    data = page1.object_list
    cuenta = len(data)
    arts = data
    data = []
    for a in arts:
        articulo_id = a[0]
        articulo = Articulo.objects.get(id=articulo_id)
        existencia = get_existencias_articulo(articulo_id=articulo_id, connection_name=using, fecha_inicio=datetime.now().strftime('01/01/%Y'), almacen='CONSOLIDADO')
        try:
            precio = ArticuloPrecio.objects.get(articulo=articulo, precio_empresa__id=42).precio
        except Exception as e:
            precio = 0

        a += ('$ %.2f' % precio,)
        a += (str(existencia),)
        data.append(a)

    data = {'data': data, 
       'pages': num_pages}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/login/')
def articles_search(request, template_name='djmicrosip_organizador/articulos.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


def get_folder_id(request):
    using = router.db_for_write(Articulo)
    folder_id = next_id('SIC_CARPETA_SQ', using)
    data = {'folder_id': folder_id}
    return HttpResponse(json.dumps(data), mimetype='application/json')


def remove_folder(request):
    data = {}
    remove = 1
    folder_id = request.GET['folder_id']
    articles = Articulo.objects.filter(carpeta__id=folder_id)
    folders = Carpeta.objects.filter(carpeta_padre=folder_id)
    if articles or folders:
        remove = 0
    else:
        Carpeta.objects.filter(id=folder_id).delete()
    data = {'remove': remove}
    return HttpResponse(json.dumps(data), mimetype='application/json')


def create_folder(request):
    folder_name = request.GET['folder_name']
    folder_id = int(request.GET['folder_id'])
    parent_id = int(request.GET['parent_id'])
    parent = Carpeta.objects.get(id=parent_id)
    folder = Carpeta.objects.create(id=folder_id, nombre=folder_name, carpeta_padre=parent)
    data = {}
    return HttpResponse(json.dumps(data), mimetype='application/json')


def rename_folder(request):
    folder_name = request.GET['folder_name']
    folder_id = int(request.GET['folder_id'])
    folder = Carpeta.objects.get(id=folder_id)
    folder.nombre = folder_name
    folder.save()
    data = {}
    return HttpResponse(json.dumps(data), mimetype='application/json')


def move_folder(request):
    parent_id = int(request.GET['parent_id'])
    folder_id = int(request.GET['folder_id'])
    folder = Carpeta.objects.get(id=folder_id)
    folder_parent = Carpeta.objects.get(id=parent_id)
    folder.carpeta_padre = folder_parent
    folder.save()
    data = {}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/login/')
def UpdateDatabaseTable(request):
    using = router.db_for_write(Articulo)
    c = connections[using].cursor()
    proc = sql_procedures['SIC_ARTICULOS_ORGANIZADOR']
    c.execute(sql_procedures['SIC_ARTICULOS_ORGANIZADOR'])
    c.execute('EXECUTE PROCEDURE SIC_ARTICULOS_ORGANIZADOR;')
    c.execute('DROP PROCEDURE SIC_ARTICULOS_ORGANIZADOR;')
    c.close()
    management.call_command('syncdb', database=using, interactive=False)
    return HttpResponseRedirect('/organizador/')