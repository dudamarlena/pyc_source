# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\WidgetPlugin.py
# Compiled at: 2018-05-17 15:54:05
# Size of source mod 2**32: 773 bytes
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from yapsy.IPlugin import IPlugin

class QWidgetPlugin(QWidget, IPlugin):
    isSingleton = False


def test_QWidgetPlugin():
    from pyqtgraph import ImageView

    class ImageViewPlugin(QWidgetPlugin, ImageView):
        pass

    app = makeapp()
    i = ImageViewPlugin()
    i.show()
    t = QTimer()
    t.singleShot(1000, i.close)
    mainloop()


def makeapp():
    app = QApplication([])
    return app


def mainloop():
    app = QApplication.instance()
    app.exec_()