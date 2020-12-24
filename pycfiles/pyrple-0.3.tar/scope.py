# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/hardware_modules/scope.py
# Compiled at: 2017-08-29 09:44:06
import time
from .dsp import all_inputs, dsp_addr_base, InputSelectRegister
from ..acquisition_module import AcquisitionModule
from ..async_utils import MainThreadTimer, PyrplFuture, sleep
from ..pyrpl_utils import sorted_dict
from ..attributes import *
from ..modules import HardwareModule
from ..pyrpl_utils import time
from ..widgets.module_widgets import ScopeWidget
logger = logging.getLogger(name=__name__)
data_length = 16384

class DecimationRegister(SelectRegister):
    """
    Careful: changing decimation changes duration and sampling_time as well
    """

    def set_value(self, obj, value):
        SelectRegister.set_value(self, obj, value)
        obj.__class__.duration.value_updated(obj, obj.duration)
        obj.__class__.sampling_time.value_updated(obj, obj.sampling_time)


class DurationProperty(SelectProperty):

    def get_value(self, obj):
        return obj.sampling_time * float(obj.data_length)

    def validate_and_normalize(self, obj, value):
        value = float(value)
        options = self.options(obj).keys()
        try:
            return min([ opt for opt in options if opt >= value ], key=lambda x: abs(x - value))
        except ValueError:
            obj._logger.info('Selected duration is longer than physically possible with the employed hardware. Picking longest-possible value %s. ', max(options))
            return max(options)

    def set_value(self, obj, value):
        """sets returns the duration of a full scope sequence the rounding
        makes sure that the actual value is longer or equal to the set value"""
        obj.sampling_time = float(value) / obj.data_length


class SamplingTimeProperty(SelectProperty):

    def get_value(self, obj):
        return 8e-09 * float(obj.decimation)

    def validate_and_normalize(self, obj, value):
        value = float(value)
        options = self.options(obj).keys()
        try:
            return min([ opt for opt in options if opt <= value ], key=lambda x: abs(x - value))
        except ValueError:
            obj._logger.info('Selected sampling time is shorter than physically possible with the employed hardware. Picking shortest-possible value %s. ', min(options))
            return min(options)

    def set_value(self, instance, value):
        """sets or returns the time separation between two subsequent
        points of a scope trace the rounding makes sure that the actual
        value is shorter or equal to the set value"""
        instance.decimation = float(value) / 8e-09


class ContinuousRollingFuture(PyrplFuture):
    """
    This Future object is the one controlling the acquisition in
    rolling_mode. It will never be fullfilled (done), since rolling_mode
    is always continuous, but the timer/slot mechanism to control the
    rolling_mode acquisition is encapsulated in this object.
    """
    DELAY_ROLLING_MODE_MS = 20
    current_avg = 1

    def __init__(self, module):
        super(ContinuousRollingFuture, self).__init__()
        self._module = module
        self._timer = MainThreadTimer(self.DELAY_ROLLING_MODE_MS)
        self._timer.timeout.connect(self._get_rolling_curve)

    def _get_rolling_curve(self):
        if not self._module._is_rolling_mode_active():
            return
        if not self._module.running_state == 'running_continuous':
            return
        data_x, datas = self._module._get_rolling_curve()
        self._module._emit_signal_by_name('display_curve', [data_x,
         datas])
        self.data_avg = datas
        self.data_x = data_x
        self._timer.start()

    def start(self):
        self._module._start_acquisition_rolling_mode()
        self._timer.start()

    def pause(self):
        self._timer.stop()

    def _set_run_continuous(self):
        """
        Dummy function: ContinuousRollingFuture instance is always
        "_run_continuous"
        """
        pass


