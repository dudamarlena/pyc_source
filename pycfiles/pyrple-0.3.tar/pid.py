# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/hardware_modules/pid.py
# Compiled at: 2017-08-29 09:44:06
import numpy as np
from qtpy import QtCore
from ..attributes import FloatProperty, BoolRegister, FloatRegister, GainRegister
from ..modules import SignalLauncher
from . import FilterModule
from ..widgets.module_widgets import PidWidget

class IValAttribute(FloatProperty):
    """
    Attribute for integrator value
    """

    def get_value(self, obj):
        return float(obj._to_pyint(obj._read(256), bitlength=16)) / 8192

    def set_value(self, obj, value):
        """set the value of the register holding the integrator's sum [volts]"""
        return obj._write(256, obj._from_pyint(int(round(value * 8192)), bitlength=16))


class SignalLauncherPid(SignalLauncher):
    update_ival = QtCore.Signal()

    def __init__(self, module):
        super(SignalLauncherPid, self).__init__(module)
        self.timer_ival = QtCore.QTimer()
        self.timer_ival.setInterval(1000)
        self.timer_ival.timeout.connect(self.update_ival)
        self.timer_ival.setSingleShot(False)
        self.timer_ival.start()

    def _clear(self):
        """
        kill all timers
        """
        self.timer_ival.stop()
        super(SignalLauncherPid, self)._clear()


class Pid(FilterModule):
    _widget_class = PidWidget
    _signal_launcher = SignalLauncherPid
    _setup_attributes = ['input',
     'output_direct',
     'setpoint',
     'p',
     'i',
     'inputfilter',
     'max_voltage',
     'min_voltage']
    _gui_attributes = _setup_attributes + ['ival']

    def _setup(self):
        """
        sets up the pid (just setting the attributes is OK).
        """
        pass

    _delay = 3
    _PSR = 12
    _ISR = 32
    _DSR = 10
    _GAINBITS = 24
    ival = IValAttribute(min=-4, max=4, increment=8.0 / 65536, doc='Current value of the integrator memory (i.e. pid output voltage offset)')
    setpoint = FloatRegister(260, bits=14, norm=8192, doc='pid setpoint [volts]')
    min_voltage = FloatRegister(292, bits=14, norm=8192, doc='minimum output signal [volts]')
    max_voltage = FloatRegister(296, bits=14, norm=8192, doc='maximum output signal [volts]')
    p = GainRegister(264, bits=_GAINBITS, norm=2 ** _PSR, doc='pid proportional gain [1]')
    i = GainRegister(268, bits=_GAINBITS, norm=2 ** _ISR * 2.0 * np.pi * 8e-09, doc='pid integral unity-gain frequency [Hz]')

    @property
    def proportional(self):
        return self.p

    @property
    def integral(self):
        return self.i

    @property
    def derivative(self):
        return self.d

    @property
    def reg_integral(self):
        return self.ival

    @proportional.setter
    def proportional(self, v):
        self.p = v

    @integral.setter
    def integral(self, v):
        self.i = v

    @derivative.setter
    def derivative(self, v):
        self.d = v

    @reg_integral.setter
    def reg_integral(self, v):
        self.ival = v

    def transfer_function(self, frequencies, extradelay=0):
        """
        Returns a complex np.array containing the transfer function of the
        current PID module setting for the given frequency array. The
        settings for p, i, d and inputfilter, as well as delay are aken into
        account for the modelisation. There is a slight dependency of delay
        on the setting of inputfilter, i.e. about 2 extracycles per filter
        that is not set to 0, which is however taken into account.

        Parameters
        ----------
        frequencies: np.array or float
            Frequencies to compute the transfer function for
        extradelay: float
            External delay to add to the transfer function (in s). If zero,
            only the delay for internal propagation from input to
            output_signal is used. If the module is fed to analog inputs and
            outputs, an extra delay of the order of 200 ns must be passed as
            an argument for the correct delay modelisation.

        Returns
        -------
        tf: np.array(..., dtype=np.complex)
            The complex open loop transfer function of the module.
        """
        return Pid._transfer_function(frequencies, p=self.p, i=self.i, d=0, filter_values=self.inputfilter, extradelay_s=extradelay, module_delay_cycle=self._delay, frequency_correction=self._frequency_correction)

    @classmethod
    def _transfer_function(cls, frequencies, p, i, filter_values=list(), d=0, module_delay_cycle=_delay, extradelay_s=0.0, frequency_correction=1.0):
        return Pid._pid_transfer_function(frequencies, p=p, i=i, d=d, frequency_correction=frequency_correction) * Pid._filter_transfer_function(frequencies, filter_values=filter_values, frequency_correction=frequency_correction) * Pid._delay_transfer_function(frequencies, module_delay_cycle=module_delay_cycle, extradelay_s=extradelay_s, frequency_correction=frequency_correction)

    @classmethod
    def _pid_transfer_function(cls, frequencies, p, i, d=0, frequency_correction=1.0):
        """
        returns the transfer function of a generic pid module
        delay is the module delay as found in pid._delay, p, i and d are the
        proportional, integral, and differential gains
        frequency_correction is the module frequency_corection as
        found in pid._frequency_corection
        """
        frequencies = np.array(frequencies, dtype=np.complex)
        tf = i / (frequencies * complex(0.0, 1.0)) * np.exp(complex(0.0, -8e-09) * frequency_correction * frequencies * 2 * np.pi)
        tf += p
        delay = 0
        tf *= np.exp(complex(0.0, -1.0) * delay * frequencies * 2 * np.pi)
        return tf

    @classmethod
    def _delay_transfer_function(cls, frequencies, module_delay_cycle=_delay, extradelay_s=0, frequency_correction=1.0):
        """
        Transfer function of the eventual extradelay of a pid module
        """
        delay = module_delay_cycle * 8e-09 / frequency_correction + extradelay_s
        frequencies = np.array(frequencies, dtype=np.complex)
        tf = np.ones(len(frequencies), dtype=np.complex)
        tf *= np.exp(complex(0.0, -1.0) * delay * frequencies * 2 * np.pi)
        return tf

    @classmethod
    def _filter_transfer_function(cls, frequencies, filter_values, frequency_correction=1.0):
        """
        Transfer function of the inputfilter part of a pid module
        """
        frequencies = np.array(frequencies, dtype=np.complex)
        module_delay = 0
        tf = np.ones(len(frequencies), dtype=complex)
        if not isinstance(filter_values, list):
            filter_values = list([filter_values])
        for f in filter_values:
            if f == 0:
                continue
            elif f > 0:
                tf /= 1.0 + complex(0.0, 1.0) * frequencies / f
                module_delay += 2
            elif f < 0:
                tf /= 1.0 + complex(0.0, 1.0) * f / frequencies
                module_delay += 1

        delay = module_delay * 8e-09 / frequency_correction
        tf *= np.exp(complex(0.0, -1.0) * delay * frequencies * 2 * np.pi)
        return tf