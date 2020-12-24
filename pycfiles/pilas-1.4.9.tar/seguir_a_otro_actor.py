# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pilasengine/habilidades/seguir_a_otro_actor.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine import habilidades
import random

class SeguirAOtroActor(habilidades.Habilidad):
    """Hace que un actor siga a otro actor."""

    def iniciar(self, receptor, actor_a_seguir, velocidad=5, inteligencia=1):
        super(SeguirAOtroActor, self).iniciar(receptor)
        self.objetivo = actor_a_seguir
        self.velocidad = velocidad
        self.inteligencia = 1
        self.perdido = None
        return

    def actualizar(self):

        def limitar(valor):
            return min(max(valor, -self.velocidad), self.velocidad)

        objetivo_x = self.objetivo.x
        objetivo_y = self.objetivo.y
        if self.inteligencia == 0:
            if self.perdido:
                objetivo_x, objetivo_y = self.perdido
                if random.randint(0, 10) > 7:
                    self.perdido = None
            elif random.randint(0, 10) > 7:
                self.perdido = (self.objetivo.x, self.objetivo.y)
        self.receptor.x += limitar(objetivo_x - self.receptor.x)
        self.receptor.y += limitar(objetivo_y - self.receptor.y)
        return