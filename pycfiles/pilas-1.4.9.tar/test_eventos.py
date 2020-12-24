# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugoruscitti/proyectos/hugoruscitti/pilas/pilasengine/tests/test_eventos.py
# Compiled at: 2016-08-25 20:52:02
import sys, unittest
from PyQt4 import QtGui
import pilasengine

class TestEventos(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar()

    def testPuedeCrearEvento(self):
        evento = self.pilas.eventos.Evento('mi_evento')
        self.assertTrue(evento, 'Puede crear un evento')

    def testPuedeConectarRespuesta(self):

        def funcion(evento):
            pass

        evento = self.pilas.eventos.Evento('mi_evento')
        evento.conectar(funcion)
        self.assertTrue(evento.esta_conectado(), 'Puede conectar respuesta')
        self.assertRaises(ValueError, evento.conectar, int, 'Solo puede conectar funciones o métodos')

    def testPuedeEmitirEvento(self):
        params = {'color': 'rojo', 'yei': ':p', 'pilas': 'pilas engine'}

        def funcion(ev):
            self.assertEquals(ev, params, 'Puede emitir evento')

        evento = self.pilas.eventos.Evento('mi_evento')
        evento.conectar(funcion)
        evento.emitir(pilas='pilas engine', color='rojo', yei=':p')

    def testPuedeDesconectarRespuesta(self):

        def funcion(ev):
            pass

        evento = self.pilas.eventos.Evento('mi_evento')
        evento.conectar(funcion, id='mi_funcion')
        evento.desconectar_por_id('mi_funcion')
        self.assertFalse(evento.esta_conectado(), 'Puede desconectar respuestas')


if __name__ == '__main__':
    unittest.main()