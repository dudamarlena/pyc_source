# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyrrd\backend\tests\test_bindings.py
# Compiled at: 2013-08-12 02:05:53
from cStringIO import StringIO
import os, sys, tempfile
from unittest import TestCase
from pyrrd.backend import bindings
from pyrrd.exceptions import ExternalCommandError
from pyrrd.rrd import DataSource, RRA, RRD

class BindingsBackendTestCase(TestCase):

    def setUp(self):
        self.ds = [
         DataSource(dsName='speed', dsType='COUNTER', heartbeat=600)]
        self.rra = [
         RRA(cf='AVERAGE', xff=0.5, steps=1, rows=24),
         RRA(cf='AVERAGE', xff=0.5, steps=6, rows=10)]
        self.rrdfile = tempfile.NamedTemporaryFile()
        self.rrd = RRD(self.rrdfile.name, ds=self.ds, rra=self.rra, start=920804400, backend=bindings)
        self.rrd.create()

    def test_infoWriteMode(self):
        expectedOutput = ("\n            rra = [{'rows': 24, 'database': None, 'cf': 'AVERAGE', 'cdp_prep': None, 'beta': None, 'seasonal_period': None, 'steps': 1, 'window_length': None, 'threshold': None, 'alpha': None, 'pdp_per_row': None, 'xff': 0.5, 'ds': [], 'gamma': None, 'rra_num': None}, {'rows': 10, 'database': None, 'cf': 'AVERAGE', 'cdp_prep': None, 'beta': None, 'seasonal_period': None, 'steps': 6, 'window_length': None, 'threshold': None, 'alpha': None, 'pdp_per_row': None, 'xff': 0.5, 'ds': [], 'gamma': None, 'rra_num': None}]\n            filename = /tmp/tmpQCLRj0\n            start = 920804400\n            step = 300\n            values = []\n            ds = [{'name': 'speed', 'min': 'U', 'max': 'U', 'unknown_sec': None, 'minimal_heartbeat': 600, 'value': None, 'rpn': None, 'type': 'COUNTER', 'last_ds': None}]\n            ds[speed].name = speed\n            ds[speed].min = U\n            ds[speed].max = U\n            ds[speed].minimal_heartbeat = 600\n            ds[speed].type = COUNTER\n            rra[0].rows = 24\n            rra[0].cf = AVERAGE\n            rra[0].steps = 1\n            rra[0].xff = 0.5\n            rra[0].ds = []\n            rra[1].rows = 10\n            rra[1].cf = AVERAGE\n            rra[1].steps = 6\n            rra[1].xff = 0.5\n            rra[1].ds = []\n            ").strip().split('\n')
        output = StringIO()
        self.assertTrue(os.path.exists(self.rrdfile.name))
        self.rrd.info(useBindings=True, stream=output)
        for (obtained, expected) in zip(output.getvalue().split('\n'), expectedOutput):
            if obtained.startswith('filename'):
                self.assertTrue(expected.strip().startswith('filename'))
            else:
                self.assertEquals(obtained.strip(), expected.strip())

    def test_infoReadMode(self):
        expectedOutput = '\n            filename = "/tmp/tmpP4bTTy"\n            rrd_version = "0003"\n            step = 300\n            last_update = 920804400\n            header_size = 800\n            ds[speed].index = 0\n            ds[speed].type = "COUNTER"\n            ds[speed].minimal_heartbeat = 600\n            ds[speed].min = NaN\n            ds[speed].max = NaN\n            ds[speed].last_ds = "U"\n            ds[speed].value = 0.0000000000e+00\n            ds[speed].unknown_sec = 0\n            rra[0].cf = "AVERAGE"\n            rra[0].rows = 24\n            rra[0].cur_row = 3\n            rra[0].pdp_per_row = 1\n            rra[0].xff = 5.0000000000e-01\n            rra[0].cdp_prep[0].value = NaN\n            rra[0].cdp_prep[0].unknown_datapoints = 0\n            rra[1].cf = "AVERAGE"\n            rra[1].rows = 10\n            rra[1].cur_row = 2\n            rra[1].pdp_per_row = 6\n            rra[1].xff = 5.0000000000e-01\n            rra[1].cdp_prep[0].value = NaN\n            rra[1].cdp_prep[0].unknown_datapoints = 0\n            '
        rrd = RRD(filename=self.rrdfile.name, mode='r', backend=bindings)
        output = StringIO()
        self.assertTrue(os.path.exists(self.rrdfile.name))
        rrd.info(useBindings=True, stream=output)
        for (obtained, expected) in zip(output.getvalue().split('\n'), expectedOutput):
            print 'obtained:', obtained
            print 'expected:', expected
            if obtained.startswith('filename'):
                self.assertTrue(expected.strip().startswith('filename'))
            else:
                self.assertEquals(obtained.strip(), expected.strip())

        sys.stdout = originalStdout