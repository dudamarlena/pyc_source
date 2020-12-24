# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/hardware_modules/filter.py
# Compiled at: 2017-08-29 09:44:06
from .dsp import DspModule
from ..attributes import FilterRegister

class FilterModule(DspModule):
    inputfilter = FilterRegister(288, filterstages=544, shiftbits=548, minbw=552, doc='Input filter bandwidths [Hz]. 0 = off, positive bandwidth <=> lowpass, negative bandwidth <=> highpass. ')

    @property
    def inputfilter_options(self):
        return self.__class__.inputfilter.valid_frequencies(self)