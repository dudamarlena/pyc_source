# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/interfaz/elemento.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores import actor

class Elemento(actor.Actor):

    def __init__(self, pilas=None, x=0, y=0):
        super(Elemento, self).__init__(pilas, x=x, y=y)
        self.z = -1000
        self.radio_de_colision = None
        self.tiene_el_foco = False
        self.pilas.escena_actual().click_de_mouse.conectar(self.cuando_hace_click)
        self._visible = True
        self.activo = True
        return

    def obtener_foco(self):
        """Retorna True si el actor tiene foco."""
        self.tiene_el_foco = True

    def perder_foco(self):
        """Quita el foco sobre el elemento."""
        self.tiene_el_foco = False

    def cuando_hace_click(self, evento):
        """Se encarga de atender el evento click y conseguir foco."""
        if self._visible:
            if self.colisiona_con_un_punto(evento.x, evento.y):
                self.obtener_foco()
            else:
                self.perder_foco()

    def ocultar(self):
        """Oculta el elemento de la interfaz."""
        self.transparencia = 100
        self._visible = False
        self.activo = False

    def mostrar(self):
        """Muestra el elemento."""
        self._visible = True
        self.activar()

    def activar(self):
        self.activo = True
        self.transparencia = 0

    def desactivar(self):
        self.activo = False
        self.transparencia = 50