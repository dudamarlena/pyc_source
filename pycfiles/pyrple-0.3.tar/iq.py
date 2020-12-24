# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/hardware_modules/iq.py
# Compiled at: 2017-08-29 09:44:06
import sys
from time import sleep
from collections import OrderedDict
import numpy as np
from ..attributes import BoolRegister, FloatRegister, SelectRegister, IntRegister, PhaseRegister, FrequencyRegister, FloatProperty, FilterRegister, FilterProperty, GainRegister
from ..widgets.module_widgets import IqWidget
from ..pyrpl_utils import sorted_dict
from . import FilterModule

class IqGain(FloatProperty):
    """descriptor for the gain of the Iq module"""

    def get_value(self, obj):
        return obj._g1 / 8

    def set_value(self, obj, val):
        obj._g1 = float(val) * 8
        obj._g4 = float(val) * 8
        return val


class IqAcbandwidth(FilterProperty):
    """descriptor for the acbandwidth of the Iq module"""

    def valid_frequencies(self, module):
        return [ freq for freq in module.__class__.inputfilter.valid_frequencies(module) if freq >= 0 ]

    def get_value(self, obj):
        if obj is None:
            return self
        else:
            return -obj.inputfilter

    def set_value(self, instance, val):
        if np.iterable(val):
            val = val[0]
        val = float(val)
        instance.inputfilter = -val
        return val


