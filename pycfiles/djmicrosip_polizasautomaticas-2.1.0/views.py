# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_polizasautomaticas\djmicrosip_polizasautomaticas\views.py
# Compiled at: 2018-07-05 12:06:11
from .forms import *
from .models import *
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import management
from django.db import connections, router
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from microsip_api.comun.sic_db import first_or_none, next_id
from microsip_api.comun.comun_functions import get_short_folio, split_letranumero
from .custom_db.contabilidad.procedures import sql_procedures
import json
from decimal import Decimal
if 'djmicrosip_tareas' in settings.EXTRA_MODULES:
    from djmicrosip_tareas.models import ProgrammedTask
    from djmicrosip_tareas.models import PendingTask

def tuncateRoundOff(number, decimals):
    before_dec, after_dec = str(number).split('.')
    return float(('.').join((before_dec, after_dec[0:decimals])))


@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_polizasautomaticas/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def preferencias_view(request, template_name='djmicrosip_polizasautomaticas/preferencias.html'):
    c = {'errors': []}
    if 'djmicrosip_tareas' in settings.EXTRA_MODULES:
        from djmicrosip_tareas.models import ProgrammedTask
        form_initial = {'integrar_contabilidad': Registry.objects.get(nombre='SIC_POLIZAS_AUTOMATICAS_integrar_contabilidad').get_value() == 'True', 'ventas_tipodocumento': Registry.objects.get(nombre='SIC_POLIZAS_AUTOMATICAS_tipo_ve').get_value(), 
           'puntodeventa_tipodocumento': Registry.objects.get(nombre='SIC_POLIZAS_AUTOMATICAS_tipo_pv').get_value(), 
           'crear_polizas_como_pendientes': Registry.objects.get(nombre='SIC_POLIZAS_AUTOMATICAS_pendientes').get_value() == 'True', 
           'permitir_modificar_polizas': Registry.objects.get(nombre='SIC_POLIZAS_AUTOMATICAS_modificar').get_value() == 'True'}
        task = first_or_none(ProgrammedTask.objects.filter(description='Polizas Automaticas')) or ProgrammedTask()
        form = ProgrammedTaskForm(request.POST or None, initial=form_initial, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            if not task.id:
                task.description = 'Polizas Automaticas'
                task.command_type = 'http'
                task.command = 'http://127.0.0.1:8001/polizas_automaticas/crear_polizas/'
            form.save()
            c['msg'] = 'Informacion actualizada'
        c['form'] = form
    else:
        c['errors'].append('Por favor instalarla para poder configurar esta opción')
    return render_to_response(template_name, c, context_instance=RequestContext(request))


def SeparaVentas(request, template_name='djmicrosip_polizasautomaticas/separaventas.html'):
    documentos_validos = 0
    exe = False
    form = SeparaVentasForm(request.POST or None)
    if form.is_valid():
        exe = True
        cuenta_ventas = form.cleaned_data['cuenta_venta']
        cuenta_ventas_iva = form.cleaned_data['cuenta_ventas_impuesto']
        cuenta_ventas_exentas = form.cleaned_data['cuenta_ventas_exenta']
        fecha_inicio = form.cleaned_data['start_date']
        fecha_fin = form.cleaned_data['end_date']
        documentos = ContabilidadDocumento.objects.filter(fecha__lte=fecha_fin, fecha__gte=fecha_inicio, estatus='P', sic_referencia__contains='#').exclude(descripcion__contains='V_S')
        cuentas_clientes = {}
        cuentas_clientes['ventas'] = cuenta_ventas
        cuentas_clientes['ventas_impuestos'] = cuenta_ventas_iva
        cuentas_clientes['ventas_exentas'] = cuenta_ventas_exentas
        documentos_con_clientes_invalidos = []
        cuenta_cobros = first_or_none(ContabilidadCuentaContable.objects.filter(cuenta=Registry.objects.get(nombre='CUENTA_COBROS').valor))
        for documento in documentos:
            detalle = first_or_none(documento.contabilidaddocumentodetalle_set.filter(cuenta=cuenta_ventas))
            if detalle and detalle.ref:
                serie, consecutivo = split_letranumero(detalle.ref)
                folio_documento = '%s%s' % (serie, ('%09d' % int(consecutivo))[len(serie):])
                documento_pv = PuntoVentaDocumento.objects.get(folio=folio_documento, tipo='F')
                documento_pv = first_or_none(PuntoVentaDocumentoLiga.objects.filter(docto_pv_destino=documento_pv)).docto_pv_fuente
                cliente = documento_pv.cliente
                if cuenta_ventas_iva and cuenta_ventas_exentas:
                    documento_impuestos = PuntoVentaDocumentoImpuesto.objects.filter(documento_pv=documento_pv, impuesto__tipoImpuesto__nombre='IVA').values_list('venta_neta', 'porcentaje_impuestos', 'otros_impuestos')
                    ventas_iva = 0
                    ventas_exentas = 0
                    otros_impuestos = 0
                    tipo_cambio = 1
                    for documento_impuesto in documento_impuestos:
                        porcentaje = documento_impuesto[1]
                        venta_neta = documento_impuesto[0] * tipo_cambio
                        otros_impuestos += documento_impuesto[2] * tipo_cambio
                        if porcentaje == 0:
                            ventas_exentas += venta_neta
                        else:
                            ventas_iva += venta_neta

                    if ventas_exentas + ventas_iva < documento_pv.importe_neto * tipo_cambio:
                        ventas_exentas += documento_pv.importe_neto * tipo_cambio - ventas_iva - ventas_exentas
                    detalle_asiento_clientes = None
                    if cuentas_clientes['ventas']:
                        detalle_asiento_clientes = first_or_none(documento.contabilidaddocumentodetalle_set.filter(cuenta=cuentas_clientes['ventas']))
                    if ventas_exentas > 0:
                        ContabilidadDocumentoDetalle.objects.create(id=-1, docto_co=documento, cuenta=cuenta_ventas_exentas, depto_co=detalle.depto_co, tipo_asiento=detalle.tipo_asiento, importe=ventas_exentas, importe_mn=0, ref=detalle.ref, descripcion=detalle.descripcion, posicion=-1, fecha=detalle.fecha, cancelado=detalle.cancelado, aplicado=detalle.aplicado, ajuste=detalle.ajuste, moneda=detalle.moneda)
                    if ventas_iva > 0:
                        ContabilidadDocumentoDetalle.objects.create(id=-1, docto_co=documento, cuenta=cuenta_ventas_iva, depto_co=detalle.depto_co, tipo_asiento=detalle.tipo_asiento, importe=ventas_iva, importe_mn=0, ref=detalle.ref, descripcion=detalle.descripcion, posicion=-1, fecha=detalle.fecha, cancelado=detalle.cancelado, aplicado=detalle.aplicado, ajuste=detalle.ajuste, moneda=detalle.moneda)
                    ventas_impuestos_total = documento_pv.total_impuestos
                    cliente_ventas_iva = Decimal(str(round(ventas_iva, 2))) + ventas_impuestos_total
                    cliente_ventas_iva = Decimal(tuncateRoundOff(cliente_ventas_iva, 2))
                    cliente_ventas_exentas = ventas_exentas
                    detalle.delete()
                    documento.descripcion += ' %s V_S' % documento_pv.cliente.nombre
                    if otros_impuestos > 0:
                        documento.descripcion += 'ARTICULOS CON IEPS E IVA: %s' % otros_impuestos
                    documento.save(update_fields=['descripcion'])
                    documentos_validos += 1
                    detalles = ContabilidadDocumentoDetalle.objects.filter(docto_co=documento)
                    using = router.db_for_write(ContabilidadDocumentoDetalle)
                    c = connections[using].cursor()
                    c.execute('Select docto_co_cfdi_id from doctos_co_cfdi where docto_co_id = %s' % documento.id)
                    liga_cfdi = c.fetchall()
                    if len(liga_cfdi) > 0:
                        liga_cfdi = liga_cfdi[0][0]
                        c = connections[using].cursor()
                        c.execute("update doctos_co_cfdi set es_global='N' where docto_co_cfdi_id = %s" % liga_cfdi)
                        c.close()
                        management.call_command('syncdb', database=using, interactive=False)
                        for det in detalles:
                            c = connections[using].cursor()
                            c.execute('INSERT INTO DOCTOS_CO_DET_CFDI VALUES (%s,%s)' % (det.id, liga_cfdi))
                            c.close()
                            management.call_command('syncdb', database=using, interactive=False)

                else:
                    documentos_con_clientes_invalidos.append(documento.poliza)
            else:
                documentos_con_clientes_invalidos.append(documento.poliza)

    context = {'exe': exe, 'num_documentos_procesados': documentos_validos, 
       'form': form}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def UpdateDatabaseView(request):
    if request.user.is_superuser:
        using = router.db_for_write(Registry)
        management.call_command('syncdb', database=using, interactive=False)
        c = connections[using].cursor()
        from custom_db.punto_de_venta import sql_queries
        for query in sql_queries.triggers_activate:
            c.execute(sql_queries.triggers_activate[query])

        from custom_db.ventas import sql_queries
        for query in sql_queries.triggers_activate:
            c.execute(sql_queries.triggers_activate[query])

        c.close()
        c = connections[using].cursor()
        c.execute(sql_procedures['SIC_CONTABILIDAD_POLIZASAUTO'])
        c.execute('EXECUTE PROCEDURE SIC_CONTABILIDAD_POLIZASAUTO;')
        c.execute('DROP PROCEDURE SIC_CONTABILIDAD_POLIZASAUTO;')
        c.execute('GRANT ALL ON SIC_PENDINGTASK TO USUARIO_MICROSIP')
        from config import configuration_registers
        for register in configuration_registers:
            padre = first_or_none(Registry.objects.filter(nombre='PreferenciasEmpresa'))
            if padre:
                if not Registry.objects.filter(nombre=register).exists():
                    Registry.objects.create(nombre=register, tipo='V', padre=padre, valor='-')

        task_name = 'Polizas Automaticas'
        if not ProgrammedTask.objects.filter(description=task_name).exists():
            ProgrammedTask.objects.create(description=task_name, command_type='http', command='http://127.0.0.1:8001/polizas_automaticas/crear_polizas/', period_start_datetime=datetime.now(), period_quantity=1, period_unit='minutes', status='Activo', next_execution=datetime.now())
        using = router.db_for_write(Registry)
        management.call_command('syncdb', database=using, interactive=False)
    return HttpResponseRedirect('/polizas_automaticas/preferencias')


@login_required(login_url='/login/')
def recalculo_view(request, template_name='djmicrosip_polizasautomaticas/recalculo.html'):
    form = GeneraAnterioresForm(request.POST or None)
    contador = 0
    exe = False
    if form.is_valid():
        exe = True
        f_ini = form.cleaned_data['start_date']
        f_fin = form.cleaned_data['end_date']
        documentos = ContabilidadDocumento.objects.filter(sic_referencia__contains='#', fecha__gte=f_ini, fecha__lte=f_fin)
        for documento in documentos:
            try:
                using = router.db_for_write(ContabilidadDocumento)
                c = connections[using].cursor()
                query = "execute procedure APLICA_DOCTO_CO(%s, 'D');" % documento.id
                c.execute(query)
                c.close()
                documento.aplicado = 'N'
                documento.save()
                query = "execute procedure APLICA_DOCTO_CO(%s, 'A');" % documento.id
                c.execute(query)
                c.close()
                documento.aplicado = 'S'
                documento.save()
                detalles = ContabilidadDocumentoDetalle.objects.filter(docto_co=documento)
                for detalle in detalles:
                    query = 'execute procedure RECALC_SALDOS_CTA_CO(%s);' % detalle.cuenta.id
                    c.execute(query)
                    c.close()

            except Exception as e:
                contador = contador + 1

    c = {'contador': contador, 
       'form': form, 
       'exe': exe}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


def crea_asientos_temporales(modulo, documento_id, tipo_documento):
    """ SE CREAN LOS ASIENTOS TEMPORALES CON UN PROCEDIMIENTO """
    using = router.db_for_write(Registry)
    proceso_id = next_id('ID_REPORTES', using)
    c = connections[using].cursor()
    if modulo == 'VE':
        query = ("EXECUTE PROCEDURE GEN_POLIZA_DOCTO_VE({},'D',{})").format(documento_id, proceso_id)
        c.execute(query)
    elif modulo == 'PV':
        if tipo_documento == 'F':
            ids = get_doctos_fte(documento_id)
            for id in ids:
                query = ('EXECUTE PROCEDURE GEN_POLIZA_DOCTO_PV({},{})').format(id, proceso_id)
                print query
                c.execute(query)

        else:
            query = ('EXECUTE PROCEDURE GEN_POLIZA_DOCTO_PV({},{})').format(documento_id, proceso_id)
            c.execute(query)
    elif modulo == 'CM':
        query = ("EXECUTE PROCEDURE GEN_POLIZA_DOCTO_CM({},'D',{})").format(documento_id, proceso_id)
        c.execute(query)
    c.close()
    return proceso_id


def get_doctos_fte(docto_dest_id):
    using = router.db_for_write(Registry)
    c = connections[using].cursor()
    query = 'SELECT DP.DOCTO_PV_ID FROM DOCTOS_PV DP JOIN\n        DOCTOS_PV_LIGAS DPL ON DPL.docto_pv_fte_id = DP.docto_pv_id JOIN\n        DOCTOS_PV DP2 ON DP2.docto_pv_id = DPL.docto_pv_dest_id\n        WHERE DP2.docto_pv_id = %s;' % docto_dest_id
    c.execute(query)
    ids = c.fetchall()
    ids = map(lambda x: x[0], ids)
    print ids
    return ids


def get_docto_origen(devolucion_id, modulo):
    using = router.db_for_write(Registry)
    c = connections[using].cursor()
    query = ('select dv.folio from doctos_{0} dv join\n        doctos_{0}_ligas dvl on dvl.docto_{0}_fte_id = dv.docto_{0}_id join\n        doctos_{0} dv2 on dv2.docto_{0}_id = dvl.docto_{0}_dest_id\n        where dv2.docto_{0}_id = {1};').format(modulo, devolucion_id)
    c.execute(query)
    result = c.fetchall()
    if result:
        return result[0][0]
    else:
        return
        return


def set_cfdi_docto_co(proceso_id, docto_id, docto_co_id):
    using = router.db_for_write(Registry)
    c = connections[using].cursor()
    query = ('execute procedure alta_doctos_co_cfdi({0}, {1}, {2});').format(proceso_id, docto_id, docto_co_id)
    c.execute(query)


@login_required(login_url='/login/')
def crear_polizas_view(request):
    count = 0
    pendientes = PendingTask.objects.filter(app='POLIZASAUTOMATICAS')
    crear_como_pendiente = Registry.objects.get(nombre='SIC_POLIZAS_AUTOMATICAS_pendientes').get_value() == 'True'
    if crear_como_pendiente:
        estatus = 'P'
    else:
        estatus = 'N'
    permitir_modificar_polizas = Registry.objects.get(nombre='SIC_POLIZAS_AUTOMATICAS_modificar').get_value() == 'True'
    print len(pendientes)
    for pendiente in pendientes:
        count += 1
        print str(count)
        poliza_descripcion = ''
        sic_referencia = ''
        documento = None
        folio = json.loads(pendiente.parameters)['FOLIO']
        tipo_documento = json.loads(pendiente.parameters)['TIPO_DOCUMENTO']
        if pendiente.type == 'VE':
            documento = first_or_none(VentasDocumento.objects.filter(tipo=tipo_documento, folio=folio))
        else:
            if pendiente.type == 'PV':
                documento = first_or_none(PuntoVentaDocumento.objects.filter(tipo=tipo_documento, folio=folio))
            elif pendiente.type == 'CM':
                documento = first_or_none(ComprasDocumento.objects.filter(tipo=tipo_documento, folio=folio))
            try:
                if documento:
                    tipo_poliza = ''
                    if pendiente.type == 'VE':
                        if documento.tipo == 'D':
                            tipo_poliza = Registry.objects.get(nombre='TIPO_POLIZA_DEVOL').get_value()
                            poliza_descripcion = Registry.objects.get(nombre='DESCRIPCION_POLIZA_DEVOL').get_value()
                            if get_docto_origen(documento.id, 'VE'):
                                poliza_descripcion += '. Devolucion de: ' + get_docto_origen(documento.id, 'VE') + '. '
                        else:
                            tipo_poliza = Registry.objects.get(nombre='TIPO_POLIZA_VENTAS').get_value()
                            poliza_descripcion = Registry.objects.get(nombre='DESCRIPCION_POLIZA_VENTAS').get_value()
                    elif pendiente.type == 'PV':
                        if documento.tipo == 'D':
                            tipo_poliza = Registry.objects.get(nombre='TIPO_POLIZA_DEVOL_PV').get_value()
                            poliza_descripcion = Registry.objects.get(nombre='DESCRIPCION_POLIZA_DEVOL_PV').get_value()
                            if get_docto_origen(documento.id, 'PV'):
                                poliza_descripcion += '. Devolucion de: ' + get_docto_origen(documento.id, 'PV') + '. '
                        else:
                            tipo_poliza = Registry.objects.get(nombre='TIPO_POLIZA_VENTAS_PV').get_value()
                            poliza_descripcion = Registry.objects.get(nombre='DESCRIPCION_POLIZA_VENTAS_PV').get_value()
                    elif pendiente.type == 'CM':
                        if documento.tipo == 'D':
                            tipo_poliza = Registry.objects.get(nombre='TIPO_POLIZA_DEVOL_CM').get_value()
                            poliza_descripcion = Registry.objects.get(nombre='DESCRIPCION_POLIZA_DEVOL_CM').get_value()
                            if get_docto_origen(documento.id, 'CM'):
                                poliza_descripcion += '. Devolucion de: ' + get_docto_origen(documento.id, 'CM') + '. '
                        else:
                            tipo_poliza = Registry.objects.get(nombre='TIPO_POLIZA_COMPRAS').get_value()
                            poliza_descripcion = Registry.objects.get(nombre='DESCRIPCION_POLIZA_COMPRAS').get_value()
                    proceso_id = crea_asientos_temporales(pendiente.type, documento.id, documento.tipo)
                    asientos_temporales = ContabilidadPoliza.objects.filter(proceso=proceso_id)
                    folio = get_short_folio(folio)
                    poliza_descripcion += ' #' + pendiente.type + '-' + tipo_documento + '-' + folio + '#'
                    sic_referencia = ' #' + pendiente.type + '-' + tipo_documento + '-' + folio + '#'
                    existe_poliza = ContabilidadDocumento.objects.filter(sic_referencia__contains=sic_referencia, estatus__in=['N', 'P']).exists()
                    if not existe_poliza:
                        if permitir_modificar_polizas:
                            sistema_origen = 'CO'
                        else:
                            sistema_origen = pendiente.type
                        tipo_poliza = TipoPoliza.objects.get(clave=tipo_poliza)
                        poliza = ContabilidadDocumento.objects.create(tipo_poliza=tipo_poliza, fecha=documento.fecha, estatus=estatus, aplicado='N', moneda=documento.moneda, descripcion=poliza_descripcion, tipo_cambio=documento.tipo_cambio, sistema_origen=sistema_origen, sic_referencia=sic_referencia)
                        for asiento in asientos_temporales:
                            tipos_asiento = {'D': 'C', 
                               'H': 'A'}
                            cuenta = ContabilidadCuentaContable.objects.get(cuenta=asiento.cuenta)
                            departamento = ContabilidadDepartamento.objects.get(clave='GRAL')
                            tipo_asiento = tipos_asiento[asiento.tipo_asiento]
                            if not asiento.posicion:
                                posicion = -1
                            else:
                                posicion = asiento.posicion
                            ContabilidadDocumentoDetalle.objects.create(id=-1, docto_co=poliza, cuenta=cuenta, depto_co=departamento, tipo_asiento=tipo_asiento, importe=asiento.importe, importe_mn=asiento.importe, ref=documento.folio, posicion=posicion, fecha=documento.fecha, moneda=documento.moneda)

                        if pendiente.type == 'PV' and documento.tipo == 'F':
                            ids = get_doctos_fte(documento.id)
                            for id in ids:
                                set_cfdi_docto_co(proceso_id, id, poliza.id)

                        else:
                            set_cfdi_docto_co(proceso_id, documento.id, poliza.id)
                        asientos_temporales.delete()
            except Exception as e:
                print 'x'
                pendiente.intents = pendiente.intents + 1
                pendiente.save()
                message = str(e.args[0].split('- At procedure'))
                if len(message) > 1:
                    message = message[0]
                message = message.replace('@', ' ')
                if not Log.objects.filter(app='POLIZASAUTOMATICAS', message=message).exists():
                    Log.objects.create(app='POLIZASAUTOMATICAS', message=message)

            pendiente.delete()

    return HttpResponseRedirect('/polizas_automaticas/')


@login_required(login_url='/login/')
def crea_anteriores_view(request, template_name='djmicrosip_polizasautomaticas/crea_anteriores.html'):
    form = GeneraAnterioresForm(request.POST or None)
    cantidad_documentos = 0
    error = ''
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        tipo_pv = Registry.objects.get(nombre='SIC_POLIZAS_AUTOMATICAS_tipo_pv').get_value()
        tipo_pv_list = [tipo_pv]
        if not tipo_pv == '-':
            tipo_pv_list.append('D')
        tipo_ventas = Registry.objects.get(nombre='SIC_POLIZAS_AUTOMATICAS_tipo_ve').get_value()
        tipo_ventas_list = [tipo_ventas]
        if not tipo_ventas == '-':
            tipo_ventas_list.append('D')
        documentos_pv = PuntoVentaDocumento.objects.filter(tipo__in=tipo_pv_list, fecha__gte=start_date, fecha__lte=end_date, estado='N').order_by('fecha')
        documentos_ventas = VentasDocumento.objects.filter(tipo__in=tipo_ventas_list, fecha__gte=start_date, fecha__lte=end_date, estado='N').order_by('fecha')
        if len(documentos_ventas) > 0 or len(documentos_pv) > 0:
            try:
                for documento_pv in documentos_pv:
                    parameters = '{"FOLIO":"' + documento_pv.folio + '","TIPO_DOCUMENTO":"' + documento_pv.tipo + '"}'
                    if not PendingTask.objects.filter(type='PV', app='POLIZASAUTOMATICAS', parameters=parameters).exists():
                        PendingTask.objects.create(type='PV', app='POLIZASAUTOMATICAS', parameters=parameters, intents=0)
                        cantidad_documentos += 1

                for documento_ventas in documentos_ventas:
                    parameters = '{"FOLIO":"' + documento_ventas.folio + '","TIPO_DOCUMENTO":"' + documento_ventas.tipo + '"}'
                    if not PendingTask.objects.filter(type='VE', app='POLIZASAUTOMATICAS', parameters=parameters).exists():
                        PendingTask.objects.create(type='VE', app='POLIZASAUTOMATICAS', parameters=parameters, intents=0)
                        cantidad_documentos += 1

                if cantidad_documentos == 0:
                    error = 'No hay Documentos por Generar en este periodo'
            except Exception:
                error = 'Error al generar pólizas'

        else:
            error = 'No hay Documentos por Generar en este periodo'
    c = {'form': form, 'error': error, 'cantidad_documentos': cantidad_documentos}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def log_view(request, template_name='djmicrosip_polizasautomaticas/log.html'):
    errores = Log.objects.filter(app='POLIZASAUTOMATICAS').order_by('-creation')
    c = {'errores': errores}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


def elimina_log_view(request):
    id = request.POST['id']
    log = Log.objects.get(id=id)
    log.delete()
    data = {}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/login/')
def reemplaza_view(request, template_name='djmicrosip_polizasautomaticas/reemplaza.html'):
    form = ReemplazaCuentaForm(request.POST or None)
    canceladas = []
    exe = False
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        cuenta_iva_contado = form.cleaned_data['cuenta_iva_contado']
        cuenta_iva_credito = form.cleaned_data['cuenta_iva_credito']
        polizas = ContabilidadDocumento.objects.filter(fecha__gte=start_date, fecha__lte=end_date, sic_referencia__contains='#')
        for poliza in polizas:
            modulo = poliza.sic_referencia.split('-')[0].strip().replace('#', '')
            tipo = poliza.sic_referencia.split('-')[1]
            serie, num = split_letranumero(poliza.sic_referencia.split('-')[2].replace('#', ''))
            folio = serie + str(num).zfill(9 - len(serie))
            if modulo == 'PV':
                documento = PuntoVentaDocumento.objects.get(folio=folio, tipo=tipo)
            try:
                if tipo == 'F':
                    documento = first_or_none(PuntoVentaDocumentoLiga.objects.filter(docto_pv_destino=documento)).docto_pv_fuente
                cobro = PuntoVentaCobro.objects.filter(documento_pv=documento)[0].forma_cobro.tipo
                if cobro == 'R':
                    detalles = ContabilidadDocumentoDetalle.objects.filter(docto_co=poliza, cuenta=cuenta_iva_contado)
                    for detalle in detalles:
                        detalle.cuenta = cuenta_iva_credito
                        detalle.save()

            except Exception as e:
                canceladas.append(folio)

        exe = True
    c = {'form': form, 'exe': exe, 'canceladas': canceladas}
    return render_to_response(template_name, c, context_instance=RequestContext(request))