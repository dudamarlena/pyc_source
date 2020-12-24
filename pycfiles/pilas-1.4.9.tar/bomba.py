# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/bomba.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.animacion import Animacion

class Bomba(Animacion):
    """Representa una bomba que puede explotar...

    .. image:: ../../pilas/data/manual/imagenes/actores/bomba.png

    La bomba adquiere la habilidad explotar al momento de crearse, así
    que puedes invocar a su método "explotar" y la bomba hará un
    explosión en pantalla con sonido.

    Este es un ejemplo de uso del actor:

        >>> bomba = pilas.actores.Bomba()
        >>> bomba.explotar()
    """

    def __init__(self, pilas, *k, **kv):
        Animacion.__init__(self, pilas, *k, **kv)

    def pre_iniciar(self, x=0, y=0):
        grilla = self.pilas.imagenes.cargar_grilla('bomba.png', 2)
        Animacion.pre_iniciar(self, grilla, ciclica=True, x=x, y=y, velocidad=10)
        self.radio_de_colision = 25
        self.aprender(self.pilas.habilidades.PuedeExplotar)

    def explotar(self):
        """Hace explotar a la bomba y la elimina de la pantalla."""
        self.eliminar()