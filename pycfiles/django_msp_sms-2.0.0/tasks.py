# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_msp_sms\django_msp_sms\tasks.py
# Compiled at: 2015-10-19 12:15:02
from .modulos.saldos_clientes.core import formar_mensaje

def enviar_correo(**kwargs):
    formar_mensaje(kwargs=kwargs)