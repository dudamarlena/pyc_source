# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/habilidades/rebotar_como_pelota.py
# Compiled at: 2016-08-25 20:52:02
import random
from pilasengine import habilidades

class RebotarComoPelota(habilidades.Habilidad):
    """Le indica al actor que rebote y colisiones como una pelota.

    >>> un_actor = pilas.actores.Aceituna()
    >>> un_actor.aprender(pilas.habilidades.RebotarComoPelota)
    """

    def iniciar(self, receptor):
        super(RebotarComoPelota, self).iniciar(receptor)
        error = random.randint(-10, 10) / 10.0
        circulo = self.pilas.fisica.Circulo(receptor.x + error, receptor.y + error, receptor.radio_de_colision)
        receptor.aprender(self.pilas.habilidades.Imitar, circulo)
        self.circulo = circulo
        receptor.impulsar = self.impulsar
        receptor.empujar = self.empujar

    def eliminar(self):
        super(RebotarComoPelota, self).eliminar()
        self.receptor.habilidades.Imitar.eliminar()

    def impulsar(self, dx, dy):
        self.circulo.impulsar(dx, dy)

    def empujar(self, dx, dy):
        self.circulo.empujar(dx, dy)