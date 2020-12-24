# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/comportamientos/avanzar.py
# Compiled at: 2016-08-25 20:52:02
import math
from pilasengine import comportamientos

class Avanzar(comportamientos.Comportamiento):
    """Desplaza al actor en la dirección y sentido indicado por una rotación."""

    def iniciar(self, receptor, pasos=0, velocidad=5):
        u"""Se invoca cuando se anexa el comportamiento a un actor.

        :param receptor: El actor que comenzará a ejecutar este comportamiento.
        """
        super(Avanzar, self).iniciar(receptor)
        self.pasos = abs(pasos)
        self.velocidad = velocidad
        rotacion_en_radianes = math.radians(receptor.rotacion)
        self.dx = math.cos(rotacion_en_radianes)
        self.dy = math.sin(rotacion_en_radianes)
        self.pasos_aux = self.pasos

    def actualizar(self):
        if self.pasos_aux > 0:
            if self.pasos_aux - self.velocidad < 0:
                avance = self.pasos_aux
            else:
                avance = self.velocidad
            self.pasos_aux -= avance
            self.receptor.x += self.dx * avance
            self.receptor.y += self.dy * avance
        else:
            return True