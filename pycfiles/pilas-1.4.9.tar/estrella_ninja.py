# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/estrella_ninja.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor

class EstrellaNinja(Actor):
    """ Representa una estrella ninja. """

    def pre_iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.imagen = self.pilas.imagenes.cargar('disparos/estrella.png')
        self.rotacion = 0
        self.escala = 0.5
        self.radio_de_colision = 20
        self.hacer(self.pilas.comportamientos.Proyectil, velocidad_maxima=1, aceleracion=1, angulo_de_movimiento=0, gravedad=0)

    def actualizar(self):
        self.rotacion += 10