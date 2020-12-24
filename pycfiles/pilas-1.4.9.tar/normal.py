# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/escenas/normal.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.escenas.escena import Escena

class Normal(Escena):

    def iniciar(self):
        self.fondo = self.pilas.fondos.Plano()

    def actualizar(self):
        pass

    def terminar(self):
        pass