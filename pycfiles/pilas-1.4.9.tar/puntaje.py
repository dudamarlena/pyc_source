# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/puntaje.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine import colores
from pilasengine.actores.texto import Texto

class Puntaje(Texto):
    """Representa un contador de Puntaje"""

    def __init__(self, pilas, texto='0', x=0, y=0, color=colores.negro):
        u"""Inicializa el Puntaje.

        :param texto: El número inicial del puntaje.
        :param x: Posición horizontal para el puntaje.
        :param y: Posición vertical para el puntaje.
        :param color: Color que tendrá el texto de puntaje.
        """
        Texto.__init__(self, pilas, str(texto), x=x, y=y)
        self.color = color
        self.valor = int(texto)

    def definir(self, puntaje_variable='0'):
        u"""Cambia el texto que se mostrará cómo puntaje.

        :param puntaje_variable: Texto a definir.
        """
        self.valor = int(puntaje_variable)
        self.texto = str(self.valor)

    def aumentar(self, cantidad=1):
        u"""Incrementa el puntaje.

        :param cantidad: La cantidad de puntaje que se aumentará.
        """
        self.definir(self.valor + int(cantidad))

    def reducir(self, cantidad=1):
        u"""Reduce el puntaje.

        :param cantidad: La cantidad de puntaje que se reducirá.
        """
        self.definir(self.valor - int(cantidad))

    def obtener(self):
        u"""Retorna el puntaje en forma de número."""
        return self.valor