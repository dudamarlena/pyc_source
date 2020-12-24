# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/plugins.py
# Compiled at: 2016-08-25 20:52:02
import os, sys, inspect, utils

class Complementos:

    def __init__(self, pilas):
        self.pilas = pilas
        lista_de_plugins = self.__cargar_plugins()
        if lista_de_plugins:
            cantidad = len(lista_de_plugins)
            if cantidad == 1:
                print 'Se encontro un plugin.'
            else:
                print 'Se econtraron %d plugins.' % cantidad
        else:
            print 'No se encontraron plugins.'
        self.__aplicar_plugins(lista_de_plugins)

    def __obtener_ruta_de_plugins(self):
        """Returna el path a los plugins de Pila."""
        CONFIG_DIR = self.pilas.utils.obtener_directorio_de_configuracion()
        pilas_home = os.path.join(CONFIG_DIR, '.pilas-engine')
        ruta_de_plugins = os.path.join(pilas_home, 'plugins')
        if not os.path.exists(ruta_de_plugins):
            os.makedirs(ruta_de_plugins)
            self.__crear_ayuda(ruta_de_plugins)
        return ruta_de_plugins

    def __crear_ayuda(self, ruta):
        ruta_al_archivo = os.path.join(ruta, 'COMO_CREAR_PLUGINS.txt')
        archivo = open(ruta_al_archivo, 'wt')
        archivo.write('Para crear plugins tienes construir archivos\nterminados en .py con el contenido que quieres ejecutar.\n\nCada plugin tiene que contener una o mas clases. Una vez que pilas\nse inicialice con el argumentos "cargar_plugins=True", todos los\nnombres de clases estaran disponibles para utilizar.\n\nMira el manual para mas detalles: \n\n - http://hugoruscitti.github.io/pilas-manual/complementos/index.html\n')
        archivo.close()

    def __lista_de_plugins_encontrados(self):
        """Retorna una lista de plugins encontrados de Pilas."""
        directorio_de_plugins = self.__obtener_ruta_de_plugins()
        lista_de_plugins = list()
        for archivo in os.listdir(directorio_de_plugins):
            if not archivo.endswith('.py'):
                continue
            nombre_del_plugin, _ = archivo.split('.py')
            lista_de_plugins.append(nombre_del_plugin)

        return lista_de_plugins

    def __cargar_plugins(self):
        """Importa la lista de plugins dado. Retorna una lista
        de modulos de plugins importados."""
        ruta_de_plugins = self.__obtener_ruta_de_plugins()
        if ruta_de_plugins not in sys.path:
            sys.path.append(ruta_de_plugins)
        plugins_encontrados = self.__lista_de_plugins_encontrados()
        lista_de_plugins_importados = list()
        for plugin in plugins_encontrados:
            plugin_importado = __import__(plugin)
            lista_de_plugins_importados.append(plugin_importado)

        return lista_de_plugins_importados

    def __aplicar_plugins(self, lista_de_plugins):
        """Aplica los modulos de plugins dados a las habilidades."""
        for modulo_de_plugin in lista_de_plugins:
            for nombre_de_clase, clase in inspect.getmembers(modulo_de_plugin):
                setattr(self, nombre_de_clase, clase)