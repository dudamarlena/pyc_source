# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/software_modules/lockbox/models/fabryperot.py
# Compiled at: 2017-08-29 09:44:06
from .. import *
from .interferometer import Interferometer
from ....async_utils import TimeoutError

class Lorentz(object):
    """ base class for Lorentzian-like signals"""

    def _lorentz(self, x):
        """ lorentzian function """
        return 1.0 / (1.0 + x ** 2)

    def _lorentz_complex(self, x):
        """ complex-valued lorentzian function """
        return 1.0 / (1.0 + complex(0.0, 1.0) * x)

    def _lorentz_slope(self, x):
        """ derivative of _lorentz"""
        return -2.0 * x * self._lorentz(x) ** 2

    def _lorentz_slope_normalized(self, x):
        """ derivative of _lorentz with maximum of 1.0 """
        return self._lorentz_slope(x) / np.abs(self._lorentz_slope(1.0 / np.sqrt(3)))

    def _lorentz_slope_slope(self, x):
        """ second derivative of _lorentz """
        return (-2.0 + 6.0 * x ** 2) * self._lorentz(x) ** 3


class FPReflection(InputSignal, Lorentz):

    def expected_signal(self, setpoint):
        detuning = setpoint * self.lockbox._setpoint_unit_in_unit('bandwidth')
        return self.calibration_data.max - (self.calibration_data.max - self.calibration_data.min) * self._lorentz(detuning)

    @property
    def relative_mean(self):
        """
        returns the ratio between the measured mean value and the expected one.
        """
        return self.mean / self.calibration_data.max

    @property
    def relative_rms(self):
        """
        returns the ratio between the measured rms value and the expected mean.
        """
        return self.rms / self.calibration_data.max


class FPTransmission(FPReflection):

    def expected_signal(self, setpoint):
        detuning = setpoint * self.lockbox._setpoint_unit_in_unit('bandwidth')
        return self.calibration_data.min + (self.calibration_data.max - self.calibration_data.min) * self._lorentz(detuning)


class FPAnalogPdh(InputSignal, Lorentz):
    mod_freq = FrequencyProperty()
    _setup_attributes = InputDirect._setup_attributes + ['mod_freq']
    _gui_attributes = InputDirect._gui_attributes + ['mod_freq']

    def is_locked(self, loglevel=logging.INFO):
        return self.lockbox.inputs.reflection.is_locked(loglevel=loglevel)

    def expected_signal(self, setpoint):
        detuning = setpoint * self.lockbox._setpoint_unit_in_unit('bandwidth')
        return self.calibration_data.amplitude * self._pdh_normalized(detuning, sbfreq=self.mod_freq / self.lockbox._bandwidth_in_Hz, phase=0, eta=self.lockbox.eta)

    def _pdh_normalized(self, x, sbfreq=10.0, phase=0, eta=1):
        """  returns a pdh error signal at for a number of detunings x. """

        def a_ref(x):
            """complex lorentzian reflection"""
            return 1.0 - eta * self._lorentz_complex(x)

        i_ref = np.conjugate(a_ref(x)) * complex(0.0, 1.0) * a_ref(x + sbfreq) + a_ref(x) * np.conjugate(complex(0.0, 1.0) * a_ref(x - sbfreq))
        return np.real(i_ref * np.exp(complex(0.0, 1.0) * phase)) / eta


class FPPdh(InputIq, FPAnalogPdh):
    """ Same as analog pdh signal, but generated from IQ module """


class FPTilt(InputSignal, Lorentz):
    """ Error signal for tilt-locking schemes, e.g.
    https://arxiv.org/pdf/1410.8773.pdf """

    def _tilt_normalized(self, detuning):
        """ do the math and you'll see that the tilt error signal is simply
        the derivative of the cavity lorentzian"""
        return self._lorentz_slope_normalized(detuning)

    def expected_signal(self, setpoint):
        """ expected error signal is centered around zero on purpose"""
        detuning = setpoint * self.lockbox._setpoint_unit_in_unit('bandwidth')
        return self.calibration_data.amplitude * self._tilt_normalized(detuning)

    def is_locked(self, loglevel=logging.INFO):
        return self.lockbox.inputs.reflection.is_locked(loglevel=loglevel)


