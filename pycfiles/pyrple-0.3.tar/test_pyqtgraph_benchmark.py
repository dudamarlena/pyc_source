# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_pyqtgraph_benchmark.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
import pyqtgraph as pg, numpy as np, time
from qtpy import QtCore
from .test_redpitaya import TestRedpitaya
from .. import APP
from ..async_utils import sleep as async_sleep

class TestPyqtgraph(TestRedpitaya):
    """ This test case creates a maximally simplistic scope gui
    that continuously plots the data of both scope channels,
    and checks the obtainable frame rate.
    Frame rates down to 20 Hz are accepted """
    N = 16384
    cycles = 50
    frequency = 10.0
    duration = 1.0
    dt = 0.01
    REDPITAYA = False
    timeout = 10.0

    def setup(self):
        self.t0 = np.linspace(0, self.duration, self.N)
        self.plotWidget = pg.plot(title='Realtime plotting benchmark')
        self.cycle = 0
        self.starttime = time.time()
        if self.REDPITAYA:
            self.r.scope.setup(trigger_source='immediately', duration=self.duration)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000 * self.dt)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def teardown(self):
        self.timer.stop()
        APP.processEvents()
        self.plotWidget.close()
        APP.processEvents()

    def update_plot(self):
        self.cycle += 1
        if self.cycle == 1:
            self.starttime = time.time()
        if self.cycle == self.cycles:
            self.endtime = time.time()
        if self.REDPITAYA:
            t = self.r.scope.times
            y1 = self.r.scope._data_ch1_current
            y2 = self.r.scope._data_ch2_current
        else:
            t = self.t0 + (time.time() - self.starttime)
            phi = 2.0 * np.pi * self.frequency * t
            y1 = np.sin(phi)
            y2 = np.cos(phi)
        if self.cycle == 1:
            self.c1 = self.plotWidget.plot(t, y1, pen='g')
            self.c2 = self.plotWidget.plot(t, y2, pen='r')
        else:
            self.c1.setData(t, y1)
            self.c2.setData(t, y2)

    def test_speed(self):
        while self.cycle < self.cycles or time.time() > self.timeout + self.starttime:
            async_sleep(0.01)

        if self.cycle < self.cycles:
            assert False, 'Must complete %d cycles before testing for speed!' % self.cycles
        else:
            dt = (self.endtime - self.starttime) / self.cycles
            print 'Frame rate: %f Hz' % (1.0 / dt)
            dt *= 1000.0
            print 'Update period: %f ms' % dt
            assert dt < 50.0, 'Frame update time of %f ms with%s redpitaya scope is above specification of 50 ms!' % (
             'out' if self.REDPITAYA else '', dt)