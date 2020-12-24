# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/dinamita.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.animacion import Animacion

class Dinamita(Animacion):

    def __init__(self, pilas, *k, **kv):
        Animacion.__init__(self, pilas, *k, **kv)

    def pre_iniciar(self, x=0, y=0, rotacion=0, velocidad_maxima=4, angulo_de_movimiento=90):
        u"""
        Construye la Dinamita.

        :param x: Posición x del proyectil.
        :param y: Posición y del proyectil.
        :param rotacion: Angulo de rotación del Actor.
        :param velocidad_maxima: Velocidad máxima que alcanzará el proyectil.
        :param angulo_de_movimiento: Angulo en que se moverá el Actor..

        """
        grilla = self.pilas.imagenes.cargar_grilla('disparos/dinamita.png', 2)
        Animacion.pre_iniciar(self, grilla, ciclica=True, x=x, y=y, velocidad=40)
        self.rotacion = rotacion
        self.radio_de_colision = 20
        self.hacer(self.pilas.comportamientos.Proyectil, velocidad_maxima=velocidad_maxima, aceleracion=0.4, angulo_de_movimiento=angulo_de_movimiento, gravedad=3)
        self.escala = 0.7
        self.aprender('PuedeExplotar')

    def actualizar(self):
        self.rotacion += 3
        Animacion.actualizar(self)