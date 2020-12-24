# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/habilidades/seguir_clicks.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine import habilidades

class SeguirClicks(habilidades.Habilidad):

    def iniciar(self, receptor):
        super(SeguirClicks, self).iniciar(receptor)
        self.pilas.eventos.click_de_mouse.conectar(self.moverse_a_este_punto)

    def moverse_a_este_punto(self, evento):
        self.receptor.x = (
         [
          evento.x], 0.5)
        self.receptor.y = ([evento.y], 0.5)