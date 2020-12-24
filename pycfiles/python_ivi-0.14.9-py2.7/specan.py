# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ivi/specan.py
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

class MarkerNotEnabledException(ivi.IviException):
    pass


class NotDeltaMarkerException(ivi.IviException):
    pass


AmplitudeUnits = set(['dBm', 'dBmV', 'dBuV', 'volt', 'watt'])
DetectorType = set(['auto_peak', 'average', 'maximum_peak', 'minimum_peak', 'sample', 'rms'])
TraceType = set(['clear_write', 'maximum_hold', 'minimum_hold', 'video_average', 'view', 'store'])
VerticalScale = set(['linear', 'logarithmic'])
AcquisitionStatus = set(['complete', 'in_progress', 'unknown'])

class Base(ivi.IviContainer):
    """Base IVI methods for all spectrum analyzers"""

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        cls = 'IviSpecAn'
        grp = 'Base'
        ivi.add_group_capability(self, cls + grp)
        self._trace_count = 1
        self._level_amplitude_units = 'dBm'
        self._level_attenuation = 0.0
        self._level_attenuation_auto = False
        self._acquisition_detector_type = 'sample'
        self._acquisition_detector_type_auto = False
        self._frequency_start = 1000.0
        self._frequency_stop = 1000000000.0
        self._frequency_offset = 0.0
        self._level_input_impedance = 50
        self._acquisition_number_of_sweeps = 1
        self._level_reference = 0.0
        self._level_reference_offset = 0.0
        self._sweep_coupling_resolution_bandwidth = 100.0
        self._sweep_coupling_resolution_bandwidth_auto = False
        self._acquisition_sweep_mode_continuous = True
        self._sweep_coupling_sweep_time = 0.1
        self._sweep_coupling_sweep_time_auto = False
        self._trace_name = list()
        self._trace_type = list()
        self._acquisition_vertical_scale = 'logarithmic'
        self._sweep_coupling_video_bandwidth = 100.0
        self._sweep_coupling_video_bandwidth_auto = False
        self._add_property('level.amplitude_units', self._get_level_amplitude_units, self._set_level_amplitude_units, None, '\n                        Specifies the amplitude units for input, output and display amplitude.\n                        ')
        self._add_property('level.attenuation', self._get_level_attenuation, self._set_level_attenuation, None, '\n                        Specifies the input attenuation (in positive dB).\n                        ')
        self._add_property('level.attenuation_auto', self._get_level_attenuation_auto, self._set_level_attenuation_auto, None, '\n                        If set to True, attenuation is automatically selected. If set to False,\n                        attenuation is manually selected.\n                        ')
        self._add_property('acquisition.detector_type', self._get_acquisition_detector_type, self._set_acquisition_detector_type, None, '\n                        Specifies the detection method used to capture and process the signal.\n                        This governs the data acquisition for a particular sweep, but does not\n                        have any control over how multiple sweeps are processed.\n                        ')
        self._add_property('acquisition.detector_type_auto', self._get_acquisition_detector_type_auto, self._set_acquisition_detector_type_auto, None, '\n                        If set to True, the detector type is automatically selected. The\n                        relationship between Trace Type and Detector Type is not defined by the\n                        specification when the Detector Type Auto is set to True. If set to False,\n                        the detector type is manually selected.\n                        ')
        self._add_property('frequency.start', self._get_frequency_start, self._set_frequency_start, None, "\n                        Specifies the left edge of the frequency domain in Hertz. This is used in\n                        conjunction with the Frequency Stop attribute to define the frequency\n                        domain. If the Frequency Start attribute value is equal to the Frequency\n                        Stop attribute value then the spectrum analyzer's horizontal attributes\n                        are in time-domain.\n                        ")
        self._add_property('frequency.stop', self._get_frequency_stop, self._set_frequency_stop, None, "\n                        Specifies the right edge of the frequency domain in Hertz. This is used in\n                        conjunction with the Frequency Start attribute to define the frequency\n                        domain. If the Frequency Start attribute value is equal to the Frequency\n                        Stop attribute value then the spectrum analyzer's horizontal attributes are\n                        in time-domain.\n                        ")
        self._add_property('frequency.offset', self._get_frequency_offset, self._set_frequency_offset, None, "\n                        Specifies an offset value, in Hertz, that is added to the frequency\n                        readout. The offset is used to compensate for external frequency\n                        conversion. This changes the driver's Frequency Start and Frequency Stop\n                        attributes.\n                        \n                        The equations relating the affected values are:\n                        \n                          Frequency Start = Actual Start Frequency + Frequency Offset\n                          Frequency Stop = Actual Stop Frequency + Frequency Offset\n                          Marker Position = Actual Marker Frequency + Frequency Offset\n                        ")
        self._add_property('level.input_impedance', self._get_level_input_impedance, self._set_level_input_impedance, None, '\n                        Specifies the value of input impedance, in ohms, expected at the active\n                        input port. This is typically 50 ohms or 75 ohms.\n                        ')
        self._add_property('acquisition.number_of_sweeps', self._get_acquisition_number_of_sweeps, self._set_acquisition_number_of_sweeps, None, '\n                        This attribute defines the number of sweeps. This attribute value has no\n                        effect if the Trace Type attribute is set to the value Clear Write.\n                        ')
        self._add_property('level.reference', self._get_level_reference, self._set_level_reference, None, '\n                        The calibrated vertical position of the captured data used as a reference\n                        for amplitude measurements. This is typically set to a value slightly\n                        higher than the highest expected signal level. The units are determined by\n                        the Amplitude Units attribute.\n                        ')
        self._add_property('level.reference_offset', self._get_level_reference_offset, self._set_level_reference_offset, None, '\n                        Specifies an offset for the Reference Level attribute. This value is used\n                        to adjust the reference level for external signal gain or loss. A\n                        positive value corresponds to a gain while a negative number corresponds\n                        to a loss. The value is in dB.\n                        ')
        self._add_property('sweep_coupling.resolution_bandwidth', self._get_sweep_coupling_resolution_bandwidth, self._set_sweep_coupling_resolution_bandwidth, None, '\n                        Specifies the width of the IF filter in Hertz. For more information see\n                        Section 4.1.1, Sweep Coupling Overview.\n                        ')
        self._add_property('sweep_coupling.resolution_bandwidth_auto', self._get_sweep_coupling_resolution_bandwidth_auto, self._set_sweep_coupling_resolution_bandwidth_auto, None, '\n                        If set to True, the resolution bandwidth is automatically selected. If set\n                        to False, the resolution bandwidth is manually selected.\n                        ')
        self._add_property('acquisition.sweep_mode_continuous', self._get_acquisition_sweep_mode_continuous, self._set_acquisition_sweep_mode_continuous, None, '\n                        If set to True, the sweep mode is continuous If set to False, the sweep\n                        mode is not continuous.\n                        ')
        self._add_property('sweep_coupling.sweep_time', self._get_sweep_coupling_sweep_time, self._set_sweep_coupling_sweep_time, None, '\n                        Specifies the length of time to sweep from the left edge to the right edge\n                        of the current domain. The units are seconds.\n                        ')
        self._add_property('sweep_coupling.sweep_time_auto', self._get_sweep_coupling_sweep_time_auto, self._set_sweep_coupling_sweep_time_auto, None, '\n                        If set to True, the sweep time is automatically selected If set to False,\n                        the sweep time is manually selected.\n                        ')
        self._add_property('traces[].name', self._get_trace_name, None, None, '\n                        Returns the physical repeated capability identifier defined by the\n                        specific driver for the trace that corresponds to the index that the user\n                        specifies. If the driver defines a qualified trace name, this property\n                        returns the qualified name.\n                        ')
        self._add_property('traces[].type', self._get_trace_type, self._set_trace_type, None, '\n                        Specifies the representation of the acquired data.\n                        ')
        self._add_property('acquisition.vertical_scale', self._get_acquisition_vertical_scale, self._set_acquisition_vertical_scale, None, '\n                        Specifies the vertical scale of the measurement hardware (use of log\n                        amplifiers versus linear amplifiers).\n                        ')
        self._add_property('sweep_coupling.video_bandwidth', self._get_sweep_coupling_video_bandwidth, self._set_sweep_coupling_video_bandwidth, None, '\n                        Specifies the video bandwidth of the post-detection filter in Hertz.\n                        ')
        self._add_property('sweep_coupling.video_bandwidth_auto', self._get_sweep_coupling_video_bandwidth_auto, self._set_sweep_coupling_video_bandwidth_auto, None, '\n                        If set to True, the video bandwidth is automatically selected. If set to\n                        False, the video bandwidth is manually selected.\n                        ')
        self._add_method('acquisition.abort', self._acquisition_abort, '\n                       This function aborts a previously initiated measurement and returns the\n                       spectrum analyzer to the idle state. This function does not check\n                       instrument status.\n                       ')
        self._add_method('acquisition.status', self._acquisition_status, '\n                       This function determines and returns the status of an acquisition.\n                       ')
        self._add_method('acquisition.configure', self._acquisition_configure, '\n                       This function configures the acquisition attributes of the spectrum\n                       analyzer.\n                       ')
        self._add_method('frequency.configure_center_span', self._frequency_configure_center_span, '\n                       This function configures the frequency range defining the center frequency\n                       and the frequency span. If the span corresponds to zero Hertz, then the\n                       spectrum analyzer operates in time-domain mode. Otherwise, the spectrum\n                       analyzer operates in frequency-domain mode.\n                       \n                       This function modifies the Frequency Start and Frequency Stop attributes as\n                       follows:\n                       \n                         Frequency Start = CenterFrequency - Span / 2\n                         Frequency Stop = CenterFrequency + Span / 2\n                       ')
        self._add_method('frequency.configure_start_stop', self._frequency_configure_start_stop, '\n                       This function configures the frequency range defining its start frequency\n                       and its stop frequency. If the start frequency is equal to the stop\n                       frequency, then the spectrum analyzer operates in time-domain mode.\n                       Otherwise, the spectrum analyzer operates in frequency-domain mode.\n                       ')
        self._add_method('level.configure', self._level_configure, '\n                       This function configures the vertical attributes of the spectrum analyzer.\n                       This corresponds to the Amplitude Units, Input Attenuation, Input\n                       Impedance, Reference Level, and Reference Level Offset attributes.\n                       ')
        self._add_method('sweep_coupling.configure', self._sweep_coupling_configure, '\n                       This function configures the coupling and sweeping attributes. For\n                       additional sweep coupling information refer to Section 4.1.1, Sweep\n                       Coupling Overview.\n                       ')
        self._add_method('traces[].fetch_y', self._trace_fetch_y, '\n                       This function returns the trace the spectrum analyzer acquires. The trace\n                       is from a previously initiated acquisition. The user calls the Initiate\n                       function to start an acquisition. The user calls the Acquisition Status\n                       function to determine when the acquisition is complete.\n                       \n                       The user may call the Read Y Trace function instead of the Initiate\n                       function. This function starts an acquisition, waits for the acquisition\n                       to complete, and returns the trace in one function call.\n                       \n                       The Amplitude array returns data that represents the amplitude of the\n                       signals obtained by sweeping from the start frequency to the stop frequency\n                       (in frequency domain, in time domain the amplitude array is ordered from\n                       beginning of sweep to end). The Amplitude Units attribute determines the\n                       units of the points in the Amplitude array.\n                       \n                       This function does not check the instrument status. The user calls the\n                       Error Query function at the conclusion of the sequence to check the\n                       instrument status.\n                       ')
        self._add_method('acquisition.initiate', self._acquisition_initiate, '\n                       This function initiates an acquisition. After calling this function, the\n                       spectrum analyzer leaves the idle state.\n                       \n                       This function does not check the instrument status. The user calls the\n                       Acquisition Status function to determine when the acquisition is complete.\n                       ')
        self._add_method('traces[].read_y', self._trace_read_y, '\n                       This function initiates a signal acquisition based on the present\n                       instrument configuration. It then waits for the acquisition to complete,\n                       and returns the trace as an array of amplitude values. The amplitude array\n                       returns data that represent the amplitude of the signals obtained by\n                       sweeping from the start frequency to the stop frequency (in frequency\n                       domain, in time domain the amplitude array is ordered from beginning of\n                       sweep to end). The Amplitude Units attribute determines the units of the\n                       points in the amplitude array. This function resets the sweep count.\n                       \n                       If the spectrum analyzer did not complete the acquisition within the time\n                       period the user specified with the MaxTime parameter, the function returns\n                       the Max Time Exceeded error.\n                       ')
        self._init_traces()
        return

    def _init_traces(self):
        try:
            super(Base, self)._init_traces()
        except AttributeError:
            pass

        self._trace_name = list()
        self._trace_type = list()
        for i in range(self._trace_count):
            self._trace_name.append('trace%d' % (i + 1))
            self._trace_type.append('')

        self.traces._set_list(self._trace_name)

    def _get_level_amplitude_units(self):
        return self._level_amplitude_units

    def _set_level_amplitude_units(self, value):
        if value not in AmplitudeUnits:
            raise ivi.ValueNotSupportedException()
        self._level_amplitude_units = value

    def _get_level_attenuation(self):
        return self._level_attenuation

    def _set_level_attenuation(self, value):
        value = float(value)
        self._level_attenuation = value

    def _get_level_attenuation_auto(self):
        return self._level_attenuation_auto

    def _set_level_attenuation_auto(self, value):
        value = bool(value)
        self._level_attenuation_auto = value

    def _get_acquisition_detector_type(self):
        return self._acquisition_detector_type

    def _set_acquisition_detector_type(self, value):
        if value not in DetectorType:
            raise ivi.ValueNotSupportedException()
        self._acquisition_detector_type = value

    def _get_acquisition_detector_type_auto(self):
        return self._acquisition_detector_type_auto

    def _set_acquisition_detector_type_auto(self, value):
        value = bool(value)
        self._acquisition_detector_type_auto = value

    def _get_frequency_start(self):
        return self._frequency_start

    def _set_frequency_start(self, value):
        value = float(value)
        self._frequency_start = value

    def _get_frequency_stop(self):
        return self._frequency_stop

    def _set_frequency_stop(self, value):
        value = float(value)
        self._frequency_stop = value

    def _get_frequency_offset(self):
        return self._frequency_offset

    def _set_frequency_offset(self, value):
        value = float(value)
        self._frequency_offset = value

    def _get_level_input_impedance(self):
        return self._level_input_impedance

    def _set_level_input_impedance(self, value):
        value = float(value)
        self._level_input_impedance = value

    def _get_acquisition_number_of_sweeps(self):
        return self._acquisition_number_of_sweeps

    def _set_acquisition_number_of_sweeps(self, value):
        value = int(value)
        self._acquisition_number_of_sweeps = value

    def _get_level_reference(self):
        return self._level_reference

    def _set_level_reference(self, value):
        value = float(value)
        self._level_reference = value

    def _get_level_reference_offset(self):
        return self._level_reference_offset

    def _set_level_reference_offset(self, value):
        value = float(value)
        self._level_reference_offset = value

    def _get_sweep_coupling_resolution_bandwidth(self):
        return self._sweep_coupling_resolution_bandwidth

    def _set_sweep_coupling_resolution_bandwidth(self, value):
        value = float(value)
        self._sweep_coupling_resolution_bandwidth = value

    def _get_sweep_coupling_resolution_bandwidth_auto(self):
        return self._sweep_coupling_resolution_bandwidth_auto

    def _set_sweep_coupling_resolution_bandwidth_auto(self, value):
        value = bool(value)
        self._sweep_coupling_resolution_bandwidth_auto = value

    def _get_acquisition_sweep_mode_continuous(self):
        return self._acquisition_sweep_mode_continuous

    def _set_acquisition_sweep_mode_continuous(self, value):
        value = bool(value)
        self._acquisition_sweep_mode_continuous = value

    def _get_sweep_coupling_sweep_time(self):
        return self._sweep_coupling_sweep_time

    def _set_sweep_coupling_sweep_time(self, value):
        value = float(value)
        self._sweep_coupling_sweep_time = value

    def _get_sweep_coupling_sweep_time_auto(self):
        return self._sweep_coupling_sweep_time_auto

    def _set_sweep_coupling_sweep_time_auto(self, value):
        value = bool(value)
        self._sweep_coupling_sweep_time_auto = value

    def _get_trace_name(self, index):
        index = ivi.get_index(self._trace_name, index)
        return self._trace_name[index]

    def _get_trace_type(self, index):
        index = ivi.get_index(self._trace_name, index)
        return self._trace_type[index]

    def _set_trace_type(self, index, value):
        index = ivi.get_index(self._trace_name, index)
        if value not in TraceType:
            raise ivi.ValueNotSupportedException()
        self._trace_type[index] = value

    def _get_acquisition_vertical_scale(self):
        return self._acquisition_vertical_scale

    def _set_acquisition_vertical_scale(self, value):
        if value not in VerticalScale:
            raise ivi.ValueNotSupportedException()
        self._acquisition_vertical_scale = value

    def _get_sweep_coupling_video_bandwidth(self):
        return self._sweep_coupling_video_bandwidth

    def _set_sweep_coupling_video_bandwidth(self, value):
        value = float(value)
        self._sweep_coupling_video_bandwidth = value

    def _get_sweep_coupling_video_bandwidth_auto(self):
        return self._sweep_coupling_video_bandwidth_auto

    def _set_sweep_coupling_video_bandwidth_auto(self, value):
        value = bool(value)
        self._sweep_coupling_video_bandwidth_auto = value

    def _acquisition_abort(self):
        pass

    def _acquisition_status(self):
        return 'unknown'

    def _acquisition_configure(self, sweep_mode_continuous, number_of_sweeps, detector_type, vertical_scale):
        self._set_acquisition_sweep_mode_continuous(sweep_mode_continuous)
        self._set_acquisition_number_of_sweeps(number_of_sweeps)
        if detector_type == 'auto' or not detector_type:
            self._set_acquisition_detector_type_auto(True)
        else:
            self._set_acquisition_detector_type_auto(False)
            self._set_acquisition_detector_type(detector_type)
        self._set_acquisition_vertical_scale(vertical_scale)

    def _frequency_configure_center_span(self, center, span):
        self._set_frequency_start(center - span / 2)
        self._set_frequency_stop(center + span / 2)

    def _frequency_configure_start_stop(self, start, stop):
        self._set_frequency_start(start)
        self._set_frequency_stop(stop)

    def _level_configure(self, amplitude_units, input_impedance, reference, reference_offset, attenuation):
        self._set_level_amplitude_units(amplitude_units)
        self._set_level_input_impedance(input_impedance)
        self._set_level_reference(reference)
        self._set_level_reference_offset(reference_offset)
        if attenuation == 'auto':
            self._set_level_attenuation_auto(True)
        else:
            self._set_level_attenuation_auto(False)
            self._set_level_attenuation(attenuation)

    def _sweep_coupling_configure(self, resolution_bandwidth, video_bandwidth, sweep_time):
        if resolution_bandwidth == 'auto':
            self._set_sweep_coupling_resolution_bandwidth_auto(True)
        else:
            self._set_sweep_coupling_resolution_bandwidth_auto(False)
            self._set_sweep_coupling_resolution_bandwidth(resolution_bandwidth)
        if video_bandwidth == 'auto':
            self._set_sweep_coupling_video_bandwidth_auto(True)
        else:
            self._set_sweep_coupling_video_bandwidth_auto(False)
            self._set_sweep_coupling_video_bandwidth(video_bandwidth)
        if sweep_time == 'auto':
            self._set_sweep_coupling_sweep_time_auto(True)
        else:
            self._set_sweep_coupling_sweep_time_auto(False)
            self._set_sweep_coupling_sweep_time(sweep_time)

    def _trace_fetch_y(self, index):
        index = ivi.get_index(self._trace_name, index)
        data = list()
        return data

    def _acquisition_initiate(self):
        pass

    def _trace_read_y(self, index):
        return self._trace_fetch_y(index)


