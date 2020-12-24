# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/habilidades/habilidad.py
# Compiled at: 2016-08-25 20:52:02


class Habilidad(object):
    """Representa una habilidad que los actores pueden aprender """

    def __init__(self, pilas):
        self.pilas = pilas

    def iniciar(self, receptor):
        self.receptor = receptor

    def actualizar(self):
        pass

    def eliminar(self):
        self.receptor.eliminar_habilidad(self.__class__)

    def __repr__(self):
        return ('<Habilidad: {0}>').format(self.__class__.__name__)