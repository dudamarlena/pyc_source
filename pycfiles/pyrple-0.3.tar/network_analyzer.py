# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/software_modules/network_analyzer.py
# Compiled at: 2017-08-29 09:44:06
from copy import copy
import numpy as np
from qtpy import QtWidgets
from ..async_utils import PyrplFuture, MainThreadTimer, CancelledError, sleep
from ..attributes import FloatProperty, SelectProperty, FrequencyProperty, IntProperty, BoolProperty, FilterProperty, SelectProperty, ProxyProperty
from ..hardware_modules import all_inputs, all_output_directs, InputSelectProperty
from ..modules import SignalModule
from ..acquisition_module import AcquisitionModule
from ..widgets.module_widgets import NaWidget
from ..hardware_modules.iq import Iq
import timeit

class NaAcBandwidth(FilterProperty):

    def valid_frequencies(self, obj):
        return [ -freq for freq in obj.iq.inputfilter_options if freq <= 0
               ]

    def get_value(self, obj):
        if obj is None:
            return self
        else:
            return -obj.iq.inputfilter

    def set_value(self, obj, value):
        if isinstance(value, list):
            value = value[0]
        obj.iq.inputfilter = -value
        return value


class NaAmplitudeProperty(FloatProperty):

    def validate_and_normalize(self, obj, value):
        return obj.iq.__class__.amplitude.validate_and_normalize(obj.iq, abs(value))


class RbwAttribute(FilterProperty):

    def get_value(self, instance):
        if instance is None:
            return self
        else:
            return instance.iq.bandwidth[0]

    def set_value(self, instance, val):
        try:
            val = list(val)
        except:
            val = [
             val, val]

        instance.iq.bandwidth = val
        return val

    def valid_frequencies(self, obj):
        return [ freq for freq in obj.iq.bandwidth_options if freq > 0 ]


class LogScaleProperty(BoolProperty):

    def set_value(self, module, val):
        super(LogScaleProperty, self).set_value(module, val)
        module._signal_launcher.x_log_toggled.emit()


class NaPointFuture(PyrplFuture):
    """
    Future object for a NetworkAnalyzer point.
    """

    def __init__(self, module, point_index, min_delay_ms=0):
        self._module = module
        self.point_index = point_index
        self._min_delay_ms = min_delay_ms
        super(NaPointFuture, self).__init__()
        self._init_timer()

    def _init_timer(self):
        self._module._start_point_acquisition(self.point_index)
        if self._min_delay_ms == 0:
            delay = self._module._remaining_time() * 1000 - 1
        else:
            delay = max(self._min_delay_ms, self._module._remaining_time() * 1000)
        self._timer = MainThreadTimer(max(0, delay))
        self._timer.timeout.connect(self._set_data_as_result)
        self._timer.start()

    def _set_data_as_result(self):
        if not self.done():
            point = self._module._get_point(self.point_index)
            if point is not None:
                self.set_result(point)
            else:
                self._timer.setInterval(self._min_delay_ms)
                self._timer.start()
        return

    def set_exception(self, exception):
        self._timer.stop()
        super(NaPointFuture, self).set_exception(exception)

    def cancel(self):
        self._timer.stop()
        super(NaPointFuture, self).cancel()


