# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/comportamientos/girar.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine import comportamientos

class Girar(comportamientos.Comportamiento):

    def iniciar(self, receptor, delta=360, velocidad=5):
        super(Girar, self).iniciar(receptor)
        if delta < 0:
            self.velocidad = -velocidad
        elif delta >= 0:
            self.velocidad = velocidad
        self.grados_a_rotar = abs(delta)

    def actualizar(self):
        if self.grados_a_rotar <= 0:
            return True
        self.receptor.rotacion += self.velocidad
        self.grados_a_rotar -= abs(self.velocidad)