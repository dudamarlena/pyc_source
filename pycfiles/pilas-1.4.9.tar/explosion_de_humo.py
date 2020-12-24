# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/explosion_de_humo.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.animacion import Animacion

class ExplosionDeHumo(Animacion):
    """Representa una explosion para una bomba, dinamita etc...

    Este actor se puede anexar a cualquier a otro
    para producir un efecto de explosión, por ejemplo::

        >>> actor = pilas.actores.Aceituna()
        >>> actor.aprender(pilas.habilidades.PuedeExplotarConHumo)
        >>> actor.eliminar()
    """

    def __init__(self, pilas, x, y):
        grilla = pilas.imagenes.cargar_grilla('efecto_humo_1.png', 10)
        Animacion.__init__(self, pilas, grilla, ciclica=False, x=x, y=y, velocidad=15)