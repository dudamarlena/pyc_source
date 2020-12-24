# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ivi/scope.py
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
from . import ivi

class ChannelNotEnabledException(ivi.IviException):
    pass


class InvalidAcquisitionTypeException(ivi.IviException):
    pass


class UnableToPerformMeasurementException(ivi.IviException):
    pass


AcquisitionType = set(['normal', 'peak_detect', 'high_resolution', 'average'])
VerticalCoupling = set(['ac', 'dc', 'gnd'])
TriggerCoupling = set(['ac', 'dc', 'hf_reject', 'lf_reject', 'noise_reject'])
Slope = set(['positive', 'negative', 'either'])
Trigger = set(['edge', 'width', 'runt', 'glitch', 'tv', 'immediate', 'ac_line'])
Interpolation = set(['none', 'sinex', 'linear'])
TVTriggerEvent = set(['field1', 'field2', 'any_field', 'any_line', 'line_number'])
TVTriggerFormat = set(['ntsc', 'pal', 'secam'])
Polarity = set(['positive', 'negative'])
Polarity3 = set(['positive', 'negative', 'either'])
GlitchCondition = set(['less_than', 'greater_than'])
WidthCondition = set(['within', 'outside'])
AcquisitionSampleMode = set(['real_time', 'equivalent_time'])
TriggerModifier = set(['none', 'auto', 'auto_level'])
MeasurementFunction = set(['rise_time', 'fall_time', 'frequency', 'period',
 'voltage_rms', 'voltage_peak_to_peak', 'voltage_max', 'voltage_min',
 'voltage_high', 'voltage_low', 'voltage_average', 'width_negative',
 'width_positive', 'duty_cycle_negative', 'duty_cycle_positive',
 'amplitude', 'voltage_cycle_rms', 'voltage_cycle_average',
 'overshoot', 'preshoot'])
AcquisitionStatus = set(['complete', 'in_progress', 'unknown'])

