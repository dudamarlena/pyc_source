# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_orden_trabajo\djmicrosip_orden_trabajo\config.py
# Compiled at: 2019-11-26 10:52:52
settings = {'name': 'Orden trabajo', 'icon_class': 'glyphicon glyphicon-list-alt', 
   'url': '/pedidos/', 
   'url_main_path': 'pedidos/', 
   'users': []}
PERMISSIONS = {'Herramientas': {'permissions': [
                                  {'name': 'Preferencias', 
                                     'codename': 'preferencias'},
                                  {'name': 'Preparar Aplicacion', 
                                     'codename': 'prepararaplicacion'}]}, 
   'permissions': [
                 {'name': 'Agregar Orden de trabajo', 
                    'codename': 'addordentrabajo'},
                 {'name': 'Editar Orden de trabajo', 
                    'codename': 'editordentrabajo'},
                 {'name': 'Cambiar progreso', 
                    'codename': 'progresoorden'},
                 {'name': 'Asignar vendedor', 
                    'codename': 'asignarvendedor'},
                 {'name': 'Reportes', 
                    'codename': 'verreportes'}]}