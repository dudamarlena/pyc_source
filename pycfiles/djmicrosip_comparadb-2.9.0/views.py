# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_comparadb\djmicrosip_comparadb\views.py
# Compiled at: 2017-08-28 17:46:22
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.db import connections, router
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from microsip_api.comun.sic_db import first_or_none
import csv, xlwt

@login_required(login_url='/login/')
def localizaciones_view(request, template_name='djmicrosip_comparadb/localizaciones.html'):
    count = 0
    enviado = 'N'
    diferencias = []
    coincidencias = []
    articulos_ids = []
    form = SingleConexionForm(request.POST or None)
    empresa = None
    dicc = {}
    if form.is_valid():
        enviado = 'S'
        empresa = form.cleaned_data['empresas']
        articulos = Articulo.objects.using(empresa).all()
        for articulo in articulos:
            count += 1
            print count
            articulo_origen_id = articulo.id
            articulo_duplicado_por = 'no'
            articulo_nombre = articulo.nombre
            articulos_claves = ArticuloClave.objects.using(empresa).filter(articulo=articulo)
            existe = False
            for clave in articulos_claves:
                if ArticuloClave.objects.filter(clave=clave.clave).exists():
                    existe = True
                    articulo_duplicado_por = 'clave'
                    articulo_dest = first_or_none(ArticuloClave.objects.filter(clave=clave.clave)).articulo

            niveles = ArticuloNivel.objects.using(empresa).filter(articulo__id=articulo_origen_id)
            if niveles:
                for nivel in niveles.values():
                    almacen_origen = nivel['almacen_id']
                    almacen_origen = Almacen.objects.using(empresa).get(ALMACEN_ID=almacen_origen)
                    almacen_nombre = almacen_origen.nombre
                    almacen = first_or_none(Almacen.objects.filter(nombre=almacen_nombre))
                    if articulo_duplicado_por == 'clave':
                        if ArticuloNivel.objects.filter(articulo=articulo_dest, almacen=almacen).exists():
                            nivel_dup = first_or_none(ArticuloNivel.objects.filter(articulo=articulo_dest, almacen=almacen))
                            nivel_dup.localizacion = nivel['localizacion']
                            nivel_dup.maximo = nivel['maximo']
                            nivel_dup.reorden = nivel['reorden']
                            nivel_dup.minimo = nivel['minimo']
                            nivel_dup.save()
                        elif almacen:
                            ArticuloNivel.objects.create(id=-1, articulo=articulo_dest, almacen=almacen, localizacion=nivel['localizacion'], maximo=nivel['maximo'], reorden=nivel['reorden'], minimo=nivel['minimo'])

            count += 1
            print count

        dicc[empresa] = {'diferencias': len(diferencias), 'coincidencias': len(coincidencias), 
           'articulos_ids': articulos_ids}
    c = {'form': form, 
       'dicc': dicc, 
       'articulos_ids': articulos_ids, 
       'enviado': enviado}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def costosultimo_view(request, template_name='djmicrosip_comparadb/costos.html'):
    count = 0
    modif = 0
    enviado = 'N'
    diferencias = []
    coincidencias = []
    articulos_ids = []
    form = SingleConexionForm(request.POST or None)
    empresa = None
    dicc = {}
    if form.is_valid():
        enviado = 'S'
        empresa = form.cleaned_data['empresas']
        articulos = Articulo.objects.using(empresa).all()
        for articulo in articulos:
            articulo_dest = None
            count += 1
            print '%s/%s-----%s' % (count, len(articulos), modif)
            articulo_origen_id = articulo.id
            articulo_duplicado_por = 'no'
            articulo_nombre = articulo.nombre
            articulos_claves = ArticuloClave.objects.using(empresa).filter(articulo=articulo)
            existe = False
            for clave in articulos_claves:
                if ArticuloClave.objects.filter(clave=clave.clave).exists():
                    existe = True
                    articulo_duplicado_por = 'clave'
                    articulo_dest = first_or_none(ArticuloClave.objects.filter(clave=clave.clave)).articulo

            if articulo_dest:
                if articulo.costo_ultima_compra > 0:
                    try:
                        articulo_dest.costo_ultima_compra = articulo.costo_ultima_compra
                        articulo_dest.save(update_fields=['costo_ultima_compra'])
                        modif += 1
                    except Exception as e:
                        pass

        dicc[empresa] = {'diferencias': len(diferencias), 
           'coincidencias': len(coincidencias), 
           'articulos_ids': articulos_ids}
    c = {'form': form, 
       'dicc': dicc, 
       'articulos_ids': articulos_ids, 
       'enviado': enviado, 
       'modif': modif}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def costosprom_view(request, template_name='djmicrosip_comparadb/costosprom.html'):
    count = 0
    modif = 0
    enviado = 'N'
    diferencias = []
    coincidencias = []
    articulos_ids = []
    costo_promedio = 0
    form = SingleConexionForm(request.POST or None)
    empresa = None
    dicc = {}
    if form.is_valid():
        enviado = 'S'
        empresa = form.cleaned_data['empresas']
        c = connections[empresa].cursor()
        articulos = Articulo.objects.using(empresa).all()
        for articulo in articulos:
            articulo_dest = None
            count += 1
            print '%s/%s-----%s' % (count, len(articulos), modif)
            articulo_origen_id = articulo.id
            articulo_duplicado_por = 'no'
            articulo_nombre = articulo.nombre
            articulos_claves = ArticuloClave.objects.using(empresa).filter(articulo=articulo)
            existe = False
            for clave in articulos_claves:
                if ArticuloClave.objects.filter(clave=clave.clave).exists():
                    existe = True
                    articulo_duplicado_por = 'clave'
                    articulo_dest = first_or_none(ArticuloClave.objects.filter(clave=clave.clave)).articulo
                    break

            if articulo_dest:
                c.execute("SELECT p.VALOR_UNITARIO FROM EXIVAL_ART(%s, (select almacen_id from almacenes where es_ppal='S'), current_date, 'N') p" % articulo_origen_id)
                costo_promedio = c.fetchall()[0][0]
                if costo_promedio > 0 and articulo_dest.costo_ultima_compra == 0:
                    try:
                        articulo_dest.costo_ultima_compra = costo_promedio
                        articulo_dest.save(update_fields=['costo_ultima_compra'])
                        modif += 1
                    except Exception as e:
                        print '////////////////////////////////////'

        dicc[empresa] = {'diferencias': len(diferencias), 'coincidencias': len(coincidencias), 
           'articulos_ids': articulos_ids}
    c = {'form': form, 
       'dicc': dicc, 
       'articulos_ids': articulos_ids, 
       'enviado': enviado, 
       'modif': modif}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def precios_linea_view(request, template_name='djmicrosip_comparadb/precios_linea.html'):
    count = 0
    enviado = 'N'
    diferencias = []
    coincidencias = []
    articulos_ids = []
    form = SingleConexionForm(request.POST or None)
    form2 = LineaForm(request.POST or None)
    empresa = None
    dicc = {}
    if form.is_valid() and form2.is_valid():
        enviado = 'S'
        empresa = form.cleaned_data['empresas']
        linea = form2.cleaned_data['linea']
        articulos = Articulo.objects.filter(linea=linea)
        for articulo in articulos:
            count += 1
            print count
            articulos_claves = ArticuloClave.objects.filter(articulo=articulo)
            for clave in articulos_claves:
                if ArticuloClave.objects.using(empresa).filter(clave=clave.clave).exists():
                    art_id = ArticuloClave.objects.using(empresa).filter(clave=clave.clave).values('articulo_id')[0]['articulo_id']
                    articulo_dest = Articulo.objects.using(empresa).get(id=art_id)
                    impuesto_nombre = Impuesto.objects.using(empresa).get(id=ImpuestosArticulo.objects.using(empresa).filter(articulo__id=art_id).values()[0]['impuesto_id']).nombre
                    impuesto_a_poner = Impuesto.objects.get(nombre=impuesto_nombre)
                    if not ImpuestosArticulo.objects.filter(impuesto=impuesto_a_poner, articulo=articulo).exists():
                        ImpuestosArticulo.objects.create(impuesto=impuesto_a_poner, articulo=articulo)
                    precios = ArticuloPrecio.objects.using(empresa).filter(articulo=articulo_dest).values()
                    for precio in precios:
                        precio_c = precio['precio']
                        margen = precio['margen']
                        moneda_nombre = Moneda.objects.using(empresa).get(id=precio['moneda_id']).nombre
                        moneda = Moneda.objects.get(nombre=moneda_nombre)
                        precio_nombre = PrecioEmpresa.objects.using(empresa).get(id=precio['precio_empresa_id']).nombre
                        precio_empresa = PrecioEmpresa.objects.get(nombre=precio_nombre)
                        existe = ArticuloPrecio.objects.filter(articulo=articulo, precio_empresa=precio_empresa).exists()
                        if existe:
                            art_precio = ArticuloPrecio.objects.filter(articulo=articulo, precio_empresa=precio_empresa)[0]
                            art_precio.precio = precio_c
                            art_precio.margen = margen
                            art_precio.moneda = moneda
                            art_precio.save()
                        else:
                            ArticuloPrecio.objects.create(articulo=articulo, precio_empresa=precio_empresa, moneda=moneda, precio=precio_c, margen=margen)

    c = {'form': form, 
       'form2': form2, 
       'dicc': dicc, 
       'articulos_ids': articulos_ids, 
       'enviado': enviado}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def articulos_view(request, template_name='djmicrosip_comparadb/articulos.html'):
    count = 0
    enviado = 'N'
    diferencias = []
    coincidencias = []
    articulos_ids = []
    form = MultipleConexionForm(request.POST or None)
    empresa = None
    dicc = {}
    if form.is_valid():
        enviado = 'S'
        empresas = form.cleaned_data['empresas']
        for empresa in empresas:
            empresa_nombre = empresa.split('-')[1]
            nombre_linea = 'Importados de ' + empresa_nombre
            count = 0
            diferencias = []
            coincidencias = []
            articulos_ids = []
            articulos = Articulo.objects.all()
            for articulo in articulos:
                count += 1
                print '%s / %s.' % (count, len(articulos))
                articulo_origen_id = articulo.id
                articulo_duplicado_por = 'no'
                articulo_nombre = articulo.nombre
                articulos_claves = ArticuloClave.objects.filter(articulo=articulo)
                existe = False
                if Articulo.objects.using(empresa).filter(nombre=articulo.nombre).exists():
                    existe = True
                for clave in articulos_claves:
                    if ArticuloClave.objects.using(empresa).filter(clave=clave.clave).exists():
                        existe = True

                if not existe:
                    diferencias.append(articulo.nombre)
                else:
                    coincidencias.append(articulo.nombre)

            response = HttpResponse(mimetype='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=comparacion.xls'
            wb = xlwt.Workbook()
            ws = wb.add_sheet('Articulos Diferentes')
            row = 0
            for diferencia in diferencias:
                cl = ''
                using = router.db_for_write(Articulo)
                c = connections[using].cursor()
                art = Articulo.objects.get(nombre=diferencia)
                id_art = art.id
                clave_art = first_or_none(ArticuloClave.objects.filter(articulo__id=id_art))
                if clave_art:
                    cl = clave_art.clave
                c.execute("select inv_fin_unid from orsp_in_aux_art(%s,'Consolidado','01/01/2000',current_date, 'N','N')" % id_art)
                existencia = c.fetchall()[0][0]
                ws.row(row).write(0, cl)
                ws.row(row).write(1, diferencia)
                ws.row(row).write(2, existencia)
                row += 1

            wb.save(response)
            return response
            dicc[empresa] = {'diferencias': len(diferencias), 
               'coincidencias': len(coincidencias), 
               'articulos_ids': articulos_ids}
            D

    c = {'form': form, 'dicc': dicc, 
       'articulos_ids': articulos_ids, 
       'enviado': enviado}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def articulos2_view(request, template_name='djmicrosip_comparadb/articulos2.html'):
    count = 0
    enviado = 'N'
    diferencias = []
    coincidencias = []
    articulos_ids = []
    form = MultipleConexionForm(request.POST or None)
    empresa = None
    dicc = {}
    if form.is_valid():
        enviado = 'S'
        empresas = form.cleaned_data['empresas']
        for empresa in empresas:
            empresa_nombre = empresa.split('-')[1]
            nombre_linea = '-Importados de ' + empresa_nombre
            count = 0
            diferencias = []
            coincidencias = []
            articulos_ids = []
            articulos = Articulo.objects.using(empresa).filter(estatus='A')
            for articulo in articulos:
                count += 1
                print '%s/%s' % (count, len(articulos))
                articulo_origen_id = articulo.id
                articulo_duplicado_por = 'no'
                articulo_nombre = articulo.nombre
                articulos_claves = ArticuloClave.objects.using(empresa).filter(articulo=articulo)
                existe = False
                if Articulo.objects.filter(nombre=articulo.nombre).exists():
                    existe = True
                    articulo_duplicado_por = 'nombre'
                    articulo_dest = first_or_none(Articulo.objects.filter(nombre=articulo_nombre))
                for clave in articulos_claves:
                    if ArticuloClave.objects.filter(clave=clave.clave).exists():
                        existe = True
                        articulo_duplicado_por = 'clave'
                        articulo_dest = first_or_none(ArticuloClave.objects.filter(clave=clave.clave)).articulo

                if not existe:
                    diferencias.append(articulo.nombre)
                    articulos_ids.append(articulo.id)
                    a = True
                    claves = ArticuloClave.objects.using(empresa).filter(articulo=articulo)
                    articulo.id = None
                    articulo.linea = LineaArticulos.objects.get_or_create(nombre=nombre_linea)[0]
                    articulo.save()
                    articulo_dest = first_or_none(Articulo.objects.filter(nombre=articulo_nombre))
                    precios_art = ArticuloPrecio.objects.using(empresa).filter(articulo__id=articulo_origen_id)
                    for precio_art in precios_art.values():
                        precio_emp_obj = PrecioEmpresa.objects.using(empresa).get(id=precio_art['precio_empresa_id']).nombre
                        precio_emp = first_or_none(PrecioEmpresa.objects.filter(nombre=precio_emp_obj))
                        if precio_emp:
                            moneda_obj = first_or_none(Moneda.objects.filter(nombre=first_or_none(Moneda.objects.using(empresa).filter(id=precio_art['moneda_id']))))
                            if moneda_obj:
                                moneda = first_or_none(Moneda.objects.filter(nombre=moneda_obj.nombre))
                                ArticuloPrecio.objects.create(articulo=articulo_dest, precio_empresa=precio_emp, moneda=moneda, precio=precio_art['precio'], margen=precio_art['margen'])

                    impuestos_art = ImpuestosArticulo.objects.using(empresa).filter(articulo__id=articulo_origen_id)
                    if impuestos_art:
                        for impuesto_art in impuestos_art.values():
                            impuesto_nombre = Impuesto.objects.using(empresa).get(id=impuesto_art['impuesto_id']).nombre
                            impuesto_a_poner = Impuesto.objects.get(nombre=impuesto_nombre)
                            ImpuestosArticulo.objects.create(impuesto=impuesto_a_poner, articulo=articulo_dest)

                    if claves:
                        clave = claves[0]
                        clave.id = None
                        clave.rol = ArticuloClaveRol.objects.get(es_ppal='S')
                        clave.articulo = Articulo.objects.get(nombre=articulo.nombre)
                        clave.save()
                else:
                    a = False
                    coincidencias.append(articulo.nombre)

            dicc[empresa] = {'diferencias': len(diferencias), 
               'coincidencias': len(coincidencias), 
               'articulos_ids': articulos_ids}

        D
    c = {'form': form, 
       'dicc': dicc, 
       'articulos_ids': articulos_ids, 
       'enviado': enviado}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def renombrar_articulos_view(request, template_name='djmicrosip_comparadb/articulosrenombrar.html'):
    count = 0
    errores = []
    enviado = 'N'
    diferencias = []
    coincidencias = []
    articulos_ids = []
    form = SingleConexionForm(request.POST or None)
    form2 = LineaForm(request.POST or None)
    empresa = None
    dicc = {}
    if form.is_valid() and form2.is_valid():
        enviado = 'S'
        empresa = form.cleaned_data['empresas']
        linea = form2.cleaned_data['linea']
        count = 0
        modif = 0
        articulos = Articulo.objects.filter(linea=linea)
        for articulo in articulos:
            count += 1
            print '%s / %s.' % (count, len(articulos))
            articulo_nombre = articulo.nombre
            articulos_claves = ArticuloClave.objects.filter(articulo=articulo)
            existe = False
            for clave in articulos_claves:
                if ArticuloClave.objects.using(empresa).filter(clave=clave.clave).exists():
                    existe = True
                    articulo_nombre_nueva = Articulo.objects.using(empresa).get(id=first_or_none(ArticuloClave.objects.using(empresa).filter(clave=clave.clave)).articulo_id).nombre
                    if articulo_nombre != articulo_nombre_nueva:
                        try:
                            articulo.nombre = articulo_nombre_nueva
                            articulo.save()
                            modif = modif + 1
                            print '%s---------------------------------------' % modif
                        except Exception as e:
                            errores.append(clave.clave)

    c = {'form': form, 
       'form2': form2, 
       'enviado': enviado, 
       'errores': errores}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_comparadb/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def sync_view(request):
    empresa = request.GET['empresa']
    using = router.db_for_write(Articulo)
    empresa_origen = using.split('-')[1]
    count = 1
    articulos = Articulo.objects.all()
    nombre_linea = 'Importados de ' + empresa_origen
    for articulo in articulos:
        articulos_claves = ArticuloClave.objects.filter(articulo=articulo)
        existe = False
        if Articulo.objects.using(empresa).filter(nombre=articulo.nombre).exists():
            existe = True
        else:
            for clave in articulos_claves:
                if ArticuloClave.objects.using(empresa).filter(clave=clave.clave).exists():
                    existe = True

        if not existe:
            claves = ArticuloClave.objects.filter(articulo=articulo)
            articulo.id = None
            articulo.linea = LineaArticulos.objects.using(empresa).get_or_create(nombre=nombre_linea)[0]
            articulo.save(using=empresa)
            if claves:
                clave = claves[0]
                clave.id = None
                clave.rol = ArticuloClaveRol.objects.using(empresa).get(es_ppal='S')
                clave.articulo = Articulo.objects.using(empresa).get(nombre=articulo.nombre)
                clave.save(using=empresa)
        count = count + 1
        print count

    data = {}
    return HttpResponse(data, mimetype='application/json')


@login_required(login_url='/login/')
def exporta_excel_view(request):
    count = 0
    diferencias = []
    coincidencias = []
    empresa = '02-RAFISA_NCG'
    articulos = Articulo.objects.all()
    for articulo in articulos:
        articulos_claves = ArticuloClave.objects.filter(articulo=articulo)
        existe = False
        if Articulo.objects.using(empresa).filter(nombre=articulo.nombre).exists():
            existe = True
        else:
            for clave in articulos_claves:
                if ArticuloClave.objects.using(empresa).filter(clave=clave.clave).exists():
                    existe = True

        if not existe:
            diferencias.append(articulo.nombre)
        else:
            coincidencias.append(articulo.nombre)
        count += 1
        print count

    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=comparacion.xls'
    wb = xlwt.Workbook()
    ws = wb.add_sheet('DIFERENCIA')
    ws.row(0).write(0, 'Diferencias')
    ws.row(0).write(1, 'Coincidencias')
    ws.row(0).write(2, str(len(diferencias)))
    ws.row(1).write(2, str(len(coincidencias)))
    ws.row(0).write(3, 'Diferencias')
    ws.row(1).write(3, 'Coincidencias')
    r = 1
    for diferencia in diferencias:
        ws.row(r).write(0, diferencia)
        r += 1

    r = 1
    for coincidencia in coincidencias:
        ws.row(r).write(1, coincidencia)
        r += 1

    wb.save(response)
    return response