# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugoruscitti/proyectos/patin/patin/simplegui/mensajes.py
# Compiled at: 2011-11-13 17:56:09
from PyQt4 import QtGui

def cuidado(mensaje):
    QtGui.QMessageBox.warning(None, 'Cuidado', mensaje)
    return


def ingresar(titulo, texto):
    texto, ok = QtGui.QInputDialog.getText(None, titulo, texto)
    return texto