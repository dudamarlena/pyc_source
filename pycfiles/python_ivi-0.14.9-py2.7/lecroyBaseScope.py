# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ivi/lecroy/lecroyBaseScope.py
# Compiled at: 2014-09-01 23:09:59
"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2014 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""
import time, struct
from .. import ivi
from .. import scope
from .. import scpi
from .. import extra
AcquisitionTypeMapping = {'normal': 'norm', 
   'peak_detect': 'peak', 
   'high_resolution': 'hres', 
   'average': 'aver'}
VerticalCoupling = set(['ac', 'dc', 'gnd'])
InputImpedance = set([1000000, 50, 'gnd'])
BandwidthLimit = set(['OFF', 'ON', '200MHZ'])
TriggerModes = set(['auto', 'norm', 'single', 'stop'])
TriggerTypes = set([
 'drop', 'edge', 'ev', 'glit', 'ht', 'hv', 'hv2', 'il', 'intv', 'is', 'i2', 'off', 'pl', 'ps', 'p2', 'ql', 'sng',
 'sq', 'sr', 'teq', 'ti', 'tl'])
TriggerCouplingMapping = {'ac': ('ac', 0, 0), 
   'dc': ('dc', 0, 0), 
   'hf_reject': ('dc', 0, 1), 
   'lf_reject': ('lfr', 0, 0), 
   'noise_reject': ('dc', 1, 0), 
   'hf_reject_ac': ('ac', 0, 1), 
   'noise_reject_ac': ('ac', 1, 0), 
   'hf_noise_reject': ('dc', 1, 1), 
   'hf_noise_reject_ac': ('ac', 1, 1), 
   'lf_noise_reject': ('lfr', 1, 0)}
TVTriggerEventMapping = {'field1': 'fie1', 'field2': 'fie2', 
   'any_field': 'afi', 
   'any_line': 'alin', 
   'line_number': 'lfi1', 
   'vertical': 'vert', 
   'line_field1': 'lfi1', 
   'line_field2': 'lfi2', 
   'line': 'line', 
   'line_alternate': 'lalt', 
   'lvertical': 'lver'}
TVTriggerFormatMapping = {'generic': 'gen', 'ntsc': 'ntsc', 
   'pal': 'pal', 
   'palm': 'palm', 
   'secam': 'sec', 
   'p480l60hz': 'p480', 
   'p480': 'p480', 
   'p720l60hz': 'p720', 
   'p720': 'p720', 
   'p1080l24hz': 'p1080', 
   'p1080': 'p1080', 
   'p1080l25hz': 'p1080l25hz', 
   'p1080l50hz': 'p1080l50hz', 
   'p1080l60hz': 'p1080l60hz', 
   'i1080l50hz': 'i1080l50hz', 
   'i1080': 'i1080l50hz', 
   'i1080l60hz': 'i1080l60hz'}
PolarityMapping = {'positive': 'pos', 'negative': 'neg'}
GlitchConditionMapping = {'less_than': 'less', 'greater_than': 'gre'}
WidthConditionMapping = {'within': 'rang'}
SampleModeMapping = {'real_time': 'rtim', 'equivalent_time': 'etim'}
SlopeMapping = {'positive': 'pos', 
   'negative': 'neg', 
   'either': 'eith', 
   'alternating': 'alt'}
MeasurementFunctionMapping = {'rise_time': 'risetime', 
   'fall_time': 'falltime', 
   'frequency': 'frequency', 
   'period': 'period', 
   'voltage_rms': 'vrms display', 
   'voltage_peak_to_peak': 'vpp', 
   'voltage_max': 'vmax', 
   'voltage_min': 'vmin', 
   'voltage_high': 'vtop', 
   'voltage_low': 'vbase', 
   'voltage_average': 'vaverage display', 
   'width_negative': 'nwidth', 
   'width_positive': 'pwidth', 
   'duty_cycle_positive': 'dutycycle', 
   'amplitude': 'vamplitude', 
   'voltage_cycle_rms': 'vrms cycle', 
   'voltage_cycle_average': 'vaverage cycle', 
   'overshoot': 'overshoot', 
   'preshoot': 'preshoot', 
   'ratio': 'vratio', 
   'phase': 'phase', 
   'delay': 'delay'}
MeasurementFunctionMappingDigital = {'rise_time': 'risetime', 
   'fall_time': 'falltime', 
   'frequency': 'frequency', 
   'period': 'period', 
   'width_negative': 'nwidth', 
   'width_positive': 'pwidth', 
   'duty_cycle_positive': 'dutycycle'}
ScreenshotImageFormatMapping = {'bmp': 'bmp', 
   'bmp24': 'bmp', 
   'bmp8': 'bmpcomp', 
   'jpeg': 'jpeg', 
   'png': 'png', 
   'png24': 'png', 
   'psd': 'psd', 
   'tiff': 'tiff'}
TimebaseModeMapping = {'main': 'main', 
   'window': 'wind', 
   'xy': 'xy', 
   'roll': 'roll'}
TimebaseReferenceMapping = {'left': 'left', 
   'center': 'cent', 
   'right': 'righ'}

