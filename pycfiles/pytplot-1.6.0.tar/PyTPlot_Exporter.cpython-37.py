# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/PyTplot/PyTplot/pytplot/QtPlotter/PyTPlot_Exporter.py
# Compiled at: 2020-04-04 16:23:02
# Size of source mod 2**32: 5669 bytes
import pyqtgraph as pg, numpy as np
import pyqtgraph.functions as fn
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.exporters import Exporter
from pyqtgraph.parametertree import Parameter

class PytplotExporter(pg.exporters.ImageExporter):

    def __init__(self, item):
        Exporter.__init__(self, item)
        tr = self.getTargetRect()
        if isinstance(item, QtGui.QGraphicsItem):
            scene = item.scene()
        else:
            scene = item
        bgbrush = scene.backgroundBrush()
        bg = bgbrush.color()
        if bgbrush.style() == QtCore.Qt.NoBrush:
            bg.setAlpha(0)
        self.params = Parameter(name='params', type='group', children=[
         {'name':'width', 
          'type':'int',  'value':tr.width(),  'limits':(0, None)},
         {'name':'height', 
          'type':'int',  'value':tr.height(),  'limits':(0, None)},
         {'name':'antialias', 
          'type':'bool',  'value':True},
         {'name':'background', 
          'type':'color',  'value':bg}])
        self.params.param('width').sigValueChanged.connect(self.widthChanged)
        self.params.param('height').sigValueChanged.connect(self.heightChanged)

    def export(self, fileName=None, toBytes=False, copy=False):
        if fileName is None:
            if not toBytes:
                if not copy:
                    if pg.Qt.USE_PYSIDE:
                        filter = ['*.' + str(f) for f in QtGui.QImageWriter.supportedImageFormats()]
                    else:
                        filter = ['*.' + bytes(f).decode('utf-8') for f in QtGui.QImageWriter.supportedImageFormats()]
                    preferred = [
                     '*.png', '*.tif', '*.jpg']
                    for p in preferred[::-1]:
                        if p in filter:
                            filter.remove(p)
                            filter.insert(0, p)

                    self.fileSaveDialog(filter=filter)
                    return
        else:
            targetRect = QtCore.QRect(0, 0, self.params['width'], self.params['height'])
            sourceRect = self.getSourceRect()
            w, h = self.params['width'], self.params['height']
            if not w == 0:
                if h == 0:
                    raise Exception('Cannot export image with size=0 (requested export size is %dx%d)' % (w, h))
                bg = np.empty((int(self.params['width']), int(self.params['height']), 4), dtype=(np.ubyte))
                color = self.params['background']
                bg[:, :, 0] = color.blue()
                bg[:, :, 1] = color.green()
                bg[:, :, 2] = color.red()
                bg[:, :, 3] = color.alpha()
                self.png = fn.makeQImage(bg, alpha=True)
                origTargetRect = self.getTargetRect()
                resolutionScale = targetRect.width() / origTargetRect.width()
                painter = QtGui.QPainter(self.png)
                try:
                    self.setExportMode(True, {'antialias':self.params['antialias'], 
                     'background':self.params['background'],  'painter':painter, 
                     'resolutionScale':resolutionScale})
                    painter.setRenderHint(QtGui.QPainter.Antialiasing, self.params['antialias'])
                    self.getScene().render(painter, QtCore.QRectF(0, 0, 1, 1), QtCore.QRectF(0, 0, 1, 1))
                    self.getScene().render(painter, QtCore.QRectF(targetRect), QtCore.QRectF(sourceRect))
                finally:
                    self.setExportMode(False)

                painter.end()
                if copy:
                    QtGui.QApplication.clipboard().setImage(self.png)
            else:
                if toBytes:
                    return self.png
                self.png.save(fileName)

    def getPaintItems(self, root=None):
        """Return a list of all items that should be painted in the correct order."""
        if root is None:
            root = self.item
        preItems = []
        postItems = []
        if isinstance(root, QtGui.QGraphicsScene):
            childs = [i for i in root.items() if i.parentItem() is None]
            rootItem = []
        else:
            try:
                childs = root.childItems()
            except:
                childs = root.items()

            rootItem = [
             root]
        childs.sort(key=(lambda a: a.zValue()))
        while len(childs) > 0:
            ch = childs.pop(0)
            tree = self.getPaintItems(ch)
            if not int(ch.flags() & ch.ItemStacksBehindParent) > 0:
                if not ch.zValue() < 0 or int(ch.flags() & ch.ItemNegativeZStacksBehindParent) > 0:
                    preItems.extend(tree)
            else:
                postItems.extend(tree)

        return preItems + rootItem + postItems

    def getTargetRect(self):
        return self.item.rect()

    def getSourceRect(self):
        return self.item.rect()