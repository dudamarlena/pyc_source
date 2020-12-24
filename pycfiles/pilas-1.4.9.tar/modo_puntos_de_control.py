# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/depurador/modo_puntos_de_control.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.depurador.modo import ModoDepurador
from pilasengine.colores import blanco

class ModoPuntosDeControl(ModoDepurador):

    def __init__(self, pilas, depurador):
        ModoDepurador.__init__(self, pilas, depurador)

    def cuando_dibuja_actor_sin_transformacion(self, actor, painter):
        self._definir_trazo_negro(painter)
        painter.drawLine(-3, -3, 3, 3)
        painter.drawLine(-3, 3, 3, -3)
        self._definir_trazo_blanco(painter)
        painter.drawLine(-3, -3, 3, 3)
        painter.drawLine(-3, 3, 3, -3)