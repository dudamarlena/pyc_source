# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/garrigaf/Documents/git/darfix/build/lib/darfix/gui/blindSourceSeparationWidget.py
# Compiled at: 2020-03-03 09:45:08
# Size of source mod 2**32: 7307 bytes
__authors__ = [
 'J. Garriga']
__license__ = 'MIT'
__date__ = '07/02/2020'
import numpy
from silx.gui import qt
from darfix.core.blindSourceSeparation import Method, BSS
from .operationThread import OperationThread
from .displayComponentsWidget import DisplayComponentsWidget

class BSSWidget(qt.QMainWindow):
    __doc__ = '\n    Widget to apply blind source separation.\n    '

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)
        top_widget = qt.QWidget(self)
        methodLabel = qt.QLabel('Method: ')
        self.methodCB = qt.QComboBox()
        for method in Method.values():
            self.methodCB.addItem(method)

        nComponentsLabel = qt.QLabel('Num comp:')
        self.nComponentsLE = qt.QLineEdit('1')
        self.nComponentsLE.setValidator(qt.QIntValidator())
        self.computeButton = qt.QPushButton('Compute')
        maxNComponentsLabel = qt.QLabel('Max number of components:')
        self.maxNumComp = qt.QLineEdit('')
        self.maxNumComp.setToolTip('For a specific number of components enter an integer, for a\npercentage enter a float between 0 (included) and 1 (not included).\nFloat 0.5 will take as max number the 50% of the images.\nEmpty text computes all components.')
        self.maxNumComp.setValidator(qt.QDoubleValidator())
        self.detectButton = qt.QPushButton('Detect number of components')
        self.computeButton.setEnabled(False)
        self.detectButton.setEnabled(False)
        layout = qt.QGridLayout()
        layout.addWidget(methodLabel, 0, 0, 1, 1)
        layout.addWidget(self.methodCB, 0, 1, 1, 1)
        layout.addWidget(nComponentsLabel, 0, 2, 1, 1)
        layout.addWidget(self.nComponentsLE, 0, 3, 1, 1)
        layout.addWidget(self.computeButton, 0, 4, 1, 1)
        layout.addWidget(maxNComponentsLabel, 1, 2, 1, 1)
        layout.addWidget(self.maxNumComp, 1, 3, 1, 1)
        layout.addWidget(self.detectButton, 1, 4, 1, 1)
        top_widget.setLayout(layout)
        self.splitter = qt.QSplitter(qt.Qt.Vertical)
        self.splitter.addWidget(top_widget)
        self.setCentralWidget(self.splitter)
        self._displayComponentsWidget = DisplayComponentsWidget()
        self.splitter.addWidget(self._displayComponentsWidget)
        self._displayComponentsWidget.hide()
        self.computeButton.clicked.connect(self._computeBSS)
        self.detectButton.clicked.connect(self._detectComp)

    def hideButton(self):
        self._computeB.hide()

    def showButton(self):
        self._computeB.show()

    def setDataset(self, dataset):
        """
        Dataset setter. Saves the dataset and updates the stack with the dataset
        data

        :param Dataset dataset: dataset
        """
        self.dataset = dataset
        self.BSS = BSS(self.dataset.hi_data)
        self.computeButton.setEnabled(True)
        self.detectButton.setEnabled(True)

    def _computeBSS(self):
        """
        Computes blind source separation with the chosen method.
        """
        self.computeButton.setEnabled(False)
        self.nComponentsLE.setEnabled(False)
        method = Method(self.methodCB.currentText())
        n_comp = int(self.nComponentsLE.text())
        if method == Method.PCA:
            self._thread = OperationThread(self.BSS.PCA)
        else:
            if method == Method.NNICA:
                self._thread = OperationThread(self.BSS.non_negative_ICA)
            else:
                if method == Method.NMF:
                    self._thread = OperationThread(self.BSS.NMF)
                else:
                    if method == Method.NNICA_NMF:
                        self._thread = OperationThread(self.BSS.NNICA_NMF)
                    else:
                        raise ValueError('BSS method not managed')
        self._thread.setArgs(n_comp)
        self._thread.finished.connect(self._displayComponents)
        self._thread.start()

    def _displayComponents(self):
        self._thread.finished.disconnect(self._displayComponents)
        comp, self.W = self._thread.data
        n_comp = int(self.nComponentsLE.text())
        if comp.shape[0] < n_comp:
            n_comp = comp.shape[0]
            msg = qt.QMessageBox()
            msg.setIcon(qt.QMessageBox.Information)
            msg.setText('Found only {0} components'.format(n_comp))
            msg.setStandardButtons(qt.QMessageBox.Ok)
            msg.exec_()
        self.comp = comp.reshape(n_comp, self.dataset.data.shape[1], self.dataset.data.shape[2])
        self._displayComponentsWidget.show()
        self.computeButton.setEnabled(True)
        self.nComponentsLE.setEnabled(True)
        if numpy.any(self.dataset.li_data):
            W = numpy.zeros((self.dataset.nframes, n_comp))
            W[self.dataset.threshold] = self.W
            self.W = W
        self._displayComponentsWidget.setComponents(self.comp, self.W, self.dataset.get_dimensions_values())

    def _detectComp(self):
        txt = self.maxNumComp.text()
        if txt != '':
            maxNumComp = float(self.maxNumComp.text())
        else:
            maxNumComp = None
        self.detectButton.setEnabled(False)
        self._thread = OperationThread(self.BSS.PCA)
        self._thread.setArgs(None, maxNumComp)
        self._thread.finished.connect(self._setNumComp)
        self._thread.start()

    def _setNumComp(self):
        self._thread.finished.disconnect(self._setNumComp)
        mean, vecs, vals = self._thread.data
        vals /= numpy.sum(vals)
        components = len(vals[(vals > 0.01)])
        self.detectButton.setEnabled(True)
        self.nComponentsLE.setText(str(components))