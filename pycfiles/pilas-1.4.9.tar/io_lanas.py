# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/interprete/io_lanas.py
# Compiled at: 2016-08-25 20:52:02
import sys

class Output(object):
    """Representación abstracta de un archivo de salida de datos."""

    def __init__(self, destino):
        self.destino = destino


class ErrorOutput(Output):
    """Representa la salida de error en la consola."""

    def write(self, linea):
        sys.__stderr__.write(linea)
        linea = linea.replace('Traceback (most recent call last):', 'Existe un error:')
        linea = linea.replace('File "<input>", line 1, in <module>', '')
        linea = linea.replace('File', 'en el archivo')
        linea = linea.replace('line', 'linea')
        linea = linea[:linea.find(', in')]
        if 'NameError' in linea:
            linea = linea.replace('name', 'el nombre').replace('is not defined', 'no existe')
        self.destino.insertar_error(linea.decode('utf-8'))
        self.destino.ensureCursorVisible()


class NormalOutput(Output):
    """Representa la salida estándar de la consola."""

    def write(self, linea):
        sys.__stdout__.write(linea)
        self.destino.imprimir_linea(linea.decode('utf-8'))
        self.destino.ensureCursorVisible()
        if '<bound method' in linea:
            print '\n\n ... Hey, tal vez olvidaste poner () al final de la anterior sentencia no?'