# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/hardware_modules/iir/iir.py
# Compiled at: 2017-08-29 09:44:06
from . import iir_theory
from .. import FilterModule
from ...attributes import IntRegister, BoolRegister, ComplexProperty, FloatProperty, StringProperty, CurveSelectProperty, GainRegister, ConstantIntRegister, FloatAttributeListProperty, ComplexAttributeListProperty
from ...widgets.module_widgets import IirWidget
from ...modules import SignalLauncher
import numpy as np
from qtpy import QtCore

class SignalLauncherIir(SignalLauncher):
    update_plot = QtCore.Signal()


class OverflowProperty(StringProperty):

    def get_value(self, obj):
        value = obj.overflow_bitfield
        if value == 0:
            text = 'no overflow'
        elif bool(value & 127):
            text = 'sum and internal saturation'
        elif bool(value & 64):
            text = 'sum saturation'
        elif bool(value & 63):
            text = 'internal saturation'
        else:
            text = 'unknown overflow %d' % value
        return text

    def validate_and_normalize(self, obj, value):
        return self.get_value(obj)

    def set_value(self, obj, value):
        self.launch_signal(obj, value)


class IirListProperty(ComplexProperty):
    """
    master property to store zeros and poles
    """
    default = []

    def set_value(self, obj, value):
        """
        the master's setter writes its value to the slave lists
        """
        real, complex = [], []
        for v in value:
            if np.imag(v) == 0:
                real.append(v.real)
            else:
                complex.append(v)

        with obj.do_setup:
            setattr(obj, 'complex_' + self.name, complex)
            setattr(obj, 'real_' + self.name, real)

    def get_value(self, obj):
        """
        the master's getter collects its value from the real and complex list
        """
        return list(getattr(obj, 'complex_' + self.name) + getattr(obj, 'real_' + self.name))

    def validate_and_normalize(self, obj, value):
        """
        Converts the value in a list of float numbers.
        """
        if not np.iterable(value):
            value = [
             value]
        return [ self.validate_and_normalize_element(obj, val) for val in value ]

    def validate_and_normalize_element(self, obj, val):
        return super(IirListProperty, self).validate_and_normalize(obj, val)


class IirFloatListProperty(FloatAttributeListProperty):
    """
    slave property to store real part of zeros and poles
    """

    def value_updated(self, obj, value=None, appendix=[]):
        super(IirFloatListProperty, self).value_updated(obj, value=value, appendix=appendix)
        pole_or_zero = self.name.split('_')[1]
        getattr(obj.__class__, pole_or_zero).value_updated(obj)

    def validate_and_normalize_element(self, obj, val):
        """
        makes sure that real poles are strictly positive. val=0 is turned into val=-1.
        """
        val = FloatAttributeListProperty.validate_and_normalize_element(self, obj, val)
        pole_or_zero = self.name.split('_')[1]
        if val > 0 and pole_or_zero == 'pole':
            obj._logger.warning('Real pole %s has a positive real part. This will lead to unstable behavior. The value was changed to %s. ', val, val * -1)
            val *= -1
        if val == 0:
            obj._logger.warning('Real %s %s has a real part of zero. This will lead to unstable behavior. The value was changed to %s. ', pole_or_zero, val, -1)
            val = -1
        return val

    def list_changed(self, module, operation, index, value=None):
        """ make sure that an element from one of the four lists is selected at once"""
        if operation == 'select':
            if not hasattr(module, '_selecting') or not getattr(module, '_selecting'):
                try:
                    setattr(module, '_selecting', True)
                    for name in [ start + '_' + end for start in ['real', 'complex'] for end in ['poles', 'zeros'] ]:
                        if name != self.name:
                            getattr(module, name).selected = None
                            module._logger.info('%s.selected = None', name)

                    setattr(module, '_selected_pole_or_zero', self.name)
                    setattr(module, '_selected_index', index)
                finally:
                    setattr(module, '_selecting', False)

                super(IirFloatListProperty, self).list_changed(module, operation, index, value=value)
                module._signal_launcher.update_plot.emit()
        else:
            super(IirFloatListProperty, self).list_changed(module, operation, index, value=value)
        return


