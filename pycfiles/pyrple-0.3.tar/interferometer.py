# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/software_modules/lockbox/models/interferometer.py
# Compiled at: 2017-08-29 09:44:06
from .. import *

class InterferometerPort1(InputDirect):

    @property
    def plot_range(self):
        maxval = np.pi * self.lockbox._unit_in_setpoint_unit('rad')
        return np.linspace(-maxval, maxval, 200)

    def expected_signal(self, phase):
        phase *= self.lockbox._setpoint_unit_in_unit('rad')
        return self.calibration_data.offset + self.calibration_data.amplitude * np.sin(phase)

    def expected_setpoint(self, transmission):
        sinvalue = (transmission - self.calibration_data.offset) / self.calibration_data.amplitude
        if sinvalue > 1.0:
            sinvalue = 1.0
        elif sinvalue < -1.0:
            sinvalue = -1.0
        phase = np.arcsin(sinvalue)
        phase /= self.lockbox._setpoint_unit_in_unit('rad')
        return phase


class InterferometerPort2(InterferometerPort1):

    def expected_signal(self, phase):
        return super(InterferometerPort2, self).expected_signal(-phase)


class Interferometer(Lockbox):
    wavelength = FloatProperty(max=1.0, min=0.0, default=1.064e-06, increment=1e-09)
    _gui_attributes = ['wavelength']
    _setup_attributes = _gui_attributes
    setpoint_unit = SelectProperty(options=['deg',
     'rad'], default='deg')
    _output_units = [
     'm', 'nm']
    _rad_in_deg = 180.0 / np.pi

    @property
    def _deg_in_m(self):
        return self.wavelength / 360.0 / 2.0

    @property
    def _rad_in_m(self):
        return self._rad_in_deg * self._deg_in_m

    inputs = LockboxModuleDictProperty(port1=InterferometerPort1, port2=InterferometerPort2)
    outputs = LockboxModuleDictProperty(piezo=PiezoOutput)


class PdhInterferometerPort1(InterferometerPort1, InputIq):

    def expected_signal(self, phase):
        phase *= self.lockbox._setpoint_unit_in_unit('rad')
        return self.calibration_data.amplitude * np.cos(phase)


class PdhInterferometerPort2(InterferometerPort2, InputIq):

    def expected_signal(self, phase):
        phase *= self.lockbox._setpoint_unit_in_unit('rad')
        return -self.calibration_data.amplitude * np.cos(phase)


class PdhInterferometer(Interferometer):
    inputs = LockboxModuleDictProperty(port1=InterferometerPort1, pdh1=PdhInterferometerPort1)