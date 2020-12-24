# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/habilidades/siempre_en_el_centro.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.habilidades.habilidad import Habilidad

class SiempreEnElCentro(Habilidad):
    """Hace que un actor siempre esté en el centro de la camara y la desplace
    cuando el actor se desplaza."""

    def actualizar(self):
        self.pilas.escena_actual().camara.x = self.receptor.x
        self.pilas.escena_actual().camara.y = self.receptor.y