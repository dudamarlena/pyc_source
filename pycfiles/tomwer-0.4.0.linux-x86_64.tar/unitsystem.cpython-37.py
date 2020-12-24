# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/utils/unitsystem.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 5012 bytes
"""
This module is used to define the process of the reference creator.
This is related to the issue #184
"""
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '21/09/2018'
from silx.gui import qt
from tomwer.unitsystem import metricsystem
import logging
_logger = logging.getLogger(__name__)

class MetricEntry(qt.QWidget):
    __doc__ = '\n    Create a simple line with a name, a QLineEdit and a combobox to define the\n    unit in order to define a metric value.\n    \n    :param str name: name of the metric value to define\n    :param str: base_unit. Default way to present a value when setted\n    '
    _CONVERSION = {'nm':metricsystem.nanometer, 
     'mm':metricsystem.millimeter, 
     'cm':metricsystem.centimeter, 
     'm':metricsystem.meter}

    def __init__(self, name, default_unit='m', parent=None):
        qt.QWidget.__init__(self, parent)
        assert type(default_unit) is str
        assert default_unit in ('nm', 'mm', 'cm', 'm')
        self._base_unit = default_unit
        self.setLayout(qt.QHBoxLayout())
        self._label = qt.QLabel(name, parent=self)
        self.layout().addWidget(self._label)
        self._qlePixelSize = qt.QLineEdit('0.0', parent=self)
        self._qlePixelSize.setValidator(qt.QDoubleValidator(self._qlePixelSize))
        self.layout().addWidget(self._qlePixelSize)
        self._qcbUnit = qt.QComboBox(parent=self)
        self._qcbUnit.addItem('nm')
        self._qcbUnit.addItem('mm')
        self._qcbUnit.addItem('cm')
        self._qcbUnit.addItem('m')
        self.layout().addWidget(self._qcbUnit)
        self._resetBaseUnit()

    def getCurrentUnit(self):
        assert self._qcbUnit.currentText() in self._CONVERSION
        return self._CONVERSION[self._qcbUnit.currentText()]

    def setValue(self, value):
        """
        
        :param float value: pixel size in international metric system (meter) 
        """
        _value = value
        if type(_value) is str:
            try:
                _value = float(_value)
            except Exception as error:
                try:
                    raise ValueError('Given string does not represent a float', error)
                    return
                finally:
                    error = None
                    del error

        assert isinstance(_value, float)
        self._qlePixelSize.setText(str(_value))
        self._resetBaseUnit()

    def _resetBaseUnit(self):
        """Simple reset of the combobox according to the base_unit"""
        index = self._qcbUnit.findText(self._base_unit)
        if index is None:
            raise ValueError('unrecognized base unit')
        else:
            self._qcbUnit.setCurrentIndex(index)

    def getValue(self):
        """
        
        :return: the value in meter
        :rtype: float
        """
        return float(self._qlePixelSize.text()) * self.getCurrentUnit()


class CentimeterEntry(MetricEntry):
    __doc__ = '\n    Define a QlineEdit which will set and get metric values in centimeter\n    '

    def __init__(self, name, default_unit='cm', parent=None):
        MetricEntry.__init__(self, name, default_unit=default_unit, parent=parent)

    def setValue(self, value):
        """
    
        :param float value: pixel size in centimeter 
        """
        _value = value
        if type(_value) is str:
            try:
                _value = float(_value)
            except Exception as error:
                try:
                    raise ValueError('Given string does not represent a float', error)
                finally:
                    error = None
                    del error

        _value = _value * metricsystem.centimeter
        MetricEntry.setValue(self, _value)

    def getValue(self):
        """

        :return: the value in meter
        :rtype: float
        """
        value = MetricEntry.getValue(self)
        return value / metricsystem.centimeter