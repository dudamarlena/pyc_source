# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_mail\djmicrosip_mail\modulos\saldos_clientes\core.py
# Compiled at: 2019-12-23 13:53:20
from ...core import MicrosipMailServer
from .models import *
from datetime import date, timedelta, datetime
from decimal import Decimal
from django.db import connections, router
from django.db.models import Sum
from microsip_api.comun.comun_functions import split_letranumero
from re import sub

def get_short_folio(folio):
    letra_numero = split_letranumero(folio)
    return '%s%s' % (letra_numero[0], letra_numero[1])


def formar_correo(kwargs):
    cargo = kwargs['kwargs']['cargo']
    cliente_nombre = Cliente.objects.get(id=cargo['cliente_id'])
    cliente_nombre = cliente_nombre.nombre
    commun = kwargs['kwargs']['commun']
    mail_login = kwargs['kwargs']['mail_login']
    detalles_str = ''
    if cargo['documentos_numero'] <= 50:
        for documento in cargo['documentos']:
            if documento['factura_vencida']:
                vencimiento = '<span style="color:red"> venció el día ' + documento['vencimiento'] + '</span>'
            else:
                vencimiento = 'vence el día ' + documento['vencimiento']
            detalles_str += ' <br/>\n            <span style="font-weight:700">%s, Folio: %s</span> \t %s %s\n            ' % (documento['concepto'], documento['folio'], documento['saldo_cargo'], vencimiento)

    if cargo['documentos_numero'] > 1:
        detalles_str += '<br/><span style="font-weight:700">%s Documentos en total.</span>' % cargo['documentos_numero']
    mensaje_attrs = {'empresa_nombre': commun['empresa_nombre'], 
       'detalles_str': detalles_str, 
       'total': cargo['total'], 
       'cliente_moneda': cargo['cliente_moneda'], 
       'mensaje_extra': commun['mensaje_extra'], 
       'cliente_nombre': cliente_nombre}
    mensajes_str = ('\n        <h2><span style="font-weight: 700;">{empresa_nombre} le informa</span></h2>\n        <h3><strong>{cliente_nombre}</strong></h3>\n        Su estado de cuenta al día de hoy es:\n        {detalles_str}\n        <br/><br/>\n        <span style="font-weight:700">Total {total}</span>\n        <br/>\n        <span style="text-decoration: underline;">Importes expresados en {cliente_moneda}.</span>\n        <br/>\n        {mensaje_extra}\n    ').format(**mensaje_attrs)
    mail_server = MicrosipMailServer(from_addr=mail_login['from_addr'], smtp_host=mail_login['smtp_host'], smtp_port=mail_login['smtp_port'], smtp_username=mail_login['smtp_username'], smtp_password=mail_login['smtp_password'])
    destinatarios = cargo['email'].split(';')
    mail_server.sendmail(destinatarios, 'Estado de cuenta en ' + commun['empresa_nombre'], mensajes_str, None, None)
    return


def formar_correo_por_vencer(kwargs):
    dias_por_vencer = int(Registry.objects.get(nombre='SIC_MAIL_DiasPorVencer').get_value())
    cargos = kwargs['data']['cargos']
    for cargo in cargos:
        cliente_nombre = Cliente.objects.get(id=cargo['cliente_id'])
        cliente_nombre = cliente_nombre.nombre
        commun = kwargs['commun']
        mail_login = kwargs['mail_login']
        detalles_por_vencer_str = ''
        detalles_str = ''
        total_saldos_por_vencer = 0
        total_saldos_vencidos = 0
        if cargo['documentos_numero'] <= 50:
            for documento in cargo['documentos']:
                vencimiento_date = datetime.strptime(documento['vencimiento'], '%d/%m/%Y').date()
                dias_dif = (vencimiento_date - datetime.now().date()).days
                if documento['factura_vencida']:
                    vencimiento = '<span style="color:red"> venció el día ' + documento['vencimiento'] + '</span>'
                    detalles_str += ' <br/>\n                    <span style="font-weight:700">%s, Folio: %s</span> \t %s %s\n                    ' % (documento['concepto'], documento['folio'], documento['saldo_cargo'], vencimiento)
                    total_saldos_vencidos += Decimal(float(documento['saldo_cargo'][1:]))
                elif dias_dif == dias_por_vencer:
                    vencimiento = 'Hoy faltan %s dias para su vencimiento. %s' % (dias_por_vencer, documento['vencimiento'])
                    detalles_por_vencer_str += ' <br/>\n                    <span style="font-weight:700">%s, Folio: %s</span> \t %s %s\n                    ' % (documento['concepto'], documento['folio'], documento['saldo_cargo'], vencimiento)
                    total_saldos_por_vencer += Decimal(sub('[^\\d.]', '', documento['saldo_cargo'][1:]))

        detalles = {'detalles_str': detalles_str, 
           'detalles_por_vencer_str': detalles_por_vencer_str, 
           'total_saldos_vencidos': total_saldos_vencidos, 
           'total_saldos_por_vencer': total_saldos_por_vencer}
        detalles_str = ('\n            <h3><strong>Cargos por vencer:</strong></h3>\n            {detalles_por_vencer_str}\n            <br/><br/>\n            <span style="font-weight:700">Total: {total_saldos_por_vencer}</span>\n            <br/><br/>\n            <h3><strong>Cargos vencidos:</strong></h3>\n            {detalles_str}\n            <br/><br/>\n            <span style="font-weight:700">Total: {total_saldos_vencidos}</span>\n            <br/><br/>\n        ').format(**detalles)
        mensaje_attrs = {'empresa_nombre': commun['empresa_nombre'], 
           'detalles_str': detalles_str, 
           'total': cargo['total'], 
           'cliente_moneda': cargo['cliente_moneda'], 
           'mensaje_extra': commun['mensaje_extra'], 
           'cliente_nombre': cliente_nombre}
        mensajes_str = ('\n            <h2><span style="font-weight: 700;">{empresa_nombre} le informa</span></h2>\n            <h3><strong>{cliente_nombre}</strong></h3>\n            <br/>\n            {detalles_str}\n            <br/>\n            <span style="text-decoration: underline;">Importes expresados en {cliente_moneda}.</span>\n            <br/>\n            {mensaje_extra}\n        ').format(**mensaje_attrs)
        mail_server = MicrosipMailServer(from_addr=mail_login['from_addr'], smtp_host=mail_login['smtp_host'], smtp_port=mail_login['smtp_port'], smtp_username=mail_login['smtp_username'], smtp_password=mail_login['smtp_password'])
        destinatarios = cargo['email'].split(';')
        if not detalles_por_vencer_str == '':
            mail_server.sendmail(destinatarios, 'Estado de cuenta en ' + commun['empresa_nombre'], mensajes_str, None, None)

    return