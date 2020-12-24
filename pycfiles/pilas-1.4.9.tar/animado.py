# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/animado.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor
import copy

class Animado(Actor):
    """Representa un actor que tiene asociada una grilla con cuadros de animacion.

    Una de las variantes que introduce este actor es el
    método 'definir_cuadro', que facilita la animación de personajes.

    Por ejemplo, si tenemos una grilla con un pingüino, podríamos
    mostrarlo usando este código:

        >>> grilla = pilas.imagenes.cargar_grilla("pingu.png", 10)
        >>> actor = Animado(grilla)
        >>> actor.definir_cuadro(2)
        >>> actor.definir_cuadro(5)

    .. image:: ../../pilas/data/manual/imagenes/actores/pingu.png
    """

    def __init__(self, pilas, *k, **kv):
        u""" Constructor del Actor.

        :param grilla: Grilla de imagenes obtenida mediante pilas.imagenes.cargar_grilla()
        :type grilla: `Grilla`
        :param x: Posición horizontal del Actor.
        :type x: int
        :param y: Posición vertical del Actor.
        :type y: int
        """
        Actor.__init__(self, pilas, *k, **kv)

    def pre_iniciar(self, x=0, y=0, grilla=None):
        self.imagen = copy.copy(grilla)
        self.definir_cuadro(0)

    def definir_cuadro(self, indice):
        u""" Permite cambiar el cuadro de animación a mostrar

        :param indice: Número del frame de la grilla que se quiere monstrar.
        :type indice: int
        """
        self.imagen.definir_cuadro(indice)
        self.centro = ('centro', 'centro')