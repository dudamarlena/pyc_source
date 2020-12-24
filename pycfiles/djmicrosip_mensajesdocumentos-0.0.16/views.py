# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_mensajesdocumentos\djmicrosip_mensajesdocumentos\views.py
# Compiled at: 2015-09-03 19:05:22
from .models import *
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import management
from django.db import router, connections
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from forms import PreferenciasManageForm
from microsip_api.apps.sms.core import SMSMasivo
from microsip_api.comun.sic_db import first_or_none
import json, re
from microsip_api.comun.comun_functions import get_short_folio
modo_pruebas = settings.MODO_SERVIDOR == 'PRUEBAS'

def validate_particularFields():
    using = router.db_for_write(Almacen)
    c = connections[using].cursor()
    errors = []
    from config import campos_particulares_tablas
    for campos_particulares_tabla in campos_particulares_tablas:
        tabla = campos_particulares_tabla['tabla']
        campos = campos_particulares_tabla['campos']
        for campo in campos:
            query = ("select 1 from RDB$RELATION_FIELDS rf where rf.RDB$RELATION_NAME = '{}' and rf.RDB$FIELD_NAME = '{}' ").format(tabla, campo)
            c.execute(query)
            existe = c.fetchall() != []
            if not existe:
                errors.append(('Es necesario Crear el campo particular [{}] par la tabla [{}]').format(campo, tabla))

    c.close()
    is_valid = len(errors) == 0
    return (is_valid, errors)


def app_isvalid():
    errors = []
    if 'djmicrosip_tareas' not in settings.EXTRA_MODULES:
        errors.append('La aplicación de tareas es obligatoria para utilizar esta aplicación')
    campos_is_valid, campos_errors = validate_particularFields()
    if not campos_is_valid:
        for error in campos_errors:
            errors.append(error)

    return errors


@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_mensajesdocumentos/index.html'):
    errors = app_isvalid()
    c = {'errors': errors}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def preferencias_manageview(request, template_name='djmicrosip_mensajesdocumentos/preferencias.html'):
    msg = ''
    form_initial = {'empresa_nombre': Registry.objects.get(nombre='SIC_SMS_NombreEmpresa').get_value(), 
       'telefono_default': Registry.objects.get(nombre='SIC_SMS_TelDefault').get_value(), 
       'ventas_tipodocumento': Registry.objects.get(nombre='SIC_MensajeDocumentos_VentasTipoDocumento').get_value(), 
       'puntodeventa_tipodocumento': Registry.objects.get(nombre='SIC_MensajeDocumentos_PuntoVentaTipoDocumento').get_value(), 
       'apikey': Registry.objects.get(nombre='SIC_SMS_ApiKey').get_value(), 
       'monto_minimo': Registry.objects.get(nombre='SIC_SMS_MontoMinimo').get_value()}
    form = PreferenciasManageForm(request.POST or None, initial=form_initial)
    if form.is_valid():
        form.save()
        msg = 'Datos guardados correctamente'
    c = {'form': form, 'msg': msg}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def preparar_aplicacion(request):
    using = router.db_for_write(Almacen)
    management.call_command('syncdb', database=using, interactive=False)
    from custom_db.punto_venta import sql_queries
    c = connections[using].cursor()
    for query in sql_queries.triggers_activate:
        c.execute(sql_queries.triggers_activate[query])

    from custom_db.ventas import sql_queries
    for query in sql_queries.triggers_activate:
        c.execute(sql_queries.triggers_activate[query])

    c.close()
    from config import configuration_registers
    for register in configuration_registers:
        padre = first_or_none(Registry.objects.filter(nombre='PreferenciasEmpresa'))
        if not Registry.objects.filter(nombre=register).exists():
            Registry.objects.create(nombre=register, tipo='V', padre=padre, valor='')

    task_name = 'Mensajes Documentos SMS'
    if not ProgrammedTask.objects.filter(description=task_name).exists():
        ProgrammedTask.objects.create(description=task_name, command_type='http', command='http://127.0.0.1:8001/mensajesdocumentos/send_messages/', period_start_datetime=datetime.now(), period_quantity=1, period_unit='minuto', status='Activo', next_execution=datetime.now())
    management.call_command('syncdb', database=using, interactive=False)
    return HttpResponseRedirect('/mensajesdocumentos/')


def generate_message():
    messages = PendingTask.objects.filter(resultado=None, aplicacion='SMS', tipo='GRACIAS')
    empresa_nombre = Registry.objects.get(nombre='SIC_SMS_NombreEmpresa').get_value()
    for message in messages:
        parametros_dict = json.loads(message.parametros)
        folio = parametros_dict['folio']
        importe = parametros_dict['importe']
        responsable = parametros_dict['responsable']
        message.resultado = empresa_nombre + ' le agradece su compra ' + get_short_folio(folio) + ' por ' + importe
        responsable = responsable.replace(' ', '')
        if responsable != '':
            message.resultado += ', Compro: ' + responsable
        message.resultado = message.resultado.rstrip()
        message.save()

    return


@login_required(login_url='/login/')
def send_messages(request):
    generate_message()
    messages = PendingTask.objects.exclude(resultado=None).filter(aplicacion='SMS')
    apikey = Registry.objects.get(nombre='SIC_SMS_ApiKey').get_value()
    sms_masivo = SMSMasivo(apikey=apikey, pruebas=modo_pruebas)
    if messages:
        for message in messages:
            phone = json.loads(message.parametros)['telefono']
            phone = unicode(phone.encode('utf-8'), errors='ignore')
            phone = re.sub('[^0-9]', '', str(phone))
            if message.intentos > 10:
                message.delete()
                print 'Mensaje eliminado por mas de 10 intentos fallidos'
            else:
                message.intentos += 1
                message.save()
                if len(phone) == 10:
                    resultado = sms_masivo.send(mensaje=message.resultado.rstrip(), telefono=phone)
                    if resultado['estatus'] == 'ok':
                        message.delete()
                else:
                    print 'Numero Invalido de ' + json.loads(message.parametros)['cliente_nombre']

    return HttpResponseRedirect('/mensajesdocumentos/')