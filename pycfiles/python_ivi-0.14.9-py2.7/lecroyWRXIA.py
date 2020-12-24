# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ivi/lecroy/lecroyWRXIA.py
# Compiled at: 2014-09-01 23:09:59
"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012 Alex Forencich

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
from .lecroyBaseScope import *

def clean_vbs(s):
    """
    Strip out the leading "VBS" that comes from reading string data from the scope using LeCroy VBS commands.
    This function splits the returned string and discards the first item before the space (strips "VBS")
    """
    s = s.split(' ', 1)[1]
    return s


NoiseFilter = set(['None', '0.5bits', '1bits', '1.5bits', '2bits', '2.5bits', '3bits'])
ScreenshotImageFormatMapping = {'bmp': 'bmp', 
   'bmp24': 'bmp', 
   'bmp8': 'bmpcomp', 
   'jpeg': 'jpeg', 
   'png': 'png', 
   'png24': 'png', 
   'psd': 'psd', 
   'tiff': 'tiff'}
TriggerTypes = set(['dropout', 'edge', 'glitch', 'interval', 'logic', 'qualify', 'runt', 'serial', 'slewrate', 'slate', 'tv', 'width'])
ExtTriggerSetting = set(['Ext', 'ExtDivide10', 'Line'])
VerticalCoupling = set(['ac', 'dc', 'gnd'])

