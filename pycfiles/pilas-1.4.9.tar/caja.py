# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/caja.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor

class Caja(Actor):
    """Representa una caja que posee fisica.

    .. image:: ../../pilas/data/manual/imagenes/actores/caja.png

    """

    def iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.imagen = self.pilas.imagenes.cargar('caja.png')
        self.radio_de_colision = 25
        self.aprender(self.pilas.habilidades.RebotarComoCaja)