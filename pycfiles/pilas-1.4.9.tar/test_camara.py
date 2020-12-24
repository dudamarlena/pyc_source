# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugoruscitti/proyectos/hugoruscitti/pilas/pilasengine/tests/test_camara.py
# Compiled at: 2016-08-25 20:52:02
import unittest, pilasengine

class TestCamara(unittest.TestCase):

    def setUp(self):
        self.pilas = pilasengine.iniciar()

    def testPuedeMoverLaCamara(self):
        self.assertEqual(0, self.pilas.camara.x, 'La cámara esta en el centro')
        self.assertEqual(0, self.pilas.camara.y, 'La cámara esta en el centro')

    def testPuedeVibrar(self):
        self.pilas.camara.vibrar()


if __name__ == '__main__':
    unittest.main()