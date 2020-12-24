# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_cambiaprecios\djmicrosip_cambiaprecios\views.py
# Compiled at: 2018-09-06 11:50:39
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.db import connections, router
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.list import ListView
from microsip_api.comun.sic_db import first_or_none, get_existencias_articulo
import csv
from datetime import datetime
from minidetector2 import detect_mobile

@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_cambiaprecios/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


@detect_mobile
@login_required(login_url='/login/')
def articulo_manageview(request, id=None):
    using = router.db_for_write(Articulo)
    con = connections[using]
    c = con.cursor()
    if request.mobile:
        template_name = 'djmicrosip_cambiaprecios/articulo_mobile.html'
    else:
        template_name = 'djmicrosip_cambiaprecios/articulo.html'
    monedas = []
    moneda_local = ''
    tipo_cambio_ultima_compra = 0
    adv_moneda = ''
    articulo = get_object_or_404(Articulo, pk=id)
    impuesto = ImpuestosArticulo.objects.filter(articulo=articulo, impuesto__porcentaje=16)
    c.execute('select costo_ultima_compra from get_ultcom_art(' + id + ')')
    costo_ultima_compra = c.fetchall()[0][0]
    precios_articulos = ArticuloPrecio.objects.filter(articulo=articulo)
    for precio_articulo in precios_articulos:
        if precio_articulo.moneda.nombre not in monedas:
            monedas.append(precio_articulo.moneda.nombre)

    if len(monedas) > 1:
        adv_moneda = 'Los precios de lista no son todos de la misma moneda'
    else:
        moneda = Moneda.objects.get(nombre=monedas[0])
        moneda_local = moneda.es_moneda_local
    c.execute("select first 1 dc.tipo_cambio from doctos_cm dc\n        join doctos_cm_det dcd on dcd.docto_cm_id = dc.docto_cm_id\n        where dcd.articulo_id = %s and dc.tipo_docto ='C'\n        order by dc.fecha desc" % articulo.id)
    try:
        tipo_cambio_ultima_compra = c.fetchall()[0][0]
    except Exception as e:
        pass

    if moneda_local == 'N':
        if tipo_cambio_ultima_compra == 0:
            fecha_ultima_compra = articulo.fecha_ultima_compra
            if fecha_ultima_compra:
                tipo_cambio_ultima_compra = first_or_none(TipoCambio.objects.filter(fecha=fecha_ultima_compra, moneda=moneda))
                if tipo_cambio_ultima_compra:
                    tipo_cambio_ultima_compra.tipo_cambio
                elif TipoCambio.objects.filter(fecha__lte=fecha_ultima_compra, moneda=moneda).order_by('fecha'):
                    tipo_cambio_ultima_compra = TipoCambio.objects.filter(fecha__lte=fecha_ultima_compra, moneda=moneda).order_by('-fecha')[0].tipo_cambio
                else:
                    tipo_cambio_ultima_compra = TipoCambio.objects.filter(fecha__gte=fecha_ultima_compra, moneda=moneda).order_by('fecha')[0].tipo_cambio
            else:
                tipo_cambio_ultima_compra = TipoCambio.objects.filter(moneda=moneda).order_by('fecha')[0].tipo_cambio
    form_articulo = ArticuloPrecioCompraForm(request.POST or None, instance=articulo)
    if form_articulo.is_valid():
        actualizar_costos = Registry.objects.get(nombre='SIC_CambiaPrecio_ActualizarCostos').get_value() == '1'
        if actualizar_costos:
            form_articulo.save()
    DetalleFormset = ArticuloPrecioFormset(ArticuloPrecioForm, extra=0, can_delete=False, can_order=False)
    formset = DetalleFormset(request.POST or None, instance=articulo)
    if formset.is_valid():
        formset.save()
        return HttpResponseRedirect('/cambiaprecios/articulos/')
    else:
        con = connections[using]
        c = con.cursor()
        c.execute('select first 5 pc.fecha_precio_ult_compra,pr.nombre,pcd.precio_uven,m.nombre from precios_compra pc\n        join precios_compra_det pcd  on pcd.precio_compra_id = pc.precio_compra_id\n        join proveedores pr on pr.proveedor_id = pc.proveedor_id\n        join monedas m on m.moneda_id = pcd.moneda_id\n        where pc.articulo_id = %s\n        order by pc.fecha_precio_ult_compra desc' % articulo.id)
        precios_compra = c.fetchall()
        existencia = get_existencias_articulo(articulo_id=articulo.id, connection_name=using, fecha_inicio=datetime.now().strftime('01/01/%Y'), almacen='CONSOLIDADO')
        precios_empresa = list(ArticuloPrecio.objects.filter(articulo=articulo))
        precios_empresa = map(lambda x: x.precio_empresa.nombre, precios_empresa)
        con = {'formset': formset, 'articulo_nombre': articulo.nombre, 
           'es_moneda_local': moneda_local, 
           'costo_ultima_compra': costo_ultima_compra, 
           'impuesto': impuesto, 
           'tipo_cambio_ultima_compra': tipo_cambio_ultima_compra, 
           'monedas': monedas, 
           'adv_moneda': adv_moneda, 
           'precios_compra': precios_compra, 
           'precios_empresa': precios_empresa, 
           'existencia': existencia, 
           'form_articulo': form_articulo, 
           'moneda_nombre': moneda.nombre}
        return render_to_response(template_name, con, context_instance=RequestContext(request))


class ArticuloListView(ListView):
    context_object_name = 'articulos'
    model = Articulo
    template_name = 'djmicrosip_cambiaprecios/articulos.html'
    paginate_by = 50

    def dispatch(self, *args, **kwargs):
        return super(ArticuloListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        documentos = []
        get_dict = self.request.GET
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