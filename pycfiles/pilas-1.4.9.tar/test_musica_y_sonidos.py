# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugoruscitti/proyectos/hugoruscitti/pilas/pilasengine/tests/test_musica_y_sonidos.py
# Compiled at: 2016-08-25 21:09:54
import sys, unittest
from PyQt4 import QtGui
import pilasengine

class TestMusicaYSonidos(unittest.TestCase):
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.pilas = pilasengine.iniciar()

    def testPuedeCargarMusica(self):
        musica = self.pilas.musica.cargar('audio/grito.wav')
        musica.reproducir()
        musica.detener()
        self.assertTrue('grito' in str(musica), 'La musica se describe correctamente así: %s.' % str(musica))

    def testPuedeCargarSonido(self):
        sonido = self.pilas.sonidos.cargar('audio/grito.wav')
        sonido.reproducir()
        sonido.detener()
        self.assertTrue('grito' in str(sonido), 'El sonido se describe correctamente: %s.' % str(sonido))

    def testPuedeDetenerGradualmente(self):
        sonido = self.pilas.sonidos.cargar('audio/grito.wav')
        sonido.reproducir()
        sonido.detener_gradualmente(2)
        musica = self.pilas.musica.cargar('audio/grito.wav')
        musica.reproducir()
        musica.detener_gradualmente(2)