class Scope(HardwareModule, AcquisitionModule):
    addr_base = 1074790400
    name = 'scope'
    _widget_class = ScopeWidget
    _gui_attributes = [
     'input1',
     'input2',
     'duration',
     'average',
     'trigger_source',
     'trigger_delay',
     'threshold',
     'hysteresis',
     'ch1_active',
     'ch2_active',
     'xy_mode']
    _setup_attributes = _gui_attributes + ['rolling_mode', 'running_state']
    data_length = data_length
    rolling_mode = BoolProperty(default=True, doc='In rolling mode, the curve is continuously acquired and translated from the right to the left of the screen while new data arrive.', call_setup=True)

    @property
    def inputs(self):
        return list(all_inputs(self).keys())

    input1 = InputSelectRegister(-addr_base + dsp_addr_base('asg0') + 0, options=all_inputs, default='in1', ignore_errors=True, doc='selects the input signal of the module')
    input2 = InputSelectRegister(-addr_base + dsp_addr_base('asg1') + 0, options=all_inputs, default='in2', ignore_errors=True, doc='selects the input signal of the module')
    _reset_writestate_machine = BoolRegister(0, 1, doc='Set to True to reset writestate machine. Automatically goes back to false.')
    _trigger_armed = BoolRegister(0, 0, doc='Set to True to arm trigger')
    _trigger_sources = sorted_dict({'off': 0, 'immediately': 1, 
       'ch1_positive_edge': 2, 
       'ch1_negative_edge': 3, 
       'ch2_positive_edge': 4, 
       'ch2_negative_edge': 5, 
       'ext_positive_edge': 6, 
       'ext_negative_edge': 7, 
       'asg0': 8, 
       'asg1': 9, 
       'dsp': 10}, sort_by_values=True)
    trigger_sources = _trigger_sources.keys()
    _trigger_source_register = SelectRegister(4, doc='Trigger source', options=_trigger_sources)
    trigger_source = SelectProperty(default='immediately', options=_trigger_sources.keys(), doc="Trigger source for the scope. Use 'immediately' if no synchronisation is required. Trigger_source will be ignored in rolling_mode.", call_setup=True)
    _trigger_debounce = IntRegister(144, doc='Trigger debounce time [cycles]')
    trigger_debounce = FloatRegister(144, bits=20, norm=125000000.0, doc='Trigger debounce time [s]')
    threshold = FloatRegister(8, bits=14, norm=8192, doc='trigger threshold [volts]')
    hysteresis = FloatRegister(32, bits=14, norm=8192, doc='hysteresis for trigger [volts]')

    @property
    def threshold_ch1(self):
        self._logger.warning('The scope attribute "threshold_chx" is deprecated. Please use "threshold" instead!')
        return self.threshold

    @threshold_ch1.setter
    def threshold_ch1(self, v):
        self._logger.warning('The scope attribute "threshold_chx" is deprecated. Please use "threshold" instead!')
        self.threshold = v

    @property
    def threshold_ch2(self):
        self._logger.warning('The scope attribute "threshold_chx" is deprecated. Please use "threshold" instead!')
        return self.threshold

    @threshold_ch2.setter
    def threshold_ch2(self, v):
        self._logger.warning('The scope attribute "threshold_chx" is deprecated. Please use "threshold" instead!')
        self.threshold = v

    @property
    def hysteresis_ch1(self):
        self._logger.warning('The scope attribute "hysteresis_chx" is deprecated. Please use "hysteresis" instead!')
        return self.hysteresis

    @hysteresis_ch1.setter
    def hysteresis_ch1(self, v):
        self._logger.warning('The scope attribute "hysteresis_chx" is deprecated. Please use "hysteresis" instead!')
        self.hysteresis = v

    @property
    def hysteresis_ch2(self):
        self._logger.warning('The scope attribute "hysteresis_chx" is deprecated. Please use "hysteresis" instead!')
        return self.hysteresis

    @hysteresis_ch2.setter
    def hysteresis_ch2(self, v):
        self._logger.warning('The scope attribute "hysteresis_chx" is deprecated. Please use "hysteresis" instead!')
        self.hysteresis = v

    _trigger_delay_register = IntRegister(16, doc='number of decimated data after trigger written into memory [samples]')
    trigger_delay = FloatProperty(min=-10, max=8e-09 * 1073741824, doc="delay between trigger and acquisition start.\nnegative values down to -duration are allowed for pretrigger. In trigger_source='immediately', trigger_delay is ignored.", call_setup=True)
    _trigger_delay_running = BoolRegister(0, 2, doc='trigger delay running (register adc_dly_do)')
    _adc_we_keep = BoolRegister(0, 3, doc='Scope resets trigger automatically (adc_we_keep)')
    _adc_we_cnt = IntRegister(44, doc='Number of samles that have passed since trigger was armed (adc_we_cnt)')
    current_timestamp = LongRegister(348, bits=64, doc='An absolute counter ' + 'for the time [cycles]')
    trigger_timestamp = LongRegister(356, bits=64, doc='An absolute counter ' + 'for the trigger time [cycles]')
    _decimations = sorted_dict({2 ** n:2 ** n for n in range(0, 17)}, sort_by_values=True)
    decimations = _decimations.keys()
    decimation = DecimationRegister(20, doc='decimation factor', default=8192, options=_decimations, call_setup=True)
    sampling_times = [ 8e-09 * dec for dec in decimations ]
    sampling_time = SamplingTimeProperty(options=sampling_times)
    durations = [ st * data_length for st in sampling_times ]
    duration = DurationProperty(options=durations)
    _write_pointer_current = IntRegister(24, doc='current write pointer position [samples]')
    _write_pointer_trigger = IntRegister(28, doc='write pointer when trigger arrived [samples]')
    average = BoolRegister(40, 0, doc='Enables averaging during decimation if set to True')
    voltage_in1 = FloatRegister(340, bits=14, norm=8192, doc='in1 current value [volts]')
    voltage_in2 = FloatRegister(344, bits=14, norm=8192, doc='in2 current value [volts]')
    voltage_out1 = FloatRegister(356, bits=14, norm=8192, doc='out1 current value [volts]')
    voltage_out2 = FloatRegister(360, bits=14, norm=8192, doc='out2 current value [volts]')
    ch1_firstpoint = FloatRegister(65536, bits=14, norm=8192, doc='1 sample of ch1 data [volts]')
    ch2_firstpoint = FloatRegister(131072, bits=14, norm=8192, doc='1 sample of ch2 data [volts]')
    pretrig_ok = BoolRegister(364, 0, doc='True if enough data have been acquired to fill the pretrig buffer')
    ch1_active = BoolProperty(default=True, doc='should ch1 be displayed in the gui?')
    ch2_active = BoolProperty(default=True, doc='should ch2 be displayed in the gui?')
    xy_mode = BoolProperty(default=False, doc='in xy-mode, data are plotted vs the other channel (instead of time)')

    def _ownership_changed(self, old, new):
        """
        If the scope was in continuous mode when slaved, it has to stop!!
        """
        if new is not None:
            self.stop()
        return

    @property
    def _rawdata_ch1(self):
        """raw data from ch1"""
        x = np.array(self._reads(65536, self.data_length), dtype=np.int16)
        x[(x >= 8192)] -= 16384
        return x

    @property
    def _rawdata_ch2(self):
        """raw data from ch2"""
        x = np.array(self._reads(131072, self.data_length), dtype=np.int16)
        x[(x >= 8192)] -= 16384
        return x

    @property
    def _data_ch1(self):
        """ acquired (normalized) data from ch1"""
        return np.array(np.roll(self._rawdata_ch1, -(self._write_pointer_trigger + self._trigger_delay_register + 1)), dtype=np.float) / 8192

    @property
    def _data_ch2(self):
        """ acquired (normalized) data from ch2"""
        return np.array(np.roll(self._rawdata_ch2, -(self._write_pointer_trigger + self._trigger_delay_register + 1)), dtype=np.float) / 8192

    @property
    def _data_ch1_current(self):
        """ (unnormalized) data from ch1 while acquisition is still running"""
        return np.array(np.roll(self._rawdata_ch1, -(self._write_pointer_current + 1)), dtype=np.float) / 8192

    @property
    def _data_ch2_current(self):
        """ (unnormalized) data from ch2 while acquisition is still running"""
        return np.array(np.roll(self._rawdata_ch2, -(self._write_pointer_current + 1)), dtype=np.float) / 8192

    @property
    def times(self):
        duration = self.duration
        trigger_delay = self.trigger_delay
        if self.trigger_source != 'immediately':
            return np.linspace(trigger_delay - duration / 2.0, trigger_delay + duration / 2.0, self.data_length, endpoint=False)
        else:
            return np.linspace(0, duration, self.data_length, endpoint=False)

    def wait_for_pretrigger(self):
        """ sleeps until scope trigger is ready (buffer has enough new data)"""
        while not self.pretrig_ok:
            sleep(0.001)

    def curve_ready(self):
        """
        Returns True if new data is ready for transfer
        """
        return not self._trigger_armed and not self._trigger_delay_running and self._setup_called

    def _curve_acquiring(self):
        """
        Returns True if data is in the process of being acquired, i.e.
        waiting for trigger event or for acquisition of data after
        trigger event.
        """
        return (self._trigger_armed or self._trigger_delay_running) and self._setup_called

    def _get_ch(self, ch):
        if ch not in (1, 2):
            raise ValueError('channel should be 1 or 2, got ' + str(ch))
        if ch == 1:
            return self._data_ch1
        return self._data_ch2

    @property
    def data_x(self):
        return self.times

    def _get_curve(self):
        """
        Simply pack together channel 1 and channel 2 curves in a numpy array
        """
        return np.array((self._get_ch(1), self._get_ch(2)))

    def _remaining_time(self):
        """
        :returns curve duration - ellapsed duration since last setup() call.
        """
        return self.duration - (time() - self._last_time_setup)

    def _data_ready(self):
        """
        :return: True if curve is ready in the hardware, False otherwise.
        """
        return self.curve_ready()

    def _start_acquisition(self):
        """
        Start acquisition of a curve in rolling_mode=False
        """
        autosave_backup = self._autosave_active
        self._autosave_active = False
        self._setup_called = True
        self._reset_writestate_machine = True
        if self.trigger_source == 'immediately':
            self._trigger_delay_register = self.data_length
        else:
            delay = int(np.round(self.trigger_delay / self.sampling_time)) + self.data_length // 2
            if delay <= 0:
                delay = 1
            elif delay > 4294967295:
                delay = 4294967295
            self._trigger_delay_register = delay
        self._trigger_armed = True
        self._trigger_source_register = self.trigger_source
        self._autosave_active = autosave_backup
        self._last_time_setup = time()

    def _start_acquisition_rolling_mode(self):
        self._start_acquisition()
        self._trigger_source_register = 'off'
        self._trigger_armed = True

    def _rolling_mode_allowed(self):
        """
        Only if duration larger than 0.1 s
        """
        return self.duration > 0.1

    def _is_rolling_mode_active(self):
        """
        Rolling_mode property evaluates to True and duration larger than 0.1 s
        """
        return self.rolling_mode and self._rolling_mode_allowed()

    def _get_ch_no_roll(self, ch):
        if ch not in (1, 2):
            raise ValueError('channel should be 1 or 2, got ' + str(ch))
        if ch == 1:
            return self._rawdata_ch1 * 1.0 / 8192
        return self._rawdata_ch2 * 1.0 / 8192

    def _get_rolling_curve(self):
        datas = np.zeros((2, len(self.times)))
        wp0 = self._write_pointer_current
        times = self.times
        times -= times[(-1)]
        for ch, active in (
         (
          0, self.ch1_active),
         (
          1, self.ch2_active)):
            if active:
                datas[ch] = self._get_ch_no_roll(ch + 1)

        wp1 = self._write_pointer_current
        for index, active in [(0, self.ch1_active),
         (
          1, self.ch2_active)]:
            if active:
                data = datas[index]
                to_discard = (wp1 - wp0) % self.data_length
                data = np.roll(data, self.data_length - wp0)[to_discard:]
                data = np.concatenate([[np.nan] * to_discard, data])
                datas[index] = data

        return (
         times, datas)

    def save_curve(self):
        """
        Saves the curve(s) that is (are) currently displayed in the gui in
        the db_system. Also, returns the list [curve_ch1, curve_ch2]...
        """
        d = self.setup_attributes
        curves = [None, None]
        for ch, active in [(0, self.ch1_active),
         (
          1, self.ch2_active)]:
            if active:
                d.update({'ch': ch, 'name': self.curve_name + ' ch' + str(ch + 1)})
                curves[ch] = self._save_curve(self._run_future.data_x, self._run_future.data_avg[ch], **d)

        return curves

    def _new_run_future(self):
        if self._is_rolling_mode_active() and self.running_state == 'running_continuous':
            self._run_future.cancel()
            self._run_future = ContinuousRollingFuture(self)
        else:
            super(Scope, self)._new_run_future()