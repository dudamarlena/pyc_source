# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/synth/new_filters.py
# Compiled at: 2015-04-18 11:05:46
from synth.interfaces import SampleGenerator
import numpy

class Delay(SampleGenerator):

    def __init__(self, options, delay_nr_of_samples=4):
        super(Delay, self).__init__(options)
        self.delay_nr_of_samples = delay_nr_of_samples
        self.delayed = numpy.array([])
        self.source = None
        return

    def set_source(self, source):
        self.source = source

    def get_samples(self, nr_of_samples, phase, release=None, pitch_bend=None):
        if self.source is None:
            return numpy.zeros(nr_of_samples)
        else:
            samples = self.source.get_samples(nr_of_samples, phase, release, pitch_bend)
            new_delayed = samples[-self.delay_nr_of_samples:].copy()
            if self.delay_nr_of_samples > nr_of_samples:
                if phase + nr_of_samples > self.delay_nr_of_samples:
                    if phase > self.delay_nr_of_samples:
                        start_index = 0
                    else:
                        start_index = self.delay_nr_of_samples - phase
                    length = nr_of_samples - start_index
                    samples[start_index:] = samples[start_index:] + self.delayed[:length]
                    samples[start_index:] /= 2.0
                    self.delayed = self.delayed[length:]
                self.delayed = numpy.concatenate((self.delayed, new_delayed))
            else:
                delayed = samples[:-self.delay_nr_of_samples]
                samples[(self.delay_nr_of_samples):] = samples[self.delay_nr_of_samples:] + delayed
                if phase > 0:
                    samples[:(self.delay_nr_of_samples)] = samples[:self.delay_nr_of_samples] + self.delayed[:self.delay_nr_of_samples]
                    samples /= 2.0
                else:
                    samples[self.delay_nr_of_samples:] /= 2.0
                self.delayed = new_delayed
            return samples


class DistortionFilter(SampleGenerator):

    def __init__(self, options, level=0.8):
        super(DistortionFilter, self).__init__(options)
        self.level = level
        self.source = None
        return

    def set_source(self, source):
        self.source = source

    def get_samples(self, nr_of_samples, phase, release=None, pitch_bend=None):
        samples = self.source.get_samples(nr_of_samples, phase, release, pitch_bend)
        s1 = numpy.where(samples > self.level, self.level, samples)
        s2 = numpy.where(samples < -self.level, -self.level, samples)
        return s2