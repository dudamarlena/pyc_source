# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/interfaz/boton.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.interfaz import elemento

class Boton(elemento.Elemento):

    def __init__(self, pilas=None, texto='Sin Texto', x=0, y=0):
        super(Boton, self).__init__(pilas, x=x, y=y)
        self.z = -1000
        self.radio_de_colision = None
        self.texto = texto
        self._crear_imagenes_de_botones()
        self.centro = ('centro', 'centro')
        self.funcion = None
        self.fijo = True
        self.contador_demora_click = 0
        self.pilas.escena_actual().mueve_mouse.conectar(self.cuando_mueve_el_mouse)
        self.pilas.escena_actual().click_de_mouse.conectar(self.cuando_hace_click)
        return

    def actualizar(self):
        if self.contador_demora_click > 0:
            self.contador_demora_click -= 1

    def conectar(self, funcion):
        u"""Asocia la función a ejecutar cuando se haga click sobre el botón.

        :param funcion: Referencia a la función que se desea vincular.
        """
        self.funcion = funcion

    def cuando_mueve_el_mouse(self, evento):
        """Detecta el movimiento del mouse.

        :param evento: El objeto que representa el movimiento del mouse.
        """
        if self.activo:
            if self.colisiona_con_un_punto(evento.x, evento.y):
                self.imagen = self.imagen_sobre
            else:
                self.imagen = self.imagen_normal

    def cuando_hace_click(self, evento):
        u"""Gestiona los clicks sobre el botón.

        :param evento: Evento que representa al click.
        """
        if self.activo and self.contador_demora_click == 0:
            if self.colisiona_con_un_punto(evento.x, evento.y):
                self.imagen = self.imagen_click
                if self.funcion:
                    self.funcion()
                self.pilas.escena_actual().tareas.una_vez(0.5, self.restaurar_imagen_luego_de_click)
                self.contador_demora_click = 60

    def restaurar_imagen_luego_de_click(self):
        self.imagen = self.imagen_normal

    def _crear_imagenes_de_botones(self):
        """Genera las 3 imagenes de los botones."""
        ancho, alto = self.pilas.utils.obtener_area_de_texto(self.texto)
        tema = self.pilas.imagenes.cargar('boton/tema.png')
        self.imagen_normal = self._crear_imagen(tema, self.texto, ancho, 0)
        self.imagen_sobre = self._crear_imagen(tema, self.texto, ancho, 103)
        self.imagen_click = self._crear_imagen(tema, self.texto, ancho, 205, 1)
        self.imagen = self.imagen_normal

    def _crear_imagen(self, tema, texto, ancho, dx, dy_texto=0):
        """Genera una imagen de superficie de boton."""
        imagen = self.pilas.imagenes.cargar_superficie(20 + ancho, 30)
        imagen.pintar_parte_de_imagen(tema, dx, 0, 5, 25, 0, 0)
        for x in range(1, ancho + 20, 5):
            imagen.pintar_parte_de_imagen(tema, dx + 5, 0, 5, 25, x, 0)

        imagen.pintar_parte_de_imagen(tema, dx + 75, 0, 5, 25, ancho + 15, 0)
        imagen.texto(texto, 10, 7 + dy_texto)
        return imagen