class IirComplexListProperty(IirFloatListProperty, ComplexAttributeListProperty):
    """
    slave property to store complex part of zeros and poles
    """

    def validate_and_normalize_element(self, obj, val):
        """
        real part should be strictly negative. imaginary part is in principle arbitrary,
        but will be kept positive for simplicity.
        """
        val = ComplexAttributeListProperty.validate_and_normalize_element(self, obj, val)
        re = val.real
        im = val.imag
        pole_or_zero = self.name.split('_')[1]
        if re > 0 and pole_or_zero == 'pole':
            re *= -1
            obj._logger.warning('Real pole %s has a positive real part. This will lead to unstable behavior. The value was changed to %s. ', val)
        if re == 0:
            re = -1
            obj._logger.warning('Real %s %s has a real part of zero. This will lead to unstable behavior. The value was changed to %s. ', pole_or_zero, val, complex(re, im))
        if im < 0:
            im *= -1
            obj._logger.info('Imaginary part of complex %s %s was inverted for simplicity. New value is %s.', pole_or_zero, val, complex(re, im))
        return complex(re, im)


class IIR(FilterModule):
    _signal_launcher = SignalLauncherIir
    iirfilter = None
    _minloops = 5
    _maxloops = 1023
    _delay = 5
    _method = 'gbt'
    _alpha = 0.5
    _invert = True
    _IIRBITS = ConstantIntRegister(512)
    _IIRSHIFT = ConstantIntRegister(516)
    _IIRSTAGES = ConstantIntRegister(520)
    _widget_class = IirWidget
    _setup_attributes = [
     'input',
     'loops',
     'zeros',
     'poles',
     'output_direct',
     'inputfilter',
     'gain',
     'on',
     'bypass',
     'data_curve']
    _gui_attributes = [
     'input',
     'loops',
     'complex_zeros',
     'complex_poles',
     'real_zeros',
     'real_poles',
     'output_direct',
     'inputfilter',
     'gain',
     'on',
     'bypass',
     'overflow',
     'data_curve']
    loops = IntRegister(256, doc='Decimation factor of IIR w.r.t. 125 MHz. Must be at least %d. ' % _minloops, default=_minloops, min=_minloops, max=_maxloops, call_setup=True)
    on = BoolRegister(260, 0, doc='IIR is on', default=False)
    bypass = BoolRegister(260, 1, doc='IIR is bypassed', default=False)
    complex_poles = IirComplexListProperty(default=[], default_element=complex(-1000.0, 10000.0), log_increment=True)
    complex_zeros = IirComplexListProperty(default=[], default_element=complex(-1000.0, 10000.0), log_increment=True)
    real_poles = IirFloatListProperty(default=[], default_element=-10000.0, log_increment=True)
    real_zeros = IirFloatListProperty(default=[], default_element=-10000.0, log_increment=True)
    zeros = IirListProperty(call_setup=True)
    poles = IirListProperty(call_setup=True)
    gain = FloatProperty(min=-1e+20, max=1e+20, default=1.0, increment=1e-20, log_increment=True, call_setup=True)
    overflow_bitfield = IntRegister(264, doc='Bitmask for various overflow conditions')
    overflow = OverflowProperty(doc='a string indicating the overflow status of the iir module')
    data_curve = CurveSelectProperty(doc='NA curve id to use as a basis for the graphical filter design', no_curve_first=True, call_setup=True, default=-1)

    @property
    def output_saturation(self):
        """ returns True if the output of the IIR filter has saturated since
        the last reset """
        return bool(self.overflow_bitfield & 64)

    @property
    def internal_overflow(self):
        """ returns True if the IIR filter has experienced an internal
        overflow (leading to saturation) since the last reset"""
        overflow = bool(self.overflow_bitfield & 63)
        if overflow:
            self._logger.info('Internal overflow has occured. Bit pattern %s', bin(self.overflow_bitfield))
        return overflow

    def _from_double(self, v, bitlength=64, shift=0):
        v = int(np.round(v * 2 ** shift))
        v = v & 2 ** bitlength - 1
        hi = v >> 32 & 4294967295
        lo = v >> 0 & 4294967295
        return (hi, lo)

    def _to_double(self, hi, lo, bitlength=64, shift=0):
        hi = int(hi) & (1 << bitlength - 32) - 1
        lo = int(lo) & 4294967295
        v = int((hi << 32) + lo)
        if v >> bitlength - 1 != 0:
            v = v - 2 ** bitlength
        v = np.float64(v) / 2 ** shift
        return v

    @property
    def coefficients(self):
        l = self.loops
        if l == 0:
            return np.array([])
        else:
            if l > self._IIRSTAGES:
                l = self._IIRSTAGES
            if hasattr(self, '_writtendata'):
                data = self._writtendata
            else:
                return
            coefficients = np.zeros((l, 6), dtype=np.float64)
            bitlength = self._IIRBITS
            shift = self._IIRSHIFT
            for i in range(l):
                for j in range(6):
                    if j == 2:
                        coefficients[(i, j)] = 0
                    elif j == 3:
                        coefficients[(i, j)] = 1.0
                    else:
                        if j > 3:
                            k = j - 2
                        else:
                            k = j
                        coefficients[(i, j)] = self._to_double(data[(i * 8 + 2 * k + 1)], data[(i * 8 + 2 * k)], bitlength=bitlength, shift=shift)
                        if j > 3 and self._invert:
                            coefficients[(i, j)] *= -1

            return coefficients

    @coefficients.setter
    def coefficients(self, v):
        bitlength = self._IIRBITS
        shift = self._IIRSHIFT
        stages = self._IIRSTAGES
        if v is None:
            v = []
            self._logger.warning('Iir coefficient was set to None. and converted to an empty list. ')
        v = np.array([ vv for vv in v ], dtype=np.float64)
        l = len(v)
        if l > stages:
            raise Exception('Error: Filter contains too many sections to be implemented')
        data = np.zeros(stages * 8, dtype=np.uint32)
        for i in range(l):
            for j in range(6):
                if j == 2:
                    if v[(i, j)] != 0:
                        self._logger.warning('Attention: b_2 (' + str(i) + ') is not zero but ' + str(v[(i, j)]))
                elif j == 3:
                    if v[(i, j)] != 1:
                        self._logger.warning('Attention: a_0 (' + str(i) + ') is not one but ' + str(v[(i, j)]))
                else:
                    if j > 3:
                        k = j - 2
                        if self._invert:
                            v[(i, j)] *= -1
                    else:
                        k = j
                    hi, lo = self._from_double(v[(i, j)], bitlength=bitlength, shift=shift)
                    data[i * 8 + k * 2 + 1] = hi
                    data[i * 8 + k * 2] = lo

        data = [ int(d) for d in data ]
        self._writes(32768, data)
        self._writtendata = data
        return

    def _setup_unity(self):
        """sets the IIR filter transfer function unity"""
        c = np.zeros((self._IIRSTAGES, 6), dtype=np.float64)
        c[(0, 0)] = 1.0
        c[:, 3] = 1.0
        self.coefficients = c
        self.loops = 1

    def _setup_zero(self):
        """sets the IIR filter transfer function zero"""
        c = np.zeros((self._IIRSTAGES, 6), dtype=np.float64)
        c[:, 3] = 1.0
        self.coefficients = c
        self.loops = 1

    def _setup(self):
        """
        Setup an IIR filter

        the transfer function of the filter will be (k ensures DC-gain = g):

                  (s-2*pi*z[0])*(s-2*pi*z[1])...
        H(s) = k*-------------------
                  (s-2*pi*p[0])*(s-2*pi*p[1])...

        returns
        --------------------------------------------------
        coefficients   data to be passed to iir.bodeplot to plot the
                       realized transfer function
        """
        with self.do_setup:
            if self._IIRSTAGES == 0:
                raise Exception('Error: This FPGA bitfile does not support IIR filters! Please use an IIR version!')
            self.on = False
            self.iirfilter = iir_theory.IirFilter(zeros=self.zeros, poles=self.poles, gain=self.gain, loops=self.loops, dt=8e-09 * self._frequency_correction, minloops=self._minloops, maxloops=self._maxloops, iirstages=self._IIRSTAGES, totalbits=self._IIRBITS, shiftbits=self._IIRSHIFT, inputfilter=0, moduledelay=self._delay)
            self.loops = self.iirfilter.loops
            self.coefficients = self.iirfilter.coefficients
            self._logger.debug('Filter sampling frequency is %.3s MHz', 1e-06 / self.sampling_time)
            self.iirfilter.inputfilter = self.inputfilter
            self._logger.debug('IIR anti-aliasing input filter set to: %s MHz', self.iirfilter.inputfilter * 1e-06)
            self.on = True
            self._logger.debug('IIR filter ready')
            dev = np.abs((self.coefficients[0:len(self.iirfilter.coefficients)] - self.iirfilter.coefficients).flatten())
            maxdev = max(dev)
            reldev = maxdev / abs(self.iirfilter.coefficients.flatten()[np.argmax(dev)])
            if reldev > 0.05:
                self._logger.warning('Maximum deviation from design coefficients: %.4g (relative: %.4g)', maxdev, reldev)
            else:
                self._logger.debug('Maximum deviation from design coefficients: %.4g (relative: %.4g)', maxdev, reldev)
            if bool(self.overflow_bitfield):
                self._logger.warning('IIR Overflow detected. Pattern: %s', bin(self.overflow_bitfield))
            else:
                self._logger.debug('IIR Overflow pattern: %s', bin(self.overflow_bitfield))
            self._signal_launcher.update_plot.emit()

    @property
    def sampling_time(self):
        return 8e-09 / self._frequency_correction * self.loops

    def transfer_function(self, frequencies, extradelay=0, kind='final'):
        """
        Returns a complex np.array containing the transfer function of the
        current IIR module setting for the given frequency array. The
        best-possible estimation of delays is automatically performed for
        all kinds of transfer function. The setting of 'bypass' is ignored
        for this computation, i.e. the theoretical and measured transfer
        functions can only agree if bypass is False.

        Parameters
        ----------
        frequencies: np.array or float
            Frequencies to compute the transfer function for
        extradelay: float
            External delay to add to the transfer function (in s). If zero,
            only the delay for internal propagation from input to
            output_signal is used. If the module is fed to analog inputs and
            outputs, an extra delay of the order of 150 ns must be passed as
            an argument for the correct delay modelisation.
        kind: str
            The IIR filter design is composed of a number of steps. Each
            step slightly modifies the transfer function to adapt it to
            the implementation of the IIR. The various intermediate transfer
            functions can be helpful to debug the iir filter.

            kind should be one of the following (default is 'implemented'):
            - 'all': returns a list of data to be passed to iir.bodeplot
              with all important kinds of transfer functions for debugging
            - 'continuous': the designed transfer function in continuous time
            - 'before_partialfraction_continuous': continuous filter just
              before partial fraction expansion of the coefficients. The
              partial fraction expansion introduces a large numerical error for
              higher order filters, so this is a good place to check whether
              this is a problem for a particular filter design
            - 'before_partialfraction_discrete': discretized filter just before
              partial fraction expansion of the coefficients. The partial
              fraction expansion introduces a large numerical error for higher
              order filters, so this is a good place to check whether this is
              a problem for a particular filter design
            - 'before_partialfraction_discrete_zoh': same as previous,
              but zero order hold assumption is used to transform from
              continuous to discrete
            - 'discrete': the transfer function after transformation to
              discrete time
            - 'discrete_samplehold': same as discrete, but zero delay
              between subsequent biquads is assumed
            - 'highprecision': hypothetical transfer function assuming that
              64 bit fixed point numbers were used in the fpga (decimal point
              at bit 48)
            - 'implemented': transfer function after rounding the
              coefficients to the precision of the fpga

        Returns
        -------
        tf: np.array(..., dtype=np.complex)
            The complex open loop transfer function of the module.
        If kind=='all', a list of plotdata tuples is returned that can be
        passed directly to iir.bodeplot().
        """
        try:
            tf = getattr(self.iirfilter, 'tf_' + kind)(frequencies)
        except AttributeError:
            tf = frequencies * 0 + 1e-12

        return tf

    def select_pole_or_zero(self, value, logdist=True, search_in=[ start + '_' + end for start in [
 'real', 'complex'] for end in [
 'poles', 'zeros']
]):
        """
        selects the pole or zero closest to value

        logdist=True computes the distance in logarithmic units
        search_in may be used to restrict the search to certain sublists
        """
        mindist = None
        for name in search_in:
            for element in getattr(self, name):
                if name.startswith('complex'):
                    elementvalue = element.imag
                else:
                    elementvalue = element
                if logdist:
                    dist = abs(abs(value) / abs(elementvalue))
                    if dist < 1.0:
                        dist = 1.0 / dist
                else:
                    dist = abs(abs(value) - abs(elementvalue))
                if mindist is None or dist < mindist:
                    mindist = dist
                    bestmatch = element
                    bestname = name

        if mindist is None:
            self.complex_poles.selected = None
        else:
            getattr(self, bestname).select(bestmatch)
        return