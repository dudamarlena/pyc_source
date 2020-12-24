# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/habilidades/puede_explotar_con_humo.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores import Actor
from pilasengine.habilidades.puede_explotar import PuedeExplotar

class PuedeExplotarConHumo(PuedeExplotar):
    """Hace que un actor se pueda hacer explotar invocando al metodo eliminar."""

    def crear_explosion(self):
        return self.pilas.actores.ExplosionDeHumo()