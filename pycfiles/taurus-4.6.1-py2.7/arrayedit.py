# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/qwt5/arrayedit.py
# Compiled at: 2019-08-19 15:09:30
"""
arrayedit.py: Widget for editing a spectrum/array via control points
"""
from __future__ import absolute_import
from builtins import range
import numpy
from taurus.external.qt import Qt, Qwt5
from taurus.qt.qtgui.util.ui import UILoadable
from .curvesAppearanceChooserDlg import CurveAppearanceProperties

@UILoadable
class ControllerBox(Qt.QWidget):
    selected = Qt.pyqtSignal(int)

    def __init__(self, parent=None, x=0, y=0, corr=0):
        Qt.QWidget.__init__(self, parent)
        self.loadUi()
        self._x = x
        self.setY(y)
        self.box.setTitle('x=%6g' % self._x)
        self.corrSB.setValue(corr)
        self.ctrlObj = self.corrSB.ctrlObj = self.lCopyBT.ctrlObj = self.rCopyBT.ctrlObj = self.lScaleBT.ctrlObj = self.rScaleBT.ctrlObj = self
        self.corrSB.focusInEvent = self.corrSB_focusInEvent
        self.box.mousePressEvent = self.mousePressEvent

    def mousePressEvent(self, event):
        self.selected.emit(self._x)

    def corrSB_focusInEvent(self, event):
        self.selected.emit(self._x)
        Qt.QDoubleSpinBox.focusInEvent(self.corrSB, event)

    def setY(self, y):
        self._y = y
        self.enableScale()

    def enableScale(self, *args):
        enable = self._y + self.corrSB.value() != 0
        self.lScaleBT.setEnabled(enable)
        self.rScaleBT.setEnabled(enable)


@UILoadable
class EditCPointsDialog(Qt.QDialog):

    def __init__(self, parent=None, x=0):
        Qt.QDialog.__init__(self, parent)
        self.loadUi()


@UILoadable
class AddCPointsDialog(Qt.QDialog):

    def __init__(self, parent=None, x=0):
        Qt.QDialog.__init__(self, parent)
        self.loadUi()


