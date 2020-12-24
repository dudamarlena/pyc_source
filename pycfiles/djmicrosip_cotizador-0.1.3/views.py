# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_cotizador\djmicrosip_cotizador\views.py
# Compiled at: 2015-03-17 17:54:10
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.core import management
from django.db import connections, router
import csv
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.list import ListView
import json

class Children(list):

    def __init__(self, parent):
        self.root = Carpeta.objects.get(id=parent)
        self.get_children(parent)

    def get_children(self, parent):
        children = Carpeta.objects.filter(carpeta_padre=parent)
        if children:
            for child in children:
                self.append(child)
                data_child = self.get_children(child)

    def get_parents(self, child):
        if child.carpeta_padre and child != self.root:
            child = child.carpeta_padre
            self.path_nodes.append(child)
            self.get_parents(child)

    def get_fullpath(self, child_id):
        """
            Regresa el pat completo de una carpeta
        """
        child = Carpeta.objects.get(id=child_id)
        self.path_nodes = [child]
        self.get_parents(child)
        path = ''
        for node in self.path_nodes:
            path = '/%s%s' % (node.nombre, path)

        return path


def get_folder_children(request):
    parent_id = request.GET['parent_id']
    children = list(Carpeta.objects.filter(carpeta_padre__id=parent_id).values_list('id', 'nombre'))
    data = {'children': children}
    return HttpResponse(json.dumps(data), mimetype='application/json')


def get_folderfullpath(request):
    root_id = request.GET['root_id']
    child_id = request.GET['child_id']
    arbol = Children(root_id)
    path = arbol.get_fullpath(child_id)
    data = {'path': path}
    return HttpResponse(json.dumps(data), mimetype='application/json')


def GetNodeStructure(request):
    node_id = request.GET['node_id']
    raiz = Carpeta.objects.get(pk=node_id)
    folders = Children(raiz.id)
    folders.append(raiz)
    data = []
    for folder in folders:
        if folder == raiz:
            parent = '#'
        else:
            parent = folder.carpeta_padre.id
        node = {'id': folder.id, 
           'parent': parent, 
           'text': folder.nombre, 
           'state': {'opened': parent == '#'}}
        data.append(node)

    data = {'data': data}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_cotizador/index.html'):
    context = {}
    error = None
    estructuras = EstructuraCotizacion.objects.all()
    try:
        len(EstructuraCotizacion.objects.all())
    except Exception as e:
        error = 'ini'

    from .config import VERSION
    context = {'estructuras': estructuras, 
       'error': error, 
       'version': 'v' + VERSION}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def updateDatabaseView(request):
    using = router.db_for_write(Articulo)
    management.call_command('syncdb', database=using, interactive=False)
    return HttpResponseRedirect('/cotizador/')


class EstructurasList(ListView):
    template_name = 'djmicrosip_cotizador/estructuras.html'
    context_object_name = 'estructuras'
    paginate_by = 10

    def get_queryset(request):
        return EstructuraCotizacion.objects.all()


def EstructurasManageView(request, id=None, template_name='djmicrosip_cotizador/estructura.html'):
    if id:
        estructura = get_object_or_404(EstructuraCotizacion, pk=id)
    else:
        estructura = EstructuraCotizacion()
    DetalleFormset = EstructuraCotizacionDetalleFormset(DetalleEstructuraCotizacionForm, extra=1, can_delete=True, can_order=True)
    formset = DetalleFormset(request.POST or None, instance=estructura)
    if request.POST:
        form = EstructuraCotizacionForm(request.POST or None, request.FILES, instance=estructura)
    else:
        form = EstructuraCotizacionForm(instance=estructura)
    if form.is_valid() and formset.is_valid():
        estructura = form.save()
        for detalle_form in formset:
            detalle = detalle_form.save(commit=False)
            if not detalle.id:
                detalle.estructura = estructura

        formset.save()
        return HttpResponseRedirect('/cotizador/estructuras/')
    else:
        c = {'form': form, 'formset': formset, 'estructura': estructura}
        return render_to_response(template_name, c, context_instance=RequestContext(request))


def EliminarEstructura(request, id=None):
    data = {}
    id_a = id
    estructura_a_eliminar = EstructuraCotizacion.objects.get(id=id_a)
    estructura_a_eliminar.delete()
    return HttpResponseRedirect('/cotizador/estructuras/')


def EditarEstructura(request, est_id=None, template_name='djmicrosip_cotizador/detalles.html'):
    c = {}
    detalles = DetalleEstructuraCotizacion.objects.filter(estructura__id=est_id)
    estructura_nombre = EstructuraCotizacion.objects.get(id=est_id).nombre
    c = {'detalles': detalles, 
       'estructura_nombre': estructura_nombre, 
       'est_id': est_id}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


def DetallesManageView(request, est_id=None, det_id=None, template_name='djmicrosip_cotizador/detalle.html'):
    if det_id:
        detalle = get_object_or_404(DetalleEstructuraCotizacion, pk=det_id)
    else:
        estructura = EstructuraCotizacion.objects.get(id=est_id)
        detalle = DetalleEstructuraCotizacion(estructura=estructura)
    form = DetalleEstructuraCotizacionForm(request.POST or None, instance=detalle, initial={'est_id': est_id})
    if form.is_valid():
        detalle.save()
        return HttpResponseRedirect('/cotizador/estructuras/')
    else:
        estructura = EstructuraCotizacion.objects.get(id=est_id)
        c = {'form': form, 'detalle': detalle, 'estructura': estructura}
        return render_to_response(template_name, c, context_instance=RequestContext(request))