# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/conditions/filter.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 5895 bytes
"""
This module is used to define the process of the reference creator.
This is related to the issue #184
"""
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '19/07/2018'
from silx.gui import qt
from tomwer.core.process.conditions import filters
from tomwer.gui import icons
from tomwer.gui.utils.sandboxes import RegularExpressionSandBox, RegularExpressionSandBoxDialog

class FileNameFilterWidget(filters.FileNameFilter, qt.QWidget):
    __doc__ = "\n    Simple widget allowing the user to define a pattern and emitting a signal\n    'sigValid' or 'sigUnvalid' if passing through the filter or not\n    "
    sigValid = qt.Signal(str)
    sigUnvalid = qt.Signal(str)

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        filters.FileNameFilter.__init__(self, None)
        self.setLayout(qt.QGridLayout())
        self._invertCB = qt.QCheckBox('Invert filter action', parent=self)
        self._invertCB.setToolTip('If not inverted and match the filter condition then let the scan pass through')
        self.layout().addWidget(self._invertCB, 0, 0, 1, 3)
        self.layout().addWidget(qt.QLabel('filter type:'), 1, 0)
        self._filterTypeCB = qt.QComboBox(parent=self)
        for filter_type in self.FILTER_TYPES:
            self._filterTypeCB.addItem(filter_type)

        self.layout().addWidget(self._filterTypeCB, 1, 1, 1, 2)
        self.layout().addWidget(qt.QLabel('pattern:', parent=self), 2, 0)
        self._patternLE = qt.QLineEdit(parent=self)
        self._patternLE.setToolTip(self.getPatternTooltip())
        self.layout().addWidget(self._patternLE, 2, 1)
        icon = icons.getQIcon('information')
        self._sandBoxPB = qt.QPushButton(icon=icon, parent=self)
        self._sandBoxPB.setToolTip(RegularExpressionSandBox.description())
        self._sandBoxPB.pressed.connect(self._showSandBox)
        self.layout().addWidget(self._sandBoxPB, 2, 2)
        self._sandBoxPB.setVisible(False)
        self.sandboxDialog = None
        if qt.BINDING in ('PyQt4', 'PySide'):
            self._filterTypeCB.currentIndexChanged[str].connect(self.setActiveFilter)
        else:
            self._filterTypeCB.currentTextChanged[str].connect(self.setActiveFilter)

    def isFiltered(self, value):
        if not type(value) is str:
            raise AssertionError
        else:
            _filtered = super().isFiltered(value)
            if self._invertCB.isChecked():
                _filtered = not _filtered
            if _filtered is True:
                self.sigUnvalid.emit(value)
            else:
                self.sigValid.emit(value)
        return _filtered

    def _showSandBox(self):
        self.getSandboxDialog().show()

    def getSandboxDialog(self):
        if self.sandboxDialog is None:
            self.sandboxDialog = RegularExpressionSandBoxDialog(parent=None, pattern=(self.getPattern()))
            self._patternLE.editingFinished.connect(self._updateSandBoxPattern)
            self.sandboxDialog.setModal(False)
        return self.sandboxDialog

    def getPatternTooltip(self):
        return 'define the pattern to accept file using the python `re` library.\nFor example if we two series of acquisition named serie_10_XXX\nand serie_100_YYY and we want to filter all the serie_10_XXX\nthen we can define the pattern "serie_100_" \nwhich will only let the serie_100_YYY go through.'

    def _updateSandBoxPattern(self):
        self.getSandboxDialog().setPattern(self._patternLE.text())

    def unvalidPatternDefinition(self, pattern, error):
        """Overwrite NameFilter.unvalidPatternDefinition"""
        title = 'regular expression %s is invalid' % pattern
        mess = qt.QMessageBox((qt.QMessageBox.warning), title, parent=self, text=(str(error)))
        mess.setModal(False)
        mess.show()

    def setActiveFilter(self, filter):
        self.activeFilter = filter
        self._sandBoxPB.setVisible(filter == 'regular expression')