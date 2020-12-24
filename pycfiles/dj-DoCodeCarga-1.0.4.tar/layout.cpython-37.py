# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Docode\Desktop\Gimbow\DoCodeCarga\procesos\layout.py
# Compiled at: 2020-01-07 20:50:49
# Size of source mod 2**32: 746 bytes
from . import procesos

def verificar(request):
    response = False
    if request.method == 'GET':
        if request.GET.get('layout') == 'Descargar Layout':
            response = True
    return response


def descargar(modelo):
    try:
        return procesos.obtenerLayout(modelo)
    except Exception as e:
        try:
            return
        finally:
            e = None
            del e


def cargar(request, modelo):
    try:
        file = request.FILES['excel']
        return procesos.leerExcel(file, modelo)
    except Exception as e:
        try:
            respuesta = {'resp':0, 
             'mensaje':'Error: cargar()'}
            return respuesta
        finally:
            e = None
            del e