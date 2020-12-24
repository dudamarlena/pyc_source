# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_hardware_modules/test_trig.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
import time, numpy as np
from time import sleep
from qtpy import QtCore, QtWidgets
from pyrpl.test.test_base import TestPyrpl

class TestScope(TestPyrpl):

    def setup(self):
        self.asg = self.pyrpl.asgs.pop('trigtest')
        self.t = self.pyrpl.rp.trig

    def teardown(self):
        self.pyrpl.asgs.free(self.asg)

    def test_trigger(self):
        self.asg = self.pyrpl.rp.asg0
        self.asg.setup(amplitude=0, offset=0.5, waveform='sin', output_direct='off')
        self.t.setup(input=self.asg, output_direct='off', threshold=self.asg.offset, hysteresis=0.001, armed=True, auto_rearm=False, trigger_source='pos_edge', output_signal='asg0_phase')
        assert self.t.armed == True
        self.asg.setup(frequency=10000.0, amplitude=0.4, offset=0.5, waveform='sin', output_direct='off', trigger_source='immediately')
        assert self.t.armed == False
        asg0phase = self.t.output_signal_to_phase(self.pyrpl.rp.sampler.trig)
        assert abs(asg0phase) <= 1.0, asg0phase
        self.t.trigger_source = 'neg_edge'
        self.t.armed = True
        asg0phase = self.t.output_signal_to_phase(self.pyrpl.rp.sampler.trig)
        assert abs(asg0phase - 180.0) <= 1.0, asg0phase
        self.asg.frequency = 10000000.0
        self.t.auto_rearm = True
        self.t.armed = True
        armed = 0
        for i in range(100):
            if self.t.armed:
                armed += 1

        assert armed >= 99, armed
        self.t.auto_rearm = False
        assert self.t.armed == False