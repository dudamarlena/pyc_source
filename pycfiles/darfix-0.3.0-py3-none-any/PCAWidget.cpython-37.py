# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/garrigaf/Documents/git/darfix/build/lib/darfix/gui/PCAWidget.py
# Compiled at: 2020-03-03 09:45:08
# Size of source mod 2**32: 3918 bytes
__authors__ = [
 'J. Garriga']
__license__ = 'MIT'
__date__ = '30/01/2020'
import numpy
from silx.gui import qt
from silx.gui.plot import Plot1D
from darfix.core.blindSourceSeparation import BSS
from .operationThread import OperationThread

class PCAWidget(qt.QMainWindow):
    __doc__ = '\n    Widget to apply PCA to a set of images and plot the eigenvalues found.\n    '
    sigComputed = qt.Signal()

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self._plot = Plot1D()
        self._plot.setDataMargins(0.05, 0.05, 0.05, 0.05)
        maxNComponentsLabel = qt.QLabel('Max number of components:')
        self.maxNumComp = qt.QLineEdit('')
        self.maxNumComp.setToolTip('Maximum number of components to compute')
        self.maxNumComp.setValidator(qt.QDoubleValidator())
        self.computeB = qt.QPushButton('Compute')
        widget = qt.QWidget(parent=self)
        layout = qt.QGridLayout()
        layout.addWidget(maxNComponentsLabel, 0, 0, 1, 1)
        layout.addWidget(self.maxNumComp, 0, 1, 1, 1)
        layout.addWidget(self.computeB, 0, 2, 1, 1)
        layout.addWidget(self._plot, 1, 0, 1, 3)
        widget.setLayout(layout)
        widget.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        self.setCentralWidget(widget)
        self._plot.hide()

    def _computePCA(self):
        self.computeB.setEnabled(False)
        try:
            txt = self.maxNumComp.text()
            if txt != '':
                maxNumComp = float(self.maxNumComp.text())
            else:
                maxNumComp = None
            self._thread = OperationThread(self.BSS.PCA)
            self._thread.setArgs(None, maxNumComp)
            self._thread.finished.connect(self._updateData)
            self._thread.start()
        except Exception as e:
            try:
                self.computeB.setEnabled(True)
                raise e
            finally:
                e = None
                del e

    def setDataset(self, dataset):
        """
        Dataset setter. Starts BSS class and initializes thread.

        :param Dataset dataset: dataset
        """
        self.dataset = dataset
        self.BSS = BSS(self.dataset.hi_data)
        self.computeB.pressed.connect(self._computePCA)

    def _updateData(self):
        """
        Plots the eigenvalues.
        """
        self._thread.finished.disconnect(self._updateData)
        self.computeB.setEnabled(True)
        mean, vecs, vals = self._thread.data
        vals = [item for sublist in vals for item in sublist]
        self._plot.show()
        self._plot.addCurve((numpy.arange(len(vals))), vals, symbol='.', linestyle=' ')
        self.sigComputed.emit()