class NaCurveFuture(PyrplFuture):
    N_POINT_BENCHMARK = 100

    def __init__(self, module, min_delay_ms, autostart=True):
        self._module = module
        self._min_delay_ms = min_delay_ms
        self.current_point = 0
        self.current_avg = 0
        self.n_points = self._module.points
        self._paused = True
        self._fut = None
        self.never_started = True
        super(NaCurveFuture, self).__init__()
        self.data_x = copy(self._module._data_x)
        self.data_avg = np.empty(self.n_points, dtype=np.complex)
        self.data_avg.fill(np.nan)
        self.data_amp = np.empty(self.n_points)
        self.data_amp.fill(np.nan)
        self._reset_benchmark()
        self.measured_time_per_point = np.nan
        if autostart:
            self.start()
        return

    def start(self):
        self._time_first_point = timeit.default_timer()
        self._module._start_acquisition()
        self._module.iq.amplitude = self._module.amplitude
        if self.never_started:
            self._module._emit_signal_by_name('clear_curve')
            self.never_started = False
        self._paused = False
        self._setup_next_point()

    def _setup_next_point(self):
        self._fut = self._module._new_point_future(self.current_point, self._min_delay_ms)
        self._fut.add_done_callback(self._new_point_arrived)

    def pause(self):
        self._module.iq.amplitude = 0
        self._paused = True
        if self._fut is not None:
            self._fut.cancel()
        return

    def _reset_benchmark(self):
        self._last_time_benchmark = timeit.default_timer()
        self._current_points_benchmark = 0

    def _update_benchmark(self):
        self._current_points_benchmark += 1
        if self._current_points_benchmark >= self.N_POINT_BENCHMARK:
            current_time = timeit.default_timer()
            self.measured_time_per_point = (current_time - self._last_time_benchmark) / self._current_points_benchmark
            self._reset_benchmark()

    def _new_point_arrived(self, point):
        if self._paused:
            return
        self._update_benchmark()
        try:
            point = point.result()
        except CancelledError:
            self._point_cancelled()
            return

        self._add_point(point)
        if self._module.is_zero_span():
            if self.current_avg == 1:
                time_now = timeit.default_timer() - self._time_first_point
                self.data_x[self.current_point] = time_now
                self._module._data_x[self.current_point] = time_now
        self.current_point += 1
        if self.current_point == self.n_points:
            self._scan_finished()
        else:
            self._setup_next_point()

    def cancel(self):
        self.pause()
        super(NaCurveFuture, self).cancel()

    def _add_point(self, point):
        y, amp = point
        self.data_avg[self.current_point] = y
        self.data_amp[self.current_point] = amp

    def _point_cancelled(self):
        self.cancel()

    def _scan_finished(self):
        self.set_result(self.data_avg)
        self.pause()


class NaRunFuture(NaCurveFuture):

    def __init__(self, module, min_delay_ms):
        super(NaRunFuture, self).__init__(module, min_delay_ms, autostart=False)
        self._run_continuous = False

    def _add_point(self, point):
        y, amp = point
        index = self.current_point
        avg_value = self.data_avg[index]
        if np.isnan(avg_value):
            avg_value = 0
        self.data_avg[index] = (avg_value * self.current_avg + y) / (self.current_avg + 1)
        self.data_amp[index] = amp
        self._module._emit_signal_by_name('update_point', index)

    def _point_cancelled(self):
        pass

    def _scan_finished(self):
        self.current_avg = min(self.current_avg + 1, self._module.trace_average)
        self._module._emit_signal_by_name('scan_finished')
        if self._run_continuous or self.current_avg < self._module.trace_average:
            self._module._start_acquisition()
            self.current_point = 0
            self.start()
        if not self._run_continuous and self.current_avg == self._module.trace_average:
            self.set_result(self.data_avg)
            self.current_point = 0
            self._module.running_state = 'paused'

    def _set_run_continuous(self):
        self._run_continuous = True
        self._min_delay_ms = self._module.MIN_DELAY_CONTINUOUS_MS


