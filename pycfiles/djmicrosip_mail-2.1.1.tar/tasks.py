# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_mail\djmicrosip_mail\tasks.py
# Compiled at: 2019-12-23 13:54:24
from .modulos.saldos_clientes.core import formar_correo

def enviar_correo(**kwargs):
    formar_correo(kwargs=kwargs)