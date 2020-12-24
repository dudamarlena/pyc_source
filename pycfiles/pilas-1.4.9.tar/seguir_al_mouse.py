# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/habilidades/seguir_al_mouse.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine import habilidades

class SeguirAlMouse(habilidades.Habilidad):
    """Hace que un actor siga la posición del mouse en todo momento."""

    def iniciar(self, receptor):
        super(SeguirAlMouse, self).iniciar(receptor)
        self.pilas.eventos.mueve_mouse.conectar(self.mover)

    def mover(self, evento):
        self.receptor.x = evento.x
        self.receptor.y = evento.y