# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/fantasma.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor

class Fantasma(Actor):
    """Representa al fantasman del clasico pac-man."""

    def pre_iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.grilla = self.pilas.imagenes.cargar_grilla('fantasma.png', 8, 1)
        self.imagen = self.grilla
        self.cuadro = 0
        self.control = self.pilas.escena_actual().control
        self.velocidad = 3
        self.posicion = 0

    def actualizar(self):
        if self.control.izquierda:
            self.posicion = 2
            self.x -= self.velocidad
            self._reproducir_animacion()
        elif self.control.derecha:
            self.posicion = 3
            self.x += self.velocidad
            self._reproducir_animacion()
        elif self.control.abajo:
            self.posicion = 1
            self.y -= self.velocidad
            self._reproducir_animacion()
        elif self.control.arriba:
            self.posicion = 0
            self.y += self.velocidad
            self._reproducir_animacion()

    def _reproducir_animacion(self):
        self.cuadro += 0.2
        if self.cuadro > 1:
            self.cuadro = 0
        self.definir_cuadro(int(self.posicion * 2 + self.cuadro))

    def definir_cuadro(self, indice):
        u"""Cambia el cuadro de animación a mostrar.

        :param indice: Número de cuadro a mostrar.
        """
        self.imagen.definir_cuadro(indice)