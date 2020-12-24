# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/ftserie/h5editor/h5filedialog.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 4000 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '23/02/2017'
from silx.gui import qt
import os

class H5FileDialog(qt.QMessageBox):
    __doc__ = 'Class defining the dialog to ask the user an h5 file to be used\n    '
    defaultH5File = os.path.expanduser('~') + '/.octave/mytomodefaults.h5'

    def __init__(self, parent=None):
        qt.QMessageBox.__init__(self, parent)
        self.setWindowTitle('.h5 file for reconstruction')
        self.h5File = None
        text = 'No .h5 found, if you want to process a reconstruction '
        text += 'you must give one.'
        self.layout().addWidget(qt.QLabel(text), 1, 0)
        if H5FileDialog.hasDefaultH5File():
            buttonText = 'Take the default octave file at ' + self.defaultH5File
            defaultOctaveFileButton = qt.QPushButton(buttonText)
            defaultOctaveFileButton.setAutoDefault(True)
            defaultOctaveFileButton.clicked.connect(self._H5FileDialog__selectDefaultH5File)
            self.layout().addWidget(defaultOctaveFileButton, 1, 0)
        selectFileButtonButton = qt.QPushButton('Select a file')
        self.layout().addWidget(selectFileButtonButton, 2, 0)
        selectFileButtonButton.setAutoDefault(True)
        self.cancelButton = self.addButton(qt.QMessageBox.Cancel)
        self.layout().removeWidget(self.cancelButton)
        self.layout().addWidget(self.cancelButton, 3, 0)
        selectFileButtonButton.clicked.connect(self._H5FileDialog__selectFileFromDlg)

    def __selectDefaultH5File(self):
        """
        Set the default h5 file as the selected one
        """
        self.h5File = self.defaultH5File
        self.accept()

    def __selectFileFromDlg(self):
        """
        Launch a QFileDialog to ask the user the path to the h5 file
        """
        self.h5File = H5FileDialog.askForH5File()
        self.accept()

    def exec_(self):
        if H5FileDialog.hasDefaultH5File():
            qt.QMessageBox.exec_(self)
        else:
            H5FileDialog.askForH5File()

    @staticmethod
    def hasDefaultH5File():
        return os.path.isfile(H5FileDialog.defaultH5File)

    @staticmethod
    def askForH5File(save):
        dialog = qt.QFileDialog()
        title = 'Select an h5 file to %s the reconstruction parameters.' % ('save' if save is True else 'load')
        dialog.setWindowTitle(title)
        dialog.setModal(1)
        dialog.setNameFilters(['HDF5 file *.h5 *.hdf5'])
        if not dialog.exec_():
            return
        qapp = qt.QApplication.instance()
        qapp.processEvents()
        return dialog.selectedFiles()[0]