class Iq(FilterModule):
    _widget_class = IqWidget
    _setup_attributes = ['input',
     'acbandwidth',
     'frequency',
     'bandwidth',
     'quadrature_factor',
     'output_signal',
     'gain',
     'amplitude',
     'phase',
     'output_direct']
    _gui_attributes = _setup_attributes
    _delay = 5
    _output_signals = sorted_dict(quadrature=0, output_direct=1, pfd=2, off=3, quadrature_hf=4)
    output_signals = _output_signals.keys()
    output_signal = SelectRegister(268, options=_output_signals, doc='Signal to send back to DSP multiplexer')
    bandwidth = FilterRegister(292, filterstages=560, shiftbits=564, minbw=568, doc='Quadrature filter bandwidths [Hz].0 = off, negative bandwidth = highpass')
    _valid_bandwidths = bandwidth.valid_frequencies

    @property
    def bandwidths(self):
        return self._valid_bandwidths(self)

    on = BoolRegister(256, 0, doc='If set to False, turns off the module, e.g. to                       re-synchronize the phases')
    pfd_on = BoolRegister(256, 1, doc='If True: Turns on the PFD module,                        if False: turns it off and resets integral')
    _LUTSZ = IntRegister(512)
    _LUTBITS = IntRegister(516)
    _PHASEBITS = 32
    _GAINBITS = 18
    _SIGNALBITS = 14
    _LPFBITS = 24
    _SHIFTBITS = 8
    pfd_integral = FloatRegister(336, bits=_SIGNALBITS, norm=_SIGNALBITS, doc='value of the pfd integral [volts]')
    phase = PhaseRegister(260, bits=_PHASEBITS, invert=True, doc='Phase shift between modulation                           and demodulation [degrees]')
    frequency = FrequencyRegister(264, bits=_PHASEBITS, doc='frequency of iq demodulation [Hz]')
    _g1 = GainRegister(272, bits=_GAINBITS, norm=2 ** _SHIFTBITS, doc='gain1 of iq module [volts]')
    _g2 = GainRegister(276, bits=_GAINBITS, norm=2 ** _SHIFTBITS, doc='gain2 of iq module [volts]')
    amplitude = GainRegister(276, bits=_GAINBITS, norm=2 ** (_GAINBITS - 1), doc='amplitude of coherent modulation [volts]')
    _g3 = GainRegister(280, bits=_GAINBITS, norm=2 ** _SHIFTBITS, doc='gain3 of iq module [volts]')
    quadrature_factor = GainRegister(280, bits=_GAINBITS, norm=1.0, default=1.0, doc='amplification factor of demodulated signal [a.u.]')
    _g4 = GainRegister(284, bits=_GAINBITS, norm=2 ** _SHIFTBITS, doc='gain4 of iq module [volts]')
    acbandwidths = [
     0] + [ int(2.371593461809983 * 2 ** n) for n in range(1, 27)
          ]
    gain = IqGain(doc='gain of the iq module (see drawing)')
    acbandwidth = IqAcbandwidth(doc='positive corner frequency of input high pass filter')

    def _setup(self):
        """
        Sets up an iq demodulator, refer to the drawing in the GUI for an explanation of the IQ layout.
        (just setting the attributes is OK).
        """
        pass

    _na_averages = IntRegister(304, doc='number of cycles to perform na-averaging over')
    _na_sleepcycles = IntRegister(308, doc='number of cycles to wait before starting to average')

    @property
    def _nadata(self):
        return self._nadata_total / float(self._na_averages)

    @property
    def _nadata_total(self):
        attempt = 0
        a, b, c, d = self._reads(320, 4)
        while not (a >> 31 == 0 and b >> 31 == 0 and c >> 31 == 0 and d >> 31 == 0):
            a, b, c, d = self._reads(320, 4)
            self._logger.warning('NA data not ready yet. Try again!')
            attempt += 1
            if attempt > 10:
                raise Exception('Trying to recover NA data while averaging is not finished. Some setting is wrong. ')

        sum = np.complex128(self._to_pyint(int(a) + (int(b) << 31), bitlength=62)) + np.complex128(self._to_pyint(int(c) + (int(d) << 31), bitlength=62)) * complex(0.0, 1.0)
        return sum

    def na_trace(self, start=0, stop=100000.0, points=1001, rbw=100, avg=1.0, amplitude=0.1, input='adc1', output_direct='off', acbandwidth=0, sleeptimes=0.5, logscale=False, stabilize=None, maxamplitude=1.0):
        if logscale:
            x = np.logspace(np.log10(start), np.log10(stop), points, endpoint=True)
        else:
            x = np.linspace(start, stop, points, endpoint=True)
        y = np.zeros(points, dtype=np.complex128)
        amplitudes = np.zeros(points, dtype=np.float64)
        maxamplitude = abs(maxamplitude)
        amplitude = abs(amplitude)
        if abs(amplitude) > maxamplitude:
            amplitude = maxamplitude
        self.setup(frequency=x[0], bandwidth=rbw, gain=0, phase=0, acbandwidth=-np.array(acbandwidth), amplitude=0, input=input, output_direct=output_direct, output_signal='output_direct')
        rbw = self.bandwidth[0]
        self._logger.info('Estimated acquisition time: %.1f s', float(avg + sleeptimes) * points / rbw)
        sys.stdout.flush()
        self._na_averages = np.int(np.round(125000000.0 / rbw * avg))
        self._na_sleepcycles = np.int(np.round(125000000.0 / rbw * sleeptimes))
        rescale = 2.0 ** (-self._LPFBITS) * 4.0
        try:
            self.amplitude = amplitude
            for i in range(points):
                self.frequency = x[i]
                sleep(1.0 / rbw * (avg + sleeptimes))
                x[i] = self.frequency
                y[i] = self._nadata
                amplitudes[i] = self.amplitude
                if amplitudes[i] == 0:
                    y[i] *= rescale
                else:
                    y[i] *= rescale / self.amplitude
                if stabilize is not None:
                    amplitude = stabilize / np.abs(y[i])
                if amplitude > maxamplitude:
                    amplitude = maxamplitude
                self.amplitude = amplitude

        except:
            self.amplitude = 0
            self._logger.info('NA output turned off due to an exception')
            raise
        else:
            self.amplitude = 0

        if start == stop:
            x = np.linspace(0, 1.0 / rbw * (avg + sleeptimes), points, endpoint=False)
        if stabilize is None:
            return (x, y)
        else:
            return (
             x, y, amplitudes)
            return

    def transfer_function(self, frequencies, extradelay=0):
        """
        Returns a complex np.array containing the transfer function of the
        current IQ module setting for the given frequency array. The given
        transfer function is only relevant if the module is used as a
        bandpass filter, i.e. with the setting (gain != 0). If extradelay = 0,
        only the default delay is taken into account, i.e. the propagation
        delay from input to output_signal.

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
        quadrature_delay = 2
        module_delay = self._delay - quadrature_delay
        frequencies = np.array(frequencies, dtype=np.complex)
        tf = np.array(frequencies * 0, dtype=np.complex) + self.gain
        for f in self.bandwidth:
            if f == 0:
                continue
            elif f > 0:
                tf *= 1.0 / (1.0 + complex(0.0, 1.0) * (frequencies - self.frequency) / f)
                quadrature_delay += 2
            elif f < 0:
                tf *= 1.0 / (1.0 + complex(0.0, 1.0) * f / (frequencies - self.frequency))
                quadrature_delay += 1

        quadrature_delay *= 8e-09 / self._frequency_correction
        tf *= np.exp(complex(0.0, -1.0) * quadrature_delay * (frequencies - self.frequency) * 2 * np.pi)
        f = self.inputfilter
        if f > 0:
            tf /= 1.0 + complex(0.0, 1.0) * frequencies / f
            module_delay += 2
        elif f < 0:
            tf /= 1.0 + complex(0.0, 1.0) * f / frequencies
            module_delay += 1
        delay = module_delay * 8e-09 / self._frequency_correction + extradelay
        tf *= np.exp(complex(0.0, -1.0) * delay * frequencies * 2 * np.pi)
        tf *= np.exp(complex(0.0, 1.0) * self.phase / 180.0 * np.pi)
        return tf