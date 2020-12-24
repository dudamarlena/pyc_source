# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_microsip_diot\django_microsip_diot\views.py
# Compiled at: 2015-11-24 15:03:24
from .forms import *
from .models import *
from custom_db.paises import paises as paises_dic
from custom_db.procedures import procedures as sql_procedures
from datetime import datetime
from decimal import Decimal
from django.contrib.auth.decorators import login_required, permission_required
from django.core import management
from django.core.paginator import Paginator
from django.db import connections, router
from django.db.models import F, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.list import ListView
from microsip_api.comun.sic_db import first_or_none
import csv, json, re, xml.etree.ElementTree as ET, xlwt
from . import app_label
from . import config

@login_required(login_url='/login/')
def preferencias_view(request, template_name='django_microsip_diot/herramientas/preferencias.html'):
    form_initial = {'impuesto_default': Registry.objects.get(nombre='SIC_DIOT_tasaNoIVADefault').get_value(), 
       'rfc': Registry.objects.get(nombre='Rfc').get_value(), 
       'integrar_contabilidad': Registry.objects.get(nombre='SIC_DIOT_integrar_contabilidad').get_value() == 'True'}
    form = PreferenciasManageForm(request.POST or None, initial=form_initial)
    msg = ''
    if form.is_valid():
        form.save()
        msg = 'Informacion actualizada'
    c = {'form': form, 'msg': msg}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def index(request, template_name='django_microsip_diot/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


class ProveedorListView(ListView):
    context_object_name = 'Proveedores'
    model = Proveedor
    template_name = 'django_microsip_diot/proveedores.html'

    def get_queryset(self):
        form = ProveedorSearchForm(self.request.GET)
        if form.is_valid():
            proveedor = form.cleaned_data['proveedor']
            nombre = form.cleaned_data['nombre']
            proveedores = Proveedor.objects.all()
            if nombre:
                proveedores = proveedores.filter(nombre__contains=nombre)
            if proveedor:
                proveedores = Proveedor.objects.filter(pk=proveedor.id)
        return proveedores

    def get_context_data(self, **kwargs):
        context = super(ProveedorListView, self).get_context_data(**kwargs)
        context['form'] = ProveedorSearchForm(self.request.GET or None)
        return context


@login_required(login_url='/login/')
def ProveedorManageView(request, id=None, template_name='django_microsip_diot/proveedor.html'):
    """ Modificacion de puntos de un lineas """
    if id:
        proveedor = get_object_or_404(Proveedor, pk=id)
        form_initial = {'cuenta_por_pagar': first_or_none(ContabilidadCuentaContable.objects.filter(cuenta=proveedor.cuenta_xpagar))}
    else:
        proveedor = Proveedor()
        form_initial = {}
    form = ProveedorForm(request.POST or None, instance=proveedor, initial=form_initial)
    if form.is_valid():
        proveedor = form.save(commit=False)
        if not proveedor.id:
            proveedor.id = -1
        proveedor.pais = proveedor.pais
        proveedor.save()
        return HttpResponseRedirect('/diot/proveedores/')
    else:
        c = {'form': form, 'Proveedor': proveedor.nombre}
        return render_to_response(template_name, c, context_instance=RequestContext(request))


def DatetimeToDays(date1):
    temp = datetime(1899, 12, 30)
    delta = date1 - temp
    return float(delta.days) + float(delta.seconds) / 86400


@login_required(login_url='/login/')
def UpdateDatabaseTable(request):
    if request.user.is_superuser:
        padre = first_or_none(Registry.objects.filter(nombre='PreferenciasEmpresa'))
        if padre:
            if not Registry.objects.filter(nombre='SIC_DIOT_tasaNoIVADefault').exists():
                Registry.objects.create(nombre='SIC_DIOT_tasaNoIVADefault', tipo='V', padre=padre, valor='0')
            if not Registry.objects.filter(nombre='SIC_DIOT_integrar_contabilidad').exists():
                Registry.objects.create(nombre='SIC_DIOT_integrar_contabilidad', tipo='V', padre=padre, valor='0')
        using = router.db_for_write(Proveedor)
        management.call_command('syncdb', database=using, interactive=False)
        c = connections[using].cursor()
        c.execute(sql_procedures['SIC_PROVEEDORES_DIOT'])
        c.execute('EXECUTE PROCEDURE SIC_PROVEEDORES_DIOT;')
        c.execute('DROP PROCEDURE SIC_PROVEEDORES_DIOT;')
        c.execute('GRANT ALL ON SIC_DIOT_CAPTURAS TO USUARIO_MICROSIP')
        c.close()
        management.call_command('syncdb', database=using, interactive=False)
        from microsip_api.apps.config.models import ReportBuilderItem, ReportBuilderFolder
        folder = ReportBuilderFolder.objects.get(pk=22)
        from custom_db import report_builder
        for report_key in report_builder.reports.keys():
            reporte = first_or_none(ReportBuilderItem.objects.filter(name=report_key, folder=folder))
            if reporte:
                reporte.template = report_builder.reports[report_key]
                reporte.save(update_fields=['template'])
            else:
                ReportBuilderItem.objects.create(id=-1, folder=folder, name=report_key, item_size=1, modified=DatetimeToDays(datetime.now()), template=report_builder.reports[report_key])

    return HttpResponseRedirect('/diot/exporta_xml')


@login_required(login_url='/login/')
def ExportaDiotXML(request, template_name='django_microsip_diot/exportadiotxml.html'):
    button = False
    mostrar_fecha = 0
    f_i = None
    fecha_fin = None
    fecha_inicio = None
    form = GeneraDiotForm(request.POST or None)
    form_manual = ManualForm(request.POST or None)
    inicio_ext = None
    repo_dic = {}
    repo_list = []
    repos_ext = None
    repositorios_ext = None
    manuales = None
    subtotal = 0
    mostrar_check_integrar = 0
    tasa_no_iva = Registry.objects.get(nombre='SIC_DIOT_tasaNoIVADefault').get_value()
    integrar_contabilidad = Registry.objects.get(nombre='SIC_DIOT_integrar_contabilidad').get_value() == 'True'
    if form.is_valid():
        mostrar_check_integrar = 1
        fecha_inicio = form.cleaned_data['fecha_inicio']
        fecha_fin = form.cleaned_data['fecha_fin']
        repos_ext = form.cleaned_data['repos_ext']
        inicio_ext = form.cleaned_data['inicio_ext']
        button = True
        manuales = CapturaManual.objects.filter(mostrar='S', fecha__lte=fecha_fin, fecha__gte=fecha_inicio)
        if integrar_contabilidad:
            fecha_inicio_str = fecha_inicio.strftime('%m/%d/%Y')
            fecha_fin_str = fecha_fin.strftime('%m/%d/%Y')
            using = router.db_for_write(Proveedor)
            c = connections[using].cursor()
            query = "select rc.cfdi_id, rc.fecha, rc.rfc, dc.poliza, dc.fecha from doctos_co dc join\n                tipos_polizas tp on tp.tipo_poliza_id = dc.tipo_poliza_id join\n                doctos_co_cfdi dcc on dcc.docto_co_id = dc.docto_co_id join\n                repositorio_cfdi rc on rc.cfdi_id = dcc.cfdi_id\n                where tp.tipo_fiscal = 2 and dc.fecha between %s and %s\n                and dc.estatus = 'N';"
            c.execute(query, [fecha_inicio_str, fecha_fin_str])
            repos_ids = c.fetchall()
            repos_ids = map(lambda x: x[0], repos_ids)
            repositorios_cfdi = RepositorioCFDI.objects.filter(id__in=repos_ids, naturaleza='R', tipo_comprobante='I')
        else:
            repositorios_cfdi = RepositorioCFDI.objects.filter(Q(diot_mostrar=None) | Q(diot_mostrar='S')).filter(naturaleza='R', tipo_comprobante='I', fecha__lte=fecha_fin, fecha__gte=fecha_inicio, importe__gt=0).order_by('rfc')
        if repos_ext:
            mostrar_fecha = 1
            if inicio_ext:
                repositorios_ext = RepositorioCFDI.objects.filter(Q(diot_mostrar=None) | Q(diot_mostrar='S')).filter(naturaleza='R', tipo_comprobante='I', fecha__lt=fecha_inicio, fecha__gte=inicio_ext, importe__gt=0).order_by('rfc')
            else:
                repositorios_ext = RepositorioCFDI.objects.filter(Q(diot_mostrar=None) | Q(diot_mostrar='S')).filter(naturaleza='R', tipo_comprobante='I', fecha__lt=fecha_inicio, importe__gt=0).order_by('rfc')
            repositorios_cfdi = repositorios_cfdi | repositorios_ext
        for repositorio in repositorios_cfdi:
            valor_impuesto = 0
            valor_ieps = 0
            subtotal = 0
            descuento = 0
            valor_retencion_iva = 0
            xml = repositorio.xml
            if xml:
                xml = xml.encode('utf8', 'ignore')
                root = ET.fromstring(xml)
                subtotal = root.attrib['subTotal']
                if 'descuento' in root.attrib:
                    descuento = root.attrib['descuento']
                impuestos = root[3]
                for impuesto in impuestos:
                    if 'Retenciones' in impuesto.tag:
                        retenciones = impuesto
                        for retencion in retenciones:
                            if retencion.attrib['impuesto'] == 'IVA':
                                valor_retencion_iva = retencion.attrib['importe']

                    for impuesto_detalle in impuesto:
                        datos = impuesto_detalle.attrib
                        try:
                            tasa = Decimal(datos['tasa'])
                        except Exception as e:
                            tasa = 1

                        if datos['impuesto'] == 'IVA' and tasa != 0:
                            valor_impuesto = datos['importe']
                        if datos['impuesto'] == 'IEPS' and tasa != 0:
                            valor_ieps = datos['importe']

                repo_dic[repositorio.id] = (
                 repositorio, valor_impuesto, subtotal, descuento, valor_retencion_iva, valor_ieps)
            else:
                repo_dic[repositorio.id] = (
                 repositorio, valor_impuesto, subtotal, descuento, valor_retencion_iva, valor_ieps)

        values = repo_dic.values()
        repo_list = sorted(values, key=lambda x: x[0].rfc)
        f_i = fecha_inicio
        fecha_inicio = fecha_inicio.strftime('%Y/%m/%d')
        fecha_fin = fecha_fin.strftime('%Y/%m/%d')
        if inicio_ext:
            inicio_ext = inicio_ext.strftime('%Y/%m/%d')
    c = {'button': button, 
       'f_i': f_i, 
       'fecha_fin': fecha_fin, 
       'fecha_inicio': fecha_inicio, 
       'form': form, 
       'form_manual': form_manual, 
       'inicio_ext': inicio_ext, 
       'integrar_contabilidad': integrar_contabilidad, 
       'manuales': manuales, 
       'mostrar_check_integrar': mostrar_check_integrar, 
       'mostrar_fecha': mostrar_fecha, 
       'repo_dic': repo_list, 
       'repos_ext': repos_ext, 
       'tasa_no_iva': tasa_no_iva}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def create_file(request):
    clave_pais = ''
    desglose_dic = {}
    desglose_list = []
    dic_diot = request.GET['dic_diot']
    fecha_inicio = request.GET['fecha_inicio']
    detallado = request.GET['detallado']
    diot_list = []
    tasa0 = 0
    tasa16 = 0
    mes = fecha_inicio.split('/')[1]
    anio = fecha_inicio.split('/')[0][2:4]
    nombre_archivo = Registry.objects.get(nombre='Rfc').valor[0:4] + mes + anio
    dic_diot = json.loads(dic_diot)
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s.txt"' % nombre_archivo
    writer = csv.writer(response, delimiter='|')
    for rfc in dic_diot:
        detalle = dic_diot[rfc]
        if detalle['extranjero'] == 'S':
            proveedor = first_or_none(Proveedor.objects.filter(nombre=detalle['nombre']))
        else:
            proveedor = first_or_none(Proveedor.objects.filter(rfc_curp=rfc))
        actividad_principal = proveedor.actividad_principal
        if proveedor.es_extranjero == 'N':
            tipo_proveedor = '04'
        else:
            tipo_proveedor = '05'
            if proveedor.pais.nombre in paises_dic:
                clave_pais = paises_dic[proveedor.pais.nombre]
            else:
                clave_pais = '.NA.'
        tasa16 = int(round(detalle['tasa16']))
        if tasa16 <= 0:
            tasa16 = ''
        tasaexento = int(round(detalle['tasaexento']))
        if tasaexento <= 0:
            tasaexento = ''
        iva_no_acreditable = int(round(detalle['iva_no_acreditable']))
        if iva_no_acreditable <= 0:
            iva_no_acreditable = ''
        iva_descuentos = int(round(detalle['iva_descuentos']))
        if iva_descuentos <= 0:
            iva_descuentos = ''
        tasa0 = int(round(detalle['tasa0']))
        if tasa0 <= 0:
            tasa0 = ''
        retenido = int(round(detalle['retenido']))
        if retenido <= 0:
            retenido = ''
        if tipo_proveedor == '04':
            diot_list.append([tipo_proveedor, actividad_principal, rfc.replace(' ', ''), '', '', '', '', tasa16, '', iva_no_acreditable, '', '', '', '', '', '', '', '', tasa0, tasaexento, '', retenido, iva_descuentos])
        else:
            diot_list.append([tipo_proveedor, actividad_principal, rfc.replace(' ', ''), clave_pais, proveedor.pais.nombre, '', '', tasa16, '', iva_no_acreditable, '', '', '', '', '', '', '', '', tasa0, tasaexento, '', retenido, iva_descuentos])
        if rfc not in desglose_dic:
            desglose_dic[rfc] = {}
            desglose_dic[rfc]['folios_fecha_importes'] = detalle['detalles']
            desglose_dic[rfc]['rfc'] = re.sub('\\W+', '', proveedor.rfc_curp)
            desglose_dic[rfc]['nombre'] = proveedor.nombre

    diot_list = sorted(diot_list, key=lambda x: x[2])
    for diot_line in diot_list:
        writer.writerow(diot_line)

    for rfc in desglose_dic.keys():
        desglose = desglose_dic[rfc]
        desglose_list.append([desglose['rfc'], desglose['nombre'], desglose['folios_fecha_importes']])

    if detallado == 'true':
        writer.writerow('')
        desglose_list.sort(key=lambda x: x[0])
        for desglose_linea in desglose_list:
            writer.writerow('')
            writer.writerow((desglose_linea[0], '------------', desglose_linea[1].encode('utf8', 'ignore')))
            for detalle in desglose_linea[2]:
                writer.writerow((detalle[0], detalle[1], detalle[2]))

    response.content = response.content[:-2]
    return response


@login_required(login_url='/login/')
def ExportaProveedoresView(request):
    proveedores = Proveedor.objects.exclude(rfc_curp=None)
    for proveedor in proveedores:
        rfc = proveedor.rfc_curp
        if rfc:
            proveedor.rfc_curp = re.sub('\\W+', '', proveedor.rfc_curp)
            proveedor.save()

    nombres = RepositorioCFDI.objects.filter(Q(diot_proveedor_revisado='N') | Q(diot_proveedor_revisado=None)).filter(naturaleza='R').values_list('nombre', 'rfc', 'id').distinct()
    nuevos = 0
    pais = first_or_none(Pais.objects.filter(nombre='Default'))
    if not pais:
        pais = Pais.objects.create(nombre='Default')
    estado = first_or_none(Estado.objects.filter(nombre='Default'))
    if not estado:
        estado = Estado.objects.create(nombre='Default', pais=pais)
    ciudad = first_or_none(Ciudad.objects.filter(nombre='Default'))
    if not ciudad:
        ciudad = Ciudad.objects.create(nombre='Default', estado=estado)
    moneda = first_or_none(Moneda.objects.filter(es_moneda_local='S'))
    cond_pago = CuentasXPagarCondicionPago.objects.filter(nombre='CONTADO')
    if not cond_pago:
        cond_pago = CuentasXPagarCondicionPago.objects.create(id=-1, nombre='CONTADO')
    cond_pago = first_or_none(CuentasXPagarCondicionPago.objects.filter(nombre='CONTADO'))
    for nombre in nombres:
        proveedor = None
        xml_nombre_proveedor = nombre[0]
        xml_rfc_proveedor = nombre[1]
        xml_id = nombre[2]
        if not xml_rfc_proveedor:
            proveedor = first_or_none(Proveedor.objects.filter(nombre=xml_nombre_proveedor))
        else:
            proveedor = first_or_none(Proveedor.objects.filter(rfc_curp=xml_rfc_proveedor))
            if not proveedor:
                proveedor = first_or_none(Proveedor.objects.filter(nombre=xml_nombre_proveedor))
                if proveedor:
                    proveedor.rfc_curp = xml_rfc_proveedor
                    proveedor.save()
        if not proveedor:
            if not xml_nombre_proveedor:
                xml_nombre_proveedor = xml_rfc_proveedor
            nuevos += 1
            Proveedor.objects.create(id=-1, nombre=xml_nombre_proveedor, rfc_curp=xml_rfc_proveedor, condicion_de_pago=cond_pago, ciudad=ciudad, estado=estado, pais=pais, moneda=moneda)
        RepositorioCFDI.objects.filter(id=xml_id).update(diot_proveedor_revisado='S')
        print xml_id

    data = {'nuevos': nuevos}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/login/')
def PaginationView(request):
    repo_dic = {}
    repositorios_ext = None
    subtotal = 0
    error = False
    pagina = None
    page = request.GET['page']
    fecha_inicio = request.GET['fecha_inicio'].replace('/', '-')
    fecha_fin = request.GET['fecha_fin'].replace('/', '-')
    inicio_ext = request.GET['inicio_ext'].replace('/', '-')
    repos_ext = request.GET['repos_ext']
    repositorios_cfdi = RepositorioCFDI.objects.filter(naturaleza='R', tipo_comprobante='I', fecha__lte=fecha_fin, fecha__gte=fecha_inicio, importe__gt=0).order_by('rfc').values('id', 'rfc', 'nombre', 'xml', 'folio', 'importe', 'tipo_comprobante', 'taxid', 'pagado', 'integrar', 'fecha')
    if repos_ext == 'True':
        repositorios_ext = RepositorioCFDI.objects.filter(naturaleza='R', tipo_comprobante='I', fecha__lt=fecha_inicio, fecha__gte=inicio_ext, importe__gt=0).order_by('rfc').values('id', 'rfc', 'nombre', 'xml', 'folio', 'importe', 'tipo_comprobante', 'taxid', 'pagado', 'integrar', 'fecha')
        repositorios_cfdi = repositorios_cfdi | repositorios_ext
    for repositorio in repositorios_cfdi:
        repositorio['pagado'] = str(repositorio['pagado'])
        repositorio['fecha'] = repositorio['fecha'].strftime('%Y/%m/%d')
        subtotal = 0
        valor_impuesto = 0
        descuento = 0
        valor_retencion_iva = 0
        repositorio['importe'] = str(repositorio['importe'])
        xml = repositorio['xml']
        if xml:
            xml = xml.encode('utf8', 'ignore')
            root = ET.fromstring(xml)
            subtotal = root.attrib['subTotal']
            if 'descuento' in root.attrib:
                descuento = root.attrib['descuento']
            impuestos = root[3]
            for impuesto in impuestos:
                if 'Retenciones' in impuesto.tag:
                    retenciones = impuesto
                    for retencion in retenciones:
                        if retencion.attrib['impuesto'] == 'IVA':
                            valor_retencion_iva = retencion.attrib['importe']

                for impuesto_detalle in impuesto:
                    datos = impuesto_detalle.attrib
                    try:
                        tasa = Decimal(datos['tasa'])
                    except Exception as e:
                        tasa = 1

                    if datos['impuesto'] == 'IVA' and tasa != 0:
                        valor_impuesto = datos['importe']

            repo_dic[repositorio['id']] = (
             repositorio, valor_impuesto, str(subtotal), str(descuento), str(valor_retencion_iva))
        else:
            repo_dic[repositorio['id']] = (
             repositorio, valor_impuesto, str(subtotal), str(descuento), str(valor_retencion_iva))

    values = repo_dic.values()
    repo_list = sorted(values, key=lambda x: x[0]['rfc'])
    p = Paginator(repo_list, 20)
    num_pages = p.num_pages
    if num_pages < int(page):
        error = True
    else:
        page1 = p.page(page)
        pagina = page1.object_list
    data = {'pagina': pagina, 'num_pages': num_pages, 
       'error': error, 
       'total': len(repo_list)}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/login/')
def CreaPaisesView(request):
    nuevos = 0
    for pais in paises_dic.items():
        pais_obj = first_or_none(Pais.objects.filter(nombre=pais[0]))
        if not pais_obj:
            nuevos += 1
            Pais.objects.create(id=-1, nombre=pais[0])

    data = {'nuevos': nuevos}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/login/')
def change_xml_status(request):
    id = request.GET['id']
    integrar = request.GET['integrar']
    repositorio = RepositorioCFDI.objects.get(id=id)
    repositorio.diot_integrar = integrar
    repositorio.save()
    data = {}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/login/')
def pago_parcial(request):
    id = request.GET['id']
    pago = Decimal(request.GET['pago'])
    repositorio = RepositorioCFDI.objects.get(id=id)
    valor = abs(pago + repositorio.diot_pagado - repositorio.importe)
    if valor < 0.05:
        repositorio.diot_pagado = repositorio.importe
    else:
        repositorio.diot_pagado = pago
    repositorio.diot_integrar = 'N'
    repositorio.save()
    data = {}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/login/')
def pago_total(request):
    id = request.GET['id']
    RepositorioCFDI.objects.filter(id=id).update(diot_pagado=F('importe'), diot_integrar='N')
    data = {}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/login/')
def inicializar_pagos(request, template_name='django_microsip_diot/inicializar_pagos.html'):
    form = InicializarPagosForm(request.POST or None)
    if form.is_valid():
        mes = form.cleaned_data['mes']
        anio = form.cleaned_data['anio']
        total = form.cleaned_data['total']
        mes_fin = int(mes) + 1
        if int(mes) == 12:
            mes_fin = 1
            anio = int(anio) + 1
        fecha_ini_str = '%02d/01/%d' % (int(mes), int(anio))
        fecha_fin_str = '%02d/01/%d' % (int(mes_fin), int(anio))
        using = router.db_for_write(Proveedor)
        c = connections[using].cursor()
        if total:
            query = "update repositorio_cfdi r set sic_diot_pagado = 0, sic_diot_iva_pagado=0, sic_diot_iva_descuentos=0, sic_diot_iva_retenido=0, sic_diot_integrar = 'N', sic_diot_mostrar='S', sic_diot_genero_ext='N' where r.naturaleza='R';"
            c.execute(query)
            query = 'delete from sic_diot_capturas;'
            c.execute(query)
        else:
            query = "update repositorio_cfdi r set sic_diot_pagado = 0, sic_diot_iva_pagado=0, sic_diot_iva_descuentos=0, sic_diot_iva_retenido=0, sic_diot_integrar = 'N', sic_diot_mostrar='S', sic_diot_genero_ext='N' where r.fecha >= %s and r.fecha < %s and r.naturaleza='R';"
            c.execute(query, [fecha_ini_str, fecha_fin_str])
            query = 'delete from sic_diot_capturas r where r.fecha >= %s and r.fecha < %s;'
            c.execute(query, [fecha_ini_str, fecha_fin_str])
        c.close()
        management.call_command('syncdb', database=using, interactive=False)
        return HttpResponseRedirect('/diot/exporta_xml/')
    else:
        c = {'form': form}
        return render_to_response(template_name, c, context_instance=RequestContext(request))


def captura_manual(request):
    id = request.GET['id_proveedor']
    folio = request.GET['folio']
    fecha = request.GET['fecha']
    importe = request.GET['importe']
    subtotal = request.GET['subtotal']
    iva_acreditable = request.GET['iva_acreditable']
    iva_no_acreditable = request.GET['iva_no_acreditable']
    iva_retenido = request.GET['iva_retenido']
    iva_descuentos = request.GET['iva_descuentos']
    proveedor = Proveedor.objects.get(id=id)
    proveedor_rfc = proveedor.rfc_curp
    CapturaManual.objects.create(folio=folio, fecha=fecha, proveedor=proveedor, importe=importe, subtotal=subtotal, iva=iva_acreditable, iva_no_acreditable=iva_no_acreditable, iva_retenido=iva_retenido, iva_descuentos=iva_descuentos)
    nombre = proveedor.nombre
    data = {'proveedor_rfc': proveedor_rfc, 
       'nombre': nombre}
    return HttpResponse(json.dumps(data), mimetype='application/json')


def ocultar_repo(request):
    id = request.GET['id']
    manual = request.GET['manual']
    if manual == '1':
        repo = CapturaManual.objects.get(id=id)
        repo.mostrar = 'N'
    else:
        repo = RepositorioCFDI.objects.get(id=id)
        repo.diot_mostrar = 'N'
    repo.save()
    data = {}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/login/')
def guardar_repositorio(request):
    id = request.GET['id']
    iva_descuentos = Decimal(request.GET['iva_descuentos'])
    iva_retenido = Decimal(request.GET['iva_retenido'])
    iva_pagado = Decimal(request.GET['iva_pagado'])
    iva = Decimal(request.GET['iva'])
    repositorio = RepositorioCFDI.objects.get(id=id)
    repositorio.diot_iva = iva
    repositorio.diot_iva_descuentos = repositorio.diot_iva_descuentos + iva_descuentos
    if repositorio.diot_iva_pagado + iva_pagado <= repositorio.diot_iva:
        repositorio.diot_iva_pagado = repositorio.diot_iva_pagado + iva_pagado
    else:
        repositorio.diot_iva_pagado = repositorio.diot_iva
    repositorio.diot_iva_retenido = repositorio.diot_iva_retenido + iva_retenido
    repositorio.save()
    data = {}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/login/')
def exporta_excel(request):
    tabla = request.GET['tabla']
    nombre_doc = request.GET['nombre_doc']
    tabla = json.loads(tabla)
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s.xls' % nombre_doc
    wb = xlwt.Workbook()
    ws = wb.add_sheet('DIOT')
    ws.row(0).write(0, 'FECHA')
    ws.row(0).write(1, 'FOLIO')
    ws.row(0).write(2, 'NOMBRE')
    ws.row(0).write(3, 'RFC')
    ws.row(0).write(4, 'PAGADO')
    ws.row(0).write(5, 'IMPORTE')
    ws.row(0).write(6, 'IVA')
    ws.row(0).write(7, 'IVA DESCUENTOS')
    ws.row(0).write(8, 'IVA RETENIDO')
    r = 1
    for detalle in tabla:
        ws.row(r).write(0, detalle[0])
        ws.row(r).write(1, detalle[1])
        ws.row(r).write(2, detalle[2])
        ws.row(r).write(3, detalle[3])
        ws.row(r).write(4, detalle[4])
        ws.row(r).write(5, detalle[5])
        ws.row(r).write(6, detalle[6])
        ws.row(r).write(7, detalle[7])
        ws.row(r).write(8, detalle[8])
        r += 1

    wb.save(response)
    return response


@login_required(login_url='/login/')
def genero_ext(request):
    id = request.GET['id']
    repo = RepositorioCFDI.objects.get(id=id)
    repo.diot_genero_ext = 'S'
    repo.save()
    data = {}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/login/')
def importar_xml(request, template_name='django_microsip_diot/herramientas/importar_xml.html'):
    if 'file' in request.FILES.keys():
        nombre_xml = request.FILES['file'].name
        xml_str = request.FILES['file'].read().decode('ascii', 'ignore').encode('utf8', 'ignore')
        root = ET.fromstring(xml_str)
        namespaces = {'cfdi': 'http://www.sat.gob.mx/cfd/3', 'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'}
        rfc_empresa = re.sub('\\W+', '', Registry.objects.get(nombre='Rfc').valor)
        receptor_rfc = root.find('cfdi:Receptor', namespaces).attrib['rfc']
        uuid = root.find('cfdi:Complemento', namespaces).find('tfd:TimbreFiscalDigital', namespaces).attrib['UUID']
        exists_repo = RepositorioCFDI.objects.filter(uuid=uuid).exists()
        if rfc_empresa == receptor_rfc and not exists_repo:
            emisor_rfc = root.find('cfdi:Emisor', namespaces).attrib['rfc']
            emisor_nombre = root.find('cfdi:Emisor', namespaces).attrib['nombre']
            importe = root.attrib['total']
            moneda = root.attrib['Moneda']
            if 'TipoCambio' in root.attrib:
                tipo_cambio = root.attrib['TipoCambio']
            else:
                tipo_cambio = 1
            tipo_comprobante = root.attrib['tipoDeComprobante']
            if tipo_comprobante == 'ingreso':
                tipo_comprobante = 'I'
            else:
                tipo_comprobante = 'E'
            if 'folio' in root.attrib and 'serie' in root.attrib:
                folio = root.attrib['serie'] + root.attrib['folio']
            else:
                folio = None
            fecha = root.attrib['fecha'].split('T')[0]
            RepositorioCFDI.objects.create(id=-1, modalidad_facturacion='CFDI', uuid=uuid, naturaleza='R', tipo_comprobante=tipo_comprobante, microsip_documento_tipo='Factura', folio=folio, fecha=fecha, rfc=emisor_rfc, taxid=None, nombre=emisor_nombre, importe=importe, moneda=moneda, tipo_cambio=tipo_cambio, es_parcialidad='N', archivo_nombre=nombre_xml, xml=xml_str, refer_grupo=None, sello_validado='M', diot_integrar='S', diot_mostrar='S', diot_genero_ext='N')
            data = {'files': request.FILES['file']}
            response = JSONResponse(data, mimetype=response_mimetype(self.request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


def cargar_pago(request):
    msg = ''
    id = request.GET['id']
    importe = Decimal(request.GET['importe'])
    iva = Decimal(request.GET['iva'])
    pago_total = 0
    using = router.db_for_write(Proveedor)
    c = connections[using].cursor()
    query = "select sum(dcd.importe) as total, min(dc.poliza) as folio, min(dc.docto_co_id) as id from repositorio_cfdi r join\n        doctos_co_cfdi dcc on r.cfdi_id = dcc.cfdi_id join\n        doctos_co_det_cfdi dcdf on dcdf.docto_co_cfdi_id = dcc.docto_co_cfdi_id join\n        doctos_co_det dcd on dcd.docto_co_det_id = dcdf.docto_co_det_id join\n        doctos_co dc on dc.docto_co_id = dcd.docto_co_id\n        where r.cfdi_id = %s\n        and dc.estatus = 'N';" % id
    c.execute(query)
    total = c.fetchall()
    total, folio, poliza_id = total[0]
    if total:
        if abs(total - importe) < 1 or total > importe:
            total = total + iva
            pago_total = 1
    else:
        query = "select sum(dcd.importe) as total, min(dc.poliza) as folio, min(dc.docto_co_id) as id from repositorio_cfdi r join\n            doctos_co_cfdi dcc on r.cfdi_id = dcc.cfdi_id join\n            doctos_co dc on dc.docto_co_id = dcc.docto_co_id join\n            doctos_co_det dcd on dcd.docto_co_id = dc.docto_co_id\n            where r.cfdi_id = %s and dcd.tipo_asiento = 'C'\n            and dc.estatus = 'N';" % id
        c.execute(query)
        total = c.fetchall()
        total, folio, poliza_id = total[0]
    if abs(total - (importe + iva)) > 1:
        query = 'select sum(rc.importe) from doctos_co dc join\n            doctos_co_cfdi dcc on dcc.docto_co_id = dc.docto_co_id join\n            repositorio_cfdi rc on rc.cfdi_id = dcc.cfdi_id\n            where dc.docto_co_id = %s;' % poliza_id
        c.execute(query)
        total_xmls = c.fetchall()[0][0]
        if abs(total_xmls - total) < 1:
            pago_total = 1
            total = importe
        elif total < importe:
            total = total
        else:
            msg = folio
    else:
        pago_total = 1
    import locale
    locale.setlocale(locale.LC_ALL, '')
    total = locale.currency(total, grouping=True).replace('$', '')
    data = {'total': total, 'pago_total': pago_total, 'msg': msg}
    return HttpResponse(json.dumps(data), mimetype='application/json')


def info_poliza_xml(request):
    id = request.GET['id']
    using = router.db_for_write(Proveedor)
    c = connections[using].cursor()
    query = 'select dc.docto_co_id as id, dc.poliza, dc.descripcion, dc.fecha, tp.nombre as tipo from doctos_co dc join\n        doctos_co_cfdi dcc on dcc.docto_co_id = dc.docto_co_id join\n        repositorio_cfdi rc on rc.cfdi_id = dcc.cfdi_id join\n        tipos_polizas tp on tp.tipo_poliza_id = dc.tipo_poliza_id\n        where rc.cfdi_id = %s' % id
    c.execute(query)
    info = c.fetchall()
    id = info[0][0]
    folio = info[0][1]
    descripcion = info[0][2]
    fecha = info[0][3]
    tipo = info[0][4]
    fecha_str = fecha.strftime('%d/%m/%Y')
    using = router.db_for_write(Proveedor)
    c = connections[using].cursor()
    query = "select sum(dcd.importe) from doctos_co dc join\n        doctos_co_det dcd on dcd.docto_co_id = dc.docto_co_id\n        where dc.docto_co_id = %s and dcd.tipo_asiento ='C';" % id
    c.execute(query)
    importe_poliza = c.fetchall()[0][0]
    import locale
    locale.setlocale(locale.LC_ALL, '')
    importe_poliza = locale.currency(importe_poliza, grouping=True).replace('$', '')
    data = {'importe_poliza': importe_poliza, 
       'folio': folio, 
       'descripcion': descripcion, 
       'fecha_str': fecha_str, 
       'tipo': tipo}
    return HttpResponse(json.dumps(data), mimetype='application/json')