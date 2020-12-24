# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/PyTplot/PyTplot/pytplot/QtPlotter/CustomLegend/CustomLegend.py
# Compiled at: 2020-04-30 01:29:24
# Size of source mod 2**32: 1720 bytes
import pyqtgraph as pg
from pyqtgraph import GraphicsWidget
from pyqtgraph import LabelItem
from pyqtgraph import functions as fn
import pyqtgraph.Point as Point
__all__ = [
 'LegendItem']

class CustomLegendItem(pg.LegendItem):

    def addItem(self, name1, name2):
        label1 = LabelItem(name1)
        label2 = LabelItem(name2)
        row = self.layout.rowCount()
        self.items.append((label1, label2))
        self.layout.addItem(label1, row, 0)
        self.layout.addItem(label2, row, 1)
        self.updateSize()

    def removeItem(self, name):
        for label, data in self.items:
            if label.text == name:
                self.items.remove((label, data))
                self.layout.removeItem(label)
                label.close()
                self.layout.removeItem(data)
                data.close()
                self.updateSize()

    def setItem(self, label_name, new_data):
        for label, data in self.items:
            if label.text == label_name:
                data.setText(new_data)
                return

        self.addItem(label_name, new_data)

    def paint(self, p, *args):
        p.setPen(fn.mkPen(255, 255, 255, 0))
        p.setBrush(fn.mkBrush(0, 0, 0, 190))
        p.drawRect(self.boundingRect())

    def hoverEvent(self, ev):
        pass

    def mouseDragEvent(self, ev):
        pass