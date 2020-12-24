# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/balas_dobles_desviadas.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor

class BalasDoblesDesviadas(Actor):
    """ Representa una bala que va en línea recta. """

    @classmethod
    def instanciar(cls, pilas, x=0, y=0, rotacion=0, velocidad_maxima=9, angulo_de_movimiento=90):
        b1 = pilas.actores.Bala(x=x, y=y, rotacion=rotacion, velocidad_maxima=velocidad_maxima, angulo_de_movimiento=angulo_de_movimiento - 5)
        b2 = pilas.actores.Bala(x=x, y=y, rotacion=rotacion, velocidad_maxima=velocidad_maxima, angulo_de_movimiento=angulo_de_movimiento + 5)
        return [
         b1, b2]