# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_inventarios\djmicrosip_inventarios\config.py
# Compiled at: 2019-11-11 18:49:27
settings = {'name': 'Inventarios fisicos', 'icon_class': 'glyphicon glyphicon-stats', 
   'url': '/inventarios/', 
   'url_main_path': 'inventarios/', 
   'users': []}
configuration_registers = ('SIC_Inventarios_ManejarSeries', 'SIC_Inventarios_ConceptoCompra',
                           'SIC_Inventarios_TipoConcepto')
PERMISSIONS = {'Herramientas': {'permissions': [
                                  {'name': 'Preferencias', 
                                     'codename': 'herramientas.preferencias'},
                                  {'name': 'Preparar Aplicacion', 
                                     'codename': 'herramientas.prepararaplicacion'},
                                  {'name': 'Ver Historial de Inventarios', 
                                     'codename': 'herramientas.historialinventarios'}]}, 
   'Documentos': {'Inventarios': {'permissions': [
                                                {'name': 'Abrir Inventario', 
                                                   'codename': 'abririnventario'},
                                                {'name': 'Capturar Inventario', 
                                                   'codename': 'capturarinventario'}]}}, 
   'permissions': [
                 {'name': 'Almacenes', 
                    'codename': 'almacenes'}]}
VERSION = '1.0.9'