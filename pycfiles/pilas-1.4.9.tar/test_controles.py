# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugoruscitti/proyectos/hugoruscitti/pilas/pilasengine/tests/test_controles.py
# Compiled at: 2016-08-25 20:52:02
import sys, unittest
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtTest import QTest
import pilasengine
from pilasengine.controles import Controles
from pilasengine.controles import simbolos

class TestControles(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        import pilasengine
        self.pilas = pilasengine.iniciar()

    def testRealizaMovimientoConControles(self):

        class ActorConControles(pilasengine.actores.actor.Actor):

            def actualizar(self):
                control = self.pilas.escena_actual().control
                if control.derecha:
                    self.x += 1
                elif control.izquierda:
                    self.x -= 1

        actor = ActorConControles(self.pilas)
        self.assertEqual(0, actor.x, 'Comienza en el punto (0, 0)')
        widget = self.pilas.obtener_widget()
        QTest.keyPress(widget, QtCore.Qt.Key_Right)
        self.pilas.simular_actualizacion_logica()
        self.assertEqual(1, actor.x, 'Luego de pulsar DERECHA se mueve')
        QTest.keyRelease(widget, QtCore.Qt.Key_Right)
        QTest.keyPress(widget, QtCore.Qt.Key_Left)
        self.pilas.simular_actualizacion_logica()
        QTest.keyPress(widget, QtCore.Qt.Key_Left)
        self.pilas.simular_actualizacion_logica()
        self.assertEqual(-1, actor.x, 'Luego de pulsar dos veces                          IZQUIERDA pasa a x=-1')

    def test_obtener_codigo_de_tecla_normalizado(self):
        izquierda = Controles.obtener_codigo_de_tecla_normalizado(QtCore.Qt.Key_Left)
        self.assertEqual(simbolos.IZQUIERDA, izquierda)
        derecha = Controles.obtener_codigo_de_tecla_normalizado(QtCore.Qt.Key_Right)
        self.assertEqual(simbolos.DERECHA, derecha)
        arriba = Controles.obtener_codigo_de_tecla_normalizado(QtCore.Qt.Key_Up)
        self.assertEqual(simbolos.ARRIBA, arriba)
        abajo = Controles.obtener_codigo_de_tecla_normalizado(QtCore.Qt.Key_Down)
        self.assertEqual(simbolos.ABAJO, abajo)
        espacio = Controles.obtener_codigo_de_tecla_normalizado(QtCore.Qt.Key_Space)
        self.assertEqual(simbolos.ESPACIO, espacio)


if __name__ == '__main__':
    unittest.main()