class lecroyWRXIA(lecroyBaseScope):
    """LeCroy WaveRunner Xi-A / MXi-A series IVI oscilloscope driver"""

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        super(lecroyWRXIA, self).__init__(*args, **kwargs)
        self._channel_interpolation = list()
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 1000000000.0
        self._display_labels = True
        self._memory_size = 5
        self._identity_description = 'LeCroy WaveRunner Xi-A / MXi-A series IVI oscilloscope driver'
        self._identity_supported_instrument_models = ['WR204MXI-A', 'WR204XI-A', 'WR104MXI-A', 'WR104XI-A', 'WR64MXI-A',
         'WR64XI-A', 'WR62XI-A', 'WR44MXI-A', 'WR44XI-A']
        ivi.add_property(self, 'channels[].noise_filter', self._get_channel_noise_filter, self._set_channel_noise_filter, None, ivi.Doc("\n                        Specifies the channel enhanced noise filter bit setting. Set to 0 to turn off the filter.\n\n                        Values:\n                        * 0.0: 'None'\n                        * 0.5: '0.5bits'\n                        * 1.0: '1bits'\n                        * 1.5: '1.5bits'\n                        * 2.0: '2bits'\n                        * 2.5: '2.5bits'\n                        * 3.0: '3bits'\n                        "))
        ivi.add_property(self, 'channels[].interpolation', self._get_channel_interpolation, self._set_channel_interpolation, None, ivi.Doc('\n                        Specifies the channel interpolation setting. Default is linear.\n\n                        Values:\n                        * Linear: Linear interpolation\n                        * Sinxx: Sinx/x interpolation\n                        '))
        self._init_channels()
        return

    def _get_channel_label(self, index):
        """
        Get the label for the specified channel.
        """
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_label[index] = self._ask('VBS? "Return=app.Acquisition.%s.LabelsText"' % self._channel_name[index])
        self._set_cache_valid(index=index)
        return self._channel_label[index]

    def _set_channel_label(self, index, value):
        """
        Set the label for the specified channel.
        """
        value = str(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write('VBS "app.Acquisition.%s.LabelsText = ""%s"' % (self._channel_name[index], value))
            if self._display_labels == True:
                self._write('VBS "app.Acquisition.%s.ViewLabels = True"' % self._channel_name[index])
        self._channel_label[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_label_position(self, index):
        """
        Get the position of the label in seconds.
        """
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_label[index] = float(self._ask('VBS? "Return=app.Acquisition.%s.LabelsPosition"' % self._channel_name[index]))
        self._set_cache_valid(index=index)
        return self._channel_label_position[index]

    def _set_channel_label_position(self, index, value):
        """
        Set the position of the label in seconds; data should be sent as a float
        ex: 55e-9 will result in a label position of 55 ns

        If display_labels is set to True then the new labels will be shown on the screen
        """
        value = str(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write('VBS "app.Acquisition.%s.LabelsPosition = ""%s"' % (self._channel_name[index], value))
            if self._display_labels == True:
                self._write('VBS "app.Acquisition.%s.ViewLabels = True"' % self._channel_name[index])
        self._channel_label_position[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_bw_limit(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            limits = self._ask('VBS? "Return=app.Acquisition.%s.BandwidthLimit"' % self._channel_name[index])
            if self._channel_name[index] in limits:
                self._channel_bw_limit[index] = limits[(limits.index(self._channel_name[index]) + 1)]
            self._set_cache_valid(index=index)
        return self._channel_bw_limit[index]

    def _set_channel_bw_limit(self, index, value):
        """
        Sets the channel bandwidth limit setting:
        * 200MHz = 200 MHz bandwidth
        * 20MHz = 20 MHz bandwidth
        * Full = full bandwidth
        """
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate:
            self._write('VBS "app.Acquisition.%s.BandwidthLimit = ""%s"' % (self._channel_name[index], value))
        self._channel_bw_limit[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_invert(self, index):
        """
        Returns the status of the channel invert setting.
        * False = Not inverted
        * True = Inverted
        """
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_invert[index] = bool(int(self._ask('VBS? "Return=app.Acquisition.%s.Invert"' % self._channel_name[index])))
            self._set_cache_valid(index=index)
        return self._channel_invert[index]

    def _set_channel_invert(self, index, value):
        """
        Sets the channel invert setting:
        * False = Not inverted
        * True = Inverted
        """
        index = ivi.get_index(self._analog_channel_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write('VBS "app.Acquisition.%s.Invert = %s"' % (self._channel_name[index], value))
        self._channel_invert[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_noise_filter(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_noise_filter[index] = self._ask('VBS? "Return=app.Acquisition.%s.EnhanceResType"' % self._channel_name[index])
            self._set_cache_valid(index=index)
        return self._channel_noise_filter[index]

    def _set_channel_noise_filter(self, index, filtertype):
        """
        Set the channel noise filter setting.

        Valid settings:
        * None
        * 0.5bits
        * 1bits
        * 1.5bits
        * 2bits
        * 2.5bits
        * 3bits
        """
        index = ivi.get_index(self._analog_channel_name, index)
        if filtertype not in NoiseFilter:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write('VBS "app.Acquisition.%s.EnhanceResType = ""%s"' % (self._channel_name[index], filtertype))
        self._channel_noise_filter[index] = str(filtertype)
        self._set_cache_valid(index=index)

    def _get_channel_interpolation(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_interpolation[index] = self._ask('VBS? "Return=app.Acquisition.%s.InterpolateType"' % self._channel_name[index])
            self._set_cache_valid(index=index)
        return self._channel_interpolation[index]

    def _set_channel_interpolation(self, index, interpolate_setting):
        """
        Set the channel interpolation setting.
        """
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate:
            self._write('VBS "app.Acquisition.%s.InterpolateType = ""%s"' % (
             self._channel_name[index], interpolate_setting))
        self._channel_interpolation[index] = interpolate_setting
        self._set_cache_valid(index=index)

    def _get_channel_probe_skew(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_probe_skew[index] = float(self._ask('VBS? "Return=app.Acquisition.%s.Deskew"' % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_probe_skew[index]

    def _set_channel_probe_skew(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write('VBS "app.Acquisition.%s.Deskew = ""%e"' % (self._channel_name[index], value))
        self._channel_probe_skew[index] = value
        self._set_cache_valid(index=index)

    def _get_trigger_source(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask('VBS? "Return=app.Acquisition.Trigger.Source"')
            self._trigger_source = value
            self._set_cache_valid()
        return self._trigger_source

    def _set_trigger_source(self, value):
        value = str(value)
        if value not in self._channel_name and ExtTriggerSetting:
            raise ivi.UnknownPhysicalNameException()
        if not self._driver_operation_simulate:
            self._write('VBS "app.Acquisition.Trigger.Source = ""%s"' % str(value))
        self._trigger_source = value
        self._set_cache_valid()

    def _get_trigger_type(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask('VBS? "Return=app.Acquisition.Trigger.Type"').lower()
            self._trigger_type = value
            self._set_cache_valid()
        return self._trigger_type

    def _set_trigger_type(self, value):
        value = value.lower()
        if value not in TriggerTypes:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write('VBS "app.Acquisition.Trigger.Type = ""%s"' % value)
        self._trigger_type = value
        self._set_cache_valid()

    def _measurement_auto_setup(self):
        if not self._driver_operation_simulate:
            self._write('VBS "app.AutoSetup"')