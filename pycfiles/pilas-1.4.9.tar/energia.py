# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/energia.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor
from pilasengine import colores

class Energia(Actor):
    """Representa un indicador de energia (en forma de barra horizontal)."""

    def __init__(self, pilas, x=0, y=0, progreso=100, ancho=200, alto=30, color_relleno=colores.amarillo, con_sombra=True, con_brillo=True):
        u""" Constructor de la barra de Energia.

        :param x: Posición horizontal de la barra.
        :type x: int
        :param y: Posición vertical de la barra.
        :type y: int
        :param progreso: Valor actual de la barra de enegia. Debe tener un valor entre 0 o 100.
        :type progreso: int
        :param ancho: Ancho de la barra de energia en pixeles.
        :type ancho: int
        :param alto: Alto de la barra de energia en pixeles.
        :type alto: int
        :param color_relleno: Color de la barra de Energia.
        :type color_relleno: pilas.colores.Color
        :param con_sombra: Permite mostrar una pequeña sombra en la barra de Energia.
        :type con_sombra: boolean
        :param con_brillo: Permite mostrar un pequeño brillo en la barra de Energia.
        :type con_brillo: boolean

        """
        Actor.__init__(self, pilas, x=x, y=y)
        self.area_ancho = ancho
        self.area_alto = alto
        self._progreso = progreso
        self.progreso_anterior = progreso
        self.imagen = pilas.imagenes.cargar_superficie(self.area_ancho, self.area_alto)
        self.color_relleno = color_relleno
        self.con_sombra = con_sombra
        self.con_brillo = con_brillo
        self.pintar_imagen()
        self.fijo = True
        self.miniatura = None
        return

    def pintar_imagen(self):
        """ Dibuja la barra de energia en pantalla. """
        self.imagen.limpiar()
        color_relleno = self.color_relleno
        brillo = colores.blanco_transparente
        sombra = colores.gris_transparente
        area = self.area_ancho / 100.0
        self.imagen.rectangulo(0, 0, area * self.progreso, self.area_alto, color=color_relleno, relleno=True)
        if self.con_brillo:
            self.imagen.rectangulo(0, 3, area * self.progreso, 3, color=brillo, relleno=True)
        if self.con_sombra:
            self.imagen.rectangulo(0, self.area_alto - 4, area * self.progreso, 1, color=sombra, relleno=True)
        self.imagen.rectangulo(1, 1, self.area_ancho - 2, self.area_alto - 2, color=colores.negro, relleno=False, grosor=2)

    def actualizar(self):
        """ Actualiza la barra de estado por si hubiera incrementado o decrementado."""
        if self.progreso_anterior != self.progreso:
            self.progreso_anterior = self.progreso
            self.pintar_imagen()

    def cargar_miniatura(self, imagen):
        """ Permite cargar una imagen a la izqiuerda de la barra de Energia.

        :param imagen: Ruta de la imagen que se desea mostrar a la izquierda de la barra de Energia.
        :type imagen: string
        """
        if self.miniatura:
            self.miniatura.eliminar()
        self.miniatura = self.pilas.actores.Actor(imagen)
        self.miniatura.derecha = self.izquierda - 5
        self.miniatura.arriba = self.arriba
        self.miniatura.fijo = True

    def definir_progreso(self, progreso):
        self.pilas.utils.interpretar_propiedad_numerica(self, 'progreso', progreso)

    def obtener_progreso(self):
        return self._progreso

    progreso = property(obtener_progreso, definir_progreso, doc='Cambia el nivel de progreso de la energia, entre 0 y 100')