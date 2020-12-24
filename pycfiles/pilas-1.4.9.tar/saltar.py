# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/comportamientos/saltar.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine import comportamientos

class Saltar(comportamientos.Comportamiento):
    """Realiza un salto, cambiando los atributos 'y'."""

    def iniciar(self, receptor, velocidad_inicial=10, cuando_termina=None):
        u"""Se invoca cuando se anexa el comportamiento a un actor.

        :param receptor: El actor que comenzará a ejecutar este comportamiento.
        """
        super(Saltar, self).iniciar(receptor)
        self.velocidad_inicial = velocidad_inicial
        self.cuando_termina = cuando_termina
        self.sonido_saltar = self.pilas.sonidos.cargar('audio/saltar.wav')
        self.suelo = int(self.receptor.y)
        self.velocidad = self.velocidad_inicial
        self.sonido_saltar.reproducir()
        self.velocidad_aux = self.velocidad_inicial

    def actualizar(self):
        self.receptor.y += self.velocidad
        self.velocidad -= 0.3
        if self.receptor.y <= self.suelo:
            self.velocidad_aux /= 2.0
            self.velocidad = self.velocidad_aux
            if self.velocidad_aux <= 1:
                self.receptor.y = self.suelo
                if self.cuando_termina:
                    self.cuando_termina()
                return True