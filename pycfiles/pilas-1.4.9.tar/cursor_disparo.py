# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/cursor_disparo.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine import actores

class CursorDisparo(actores.Actor):

    def __init__(self, pilas, *k, **kv):
        actores.Actor.__init__(self, pilas, *k, **kv)

    def pre_iniciar(self, x=0, y=0, usar_el_mouse=True):
        if usar_el_mouse:
            self.aprender(self.pilas.habilidades.SeguirAlMouse)
            self.pilas.ocultar_puntero_del_mouse()
        self.imagen = self.pilas.imagenes.cargar('cursordisparo.png')
        self.rotacion = 0
        self.radio_de_colision = 25