class lecroyBaseScope(scpi.common.IdnCommand, scpi.common.ErrorQuery, scpi.common.Reset, scpi.common.SelfTest, scpi.common.Memory, scope.Base, scope.TVTrigger, scope.GlitchTrigger, scope.WidthTrigger, scope.AcLineTrigger, scope.WaveformMeasurement, scope.MinMaxWaveform, scope.ContinuousAcquisition, scope.AverageAcquisition, scope.SampleMode, scope.AutoSetup, extra.common.SystemSetup, extra.common.Screenshot, ivi.Driver):
    """LeCroy generic IVI oscilloscope driver"""

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._channel_label = list()
        self._channel_label_position = list()
        self._channel_noise_filter = list()
        self._channel_interpolation = list()
        self._channel_probe_skew = list()
        self._channel_invert = list()
        self._channel_probe_id = list()
        self._channel_bw_limit = list()
        super(lecroyBaseScope, self).__init__(*args, **kwargs)
        self._memory_size = 5
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 1000000000.0
        self._horizontal_divisions = 10
        self._vertical_divisions = 8
        self._timebase_mode = 'main'
        self._timebase_reference = 'center'
        self._timebase_position = 0.0
        self._timebase_range = 0.001
        self._timebase_scale = 0.0001
        self._timebase_window_position = 0.0
        self._timebase_window_range = 5e-06
        self._timebase_window_scale = 5e-07
        self._trigger_mode = 'auto'
        self._trigger_type = 'edge'
        self._display_vectors = True
        self._display_labels = True
        self._display_grid = 'single'
        self._identity_description = 'LeCroy generic IVI oscilloscope driver'
        self._identity_identifier = ''
        self._identity_revision = ''
        self._identity_vendor = ''
        self._identity_instrument_manufacturer = 'LeCroy'
        self._identity_instrument_model = ''
        self._identity_instrument_firmware_revision = ''
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = ['WR204MXI-A', 'WR204XI-A', 'WR104MXI-A', 'WR104XI-A', 'WR64MXI-A',
         'WR64XI-A',
         'WR62XI-A', 'WR44MXI-A', 'WR44XI-A']
        self._write('CHDR OFF')
        self._add_property('channels[].bw_limit', self._get_channel_bw_limit, self._set_channel_bw_limit, None, ivi.Doc('\n                        Commands an internal low-pass filter.  When the filter is on, the\n                        bandwidth of the channel is limited to approximately 20 MHz.\n                        '))
        self._add_property('channels[].invert', self._get_channel_invert, self._set_channel_invert, None, ivi.Doc('\n                        Selects whether or not to invert the channel.\n                        '))
        self._add_property('channels[].label', self._get_channel_label, self._set_channel_label, None, ivi.Doc("\n                        Sets the channel label.  Setting a channel label also adds the label to\n                        the nonvolatile label list. Setting the label will turn it's display on.\n                        "))
        self._add_property('channels[].label_position', self._get_channel_label_position, self._set_channel_label_position, None, ivi.Doc('\n                        Set the channel label positions\n                        '))
        self._add_property('channels[].probe_skew', self._get_channel_probe_skew, self._set_channel_probe_skew, None, ivi.Doc('\n                        Specifies the channel-to-channel skew factor for the channel.  Each analog\n                        channel can be adjusted + or - 100 ns for a total of 200 ns difference\n                        between channels.  This can be used to compensate for differences in cable\n                        delay.  Units are seconds.\n                        '))
        self._add_property('channels[].scale', self._get_channel_scale, self._set_channel_scale, None, ivi.Doc('\n                        Specifies the vertical scale, or units per division, of the channel.  Units\n                        are volts.\n                        '))
        self._add_property('channels[].trigger_level', self._get_channel_trigger_level, self._set_channel_trigger_level, None, ivi.Doc('\n                        Specifies the voltage threshold for the trigger sub-system. The units are\n                        volts. This attribute affects instrument behavior only when the Trigger\n                        Type is set to one of the following values: Edge Trigger, Glitch Trigger,\n                        or Width Trigger.\n\n                        This attribute, along with the Trigger Slope, Trigger Source, and Trigger\n                        Coupling attributes, defines the trigger event when the Trigger Type is\n                        set to Edge Trigger.\n                        '))
        self._add_property('timebase.mode', self._get_timebase_mode, self._set_timebase_mode, None, ivi.Doc("\n                        Sets the current time base. There are four time base modes:\n\n                        * 'main': normal timebase\n                        * 'window': zoomed or delayed timebase\n                        * 'xy': channels are plotted against each other, no timebase\n                        * 'roll': data moves continuously from left to right\n                        "))
        self._add_property('timebase.reference', self._get_timebase_reference, self._set_timebase_reference, None, ivi.Doc("\n                        Sets the time reference to one division from the left side of the screen,\n                        to the center of the screen, or to one division from the right side of the\n                        screen. Time reference is the point on the display where the trigger point\n                        is referenced.\n                        \n                        Values:\n                        * 'left'\n                        * 'center'\n                        * 'right'\n                        "))
        self._add_property('timebase.position', self._get_timebase_position, self._set_timebase_position, None, ivi.Doc('\n                        Sets the time interval between the trigger event and the display reference\n                        point on the screen. The display reference point is either left, right, or\n                        center and is set with the timebase.reference property. The maximum\n                        position value depends on the time/division settings.\n                        '))
        self._add_property('timebase.range', self._get_timebase_range, self._set_timebase_range, None, ivi.Doc('\n                        Sets the full-scale horizontal time in seconds for the main window. The\n                        range is 10 times the current time-per-division setting.\n                        '))
        self._add_property('timebase.scale', self._get_timebase_scale, self._set_timebase_scale, None, ivi.Doc('\n                        Sets the horizontal scale or units per division for the main window.\n                        '))
        self._add_property('timebase.window.position', self._get_timebase_window_position, self._set_timebase_window_position, None, ivi.Doc('\n                        Sets the horizontal position in the zoomed (delayed) view of the main\n                        sweep. The main sweep range and the main sweep horizontal position\n                        determine the range for this command. The value for this command must\n                        keep the zoomed view window within the main sweep range.\n                        '))
        self._add_property('timebase.window.range', self._get_timebase_window_range, self._set_timebase_window_range, None, ivi.Doc('\n                        Sets the fullscale horizontal time in seconds for the zoomed (delayed)\n                        window. The range is 10 times the current zoomed view window seconds per\n                        division setting. The main sweep range determines the range for this\n                        command. The maximum value is one half of the timebase.range value.\n                        '))
        self._add_property('timebase.window.scale', self._get_timebase_window_scale, self._set_timebase_window_scale, None, ivi.Doc('\n                        Sets the zoomed (delayed) window horizontal scale (seconds/division). The\n                        main sweep scale determines the range for this command. The maximum value\n                        is one half of the timebase.scale value.\n                        '))
        self._add_property('display.vectors', self._get_display_vectors, self._set_display_vectors, None, ivi.Doc('\n                        When enabled, draws a line between consecutive waveform data points.\n                        '))
        self._add_property('display.grid', self._get_grid_mode, self._set_grid_mode, None, ivi.Doc("\n                        Sets the current grid used in the display. There are multiple grid modes.\n\n                        Values:\n                        * 'single'\n                        * 'dual'\n                        * 'quad'\n                        * 'octal'\n                        * 'auto'\n                        * 'xy'\n                        * 'xysingle'\n                        * 'xydual'\n                        "))
        self._add_property('trigger.mode', self._get_trigger_mode, self._set_trigger_mode, None, ivi.Doc("\n                        Specifies the trigger mode of the oscilloscope.\n\n                        Values:\n                        'auto', 'norm', 'single', 'stop'\n                        * 'auto'\n                        * 'norm'\n                        * 'single'\n                        * 'stop'\n                        "))
        self._add_method('system.fetch_setup', self._system_fetch_setup, ivi.Doc('\n                        Returns the current oscilloscope setup in the form of a binary block.  The\n                        setup can be stored in memory or written to a file and then reloaded to the\n                        oscilloscope at a later time with system.load_setup.\n                        '))
        self._add_method('system.load_setup', self._system_load_setup, ivi.Doc('\n                        Transfers a binary block of setup data to the scope to reload a setup\n                        previously saved with system.fetch_setup.\n                        '))
        self._add_method('system.display_string', self._system_display_string, ivi.Doc('\n                        Writes a string to the advisory line on the instrument display.  Send None\n                        or an empty string to clear the advisory line.  \n                        '))
        self._add_method('display.fetch_screenshot', self._display_fetch_screenshot, ivi.Doc('\n                        Captures the oscilloscope screen and transfers it in the specified format.\n                        The display graticule is optionally inverted.\n                        '))
        self._add_method('memory.save', self._memory_save, ivi.Doc('\n                        Stores the current state of the instrument into an internal storage\n                        register.  Use memory.recall to restore the saved state.\n                        '))
        self._add_method('memory.recall', self._memory_recall, ivi.Doc('\n                        Recalls the state of the instrument from an internal storage register\n                        that was previously saved with memory.save.\n                        '))
        self._init_channels()
        return

    def initialize(self, resource=None, id_query=False, reset=False, **keywargs):
        """Opens an I/O session to the instrument."""
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        super(lecroyBaseScope, self).initialize(resource, id_query, reset, **keywargs)
        if not self._driver_operation_simulate:
            self._clear()
        if id_query and not self._driver_operation_simulate:
            id = self.identity.instrument_model
            id_check = self._instrument_id
            id_short = id[:len(id_check)]
            if id_short != id_check:
                raise Exception('Instrument ID mismatch, expecting %s, got %s', id_check, id_short)
        if reset:
            self.utility.reset()

    def _load_id_string(self):
        if self._driver_operation_simulate:
            self._identity_instrument_manufacturer = 'Not available while simulating'
            self._identity_instrument_model = 'Not available while simulating'
            self._identity_instrument_firmware_revision = 'Not available while simulating'
        else:
            lst = self._ask('*IDN?').split(',')
            self._identity_instrument_manufacturer = lst[0]
            self._identity_instrument_model = lst[1]
            self._identity_instrument_firmware_revision = lst[3]
            self._set_cache_valid(True, 'identity_instrument_manufacturer')
            self._set_cache_valid(True, 'identity_instrument_model')
            self._set_cache_valid(True, 'identity_instrument_firmware_revision')

    def _get_identity_instrument_manufacturer(self):
        if self._get_cache_valid():
            return self._identity_instrument_manufacturer
        self._load_id_string()
        return self._identity_instrument_manufacturer

    def _get_identity_instrument_model(self):
        if self._get_cache_valid():
            return self._identity_instrument_model
        self._load_id_string()
        return self._identity_instrument_model

    def _get_identity_instrument_firmware_revision(self):
        if self._get_cache_valid():
            return self._identity_instrument_firmware_revision
        self._load_id_string()
        return self._identity_instrument_firmware_revision

    def _utility_disable(self):
        pass

    def _utility_error_query(self):
        error_code = 0
        error_message = 'No error'
        if not self._driver_operation_simulate:
            error_code, error_message = self._ask(':system:error?').split(',')
            error_code = int(error_code)
            error_message = error_message.strip(' "')
        return (
         error_code, error_message)

    def _utility_lock_object(self):
        pass

    def _utility_reset(self):
        if not self._driver_operation_simulate:
            self._write('*RST')
            self.driver_operation.invalidate_all_attributes()

    def _utility_reset_with_defaults(self):
        self._utility_reset()

    def _utility_self_test(self):
        code = 0
        message = 'Self test passed'
        if not self._driver_operation_simulate:
            self._write('*TST?')
            time.sleep(40)
            code = int(self._read())
            if code != 0:
                message = 'Self test failed'
        return (
         code, message)

    def _utility_unlock_object(self):
        pass

    def _init_channels(self):
        try:
            super(lecroyBaseScope, self)._init_channels()
        except AttributeError:
            pass

        self._channel_name = list()
        self._channel_label = list()
        self._channel_label_position = list()
        self._channel_noise_filter = list()
        self._channel_interpolation = list()
        self._channel_probe_skew = list()
        self._channel_invert = list()
        self._channel_probe_id = list()
        self._channel_bw_limit = list()
        self._channel_input_impedance = list()
        self._channel_trigger_level = list()
        self._analog_channel_name = list()
        for i in range(self._analog_channel_count):
            self._channel_name.append('C%d' % (i + 1))
            self._channel_label.append('%d' % (i + 1))
            self._channel_label_position.append(0)
            self._channel_noise_filter.append('None')
            self._channel_interpolation.append('Linear')
            self._analog_channel_name.append('C%d' % (i + 1))
            self._channel_probe_skew.append(0)
            self._channel_invert.append(False)
            self._channel_probe_id.append('NONE')
            self._channel_bw_limit.append(False)
            self._channel_coupling.append('NONE')
            self._channel_input_impedance.append(0)
            self._channel_trigger_level.append(0)

        self._digital_channel_name = list()
        if self._digital_channel_count > 0:
            for i in range(self._digital_channel_count):
                self._channel_name.append('digital%d' % i)
                self._channel_label.append('D%d' % i)
                self._digital_channel_name.append('digital%d' % i)

            for i in range(self._analog_channel_count, self._channel_count):
                self._channel_input_frequency_max[i] = 1000000000.0
                self._channel_probe_attenuation[i] = 1
                self._channel_offset[i] = 0
                self._channel_range[i] = 1

        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self.channels._set_list(self._channel_name)

    def _system_fetch_setup(self):
        if self._driver_operation_simulate:
            return ''
        self._write(':system:setup?')
        return self._read_ieee_block()

    def _system_load_setup(self, data):
        if self._driver_operation_simulate:
            return
        self._write_ieee_block(data, ':system:setup ')
        self.driver_operation.invalidate_all_attributes()

    def _system_display_string(self, string=None):
        if string is None:
            string = ''
        if not self._driver_operation_simulate:
            self._write('MESSAGE "%s"' % string)
        return

    def _display_fetch_screenshot(self, format='png', invert=True):
        if self._driver_operation_simulate:
            return ''
        if format not in ScreenshotImageFormatMapping:
            raise ivi.ValueNotSupportedException()
        format = ScreenshotImageFormatMapping[format]
        if invert == False:
            color = 'BLACK'
        elif invert == True:
            color = 'WHITE'
        else:
            color = 'WHITE'
        self._write('HCSU DEV,%s,FORMAT,PORTRAIT,BCKG,%s,DEST,"REMOTE",PORT,"NET",AREA,GRIDAREAONLY' % (str(format), color))
        self._write('SCDP')
        return self._read_raw()

    def _get_timebase_mode(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(':timebase:mode?').lower()
            self._timebase_mode = [ k for k, v in TimebaseModeMapping.items() if v == value ][0]
            self._set_cache_valid
        return self._timebase_mode

    def _set_timebase_mode(self, value):
        if value not in TimebaseModeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(':timebase:mode %s' % TimebaseModeMapping[value])
        self._timebase_mode = value
        self._set_cache_valid()

    def _get_timebase_reference(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(':timebase:reference?').lower()
            self._timebase_reference = [ k for k, v in TimebaseReferenceMapping.items() if v == value ][0]
            self._set_cache_valid
        return self._timebase_reference

    def _set_timebase_reference(self, value):
        if value not in TimebaseReferenceMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(':timebase:reference %s' % TimebaseReferenceMapping[value])
        self._timebase_reference = value
        self._set_cache_valid()

    def _get_timebase_position(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_position = float(self._ask(':timebase:position?'))
            self._set_cache_valid()
        return self._timebase_position

    def _set_timebase_position(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(':timebase:position %e' % value)
        self._timebase_position = value
        self._set_cache_valid()

    def _get_timebase_range(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_scale = float(self._ask('TDIV?'))
            self._timebase_range = self._timebase_scale * self._horizontal_divisions
            self._set_cache_valid()
            self._set_cache_valid(True, 'timebase_scale')
        return self._timebase_range

    def _set_timebase_range(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write('TDIV %e' % (value / self._horizontal_divisions))
        self._timebase_scale = value / self._horizontal_divisions
        self._timebase_range = value
        self._set_cache_valid()
        self._set_cache_valid(True, 'timebase_scale')

    def _get_timebase_scale(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_scale = float(self._ask('TDIV?'))
            self._timebase_range = self._timebase_scale * self._horizontal_divisions
            self._set_cache_valid()
            self._set_cache_valid(True, 'timebase_range')
        return self._timebase_scale

    def _set_timebase_scale(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write('TDIV %e' % value)
        self._timebase_scale = value
        self._timebase_range = value * self._horizontal_divisions
        self._set_cache_valid()
        self._set_cache_valid(True, 'timebase_range')

    def _get_timebase_window_position(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_window_position = float(self._ask(':timebase:window:position?'))
            self._set_cache_valid()
        return self._timebase_window_position

    def _set_timebase_window_position(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(':timebase:window:position %e' % value)
        self._timebase_window_position = value
        self._set_cache_valid()

    def _get_timebase_window_range(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_window_range = float(self._ask(':timebase:window:range?'))
            self._timebase_window_scale = self._timebase_window_range / self._horizontal_divisions
            self._set_cache_valid()
            self._set_cache_valid(True, 'timebase_window_scale')
        return self._timebase_window_range

    def _set_timebase_window_range(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(':timebase:window:range %e' % value)
        self._timebase_window_range = value
        self._timebase_window_scale = value / self._horizontal_divisions
        self._set_cache_valid()
        self._set_cache_valid(True, 'timebase_window_scale')

    def _get_timebase_window_scale(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_window_scale = float(self._ask(':timebase:window:scale?'))
            self._timebase_window_range = self._timebase_window_scale * self._horizontal_divisions
            self._set_cache_valid()
            self._set_cache_valid(True, 'timebase_window_range')
        return self._timebase_window_scale

    def _set_timebase_window_scale(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(':timebase:window:scale %e' % value)
        self._timebase_window_scale = value
        self._timebase_window_range = value * self._horizontal_divisions
        self._set_cache_valid()
        self._set_cache_valid(True, 'timebase_window_range')

    def _get_display_vectors(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._display_vectors = bool(int(self._ask(':display:vectors?')))
            self._set_cache_valid()
        return self._display_vectors

    def _set_display_vectors(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(':display:vectors %d' % int(value))
        self._display_vectors = value
        self._set_cache_valid()

    def _get_grid_mode(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._display_vectors = str(self._ask('GRID?'))
            self._set_cache_valid()
        return self._display_vectors

    def _set_grid_mode(self, value):
        if not self._driver_operation_simulate:
            self._write('GRID %s' % str(value))
        self._display_vectors = str(value)
        self._set_cache_valid()

    def _get_acquisition_start_time(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_start_time = float(self._ask(':waveform:xorigin?'))
            self._set_cache_valid()
        return self._acquisition_start_time

    def _set_acquisition_start_time(self, value):
        value = float(value)
        value = value + self._get_acquisition_time_per_record() * 5 / 10
        if not self._driver_operation_simulate:
            self._write(':timebase:position %e' % value)
        self._acquisition_start_time = value
        self._set_cache_valid()

    def _get_acquisition_type(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(':acquire:type?').lower()
            self._acquisition_type = [ k for k, v in AcquisitionTypeMapping.items() if v == value ][0]
            self._set_cache_valid()
        return self._acquisition_type

    def _set_acquisition_type(self, value):
        if value not in AcquisitionTypeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(':acquire:type %s' % AcquisitionTypeMapping[value])
        self._acquisition_type = value
        self._set_cache_valid()

    def _get_acquisition_number_of_points_minimum(self):
        return self._acquisition_number_of_points_minimum

    def _set_acquisition_number_of_points_minimum(self, value):
        value = int(value)
        self._acquisition_number_of_points_minimum = value

    def _get_acquisition_record_length(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_record_length = float(self._ask('MSIZ?'))
            self._set_cache_valid()
        return self._acquisition_record_length

    def _get_acquisition_time_per_record(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_time_per_record = float(self._ask('TDIV?')) * self._horizontal_divisions
            self._set_cache_valid()
        return self._acquisition_time_per_record

    def _set_acquisition_time_per_record(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write('TDIV %e' % (value / self._horizontal_divisions))
        self._acquisition_time_per_record = value * self._horizontal_divisions
        self._set_cache_valid()
        self._set_cache_valid(False, 'acquisition_start_time')

    def _get_channel_label(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_label[index] = self._ask(':%s:label?' % self._channel_name[index]).strip('"')
            self._set_cache_valid(index=index)
        return self._channel_label[index]

    def _set_channel_label(self, index, value):
        value = str(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write(':%s:label "%s"' % (self._channel_name[index], value))
        self._channel_label[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_enabled(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            trace = self._ask('%s:TRA?' % self._channel_name[index])
            if trace == 'ON':
                self._channel_enabled[index] = True
            elif trace == 'OFF':
                self._channel_enabled[index] = False
            self._set_cache_valid(index=index)
        return self._channel_enabled[index]

    def _set_channel_enabled(self, index, value):
        value = bool(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            if value == False:
                self._write('%s:TRA OFF' % self._channel_name[index])
            elif value == True:
                self._write('%s:TRA ON' % self._channel_name[index])
        self._channel_enabled[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_input_impedance(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            result = str(self._ask('%s:coupling?' % self._channel_name[index])).lower().split()
            result = result[1]
            if result == 'a1m':
                impedance = 1000000
                coupling = 'ac'
            elif result == 'a1m':
                impedance = 1000000
                coupling = 'dc'
            elif result == 'd50':
                impedance = 50
                coupling = 'dc'
            elif result == 'gnd':
                impedance = 1000000
                coupling = 'gnd'
            self._channel_input_impedance[index] = impedance
            self._channel_coupling[index] = coupling
            self._set_cache_valid(index=index)
        return self._channel_input_impedance[index]

    def _set_channel_input_impedance(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        if value not in InputImpedance:
            raise Exception('Invalid input impedance selection')
        result = str(self._ask('%s:coupling?' % self._channel_name[index])).lower()
        if result[0] == 'a' and value == 1000000:
            coupling = 'a1m'
        elif result[0] == 'a' and value == 50:
            raise Exception('Invalid impedance selection')
        elif result[0] == 'd' and value == 1000000:
            coupling = 'd1m'
        elif result[0] == 'd' and value == 50:
            coupling = 'd50'
        elif result == 'gnd':
            if value == 50:
                coupling = 'd50'
            elif value == 1000000:
                coupling = 'd1m'
        else:
            raise Exception('Invalid impedance selection')
        if not self._driver_operation_simulate:
            self._write('%s:coupling %s' % (self._channel_name[index], coupling.upper()))
        self._channel_input_impedance[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_input_frequency_max(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        return self._channel_input_frequency_max[index]

    def _set_channel_input_frequency_max(self, index, value):
        value = float(value)
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate:
            self._set_channel_bw_limit(index, value < 20000000.0)
        self._channel_input_frequency_max[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_probe_attenuation(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_probe_attenuation[index] = int(self._ask('%s:attenuation?' % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_probe_attenuation[index]

    def _set_channel_probe_attenuation(self, index, value):
        """
        <channel> : ATTeNuation <attenuation>
        <channel> :={C1,C2,C3,C4,EX,EX10}
        <attenuation> : = {1, 2, 5, 10, 20, 25, 50, 100, 200, 500, 1000, 10000}
        """
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate:
            self._write('%s:ATTN %e' % (self._channel_name[index], value))
        self._channel_probe_attenuation[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_invert(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_invert[index] = bool(int(self._ask(':%s:invert?' % self._channel_name[index])))
            self._set_cache_valid(index=index)
        return self._channel_invert[index]

    def _set_channel_invert(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(':%s:invert %e' % (self._channel_name[index], int(value)))
        self._channel_invert[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_probe_id(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_probe_id[index] = self._ask(':%s:probe:id?' % self._channel_name[index])
            self._set_cache_valid(index=index)
        return self._channel_probe_id[index]

    def _get_channel_bw_limit(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            limits = self._ask('BWL?').strip().split(',')
            if self._channel_name[index] in limits:
                self._channel_bw_limit[index] = limits[(limits.index(self._channel_name[index]) + 1)]
            self._set_cache_valid(index=index)
        return self._channel_bw_limit[index]

    def _set_channel_bw_limit(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate:
            self._write('BWL %s,%s' % (self._channel_name[index], value))
        self._channel_bw_limit[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_coupling(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            result = self._ask('%s:coupling?' % self._channel_name[index]).lower().split()
            self._channel_coupling[index] = result[1]
        return self._channel_coupling[index]

    def _set_channel_coupling(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        if value not in VerticalCoupling:
            raise ivi.ValueNotSupportedException()
        result = str(self._ask('%s:coupling?' % self._channel_name[index])).lower()
        if result[1:3] == '1m' or result == 'gnd':
            if value == 'ac':
                coupling = 'a1m'
            elif value == 'dc':
                coupling = 'd1m'
        elif result[1:3] == '50' and value == 'dc':
            coupling = 'd50'
        elif result[1:3] == '50' and value == 'ac':
            raise Exception('Invalid coupling selection, set correct impedance')
        elif value == 'gnd':
            coupling = 'gnd'
        if not self._driver_operation_simulate:
            self._write('%s:coupling %s' % (self._channel_name[index], coupling.upper()))
        self._channel_coupling[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_offset(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_offset[index] = float(self._ask('%s:offset?' % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_offset[index]

    def _set_channel_offset(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write('%s:offset %e' % (self._channel_name[index], value))
        self._channel_offset[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_range(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_range[index] = float(self._ask(':%s:range?' % self._channel_name[index]))
            self._channel_scale[index] = self._channel_range[index] / self._vertical_divisions
            self._set_cache_valid(index=index)
            self._set_cache_valid(True, 'channel_scale', index)
        return self._channel_range[index]

    def _set_channel_range(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(':%s:range %e' % (self._channel_name[index], value))
        self._channel_range[index] = value
        self._channel_scale[index] = value / self._vertical_divisions
        self._set_cache_valid(index=index)
        self._set_cache_valid(True, 'channel_scale', index)

    def _get_channel_scale(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_scale[index] = float(self._ask(':%s:scale?' % self._channel_name[index]))
            self._channel_range[index] = self._channel_scale[index] * self._vertical_divisions
            self._set_cache_valid(index=index)
            self._set_cache_valid(True, 'channel_range', index)
        return self._channel_scale[index]

    def _set_channel_scale(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(':%s:scale %e' % (self._channel_name[index], value))
        self._channel_scale[index] = value
        self._channel_range[index] = value * self._vertical_divisions
        self._set_cache_valid(index=index)
        self._set_cache_valid(True, 'channel_range', index)

    def _get_measurement_status(self):
        return self._measurement_status

    def _get_trigger_coupling(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            cpl = self._ask(':trigger:coupling?').lower()
            noise = int(self._ask(':trigger:nreject?'))
            hf = int(self._ask(':trigger:hfreject?'))
            for k in TriggerCouplingMapping:
                if (
                 cpl, noise, hf) == TriggerCouplingMapping[k]:
                    self._trigger_coupling = k

        return self._trigger_coupling

    def _set_trigger_coupling(self, value):
        if value not in TriggerCouplingMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            cpl, noise, hf = TriggerCouplingMapping[value]
            self._write(':trigger:coupling %s' % cpl)
            self._write(':trigger:nreject %d' % noise)
            self._write(':trigger:hfreject %d' % hf)
        self._trigger_coupling = value
        self._set_cache_valid()

    def _get_trigger_holdoff(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._trigger_holdoff = float(self._ask(':trigger:holdoff?'))
            self._set_cache_valid()
        return self._trigger_holdoff

    def _set_trigger_holdoff(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(':trigger:holdoff %e' % value)
        self._trigger_holdoff = value
        self._set_cache_valid()

    def _get_channel_trigger_level(self, index):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._channel_trigger_level[index] = float(self._ask('%s:TRLV?' % self._channel_name[index]).split(',')[0].split(' ')[0])
            self._set_cache_valid()
        return self._channel_trigger_level[index]

    def _set_channel_trigger_level(self, index, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write('%s:TRLV %e' % (self._channel_name[index], value))
        self._channel_trigger_level[index] = value
        self._set_cache_valid()

    def _get_trigger_edge_slope(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(':trigger:edge:slope?').lower()
            self._trigger_edge_slope = [ k for k, v in SlopeMapping.items() if v == value ][0]
            self._set_cache_valid()
        return self._trigger_edge_slope

    def _set_trigger_edge_slope(self, value):
        if value not in SlopeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(':trigger:edge:slope %s' % SlopeMapping[value])
        self._trigger_edge_slope = value
        self._set_cache_valid()

    def _get_trigger_source(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            vals = self._ask('TRSE?')
            vals = vals.split(',')
            source = vals[(vals.index('SR') + 1)]
            self._trigger_source = source
            self._set_cache_valid()
        return self._trigger_source

    def _set_trigger_source(self, value):
        value = str(value)
        if value not in self._channel_name:
            raise ivi.UnknownPhysicalNameException()
        if not self._driver_operation_simulate:
            vals = self._ask('TRSE?')
            split_vals = vals.split(',')
            split_vals[split_vals.index('SR') + 1] = value
            vals = (',').join(split_vals)
            self._write('TRSE %s' % vals)
        self._trigger_source = value
        self._set_cache_valid()

    def _set_trigger_mode(self, value):
        value = value.lower()
        if value not in TriggerModes:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write('TRMD %s' % value.lower())
        self._trigger_mode = value
        self._set_cache_valid()

    def _get_trigger_mode(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask('TRMD?').lower()
            self._trigger_mode = value
            self._set_cache_valid()
        return self._trigger_mode

    def _get_trigger_type(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            vals = self._ask('TRSE?')
            value = vals.split(',')[0]
            self._trigger_type = value.lower()
            self._set_cache_valid()
        return self._trigger_type

    def _set_trigger_type(self, value):
        value = value.lower()
        if value not in TriggerTypes:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write('TRSE %s' % value)
        self._trigger_type = value
        self._set_cache_valid()

    def _measurement_abort(self):
        pass

    def _measurement_fetch_waveform(self, index):
        index = ivi.get_index(self._channel_name, index)
        if self._driver_operation_simulate:
            return list()
        self._write('COMM_ORDER HI')
        self._write('COMM_FORMAT DEF9,WORD,BIN')
        pre = self._ask('%s:INSPECT? WAVEDESC' % self._channel_name[index]).split('\r\n')
        temp = []
        for item in pre:
            temp.append(item.split(':'))

        mydict = dict([ (d[0].strip(), ('').join(d[1:]).strip()) for d in temp ])
        format = str(mydict['COMM_TYPE'])
        points = int(mydict['PNTS_PER_SCREEN'])
        xincrement = float(mydict['HORIZ_INTERVAL'])
        xorigin = float(mydict['HORIZ_OFFSET'])
        yincrement = float(mydict['VERTICAL_GAIN'])
        yorigin = float(mydict['VERTICAL_OFFSET'])
        if format.lower() != 'word':
            raise ivi.UnexpectedResponseException()
        self._write('%s:WAVEFORM? DAT1' % self._channel_name[index])
        raw_data = raw_data = self._read_ieee_block()
        data = list()
        for i in range(points):
            x = i * xincrement + xorigin
            yval = struct.unpack('>H', raw_data[i * 2:i * 2 + 2])[0]
            if yval > 32767:
                yval = yval - 65536
            if yval == 0:
                y = float('nan')
            else:
                y = yincrement * yval - yorigin
            data.append((x, y))

        return data

    def _measurement_read_waveform(self, index, maximum_time):
        return self._measurement_fetch_waveform(index)

    def _measurement_initiate(self):
        if not self._driver_operation_simulate:
            self._write(':acquire:complete 100')
            self._write(':digitize')
            self._set_cache_valid(False, 'trigger_continuous')

    def _get_reference_level_high(self):
        return self._reference_level_high

    def _set_reference_level_high(self, value):
        value = float(value)
        if value < 5:
            value = 5
        if value > 95:
            value = 95
        self._reference_level_high = value
        if not self._driver_operation_simulate:
            self._write(':measure:define thresholds, %e, %e, %e' % (
             self._reference_level_high,
             self._reference_level_middle,
             self._reference_level_low))

    def _get_reference_level_low(self):
        return self._reference_level_low

    def _set_reference_level_low(self, value):
        value = float(value)
        if value < 5:
            value = 5
        if value > 95:
            value = 95
        self._reference_level_low = value
        if not self._driver_operation_simulate:
            self._write(':measure:define thresholds, %e, %e, %e' % (
             self._reference_level_high,
             self._reference_level_middle,
             self._reference_level_low))

    def _get_reference_level_middle(self):
        return self._reference_level_middle

    def _set_reference_level_middle(self, value):
        value = float(value)
        if value < 5:
            value = 5
        if value > 95:
            value = 95
        self._reference_level_middle = value
        if not self._driver_operation_simulate:
            self._write(':measure:define thresholds, %e, %e, %e' % (
             self._reference_level_high,
             self._reference_level_middle,
             self._reference_level_low))

    def _measurement_fetch_waveform_measurement(self, index, measurement_function, ref_channel=None):
        index = ivi.get_index(self._channel_name, index)
        if index < self._analog_channel_count:
            if measurement_function not in MeasurementFunctionMapping:
                raise ivi.ValueNotSupportedException()
            func = MeasurementFunctionMapping[measurement_function]
        else:
            if measurement_function not in MeasurementFunctionMappingDigital:
                raise ivi.ValueNotSupportedException()
            func = MeasurementFunctionMappingDigital[measurement_function]
        if not self._driver_operation_simulate:
            l = func.split(' ')
            l[0] = l[0] + '?'
            if len(l) > 1:
                l[-1] = l[(-1)] + ','
            func = (' ').join(l)
            query = ':measure:%s %s' % (func, self._channel_name[index])
            if measurement_function in ('ratio', 'phase', 'delay'):
                ref_index = ivi.get_index(self._channel_name, ref_channel)
                query += ', %s' % self._channel_name[ref_index]
            return float(self._ask(query))
        return 0

    def _measurement_read_waveform_measurement(self, index, measurement_function, maximum_time):
        return self._measurement_fetch_waveform_measurement(index, measurement_function)

    def _get_acquisition_number_of_envelopes(self):
        return self._acquisition_number_of_envelopes

    def _set_acquisition_number_of_envelopes(self, value):
        self._acquisition_number_of_envelopes = value

    def _measurement_fetch_waveform_min_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        data = list()
        return data

    def _measurement_read_waveform_min_max(self, index, maximum_time):
        return _measurement_fetch_waveform_min_max(index)

    def _get_trigger_continuous(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._trigger_continuous = int(self._ask(':oper:cond?')) & 8 != 0
            self._set_cache_valid()
        return self._trigger_continuous

    def _set_trigger_continuous(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            t = 'stop'
            if value:
                t = 'run'
            self._write(':%s' % t)
        self._trigger_continuous = value
        self._set_cache_valid()

    def _get_acquisition_number_of_averages(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_number_of_averages = int(self._ask(':acquire:count?'))
            self._set_cache_valid()
        return self._acquisition_number_of_averages

    def _set_acquisition_number_of_averages(self, value):
        if value < 1 or value > 65536:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(':acquire:count %d' % value)
        self._acquisition_number_of_averages = value
        self._set_cache_valid()

    def _get_acquisition_sample_mode(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(':acquire:mode?').lower()
            self._acquisition_sample_mode = [ k for k, v in SampleModeMapping.items() if v == value ][0]
            self._set_cache_valid()
        return self._acquisition_sample_mode

    def _set_acquisition_sample_mode(self, value):
        if value not in SampleModeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(':acquire:mode %s' % SampleModeMapping[value])
        self._acquisition_sample_mode = value
        self._set_cache_valid()

    def _measurement_auto_setup(self):
        if not self._driver_operation_simulate:
            self._write('ASET')

    def _memory_save(self, index):
        index = int(index)
        if index < 0 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write('*sav %d' % index)

    def _memory_recall(self, index):
        index = int(index)
        if index < 0 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write('*rcl %d' % index)
            self.driver_operation.invalidate_all_attributes()