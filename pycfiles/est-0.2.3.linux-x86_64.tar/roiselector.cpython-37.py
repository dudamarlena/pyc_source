# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/gui/roiselector.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 6276 bytes
"""Tools to visualize spectra"""
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '04/07/2019'
from silx.gui import qt
from silx.gui.plot.items.roi import RectangleROI
from silx.gui.plot.tools.roi import RegionOfInterestManager
from silx.gui.plot.tools.roi import RegionOfInterestTableWidget
from est.gui.XasObjectViewer import MapViewer

class ROISelector(qt.QWidget):
    __doc__ = '\n    Used to defined a roi on a spectra map\n    '

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self._xas_object_map = MapViewer(keys=['mu'])
        self.layout().addWidget(self._xas_object_map)
        self._plot = self._xas_object_map.getPlot()
        self._roiManager = RegionOfInterestManager(self._plot)
        self._roiManager.setColor('red')
        self._roiManager.sigRoiAdded.connect(self.updateAddedRegionOfInterest)
        self._roi = RectangleROI()
        self._roi.setGeometry(origin=(0, 0), size=(2, 2))
        self._roi.setLabel('ROI')
        self._roiManager.addRoi(self._roi)
        self._ROISelector__roi_first_definition = True
        self._roiTable = RegionOfInterestTableWidget()
        self._roiTable.setRegionOfInterestManager(self._roiManager)
        widget = qt.QWidget()
        layout = qt.QVBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(self._roiTable)
        layout.addWidget(self._xas_object_map.keySelectionDocker)
        dock = qt.QDockWidget('Image ROI')
        dock.setWidget(widget)
        self._plot.addDockWidget(qt.Qt.RightDockWidgetArea, dock)
        self.setColormap = self._plot.setDefaultColormap

    def setXasObject(self, xas_obj):
        self._xas_object_map.setXasObject(xas_obj=xas_obj)
        if self._ROISelector__roi_first_definition is True:
            origin = (0, 0)
            size = (xas_obj.dim2, xas_obj.dim1)
            self.setROI(origin=origin, size=size)
            self._roi.setEditable(True)

    def getXasObject(self):
        return self._xas_object_map._xasObj

    def updateAddedRegionOfInterest(self, roi):
        """Called for each added region of interest: set the name"""
        if roi.getLabel() == '':
            roi.setLabel('ROI %d' % len(self._roiManager.getRois()))

    def setROI(self, origin, size):
        self._roi.setGeometry(origin=origin, size=size)

    def getROI(self):
        return self._roi


class ROISelectorDialog(qt.QDialog):
    __doc__ = 'Dialog embedding the SoiSelector'

    def __init__(self, parent=None):
        qt.QDialog.__init__(self, parent)
        self._mainWindow = ROISelector(parent=self)
        self.setWindowTitle('Roi selection')
        self.setWindowFlags(qt.Qt.Widget)
        types = qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.Cancel
        _buttons = qt.QDialogButtonBox(parent=self)
        _buttons.setStandardButtons(types)
        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self._mainWindow)
        self.layout().addWidget(_buttons)
        _buttons.accepted.connect(self.accept)
        _buttons.rejected.connect(self.reject)
        self.setXasObject = self._mainWindow.setXasObject
        self.getXasObject = self._mainWindow.getXasObject
        self.getROI = self._mainWindow.getROI
        self.setROI = self._mainWindow.setROI
        self.setColormap = self._mainWindow.setColormap


if __name__ == '__main__':
    from est.core.types import XASObject
    import numpy
    import est.core.utils as spectra_utils
    from est.core.process.roi import ROIProcess, _ROI
    from silx.gui.colors import Colormap
    energy, spectra = spectra_utils.create_dataset(shape=(256, 32, 64))
    xas_obj = XASObject(spectra=spectra, energy=energy, configuration=None)
    app = qt.QApplication([])

    class ROISelectorDialogTest(ROISelectorDialog):
        __doc__ = 'Infinite update the xas obj according to ROI'

        def accept(self):
            roi_process = ROIProcess()
            roi_ = _ROI.from_silx_def(self.getROI())
            roi_process.setProperties({'roi': roi_.to_dict()})
            update_xas_object = roi_process.process(self.getXasObject())
            self.setXasObject(update_xas_object)
            self.show()


    roiSelector = ROISelectorDialogTest()
    roiSelector.setColormap(Colormap(name='temperature', vmin=0, vmax=10))
    roiSelector.setXasObject(xas_obj=xas_obj)
    roiSelector.show()
    app.exec_()