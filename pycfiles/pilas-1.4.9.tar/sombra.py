# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/sombra.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor

class Sombra(Actor):

    def iniciar(self, x, y):
        self.x = x
        self.y = y
        self.imagen = 'sombra.png'
        self.radio_de_colision = 15

    def actualizar(self):
        pass

    def terminar(self):
        pass