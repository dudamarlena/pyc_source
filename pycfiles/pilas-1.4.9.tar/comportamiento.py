# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/comportamientos/comportamiento.py
# Compiled at: 2016-08-25 20:52:02


class Comportamiento(object):
    """Representa un comportamiento (estrategia) que se puede anexar a un actor."""

    def __init__(self, pilas=None):
        self.pilas = pilas

    def iniciar(self, receptor):
        u"""Se invoca cuando se anexa el comportamiento a un actor.

        :param receptor: El actor que comenzará a ejecutar este comportamiento.
        """
        if getattr(self, 'pilas', None) is None:
            self.pilas = receptor.pilas
        self.receptor = receptor
        return

    def actualizar(self):
        u"""Actualiza el comportamiento en un instante dado.

        Si este metodo retorna True entonces el actor dejará
        de ejecutar este comportamiento."""
        pass

    def terminar(self):
        pass