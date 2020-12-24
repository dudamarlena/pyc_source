# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/planeta.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor

class Planeta(Actor):
    """Representa un planeta para utilizar con el ovni.

        .. image:: ../../pilas/data/manual/imagenes/actores/planeta_azul.png

    """

    def iniciar(self, x, y):
        self.x = x
        self.y = y
        self.cambiar_color('azul')

    def cambiar_color(self, color):
        if color in ('azul', 'marron', 'naranja', 'rojo', 'verde'):
            self.imagen = self.pilas.imagenes.cargar(('planeta_{}.png').format(color))
        else:
            raise Exception('No se puede definir el color ' + color)

    def actualizar(self):
        pass