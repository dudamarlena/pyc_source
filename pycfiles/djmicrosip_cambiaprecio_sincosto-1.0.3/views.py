# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_cambiaprecio_sincosto\djmicrosip_cambiaprecio_sincosto\views.py
# Compiled at: 2015-07-07 15:52:22
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .models import *
from django.db import connections, router
from .forms import ArticuloSearchForm, ArticuloPrecioForm, ArticuloPrecioCompraForm, ArticuloPrecioFormset
import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django_microsip_base.libs.models_base.models import Articulo, ArticuloClave, ArticuloPrecio, ImpuestosArticulo, Moneda
from django.shortcuts import render_to_response, get_object_or_404
from microsip_api.comun.sic_db import first_or_none, get_existencias_articulo
from datetime import datetime

@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_cambiaprecio_sincosto/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


class ArticuloListView(ListView):
    context_object_name = 'articulos'
    model = Articulo
    template_name = 'djmicrosip_cambiaprecio_sincosto/articulos.html'
    paginate_by = 50

    def dispatch(self, *args, **kwargs):
        return super(ArticuloListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        form = ArticuloSearchForm(self.request.GET)
        if form.is_valid():
            articulo = form.cleaned_data['articulo']
            clave = form.cleaned_data['clave']
            articulos = Articulo.objects.all()
            if clave:
                claves = ArticuloClave.objects.filter(clave=clave)
                if claves:
                    articulos = Articulo.objects.filter(pk=claves[0].articulo.id)
            if articulo:
                articulos = Articulo.objects.filter(pk=articulo.id)
        return articulos

    def get_context_data(self, **kwargs):
        context = super(ArticuloListView, self).get_context_data(**kwargs)
        context['form'] = ArticuloSearchForm(self.request.GET or None)
        return context

    def render_to_response(self, context):
        if len(self.object_list) == 1:
            return HttpResponseRedirect('/cambiaprecionormal/articulo/%s/' % self.object_list[0].id)
        return super(ArticuloListView, self).render_to_response(context)


@login_required(login_url='/login/')
def articulo_manageview(request, id=None, template_name='djmicrosip_cambiaprecio_sincosto/articulo.html'):
    monedas = []
    moneda_local = ''
    tipo_cambio_ultima_compra = 0
    adv_moneda = ''
    articulo = get_object_or_404(Articulo, pk=id)
    impuesto = ImpuestosArticulo.objects.filter(articulo=articulo)
    costo_ultima_compra = articulo.costo_ultima_compra
    precios_articulos = ArticuloPrecio.objects.filter(articulo=articulo)
    for precio_articulo in precios_articulos:
        if precio_articulo.moneda.nombre not in monedas:
            monedas.append(precio_articulo.moneda.nombre)

    if len(monedas) > 1:
        adv_moneda = 'Los precios de lista no son todos de la misma moneda'
    else:
        if monedas:
            moneda = Moneda.objects.get(nombre=monedas[0])
        else:
            moneda = Moneda.objects.get(es_moneda_local='S')
        moneda_local = moneda.es_moneda_local
    using = router.db_for_write(Articulo)
    con = connections[using]
    c = con.cursor()
    c.execute("select first 1 dc.tipo_cambio from doctos_cm dc\n        join doctos_cm_det dcd on dcd.docto_cm_id = dc.docto_cm_id\n        where dcd.articulo_id = %s and dc.tipo_docto ='C'\n        order by dc.fecha desc" % articulo.id)
    try:
        tipo_cambio_ultima_compra = c.fetchall()[0][0]
    except Exception as e:
        pass

    if moneda_local == 'N':
        if tipo_cambio_ultima_compra == 0:
            fecha_ultima_compra = articulo.fecha_ultima_compra
            if fecha_ultima_compra:
                tipo_cambio_ultima_compra = TipoCambio.objects.get(fecha=fecha_ultima_compra, moneda=moneda).tipo_cambio
            else:
                tipo_cambio_ultima_compra = TipoCambio.objects.filter(moneda=moneda).order_by('fecha')[0].tipo_cambio
    if moneda_local == 'N':
        costo_ultima_compra = costo_ultima_compra / tipo_cambio_ultima_compra
    DetalleFormset = ArticuloPrecioFormset(ArticuloPrecioForm, extra=0, can_delete=False, can_order=False)
    formset = DetalleFormset(request.POST or None, instance=articulo)
    if formset.is_valid():
        formset.save()
        return HttpResponseRedirect('/cambiaprecionormal/articulos/')
    else:
        con = connections[using]
        c = con.cursor()
        c.execute('select first 5 pc.fecha_precio_ult_compra,pr.nombre,pcd.precio_uven,m.nombre from precios_compra pc\n        join precios_compra_det pcd  on pcd.precio_compra_id = pc.precio_compra_id\n        join proveedores pr on pr.proveedor_id = pc.proveedor_id\n        join monedas m on m.moneda_id = pcd.moneda_id\n        where pc.articulo_id = %s\n        order by pc.fecha_precio_ult_compra desc' % articulo.id)
        precios_compra = c.fetchall()
        existencia = get_existencias_articulo(articulo_id=articulo.id, connection_name=using, fecha_inicio=datetime.now().strftime('01/01/%Y'), almacen='CONSOLIDADO')
        precios_empresa = list(ArticuloPrecio.objects.filter(articulo=articulo))
        precios_empresa = map(lambda x: x.precio_empresa.nombre, precios_empresa)
        context = {'formset': formset, 'articulo_nombre': articulo.nombre, 
           'es_moneda_local': moneda_local, 
           'costo_ultima_compra': costo_ultima_compra, 
           'impuesto': impuesto, 
           'tipo_cambio_ultima_compra': tipo_cambio_ultima_compra, 
           'monedas': monedas, 
           'adv_moneda': adv_moneda, 
           'precios_compra': precios_compra, 
           'precios_empresa': precios_empresa, 
           'existencia': existencia}
        if impuesto:
            context['impuesto_porcentaje'] = impuesto[0].impuesto.porcentaje
        return render_to_response(template_name, context, context_instance=RequestContext(request))