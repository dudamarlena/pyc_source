# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/texto_inferior.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.texto import Texto
from pilasengine.colores import blanco

class TextoInferior(Texto):
    """Representa un texto al pie de la ventana.

    Esta clase se utiliza desde el método "pilas.avisar()".
    """

    def __init__(self, pilas, texto='Sin texto', magnitud=20, retraso=5):
        u"""Inicializa el texto.

        :param texto: Texto a mostrar.
        :param magnitud: Tamaño del texto.
        """
        Texto.__init__(self, pilas, texto, magnitud)
        izquierda, _, _, abajo = self.obtener_bordes()
        self.z = -100
        TextoInferior.anterior_texto = self
        self.centro = ('centro', 'centro')
        self.izquierda = izquierda + 10
        self.color = pilas.colores.blanco
        self.altura_desvanecimiento = magnitud * 2.5
        self.y = abajo + magnitud - self.altura_desvanecimiento
        self.y = [self.y + self.altura_desvanecimiento]
        self.fijo = True
        pilas.tareas.una_vez(retraso, self.desvanecer)

    def desvanecer(self):
        self.y = [
         self.y - self.altura_desvanecimiento]
        self.pilas.tareas.una_vez(1, self.eliminar)

    def obtener_bordes(self):
        return self.pilas.obtener_widget().obtener_bordes()