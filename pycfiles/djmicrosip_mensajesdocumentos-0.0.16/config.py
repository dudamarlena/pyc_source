# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_mensajesdocumentos\djmicrosip_mensajesdocumentos\config.py
# Compiled at: 2015-09-03 19:08:08
settings = {'name': 'Envio mensajes Documentos', 'icon_class': 'glyphicon glyphicon-list-alt', 
   'url': '/mensajesdocumentos/', 
   'url_main_path': 'mensajesdocumentos/', 
   'users': [
           'SYSDBA']}
configuration_registers = ('SIC_SMS_NombreEmpresa', 'SIC_SMS_TelDefault', 'SIC_SMS_ApiKey',
                           'SIC_MensajeDocumentos_VentasTipoDocumento', 'SIC_MensajeDocumentos_PuntoVentaTipoDocumento')
campos_particulares_tablas = [
 {'tabla': 'LIBRES_CLIENTES', 
    'campos': [
             'RESPONSABLE_DE_VENTA']},
 {'tabla': 'LIBRES_REM_VE', 
    'campos': [
             'RESPONSABLE']},
 {'tabla': 'LIBRES_FAC_VE', 
    'campos': [
             'RESPONSABLE']}]