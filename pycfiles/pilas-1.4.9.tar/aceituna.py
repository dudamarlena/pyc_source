# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/aceituna.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor

class Aceituna(Actor):

    def pre_iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.imagen = 'aceituna.png'
        self.radio_de_colision = 15

    def actualizar(self):
        pass

    def terminar(self):
        pass