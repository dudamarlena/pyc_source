# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/panel/qrawdatachooser.py
# Compiled at: 2019-08-19 15:09:30
"""
RawDataChooser.py:  widget for importing RawData (from file or from a function)
"""
__all__ = [
 'QRawDataWidget']
import numpy
from taurus.external.qt import Qt
from taurus.core.util.safeeval import SafeEvaluator
from taurus.qt.qtgui.util.ui import UILoadable

@UILoadable
class QRawDataWidget(Qt.QWidget):
    ReadFromFiles = Qt.pyqtSignal(int, int)
    AddCurve = Qt.pyqtSignal(dict)

    def __init__(self, parent=None):
        super(QRawDataWidget, self).__init__(parent)
        self.loadUi()
        self.openFilesBT.clicked.connect(self.onOpenFilesButtonClicked)
        self.addCurveBT.clicked.connect(self.onAddCurveButtonClicked)
        self.xFromLE.setValidator(Qt.QDoubleValidator(self))
        self.xToLE.setValidator(Qt.QDoubleValidator(self))
        self.xStepLE.setValidator(Qt.QDoubleValidator(self))

    def onOpenFilesButtonClicked(self):
        """ Emit a ReadFromFiles signal with the selected xcol and skiprows as parameters"""
        xcol = self.xcolSB.value()
        if xcol == self.xcolSB.minimum():
            xcol = None
        skiprows = self.headerSB.value()
        self.ReadFromFiles.emit(xcol, skiprows)
        return

    def onAddCurveButtonClicked(self):
        """ Emit a AddCurve signal with a rawdata dictionary as a parameter.
        The rawdata dictionary is prepared from the from the GUI's selection."""
        rawdata = {}
        if self.xRangeRB.isChecked():
            rawdata['x'] = numpy.arange(float(self.xFromLE.text()), float(self.xToLE.text()), float(self.xStepLE.text()))
        else:
            sev = SafeEvaluator()
            try:
                rawdata['x'] = sev.eval(str(self.xValuesLE.text()))
            except:
                Qt.QMessageBox.warning(self, 'Invalid x valuesCannot interpret the x values.\n Use Python expressions like "[1, 3 , 67]" or "arange(100)")')
                return

        rawdata['f(x)'] = str(self.f_xLE.text())
        self.AddCurve.emit(rawdata)


if __name__ == '__main__':
    import sys
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(sys.argv, cmd_line_parser=None)
    form = QRawDataWidget()
    form.show()
    sys.exit(app.exec_())