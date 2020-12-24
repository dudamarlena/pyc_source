# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/ProgressDialog.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 3751 bytes
from ..Qt import QtGui, QtCore
__all__ = [
 'ProgressDialog']

class ProgressDialog(QtGui.QProgressDialog):
    """ProgressDialog"""

    def __init__(self, labelText, minimum=0, maximum=100, cancelText='Cancel', parent=None, wait=250, busyCursor=False, disable=False):
        """
        ============== ================================================================
        **Arguments:**
        labelText      (required)
        cancelText     Text to display on cancel button, or None to disable it.
        minimum
        maximum
        parent       
        wait           Length of time (im ms) to wait before displaying dialog
        busyCursor     If True, show busy cursor until dialog finishes
        disable        If True, the progress dialog will not be displayed
                       and calls to wasCanceled() will always return False.
                       If ProgressDialog is entered from a non-gui thread, it will
                       always be disabled.
        ============== ================================================================
        """
        isGuiThread = QtCore.QThread.currentThread() == QtCore.QCoreApplication.instance().thread()
        self.disabled = disable or 
        if self.disabled:
            return
        noCancel = False
        if cancelText is None:
            cancelText = ''
            noCancel = True
        self.busyCursor = busyCursor
        QtGui.QProgressDialog.__init__(self, labelText, cancelText, minimum, maximum, parent)
        self.setMinimumDuration(wait)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setValue(self.minimum())
        if noCancel:
            self.setCancelButton(None)

    def __enter__(self):
        if self.disabled:
            return self
        if self.busyCursor:
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        return self

    def __exit__(self, exType, exValue, exTrace):
        if self.disabled:
            return
        if self.busyCursor:
            QtGui.QApplication.restoreOverrideCursor()
        self.setValue(self.maximum())

    def __iadd__(self, val):
        """Use inplace-addition operator for easy incrementing."""
        if self.disabled:
            return self
        self.setValue(self.value() + val)
        return self

    def setValue(self, val):
        if self.disabled:
            return
        QtGui.QProgressDialog.setValue(self, val)

    def setLabelText(self, val):
        if self.disabled:
            return
        QtGui.QProgressDialog.setLabelText(self, val)

    def setMaximum(self, val):
        if self.disabled:
            return
        QtGui.QProgressDialog.setMaximum(self, val)

    def setMinimum(self, val):
        if self.disabled:
            return
        QtGui.QProgressDialog.setMinimum(self, val)

    def wasCanceled(self):
        if self.disabled:
            return False
        return QtGui.QProgressDialog.wasCanceled(self)

    def maximum(self):
        if self.disabled:
            return 0
        return QtGui.QProgressDialog.maximum(self)

    def minimum(self):
        if self.disabled:
            return 0
        return QtGui.QProgressDialog.minimum(self)