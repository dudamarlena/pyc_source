# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/utils/sandboxes.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 7449 bytes
"""
This module is used to define the process of the reference creator.
This is related to the issue #184
"""
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '19/07/2018'
from silx.gui import qt
from tomwer.core.process.conditions.filters import RegularExpressionFilter

class RegularExpressionSandBoxDialog(qt.QDialog):
    __doc__ = '\n    Dialog for showing the NameFilterSandBoxDialog\n    '

    def __init__(self, parent=None, pattern=None):
        qt.QDialog.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self.setWindowTitle('Regular expression sand box')
        self.sandbox = RegularExpressionSandBox(parent=self, pattern=pattern)
        self.layout().addWidget(self.sandbox)
        types = qt.QDialogButtonBox.Close
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._buttons.setStandardButtons(types)
        self.layout().addWidget(self._buttons)
        self._buttons.button(qt.QDialogButtonBox.Close).clicked.connect(self.hide)
        self.setPattern = self.sandbox.setPattern
        self.setPattern(pattern=pattern)


class RegularExpressionSandBox(RegularExpressionFilter, qt.QWidget):
    __doc__ = "\n    Widget to see if the pattern will 'valid' the given value or not\n    "

    def __init__(self, parent=None, pattern=None):
        _pattern = pattern
        if _pattern is None:
            _pattern = ''
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self._docLabel = qt.QLabel('<a href="https://docs.python.org/3/library/re.html"> See documentation</a>', self)
        self._docLabel.setOpenExternalLinks(True)
        self.layout().addWidget(self._docLabel)
        self._valueLE = qt.QLineEdit('', parent=self)
        self._valueLE.editingFinished.connect(self.applyFilter)
        self._valueLE.setAlignment(qt.Qt.AlignCenter)
        self.layout().addWidget(self._valueLE)
        style = qt.QApplication.style()
        self._arrowWidget = qt.QWidget(parent=self)
        self._arrowWidget.setLayout(qt.QHBoxLayout())
        self._arrowWidget.setContentsMargins(0, 0, 0, 0)
        self._arrowWidget.layout().setSpacing(0)
        self._arrow = qt.QLabel(parent=(self._arrowWidget))
        self._arrow.setMinimumSize(qt.QSize(55, 55))
        icon = style.standardIcon(qt.QStyle.SP_ArrowDown)
        self._arrow.setPixmap(icon.pixmap(55, 55))
        slicer1 = qt.QWidget(parent=(self._arrowWidget))
        slicer1.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        slicer2 = qt.QWidget(parent=(self._arrowWidget))
        slicer2.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self._arrowWidget.layout().addWidget(slicer1)
        self._arrowWidget.layout().addWidget(self._arrow)
        self._arrowWidget.layout().addWidget(slicer2)
        self.layout().addWidget(self._arrowWidget)
        self._patternWidget = qt.QWidget(parent=self)
        self._patternWidget.setLayout(qt.QHBoxLayout())
        slicer1 = qt.QWidget(parent=(self._arrowWidget))
        slicer1.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        slicer2 = qt.QWidget(parent=(self._arrowWidget))
        slicer2.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self._patternWidget.layout().addWidget(slicer1)
        self._patternWidget.layout().addWidget(qt.QLabel('pattern:'))
        self._patternLE = qt.QLineEdit((_pattern or ''), parent=(self._patternWidget))
        self._patternWidget.layout().addWidget(self._patternLE)
        self._patternWidget.layout().addWidget(slicer2)
        self.layout().addWidget(self._patternWidget)
        self._patternLE.editingFinished.connect(self._updatePattern)
        self._resultWidget = qt.QWidget(parent=self)
        self._resultWidget.setLayout(qt.QHBoxLayout())
        self._resultWidget.setContentsMargins(0, 0, 0, 0)
        self._resultWidget.layout().setSpacing(0)
        self._resultLabel = qt.QLabel(parent=(self._resultWidget))
        self._resultLabel.setMinimumSize(qt.QSize(40, 40))
        slicer1 = qt.QWidget(parent=(self._resultWidget))
        slicer1.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        slicer2 = qt.QWidget(parent=(self._resultWidget))
        slicer2.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self._resultWidget.layout().addWidget(slicer1)
        self._resultWidget.layout().addWidget(self._resultLabel)
        self._resultWidget.layout().addWidget(slicer2)
        self.layout().addWidget(self._resultWidget)
        RegularExpressionFilter.__init__(self, _pattern)

    def setPattern(self, pattern):
        self._patternLE.setText(pattern or '')
        RegularExpressionFilter.setPattern(self, pattern)
        self.applyFilter()

    def applyFilter(self):
        """
        Update result label depending on the value to check and the filter
        """
        value = self._valueLE.text()
        style = qt.QApplication.style()
        if self.isFiltered(value):
            icon = style.standardIcon(qt.QStyle.SP_DialogNoButton)
        else:
            icon = style.standardIcon(qt.QStyle.SP_DialogYesButton)
        self._resultLabel.setPixmap(icon.pixmap(40, 40))

    def _updatePattern(self):
        """callback when the pattern is modify"""
        self.blockSignals(True)
        self.setPattern(self._patternLE.text())
        self.blockSignals(False)

    @staticmethod
    def description():
        return 'A simple sand box to play with pattern definition and input names to make sure it will have the requested behavior.'

    def unvalidPatternDefinition(self, pattern, error):
        """Overwrite NameFilter.unvalidPatternDefinition"""
        txt = 'regular expression "%s" is invalid. Error is:' % pattern
        mess = qt.QMessageBox(parent=self, icon=(qt.QMessageBox.warning), text=txt)
        mess.setInformativeText(str(error))
        mess.setWindowTitle('Regular expression failed')
        mess.setModal(False)
        mess.show()