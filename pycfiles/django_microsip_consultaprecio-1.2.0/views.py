# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_microsip_consultaprecio\django_microsip_consultaprecio\views.py
# Compiled at: 2017-09-22 14:04:55
from microsip_api.comun.sic_db import get_conecctionname, first_or_none
from django.db import connections
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .models import *
import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from .forms import *
from django.core import management
from django.db import router

@login_required(login_url='/login/')
def index(request, template_name='django_microsip_consultaprecio/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def PrecioArticuloView(request, template_name='django_microsip_consultaprecio/precioarticulo.html'):
    form = ArticuloSearchForm(request.POST or None)
    nombre_empresa = Registry.objects.get(nombre='SIC_ConsultaPrecio_NombreEmpresa').get_value()
    if not nombre_empresa:
        nombre_empresa = ''
    slogan = Registry.objects.get(nombre='SIC_ConsultaPrecio_Slogan').get_value()
    if not slogan:
        slogan = ''
    cliente_eventual = Registry.objects.get(nombre='SIC_ConsultaPrecio_Cliente').valor
    msg = ''
    variable = ''
    articulo = ''
    precio_actual = 0
    descuento = 0
    art = None
    precio_original = 0
    ahorro = 0
    if form.is_valid():
        clave = form.cleaned_data['clave']
        try:
            art = ArticuloClave.objects.get(clave=clave)
            articulo = art.articulo
        except Exception as e:
            msg = 'No se encontro ningun articulo con esa clave.'
        else:
            try:
                articuloprecio = ArticuloPrecio.objects.get(articulo=articulo, precio_empresa__id=42)
                precio_original = articuloprecio.precio
                connection_name = get_conecctionname(request.session)
                c = connections[connection_name].cursor()
                c.execute("execute procedure precio_con_impto(%s,%s,'N','P','S')" % (articulo.id, precio_original))
                variable = c.fetchall()
                precio_original = variable[0][0]
                c.close()
            except Exception as e:
                precio_original = 0

    if articulo:
        descuento = articulo.get_descuento_total(cliente_id=cliente_eventual, unidades=1)
        if descuento != 0:
            precio_actual = precio_original - precio_original * descuento / 100
            ahorro = '%.2f' % (precio_original - precio_actual)
            precio_actual = '%.2f' % precio_actual
        else:
            precio_actual = round(precio_original, 2)
            precio_actual = '%.2f' % precio_original
        precio_original = '%.2f' % precio_original
    imagenes = ImagenSlideChecador.objects.all().order_by('id')
    context = {'Descuento': descuento, 
       'Articulo': articulo, 
       'form': form, 
       'msg': msg, 
       'precio_original': precio_original, 
       'precio_actual': precio_actual, 
       'Ahorro': ahorro, 
       'nombre_empresa': nombre_empresa, 
       'slogan': slogan, 
       'imagenes': imagenes}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def InitialzeConfigurationDatabase(request):
    """ Agrega campos nuevos en tablas de base de datos. """
    padre = first_or_none(Registry.objects.filter(nombre='PreferenciasEmpresa'))
    if request.user.is_superuser and padre:
        if not Registry.objects.filter(nombre='SIC_ConsultaPrecio_NombreEmpresa').exists():
            Registry.objects.create(nombre='SIC_ConsultaPrecio_NombreEmpresa', tipo='V', padre=padre, valor='')
        if not Registry.objects.filter(nombre='SIC_ConsultaPrecio_Slogan').exists():
            Registry.objects.create(nombre='SIC_ConsultaPrecio_Slogan', tipo='V', padre=padre, valor='')
        if not Registry.objects.filter(nombre='SIC_ConsultaPrecio_Cliente').exists():
            Registry.objects.create(nombre='SIC_ConsultaPrecio_Cliente', tipo='V', padre=padre, valor='')
        using = router.db_for_write(Almacen)
        management.call_command('syncdb', database=using, interactive=False)
    return HttpResponseRedirect('/precios/')


@login_required(login_url='/login/')
def PreferenciasManageView(request, template_name='django_microsip_consultaprecio/preferencias.html'):
    msg = ''
    form_initial = {'empresa_nombre': Registry.objects.get(nombre='SIC_ConsultaPrecio_NombreEmpresa').get_value(), 
       'empresa_slogan': Registry.objects.get(nombre='SIC_ConsultaPrecio_Slogan').get_value(), 
       'cliente_eventual': Registry.objects.get(nombre='SIC_ConsultaPrecio_Cliente').get_value()}
    form = PreferenciasManageForm(request.POST or None, initial=form_initial)
    warrning = ''
    if form.is_valid():
        form.save()
        msg = 'Datos guardados correctamente'
    imagenes = ImagenSlideChecador.objects.all().order_by('id')
    c = {'form': form, 
       'msg': msg, 
       'imagenes': imagenes}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def imagen_manageview(request, id=None, template_name='django_microsip_consultaprecio/imagen.html'):
    if id:
        imagen = get_object_or_404(ImagenSlideChecador, pk=id)
    else:
        imagen = ImagenSlideChecador()
    if request.POST:
        form = ImagenManageForm(request.POST or None, request.FILES, instance=imagen)
    else:
        form = ImagenManageForm(instance=imagen)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/precios/preferencias/')
    else:
        c = {'form': form}
        return render_to_response(template_name, c, context_instance=RequestContext(request))


def eliminarimagen(request, id=None):
    imagen_a_eliminar = ImagenSlideChecador.objects.get(id=id)
    imagen_a_eliminar.delete()
    return HttpResponseRedirect('/precios/preferencias/')