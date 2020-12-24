# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/habilidades/puede_explotar.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores import Actor
from pilasengine.habilidades.habilidad import Habilidad

class PuedeExplotar(Habilidad):
    """Hace que un actor se pueda hacer explotar invocando al metodo eliminar."""

    def iniciar(self, receptor):
        super(PuedeExplotar, self).iniciar(receptor)
        receptor.eliminar = self.eliminar_y_explotar

    def eliminar_y_explotar(self):
        explosion = self.crear_explosion()
        explosion.x = self.receptor.x
        explosion.y = self.receptor.y
        Actor.eliminar(self.receptor)

    def crear_explosion(self):
        a = self.pilas.actores.Explosion()
        a.escala = self.receptor.escala * 2
        return a