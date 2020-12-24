# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/habilidades/eliminarse_si_sale_de_pantalla.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine import habilidades

class EliminarseSiSaleDePantalla(habilidades.Habilidad):
    """Se asegura de que el actor sea eliminado si sale de los
    bordes de la pantalla.
    """

    def iniciar(self, receptor):
        u"""
        :param receptor: El actor que aprenderá la habilidad.
        """
        super(EliminarseSiSaleDePantalla, self).iniciar(receptor)
        self.ancho, self.alto = self.pilas.obtener_area()
        self.camara = self.pilas.escena_actual().camara

    def actualizar(self):
        if self.receptor.derecha < -(self.ancho / 2) + self.camara.x:
            self.eliminar_actor()
        elif self.receptor.izquierda > self.ancho / 2 + self.camara.x:
            self.eliminar_actor()
        if self.receptor.abajo > self.alto / 2 + self.camara.y:
            self.eliminar_actor()
        elif self.receptor.arriba < -(self.alto / 2) + self.camara.y:
            self.eliminar_actor()

    def eliminar_actor(self):
        self.receptor.eliminar()