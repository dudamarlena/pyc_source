# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/misil.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor

class Misil(Actor):
    """Representa un misil que va en línea recta con aceleración."""

    def __init__(self, pilas, x=0, y=0, rotacion=0, velocidad_maxima=9, angulo_de_movimiento=90):
        u"""
        Construye el Misil.

        :param x: Posición x del proyectil.
        :param y: Posición y del proyectil.
        :param rotacion: Angulo de rotación del Actor.
        :param velocidad_maxima: Velocidad máxima que alcanzará el proyectil.
        :param angulo_de_movimiento: Angulo en que se moverá el Actor..

        """
        super(Misil, self).__init__(pilas=pilas, x=x, y=y)
        self.imagen = pilas.imagenes.cargar_grilla('disparo.png', 2)
        self.velocidad_maxima = velocidad_maxima
        self.angulo_de_movimiento = angulo_de_movimiento
        self.radio_de_colision = 5
        self.rotacion = rotacion + 180
        self.hacer(self.pilas.comportamientos.Proyectil, velocidad_maxima=velocidad_maxima, aceleracion=0.4, angulo_de_movimiento=angulo_de_movimiento, gravedad=0)
        self.aprender(self.pilas.habilidades.EliminarseSiSaleDePantalla)
        self.cuando_se_elimina = None
        return

    def actualizar(self):
        self.imagen.avanzar(20)

    def eliminar(self):
        if self.cuando_se_elimina:
            self.cuando_se_elimina(self)
        super(Misil, self).eliminar()