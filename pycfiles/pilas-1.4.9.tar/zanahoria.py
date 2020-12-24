# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/zanahoria.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor

class Zanahoria(Actor):
    """Representa un actor que parece una Zanahoria."""

    def iniciar(self, x, y):
        self.x = x
        self.y = y
        self.cuadro_normal = self.pilas.imagenes.cargar('zanahoria_normal.png')
        self.cuadro_reir = self.pilas.imagenes.cargar('zanahoria_sonrie.png')
        self.normal()
        self.radio_de_colision = 25

    def normal(self):
        """Cambia la imagen actual por una donde se ve la zanahora normal."""
        self.imagen = self.cuadro_normal
        self.centro = ('centro', 65)

    def sonreir(self):
        """Cambia la imagen actual por una en donde tiene una sonrisa"""
        self.imagen = self.cuadro_reir
        self.centro = ('centro', 65)

    def saltar(self):
        """Realiza un salto hacia arriba."""
        self.sonreir()
        self.hacer(self.pilas.comportamientos.Saltar, cuando_termina=self.normal)

    def decir(self, mensaje):
        u"""Emite un mensaje usando un globo similar al de los commics.

        :param mensaje: La cadena de mensaje que mostrará."""
        self.sonreir()
        Actor.decir(self, mensaje)
        self.pilas.tareas.una_vez(2, self.normal)