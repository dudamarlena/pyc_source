# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/comportamientos/orbitar.py
# Compiled at: 2016-08-25 20:52:02
import math
from pilasengine import comportamientos

class Orbitar(comportamientos.Comportamiento):

    def iniciar(self, receptor, x=0, y=0, radio=50, velocidad=5, direccion='derecha'):
        super(Orbitar, self).iniciar(receptor)
        self.punto_de_orbita_x = x
        self.punto_de_orbita_y = y
        self.radio = radio
        self.direccion = direccion
        if self.direccion == 'derecha':
            self.velocidad = velocidad
        elif self.direccion == 'izquierda':
            self.velocidad = -velocidad
        self.angulo = 0

    def actualizar(self):
        self.angulo += self.velocidad
        self.angulo %= 360
        self.mover_astro()

    def mover_astro(self):
        self.receptor.x = self.punto_de_orbita_x + math.cos(math.radians(self.angulo)) * self.radio
        self.receptor.y = self.punto_de_orbita_y - math.sin(math.radians(self.angulo)) * self.radio


class OrbitarSobreActor(Orbitar):

    def iniciar(self, receptor, actor, radio=50, velocidad=5, direccion='derecha'):
        super(OrbitarSobreActor, self).iniciar(receptor, actor.x, actor.y, radio, velocidad, direccion)
        self.actor = actor

    def mover_astro(self):
        self.punto_de_orbita_x = self.actor.x
        self.punto_de_orbita_y = self.actor.y
        super(OrbitarSobreActor, self).mover_astro()