# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugoruscitti/proyectos/hugoruscitti/pilas/pilasengine/tests/test_general.py
# Compiled at: 2016-08-25 20:52:02
import sys, unittest
from PyQt4 import QtGui
import pilasengine

class TestGeneral(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        import pilasengine
        self.pilas = pilasengine.iniciar()

    def testEscribirConAvisar(self):
        actor = self.pilas.avisar('Hola mundo !!')


if __name__ == '__main__':
    unittest.main()