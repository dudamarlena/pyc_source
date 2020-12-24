# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ivi/agilent/agilent34401A.py
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
from .. import dmm
from .. import scpi
MeasurementFunctionMapping = {'dc_volts': 'volt', 
   'ac_volts': 'volt:ac', 
   'dc_current': 'curr', 
   'ac_current': 'curr:ac', 
   'two_wire_resistance': 'res', 
   'four_wire_resistance': 'fres', 
   'frequency': 'freq', 
   'period': 'per', 
   'continuity': 'cont', 
   'diode': 'diod'}
MeasurementRangeMapping = {'dc_volts': 'volt:dc:range', 
   'ac_volts': 'volt:ac:range', 
   'dc_current': 'curr:dc:range', 
   'ac_current': 'curr:ac:range', 
   'two_wire_resistance': 'res:range', 
   'four_wire_resistance': 'fres:range'}
MeasurementAutoRangeMapping = {'dc_volts': 'volt:dc:range:auto', 
   'ac_volts': 'volt:ac:range:auto', 
   'dc_current': 'curr:dc:range:auto', 
   'ac_current': 'curr:ac:range:auto', 
   'two_wire_resistance': 'res:range:auto', 
   'four_wire_resistance': 'fres:range:auto'}
MeasurementResolutionMapping = {'dc_volts': 'volt:dc:resolution', 
   'ac_volts': 'volt:ac:resolution', 
   'dc_current': 'curr:dc:resolution', 
   'ac_current': 'curr:ac:resolution', 
   'two_wire_resistance': 'res:resolution', 
   'four_wire_resistance': 'fres:resolution'}

class agilent34401A(scpi.dmm.Base, scpi.dmm.MultiPoint, scpi.dmm.SoftwareTrigger):
    """Agilent 34401A IVI DMM driver"""

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '34401A')
        super(agilent34401A, self).__init__(*args, **kwargs)
        self._memory_size = 5
        self._identity_description = 'Agilent 34401A IVI DMM driver'
        self._identity_identifier = ''
        self._identity_revision = ''
        self._identity_vendor = ''
        self._identity_instrument_manufacturer = 'Agilent Technologies'
        self._identity_instrument_model = ''
        self._identity_instrument_firmware_revision = ''
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = ['34401A']

    def _initialize(self, resource=None, id_query=False, reset=False, **keywargs):
        """Opens an I/O session to the instrument."""
        super(agilent34401A, self)._initialize(resource, id_query, reset, **keywargs)
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