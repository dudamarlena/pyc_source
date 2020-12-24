# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_msp_sms\django_msp_sms\views.py
# Compiled at: 2015-10-19 12:15:02
import json, re
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from . import core
from . import forms
from .models import *
from microsip_api.apps.sms.core import SMSMasivo
modo_pruebas = settings.MODO_SERVIDOR == 'PRUEBAS'

@login_required(login_url='/login/')
def index(request, template_name='django_msp_sms/index.html'):
    error = ''
    apikey = None
    creditos = 0
    initial_configuration = core.InitialConfiguration()
    if not initial_configuration.is_valid:
        error = 'Inicializar Configuracion'
    else:
        apikey = str(Registry.objects.get(nombre='SIC_SMS_ApiKey').get_value())
    if apikey != 'None':
        sms_masivo = SMSMasivo(apikey=apikey, pruebas=modo_pruebas)
        dic_cred = sms_masivo.credito()
        if dic_cred['estatus'] == 'ok':
            creditos = int(dic_cred['credito'])
    else:
        error = 'Llave no Definida'
    c = {'creditos': creditos, 'error': error, 'modo_servidor': settings.MODO_SERVIDOR}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def personalizadosView(request, template_name='django_msp_sms/personalizados.html'):
    apikey = str(Registry.objects.get(nombre='SIC_SMS_ApiKey').get_value())
    c = {}
    multi = False
    form = forms.SMSForm(request.POST or None)
    mensaje_respuesta = ''
    estatus = ''
    if form.is_valid():
        mensaje = form.cleaned_data['mensaje']
        mensaje = mensaje.encode('ascii', 'replace')
        telefono = form.cleaned_data['telefono']
        sms_masivo = SMSMasivo(apikey=apikey, pruebas=modo_pruebas)
        if len(telefono.split(',')) > 1:
            multi = True
            j = sms_masivo.multisend(mensaje=mensaje, telefono=telefono)
            mensaje_respuesta = j['respuestas']
            estatus = None
        else:
            j = sms_masivo.send(mensaje=mensaje, telefono=telefono)
            mensaje_respuesta = j['mensaje']
            estatus = j['estatus']
    c = {'mensaje': mensaje_respuesta, 'form': form, 'estatus': estatus, 'multi': multi}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def enviar_smsView(request):
    apikey = str(Registry.objects.get(nombre='SIC_SMS_ApiKey').get_value())
    mensaje = request.GET['mensaje']
    mensaje = mensaje.encode('ascii', 'replace')
    telefono = request.GET['telefono']
    numero_mensaje = int(request.GET['numero_mensaje'])
    numero_mensaje += 1
    sms = SMSMasivo(apikey=apikey, pruebas=modo_pruebas)
    resultado = sms.send(mensaje=mensaje, telefono=telefono)['mensaje']
    data = {'telefono': telefono, 
       'numero_mensaje': numero_mensaje, 
       'resultado': resultado}
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')


@login_required(login_url='/login/')
def enviar_mensaje(request):
    apikey = str(Registry.objects.get(nombre='SIC_SMS_ApiKey').get_value())
    telefono = request.GET['telefono']
    mensaje = request.GET['mensaje']
    mensaje = mensaje.encode('ascii', 'replace')
    sms = SMSMasivo(apikey=apikey, pruebas=modo_pruebas)
    resultado = sms.send(mensaje=mensaje, telefono=telefono)['mensaje']
    data = json.dumps({'resultado': resultado})
    return HttpResponse(data, mimetype='application/json')


@login_required(login_url='/login/')
def get_creditos(request):
    apikey = str(Registry.objects.get(nombre='SIC_SMS_ApiKey').get_value())
    sms_masivo = SMSMasivo(apikey=apikey, pruebas=modo_pruebas)
    creditos = int(sms_masivo.credito()['credito'])
    if modo_pruebas:
        creditos = len(mensajes)
    data = json.dumps({'creditos': creditos})
    return HttpResponse(data, mimetype='application/json')


@login_required(login_url='/login/')
def get_mensajes_personalizados(request):
    clientes_ids = str(request.GET['clientes_ids']).replace('[', '').replace(']', '').replace('"', '').split(',')
    mensaje = request.GET['mensaje']
    mensaje = mensaje.encode('ascii', 'replace')
    clientes = ClienteDireccion.objects.filter(cliente__id__in=clientes_ids).order_by('telefono1').values_list('cliente', 'cliente__nombre', 'telefono1')
    mensajes_clientes = {}
    clientes_con_telefono_invalido = []
    for cliente in clientes:
        cliente_id = cliente[0]
        cliente_nombre = cliente[1].lstrip().rstrip()
        telefono = cliente[2]
        if telefono:
            telefono = unicode(telefono.encode('utf-8'), errors='ignore')
            telefono = re.sub('[^0-9]', '', str(telefono))
            if len(telefono) != 10 and cliente_nombre not in clientes_con_telefono_invalido:
                clientes_con_telefono_invalido.append(cliente_nombre)
            elif cliente_id not in mensajes_clientes:
                if cliente_nombre in clientes_con_telefono_invalido:
                    clientes_con_telefono_invalido.remove(cliente_nombre)
                mensajes_clientes[cliente_id] = (telefono, mensaje, cliente_nombre)
        elif cliente_nombre not in clientes_con_telefono_invalido:
            clientes_con_telefono_invalido.append(cliente_nombre)

    data = json.dumps({'mensajes': mensajes_clientes.values(), 
       'clientes_con_telefono_invalido': clientes_con_telefono_invalido})
    return HttpResponse(data, mimetype='application/json')