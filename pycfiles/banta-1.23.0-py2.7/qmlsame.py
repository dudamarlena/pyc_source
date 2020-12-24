# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\experimental\qmlsame.py
# Compiled at: 2012-11-30 04:23:54
from __future__ import absolute_import, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)
import PySide.QtCore as _qc, banta.packages as _pack

class QMLSame(_pack.GenericModule):
    REQUIRES = []
    NAME = b'samegame'
    products = _qc.Signal(int)

    def __init__(self, app):
        super(QMLSame, self).__init__(app)
        self.app.window.acSameGame.setEnabled(False)

    def load(self):
        import PySide.QtDeclarative
        self.f = PySide.QtDeclarative.QDeclarativeView()
        self.f.setSource(b'qrc:/same/samegame.qml')
        self.f.setWindowTitle(b'Iguales')
        self.f.setWindowIcon(self.app.window.windowIcon())
        self.app.window.acSameGame.triggered.connect(self.show)
        self.app.window.acSameGame.setEnabled(True)
        self.f.engine().quit.connect(self.f.close)

    @_qc.Slot()
    def show(self):
        self.f.show()