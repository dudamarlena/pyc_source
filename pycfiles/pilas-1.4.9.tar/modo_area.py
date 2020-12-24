# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/depurador/modo_area.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.depurador.modo import ModoDepurador

class ModoArea(ModoDepurador):

    def __init__(self, pilas, depurador):
        ModoDepurador.__init__(self, pilas, depurador)

    def cuando_dibuja_actor(self, actor, painter):
        self._dibujar_rectangulo(painter, actor)

    def _dibujar_rectangulo(self, painter, actor):
        dx, dy = actor.centro
        ancho = actor.ancho
        alto = actor.alto
        self._definir_trazo_negro(painter)
        painter.drawRect(-dx, -dy, ancho, alto)
        self._definir_trazo_blanco(painter)
        painter.drawRect(-dx, -dy, ancho, alto)