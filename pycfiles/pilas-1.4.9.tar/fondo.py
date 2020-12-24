# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/fondos/fondo.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores import actor

class Fondo(actor.Actor):
    """Representa un fondo de pantalla.

    Los fondos en pilas son actores normales, solo
    que generalmente están por detrás de toda la
    escena y ocupan toda el area de la ventana.
    """

    def __init__(self, pilas=None, imagen=None):
        super(Fondo, self).__init__(pilas)
        if imagen:
            self.imagen = imagen
        self.z = 1000
        self.radio_de_colision = None
        return

    def pre_iniciar(self, *k, **kw):
        pass

    def obtener_z(self):
        return self._z

    def definir_z(self, z):
        self._z = z
        self.pilas.escena_actual()._actores.sort()

    z = property(obtener_z, definir_z, doc='Define lejania respecto del observador.')