class Multitrace(ivi.IviContainer):
    """Extension IVI methods for spectrum analyzers supporting simple mathematical operations on traces"""

    def __init__(self, *args, **kwargs):
        super(Interpolation, self).__init__(*args, **kwargs)
        cls = 'IviSpecAn'
        grp = 'Multitrace'
        ivi.add_group_capability(self, cls + grp)
        self._add_method('trace_math.add', self._trace_math_add, '\n                       This function modifies a trace to be the point by point sum of two other\n                       traces. Any data in the destination trace is deleted.\n                       \n                         DestinationTrace = Trace1 + Trace2\n                       ')
        self._add_method('trace_math.copy', self._trace_math_copy, '\n                       This function copies the data array from one trace into another trace. Any\n                       data in the Destination Trace is deleted.\n                       ')
        self._add_method('trace_math.exchange', self._trace_math_exchange, '\n                       This function exchanges the data arrays of two traces.\n                       ')
        self._add_method('trace_math.subtract', self._trace_math_subtract, '\n                       This function modifies a trace to be the point by point difference between\n                       two traces. Any data in the destination trace is deleted.\n                       \n                         DestinationTrace = Trace1 - Trace2\n                       ')

    def _trace_math_add(self, dest, trace1, trace2):
        pass

    def _trace_math_copy(self, dest, src):
        pass

    def _trace_math_exchange(self, trace1, trace2):
        pass

    def _trace_math_subtract(self, dest, trace1, trace2):
        pass