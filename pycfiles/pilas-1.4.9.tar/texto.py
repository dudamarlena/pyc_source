# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/imagenes/texto.py
# Compiled at: 2016-08-25 20:52:02
import os
from PyQt4 import QtGui
from PyQt4 import QtCore
from pilasengine.imagenes.superficie import Superficie
from pilasengine import utils

class Texto(Superficie):

    def __init__(self, pilas, texto, magnitud, vertical, fuente, color, ancho):
        ancho, alto = self.obtener_area_de_texto(texto, magnitud, vertical, fuente, ancho)
        Superficie.__init__(self, pilas, ancho, alto)
        self._ancho_del_texto = ancho
        self.dibujar_texto = self.texto
        self.dibujar_texto(texto, magnitud=magnitud, fuente=fuente, color=color, ancho=ancho, vertical=vertical)
        self.ruta_original = texto.encode('ascii', 'xmlcharrefreplace') + str(os.urandom(25))
        self.texto = texto

    def obtener_area_de_texto(self, cadena, magnitud=10, vertical=False, fuente=None, ancho=0):
        pic = QtGui.QPicture()
        p = QtGui.QPainter(pic)
        if fuente:
            nombre_de_fuente = self.cargar_fuente(fuente)
        else:
            nombre_de_fuente = p.font().family()
        font = QtGui.QFont(nombre_de_fuente, magnitud)
        p.setFont(font)
        alto = 0
        if vertical:
            lineas = [ t for t in cadena ]
        else:
            lineas = cadena.split('\n')
        if not ancho:
            flags = QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        else:
            flags = QtCore.Qt.AlignLeft | QtCore.Qt.TextWordWrap | QtCore.Qt.AlignTop
        for line in lineas:
            if line == '':
                line = ' '
            brect = p.drawText(QtCore.QRect(0, 0, ancho, 2000), flags, line)
            ancho = max(ancho, brect.width())
            alto += brect.height()

        p.end()
        return (ancho, alto)