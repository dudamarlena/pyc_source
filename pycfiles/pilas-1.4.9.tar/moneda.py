# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/moneda.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.animacion import Animacion

class Moneda(Animacion):
    """Representa una moneda con animación.

    .. image:: ../../pilas/data/manual/imagenes/actores/moneda.png

    Ejemplo:

        >>> moneda = pilas.actores.Moneda()

    """

    def __init__(self, pilas, x=0, y=0):
        Animacion.__init__(self, pilas, pilas.imagenes.cargar_grilla('moneda.png', 8), ciclica=True, x=x, y=y)