# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/banana.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor

class Banana(Actor):
    """Muestra una banana que se combina (temáticamente) con el actor Mono.

    .. image:: ../../pilas/data/manual/imagenes/actores/banana.png

    Este actor se podría usar cómo alimento o bonus para otros
    actores.

    Este actor tiene solo dos cuadros de animación que se pueden
    mostrar con los métodos ``abrir`` y ``cerrar``:

        >>> banana = pilas.actores.Banana()
        >>> banana.abrir()
        >>> banana.cerrar()

    """

    def pre_iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.imagen = self.pilas.imagenes.cargar_grilla('banana.png', 2)
        self.definir_cuadro(0)

    def definir_cuadro(self, indice):
        """ Define el frame de la Banana a mostrar."""
        self.imagen.definir_cuadro(indice)

    def abrir(self):
        u"""Muestra el gráfico de la banana abierta con menos cáscara."""
        self.definir_cuadro(1)

    def cerrar(self):
        u"""Muestra el gráfico de banana normal (con cáscara)."""
        self.definir_cuadro(0)