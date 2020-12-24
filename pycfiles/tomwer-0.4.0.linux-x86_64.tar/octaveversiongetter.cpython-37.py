# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/ftserie/h5editor/octaveversiongetter.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 2885 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '15/06/2017'
from silx.gui import qt

class OctaveVersionGetter(qt.QGroupBox):
    __doc__ = 'Simple class to set the octave version'
    valueHasChanged = qt.Signal(float)

    def __init__(self, title, parent=None):
        """

        :param str title: the name of the groupbox
        :param QObject parent: the QObject parent of the GroupBox
        """
        qt.QGroupBox.__init__(self, title=title, parent=parent)
        self.setLayout(qt.QHBoxLayout())
        self._qrbInf3_8 = qt.QRadioButton('version < 3.8', parent=self)
        self._qrbInf3_8.setChecked(True)
        self.layout().addWidget(self._qrbInf3_8)
        self._qrbInf3_8.toggled.connect(self.valueChanged)
        self._qrbSup3_8 = qt.QRadioButton('version >= 3.8', parent=self)
        self.layout().addWidget(self._qrbSup3_8)
        self._qrbSup3_8.toggled.connect(self.valueChanged)

    def setVersionInf3_8(self, b):
        """

        :param boolean b: if true then target the octave version < 3.8
        """
        if b:
            self._qrbInf3_8.setChecked(True)
        else:
            self._qrbSup3_8.setChecked(True)

    def isVersionInf3_8(self):
        """
        :return: True if the octave version we are trying to load is oldest
            than 3.8
        """
        return self._qrbInf3_8.isChecked()

    def valueChanged(self):
        self.valueHasChanged.emit(3.6 if self.isVersionInf3_8() else 3.8)