# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_hardware_modules/test_sampler.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
from pyrpl.test.test_base import TestPyrpl

class TestInput(TestPyrpl):

    def setup(self):
        self.p = self.pyrpl
        self.sampler = self.r.sampler

    def teardown(self):
        pass

    def test_sampler(self):
        with self.pyrpl.asgs.pop('test_sampler') as (asg):
            asg.setup(amplitude=0.5, offset=0.1, frequency=500000.0, waveform='sin', output_direct='off', trigger_source='immediately')
            sample = getattr(self.sampler, asg.name)
            assert sample >= asg.offset - asg.amplitude, sample
            assert sample <= asg.offset + asg.amplitude, sample
            mean, std, max, min = self.sampler.stats(asg.name, t=1.0)
            assert min <= mean, (mean, std, max, min)
            assert mean <= max, (mean, std, max, min)
            assert std <= (max - min) / 2.0, (mean, std, max, min, (max - min) / 2.0)
            assert max <= asg.offset + asg.amplitude, (mean, std, max, min, asg.offset + asg.amplitude)
            assert min + 6.103515625e-05 >= asg.offset - asg.amplitude, (
             mean, std, max, min, min + 6.103515625e-05, asg.offset - asg.amplitude)