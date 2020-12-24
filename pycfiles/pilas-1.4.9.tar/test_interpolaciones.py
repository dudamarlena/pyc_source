# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugoruscitti/proyectos/hugoruscitti/pilas/pilasengine/tests/test_interpolaciones.py
# Compiled at: 2016-08-25 20:52:02
import sys, unittest
from PyQt4 import QtGui
import pilasengine

class TestInterpolaciones(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar()

    def testPuedeInterpolarPosiciones(self):
        un_actor = self.pilas.actores.Aceituna()
        un_actor.x = [100]
        un_actor.y = [100]
        self.assertEqual(0, un_actor.x, 'La posicion inicial x es 0')

    def testPuedeInterpolarPosicionesDeBordes(self):
        un_actor = self.pilas.actores.Aceituna()
        un_actor.izquierda = [100]
        un_actor.izquierda = ([100], 10)
        self.assertEqual(0, un_actor.x, 'La posicion inicial x es 0')
        un_actor.derecha = [
         100]
        un_actor.derecha = ([100], 10)
        self.assertEqual(0, un_actor.x, 'La posicion inicial x es 0')
        un_actor.arriba = [
         100]
        un_actor.arriba = ([100], 10)
        self.assertEqual(0, un_actor.y, 'La posicion inicial y es 0')
        un_actor.abajo = [
         100]
        un_actor.abajo = ([100], 10)
        self.assertEqual(0, un_actor.y, 'La posicion inicial y es 0')


if __name__ == '__main__':
    unittest.main()