class Base(ivi.IviContainer):
    """Base IVI methods for all oscilloscopes"""

    def __init__(self, *args, **kwargs):
        self._channel_count = 1
        super(Base, self).__init__(*args, **kwargs)
        cls = 'IviScope'
        grp = 'Base'
        ivi.add_group_capability(self, cls + grp)
        self._acquisition_start_time = 0
        self._acquisition_type = 'normal'
        self._acquisition_number_of_points_minimum = 0
        self._acquisition_record_length = 1000
        self._acquisition_time_per_record = 0.001
        self._channel_name = list()
        self._channel_enabled = list()
        self._channel_input_impedance = list()
        self._channel_input_frequency_max = list()
        self._channel_probe_attenuation = list()
        self._channel_coupling = list()
        self._channel_offset = list()
        self._channel_range = list()
        self._channel_count = 1
        self._measurement_status = 'unknown'
        self._trigger_coupling = 'dc'
        self._trigger_holdoff = 0
        self._trigger_level = 0
        self._trigger_edge_slope = 'positive'
        self._trigger_source = ''
        self._trigger_type = 'edge'
        self._add_property('acquisition.start_time', self._get_acquisition_start_time, self._set_acquisition_start_time, None, ivi.Doc('\n                        Specifies the length of time from the trigger event to the first point in\n                        the waveform record. If the value is positive, the first point in the\n                        waveform record occurs after the trigger event. If the value is negative,\n                        the first point in the waveform record occurs before the trigger event.\n                        The units are seconds.\n                        ', cls, grp, '4.2.1'))
        self._add_property('acquisition.type', self._get_acquisition_type, self._set_acquisition_type, None, ivi.Doc("\n                        Specifies how the oscilloscope acquires data and fills the waveform\n                        record.\n                        \n                        Values:\n                        * 'normal'\n                        * 'high_resolution'\n                        * 'average'\n                        * 'peak_detect'\n                        * 'envelope'\n                        ", cls, grp, '4.2.3'))
        self._add_property('acquisition.number_of_points_minimum', self._get_acquisition_number_of_points_minimum, self._set_acquisition_number_of_points_minimum, None, ivi.Doc('\n                        Specifies the minimum number of points the end-user requires in the\n                        waveform record for each channel. The instrument driver uses the value the\n                        end-user specifies to configure the record length that the oscilloscope\n                        uses for waveform acquisition. If the instrument cannot support the\n                        requested record length, the driver shall configure the instrument to the\n                        closest bigger record length. The Horizontal Record Length attribute\n                        returns the actual record length.\n                        ', cls, grp, '4.2.8'))
        self._add_property('acquisition.record_length', self._get_acquisition_record_length, None, None, ivi.Doc('\n                        Returns the actual number of points the oscilloscope acquires for each\n                        channel. The value is equal to or greater than the minimum number of\n                        points the end-user specifies with the Horizontal Minimum Number of Points\n                        attribute.\n                        \n                        Note: Oscilloscopes may use different size records depending on the value\n                        the user specifies for the Acquisition Type attribute.\n                        ', cls, grp, '4.2.9'))
        self._add_property('acquisition.sample_rate', self._get_acquisition_sample_rate, None, None, ivi.Doc('\n                        Returns the effective sample rate of the acquired waveform using the\n                        current configuration. The units are samples per second.\n                        ', cls, grp, '4.2.10'))
        self._add_property('acquisition.time_per_record', self._get_acquisition_time_per_record, self._set_acquisition_time_per_record, None, ivi.Doc('\n                        Specifies the length of time that corresponds to the record length. The\n                        units are seconds.\n                        ', cls, grp, '4.2.11'))
        self._add_method('acquisition.configure_record', self._acquisition_configure_record, ivi.Doc('\n                        This function configures the most commonly configured attributes of the\n                        oscilloscope acquisition sub-system. These attributes are the time per\n                        record, minimum record length, and the acquisition start time.\n                        ', cls, grp, '4.3.4'))
        self._add_property('channels[].name', self._get_channel_name, None, None, ivi.Doc('\n                        This attribute returns the repeated capability identifier defined by\n                        specific driver for the channel that corresponds to the index that the\n                        user specifies. If the driver defines a qualified channel name, this\n                        property returns the qualified name.\n                        \n                        If the value that the user passes for the Index parameter is less than\n                        zero or greater than the value of the channel count, the attribute raises\n                        a SelectorRangeException.\n                        ', cls, grp, '4.2.7'))
        self._add_property('channels[].enabled', self._get_channel_enabled, self._set_channel_enabled, None, ivi.Doc('\n                        If set to True, the oscilloscope acquires a waveform for the channel. If\n                        set to False, the oscilloscope does not acquire a waveform for the\n                        channel.\n                        ', cls, grp, '4.2.5'))
        self._add_property('channels[].input_impedance', self._get_channel_input_impedance, self._set_channel_input_impedance, None, ivi.Doc('\n                        Specifies the input impedance for the channel in Ohms.\n                        \n                        Common values are 50.0, 75.0, and 1,000,000.0.\n                        ', cls, grp, '4.2.12'))
        self._add_property('channels[].input_frequency_max', self._get_channel_input_frequency_max, self._set_channel_input_frequency_max, None, ivi.Doc('\n                        Specifies the maximum frequency for the input signal you want the\n                        instrument to accommodate without attenuating it by more than 3dB. If the\n                        bandwidth limit frequency of the instrument is greater than this maximum\n                        frequency, the driver enables the bandwidth limit. This attenuates the\n                        input signal by at least 3dB at frequencies greater than the bandwidth\n                        limit.\n                        ', cls, grp, '4.2.13'))
        self._add_property('channels[].probe_attenuation', self._get_channel_probe_attenuation, self._set_channel_probe_attenuation, None, ivi.Doc("\n                        Specifies the scaling factor by which the probe the end-user attaches to\n                        the channel attenuates the input. For example, for a 10:1 probe, the\n                        end-user sets this attribute to 10.0.\n                        \n                        Note that if the probe is changed to one with a different attenuation, and\n                        this attribute is not set, the amplitude calculations will be incorrect.\n                        \n                        Querying this value will return the probe attenuation corresponding to the\n                        instrument's actual probe attenuation. Setting this property sets Probe\n                        Attenuation Auto to False Negative values are not valid.\n                        ", cls, grp, '4.2.16'))
        self._add_property('channels[].coupling', self._get_channel_coupling, self._set_channel_coupling, None, ivi.Doc("\n                        Specifies how the oscilloscope couples the input signal for the channel.\n                        \n                        Values:\n                        \n                        * 'ac'\n                        * 'dc'\n                        * 'gnd'\n                        ", cls, grp, '4.2.23'))
        self._add_property('channels[].offset', self._get_channel_offset, self._set_channel_offset, None, ivi.Doc('\n                        Specifies the location of the center of the range that the Vertical Range\n                        attribute specifies. The value is with respect to ground and is in volts.\n                        \n                        For example, to acquire a sine wave that spans between on 0.0 and 10.0\n                        volts, set this attribute to 5.0 volts.\n                        ', cls, grp, '4.2.24'))
        self._add_property('channels[].range', self._get_channel_range, self._set_channel_range, None, ivi.Doc('\n                        Specifies the absolute value of the full-scale input range for a channel.\n                        The units are volts.\n                        \n                        For example, to acquire a sine wave that spans between -5.0 and 5.0 volts,\n                        set the Vertical Range attribute to 10.0 volts.\n                        ', cls, grp, '4.2.25'))
        self._add_method('channels[].configure', self._channel_configure, ivi.Doc('\n                        This function configures the most commonly configured attributes of the\n                        oscilloscope channel sub-system. These attributes are the range, offset,\n                        coupling, probe attenuation, and whether the channel is enabled.\n                        ', cls, grp, '4.3.6'))
        self._add_method('channels[].configure_characteristics', self._channel_configure_characteristics, ivi.Doc('\n                        This function configures the attributes that control the electrical\n                        characteristics of the channel. These attributes are the input impedance\n                        and the maximum frequency of the input signal.\n                        ', cls, grp, '4.3.8'))
        self._add_method('channels[].measurement.fetch_waveform', self._measurement_fetch_waveform, ivi.Doc('\n                        This function returns the waveform the oscilloscope acquires for the\n                        specified channel. The waveform is from a previously initiated\n                        acquisition.\n                        \n                        You use the Initiate Acquisition function to start an acquisition on the\n                        channels that the end-user configures with the Configure Channel function.\n                        The oscilloscope acquires waveforms on the concurrently enabled channels.\n                        If the channel is not enabled for the acquisition, this function returns\n                        the Channel Not Enabled error.\n                        \n                        Use this function only when the acquisition mode is Normal, Hi Res, or\n                        Average. If the acquisition type is not one of the listed types, the\n                        function returns the Invalid Acquisition Type error.\n                        \n                        You use the Acquisition Status function to determine when the acquisition\n                        is complete. You must call this function separately for each enabled\n                        channel to obtain the waveforms.\n                        \n                        You can call the Read Waveform function instead of the Initiate\n                        Acquisition function. The Read Waveform function starts an acquisition on\n                        all enabled channels, waits for the acquisition to complete, and returns\n                        the waveform for the specified channel. You call this function to obtain\n                        the waveforms for each of the remaining channels.\n                        \n                        The return value is a list of (x, y) tuples that represent the time and\n                        voltage of each data point.  The y point may be NaN in the case that the\n                        oscilloscope could not sample the voltage.\n                        \n                        The end-user configures the interpolation method the oscilloscope uses\n                        with the Acquisition.Interpolation property. If interpolation is disabled,\n                        the oscilloscope does not interpolate points in the waveform. If the\n                        oscilloscope cannot sample a value for a point in the waveform, the driver\n                        sets the corresponding element in the waveformArray to an IEEE-defined NaN\n                        (Not a Number) value. Check for this value with math.isnan() or\n                        numpy.isnan().\n                        \n                        This function does not check the instrument status. Typically, the\n                        end-user calls this function only in a sequence of calls to other\n                        low-level driver functions. The sequence performs one operation. The\n                        end-user uses the low-level functions to optimize one or more aspects of\n                        interaction with the instrument. Call the Error Query function at the\n                        conclusion of the sequence to check the instrument status.\n                        ', cls, grp, '4.3.13'))
        self._add_method('channels[].measurement.read_waveform', self._measurement_read_waveform, ivi.Doc('\n                        This function initiates an acquisition on the channels that the end-user\n                        configures with the Configure Channel function. If the channel is not\n                        enabled for the acquisition, this function returns Channel Not Enabled\n                        error. It then waits for the acquisition to complete, and returns the\n                        waveform for the channel the end-user specifies. If the oscilloscope did\n                        not complete the acquisition within the time period the user specified\n                        with the max_time parameter, the function returns the Max Time Exceeded\n                        error.\n                        \n                        Use this function only when the acquisition mode is Normal, Hi Res, or\n                        Average. If the acquisition type is not one of the listed types, the\n                        function returns the Invalid Acquisition Type error.\n                        \n                        You call the Fetch Waveform function to obtain the waveforms for each of\n                        the remaining enabled channels without initiating another acquisition.\n                        After this function executes, each element in the WaveformArray parameter\n                        is either a voltage or a value indicating that the oscilloscope could not\n                        sample a voltage.\n                        \n                        \n                        The end-user configures the interpolation method the oscilloscope uses\n                        with the Acquisition.Interpolation property. If interpolation is disabled,\n                        the oscilloscope does not interpolate points in the waveform. If the\n                        oscilloscope cannot sample a value for a point in the waveform, the driver\n                        sets the corresponding element in the waveformArray to an IEEE-defined NaN\n                        (Not a Number) value. Check for this value with math.isnan() or\n                        numpy.isnan(). Check an entire array with\n                        \n                        any(any(math.isnan(b) for b in a) for a in waveform)\n                        ', cls, grp, '4.3.16'))
        self._add_property('measurement.status', self._get_measurement_status, None, None, ivi.Doc("\n                        Acquisition status indicates whether an acquisition is in progress,\n                        complete, or if the status is unknown.\n                        \n                        Acquisition status is not the same as instrument status, and does not\n                        necessarily check for instrument errors. To make sure that the instrument\n                        is checked for errors after getting the acquisition status, call the Error\n                        Query method. (Note that the end user may want to call Error Query at the\n                        end of a sequence of other calls which include getting the acquisition\n                        status - it does not necessarily need to be called immediately.)\n                        \n                        If the driver cannot determine whether the acquisition is complete or not,\n                        it returns the Acquisition Status Unknown value.\n                        \n                        Values:\n                        * 'compete'\n                        * 'in_progress'\n                        * 'unknown'\n                        ", cls, grp, '4.2.2'))
        self._add_method('measurement.abort', self._measurement_abort, ivi.Doc('\n                        This function aborts an acquisition and returns the oscilloscope to the\n                        Idle state. This function does not check the instrument status.\n                        \n                        Typically, the end-user calls this function only in a sequence of calls to\n                        other low-level driver functions. The sequence performs one operation. The\n                        end-user uses the low-level functions to optimize one or more aspects of\n                        interaction with the instrument. Call the Error Query function at the\n                        conclusion of the sequence to check the instrument status.\n                        \n                        If the instrument cannot abort an initiated acquisition, the driver shall\n                        return the Function Not Supported error.\n                        ', cls, grp, '4.3.1'))
        self._add_method('measurement.initiate', self._measurement_initiate, ivi.Doc('\n                        This function initiates a waveform acquisition. After calling this\n                        function, the oscilloscope leaves the idle state and waits for a trigger.\n                        The oscilloscope acquires a waveform for each channel the end-user has\n                        enabled with the Configure Channel function.\n                        \n                        This function does not check the instrument status. Typically, the\n                        end-user calls this function only in a sequence of calls to other\n                        low-level driver functions. The sequence performs one operation. The\n                        end-user uses the low-level functions to optimize one or more aspects of\n                        interaction with the instrument. Call the Error Query function at the\n                        conclusion of the sequence to check the instrument status.\n                        ', cls, grp, '4.3.14'))
        self._add_property('trigger.coupling', self._get_trigger_coupling, self._set_trigger_coupling, None, ivi.Doc("\n                        Specifies how the oscilloscope couples the trigger source.\n                        \n                        Values:\n                        \n                        * 'ac'\n                        * 'dc'\n                        * 'lf_reject'\n                        * 'hf_reject'\n                        * 'noise_reject'\n                        ", cls, grp, '4.2.17'))
        self._add_property('trigger.holdoff', self._get_trigger_holdoff, self._set_trigger_holdoff, None, ivi.Doc('\n                        Specifies the length of time the oscilloscope waits after it detects a\n                        trigger until the oscilloscope enables the trigger subsystem to detect\n                        another trigger. The units are seconds. The Trigger Holdoff attribute\n                        affects instrument operation only when the oscilloscope requires multiple\n                        acquisitions to build a complete waveform. The oscilloscope requires\n                        multiple waveform acquisitions when it uses equivalent-time sampling or\n                        when the Acquisition Type attribute is set to Envelope or Average.\n                        \n                        Note: Many scopes have a small, non-zero value as the minimum value for\n                        this attribute. To configure the instrument to use the shortest trigger\n                        hold-off, the user can specify a value of zero for this attribute.\n                        \n                        Therefore, the IVI Class-Compliant specific driver shall coerce any value\n                        between zero and the minimum value to the minimum value. No other coercion\n                        is allowed on this attribute.\n                        ', cls, grp, '4.2.18'))
        self._add_property('trigger.level', self._get_trigger_level, self._set_trigger_level, None, ivi.Doc('\n                        Specifies the voltage threshold for the trigger sub-system. The units are\n                        volts. This attribute affects instrument behavior only when the Trigger\n                        Type is set to one of the following values: Edge Trigger, Glitch Trigger,\n                        or Width Trigger.\n                        \n                        This attribute, along with the Trigger Slope, Trigger Source, and Trigger\n                        Coupling attributes, defines the trigger event when the Trigger Type is\n                        set to Edge Trigger.\n                        ', cls, grp, '4.2.19'))
        self._add_property('trigger.edge.slope', self._get_trigger_edge_slope, self._set_trigger_edge_slope, None, ivi.Doc("\n                        Specifies whether a rising or a falling edge triggers the oscilloscope.\n                        \n                        This attribute affects instrument operation only when the Trigger Type\n                        attribute is set to Edge Trigger.\n                        \n                        Values:\n                         * 'positive'\n                         * 'negative'\n                        ", cls, grp, '4.2.20'))
        self._add_method('trigger.edge.configure', self._trigger_edge_configure, ivi.Doc('\n                        This function sets the edge triggering attributes. An edge trigger occurs\n                        when the trigger signal that the end-user specifies with the Source\n                        parameter passes through the voltage threshold that the end-user\n                        specifies with the level parameter and has the slope that the end-user\n                        specifies with the Slope parameter.\n                        \n                        This function affects instrument behavior only if the Trigger Type is Edge\n                        Trigger. Set the Trigger Type and Trigger Coupling before calling this\n                        function.\n                        \n                        If the trigger source is one of the analog input channels, an application\n                        program should configure the vertical range, vertical offset, vertical\n                        coupling, probe attenuation, and the maximum input frequency before\n                        calling this function.\n                        ', cls, grp, '4.3.9'))
        self._add_property('trigger.source', self._get_trigger_source, self._set_trigger_source, None, ivi.Doc('\n                        Specifies the source the oscilloscope monitors for the trigger event. The \n                        value can be a channel name alias, a driver-specific channel string, or\n                        one of the values below.\n                        \n                        This attribute affects the instrument operation only when the Trigger Type\n                        is set to one of the following values: Edge Trigger, TV Trigger, Runt\n                        Trigger, Glitch Trigger, or Width Trigger.\n                        ', cls, grp, '4.2.21'))
        self._add_property('trigger.type', self._get_trigger_type, self._set_trigger_type, None, ivi.Doc("\n                        Specifies the event that triggers the oscilloscope.\n                        \n                        Values:\n                        \n                        * 'edge'\n                        * 'tv'\n                        * 'runt'\n                        * 'glitch'\n                        * 'width'\n                        * 'immediate'\n                        * 'ac_line'\n                        ", cls, grp, '4.2.22'))
        self._add_method('trigger.configure', self._trigger_configure, ivi.Doc('\n                        This function configures the common attributes of the trigger subsystem.\n                        These attributes are the trigger type and trigger holdoff.\n                        \n                        When the end-user calls Read Waveform, Read Waveform Measurement, Read Min\n                        Max Waveform, or Initiate Acquisition, the oscilloscope waits for a\n                        trigger. The end-user specifies the type of trigger for which the\n                        oscilloscope waits with the TriggerType parameter.\n                        \n                        If the oscilloscope requires multiple waveform acquisitions to build a\n                        complete waveform, it waits for the length of time the end-user specifies\n                        with the Holdoff parameter to elapse since the previous trigger. The\n                        oscilloscope then waits for the next trigger. Once the oscilloscope\n                        acquires a complete waveform, it returns to the idle state.\n                        ', cls, grp, '4.3.10'))
        self._init_channels()
        return

    def _init_channels(self):
        try:
            super(Base, self)._init_channels()
        except AttributeError:
            pass

        self._channel_name = list()
        self._channel_enabled = list()
        self._channel_input_impedance = list()
        self._channel_input_frequency_max = list()
        self._channel_probe_attenuation = list()
        self._channel_coupling = list()
        self._channel_offset = list()
        self._channel_range = list()
        for i in range(self._channel_count):
            self._channel_name.append('channel%d' % (i + 1))
            self._channel_enabled.append(False)
            self._channel_input_impedance.append(1000000)
            self._channel_input_frequency_max.append(1000000000.0)
            self._channel_probe_attenuation.append(1)
            self._channel_coupling.append('dc')
            self._channel_offset.append(0)
            self._channel_range.append(1)

        self.channels._set_list(self._channel_name)

    def _get_acquisition_start_time(self):
        return self._acquisition_start_time

    def _set_acquisition_start_time(self, value):
        value = float(value)
        self._acquisition_start_time = value

    def _get_acquisition_type(self):
        return self._acquisition_type

    def _set_acquisition_type(self, value):
        if value not in AcquisitionType:
            raise ivi.ValueNotSupportedException()
        self._acquisition_type = value

    def _get_acquisition_number_of_points_minimum(self):
        return self._acquisition_number_of_points_minimum

    def _set_acquisition_number_of_points_minimum(self, value):
        value = int(value)
        self._acquisition_number_of_points_minimum = value

    def _get_acquisition_record_length(self):
        return self._acquisition_record_length

    def _get_acquisition_sample_rate(self):
        return self._get_acquisition_record_length() / self._get_acquisition_time_per_record()

    def _get_acquisition_time_per_record(self):
        return self._acquisition_time_per_record

    def _set_acquisition_time_per_record(self, value):
        value = float(value)
        self._acquisition_time_per_record = value

    def _get_channel_count(self):
        return self._channel_count

    def _get_channel_name(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_name[index]

    def _get_channel_enabled(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_enabled[index]

    def _set_channel_enabled(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = bool(value)
        self._channel_enabled[index] = value

    def _get_channel_input_impedance(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_input_impedance[index]

    def _set_channel_input_impedance(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_input_impedance[index] = value

    def _get_channel_input_frequency_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_input_frequency_max[index]

    def _set_channel_input_frequency_max(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_input_frequency_max[index] = value

    def _get_channel_probe_attenuation(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_probe_attenuation[index]

    def _set_channel_probe_attenuation(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_probe_attenuation[index] = value

    def _get_channel_coupling(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_coupling[index]

    def _set_channel_coupling(self, index, value):
        if value not in VerticalCoupling:
            raise ivi.ValueNotSupportedException()
        index = ivi.get_index(self._channel_name, index)
        self._channel_coupling[index] = value

    def _get_channel_offset(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_offset[index]

    def _set_channel_offset(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_offset[index] = value

    def _get_channel_range(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_range[index]

    def _set_channel_range(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_range[index] = value

    def _get_measurement_status(self):
        return self._measurement_status

    def _get_trigger_coupling(self):
        return self._trigger_coupling

    def _set_trigger_coupling(self, value):
        if value not in TriggerCoupling:
            raise ivi.ValueNotSupportedException()
        self._trigger_coupling = value

    def _get_trigger_holdoff(self):
        return self._trigger_holdoff

    def _set_trigger_holdoff(self, value):
        value = float(value)
        self._trigger_holdoff = value

    def _get_trigger_level(self):
        return self._trigger_level

    def _set_trigger_level(self, value):
        value = float(value)
        self._trigger_level = value

    def _get_trigger_edge_slope(self):
        return self._trigger_edge_slope

    def _set_trigger_edge_slope(self, value):
        if value not in Slope:
            raise ivi.ValueNotSupportedException()
        self._trigger_edge_slope = value

    def _get_trigger_source(self):
        return self._trigger_source

    def _set_trigger_source(self, value):
        self._trigger_source = value

    def _get_trigger_type(self):
        return self._trigger_type

    def _set_trigger_type(self, value):
        if value not in Trigger:
            raise ivi.ValueNotSupportedException()
        self._trigger_type = value

    def _measurement_abort(self):
        pass

    def _acquisition_configure_record(self, time_per_record, minimum_number_of_points, acquisition_start_time):
        self._set_acquisition_time_per_record(time_per_record)
        self._set_acquisition_number_of_points_minimum(minimum_number_of_points)
        self._set_acquisition_start_time(acquisition_start_time)

    def _channel_configure(self, index, range, offset, coupling, probe_attenuation, enabled):
        self._set_channel_range(index, range)
        self._set_channel_offset(index, offset)
        self._set_channel_coupling(index, coupling)
        self._set_channel_probe_attenuation(index, probe_attenuation)
        self._set_channel_enabled(index, enabled)

    def _channel_configure_characteristics(self, index, input_impedance, input_frequency_maximum):
        self._set_channel_input_impedance(index, input_impedance)
        self._set_channel_input_frequency_max(index, input_frequency_maximum)

    def _trigger_edge_configure(self, source, level, slope):
        self._set_trigger_source(source)
        self._set_trigger_level(level)
        self._set_trigger_edge_slope(slope)

    def _trigger_configure(self, type, holdoff):
        self._set_trigger_type(type)
        self._set_trigger_holdoff(holdoff)

    def _measurement_fetch_waveform(self, index):
        index = ivi.get_index(self._channel_name, index)
        data = list()
        return data

    def _measurement_read_waveform(self, index, maximum_time):
        return self._measurement_fetch_waveform(index)

    def _measurement_initiate(self):
        pass


class Interpolation(ivi.IviContainer):
    """Extension IVI methods for oscilloscopes supporting interpolation"""

    def __init__(self, *args, **kwargs):
        super(Interpolation, self).__init__(*args, **kwargs)
        cls = 'IviScope'
        grp = 'Interpolation'
        ivi.add_group_capability(self, cls + grp)
        self._acquisition_interpolation = 'none'
        self._add_property('acquisition.interpolation', self._get_acquisition_interpolation, self._set_acquisition_interpolation, None, ivi.Doc("\n                        Specifies the interpolation method the oscilloscope uses when it cannot\n                        resolve a voltage for every point in the waveform record.\n                        \n                        Values:\n                        * 'none'\n                        * 'sinex'\n                        * 'linear'\n                        ", cls, grp, '5.2.1'))
        return

    def _get_acquisition_interpolation(self):
        return self._acquisition_interpolation

    def _set_acquisition_interpolation(self, value):
        self._acquisition_interpolation = value


class TVTrigger(ivi.IviContainer):
    """Extension IVI methods for oscilloscopes supporting TV triggering"""

    def __init__(self, *args, **kwargs):
        super(TVTrigger, self).__init__(*args, **kwargs)
        cls = 'IviScope'
        grp = 'TVTrigger'
        ivi.add_group_capability(self, cls + grp)
        self._trigger_tv_trigger_event = 'any_line'
        self._trigger_tv_line_number = 0
        self._trigger_tv_polarity = 'positive'
        self._trigger_tv_signal_format = 'ntsc'
        self._add_property('trigger.tv.trigger_event', self._get_trigger_tv_trigger_event, self._set_trigger_tv_trigger_event, None, ivi.Doc("\n                        Specifies the event on which the oscilloscope triggers.\n                        \n                        Values:\n                        * 'field1'\n                        * 'field2'\n                        * 'any_field'\n                        * 'any_line'\n                        * 'line_number'\n                        ", cls, grp, '6.2.1'))
        self._add_property('trigger.tv.line_number', self._get_trigger_tv_line_number, self._set_trigger_tv_line_number, None, ivi.Doc('\n                        Specifies the line on which the oscilloscope triggers. The driver uses\n                        this attribute when the TV Trigger Event is set to TV Event Line Number.\n                        The line number setting is independent of the field. This means that to\n                        trigger on the first line of the second field, the user must configure\n                        the line number to the value of 263 (if we presume that field one had 262\n                        lines).\n                        ', cls, grp, '6.2.2'))
        self._add_property('trigger.tv.polarity', self._get_trigger_tv_polarity, self._set_trigger_tv_polarity, None, ivi.Doc("\n                        Specifies the polarity of the TV signal.\n                        \n                        Values:\n                        * 'positive'\n                        * 'negative'\n                        ", cls, grp, '6.2.3'))
        self._add_property('trigger.tv.signal_format', self._get_trigger_tv_signal_format, self._set_trigger_tv_signal_format, None, ivi.Doc("\n                        Specifies the format of TV signal on which the oscilloscope triggers.\n                        \n                        Values:\n                        * 'ntsc'\n                        * 'pal'\n                        * 'secam'\n                        ", cls, grp, '6.2.4'))
        self._add_method('trigger.tv.configure', self._trigger_tv_configure, ivi.Doc('\n                        This function configures the oscilloscope for TV triggering. It configures\n                        the TV signal format, the event and the signal polarity.\n                        \n                        This function affects instrument behavior only if the trigger type is TV\n                        Trigger. Set the Trigger Type and Trigger Coupling before calling this\n                        function.\n                        ', cls, grp, '6.3.2'))
        return

    def _get_trigger_tv_trigger_event(self):
        return self._trigger_tv_trigger_event

    def _set_trigger_tv_trigger_event(self, value):
        if value not in TVTriggerEvent:
            raise ivi.ValueNotSupportedException()
        self._trigger_tv_trigger_event = value

    def _get_trigger_tv_line_number(self):
        return self._trigger_tv_line_number

    def _set_trigger_tv_line_number(self, value):
        self._trigger_tv_line_number = value

    def _get_trigger_tv_polarity(self):
        return self._trigger_tv_polarity

    def _set_trigger_tv_polarity(self, value):
        if value not in Polarity:
            raise ivi.ValueNotSupportedException()
        self._trigger_tv_polarity = value

    def _get_trigger_tv_signal_format(self):
        return self._trigger_tv_signal_format

    def _set_trigger_tv_signal_format(self, value):
        if value not in TVTriggerFormat:
            raise ivi.ValueNotSupportedException()
        self._trigger_tv_signal_format = value

    def _trigger_tv_configure(self, source, signal_format, event, polarity):
        self._set_trigger_source(source)
        self._set_trigger_tv_signal_format(signal_format)
        self._set_trigger_tv_trigger_event(event)
        self._set_trigger_tv_polarity(polarity)


class RuntTrigger(ivi.IviContainer):
    """Extension IVI methods for oscilloscopes supporting runt triggering"""

    def __init__(self, *args, **kwargs):
        super(RuntTrigger, self).__init__(*args, **kwargs)
        cls = 'IviScope'
        grp = 'RuntTrigger'
        ivi.add_group_capability(self, cls + grp)
        self._trigger_runt_threshold_high = 0
        self._trigger_runt_threshold_low = 0
        self._trigger_runt_polarity = 'positive'
        self._add_property('trigger.runt.threshold_high', self._get_trigger_runt_threshold_high, self._set_trigger_runt_threshold_high, None, ivi.Doc('\n                        Specifies the high threshold the oscilloscope uses for runt triggering.\n                        The units are volts.\n                        ', cls, grp, '7.2.1'))
        self._add_property('trigger.runt.threshold_low', self._get_trigger_runt_threshold_low, self._set_trigger_runt_threshold_low, None, ivi.Doc('\n                        Specifies the low threshold the oscilloscope uses for runt triggering.\n                        The units are volts.\n                        ', cls, grp, '7.2.2'))
        self._add_property('trigger.runt.polarity', self._get_trigger_runt_polarity, self._set_trigger_runt_polarity, None, ivi.Doc("\n                        Specifies the polarity of the runt that triggers the oscilloscope.\n                        \n                        Values:\n                        * 'positive'\n                        * 'negative'\n                        * 'either'\n                        ", cls, grp, '7.2.3'))
        self._add_method('trigger.runt.configure', self._trigger_runt_configure, ivi.Doc('\n                        This function configures the runt trigger. A runt trigger occurs when the\n                        trigger signal crosses one of the runt thresholds twice without crossing\n                        the other runt threshold. The end-user specifies the runt thresholds with\n                        the RuntLowThreshold and RuntHighThreshold parameters. The end-user\n                        specifies the polarity of the runt with the RuntPolarity parameter.\n                        \n                        This function affects instrument behavior only if the trigger type is Runt\n                        Trigger. Set the trigger type and trigger coupling before calling this\n                        function.\n                        ', cls, grp, '7.3.1'))
        return

    def _get_trigger_runt_threshold_high(self):
        return self._trigger_runt_threshold_high

    def _set_trigger_runt_threshold_high(self, value):
        value = float(value)
        self._trigger_runt_threshold_high = value

    def _get_trigger_runt_threshold_low(self):
        return self._trigger_runt_threshold_low

    def _set_trigger_runt_threshold_low(self, value):
        value = float(value)
        self._trigger_runt_threshold_low = value

    def _get_trigger_runt_polarity(self):
        return self._trigger_runt_polarity

    def _set_trigger_runt_polarity(self, value):
        if value not in Polarity:
            raise ivi.ValueNotSupportedException()
        self._trigger_runt_polarity = value

    def _trigger_runt_configure(self, source, threshold_high, threshold_low, polarity):
        self._set_trigger_source(source)
        self._set_trigger_runt_threshold_high(threshold_high)
        self._set_trigger_runt_threshold_low(threshold_low)
        self._set_trigger_runt_polarity(polarity)


class GlitchTrigger(ivi.IviContainer):
    """Extension IVI methods for oscilloscopes supporting glitch triggering"""

    def __init__(self, *args, **kwargs):
        super(GlitchTrigger, self).__init__(*args, **kwargs)
        cls = 'IviScope'
        grp = 'GlitchTrigger'
        ivi.add_group_capability(self, cls + grp)
        self._trigger_glitch_condition = 'less_than'
        self._trigger_glitch_polarity = 'positive'
        self._trigger_glitch_width = 0
        self._add_property('trigger.glitch.condition', self._get_trigger_glitch_condition, self._set_trigger_glitch_condition, None, ivi.Doc("\n                        Specifies the glitch condition. This attribute determines whether the\n                        glitch trigger happens when the oscilloscope detects a pulse with a\n                        width less than or greater than the width value.\n                        \n                        Values:\n                        * 'greater_than'\n                        * 'less_than'\n                        ", cls, grp, '8.2.1'))
        self._add_property('trigger.glitch.polarity', self._get_trigger_glitch_polarity, self._set_trigger_glitch_polarity, None, ivi.Doc("\n                        Specifies the polarity of the glitch that triggers the oscilloscope.\n                        \n                        Values:\n                        * 'positive'\n                        * 'negative'\n                        * 'either'\n                        ", cls, grp, '8.2.2'))
        self._add_property('trigger.glitch.width', self._get_trigger_glitch_width, self._set_trigger_glitch_width, None, ivi.Doc('\n                        Specifies the glitch width. The units are seconds. The oscilloscope\n                        triggers when it detects a pulse with a width less than or greater than\n                        this value, depending on the Glitch Condition attribute.\n                        ', cls, grp, '8.2.3'))
        self._add_method('trigger.glitch.configure', self._trigger_glitch_configure, ivi.Doc('\n                        This function configures the glitch trigger. A glitch trigger occurs when\n                        the trigger signal has a pulse with a width that is less than or greater\n                        than the glitch width. The end user specifies which comparison criterion\n                        to use with the GlitchCondition parameter. The end-user specifies the\n                        glitch width with the GlitchWidth parameter. The end-user specifies the\n                        polarity of the pulse with the GlitchPolarity parameter. The trigger does\n                        not actually occur until the edge of a pulse that corresponds to the\n                        GlitchWidth and GlitchPolarity crosses the threshold the end-user\n                        specifies in the TriggerLevel parameter.\n                        \n                        This function affects instrument behavior only if the trigger type is\n                        Glitch Trigger. Set the trigger type and trigger coupling before calling\n                        this function.\n                        ', cls, grp, '8.3.1'))
        return

    def _get_trigger_glitch_condition(self):
        return self._trigger_glitch_condition

    def _set_trigger_glitch_condition(self, value):
        if value not in GlitchCondition:
            raise ivi.ValueNotSupportedException()
        self._trigger_glitch_condition = value

    def _get_trigger_glitch_polarity(self):
        return self._trigger_glitch_polarity

    def _set_trigger_glitch_polarity(self, value):
        if value not in Polarity:
            raise ivi.ValueNotSupportedException()
        self._trigger_glitch_polarity = value

    def _get_trigger_glitch_width(self):
        return self._trigger_glitch_width

    def _set_trigger_glitch_width(self, value):
        value = float(value)
        self._trigger_glitch_width = value

    def _trigger_glitch_configure(self, source, level, width, polarity, condition):
        self._set_trigger_source(source)
        self._set_trigger_level(level)
        self._set_trigger_glitch_width(width)
        self._set_trigger_glitch_polarity(polarity)
        self._set_trigger_glitch_condition(condition)


class WidthTrigger(ivi.IviContainer):
    """Extension IVI methods for oscilloscopes supporting width triggering"""

    def __init__(self, *args, **kwargs):
        super(WidthTrigger, self).__init__(*args, **kwargs)
        cls = 'IviScope'
        grp = 'WidthTrigger'
        ivi.add_group_capability(self, cls + grp)
        self._trigger_width_condition = 'within'
        self._trigger_width_threshold_high = 0
        self._trigger_width_threshold_low = 0
        self._trigger_width_polarity = 'positive'
        self._add_property('trigger.width.condition', self._get_trigger_width_condition, self._set_trigger_width_condition, None, ivi.Doc("\n                        Specifies whether a pulse that is within or outside the high and low\n                        thresholds triggers the oscilloscope. The end-user specifies the high and\n                        low thresholds with the Width High Threshold and Width Low Threshold\n                        attributes.\n                        \n                        Values:\n                        * 'within'\n                        * 'outside'\n                        ", cls, grp, '9.2.1'))
        self._add_property('trigger.width.threshold_high', self._get_trigger_width_threshold_high, self._set_trigger_width_threshold_high, None, ivi.Doc('\n                        Specifies the high width threshold time. Units are seconds.\n                        ', cls, grp, '9.2.2'))
        self._add_property('trigger.width.threshold_low', self._get_trigger_width_threshold_low, self._set_trigger_width_threshold_low, None, ivi.Doc('\n                        Specifies the low width threshold time. Units are seconds.\n                        ', cls, grp, '9.2.3'))
        self._add_property('trigger.width.polarity', self._get_trigger_width_polarity, self._set_trigger_width_polarity, None, ivi.Doc("\n                        Specifies the polarity of the pulse that triggers the oscilloscope.\n                        \n                        Values:\n                        * 'positive'\n                        * 'negative'\n                        * 'either'\n                        ", cls, grp, '9.2.4'))
        self._add_method('trigger.width.configure', self._trigger_width_configure, ivi.Doc('\n                        This function configures the width trigger. A width trigger occurs when\n                        the oscilloscope detects a positive or negative pulse with a width\n                        between, or optionally outside, the width thresholds. The end-user\n                        specifies the width thresholds with the WidthLowThreshold and\n                        WidthHighThreshold parameters. The end-user specifies whether the\n                        oscilloscope triggers on pulse widths that are within or outside the width\n                        thresholds with the WidthCondition parameter. The end-user specifies the\n                        polarity of the pulse with the WidthPolarity parameter. The trigger does\n                        not actually occur until the edge of a pulse that corresponds to the\n                        WidthLowThreshold, WidthHighThreshold, WidthCondition, and WidthPolarity\n                        crosses the threshold the end-user specifies with the TriggerLevel\n                        parameter.\n                        \n                        This function affects instrument behavior only if the trigger type is\n                        Width Trigger. Set the trigger type and trigger coupling before calling\n                        this function.\n                        ', cls, grp, '9.3.1'))
        return

    def _get_trigger_width_condition(self):
        return self._trigger_width_condition

    def _set_trigger_width_condition(self, value):
        if value not in WidthCondition:
            raise ivi.ValueNotSupportedException()
        self._trigger_width_condition = value

    def _get_trigger_width_threshold_high(self):
        return self._trigger_width_threshold_high

    def _set_trigger_width_threshold_high(self, value):
        value = float(value)
        self._trigger_width_threshold_high = value

    def _get_trigger_width_threshold_low(self):
        return self._trigger_width_threshold_low

    def _set_trigger_width_threshold_low(self, value):
        value = float(value)
        self._trigger_width_threshold_low = value

    def _get_trigger_width_polarity(self):
        return self._trigger_width_polarity

    def _set_trigger_width_polarity(self, value):
        if value not in Polarity:
            raise ivi.ValueNotSupportedException()
        self._trigger_width_polarity = value

    def _trigger_width_configure(self, source, level, threshold_low, threshold_high, polarity, condition):
        self._set_trigger_source(source)
        self._set_trigger_level(level)
        self._set_trigger_width_threshold_low(threshold_low)
        self._set_trigger_width_threshold_high(threshold_high)
        self._set_trigger_width_polarity(polarity)
        self._set_trigger_width_condition(condition)


class AcLineTrigger(ivi.IviContainer):
    """Extension IVI methods for oscilloscopes supporting AC line triggering"""

    def __init__(self, *args, **kwargs):
        super(AcLineTrigger, self).__init__(*args, **kwargs)
        cls = 'IviScope'
        grp = 'AcLineTrigger'
        ivi.add_group_capability(self, cls + grp)
        self._trigger_ac_line_slope = 'positive'
        self._add_property('trigger.ac_line.slope', self._get_trigger_ac_line_slope, self._set_trigger_ac_line_slope, None, ivi.Doc("\n                        Specifies the slope of the zero crossing upon which the scope triggers.\n                        \n                        Values:\n                        * 'positive'\n                        * 'negative'\n                        * 'either'\n                        ", cls, grp, '10.2.1'))
        return

    def _get_trigger_ac_line_slope(self):
        return self._trigger_ac_line_slope

    def _set_trigger_ac_line_slope(self, value):
        if value not in Slope:
            raise ivi.ValueNotSupportedException()
        self._trigger_ac_line_slope = value


class WaveformMeasurement(ivi.IviContainer):
    """Extension IVI methods for oscilloscopes supporting waveform measurements"""

    def __init__(self, *args, **kwargs):
        super(WaveformMeasurement, self).__init__(*args, **kwargs)
        cls = 'IviScope'
        grp = 'WaveformMeasurement'
        ivi.add_group_capability(self, cls + grp)
        self._reference_level_high = 90
        self._reference_level_low = 10
        self._reference_level_middle = 50
        self._add_property('reference_level.high', self._get_reference_level_high, self._set_reference_level_high, None, ivi.Doc('\n                        Specifies the high reference the oscilloscope uses for waveform\n                        measurements. The value is a percentage of the difference between the\n                        Voltage High and Voltage Low.\n                        ', cls, grp, '11.2.1'))
        self._add_property('reference_level.middle', self._get_reference_level_middle, self._set_reference_level_middle, None, ivi.Doc('\n                        Specifies the middle reference the oscilloscope uses for waveform\n                        measurements. The value is a percentage of the difference between the\n                        Voltage High and Voltage Low.\n                        ', cls, grp, '11.2.3'))
        self._add_property('reference_level.low', self._get_reference_level_low, self._set_reference_level_low, None, ivi.Doc('\n                        Specifies the low reference the oscilloscope uses for waveform\n                        measurements. The value is a percentage of the difference between the\n                        Voltage High and Voltage Low.\n                        ', cls, grp, '11.2.2'))
        self._add_method('reference_level.configure', self._reference_level_configure, ivi.Doc('\n                        This function configures the reference levels for waveform measurements.\n                        Call this function before calling the Read Waveform Measurement or Fetch\n                        Waveform Measurement to take waveform measurements.\n                        ', cls, grp, '11.3.1'))
        self._add_method('channels[].measurement.fetch_waveform_measurement', self._measurement_fetch_waveform_measurement, ivi.Doc("\n                        This function fetches a specified waveform measurement from a specific\n                        channel from a previously initiated waveform acquisition. If the channel\n                        is not enabled for the acquisition, this function returns the Channel Not\n                        Enabled error.\n                        \n                        This function obtains a waveform measurement and returns the measurement\n                        value. The end-user specifies a particular measurement type, such as rise\n                        time, frequency, and voltage peak-to-peak. The waveform on which the\n                        oscilloscope calculates the waveform measurement is from an acquisition\n                        that was previously initiated.\n                        \n                        Use the Initiate Acquisition function to start an acquisition on the\n                        channels that were enabled with the Configure Channel function. The\n                        oscilloscope acquires waveforms for the enabled channels concurrently. Use\n                        the Acquisition Status function to determine when the acquisition is\n                        complete. Call this function separately for each waveform measurement on a\n                        specific channel.\n                        \n                        The end-user can call the Read Waveform Measurement function instead of\n                        the Initiate Acquisition function. The Read Waveform Measurement function\n                        starts an acquisition on all enabled channels. It then waits for the\n                        acquisition to complete, obtains a waveform measurement on the specified\n                        channel, and returns the measurement value. Call this function separately\n                        to obtain any other waveform measurements on a specific channel.\n                        \n                        Configure the appropriate reference levels before calling this function to\n                        take a rise time, fall time, width negative, width positive, duty cycle\n                        negative, or duty cycle positive measurement.\n                        \n                        The end-user can configure the low, mid, and high references either by\n                        calling the Configure Reference Levels function or by setting the\n                        following attributes.\n                        \n                        * Measurement High Reference\n                        * Measurement Low Reference\n                        * Measurement Mid Reference\n                        \n                        This function does not check the instrument status. Typically, the\n                        end-user calls this function only in a sequence of calls to other\n                        low-level driver functions. The sequence performs one operation. The\n                        end-user uses the low-level functions to optimize one or more aspects of\n                        interaction with the instrument. Call the Error Query function at the\n                        conclusion of the sequence to check the instrument status.\n                        \n                        Values for measurement_function:\n                        * 'rise_time'\n                        * 'fall_time'\n                        * 'frequency'\n                        * 'period'\n                        * 'voltage_rms'\n                        * 'voltage_peak_to_peak'\n                        * 'voltage_max'\n                        * 'voltage_min'\n                        * 'voltage_high'\n                        * 'voltage_low'\n                        * 'voltage_average'\n                        * 'width_negative'\n                        * 'width_positive'\n                        * 'duty_cycle_negative'\n                        * 'duty_cycle_positive'\n                        * 'amplitude'\n                        * 'voltage_cycle_rms'\n                        * 'voltage_cycle_average'\n                        * 'overshoot'\n                        * 'preshoot'\n                        ", cls, grp, '11.3.2'))
        self._add_method('channels[].measurement.read_waveform_measurement', self._measurement_read_waveform_measurement, ivi.Doc('\n                        This function initiates a new waveform acquisition and returns a specified\n                        waveform measurement from a specific channel.\n                        \n                        This function initiates an acquisition on the channels that the end-user\n                        enables with the Configure Channel function. If the channel is not enabled\n                        for the acquisition, this function returns Channel Not Enabled error. It\n                        then waits for the acquisition to complete, obtains a waveform measurement\n                        on the channel the end-user specifies, and returns the measurement value.\n                        The end-user specifies a particular measurement type, such as rise time,\n                        frequency, and voltage peak-to-peak.\n                        \n                        If the oscilloscope did not complete the acquisition within the time\n                        period the user specified with the MaxTimeMilliseconds parameter, the\n                        function returns the Max Time Exceeded error.\n                        \n                        The end-user can call the Fetch Waveform Measurement function separately\n                        to obtain any other waveform measurement on a specific channel without\n                        initiating another acquisition.\n                        \n                        The end-user must configure the appropriate reference levels before\n                        calling this function. Configure the low, mid, and high references either\n                        by calling the Configure Reference Levels function or by setting the\n                        following attributes.\n                        following attributes.\n                        \n                        * Measurement High Reference\n                        * Measurement Low Reference\n                        * Measurement Mid Reference\n                        ', cls, grp, '11.3.3'))
        return

    def _get_reference_level_high(self):
        return self._reference_level_high

    def _set_reference_level_high(self, value):
        value = float(value)
        self._reference_level_high = value

    def _get_reference_level_low(self):
        return self._reference_level_low

    def _set_reference_level_low(self, value):
        value = float(value)
        self._reference_level_low = value

    def _get_reference_level_middle(self):
        return self._reference_level_middle

    def _set_reference_level_middle(self, value):
        value = float(value)
        self._reference_level_middle = value

    def _reference_level_configure(self, low, middle, high):
        self._set_reference_level_low(low)
        self._set_reference_level_middle(middle)
        self._set_reference_level_high(high)

    def _measurement_fetch_waveform_measurement(self, index, measurement_function):
        index = ivi.get_index(self._channel_name, index)
        if measurement_function not in MeasurementFunction:
            raise ivi.ValueNotSupportedException()
        return 0

    def _measurement_read_waveform_measurement(self, index, measurement_function, maximum_time):
        return self._measurement_fetch_waveform_measurement(index, measurement_function)


class MinMaxWaveform(ivi.IviContainer):
    """Extension IVI methods for oscilloscopes supporting minimum and maximum waveform acquisition"""

    def __init__(self, *args, **kwargs):
        super(MinMaxWaveform, self).__init__(*args, **kwargs)
        cls = 'IviScope'
        grp = 'MinMaxWaveform'
        ivi.add_group_capability(self, cls + grp)
        self._acquisition_number_of_envelopes = 0
        self._add_property('acquisition.number_of_envelopes', self._get_acquisition_number_of_envelopes, self._set_acquisition_number_of_envelopes, None, ivi.Doc('\n                        When the end-user sets the Acquisition Type attribute to Envelope, the\n                        oscilloscope acquires multiple waveforms. After each waveform acquisition,\n                        the oscilloscope keeps the minimum and maximum values it finds for each\n                        point in the waveform record. This attribute specifies the number of\n                        waveforms the oscilloscope acquires and analyzes to create the minimum and\n                        maximum waveforms. After the oscilloscope acquires as many waveforms as\n                        this attribute specifies, it returns to the idle state. This attribute\n                        affects instrument operation only when the Acquisition Type attribute is\n                        set to Envelope.\n                        ', cls, grp, '12.2.1'))
        self._add_method('channels[].measurement.fetch_waveform_min_max', self._measurement_fetch_waveform_min_max, ivi.Doc('\n                        This function returns the minimum and maximum waveforms that the\n                        oscilloscope acquires for the specified channel. If the channel is not\n                        enabled for the acquisition, this function returns the Channel Not Enabled\n                        error.\n                        \n                        The waveforms are from a previously initiated acquisition. Use this\n                        function to fetch waveforms when the acquisition type is set to Peak\n                        Detect or Envelope. If the acquisition type is not one of the listed\n                        types, the function returns the Invalid Acquisition Type error.\n                        \n                        Use the Initiate Acquisition function to start an acquisition on the\n                        enabled channels. The oscilloscope acquires the min/max waveforms for the\n                        enabled channels concurrently. Use the Acquisition Status function to\n                        determine when the acquisition is complete. The end-user must call this\n                        function separately for each enabled channel to obtain the min/max\n                        waveforms.\n                        \n                        The end-user can call the Read Min Max Waveform function instead of the\n                        Initiate Acquisition function. The Read Min Max Waveform function starts\n                        an acquisition on all enabled channels, waits for the acquisition to\n                        complete, and returns the min/max waveforms for the specified channel. You\n                        call this function to obtain the min/max waveforms for each of the\n                        remaining channels.\n                        \n                        After this function executes, each element in the MinWaveform and\n                        MaxWaveform parameters is either a voltage or a value indicating that the\n                        oscilloscope could not sample a voltage.\n                        \n                        The return value is a list of (x, y_min, y_max) tuples that represent the\n                        time and voltage of each data point.  Either of the y points may be NaN in\n                        the case that the oscilloscope could not sample the voltage.\n                        \n                        The end-user configures the interpolation method the oscilloscope uses\n                        with the Acquisition.Interpolation property. If interpolation is disabled,\n                        the oscilloscope does not interpolate points in the waveform. If the\n                        oscilloscope cannot sample a value for a point in the waveform, the driver\n                        sets the corresponding element in the waveformArray to an IEEE-defined NaN\n                        (Not a Number) value. Check for this value with math.isnan() or\n                        numpy.isnan(). Check an entire array with\n                        \n                        any(any(math.isnan(b) for b in a) for a in waveform)\n                        \n                        This function does not check the instrument status. Typically, the\n                        end-user calls this function only in a sequence of calls to other\n                        low-level driver functions. The sequence performs one operation. The\n                        end-user uses the low-level functions to optimize one or more aspects of\n                        interaction with the instrument. Call the Error Query function at the\n                        conclusion of the sequence to check the instrument status.\n                        ', cls, grp, '12.3.2'))
        self._add_method('channels[].measurement.read_waveform_min_max', self._measurement_read_waveform_min_max, ivi.Doc('\n                        This function initiates new waveform acquisition and returns minimum and\n                        maximum waveforms from a specific channel. If the channel is not enabled\n                        for the acquisition, this function returns the Channel Not Enabled error.\n                        \n                        This function is used when the Acquisition Type is Peak Detect or\n                        Envelope. If the acquisition type is not one of the listed types, the\n                        function returns the Invalid Acquisition Type error.\n                        \n                        This function initiates an acquisition on the enabled channels. It then\n                        waits for the acquisition to complete, and returns the min/max waveforms\n                        for the specified channel. Call the Fetch Min Max Waveform function to\n                        obtain the min/max waveforms for each of the remaining enabled channels\n                        without initiating another acquisition. If the oscilloscope did not\n                        complete the acquisition within the time period the user specified with\n                        the max_time parameter, the function returns the Max Time Exceeded error.\n                        \n                        The return value is a list of (x, y_min, y_max) tuples that represent the\n                        time and voltage of each data point.  Either of the y points may be NaN in\n                        the case that the oscilloscope could not sample the voltage.\n                        \n                        The end-user configures the interpolation method the oscilloscope uses\n                        with the Acquisition.Interpolation property. If interpolation is disabled,\n                        the oscilloscope does not interpolate points in the waveform. If the\n                        oscilloscope cannot sample a value for a point in the waveform, the driver\n                        sets the corresponding element in the waveformArray to an IEEE-defined NaN\n                        (Not a Number) value. Check for this value with math.isnan() or\n                        numpy.isnan(). Check an entire array with\n                        \n                        any(any(math.isnan(b) for b in a) for a in waveform)\n                        \n                        This function does not check the instrument status. Typically, the\n                        end-user calls this function only in a sequence of calls to other\n                        low-level driver functions. The sequence performs one operation. The\n                        end-user uses the low-level functions to optimize one or more aspects of\n                        interaction with the instrument. Call the Error Query function at the\n                        conclusion of the sequence to check the instrument status.\n                        ', cls, grp, '12.3.3'))
        return

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


class ProbeAutoSense(ivi.IviContainer):
    """Extension IVI methods for oscilloscopes supporting probe attenuation sensing"""

    def __init__(self, *args, **kwargs):
        super(ProbeAutoSense, self).__init__(*args, **kwargs)
        cls = 'IviScope'
        grp = 'ProbeAutoSense'
        ivi.add_group_capability(self, cls + grp)
        self._channel_probe_attenuation_auto = list()
        self._add_property('channels[].probe_attenuation_auto', self._get_channel_probe_attenuation_auto, self._set_channel_probe_attenuation_auto, None, ivi.Doc('\n                        If this attribute is True, the driver configures the oscilloscope to sense\n                        the attenuation of the probe automatically.\n                        \n                        If this attribute is False, the driver disables the automatic probe sense\n                        and configures the oscilloscope to use the value of the Probe Attenuation\n                        attribute.\n                        \n                        The actual probe attenuation the oscilloscope is currently using can be\n                        determined from the Probe Attenuation attribute.\n                        \n                        Setting the Probe Attenuation attribute also sets the Probe Attenuation\n                        Auto attribute to false.\n                        ', cls, grp, '13.2.1'))
        return

    def init_channels(self):
        try:
            super(ProbeAutoSense, self)._init_channels()
        except AttributeError:
            pass

        self._channel_probe_attenuation_auto = list()
        for i in range(self._channel_count):
            self._channel_probe_attenuation_auto.append(True)

    def _get_channel_probe_attenuation_auto(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_probe_attenuation_auto[index]

    def _set_channel_probe_attenuation_auto(self, index, value):
        value = bool(value)
        index = ivi.get_index(self._channel_name, index)
        self._channel_probe_attenuation_auto[index] = value


class ContinuousAcquisition(ivi.IviContainer):
    """Extension IVI methods for oscilloscopes supporting continuous acquisition"""

    def __init__(self, *args, **kwargs):
        super(ContinuousAcquisition, self).__init__(*args, **kwargs)
        cls = 'IviScope'
        grp = 'ContinuousAcquisition'
        ivi.add_group_capability(self, cls + grp)
        self._trigger_continuous = False
        self._add_property('trigger.continuous', self._get_trigger_continuous, self._set_trigger_continuous, None, ivi.Doc('\n                        Specifies whether the oscilloscope continuously initiates waveform\n                        acquisition. If the end-user sets this attribute to True, the oscilloscope\n                        immediately waits for another trigger after the previous waveform\n                        acquisition is complete. Setting this attribute to True is useful when the\n                        end-user requires continuous updates of the oscilloscope display. This\n                        specification does not define the behavior of the read waveform and fetch\n                        waveform functions when this attribute is set to True. The behavior of\n                        these functions is instrument specific.\n                        ', cls, grp, '14.2.1'))
        return

    def _get_trigger_continuous(self):
        return self._trigger_continuous

    def _set_trigger_continuous(self, value):
        self._trigger_continuous = value


class AverageAcquisition(ivi.IviContainer):
    """Extension IVI methods for oscilloscopes supporting average acquisition"""

    def __init__(self, *args, **kwargs):
        super(AverageAcquisition, self).__init__(*args, **kwargs)
        cls = 'IviScope'
        grp = 'AverageAcquisition'
        ivi.add_group_capability(self, cls + grp)
        self._acquisition_number_of_averages = 1
        self._add_property('acquisition.number_of_averages', self._get_acquisition_number_of_averages, self._set_acquisition_number_of_averages, None, ivi.Doc('\n                        Specifies the number of waveform the oscilloscope acquires and averages.\n                        After the oscilloscope acquires as many waveforms as this attribute\n                        specifies, it returns to the idle state. This attribute affects instrument\n                        behavior only when the Acquisition Type attribute is set to Average.\n                        ', cls, grp, '15.2.1'))
        return

    def _get_acquisition_number_of_averages(self):
        return self._acquisition_number_of_averages

    def _set_acquisition_number_of_averages(self, value):
        self._acquisition_number_of_averages = value


class SampleMode(ivi.IviContainer):
    """Extension IVI methods for oscilloscopes supporting equivalent and real time acquisition"""

    def __init__(self, *args, **kwargs):
        super(SampleMode, self).__init__(*args, **kwargs)
        cls = 'IviScope'
        grp = 'SampleMode'
        ivi.add_group_capability(self, cls + grp)
        self._acquisition_sample_mode = 'real_time'
        self._add_property('acquisition.sample_mode', self._get_acquisition_sample_mode, self._set_acquisition_sample_mode, None, ivi.Doc("\n                        Returns the sample mode the oscilloscope is currently using.\n                        \n                        Values:\n                        * 'real_time'\n                        * 'equivalent_time'\n                        ", cls, grp, '16.2.1'))
        return

    def _get_acquisition_sample_mode(self):
        return self._acquisition_sample_mode

    def _set_acquisition_sample_mode(self, value):
        if value not in AcquisitionSampleMode:
            raise ivi.ValueNotSupportedException()
        self._acquisition_sample_mode = value


class TriggerModifier(ivi.IviContainer):
    """Extension IVI methods for oscilloscopes supporting specific triggering subsystem behavior in the absence of a trigger"""

    def __init__(self, *args, **kwargs):
        super(TriggerModifier, self).__init__(*args, **kwargs)
        cls = 'IviScope'
        grp = 'TriggerModifier'
        ivi.add_group_capability(self, cls + grp)
        self._trigger_modifier = 'none'
        self._add_property('trigger.modifier', self._get_trigger_modifier, self._set_trigger_modifier, None, ivi.Doc("\n                        Specifies the trigger modifier. The trigger modifier determines the\n                        oscilloscope's behavior in the absence of the configured trigger.\n                        \n                        Values:\n                        * 'none'\n                        * 'auto'\n                        * 'auto_level'\n                        ", cls, grp, '17.2.1'))
        return

    def _get_trigger_modifier(self):
        return self._trigger_modifier

    def _set_trigger_modifier(self, value):
        if value not in TriggerModifier:
            raise ivi.ValueNotSupportedException()
        self._trigger_modifier = value


class AutoSetup(ivi.IviContainer):
    """Extension IVI methods for oscilloscopes supporting automatic setup"""

    def __init__(self, *args, **kwargs):
        super(AutoSetup, self).__init__(*args, **kwargs)
        cls = 'IviScope'
        grp = 'AutoSetup'
        ivi.add_group_capability(self, cls + grp)
        self._add_method('measurement.auto_setup', self._measurement_auto_setup, ivi.Doc('\n                        This function performs an auto-setup on the instrument.\n                        ', cls, grp, '18.2.1'))

    def _measurement_auto_setup(self):
        pass