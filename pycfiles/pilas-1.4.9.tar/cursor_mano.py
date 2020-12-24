# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/cursor_mano.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine import actores

class CursorMano(actores.Actor):

    def pre_iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self._cargar_imagenes()
        self.imagen = self.imagen_normal
        self.centro = ('izquierda', 'arriba')
        self.z = -200
        self.pulsado = False
        self.pilas.escena_actual().mueve_mouse.conectar(self.cuando_mueve_el_mouse)
        self.pilas.escena_actual().click_de_mouse.conectar(self.cuando_pulsa_el_mouse)
        self.pilas.escena_actual().termina_click.conectar(self.cuando_suelta_el_mouse)
        self.aprender(self.pilas.habilidades.SeguirAlMouse)
        self.pilas.ocultar_puntero_del_mouse()

    def _cargar_imagenes(self):
        self.imagen_normal = self.pilas.imagenes.cargar('cursores/normal.png')
        self.imagen_arrastrando = self.pilas.imagenes.cargar('cursores/arrastrando.png')

    def cuando_pulsa_el_mouse(self, evento):
        self.pulsado = True

    def cuando_mueve_el_mouse(self, evento):
        if self.pulsado:
            self.imagen = self.imagen_arrastrando
            self.centro = ('izquierda', 'arriba')

    def cuando_suelta_el_mouse(self, evento):
        if self.pulsado:
            self.imagen = self.imagen_normal
            self.pulsado = False
            self.centro = ('izquierda', 'arriba')