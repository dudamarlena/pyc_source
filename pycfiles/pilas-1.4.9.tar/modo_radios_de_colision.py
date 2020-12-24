# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/depurador/modo_radios_de_colision.py
# Compiled at: 2016-08-25 20:52:02
from PyQt4 import QtCore
from pilasengine.depurador.modo import ModoDepurador

class ModoRadiosDeColision(ModoDepurador):

    def __init__(self, pilas, depurador):
        ModoDepurador.__init__(self, pilas, depurador)

    def cuando_dibuja_actor(self, actor, painter):
        pass

    def _dibujar_circulo(self, painter, x, y, radio):
        self._definir_trazo_negro(painter)
        painter.drawEllipse(-radio, -radio, radio * 2, radio * 2)
        self._definir_trazo_blanco(painter)
        painter.drawEllipse(-radio, -radio, radio * 2, radio * 2)