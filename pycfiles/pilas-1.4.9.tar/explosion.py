# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/explosion.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.animacion import Animacion

class Explosion(Animacion):
    """Representa una explosion para una bomba, dinamita etc...

    El actor simplemente aparece reproduciendo un sonido y
    haciendo una animación:

        >>> actor = pilas.actores.Bomba()

    .. image:: ../../pilas/data/manual/imagenes/actores/explosion.png

    y una vez que termina se elimina a sí mismo.

    Este actor también se puede anexar a cualquier
    otro para producir explosiones. Cuando enseñamos a un
    actor a explotar (por ejemplo un pingüino), el actor
    ``Explosion`` aparece cuando se elimina al actor::

        >>> actor = pilas.actores.Pingu()
        >>> actor.aprender(pilas.habilidades.PuedeExplotar)
        >>> actor.eliminar()
    """

    def __init__(self, pilas, x, y):
        grilla = pilas.imagenes.cargar_grilla('explosion.png', 7)
        Animacion.__init__(self, pilas, grilla, ciclica=False, x=x, y=y, velocidad=10)
        self.sonido_explosion = pilas.sonidos.cargar('audio/explosion.wav')
        self.sonido_explosion.reproducir()