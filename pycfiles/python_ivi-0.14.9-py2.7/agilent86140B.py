# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ivi/agilent/agilent86140B.py
# Compiled at: 2014-09-01 23:09:59
"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2014 Alex Forencich

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
from .. import ivi
from .. import extra
from .. import scpi
import time
AmplitudeUnitsMapping = {'dBm': 'dbm', 'watt': 'w'}
DetectorType = set(['auto_peak', 'average', 'maximum_peak', 'minimum_peak', 'sample', 'rms'])
TraceType = set(['clear_write', 'maximum_hold', 'minimum_hold', 'video_average', 'view', 'store'])
VerticalScale = set(['linear', 'logarithmic'])
AcquisitionStatus = set(['complete', 'in_progress', 'unknown'])
ScreenshotImageFormatMapping = {'pcl': 'pcl', 
   'cgm': 'cgm', 
   'gif': 'gif'}

class agilent86140B(ivi.Driver, extra.common.Screenshot, scpi.common.Memory):
    """Agilent 86140B Series Optical Spectrum Analyzer Driver"""

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '86140B')
        super(agilent86140B, self).__init__(*args, **kwargs)
        self._memory_size = 10
        self._trace_count = 1
        self._level_amplitude_units = 'dBm'
        self._acquisition_detector_type = 'sample'
        self._acquisition_detector_type_auto = False
        self._wavelength_start = 6e-07
        self._wavelength_stop = 1.7e-06
        self._wavelength_offset = 0.0
        self._acquisition_number_of_sweeps = 1
        self._level_reference = 0.0
        self._level_reference_offset = 0.0
        self._sweep_coupling_resolution_bandwidth = 1.1e-08
        self._sweep_coupling_resolution_bandwidth_auto = False
        self._acquisition_sweep_mode_continuous = True
        self._sweep_coupling_sweep_time = 0.1
        self._sweep_coupling_sweep_time_auto = False
        self._trace_name = list()
        self._trace_type = list()
        self._acquisition_vertical_scale = 'logarithmic'
        self._sweep_coupling_video_bandwidth = 100.0
        self._sweep_coupling_video_bandwidth_auto = False
        self._identity_description = 'Agilent 86140B Series Optical Spectrum Analyzer Driver'
        self._identity_identifier = ''
        self._identity_revision = ''
        self._identity_vendor = ''
        self._identity_instrument_manufacturer = 'Agilent Technologies'
        self._identity_instrument_model = ''
        self._identity_instrument_firmware_revision = ''
        self._identity_specification_major_version = 0
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['86140B', '86141B', '86142B', '86143B',
         '86144B', '86145B', '86146B']
        self._add_property('level.amplitude_units', self._get_level_amplitude_units, self._set_level_amplitude_units, None, '\n                        Specifies the amplitude units for input, output and display amplitude.\n                        ')
        self._add_property('acquisition.detector_type', self._get_acquisition_detector_type, self._set_acquisition_detector_type, None, '\n                        Specifies the detection method used to capture and process the signal.\n                        This governs the data acquisition for a particular sweep, but does not\n                        have any control over how multiple sweeps are processed.\n                        ')
        self._add_property('acquisition.detector_type_auto', self._get_acquisition_detector_type_auto, self._set_acquisition_detector_type_auto, None, '\n                        If set to True, the detector type is automatically selected. The\n                        relationship between Trace Type and Detector Type is not defined by the\n                        specification when the Detector Type Auto is set to True. If set to False,\n                        the detector type is manually selected.\n                        ')
        self._add_property('wavelength.start', self._get_wavelength_start, self._set_wavelength_start, None, "\n                        Specifies the left edge of the wavelength domain in meters. This is used in\n                        conjunction with the Wavelength Stop attribute to define the wavelength\n                        domain. If the Wavelength Start attribute value is equal to the Wavelength\n                        Stop attribute value then the spectrum analyzer's horizontal attributes\n                        are in time-domain.\n                        ")
        self._add_property('wavelength.stop', self._get_wavelength_stop, self._set_wavelength_stop, None, "\n                        Specifies the right edge of the wavelength domain in meters. This is used in\n                        conjunction with the Wavelength Start attribute to define the wavelength\n                        domain. If the Wavelength Start attribute value is equal to the Wavelength\n                        Stop attribute value then the spectrum analyzer's horizontal attributes are\n                        in time-domain.\n                        ")
        self._add_property('wavelength.offset', self._get_wavelength_offset, self._set_wavelength_offset, None, "\n                        Specifies an offset value, in meters, that is added to the wavelength\n                        readout. This changes the driver's Wavelength Start and Wavelength Stop\n                        attributes.\n                        \n                        The equations relating the affected values are:\n                        \n                          Wavelength Start = Actual Start Wavelength + Wavelength Offset\n                          Wavelength Stop = Actual Stop Wavelength + Wavelength Offset\n                          Marker Position = Actual Marker Wavelength + Wavelength Offset\n                        ")
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
        self._add_method('wavelength.configure_center_span', self._wavelength_configure_center_span, '\n                       This function configures the wavelength range defining the center wavelength\n                       and the wavelength span. If the span corresponds to zero meters, then the\n                       spectrum analyzer operates in time-domain mode. Otherwise, the spectrum\n                       analyzer operates in wavelength-domain mode.\n                       \n                       This function modifies the Wavelength Start and Wavelength Stop attributes as\n                       follows:\n                       \n                         Wavelength Start = CenterWavelength - Span / 2\n                         Wavelength Stop = CenterWavelength + Span / 2\n                       ')
        self._add_method('wavelength.configure_start_stop', self._wavelength_configure_start_stop, '\n                       This function configures the wavelength range defining its start wavelength\n                       and its stop wavelength. If the start wavelength is equal to the stop\n                       wavelength, then the spectrum analyzer operates in time-domain mode.\n                       Otherwise, the spectrum analyzer operates in wavelength-domain mode.\n                       ')
        self._add_method('level.configure', self._level_configure, '\n                       This function configures the vertical attributes of the spectrum analyzer.\n                       This corresponds to the Amplitude Units, Input Attenuation, Input\n                       Impedance, Reference Level, and Reference Level Offset attributes.\n                       ')
        self._add_method('sweep_coupling.configure', self._sweep_coupling_configure, '\n                       This function configures the coupling and sweeping attributes. For\n                       additional sweep coupling information refer to Section 4.1.1, Sweep\n                       Coupling Overview.\n                       ')
        self._add_method('traces[].fetch_y', self._trace_fetch_y, '\n                       This function returns the trace the spectrum analyzer acquires. The trace\n                       is from a previously initiated acquisition. The user calls the Initiate\n                       function to start an acquisition. The user calls the Acquisition Status\n                       function to determine when the acquisition is complete.\n                       \n                       The user may call the Read Y Trace function instead of the Initiate\n                       function. This function starts an acquisition, waits for the acquisition\n                       to complete, and returns the trace in one function call.\n                       \n                       The Amplitude array returns data that represents the amplitude of the\n                       signals obtained by sweeping from the start wavelength to the stop wavelength\n                       (in wavelength domain, in time domain the amplitude array is ordered from\n                       beginning of sweep to end). The Amplitude Units attribute determines the\n                       units of the points in the Amplitude array.\n                       \n                       This function does not check the instrument status. The user calls the\n                       Error Query function at the conclusion of the sequence to check the\n                       instrument status.\n                       ')
        self._add_method('acquisition.initiate', self._acquisition_initiate, '\n                       This function initiates an acquisition. After calling this function, the\n                       spectrum analyzer leaves the idle state.\n                       \n                       This function does not check the instrument status. The user calls the\n                       Acquisition Status function to determine when the acquisition is complete.\n                       ')
        self._add_method('traces[].read_y', self._trace_read_y, '\n                       This function initiates a signal acquisition based on the present\n                       instrument configuration. It then waits for the acquisition to complete,\n                       and returns the trace as an array of amplitude values. The amplitude array\n                       returns data that represent the amplitude of the signals obtained by\n                       sweeping from the start wavelength to the stop wavelength (in wavelength\n                       domain, in time domain the amplitude array is ordered from beginning of\n                       sweep to end). The Amplitude Units attribute determines the units of the\n                       points in the amplitude array. This function resets the sweep count.\n                       \n                       If the spectrum analyzer did not complete the acquisition within the time\n                       period the user specified with the MaxTime parameter, the function returns\n                       the Max Time Exceeded error.\n                       ')
        self._init_traces()
        return

    def _initialize(self, resource=None, id_query=False, reset=False, **keywargs):
        """Opens an I/O session to the instrument."""
        super(agilent86140B, self)._initialize(resource, id_query, reset, **keywargs)
        if not self._driver_operation_simulate:
            self._clear()
        if id_query and not self._driver_operation_simulate:
            id = self.identity.instrument_model
            id_check = self._instrument_id
            id_short = id[:len(id_check)]
            if id_short != id_check:
                raise Exception('Instrument ID mismatch, expecting %s, got %s', id_check, id_short)
        if reset:
            self.utility_reset()

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
            error_code, error_message = self._ask(':system:error:next?').split(',')
            error_code = int(error_code)
            error_message = error_message.strip(' "')
        return (
         error_code, error_message)

    def _utility_lock_object(self):
        pass

    def _utility_reset(self):
        if not self._driver_operation_simulate:
            self._write('*RST')
            self._clear()
            self.driver_operation.invalidate_all_attributes()

    def _utility_reset_with_defaults(self):
        self._utility_reset()

    def _utility_self_test(self):
        code = 0
        message = 'Self test passed'
        if not self._driver_operation_simulate:
            code = int(self._ask('*TST?'))
            if code != 0:
                message = 'Self test failed'
        return (
         code, message)

    def _utility_unlock_object(self):
        pass

    def _init_traces(self):
        try:
            super(agilent86140B, self)._init_traces()
        except AttributeError:
            pass

        self._trace_name = list()
        self._trace_type = list()
        for i in range(self._trace_count):
            self._trace_name.append('tr%c' % chr(i + ord('a')))
            self._trace_type.append('')

        self.traces._set_list(self._trace_name)

    def _display_fetch_screenshot(self, format='gif'):
        if self._driver_operation_simulate:
            return ''
        if format not in ScreenshotImageFormatMapping:
            raise ivi.ValueNotSupportedException()
        format = ScreenshotImageFormatMapping[format]
        self._write('hcopy:device:language "%s"' % format)
        self._write('hcopy:data?')
        time.sleep(25)
        return self._read_ieee_block()

    def _get_level_amplitude_units(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask('unit:pow?').lower()
            self._level_amplitude_units = [ k for k, v in AmplitudeUnitsMapping.items() if v == value ][0]
            self._set_cache_valid()
        return self._level_amplitude_units

    def _set_level_amplitude_units(self, value):
        if value not in AmplitudeUnitsMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write('unit:pow %s' % AmplitudeUnitsMapping[value])
        self._level_amplitude_units = value
        self._set_cache_valid()

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

    def _get_wavelength_start(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._wavelength_start = float(self._ask('sense:wavelength:start?'))
            self._set_cache_valid()
        return self._wavelength_start

    def _set_wavelength_start(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write('sense:wavelength:start %e' % value)
        self._wavelength_start = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'sweep_coupling_resolution_bandwidth')

    def _get_wavelength_stop(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._wavelength_stop = float(self._ask('sense:wavelength:stop?'))
            self._set_cache_valid()
        return self._wavelength_stop

    def _set_wavelength_stop(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write('sense:wavelength:stop %e' % value)
        self._wavelength_stop = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'sweep_coupling_resolution_bandwidth')

    def _get_wavelength_offset(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._wavelength_offset = float(self._ask('sense:wavelength:offset?'))
            self._set_cache_valid()
        return self._wavelength_offset

    def _set_wavelength_offset(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write('sense:wavelength:offset %e' % value)
        self._wavelength_offset = value
        self._set_cache_valid()

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
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_coupling_resolution_bandwidth = float(self._ask('sense:bandwidth:resolution?'))
            self._set_cache_valid()
        return self._sweep_coupling_resolution_bandwidth

    def _set_sweep_coupling_resolution_bandwidth(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write('sense:bandwidth:resolution %e' % value)
        self._sweep_coupling_resolution_bandwidth = value
        self._set_cache_valid()

    def _get_sweep_coupling_resolution_bandwidth_auto(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_coupling_resolution_bandwidth_auto = bool(int(self._ask('sense:bandwidth:resolution:auto?')))
            self._set_cache_valid()
        return self._sweep_coupling_resolution_bandwidth_auto

    def _set_sweep_coupling_resolution_bandwidth_auto(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write('sense:bandwidth:resolution:auto %d' % int(value))
        self._sweep_coupling_resolution_bandwidth_auto = value
        self._set_cache_valid()

    def _get_acquisition_sweep_mode_continuous(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_sweep_mode_continuous = bool(int(self._ask('initiate:continuous?')))
            self._set_cache_valid()
        return self._acquisition_sweep_mode_continuous

    def _set_acquisition_sweep_mode_continuous(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write('initiate:continuous %d' % int(value))
        self._acquisition_sweep_mode_continuous = value
        self._set_cache_valid()

    def _get_sweep_coupling_sweep_time(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_coupling_sweep_time = float(self._ask('sense:sweep:time?'))
            self._set_cache_valid()
        return self._sweep_coupling_sweep_time

    def _set_sweep_coupling_sweep_time(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write('sense:sweep:time %e' % value)
        self._sweep_coupling_sweep_time = value
        self._set_cache_valid()

    def _get_sweep_coupling_sweep_time_auto(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_coupling_sweep_time_auto = bool(int(self._ask('sense:sweep:time:auto?')))
            self._set_cache_valid()
        return self._sweep_coupling_sweep_time_auto

    def _set_sweep_coupling_sweep_time_auto(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write('sense:sweep:time:auto %d' % int(value))
        self._sweep_coupling_sweep_time_auto = value
        self._set_cache_valid()

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
        value = float(value)
        self._acquisition_vertical_scale = value

    def _get_sweep_coupling_video_bandwidth(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_coupling_video_bandwidth = float(self._ask('sense:bandwidth:video?'))
            self._set_cache_valid()
        return self._sweep_coupling_video_bandwidth

    def _set_sweep_coupling_video_bandwidth(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write('sense:bandwidth:video %e' % value)
        self._sweep_coupling_video_bandwidth = value
        self._set_cache_valid()

    def _get_sweep_coupling_video_bandwidth_auto(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_coupling_video_bandwidth_auto = bool(int(self._ask('sense:bandwidth:video:auto?')))
            self._set_cache_valid()
        return self._sweep_coupling_video_bandwidth_auto

    def _set_sweep_coupling_video_bandwidth_auto(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write('sense:bandwidth:video:auto %d' % int(value))
        self._sweep_coupling_video_bandwidth_auto = value
        self._set_cache_valid()

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

    def _wavelength_configure_center_span(self, center, span):
        self._set_wavelength_start(center - span / 2)
        self._set_wavelength_stop(center + span / 2)

    def _wavelength_configure_start_stop(self, start, stop):
        self._set_wavelength_start(start)
        self._set_wavelength_stop(stop)

    def _level_configure(self, amplitude_units, reference, reference_offset):
        self._set_level_amplitude_units(amplitude_units)
        self._set_level_reference(reference)
        self._set_level_reference_offset(reference_offset)

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
        name = self._trace_name[index]
        if self._driver_operation_simulate:
            return list()
        self._write('format:data ascii')
        l = self._ask('trace:data:y? %s' % name)
        data = list()
        for p in l.split(','):
            data.append(float(p))

        return data

    def _acquisition_initiate(self):
        if not self._driver_operation_simulate:
            self._write('initiate:immediate')

    def _trace_read_y(self, index):
        return self._trace_fetch_y(index)