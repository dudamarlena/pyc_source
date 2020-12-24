# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/lamino/tofu/misc.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 5405 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '01/06/2018'
from silx.gui import qt
from tomwer.gui import icons
from tomwer.gui.utils.buttons import PadlockButton
import logging
_logger = logging.getLogger()

class _AngleWidget(qt.QWidget):
    __doc__ = 'Simple widget used to defined an angle'

    def __init__(self, parent, name, defaultVal=0, lockable=False, information=None):
        """
        
        :param parent: 
        :param name: 
        :param defaultVal: 
        :param lockable: if True then add a push button to lock / unlock the
                         variable
        :param information: callabak to display some information. If not None
                            then add a QPushButton calling this callback
        """
        assert type(defaultVal) in (int, float)
        self._lockable = lockable
        qt.QWidget.__init__(self, parent=parent)
        self.setLayout(qt.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(qt.QLabel((name + ':'), parent=self))
        self._angleLE = qt.QLineEdit((str(defaultVal)), parent=self)
        validator = qt.QDoubleValidator(self._angleLE)
        self._angleLE.setValidator(validator)
        self.layout().addWidget(self._angleLE)
        self._infoCallback = information
        if self._infoCallback is not None:
            icon = icons.getQIcon('information')
            self._infoPB = qt.QPushButton(parent=self, icon=icon)
            self._infoPB.pressed.connect(self._infoCallback)
            self._infoPB.setCheckable(False)
            self.layout().addWidget(self._infoPB)
        self._lockButton = PadlockButton(parent=self)
        self.layout().addWidget(self._lockButton)
        self._lockButton.setVisible(self.isLockable())
        self.sigEdited = self._angleLE.textEdited

    def getAngle(self):
        return float(self._angleLE.text())

    def setAngle(self, val):
        if type(val) is not str:
            assert type(val) in (float, int)
        self._angleLE.setText(str(val))

    def isLockable(self):
        return self._lockable

    def isLocked(self):
        return self._lockable and self._lockButton.isLocked()

    def lock(self):
        if self._lockable is False:
            _logger.warning('unable to lock the _AngleWidget cause not defined as lockable')
        self._lockButton.setChecked(True)


class _RegionLE(qt.QWidget):
    __doc__ = 'Widget used to defined a region as (start, end, step)'

    def __init__(self, parent, name):
        super().__init__(parent)
        self.setLayout(qt.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(qt.QLabel(name, parent=self))
        self._regionLE = qt.QLineEdit(parent=self)
        self.layout().addWidget(self._regionLE)
        self.setToolTip('region should be defined as: start, end, step')

    def getRegion(self):
        """

        :return: start voxel, end voxel, step voxel
        :rtype: tuple of int
        """

        def _getParam(regions, index, default):
            try:
                return int(regions[index])
            except:
                return default

        if self._regionLE.text() == '':
            return
        regions = self._regionLE.text().replace(' ', '').split(',')
        sv = _getParam(regions, 0, 0)
        se = _getParam(regions, 1, -1)
        ss = _getParam(regions, 2, 1)
        return (sv, se, ss)

    def setRegion(self, startVox, endVox, stepVox):
        self.setRegionFromStr(','.join([str(startVox), str(endVox), str(stepVox)]))

    def setRegionFromStr(self, _str):
        if _str is None:
            self._regionLE.clear()
        else:
            assert type(_str) is str
            _str = _str.lstrip('(')
            _str = _str.rstrip(')')
            self._regionLE.setText(_str)