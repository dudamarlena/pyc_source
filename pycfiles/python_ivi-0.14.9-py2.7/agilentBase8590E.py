# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ivi/agilent/agilentBase8590E.py
# Compiled at: 2014-09-01 23:09:59
"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2013-2014 Alex Forencich

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
from .agilentBase8590 import *

class agilentBase8590E(agilentBase8590):
    """Agilent 8590E series IVI spectrum analyzer driver"""

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        super(agilentBase8590E, self).__init__(*args, **kwargs)
        self._identity_description = 'Agilent 8590 series IVI spectrum analyzer driver'
        self._identity_supported_instrument_models = ['8590E', '8590L', '8591C', '8591E', '8591EM', '8592L',
         '8593E', '8593EM', '8594E', '8594EM', '8594L', '8594Q', '8595E', '8595EM', '8596E',
         '8596EM']