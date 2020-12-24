# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/watcher.py
# Compiled at: 2016-08-25 20:52:02
import os, glob
from PyQt4 import QtGui
from PyQt4 import QtCore

class Watcher(QtCore.QObject):

    def __init__(self, aFile=None, callback=None, checkEvery=2):
        super(Watcher, self).__init__()
        self._cantidad_archivos_py = -1
        self._sumatoria_mtime = 0
        self.ultima_modificacion = 0
        self.cambiar_archivo_a_observar(aFile)
        self.callback = callback
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkFile)
        self._timer.start()

    def cambiar_archivo_a_observar(self, aFile):
        if aFile:
            self.file = os.path.dirname(os.path.realpath(aFile))
            self._actualizar_contadores_de_archivos()
            self.ultima_modificacion = os.path.getmtime(self.file)
        else:
            self.file = None
        return

    def _actualizar_contadores_de_archivos(self):
        self._sumatoria_mtime = 0
        archivos_py = glob.glob(self.file + '/*.py')
        for name in archivos_py:
            self._sumatoria_mtime += os.path.getmtime(name)

        self._cantidad_archivos_py = len(archivos_py)

    def prevenir_reinicio(self):
        if self.file:
            self._actualizar_contadores_de_archivos()

    def _checkFile(self):
        if not self.file:
            return
        anterior_cantidad_archivos_py = self._cantidad_archivos_py
        anterior_sumatoria_mtime = self._sumatoria_mtime
        self._actualizar_contadores_de_archivos()
        if anterior_cantidad_archivos_py != self._cantidad_archivos_py or anterior_sumatoria_mtime != self._sumatoria_mtime:
            if self.callback:
                self.callback()