# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/piedra.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor

class Piedra(Actor):
    """Representa una piedra que podría ser usada como meteoríto."""

    def iniciar(self, x, y):
        self.x = x
        self.y = y
        self.definir_tamano('grande')
        self.velocidad_rotacion = 1
        self.dx = 0
        self.dy = 0

    def definir_tamano(self, tamano):
        if tamano not in ('grande', 'media', 'chica'):
            raise Exception("El tamano indicado es incorrecto, solo se permite                             grande', 'media' o 'chica'.")
        self.imagen = self.pilas.imagenes.cargar('piedra_' + tamano + '.png')
        radios = {'grande': 25, 'media': 20, 'chica': 10}
        self.radio_de_colision = radios[tamano]
        self.aprender(self.pilas.habilidades.SeMantieneEnPantalla)

    def actualizar(self):
        u"""Realiza una actualización de la posición."""
        self.rotacion += self.velocidad_rotacion
        self.x += self.dx
        self.y += self.dy

    def empujar(self, dx, dy):
        self.dx = dx
        self.dy = dy