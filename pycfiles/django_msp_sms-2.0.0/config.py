# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_msp_sms\django_msp_sms\config.py
# Compiled at: 2016-12-13 18:15:27
settings = {'name': 'Mensajes de Texto', 'icon_class': 'glyphicon glyphicon-envelope', 
   'url': '/sms/', 
   'url_main_path': 'sms/', 
   'users': []}
configuration_registers = ('SIC_SMS_NombreEmpresa', 'SIC_SMS_TelDefault', 'SIC_SMS_ApiKey',
                           'SIC_SMS_MontoMinimo', 'SIC_SMS_EnviarRemisionesPendientes',
                           'SIC_SMS_ResumirMensajes', 'SIC_SMS_InformacionExtra',
                           'SIC_SMS_DiasPorVencer')
extrafields = (('CLIENTES', 'SIC_SMS_NOENVIAR'), )