# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ivi/agilent/agilentBaseInfiniium.py
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
from .agilentBaseScope import *
AcquisitionModeMapping = {'etim': ('normal', 'equivalent_time'), 
   'rtim': ('normal', 'real_time'), 
   'pdet': ('peak_detect', 'real_time'), 
   'hres': ('high_resolution', 'real_time'), 
   'segm': ('normal', 'segmented'), 
   'segp': ('peak_detect', 'segmented'), 
   'segh': ('high_resolution', 'segmented')}
AcquisitionType = set(['normal', 'peak_detect', 'high_resolution'])
VerticalCoupling = set(['dc'])
ScreenshotImageFormatMapping = {'tif': 'tif', 
   'tiff': 'tif', 
   'bmp': 'bmp', 
   'bmp24': 'bmp', 
   'png': 'png', 
   'png24': 'png', 
   'jpg': 'jpg', 
   'jpeg': 'jpg', 
   'gif': 'gif'}
SampleMode = set(['real_time', 'equivalent_time', 'segmented'])

class agilentBaseInfiniium(agilentBaseScope):
    """Agilent Infiniium series IVI oscilloscope driver"""

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._channel_common_mode = list()
        self._channel_differential = list()
        self._channel_differential_skew = list()
        self._channel_display_auto = list()
        self._channel_display_offset = list()
        self._channel_display_range = list()
        self._channel_display_scale = list()
        super(agilentBaseInfiniium, self).__init__(*args, **kwargs)
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 13000000000.0
        self._horizontal_divisions = 10
        self._vertical_divisions = 8
        self._display_screenshot_image_format_mapping = ScreenshotImageFormatMapping
        self._display_color_grade = False
        self._identity_description = 'Agilent Infiniium series IVI oscilloscope driver'
        self._identity_supported_instrument_models = ['DSO90254A', 'DSO90404A', 'DSO90604A',
         'DSO90804A', 'DSO91204A', 'DSO91304A', 'DSOX91304A', 'DSOX91604A', 'DSOX92004A',
         'DSOX92504A', 'DSOX92804A', 'DSOX93204A', 'DSA90254A', 'DSA90404A', 'DSA90604A',
         'DSA90804A', 'DSA91204A', 'DSA91304A', 'DSAX91304A', 'DSAX91604A', 'DSAX92004A',
         'DSAX92504A', 'DSAX92804A', 'DSAX93204A', 'MSOX91304A', 'MSOX91604A', 'MSOX92004A',
         'MSOX92504A', 'MSOX92804A', 'MSOX93204A']
        self._add_property('display.color_grade', self._get_display_color_grade, self._set_display_color_grade, None, ivi.Doc('\n                        Controls color grade persistance.\n                        \n                        When in the color grade persistance mode, all waveforms are mapped into a\n                        database and shown with different colors representing varying number of\n                        hits in a pixel.  Vector display mode is disabled when color grade is\n                        enabled.\n                        '))
        self._add_method('display.fetch_color_grade_levels', self._fetch_display_color_grade_levels, ivi.Doc('\n                        Returns the range of hits represented by each color.  Fourteen values are\n                        returned, representing the minimum and maximum count for each of seven\n                        colors.  The values are returned in the following order:\n                        \n                        * White minimum value\n                        * White maximum value\n                        * Yellow minimum value\n                        * Yellow maximum value\n                        * Orange minimum value\n                        * Orange maximum value\n                        * Red minimum value\n                        * Red maximum value\n                        * Pink minimum value\n                        * Pink maximum value\n                        * Blue minimum value\n                        * Blue maximum value\n                        * Green minimum value\n                        * Green maximum value\n                        '))
        self._init_channels()
        return

    def _utility_error_query(self):
        error_code = 0
        error_message = 'No error'
        if not self._driver_operation_simulate:
            error_code = self._ask(':system:error?')
            error_code = int(error_code)
            if error_code != 0:
                error_message = 'Unknown'
        return (
         error_code, error_message)

    def _init_channels(self):
        try:
            super(agilentBaseInfiniium, self)._init_channels()
        except AttributeError:
            pass

    def _display_fetch_screenshot(self, format='png', invert=False):
        if self._driver_operation_simulate:
            return ''
        if format not in self._display_screenshot_image_format_mapping:
            raise ivi.ValueNotSupportedException()
        format = self._display_screenshot_image_format_mapping[format]
        self._write(':display:data? %s, screen, on, %s' % (format, 'invert' if invert else 'normal'))
        return self._read_ieee_block()

    def _get_display_vectors(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._display_vectors = bool(int(self._ask(':display:connect?')))
            self._set_cache_valid()
        return self._display_vectors

    def _set_display_vectors(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(':display:connect %d' % int(value))
        self._display_vectors = value
        self._set_cache_valid()

    def _get_display_color_grade(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._display_color_grade = bool(int(self._ask(':display:cgrade?')))
            self._set_cache_valid()
        return self._display_color_grade

    def _set_display_color_grade(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(':display:cgrade %d' % int(value))
        self._display_color_grade = value
        self._set_cache_valid()

    def _fetch_display_color_grade_levels(self):
        if self._driver_operation_simulate():
            return [0] * 14
        lst = self._ask(':display:cgrade:levels?').split(',')
        return [ int(x) for x in lst ]

    def _get_channel_input_impedance(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        self._channel_input_impedance[index] = 50
        return self._channel_input_impedance[index]

    def _set_channel_input_impedance(self, index, value):
        value = float(value)
        index = ivi.get_index(self._analog_channel_name, index)
        if value != 50:
            raise Exception('Invalid impedance selection')
        self._channel_input_impedance[index] = value
        self._set_cache_valid(index=index)

    def _measurement_fetch_waveform(self, index):
        index = ivi.get_index(self._channel_name, index)
        if self._driver_operation_simulate:
            return list()
        self._write(':waveform:byteorder msbfirst')
        self._write(':waveform:format word')
        self._write(':waveform:source %s' % self._channel_name[index])
        pre = self._ask(':waveform:preamble?').split(',')
        format = int(pre[0])
        type = int(pre[1])
        points = int(pre[2])
        count = int(pre[3])
        xincrement = float(pre[4])
        xorigin = float(pre[5])
        xreference = int(float(pre[6]))
        yincrement = float(pre[7])
        yorigin = float(pre[8])
        yreference = int(float(pre[9]))
        if format != 2:
            raise UnexpectedResponseException()
        self._write(':waveform:data?')
        raw_data = self._read_ieee_block()
        data = list()
        for i in range(points):
            x = (i - xreference) * xincrement + xorigin
            yval = struct.unpack('>h', raw_data[i * 2:i * 2 + 2])[0]
            if yval == 31232:
                y = float('nan')
            else:
                y = (yval - yreference) * yincrement + yorigin
            data.append((x, y))

        return data

    def _measurement_read_waveform(self, index, maximum_time):
        return self._measurement_fetch_waveform(index)

    def _measurement_initiate(self):
        if not self._driver_operation_simulate:
            self._write(':acquire:complete 100')
            self._write(':digitize')
            self._set_cache_valid(False, 'trigger_continuous')

    def _get_acquisition_mode(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(':acquire:mode?').lower()
            t = AcquisitionModeMapping[value]
            self._acquisition_type = t[0]
            self._acquisition_sample_mode = t[1]
            self._set_cache_valid()
            self._set_cache_valid(True, 'acquisition_sample_mode')
            self._set_cache_valid(True, 'acquisition_type')

    def _set_acquisition_mode(self, t, value):
        f1 = None
        f2 = None
        if t == 'type':
            f1 = [ k for k, v in AcquisitionModeMapping.items() if v[0] == value ]
            f2 = [ k for k, v in AcquisitionModeMapping.items() if v[1] == self._acquisition_sample_mode and k in f1 ]
        elif t == 'mode':
            f1 = [ k for k, v in AcquisitionModeMapping.items() if v[1] == value ]
            f2 = [ k for k, v in AcquisitionModeMapping.items() if v[0] == self._acquisition_type and k in f1 ]
        if len(f2):
            v = f2[0]
        else:
            v = f1[0]
        t = AcquisitionModeMapping[v]
        if not self._driver_operation_simulate:
            self._write(':acquire:mode %s' % v)
        self._acquisition_type = t[0]
        self._acquisition_sample_mode = t[1]
        self._set_cache_valid()
        self._set_cache_valid(True, 'acquisition_sample_mode')
        self._set_cache_valid(True, 'acquisition_type')
        return

    def _get_acquisition_type(self):
        self._get_acquisition_mode()
        return self._acquisition_type

    def _set_acquisition_type(self, value):
        if value not in AcquisitionType:
            raise ivi.ValueNotSupportedException()
        self._set_acquisition_mode('type', value)

    def _get_acquisition_sample_mode(self):
        self._get_acquisition_mode()
        return self._acquisition_sample_mode

    def _set_acquisition_sample_mode(self, value):
        if value not in SampleMode:
            raise ivi.ValueNotSupportedException()
        self._set_acquisition_mode('mode', value)