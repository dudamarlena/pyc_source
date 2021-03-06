# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_hardware_modules/test_dsp_inputs.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
import time, numpy as np
from time import sleep
from qtpy import QtCore, QtWidgets
from pyrpl.test.test_base import TestPyrpl

class TestInput(TestPyrpl):

    def setup(self):
        self.p = self.pyrpl
        self.l = self.pyrpl.lockbox
        self.l.classname = 'Interferometer'

    def teardown(self):
        pass

    def test_input(self):
        self.p.lockbox.sequence[0].input = 'port1'
        assert self.p.lockbox.sequence[0].input == 'port1', self.p.lockbox.sequence[0].input
        self.p.lockbox.sequence[0].input = 'port2'
        assert self.p.lockbox.sequence[0].input == 'port2', self.p.lockbox.sequence[0].input
        self.p.lockbox.sequence[0].input = self.p.lockbox.inputs.port1
        assert self.p.lockbox.sequence[0].input == 'port1', self.p.lockbox.sequence[0].input
        self.p.rp.pid0.input = self.p.lockbox.inputs.port2
        assert self.p.rp.pid0.input == 'lockbox.inputs.port2', self.p.rp.pid0.input
        self.p.rp.pid0.input = self.p.lockbox.sequence[0].input
        assert self.p.rp.pid0.input == 'lockbox.inputs.port1', self.p.rp.pid0.input