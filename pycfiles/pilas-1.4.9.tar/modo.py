# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/depurador/modo.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.colores import negro
from PyQt4 import QtGui
from PyQt4 import QtCore

class ModoDepurador(object):

    def __init__(self, pilas, depurador):
        self.pilas = pilas
        self.depurador = depurador

    def realizar_dibujado(self, painter):
        pass

    def cuando_dibuja_actor(self, actor, painter):
        pass

    def cuando_dibuja_actor_sin_transformacion(self, actor, painter):
        pass

    def sale_del_modo(self):
        pass

    def _texto(self, painter, cadena, x=0, y=0, magnitud=12, fuente=None, color=negro, alineado_a_derecha=False):
        """Imprime un texto respespetando el desplazamiento de la camara."""
        r, g, b, _ = color.obtener_componentes()
        painter.setPen(QtGui.QColor(r, g, b))
        nombre_de_fuente = painter.font().family()
        font = QtGui.QFont(nombre_de_fuente, magnitud)
        painter.setFont(font)
        if alineado_a_derecha:
            fm = QtGui.QFontMetrics(font)
            w = fm.width(cadena) + 1
            h = fm.height()
            painter.drawText(x - w, y - h, cadena)
        else:
            painter.drawText(x, y, cadena)

    def _texto_absoluto(self, painter, cadena, x=0, y=0, magnitud=10, fuente=None, color=negro, alineado_a_derecha=False):
        """Imprime un texto sin respetar al camara."""
        x, y = self.pilas.obtener_coordenada_de_pantalla_absoluta(x, y)
        self._texto(painter, cadena, x, y, magnitud, fuente, color, alineado_a_derecha)

    def _definir_trazo_negro(self, painter):
        """Define las propiedades para pintar en color negro."""
        negro = QtGui.QColor(0, 0, 0)
        pen = QtGui.QPen(negro, 4)
        painter.setBrush(QtCore.Qt.NoBrush)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        painter.setPen(pen)
        return pen

    def _definir_trazo_blanco(self, painter):
        """Define las propiedades para pintar en color blanco."""
        blanco = QtGui.QColor(255, 255, 255)
        pen = QtGui.QPen(blanco, 2)
        painter.setBrush(QtCore.Qt.NoBrush)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        painter.setPen(pen)
        return pen

    def _definir_trazo_gris(self, painter):
        """Define las propiedades para pintar en color blanco."""
        blanco = QtGui.QColor(100, 100, 100)
        pen = QtGui.QPen(blanco, 2)
        painter.setBrush(QtCore.Qt.NoBrush)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        painter.setPen(pen)
        return pen

    def _definir_trazo_verde(self, painter):
        """Define las propiedades para pintar en color blanco."""
        blanco = QtGui.QColor(150, 255, 150)
        pen = QtGui.QPen(blanco, 2)
        painter.setBrush(QtCore.Qt.NoBrush)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        painter.setPen(pen)
        return pen

    def _definir_trazo_verde_oscuro(self, painter):
        """Define las propiedades para pintar en color blanco."""
        blanco = QtGui.QColor(50, 175, 50)
        pen = QtGui.QPen(blanco, 2)
        painter.setBrush(QtCore.Qt.NoBrush)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        painter.setPen(pen)
        return pen