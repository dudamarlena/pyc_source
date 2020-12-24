# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/exporters/PrintExporter.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2671 bytes
from .Exporter import Exporter
from ..parametertree import Parameter
from ..Qt import QtGui, QtCore, QtSvg
import re
__all__ = ['PrintExporter']

class PrintExporter(Exporter):
    Name = 'Printer'

    def __init__(self, item):
        Exporter.__init__(self, item)
        tr = self.getTargetRect()
        self.params = Parameter(name='params', type='group', children=[
         {'name':'width', 
          'type':'float',  'value':0.1,  'limits':(0, None),  'suffix':'m',  'siPrefix':True},
         {'name':'height', 
          'type':'float',  'value':0.1 * tr.height() / tr.width(),  'limits':(0, None),  'suffix':'m',  'siPrefix':True}])
        self.params.param('width').sigValueChanged.connect(self.widthChanged)
        self.params.param('height').sigValueChanged.connect(self.heightChanged)

    def widthChanged(self):
        sr = self.getSourceRect()
        ar = sr.height() / sr.width()
        self.params.param('height').setValue((self.params['width'] * ar), blockSignal=(self.heightChanged))

    def heightChanged(self):
        sr = self.getSourceRect()
        ar = sr.width() / sr.height()
        self.params.param('width').setValue((self.params['height'] * ar), blockSignal=(self.widthChanged))

    def parameters(self):
        return self.params

    def export(self, fileName=None):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        dialog = QtGui.QPrintDialog(printer)
        dialog.setWindowTitle('Print Document')
        if dialog.exec_() != QtGui.QDialog.Accepted:
            return
        sr = self.getSourceRect()
        res = QtGui.QDesktopWidget().physicalDpiX()
        printer.setResolution(res)
        rect = printer.pageRect()
        center = rect.center()
        h = self.params['height'] * res * 100.0 / 2.54
        w = self.params['width'] * res * 100.0 / 2.54
        x = center.x() - w / 2.0
        y = center.y() - h / 2.0
        targetRect = QtCore.QRect(x, y, w, h)
        sourceRect = self.getSourceRect()
        painter = QtGui.QPainter(printer)
        try:
            self.setExportMode(True, {'painter': painter})
            self.getScene().render(painter, QtCore.QRectF(targetRect), QtCore.QRectF(sourceRect))
        finally:
            self.setExportMode(False)

        painter.end()