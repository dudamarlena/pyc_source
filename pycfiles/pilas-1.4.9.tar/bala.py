# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/bala.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor

class Bala(Actor):
    """ Representa una bala que va en línea recta. """

    def __init__(self, pilas, x=0, y=0, rotacion=0, velocidad_maxima=9, angulo_de_movimiento=90):
        u"""
        Construye la Bala.

        :param x: Posición x del proyectil.
        :param y: Posición y del proyectil.
        :param velocidad_maxima: Velocidad máxima que alcanzará el proyectil.
        :param angulo_de_movimiento: Angulo en que se moverá el Actor..

        """
        super(Bala, self).__init__(pilas=pilas, x=x, y=y)
        self.imagen = pilas.imagenes.cargar('disparos/bola_amarilla.png')
        self.rotacion = rotacion
        self.radio_de_colision = 5
        self.hacer(pilas.comportamientos.Proyectil, velocidad_maxima=velocidad_maxima, aceleracion=1, angulo_de_movimiento=angulo_de_movimiento, gravedad=0)
        self.aprender(self.pilas.habilidades.EliminarseSiSaleDePantalla)
        self.cuando_se_elimina = None
        return

    def eliminar(self):
        if self.cuando_se_elimina:
            self.cuando_se_elimina(self)
        super(Bala, self).eliminar()