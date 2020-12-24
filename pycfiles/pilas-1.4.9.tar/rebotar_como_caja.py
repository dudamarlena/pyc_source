# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/habilidades/rebotar_como_caja.py
# Compiled at: 2016-08-25 20:52:02
import random
from pilasengine import habilidades

class RebotarComoCaja(habilidades.Habilidad):
    """Le indica al actor que rebote y colisiones como una caja cuadrada.

    >>> un_actor = pilas.actores.Aceituna()
    >>> un_actor.aprender(pilas.habilidades.RebotarComoPelota)
    """

    def iniciar(self, receptor):
        super(RebotarComoCaja, self).iniciar(receptor)
        error = random.randint(-10, 10) / 10.0
        rectangulo = self.pilas.fisica.Rectangulo(receptor.x + error, receptor.y + error, receptor.radio_de_colision * 2 - 4, receptor.radio_de_colision * 2 - 4)
        receptor.aprender(self.pilas.habilidades.Imitar, rectangulo)

    def eliminar(self):
        super(RebotarComoCaja, self).eliminar()
        self.receptor.habilidades.Imitar.eliminar()