# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/datawatcher/configuration.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 5966 bytes
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '18/02/2018'
from silx.gui import qt
from tomwer.core.process.datawatcher.datawatcher import _DataWatcher
from tomwer.core.process.datawatcher import status

class _DWConfigurationWidget(qt.QWidget):
    startByOldestStateChanged = qt.Signal(bool)

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self._observationMethod = _ObservationMethodSelector(parent=self)
        self.layout().addWidget(self._observationMethod)
        self._qcboldest = qt.QCheckBox('Start scan by the oldest', parent=self)
        tooltip = 'If NOT activated will explore folders from the latest to the newest. Otherwise will explore the folders from the newest to the oldest.'
        self._qcboldest.setToolTip(tooltip)
        self.startByOldestStateChanged = self._qcboldest.toggled
        self.layout().addWidget(self._qcboldest)


class _ObservationMethodSelector(qt.QGroupBox):
    __doc__ = 'Group box allowing selection of an observation method'
    sigSelectionChanged = qt.Signal(tuple)

    def __init__(self, parent):
        qt.QGroupBox.__init__(self, parent, title='End acquisition observation method for edf')
        self.setLayout(qt.QVBoxLayout())
        self._qrbXml = qt.QRadioButton((status.DET_END_XML), parent=self)
        self.layout().addWidget(self._qrbXml)
        self._qrbInfo = qt.QRadioButton((status.PARSE_INFO_FILE), parent=self)
        self.layout().addWidget(self._qrbInfo)
        self._qwUserEntry = qt.QWidget(parent=self)
        self.layout().addWidget(self._qwUserEntry)
        self._qrbUserEntry = qt.QRadioButton((status.DET_END_USER_ENTRY), parent=self)
        self.layout().addWidget(self._qrbUserEntry)
        widgetFilePtrn = qt.QWidget(parent=self)
        widgetFilePtrn.setLayout(qt.QHBoxLayout())
        widgetFilePtrn.layout().addWidget(qt.QLabel(text='pattern: ', parent=widgetFilePtrn))
        self._qleFilePattern = qt.QLineEdit(text='', parent=(self._qwUserEntry))
        widgetFilePtrn.layout().addWidget(self._qleFilePattern)
        self.widgetFilePtrn = widgetFilePtrn
        self.layout().addWidget(self.widgetFilePtrn)
        self._qrbXml.setChecked(_DataWatcher.DEFAULT_OBS_METH == status.DET_END_XML)
        self._qrbInfo.setChecked(_DataWatcher.DEFAULT_OBS_METH == status.PARSE_INFO_FILE)
        self._qrbUserEntry.setChecked(_DataWatcher.DEFAULT_OBS_METH == status.DET_END_USER_ENTRY)
        self.widgetFilePtrn.setVisible(self._qrbUserEntry.isVisible())
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer)
        self._qrbUserEntry.toggled.connect(self.widgetFilePtrn.setVisible)
        self._qrbXml.toggled.connect(self._selectionChanged)
        self._qrbInfo.toggled.connect(self._selectionChanged)
        self._qrbUserEntry.toggled.connect(self._selectionChanged)
        self._qleFilePattern.editingFinished.connect(self._selectionChanged)
        t = 'If a file with this pattern is found in the [scan] folder then\n            we will consider the acquisition as ended'
        self._qrbUserEntry.setToolTip(t)
        t = 'Wild charracter allowed'
        self._qleFilePattern.setToolTip(t)
        t = 'If we founf the [scan].xml in the [scan] folder then\n            we will consider the acquisition ended'
        self._qrbXml.setToolTip(t)
        t = 'We will look for the [scan].info file in the [scan]\n            directory. If it exists then we will parse it to get the number of\n            .edf file we should have and wait for all of them to be acquired\n            (also checking file size)'
        self._qrbInfo.setToolTip(t)

    def _selectionChanged(self):
        if self._qrbXml.isChecked():
            self.sigSelectionChanged.emit((status.DET_END_XML,))
        else:
            if self._qrbInfo.isChecked():
                self.sigSelectionChanged.emit((status.PARSE_INFO_FILE,))
            else:
                self.sigSelectionChanged.emit((status.DET_END_USER_ENTRY,
                 {'pattern': self._qleFilePattern.text()}))