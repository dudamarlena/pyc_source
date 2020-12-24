# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/canvas/CanvasItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 19268 bytes
from ..Qt import QtGui, QtCore, QtSvg, USE_PYSIDE
import graphicsItems.ROI as ROI
from .. import SRTTransform, ItemGroup
if USE_PYSIDE:
    from . import TransformGuiTemplate_pyside as TransformGuiTemplate
else:
    from . import TransformGuiTemplate_pyqt as TransformGuiTemplate
from .. import debug

class SelectBox(ROI):

    def __init__(self, scalable=False, rotatable=True):
        ROI.__init__(self, [0, 0], [1, 1], invertible=True)
        center = [0.5, 0.5]
        if scalable:
            self.addScaleHandle([1, 1], center, lockAspect=True)
            self.addScaleHandle([0, 0], center, lockAspect=True)
        if rotatable:
            self.addRotateHandle([0, 1], center)
            self.addRotateHandle([1, 0], center)


class CanvasItem(QtCore.QObject):
    sigResetUserTransform = QtCore.Signal(object)
    sigTransformChangeFinished = QtCore.Signal(object)
    sigTransformChanged = QtCore.Signal(object)
    sigVisibilityChanged = QtCore.Signal(object)
    transformCopyBuffer = None

    def __init__(self, item, **opts):
        defOpts = {'name':None, 
         'z':None,  'movable':True,  'scalable':False,  'rotatable':True,  'visible':True,  'parent':None}
        defOpts.update(opts)
        self.opts = defOpts
        self.selectedAlone = False
        QtCore.QObject.__init__(self)
        self.canvas = None
        self._graphicsItem = item
        parent = self.opts['parent']
        if parent is not None:
            self._graphicsItem.setParentItem(parent.graphicsItem())
            self._parentItem = parent
        else:
            self._parentItem = None
        z = self.opts['z']
        if z is not None:
            item.setZValue(z)
        self.ctrl = QtGui.QWidget()
        self.layout = QtGui.QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.ctrl.setLayout(self.layout)
        self.alphaLabel = QtGui.QLabel('Alpha')
        self.alphaSlider = QtGui.QSlider()
        self.alphaSlider.setMaximum(1023)
        self.alphaSlider.setOrientation(QtCore.Qt.Horizontal)
        self.alphaSlider.setValue(1023)
        self.layout.addWidget(self.alphaLabel, 0, 0)
        self.layout.addWidget(self.alphaSlider, 0, 1)
        self.resetTransformBtn = QtGui.QPushButton('Reset Transform')
        self.copyBtn = QtGui.QPushButton('Copy')
        self.pasteBtn = QtGui.QPushButton('Paste')
        self.transformWidget = QtGui.QWidget()
        self.transformGui = TransformGuiTemplate.Ui_Form()
        self.transformGui.setupUi(self.transformWidget)
        self.layout.addWidget(self.transformWidget, 3, 0, 1, 2)
        self.transformGui.mirrorImageBtn.clicked.connect(self.mirrorY)
        self.transformGui.reflectImageBtn.clicked.connect(self.mirrorXY)
        self.layout.addWidget(self.resetTransformBtn, 1, 0, 1, 2)
        self.layout.addWidget(self.copyBtn, 2, 0, 1, 1)
        self.layout.addWidget(self.pasteBtn, 2, 1, 1, 1)
        self.alphaSlider.valueChanged.connect(self.alphaChanged)
        self.alphaSlider.sliderPressed.connect(self.alphaPressed)
        self.alphaSlider.sliderReleased.connect(self.alphaReleased)
        self.resetTransformBtn.clicked.connect(self.resetTransformClicked)
        self.copyBtn.clicked.connect(self.copyClicked)
        self.pasteBtn.clicked.connect(self.pasteClicked)
        self.setMovable(self.opts['movable'])
        if 'transform' in self.opts:
            self.baseTransform = self.opts['transform']
        else:
            self.baseTransform = SRTTransform()
            if 'pos' in self.opts:
                if self.opts['pos'] is not None:
                    self.baseTransform.translate(self.opts['pos'])
            if 'angle' in self.opts:
                if self.opts['angle'] is not None:
                    self.baseTransform.rotate(self.opts['angle'])
        if 'scale' in self.opts:
            if self.opts['scale'] is not None:
                self.baseTransform.scale(self.opts['scale'])
        tr = self.baseTransform.saveState()
        if 'scalable' not in opts:
            if tr['scale'] == (1, 1):
                self.opts['scalable'] = True
        self.selectBox = SelectBox(scalable=(self.opts['scalable']), rotatable=(self.opts['rotatable']))
        self.selectBox.hide()
        self.selectBox.setZValue(1000000.0)
        self.selectBox.sigRegionChanged.connect(self.selectBoxChanged)
        self.selectBox.sigRegionChangeFinished.connect(self.selectBoxChangeFinished)
        self.itemRotation = QtGui.QGraphicsRotation()
        self.itemScale = QtGui.QGraphicsScale()
        self._graphicsItem.setTransformations([self.itemRotation, self.itemScale])
        self.tempTransform = SRTTransform()
        self.userTransform = SRTTransform()
        self.resetUserTransform()

    def setMovable(self, m):
        self.opts['movable'] = m
        if m:
            self.resetTransformBtn.show()
            self.copyBtn.show()
            self.pasteBtn.show()
        else:
            self.resetTransformBtn.hide()
            self.copyBtn.hide()
            self.pasteBtn.hide()

    def setCanvas(self, canvas):
        if canvas is self.canvas:
            return
        if canvas is None:
            self.canvas.removeFromScene(self._graphicsItem)
            self.canvas.removeFromScene(self.selectBox)
        else:
            canvas.addToScene(self._graphicsItem)
            canvas.addToScene(self.selectBox)
        self.canvas = canvas

    def graphicsItem(self):
        """Return the graphicsItem for this canvasItem."""
        return self._graphicsItem

    def parentItem(self):
        return self._parentItem

    def setParentItem(self, parent):
        self._parentItem = parent
        if parent is not None:
            if isinstance(parent, CanvasItem):
                parent = parent.graphicsItem()
        self.graphicsItem().setParentItem(parent)

    def copyClicked(self):
        CanvasItem.transformCopyBuffer = self.saveTransform()

    def pasteClicked(self):
        t = CanvasItem.transformCopyBuffer
        if t is None:
            return
        self.restoreTransform(t)

    def mirrorY(self):
        if not self.isMovable():
            return
        inv = SRTTransform()
        inv.scale(-1, 1)
        self.userTransform = self.userTransform * inv
        self.updateTransform()
        self.selectBoxFromUser()
        self.sigTransformChangeFinished.emit(self)

    def mirrorXY(self):
        if not self.isMovable():
            return
        self.rotate(180.0)

    def hasUserTransform(self):
        return not self.userTransform.isIdentity()

    def ctrlWidget(self):
        return self.ctrl

    def alphaChanged(self, val):
        alpha = val / 1023.0
        self._graphicsItem.setOpacity(alpha)

    def isMovable(self):
        return self.opts['movable']

    def selectBoxMoved(self):
        """The selection box has moved; get its transformation information and pass to the graphics item"""
        self.userTransform = self.selectBox.getGlobalTransform(relativeTo=(self.selectBoxBase))
        self.updateTransform()

    def scale(self, x, y):
        self.userTransform.scale(x, y)
        self.selectBoxFromUser()
        self.updateTransform()

    def rotate(self, ang):
        self.userTransform.rotate(ang)
        self.selectBoxFromUser()
        self.updateTransform()

    def translate(self, x, y):
        self.userTransform.translate(x, y)
        self.selectBoxFromUser()
        self.updateTransform()

    def setTranslate(self, x, y):
        self.userTransform.setTranslate(x, y)
        self.selectBoxFromUser()
        self.updateTransform()

    def setRotate(self, angle):
        self.userTransform.setRotate(angle)
        self.selectBoxFromUser()
        self.updateTransform()

    def setScale(self, x, y):
        self.userTransform.setScale(x, y)
        self.selectBoxFromUser()
        self.updateTransform()

    def setTemporaryTransform(self, transform):
        self.tempTransform = transform
        self.updateTransform()

    def applyTemporaryTransform(self):
        """Collapses tempTransform into UserTransform, resets tempTransform"""
        self.userTransform = self.userTransform * self.tempTransform
        self.resetTemporaryTransform()
        self.selectBoxFromUser()

    def resetTemporaryTransform(self):
        self.tempTransform = SRTTransform()
        self.updateTransform()

    def transform(self):
        return self._graphicsItem.transform()

    def updateTransform(self):
        """Regenerate the item position from the base, user, and temp transforms"""
        transform = self.baseTransform * self.userTransform * self.tempTransform
        s = transform.saveState()
        (self._graphicsItem.setPos)(*s['pos'])
        self.itemRotation.setAngle(s['angle'])
        self.itemScale.setXScale(s['scale'][0])
        self.itemScale.setYScale(s['scale'][1])
        self.displayTransform(transform)
        return s

    def displayTransform(self, transform):
        """Updates transform numbers in the ctrl widget."""
        tr = transform.saveState()
        self.transformGui.translateLabel.setText('Translate: (%f, %f)' % (tr['pos'][0], tr['pos'][1]))
        self.transformGui.rotateLabel.setText('Rotate: %f degrees' % tr['angle'])
        self.transformGui.scaleLabel.setText('Scale: (%f, %f)' % (tr['scale'][0], tr['scale'][1]))

    def resetUserTransform(self):
        self.userTransform.reset()
        self.updateTransform()
        self.selectBox.blockSignals(True)
        self.selectBoxToItem()
        self.selectBox.blockSignals(False)
        self.sigTransformChanged.emit(self)
        self.sigTransformChangeFinished.emit(self)

    def resetTransformClicked(self):
        self.resetUserTransform()
        self.sigResetUserTransform.emit(self)

    def restoreTransform(self, tr):
        try:
            self.userTransform = SRTTransform(tr)
            self.updateTransform()
            self.selectBoxFromUser()
            self.sigTransformChanged.emit(self)
            self.sigTransformChangeFinished.emit(self)
        except:
            self.userTransform = SRTTransform()
            debug.printExc('Failed to load transform:')

    def saveTransform(self):
        """Return a dict containing the current user transform"""
        return self.userTransform.saveState()

    def selectBoxFromUser(self):
        """Move the selection box to match the current userTransform"""
        self.selectBox.blockSignals(True)
        self.selectBox.setState(self.selectBoxBase)
        self.selectBox.applyGlobalTransform(self.userTransform)
        self.selectBox.blockSignals(False)

    def selectBoxToItem(self):
        """Move/scale the selection box so it fits the item's bounding rect. (assumes item is not rotated)"""
        self.itemRect = self._graphicsItem.boundingRect()
        rect = self._graphicsItem.mapRectToParent(self.itemRect)
        self.selectBox.blockSignals(True)
        self.selectBox.setPos([rect.x(), rect.y()])
        self.selectBox.setSize(rect.size())
        self.selectBox.setAngle(0)
        self.selectBoxBase = self.selectBox.getState().copy()
        self.selectBox.blockSignals(False)

    def zValue(self):
        return self.opts['z']

    def setZValue(self, z):
        self.opts['z'] = z
        if z is not None:
            self._graphicsItem.setZValue(z)

    def selectionChanged(self, sel, multi):
        """
        Inform the item that its selection state has changed. 
        ============== =========================================================
        **Arguments:**
        sel            (bool) whether the item is currently selected
        multi          (bool) whether there are multiple items currently 
                       selected
        ============== =========================================================
        """
        self.selectedAlone = sel and not multi
        self.showSelectBox()
        if self.selectedAlone:
            self.ctrlWidget().show()
        else:
            self.ctrlWidget().hide()

    def showSelectBox(self):
        """Display the selection box around this item if it is selected and movable"""
        if self.selectedAlone and self.isMovable() and self.isVisible():
            self.selectBox.show()
        else:
            self.selectBox.hide()

    def hideSelectBox(self):
        self.selectBox.hide()

    def selectBoxChanged(self):
        self.selectBoxMoved()
        self.sigTransformChanged.emit(self)

    def selectBoxChangeFinished(self):
        self.sigTransformChangeFinished.emit(self)

    def alphaPressed(self):
        """Hide selection box while slider is moving"""
        self.hideSelectBox()

    def alphaReleased(self):
        self.showSelectBox()

    def show(self):
        if self.opts['visible']:
            return
        self.opts['visible'] = True
        self._graphicsItem.show()
        self.showSelectBox()
        self.sigVisibilityChanged.emit(self)

    def hide(self):
        if not self.opts['visible']:
            return
        self.opts['visible'] = False
        self._graphicsItem.hide()
        self.hideSelectBox()
        self.sigVisibilityChanged.emit(self)

    def setVisible(self, vis):
        if vis:
            self.show()
        else:
            self.hide()

    def isVisible(self):
        return self.opts['visible']


class GroupCanvasItem(CanvasItem):
    """GroupCanvasItem"""

    def __init__(self, **opts):
        defOpts = {'movable':False, 
         'scalable':False}
        defOpts.update(opts)
        item = ItemGroup()
        (CanvasItem.__init__)(self, item, **defOpts)