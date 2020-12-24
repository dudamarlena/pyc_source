# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/hardware_modules/filter.py
# Compiled at: 2017-08-29 09:44:06
from .dsp import DspModule
from ..attributes import FilterRegister

class FilterModule(DspModule):
    inputfilter = FilterRegister(288, filterstages=544, shiftbits=548, minbw=552, doc='Input filter bandwidths [Hz]. 0 = off, positive bandwidth <=> lowpass, negative bandwidth <=> highpass. ')

    @property
    def inputfilter_options(self):
        return self.__class__.inputfilter.valid_frequencies(self)