# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugoruscitti/proyectos/hugoruscitti/pilas/pilasengine/tests/test_grupos.py
# Compiled at: 2016-08-25 20:52:02
import collections, sys, unittest
from PyQt4 import QtGui
import pilasengine

class Test(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar()

    def testPuedeCrearGrupos(self):
        grupo = self.pilas.actores.Grupo()
        self.assertIsInstance(grupo, collections.MutableSequence, 'Se pueden crear grupos')

    def testCuentaCorrectamenteActoresDentroDeGrupos(self):
        grupo = self.pilas.actores.Grupo()
        self.assertEquals(grupo.obtener_cantidad_de_actores(), 0, 'Hay 0 _actores al crear un grupo')
        actor = self.pilas.actores.Aceituna()
        grupo.agregar(actor)
        self.assertEquals(grupo.obtener_cantidad_de_actores(), 1, 'Hay 0 _actores al crear un grupo')
        self.assertEquals(grupo.obtener_actores(), [actor], 'Retoran correctamente los _actores')
        grupo.eliminar(actor)
        self.assertEquals(grupo.obtener_actores(), [], 'Borra correctamente un actor')
        self.assertEquals(grupo.obtener_cantidad_de_actores(), 0, 'El grupo vuelve a estar vacío')

    def testRechazaAgregarNoActores(self):
        grupo = self.pilas.actores.Grupo()
        with self.assertRaises(Exception, msg='No debe permitir agregar clases'):
            grupo.agregar(self.pilas.actores.Aceituna)
        with self.assertRaises(Exception, msg='No debe permitir agregar cosas que no sean actores'):
            grupo.agregar('hola?')

    def testLosGruposSonBidireccionales(self):
        actor = self.pilas.actores.Aceituna()
        self.assertEqual(1, actor.obtener_cantidad_de_grupos_al_que_pertenece(), 'Está en un solo grupo')
        grupo = self.pilas.actores.Grupo()
        grupo.agregar(actor)
        self.assertEqual(2, actor.obtener_cantidad_de_grupos_al_que_pertenece(), 'Pasa a estar en dos grupos')
        grupo.eliminar(actor)
        self.assertEqual(1, actor.obtener_cantidad_de_grupos_al_que_pertenece(), 'Regresa a estar en un solo grupo')


if __name__ == '__main__':
    unittest.main()