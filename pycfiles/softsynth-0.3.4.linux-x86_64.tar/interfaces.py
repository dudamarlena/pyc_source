# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/synth/interfaces.py
# Compiled at: 2015-04-18 11:05:46
import numpy

class SampleGenerator(object):

    def __init__(self, options):
        self.options = options
        self.last_level = 0.0

    def get_samples(self, nr_of_samples, phase, release=None, pitch_bend=None):
        pass

    def get_samples_in_byte_rate(self, nr_of_samples, phase, release=None, pitch_bend=None):
        result = self.get_samples(nr_of_samples, phase, release, pitch_bend)
        if result is None:
            return
        else:
            return numpy.multiply(result, self.options.max_value).astype(int)