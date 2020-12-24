# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/sonidos/sonido.py
# Compiled at: 2016-08-25 21:09:54
import os

class Sonido(object):
    deshabilitado = False

    def __init__(self, ruta):
        import pygame
        self.ruta = ruta
        if not Sonido.deshabilitado:
            self.sonido = pygame.mixer.Sound(ruta)

    def reproducir(self, repetir=False):
        if not Sonido.deshabilitado:
            if repetir:
                self.sonido.play(-1)
            else:
                self.sonido.play()

    def detener(self):
        """Detiene el audio."""
        if not Sonido.deshabilitado:
            self.sonido.stop()

    def detener_gradualmente(self, segundos=2):
        if not Sonido.deshabilitado:
            self.sonido.fadeout(segundos * 1000)

    def pausar(self):
        """Hace una pausa del audio."""
        if not Sonido.deshabilitado:
            self.sonido.stop()

    def continuar(self):
        u"""Continúa reproduciendo el audio."""
        if not Sonido.deshabilitado:
            self.sonido.play()

    def __repr__(self):
        nombre = os.path.basename(self.ruta)
        if Sonido.deshabilitado:
            return "<%s Deshabilitado, del archivo '%s'>" % (self.__class__.__name__, nombre)
        else:
            return "<%s del archivo '%s'>" % (self.__class__.__name__, nombre)


class SonidoDeshabilitado(object):

    def __init__(self, ruta):
        self.ruta = ruta

    def reproducir(self, repetir=False):
        pass

    def detener(self):
        pass

    def pausar(self):
        pass

    def continuar(self):
        pass

    def __repr__(self):
        nombre = os.path.basename(self.ruta)
        return "<%s deshabilitado del archivo '%s'>" % (self.__class__.__name__, nombre)

    def detener_gradualmente(self, segundos=2):
        pass