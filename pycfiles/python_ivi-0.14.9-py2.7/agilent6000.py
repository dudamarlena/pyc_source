# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ivi/agilent/agilent6000.py
# Compiled at: 2014-04-16 18:42:56
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

class agilent6000(agilentBaseScope):
    """Agilent InfiniiVision 6000 series IVI oscilloscope driver"""

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        super(agilent6000, self).__init__(*args, **kwargs)
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 1000000000.0
        self._identity_description = 'Agilent InfiniiVision 6000 series IVI oscilloscope driver'
        self._identity_supported_instrument_models = ['DSO6012A', 'DSO6014A', 'DSO6032A',
         'DSO6034A', 'DSO6052A', 'DSO6054A', 'DSO6102A', 'DSO6104A', 'MSO6012A', 'MSO6014A',
         'MSO6032A', 'MSO6034A', 'MSO6052A', 'MSO6054A', 'MSO6102A', 'MSO6104A']