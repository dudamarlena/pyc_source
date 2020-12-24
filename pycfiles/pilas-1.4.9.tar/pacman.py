# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/pacman.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor

class Pacman(Actor):
    """Muestra un personaje similar al juego Pac-Man

    .. image:: ../../pilas/data/manual/imagenes/actores/pacman.png

    Este actor se puede mover con el teclado, pulsando las teclas ``izquierda``,
    ``arriba``, ``abajo`` y ``derecha``.

        >>> pacman = pilas.actores.Pacman(velocidad=5)

    """

    def pre_iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.grilla = self.pilas.imagenes.cargar_grilla('pacman.png', 4, 4)
        self.imagen = self.grilla
        self.cuadro = 0
        self.control = self.pilas.escena_actual().control
        self.velocidad = 3
        self.aprender(self.pilas.habilidades.SeMantieneEnPantalla)
        self.radio_de_colision = 5
        self.posicion = 0

    def actualizar(self):
        if self.control.izquierda:
            self.posicion = 0
            self.x -= self.velocidad
            self._reproducir_animacion()
        elif self.control.derecha:
            self.posicion = 1
            self.x += self.velocidad
            self._reproducir_animacion()
        elif self.control.abajo:
            self.posicion = 3
            self.y -= self.velocidad
            self._reproducir_animacion()
        elif self.control.arriba:
            self.posicion = 2
            self.y += self.velocidad
            self._reproducir_animacion()

    def _reproducir_animacion(self):
        self.cuadro += 0.4
        if self.cuadro > 3:
            self.cuadro = 0
        self.definir_cuadro(int(self.posicion * 4 + self.cuadro))

    def definir_cuadro(self, indice):
        u"""Cambia el cuadro de animación del actor."""
        self.imagen.definir_cuadro(indice)