class FabryPerot(Interferometer):
    _gui_attributes = [
     'finesse', 'round_trip_length', 'eta']
    _setup_attributes = _gui_attributes
    inputs = LockboxModuleDictProperty(transmission=FPTransmission, reflection=FPReflection, pdh=FPPdh)
    finesse = FloatProperty(max=10000000.0, min=0, default=10000)
    round_trip_length = FloatProperty(max=10000000000000.0, min=0, default=1.0)
    eta = FloatProperty(min=0.0, max=1.0, default=1.0)

    @property
    def free_spectral_range(self):
        """ returns the cavity free spectral range in Hz """
        return 299800000.0 / self.round_trip_length

    setpoint_unit = SelectProperty(options=['bandwidth',
     'linewidth'], default='bandwidth')
    _output_units = ['V', 'm', 'Hz', 'nm', 'MHz']

    @property
    def _linewidth_in_m(self):
        return self.wavelength / self.finesse / 2.0

    @property
    def _linewidth_in_Hz(self):
        return self.free_spectral_range / self.finesse

    @property
    def _bandwidth_in_Hz(self):
        return self._linewidth_in_Hz / 2.0

    @property
    def _bandwidth_in_m(self):
        return self._linewidth_in_m / 2.0


class HighFinesseInput(InputSignal):
    """
    Since the number of points in the scope is too small for high finesse cavities, the acquisition is performed in
    2 steps:
        1. Full scan with the actuator, full scope duration, trigged on asg
        2. Full scan with the actuator, smaller scope duration, trigged on input (level defined by previous scan).
    Scope states corresponding to 1 and 2 are "sweep" and "sweep_zoom"
    """

    def sweep_acquire_zoom(self, threshold, input2=None):
        try:
            with self.pyrpl.scopes.pop(self.name) as (scope):
                self.lockbox.unlock()
                scope.load_state('autosweep')
                if 'sweep_zoom' in scope.states:
                    scope.load_state('sweep_zoom')
                else:
                    scope.duration /= self.lockbox.finesse / 20.0
                    scope.trigger_source = 'ch1_negative_edge'
                    scope.hysteresis = 0.002
                    scope.trigger_delay = 0.0
                scope.setup(threshold=threshold, input1=self.signal())
                if input2 is not None:
                    scope.input2 = input2
                scope.save_state('autosweep_zoom')
                self._logger.debug('calibration threshold: %f', threshold)
                curves = scope.curve_async()
                self.lockbox._sweep()
                try:
                    curve1, curve2 = curves.await_result(timeout=100.0 / self.lockbox.asg.frequency + scope.duration)
                except TimeoutError:
                    self._logger.warning('Signal %s could not be calibrated because no trigger was detected while sweeping the cavity before the expiration of a timeout of %.1e s!', self.name, 100.0 / self.lockbox.asg.frequency + scope.duration)
                    return (None, None, None)

                times = scope.times
                self.calibration_data._asg_phase = self.lockbox.asg.scopetriggerphase
                return (
                 curve1, curve2, times)
        except InsufficientResourceError:
            self._logger.warning('No free scopes left for sweep_acquire_zoom. ')
            return (None, None, None)

        return

    def calibrate(self, autosave=False):
        curve0, _ = super(HighFinesseInput, self).sweep_acquire()
        if curve0 is None:
            self._logger.warning('Aborting calibration because no scope is available...')
            return
        else:
            curve1, _, times = self.sweep_acquire_zoom(threshold=self.get_threshold(curve0))
            curve1 -= self.calibration_data._analog_offset
            self.calibration_data.get_stats_from_curve(curve1)
            self._logger.info('%s high-finesse calibration successful - Min: %.3f  Max: %.3f  Mean: %.3f  Rms: %.3f', self.name, self.calibration_data.min, self.calibration_data.max, self.calibration_data.mean, self.calibration_data.rms)
            self.lockbox._signal_launcher.input_calibrated.emit([self])
            if autosave:
                params = self.calibration_data.setup_attributes
                params['name'] = self.name + '_calibration'
                newcurve = self._save_curve(times, curve1, **params)
                self.calibration_data.curve = newcurve
                return newcurve
            return
            return

    def get_threshold_empirical(self, curve):
        """ returns a reasonable scope threshold for the interesting part of this curve """
        calibration_params = self.calibration_data.setup_attributes
        self.calibration_data.get_stats_from_curve(curve)
        threshold = self.expected_signal(1.0 * self.lockbox._unit_in_setpoint_unit('bandwidth'))
        self.calibration_data.setup_attributes = calibration_params
        return threshold

    def get_threshold_theoretical(self, curve):
        """ returns a reasonable scope threshold for the interesting part of this curve """
        calibration_params = self.calibration_data.setup_attributes
        self.calibration_data.get_stats_from_curve(curve)
        eta = max(0.0, min(self.lockbox.eta, 1.0))
        self.calibration_data.min = (1.0 - eta) * self.calibration_data.max
        threshold = self.expected_signal(1.0 * self.lockbox._unit_in_setpoint_unit('bandwidth'))
        self.calibration_data.setup_attributes = calibration_params
        return threshold

    get_threshold = get_threshold_empirical


