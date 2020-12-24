# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/habilidades/rotar_con_mouse.py
# Compiled at: 2016-08-25 21:09:54
from pilasengine import habilidades
from pilasengine import utils

class RotarConMouse(habilidades.Habilidad):
    """"Hace que un actor rote con respecto a la posicion del mouse.

    Ejemplo:

        >>> actor.aprender(pilas.habilidades.RotarConMouse,
                           lado_seguimiento='ABAJO')

    """

    def iniciar(self, receptor, lado_seguimiento='ARRIBA'):
        u"""Inicializa la Habilidad

        :param receptor: La referencia al actor.
        :param lado_seguimiento: Establece el lado del actor que rotará para
                                 estar encarado hacia el puntero del mouse.
        """
        super(RotarConMouse, self).iniciar(receptor)
        self.lados_de_seguimiento = {'ARRIBA': '90', 'ABAJO': '270', 
           'IZQUIERDA': '180', 
           'DERECHA': '0'}
        self.pilas.eventos.mueve_mouse.conectar(self.se_movio_el_mouse)
        self.pilas.eventos.actualizar.conectar(self.rotar)
        self.lado_seguimiento = int(self.lados_de_seguimiento[lado_seguimiento.upper()])
        self.raton_x = receptor.x
        self.raton_y = receptor.y

    def se_movio_el_mouse(self, evento):
        self.raton_x = evento.x
        self.raton_y = evento.y

    def rotar(self, evento):
        receptor = (
         self.receptor.x, self.receptor.y)
        raton = (self.raton_x, self.raton_y)
        angulo = self.pilas.utils.obtener_angulo_entre(receptor, raton)
        self.receptor.rotacion = angulo - self.lado_seguimiento