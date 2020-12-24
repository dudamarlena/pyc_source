# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_exportaimportaprecios\djmicrosip_exportaimportaprecios\views.py
# Compiled at: 2016-07-25 12:19:41
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ArticulosSearchForm, ImportarPreciosForm
import csv
from django.http import HttpResponse
from django.views.generic.list import ListView
import unicodecsv
from microsip_api.comun.sic_db import first_or_none
from decimal import Decimal
import xlwt, xlrd

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_exportaimportaprecios/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def importar_precios_view(request, template_name='djmicrosip_exportaimportaprecios/importar_precios.html'):
    form = ImportarPreciosForm(request.POST or None, request.FILES)
    msg = ''
    if form.is_valid():
        archivo = form.cleaned_data['archivo']
        linea = form.cleaned_data['linea']
        moneda = form.cleaned_data['moneda']
        book = xlrd.open_workbook(file_contents=archivo.read())
        sheet = book.sheet_by_index(0)
        num_rows = sheet.nrows - 1
        precios_posiciones = {}
        margenes_posiciones = {}
        ncols = sheet.ncols
        for curr_col in range(2, ncols):
            precio_nombre = sheet.cell_value(rowx=0, colx=curr_col)
            precios_posiciones[precio_nombre] = curr_col
            margenes_posiciones[precio_nombre] = curr_col + 1

        curr_row = 0
        while curr_row < num_rows:
            curr_row += 1
            print curr_row
            clave = sheet.cell_value(rowx=curr_row, colx=0)
            articulo_clave = first_or_none(ArticuloClave.objects.filter(clave=clave))
            if articulo_clave:
                articulo = articulo_clave.articulo
                if articulo.linea == linea:
                    for precio_nombre, posicion in precios_posiciones.items():
                        precio = sheet.cell_value(rowx=curr_row, colx=posicion)
                        if is_number(precio):
                            precio_empresa = PrecioEmpresa.objects.get(nombre=precio_nombre)
                            articulo_precio = first_or_none(ArticuloPrecio.objects.filter(articulo=articulo, precio_empresa__nombre=precio_nombre))
                            precio = round(precio, 2)
                            if articulo_precio:
                                articulo_precio.precio = precio
                                articulo_precio.moneda = moneda
                                articulo_precio.save(update_fields=('precio', 'moneda'))
                            else:
                                ArticuloPrecio.objects.create(articulo=articulo, precio_empresa=precio_empresa, moneda=moneda, precio=precio, margen=0)

        msg = 'Precios actualizados correctamente'
    context = {'form': form, 
       'msg': msg}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def exportar_precios_view(request, template_name='djmicrosip_exportaimportaprecios/exportar_precios.html'):
    form = ArticulosSearchForm(request.POST or None)
    if form.is_valid():
        linea = form.cleaned_data['linea']
        response = HttpResponse(mimetype='application/ms-excel')
        if linea:
            response['Content-Disposition'] = 'attachment; filename=%s.xls' % linea.nombre.replace(' ', '_')
            articulos = Articulo.objects.filter(linea=linea)
        else:
            response['Content-Disposition'] = 'attachment; filename=arts.xls'
            articulos = Articulo.objects.all()
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Precios')
        ws.row(0).write(0, 'Clave')
        ws.row(0).write(1, 'Articulo')
        precios_empresa = PrecioEmpresa.objects.all()
        curr_col = 2
        precios_posiciones = {}
        for precio_empresa in precios_empresa:
            ws.row(0).write(curr_col, precio_empresa.nombre)
            precios_posiciones[precio_empresa.nombre] = curr_col
            curr_col += 1

        r = 1
        for articulo in articulos:
            articulo_clave = first_or_none(ArticuloClave.objects.filter(articulo=articulo))
            if articulo_clave:
                precio = 0
                clave = articulo_clave.clave
                ws.row(r).write(0, clave)
                ws.row(r).write(1, articulo.nombre)
                articulos_precios = ArticuloPrecio.objects.filter(articulo=articulo)
                for articulo_precio in articulos_precios:
                    if articulo_precio:
                        precio = articulo_precio.precio
                        lista_precio_nombre = articulo_precio.precio_empresa.nombre
                        ws.row(r).write(precios_posiciones[lista_precio_nombre], precio)

                r += 1

        wb.save(response)
        return response
    else:
        context = {'form': form}
        return render_to_response(template_name, context, context_instance=RequestContext(request))