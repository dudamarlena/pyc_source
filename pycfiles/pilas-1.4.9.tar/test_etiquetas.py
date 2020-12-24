# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugoruscitti/proyectos/hugoruscitti/pilas/pilasengine/tests/test_etiquetas.py
# Compiled at: 2016-08-25 20:52:02
import sys, time, unittest
from PyQt4 import QtGui
import pilasengine

class TestEtiquetas(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar(modo_test=True)

    def testEtiquetasEnActores(self):
        m = self.pilas.actores.Mono()
        self.assertEquals(str(m.etiquetas), "['mono']")
        a = self.pilas.actores.Aceituna()
        self.assertEquals(str(a.etiquetas), "['aceituna']")
        a.etiquetas.agregar('enemigo')
        self.assertEquals(str(a.etiquetas), "['aceituna', 'enemigo']")
        a.etiquetas.eliminar('enemigo')
        self.assertEquals(str(a.etiquetas), "['aceituna']")

    def testEtiquetasEnFiguras(self):
        m = self.pilas.fisica.Circulo()
        self.assertEquals(str(m.etiquetas), "['circulo']")
        rectangulo = self.pilas.fisica.Rectangulo(0, 0, 100, 100)
        self.assertEquals(str(rectangulo.etiquetas), "['rectangulo']")
        rectangulo.etiquetas.agregar('enemigo')
        self.assertEquals(str(rectangulo.etiquetas), "['rectangulo', 'enemigo']")
        rectangulo.etiquetas.eliminar('enemigo')
        self.assertEquals(str(rectangulo.etiquetas), "['rectangulo']")


if __name__ == '__main__':
    unittest.main()