class NetworkAnalyzer(AcquisitionModule, SignalModule):
    """
    Using an IQ module, the network analyzer can measure the complex coherent
    response between an output and any signal in the redpitaya.

    Three example ways on how to use the NetworkAnalyzer:

    - Example 1::

          r = RedPitaya("1.1.1.1")
          na = NetworkAnalyzer(r)
          curve = na.curve(start=100, stop=1000, rbw=10...)

    - Example 2::

          na.start = 100
          na.stop = 1000
          curve = na.curve(rbw=10)

    - Example 3::

          na.setup(start=100, stop=1000, ...)
          for freq, response, amplitude in na.values():
              print response
    """
    _widget_class = NaWidget
    _gui_attributes = ['input',
     'output_direct',
     'acbandwidth',
     'start_freq',
     'stop_freq',
     'rbw',
     'avg_per_point',
     'points',
     'amplitude',
     'logscale',
     'infer_open_loop_tf']
    _setup_attributes = _gui_attributes + ['running_state']
    trace_average = IntProperty(doc="number of curves to average in single mode. In continuous mode, a decaying average with a characteristic memory of 'trace_average' curves is performed.", default=10, min=1)
    input = InputSelectProperty(default='networkanalyzer', call_setup=True, ignore_errors=True)
    output_direct = SelectProperty(options=all_output_directs, default='off', call_setup=True)
    start_freq = FrequencyProperty(default=1000.0, call_setup=True, min=Iq.frequency.increment)
    stop_freq = FrequencyProperty(default=1000000.0, call_setup=True, min=Iq.frequency.increment)
    rbw = RbwAttribute(default=500.0, call_setup=True)
    avg_per_point = IntProperty(min=1, default=1, call_setup=True)
    amplitude = NaAmplitudeProperty(default=0.1, min=0, max=1, call_setup=True)
    points = IntProperty(min=1, max=100000000.0, default=1001, call_setup=True)
    logscale = LogScaleProperty(default=True, call_setup=True)
    infer_open_loop_tf = BoolProperty(default=False)
    acbandwidth = NaAcBandwidth(default=50.0, doc='Bandwidth of the input high-pass filter of the na.', call_setup=True)

    def __init__(self, parent, name=None):
        self._setup_attributes.remove('running_state')
        self._setup_attributes.append('running_state')
        self.sleeptimes = 0.5
        self._time_last_point = None
        self._data_x = None
        super(NetworkAnalyzer, self).__init__(parent, name=name)
        return

    def _load_setup_attributes(self):
        super(NetworkAnalyzer, self)._load_setup_attributes()
        if self.running_state in ('running_continuous', 'running_single'):
            self._logger.warning("Network analyzer is currently in the 'running' state, i.e. it is performing a measurement. If this is not desired, please call network_analyzer.stop() or click the corresponding GUI button!")

    @property
    def iq(self):
        """
        underlying iq module.
        """
        if not hasattr(self, '_iq'):
            self._iq = self.pyrpl.iqs.pop(owner=self.name)
            self.iq.bandwidth = [
             self.__class__.rbw.default, self.__class__.rbw.default]
            self.iq.inputfilter = -self.__class__.acbandwidth.default
        return self._iq

    @property
    def output_directs(self):
        return self.iq.output_directs

    @property
    def inputs(self):
        return self.iq.inputs

    def _time_per_point(self):
        return float(self.iq._na_sleepcycles + self.iq._na_averages) / (125000000.0 * self.iq._frequency_correction)

    def signal(self):
        return self.iq.signal()

    @property
    def current_freq(self):
        """
        current frequency during the scan
        """
        return self.iq.frequency

    _delay = 3.0

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
        module_delay = self._delay
        frequencies = np.array(np.array(frequencies, dtype=np.float), dtype=np.complex)
        tf = np.array(frequencies * 0, dtype=np.complex) + 1.0
        f = self.iq.inputfilter
        if f > 0:
            tf /= 1.0 + complex(0.0, 1.0) * frequencies / f
            module_delay += 2
        elif f < 0:
            tf /= 1.0 + complex(0.0, 1.0) * f / frequencies
            module_delay += 1
        delay = module_delay * 8e-09 / self.iq._frequency_correction + extradelay
        tf *= np.exp(complex(0.0, -1.0) * delay * frequencies * 2 * np.pi)
        return tf

    def threshold_hook(self, current_val):
        """
        A convenience function to stop the run upon some condition
        (such as reaching of a threshold. current_val is the complex amplitude
        of the last data point).

        To be overwritten in derived class...
        Parameters
        ----------
        current_val

        Returns
        -------

        """
        pass

    MIN_DELAY_SINGLE_MS = 0
    MIN_DELAY_CONTINUOUS_MS = 0
    _curve_future_cls = NaCurveFuture
    _run_future_cls = NaRunFuture

    def _new_run_future_obsolete(self):
        assert self.running_state in ('running_single', 'running_continuous'), 'Run future cannot be created in state %s' % self.running_state
        self._run_future.cancel()
        if self.running_state == 'running_continuous':
            self._run_future = NaRunFuture(self, min_delay_ms=self.MIN_DELAY_CONTINUOUS_MS)
            self._run_future._set_run_continuous()
        if self.running_state == 'running_single':
            self._run_future = NaRunFuture(self, min_delay_ms=self.MIN_DELAY_SINGLE_MS)

    def _get_new_curve_future(self, min_delay_ms):
        return NaCurveFuture(self, min_delay_ms)

    def _new_point_future(self, index, min_delay_ms):
        if hasattr(self, '_point_future'):
            self._point_future.cancel()
        self._point_future = NaPointFuture(self, index, min_delay_ms)
        return self._point_future

    def is_zero_span(self):
        """
        Returns true if start_freq is the same as stop_freq.
        """
        return self.start_freq == self.stop_freq

    def _start_point_acquisition(self, index):
        if not self.is_zero_span():
            self.iq.frequency = self._data_x[index]
        else:
            self.iq.frequency = self.start_freq
        self._time_last_point = timeit.default_timer()

    def _get_point(self, index):
        if self._remaining_time() > 0:
            return None
        else:
            y = self.iq._nadata_total / self._cached_na_averages
            x = self._data_x[index]
            tf = self._tf_values[index]
            amp = self.amplitude
            if amp == 0:
                y *= self._rescale
            else:
                y *= self._rescale / amp
            y /= tf
            return (
             y, amp)

    def take_ringdown(self, frequency, rbw=1000, points=1000, trace_average=1):
        self.start_freq = frequency
        self.stop_freq = frequency
        self.rbw = rbw
        self.points = points
        self.trace_average = trace_average
        curve = self.single_async()
        sleep(0.1)
        self.iq.output_direct = 'off'
        self._time_first_point = timeit.default_timer()
        res = curve.await_result()
        x = self._run_future.data_x - self._time_first_point
        return [
         x, res]

    def _start_acquisition(self):
        """
        For the NA, resuming (from pause to start for instance... should
        not setup the instrument again, otherwise, this would restart at
        the beginning of the curve)
        Moreover, iq is disabled even when na is just paused.
        :return:
        """
        x = (self.is_zero_span() or self)._data_x if 1 else self.start_freq * np.ones(self.points)
        self.iq.setup(frequency=x[0], bandwidth=self.rbw, gain=0, phase=0, acbandwidth=self.acbandwidth, amplitude=self.amplitude, input=self.input, output_direct=self.output_direct, output_signal='output_direct')
        self.iq._na_averages = np.int(np.round(125000000.0 / self.rbw * self.avg_per_point))
        self._cached_na_averages = self.iq._na_averages
        self.iq._na_sleepcycles = np.int(np.round(125000000.0 / self.rbw * self.sleeptimes))
        self.time_per_point = self._time_per_point()
        self._rescale = 2.0 ** (-self.iq._LPFBITS) * 4.0
        self.iq.frequency = x[0]
        self._time_last_point = timeit.default_timer()
        self._tf_values = self.transfer_function(x)
        self.iq.on = True
        if self.time_per_point < 0.001:
            self._logger.info("Time between successive points is %.1f ms. You should increase 'avg_per_point' to at least %i for efficient acquisition.", self.time_per_point * 1000, self.avg_per_point * 0.001 / self.time_per_point)

    def _stop_acquisition(self):
        """
        Stop the iq.
        """
        self.iq.output_direct = 'off'

    @property
    def data_x(self):
        """
        x-data for the network analyzer are computed during setup() and cached
        in the variable _data_x.
        """
        return self._data_x

    @property
    def frequencies(self):
        """
        alias for data_x

        :return: frequency array
        """
        return self.data_x

    def _update_data_x(self):
        if self.is_zero_span():
            self._data_x = np.zeros(self.points)
            return
        if self.logscale:
            raw_values = np.logspace(np.log10(self.start_freq), np.log10(self.stop_freq), self.points, endpoint=True)
        else:
            raw_values = np.linspace(self.start_freq, self.stop_freq, self.points, endpoint=True)
        values = np.zeros(len(raw_values))
        for index, val in enumerate(raw_values):
            values[index] = self.iq.__class__.frequency.validate_and_normalize(self, val)

        self._data_x = values

    def _remaining_time(self):
        """Remaining time in seconds until current point is ready"""
        if self.current_point == 0:
            time_per_point = 3 * self.time_per_point
        else:
            time_per_point = self.time_per_point
        return time_per_point - (timeit.default_timer() - self._time_last_point)

    @property
    def last_valid_point(self):
        if self.current_avg >= 1:
            return self.points - 1
        else:
            return self.current_point

    @property
    def current_point(self):
        return self._run_future.current_point

    @property
    def measured_time_per_point(self):
        return self._run_future.measured_time_per_point

    def _setup(self):
        self._update_data_x()
        super(NetworkAnalyzer, self)._setup()

    @property
    def data_avg(self):
        return self._run_future.data_avg

    @property
    def last_valid_point(self):
        if self._run_future.current_avg <= 1:
            return self._run_future.current_point
        return self.points