# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugoruscitti/proyectos/hugoruscitti/pilas/pilasengine/tests/test_iniciar.py
# Compiled at: 2016-08-25 20:52:02
import sys, unittest
from PyQt4 import QtGui
import pilasengine

class TestIniciar(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar()

    def testIniciaronTodosLosModulos(self):
        self.assertTrue(self.pilas.actores, 'Existe el modulo actores')
        self.assertTrue(self.pilas.escenas, 'Existe el modulo escenas')
        self.assertTrue(self.pilas.imagenes, 'Existe el modulo escenas')
        self.assertTrue(self.pilas.habilidades, 'Existe el modulo habilidades')
        self.assertTrue(self.pilas.eventos, 'Existe el modulo eventos')
        self.assertTrue(self.pilas.utils, 'Existe el modulo escenas')
        self.assertTrue(self.pilas.widget, 'Existe el componente widget')

    def testPuedeCrearUnActor(self):
        un_actor = self.pilas.actores.Aceituna()
        self.assertTrue(un_actor, 'Existe el actor')
        self.assertEquals(un_actor.x, 0, 'Se ubica en la posicion x=0')
        self.assertEquals(un_actor.y, 0, 'Se ubica en la posicion y=0')

    def testPuedeEliminarUnActor(self):
        actor = self.pilas.actores.Aceituna()
        self.assertTrue(actor, 'Creando un actor')
        actor.eliminar()

    def testAreaDePantalla(self):
        centro = self.pilas.obtener_centro_fisico()
        self.assertEqual((320, 240), centro, 'El centro es la mitad de 640x480')

    def testDetenerBucleDosVecesFalla(self):
        self.pilas.widget.detener_bucle_principal()
        with self.assertRaises(Exception, msg='No se permite detener el bucle dos veces'):
            self.pilas.widget.detener_bucle_principal()

    def testReiniciarBucleDosVecesFalla(self):
        self.pilas.widget.detener_bucle_principal()
        self.pilas.widget.reiniciar_bucle_principal()
        with self.assertRaises(Exception, msg='No se permite reiniciar al bucle dos veces'):
            self.pilas.widget.reiniciar_bucle_principal()


if __name__ == '__main__':
    unittest.main()