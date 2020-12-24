# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_lockbox.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
import time, numpy as np
from ..async_utils import sleep as async_sleep
from .test_base import TestPyrpl

class TestLockbox(TestPyrpl):
    source_config_file = 'nosetests_source_lockbox.yml'

    def setup(self):
        self.lockbox = self.pyrpl.lockbox

    def test_create_stage(self):
        old_len = len(self.lockbox.sequence)
        widget = self.lockbox._create_widget()
        self.lockbox.sequence.append({'gain_factor': 2.0})
        assert len(self.lockbox.sequence) == old_len + 1
        async_sleep(0.1)
        assert len(widget.sequence_widget.stage_widgets) == old_len + 1
        self.lockbox.sequence.append({'gain_factor': 3.0})
        assert self.lockbox.sequence[(-1)].gain_factor == 3.0
        assert self.lockbox.sequence[(-2)].name == old_len
        assert self.lockbox.sequence[old_len].gain_factor == 2.0
        self.lockbox.sequence.pop()
        assert len(self.lockbox.sequence) == old_len + 1
        assert self.lockbox.sequence.pop()['gain_factor'] == 2.0

    def test_real_lock(self):
        delay = 0.01
        pid = self.pyrpl.rp.pid1
        pid.i = 0.1
        pid.p = 0.1
        self.lockbox.classname = 'Linear'
        self.lockbox.sequence = []
        self.lockbox.sequence.append({})
        self.lockbox.outputs.output1.p = 0
        self.lockbox.outputs.output1.i = -10.0

    def test_lock(self):
        pass