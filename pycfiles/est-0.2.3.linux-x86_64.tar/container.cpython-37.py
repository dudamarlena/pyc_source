# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/orangecontrib/est/widgets/container.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 4100 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '13/08/2019'
from silx.gui import qt

class _ParameterWindowContainer(qt.QWidget):
    __doc__ = "Embed the larch parameters windows (should contains getParameters and\n    setParameters and have a sigChanged signal) and add it a 'manual' update\n    mode for convenience\n    "
    sigChanged = qt.Signal()

    def __init__(self, parent, parametersWindow):
        if not parametersWindow is not None:
            raise AssertionError
        else:
            super().__init__(parent=parent)
            self.setLayout(qt.QGridLayout())
            self._mainwidget = parametersWindow(parent=self)
            if not hasattr(self._mainwidget, 'setParameters'):
                raise AssertionError
            elif not hasattr(self._mainwidget, 'getParameters'):
                raise AssertionError
            else:
                self.layout().addWidget(self._mainwidget, 0, 0, 1, 3)
                self._autoCB = qt.QCheckBox('manual update', parent=self)
                self.layout().addWidget(self._autoCB, 1, 1, 1, 1)
                self._autoCB.setToolTip('if activated will wait until you press the "update" button to launch processing. Otherwise executed for each modification in the paramters')
                self._manualUpdatePB = qt.QPushButton('update')
                self.layout().addWidget(self._manualUpdatePB, 1, 2, 1, 1)
                self._manualUpdatePB.setVisible(False)
                self.setParameters = self._mainwidget.setParameters
                self.getParameters = self._mainwidget.getParameters
                self._autoCB.toggled.connect(self._manualUpdatePB.setVisible)
                self._manualUpdatePB.pressed.connect(self._update)
                if hasattr(self._mainwidget, 'sigChanged'):
                    _sig = self._mainwidget.sigChanged
                else:
                    if hasattr(self._mainwidget, 'sigFTParametersSignal'):
                        _sig = self._mainwidget.sigFTParametersSignal
                    else:
                        if hasattr(self._mainwidget, 'sigNormalizationParametersSignal'):
                            _sig = self._mainwidget.sigNormalizationParametersSignal
                        else:
                            if hasattr(self._mainwidget, 'sigXASNormalizationParametersSignal'):
                                _sig = self._mainwidget.sigXASNormalizationParametersSignal
                            else:
                                if hasattr(self._mainwidget, 'sigPostEdgeParametersSignal'):
                                    _sig = self._mainwidget.sigPostEdgeParametersSignal
                                else:
                                    raise ValueError('window not recognized')
        _sig.connect(self._filteredUpdate)

    def _filteredUpdate(self, *args, **kwargs):
        """call _update only if in automatic update mode"""
        if not self._autoCB.isChecked():
            self._update()

    def _update(self, *args, **kwargs):
        self.sigChanged.emit()