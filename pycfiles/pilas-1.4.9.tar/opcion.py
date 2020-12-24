# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/opcion.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.texto import Texto
from pilasengine import colores

class Opcion(Texto):
    """Un item discreto, dispara una funcion al seleccionares."""

    def __init__(self, pilas, texto='', x=0, y=0, funcion_a_invocar=None, argumentos=None, fuente=None, color_normal=colores.gris, color_resaltado=colores.blanco):
        u"""Inicializa el actor.

        :param texto: Etiqueta a mostrar
        :param x: Posicion en el eje x
        :param y: Posicion en el eje y
        :param funcion_a_invocar: Manejador, se dispara al seleccionar la opcion
        :param argumentos: Argumentos posicionales para :funcion_a_invocar:
        :param fuente: Tipografía a utilizar.
        """
        Texto.__init__(self, pilas, texto, x=x, y=y, fuente=fuente)
        self.magnitud = 20
        self.funcion_a_invocar = funcion_a_invocar
        self.argumentos = argumentos
        self.color_normal = color_normal
        self.color_resaltado = color_resaltado
        self.color = self.color_normal
        self.z = -300
        self.centro = ('centro', 'centro')

    def resaltar(self, estado=True):
        u"""Pinta la opcion actual de un color mas claro.

        :param estado: True o False indicando si se tiene que resaltar o deseleccionar la opción.
        """
        if estado:
            self.color = self.color_resaltado
        else:
            self.color = self.color_normal

    def seleccionar(self):
        """Invoca a la funcion que tiene asociada para ejecutar."""
        if self.funcion_a_invocar:
            self.funcion_a_invocar(*self.argumentos)
        else:
            print 'Cuidado, la opcion', self, 'no tiene funcion asociada.'