@UILoadable
class ArrayEditor(Qt.QWidget):

    def __init__(self, parent=None):
        Qt.QWidget.__init__(self, parent)
        self.loadUi()
        self._controllers = []
        self.ctrlLayout = Qt.QHBoxLayout(self.controllersContainer)
        self.ctrlLayout.setContentsMargins(5, 0, 5, 0)
        self.ctrlLayout.setSpacing(1)
        self.scrollArea = Qt.QScrollArea(self)
        self.scrollArea.setWidget(self.controllersContainer)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.cpointsGroupBox.layout().insertWidget(0, self.scrollArea)
        cpoints = 2
        self.x = numpy.arange(256, dtype='double')
        self.y = numpy.zeros(256, dtype='double')
        self.xp = numpy.linspace(self.x[0], self.x[(-1)], cpoints)
        self.corrp = numpy.zeros(cpoints)
        self.yp = numpy.interp(self.xp, self.x, self.y)
        self.corr = numpy.zeros(self.x.size)
        self.markerPos = self.xp[0]
        self.marker1 = Qwt5.QwtPlotMarker()
        self.marker1.setSymbol(Qwt5.QwtSymbol(Qwt5.QwtSymbol.Rect, Qt.QBrush(Qt.Qt.NoBrush), Qt.QPen(Qt.Qt.green), Qt.QSize(8, 8)))
        self.marker1.attach(self.plot1)
        self.marker2 = Qwt5.QwtPlotMarker()
        self.marker2.setSymbol(Qwt5.QwtSymbol(Qwt5.QwtSymbol.Rect, Qt.QBrush(Qt.Qt.NoBrush), Qt.QPen(Qt.Qt.green), Qt.QSize(8, 8)))
        self.marker2.attach(self.plot2)
        self._cpointMovingIndex = None
        self._cpointsPicker1 = Qwt5.QwtPicker(self.plot1.canvas())
        self._cpointsPicker1.setSelectionFlags(Qwt5.QwtPicker.PointSelection)
        self._cpointsPicker2 = Qwt5.QwtPicker(self.plot2.canvas())
        self._cpointsPicker2.setSelectionFlags(Qwt5.QwtPicker.PointSelection)
        self._cpointsPicker1.widgetMousePressEvent = self.plot1MousePressEvent
        self._cpointsPicker1.widgetMouseReleaseEvent = self.plot1MouseReleaseEvent
        self._cpointsPicker2.widgetMousePressEvent = self.plot2MousePressEvent
        self._cpointsPicker2.widgetMouseReleaseEvent = self.plot2MouseReleaseEvent
        self._cpointsPicker1.widgetMouseDoubleClickEvent = self.plot1MouseDoubleClickEvent
        self._cpointsPicker2.widgetMouseDoubleClickEvent = self.plot2MouseDoubleClickEvent
        self._populatePlots()
        self.resetCorrection()
        self._selectedController = self._controllers[0]
        self._addCPointsDialog = AddCPointsDialog(self)
        self.addCPointsBT.clicked.connect(self._addCPointsDialog.show)
        self._addCPointsDialog.editBT.clicked.connect(self.showEditCPointsDialog)
        self._addCPointsDialog.cleanBT.clicked.connect(self.resetCorrection)
        self._addCPointsDialog.addSingleCPointBT.clicked.connect(self.onAddSingleCPointBT)
        self._addCPointsDialog.addRegEspCPointsBT.clicked.connect(self.onAddRegEspCPointsBT)
        return

    def plot1MousePressEvent(self, event):
        self.plotMousePressEvent(event, self.plot1)

    def plot2MousePressEvent(self, event):
        self.plotMousePressEvent(event, self.plot2)

    def plotMousePressEvent(self, event, taurusplot):
        picked, pickedCurveName, pickedIndex = taurusplot.pickDataPoint(event.pos(), scope=20, showMarker=False, targetCurveNames=['Control Points'])
        if picked is not None:
            self.changeCPointSelection(picked.x())
            self.makeControllerVisible(self._controllers[pickedIndex])
            self._cpointMovingIndex = pickedIndex
            self._movingStartYPos = event.y()
            taurusplot.canvas().setCursor(Qt.Qt.SizeVerCursor)
        return

    def plot1MouseReleaseEvent(self, event):
        self.plotMouseReleaseEvent(event, self.plot1)

    def plot2MouseReleaseEvent(self, event):
        self.plotMouseReleaseEvent(event, self.plot2)

    def plotMouseReleaseEvent(self, event, taurusplot):
        if self._cpointMovingIndex is None:
            return
        else:
            validMotion = self._movingStartYPos != event.pos().y() and taurusplot.canvas().rect().contains(event.pos())
            if validMotion:
                newCorr = taurusplot.invTransform(taurusplot.getCurve('Control Points').yAxis(), event.y())
                if taurusplot is self.plot1:
                    newCorr -= self.yp[self._cpointMovingIndex]
                self._controllers[self._cpointMovingIndex].corrSB.setValue(newCorr)
            self._cpointMovingIndex = None
            taurusplot.canvas().setCursor(Qt.Qt.CrossCursor)
            return

    def plot1MouseDoubleClickEvent(self, event):
        self.plotMouseDoubleClickEvent(event, self.plot1)

    def plot2MouseDoubleClickEvent(self, event):
        self.plotMouseDoubleClickEvent(event, self.plot2)

    def plotMouseDoubleClickEvent(self, event, taurusplot):
        picked, pickedCurveName, pickedIndex = taurusplot.pickDataPoint(event.pos(), scope=20, showMarker=False, targetCurveNames=['Control Points'])
        if picked is not None:
            return
        else:
            xp = taurusplot.invTransform(taurusplot.getCurve('Control Points').xAxis(), event.x())
            if xp < self.xp[0] or xp > self.xp[(-1)]:
                return
            if Qt.QMessageBox.question(self, 'Create Control Point?', 'Insert a new control point at x=%g?' % xp, 'Yes', 'No') == 0:
                self.insertController(xp)
                self.changeCPointSelection(xp)
                Qt.QTimer.singleShot(1, self.makeControllerVisible)
            return

    def makeControllerVisible(self, ctrl=None):
        if ctrl is None:
            ctrl = self._selectedController
        self.scrollArea.ensureWidgetVisible(ctrl)
        return

    def connectToController(self, ctrl):
        ctrl.selected.connect(self.changeCPointSelection)
        ctrl.corrSB.valueChanged.connect(self.onCorrSBChanged)
        ctrl.lCopyBT.clicked.connect(self.onLCopy)
        ctrl.rCopyBT.clicked.connect(self.onRCopy)
        ctrl.lScaleBT.clicked.connect(self.onLScale)
        ctrl.rScaleBT.clicked.connect(self.onRScale)

    def onAddSingleCPointBT(self):
        x = self._addCPointsDialog.singleCPointXSB.value()
        self.insertController(x)

    def onAddRegEspCPointsBT(self):
        cpoints = self._addCPointsDialog.regEspCPointsSB.value()
        positions = numpy.linspace(self.x[0], self.x[(-1)], cpoints + 2)[1:-1]
        for xp in positions:
            self.insertController(xp)

    def showEditCPointsDialog(self):
        dialog = EditCPointsDialog(self)
        table = dialog.tableTW
        table.setRowCount(self.xp.size)
        for i, (xp, corrp) in enumerate(zip(self.xp, self.corrp)):
            table.setItem(i, 0, Qt.QTableWidgetItem(str(xp)))
            table.setItem(i, 1, Qt.QTableWidgetItem(str(corrp)))

        if dialog.exec_():
            for c in self._controllers:
                c.setParent(None)
                c.deleteLater()

            self._controllers = []
            new_xp = numpy.zeros(table.rowCount())
            new_corrp = numpy.zeros(table.rowCount())
            try:
                for i in range(table.rowCount()):
                    new_xp[i] = float(table.item(i, 0).text())
                    new_corrp[i] = float(table.item(i, 1).text())

                self.setCorrection(new_xp, new_corrp)
            except:
                Qt.QMessageBox.warning(self, 'Invalid data', 'Some values were not valid. Edition is ignored.')

        return

    def _getInsertionIndex(self, xp):
        i = 0
        while self.xp[i] < xp:
            i += 1

        return i

    def insertControllers(self, xplist):
        for xp in xplist:
            self.insertController(xp)

    def insertController(self, xp, index=None):
        if xp in self.xp:
            return
        else:
            if index is None:
                index = self._getInsertionIndex(xp)
            old_xp = self.xp
            self.xp = numpy.concatenate((self.xp[:index], (xp,), self.xp[index:]))
            self.yp = numpy.interp(self.xp, self.x, self.y)
            self.corrp = numpy.interp(self.xp, old_xp, self.corrp)
            ctrl = ControllerBox(parent=None, x=xp, y=self.yp[index], corr=self.corrp[index])
            self.ctrlLayout.insertWidget(index, ctrl)
            self._controllers.insert(index, ctrl)
            self.connectToController(ctrl)
            self.updatePlots()
            return index

    def delController(self, index):
        c = self._controllers.pop(index)
        c.setParent(None)
        c.deleteLater()
        self.xp = numpy.concatenate((self.xp[:index], self.xp[index + 1:]))
        self.yp = numpy.interp(self.xp, self.x, self.y)
        self.corrp = numpy.concatenate((
         self.corrp[:index], self.corrp[index + 1:]))
        return

    def _populatePlots(self):
        self._yAppearance = CurveAppearanceProperties(sStyle=Qwt5.QwtSymbol.NoSymbol, lStyle=Qt.Qt.SolidLine, lWidth=2, lColor='black', cStyle=Qwt5.QwtPlotCurve.Lines, yAxis=Qwt5.QwtPlot.yLeft)
        self._correctedAppearance = CurveAppearanceProperties(sStyle=Qwt5.QwtSymbol.NoSymbol, lStyle=Qt.Qt.DashLine, lWidth=1, lColor='blue', cStyle=Qwt5.QwtPlotCurve.Lines, yAxis=Qwt5.QwtPlot.yLeft)
        self._cpointsAppearance = CurveAppearanceProperties(sStyle=Qwt5.QwtSymbol.Rect, sSize=5, sColor='blue', sFill=True, lStyle=Qt.Qt.NoPen, yAxis=Qwt5.QwtPlot.yLeft)
        self._corrAppearance = CurveAppearanceProperties(sStyle=Qwt5.QwtSymbol.NoSymbol, lStyle=Qt.Qt.SolidLine, lWidth=1, lColor='blue', cStyle=Qwt5.QwtPlotCurve.Lines, yAxis=Qwt5.QwtPlot.yLeft)
        self.plot1.attachRawData({'x': self.x, 'y': self.y, 'title': 'Master'})
        self.plot1.setCurveAppearanceProperties({'Master': self._yAppearance})
        self.plot1.attachRawData({'x': self.xp, 'y': self.yp + self.corrp, 'title': 'Control Points'})
        self.plot1.setCurveAppearanceProperties({'Control Points': self._cpointsAppearance})
        self.plot1.attachRawData({'x': self.x, 'y': self.y + self.corr, 'title': 'Corrected'})
        self.plot1.setCurveAppearanceProperties({'Corrected': self._correctedAppearance})
        self.plot2.attachRawData({'x': self.x, 'y': self.corr, 'title': 'Correction'})
        self.plot2.setCurveAppearanceProperties({'Correction': self._corrAppearance})
        self.plot2.attachRawData({'x': self.xp, 'y': self.corrp, 'title': 'Control Points'})
        self.plot2.setCurveAppearanceProperties({'Control Points': self._cpointsAppearance})

    def updatePlots(self):
        self.plot1.getCurve('Control Points').setData(self.xp, self.yp + self.corrp)
        self.plot1.getCurve('Corrected').setData(self.x, self.y + self.corr)
        self.plot2.getCurve('Correction').setData(self.x, self.corr)
        self.plot2.getCurve('Control Points').setData(self.xp, self.corrp)
        index = self._getInsertionIndex(self.markerPos)
        self.marker1.setValue(self.xp[index], self.yp[index] + self.corrp[index])
        self.marker2.setValue(self.xp[index], self.corrp[index])
        self.plot1.replot()
        self.plot2.replot()

    def onLCopy(self, checked):
        sender = self.sender().ctrlObj
        index = self._getInsertionIndex(sender._x)
        v = sender.corrSB.value()
        for ctrl in self._controllers[:index]:
            ctrl.corrSB.setValue(v)

    def onRCopy(self, checked):
        sender = self.sender().ctrlObj
        index = self._getInsertionIndex(sender._x)
        v = sender.corrSB.value()
        for ctrl in self._controllers[index + 1:]:
            ctrl.corrSB.setValue(v)

    def onLScale(self, checked):
        sender = self.sender().ctrlObj
        index = self._getInsertionIndex(sender._x)
        if self.yp[index] == 0:
            Qt.QMessageBox.warning(self, 'Scaling Error', 'The master at this control point is zero-valued. This point cannot be used as reference for scaling')
            return
        v = sender.corrSB.value() / self.yp[index]
        for i in range(0, index):
            self._controllers[i].corrSB.setValue(v * self.yp[i])

    def onRScale(self, checked):
        sender = self.sender().ctrlObj
        index = self._getInsertionIndex(sender._x)
        if self.yp[index] == 0:
            Qt.QMessageBox.warning(self, 'Scaling Error', 'The master at this control point is zero-valued. This point cannot be used as reference for scaling')
            return
        v = sender.corrSB.value() / self.yp[index]
        for i in range(index + 1, self.xp.size):
            self._controllers[i].corrSB.setValue(v * self.yp[i])

    def changeCPointSelection(self, newpos):
        index = self._getInsertionIndex(newpos)
        old_index = self._getInsertionIndex(self.markerPos)
        self.markerPos = self.xp[index]
        self.marker1.setValue(self.xp[index], self.yp[index] + self.corrp[index])
        self.marker2.setValue(self.xp[index], self.corrp[index])
        self.plot1.replot()
        self.plot2.replot()
        self._controllers[old_index].corrSB.setStyleSheet('')
        self._controllers[index].corrSB.setStyleSheet('background:lightgreen')
        self._selectedController = self._controllers[index]

    def onCorrSBChanged(self, value=None):
        """recalculates the position and value of the control points (self.xp and self.corrp)
        as well as the correction curve (self.corr)"""
        ctrl = self.sender().ctrlObj
        self.corrp[self._getInsertionIndex(ctrl._x)] = value
        self.corr = numpy.interp(self.x, self.xp, self.corrp)
        self.updatePlots()

    def setMaster(self, x, y, keepCP=False, keepCorr=False):
        x, y = numpy.array(x), numpy.array(y)
        if x.shape != y.shape or x.size == 0 or y.size == 0:
            raise ValueError('The master curve is not valid')
        sortedindexes = numpy.argsort(x)
        self.x, self.y = x[sortedindexes], y[sortedindexes]
        self.plot1.getCurve('Master').setData(self.x, self.y)
        xp = None
        corrp = None
        if self.x[0] == self.xp[0] and self.x[(-1)] == self.x[(-1)]:
            if keepCP:
                xp = self.xp
            if keepCorr:
                corrp = self.corrp
        self.setCorrection(xp, corrp)
        self._addCPointsDialog.singleCPointXSB.setRange(self.x[0], self.x[(-1)])
        return

    def getMaster(self):
        """returns x,m where x and m are numpy arrays representing the
        abcissas and ordinates for the master, respectively"""
        return (
         self.x.copy(), self.y.copy())

    def resetMaster(self):
        x = numpy.arange(256, dtype='double')
        y = numpy.zeros(256, dtype='double')
        self.setMaster(x, y)

    def getCorrected(self):
        """returns x,c where x and c are numpy arrays representing the
        abcissas and ordinates for the corrected curve, respectively"""
        return (
         self.x.copy(), self.y + self.corr)

    def getCorrection(self):
        """returns xp,cp where xp and cp are numpy arrays representing the
        abcissas and ordinates for the correction points, respectively"""
        return (
         self.xp.copy(), self.corrp.copy())

    def setCorrection(self, xp=None, corrp=None):
        """sets control points at the points specified by xp and with the
        values specified by corrp. Example::

            setCorrection([1,2,8,9], [0,0,0,0])

        would set 4 control points with initial value 0 at x=1, 2, 8 and 9s
        """
        for c in self._controllers:
            c.setParent(None)
            c.deleteLater()

        self._controllers = []
        if xp is None:
            xp = numpy.array((self.x[0], self.x[(-1)]))
            corrp = numpy.zeros(2)
        if corrp is None:
            corrp = numpy.zeros(xp.size)
        if xp[0] > self.x[0]:
            xp = numpy.concatenate(((self.x[0],), xp))
            corrp = numpy.concatenate(((self.corrp[0],), corrp))
        if xp[(-1)] < self.x[(-1)]:
            xp = numpy.concatenate((xp, (self.x[(-1)],)))
            corrp = numpy.concatenate((corrp, (self.corrp[(-1)],)))
        self.xp = numpy.unique(xp)
        self.corrp = numpy.interp(self.xp, xp, corrp)
        self.yp = numpy.interp(self.xp, self.x, self.y)
        for i, (x, c) in enumerate(zip(xp, corrp)):
            ctrl = ControllerBox(parent=None, x=xp[i], y=self.yp[i])
            self.ctrlLayout.insertWidget(i, ctrl)
            self._controllers.insert(i, ctrl)
            self.connectToController(ctrl)

        self.corr = numpy.interp(self.x, self.xp, self.corrp)
        self.updatePlots()
        self.changeCPointSelection(self.xp[0])
        return

    def resetCorrection(self):
        self.setCorrection()


if __name__ == '__main__':
    import sys
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(sys.argv, cmd_line_parser=None)
    form = ArrayEditor()
    x = numpy.linspace(0.1, 0.9, 100)
    y = x ** 2 - 5 * x
    form.setMaster(x, y)
    form.show()
    status = app.exec_()
    sys.exit(status)