# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugoruscitti/proyectos/hugoruscitti/pilas/pilasengine/tests/test_escenas.py
# Compiled at: 2016-08-25 20:52:02
import sys, unittest
from PyQt4 import QtGui
import pilasengine

class TestEscenas(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar()

    def testPuedeCrearVincularUnaEscena(self):

        class EscenaNueva(pilasengine.escenas.Escena):
            pass

        self.pilas.escenas.vincular(EscenaNueva)
        escena = self.pilas.escenas.EscenaNueva()
        self.assertTrue(escena, 'A creado la escena correctamente.')
        self.assertEqual(escena, self.pilas.escena_actual(), 'Ha vinculado la escena correctamente.')

    def testInformaConUnaExcepcionSiFaltaArgumentoPilas(self):

        class EscenaNueva(pilasengine.escenas.Escena):
            pass

        with self.assertRaises(Exception):
            EscenaNueva()


if __name__ == '__main__':
    unittest.main()