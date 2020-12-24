# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/interprete/editorbase/editor_con_deslizador.py
# Compiled at: 2016-08-25 20:52:02
import re
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import deslizador
EXPRESION_SENTENCIA = '.*\\s*\\=\\s*(-*\\d+\\.*\\d*)$'

class EditorConDeslizador(object):

    def _cambiar_sentencia_con_deslizador(self, nueva):
        try:
            linea = self._get_current_line()
            numero = self._obtener_numero_de_la_linea(linea)
            tc = self.textCursor()
            tc.select(QtGui.QTextCursor.LineUnderCursor)
            texto = tc.selectedText()
            texto = texto.replace(numero, str(nueva))
            tc.removeSelectedText()
            tc.insertText(texto)
            self.setTextCursor(tc)
            linea = str(self._get_current_line())
            exec linea in self.interpreterLocals
        except:
            pass

    def _obtener_numero_de_la_linea(self, linea):
        grupos = re.search(EXPRESION_SENTENCIA, linea).groups()
        return grupos[0]

    def mousePressEvent(self, event):
        retorno = QtGui.QTextEdit.mousePressEvent(self, event)
        if event.button() == Qt.RightButton:
            pos = event.pos()
            cursor = self.cursorForPosition(pos)
            self.setTextCursor(cursor)
            linea = self._get_current_line()
            try:
                if re.match(EXPRESION_SENTENCIA, str(linea)):
                    self.mostrar_deslizador()
            except UnicodeEncodeError:
                pass

        return retorno

    def _es_sentencia_asignacion_simple(self, linea):
        return re.match(EXPRESION_SENTENCIA, str(linea))

    def mostrar_deslizador(self):
        valor_inicial = self._obtener_numero_de_la_linea(self._get_current_line())
        self.deslizador = deslizador.Deslizador(self, self.textCursor(), valor_inicial, self._cambiar_sentencia_con_deslizador)
        self.deslizador.show()