class HighFinesseReflection(HighFinesseInput, FPReflection):
    """
    Reflection for a FabryPerot. The only difference with FPReflection is that
    acquire will be done in 2 steps (coarse, then fine)
    """


class HighFinesseTransmission(HighFinesseInput, FPTransmission):
    pass


class HighFinesseAnalogPdh(HighFinesseInput, FPAnalogPdh):

    def calibrate(self, trigger_signal='reflection', autosave=False):
        trigger_signal = self.lockbox.inputs[trigger_signal]
        curve0, _ = trigger_signal.sweep_acquire()
        if curve0 is None:
            self._logger.warning('Aborting calibration because no scope is available...')
            return
        else:
            curve1, curve2, times = trigger_signal.sweep_acquire_zoom(threshold=trigger_signal.get_threshold(curve0), input2=self.signal())
            curve1 -= trigger_signal.calibration_data._analog_offset
            curve2 -= self.calibration_data._analog_offset
            self.calibration_data.get_stats_from_curve(curve2)
            self.calibration_data._asg_phase = trigger_signal.calibration_data._asg_phase
            self._logger.info('%s high-finesse calibration successful - Min: %.3f  Max: %.3f  Mean: %.3f  Rms: %.3f', self.name, self.calibration_data.min, self.calibration_data.max, self.calibration_data.mean, self.calibration_data.rms)
            self.lockbox._signal_launcher.input_calibrated.emit([self])
            if autosave:
                params = self.calibration_data.setup_attributes
                params['name'] = self.name + '_calibration'
                newcurve = self._save_curve(times, curve2, **params)
                params = trigger_signal.calibration_data.setup_attributes
                params['name'] = trigger_signal.name + '_calibration'
                trigcurve = self._save_curve(times, curve1, **params)
                newcurve.add_child(trigcurve)
                self.calibration_data.curve = newcurve
                return newcurve
            return
            return


class HighFinessePdh(HighFinesseAnalogPdh, FPPdh):
    pass


class HighFinesseFabryPerot(FabryPerot):
    _setup_attributes = [
     'inputs', 'sequence']
    inputs = LockboxModuleDictProperty(transmission=HighFinesseTransmission, reflection=HighFinesseReflection, pdh=HighFinessePdh)