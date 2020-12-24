# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyrrd\backend\tests\test_external.py
# Compiled at: 2013-08-12 02:05:53
from cStringIO import StringIO
import os, sys, tempfile
from unittest import TestCase
from pyrrd.exceptions import ExternalCommandError
from pyrrd.rrd import DataSource, RRA, RRD

class ExternalBackendTestCase(TestCase):

    def setUp(self):
        ds = [
         DataSource(dsName='speed', dsType='COUNTER', heartbeat=600)]
        rra = [
         RRA(cf='AVERAGE', xff=0.5, steps=1, rows=24),
         RRA(cf='AVERAGE', xff=0.5, steps=6, rows=10)]
        self.rrdfile = tempfile.NamedTemporaryFile()
        self.rrd = RRD(self.rrdfile.name, ds=ds, rra=rra, start=920804400)
        self.rrd.create()

    def test_updateError(self):
        self.rrd.bufferValue(1261214678, 612)
        self.rrd.bufferValue(1261214678, 612)
        self.assertRaises(ExternalCommandError, self.rrd.update)
        expected = 'illegal attempt to update using time 1261214678 when last update time is 1261214678 (minimum one second step)'
        try:
            self.rrd.update()
        except ExternalCommandError, error:
            self.assertTrue(str(error).startswith('ERROR:'))
            self.assertTrue(str(error).endswith(expected))

    def test_infoWriteMode(self):
        expectedOutput = ("\n            rra = [{'rows': 24, 'database': None, 'cf': 'AVERAGE', 'cdp_prep': None, 'beta': None, 'seasonal_period': None, 'steps': 1, 'window_length': None, 'threshold': None, 'alpha': None, 'pdp_per_row': None, 'xff': 0.5, 'ds': [], 'gamma': None, 'rra_num': None}, {'rows': 10, 'database': None, 'cf': 'AVERAGE', 'cdp_prep': None, 'beta': None, 'seasonal_period': None, 'steps': 6, 'window_length': None, 'threshold': None, 'alpha': None, 'pdp_per_row': None, 'xff': 0.5, 'ds': [], 'gamma': None, 'rra_num': None}]\n            filename = /tmp/tmpQCLRj0\n            start = 920804400\n            step = 300\n            values = []\n            ds = [{'name': 'speed', 'min': 'U', 'max': 'U', 'unknown_sec': None, 'minimal_heartbeat': 600, 'value': None, 'rpn': None, 'type': 'COUNTER', 'last_ds': None}]\n            ds[speed].name = speed\n            ds[speed].min = U\n            ds[speed].max = U\n            ds[speed].minimal_heartbeat = 600\n            ds[speed].type = COUNTER\n            rra[0].rows = 24\n            rra[0].cf = AVERAGE\n            rra[0].steps = 1\n            rra[0].xff = 0.5\n            rra[0].ds = []\n            rra[1].rows = 10\n            rra[1].cf = AVERAGE\n            rra[1].steps = 6\n            rra[1].xff = 0.5\n            rra[1].ds = []\n            ").strip().split('\n')
        originalStdout = sys.stdout
        sys.stdout = StringIO()
        self.assertTrue(os.path.exists(self.rrdfile.name))
        self.rrd.info()
        for (obtained, expected) in zip(sys.stdout.getvalue().split('\n'), expectedOutput):
            if obtained.startswith('filename'):
                self.assertTrue(expected.strip().startswith('filename'))
            else:
                self.assertEquals(obtained.strip(), expected.strip())

        sys.stdout = originalStdout