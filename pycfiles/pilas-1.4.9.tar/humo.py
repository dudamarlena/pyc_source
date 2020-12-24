# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/humo.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.animacion import Animacion

class Humo(Animacion):
    """Muestra una animación de una nube de humo.

    .. image:: ../../pilas/data/manual/imagenes/actores/humo.png

    La animación se ejecuta una vez y desaparece.

    """

    def __init__(self, pilas, x, y):
        grilla = pilas.imagenes.cargar_grilla('humo.png', 4)
        Animacion.__init__(self, pilas, grilla, ciclica=False, x=x, y=y, velocidad=8)