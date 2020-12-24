# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_na.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
import time, copy
from qtpy import QtWidgets, QtCore
from .test_base import TestPyrpl
import numpy as np
from .. import global_config
from ..async_utils import sleep as async_sleep
try:
    from pysine import sine
    raise
except:

    def sine(frequency, duration):
        print 'Called sine(frequency=%f, duration=%f)' % (frequency, duration)


class TestNA(TestPyrpl):

    def setup(self):
        self.na = self.pyrpl.networkanalyzer
        self.r.scope.stop()
        self.pyrpl.spectrumanalyzer.stop()

    def test_first_na_stopped_at_startup(self):
        """
        This was so hard to detect, I am making a unit test
        """
        assert self.na.running_state == 'stopped'

    def teardown(self):
        self.na.stop()

    def test_na_running_states(self):
        with self.pyrpl.networkanalyzer as (self.na):

            def data_changing():
                data = copy.deepcopy(self.na.data_avg)
                async_sleep(self.communication_time * 10 + 0.01)
                return (data != self.na.data_avg).any()

            self.na.setup(start_freq=1000, stop_freq=10000.0, rbw=1000, points=10000, trace_average=1)
            async_sleep(2.0 * self.communication_time)
            self.na.single_async()
            async_sleep(self.communication_time * 5.0 + 0.1)
            assert data_changing()
            current_point = self.na.current_point
            self.na.rbw = 10000
            assert self.na.current_point < current_point
            self.na.continuous()
            async_sleep(self.communication_time * 5.0)
            assert data_changing()
        self.na.stop()

    def test_benchmark_nogui(self):
        """
        test na speed without gui
        """
        with self.pyrpl.networkanalyzer as (self.na):
            try:
                reads_per_na_cycle = global_config.test.reads_per_na_cycle
            except:
                reads_per_na_cycle = 2.9
                logger.info("Could not find global config file entry 'test.reads_per_na_cycle. Assuming default value %.1f.", reads_per_na_cycle)

            maxduration = self.communication_time * reads_per_na_cycle
            points = int(round(10.0 / maxduration))
            self.na.setup(start_freq=1000.0, stop_freq=10000.0, rbw=1000000.0, points=points, running_state='stopped', average_per_point=1, trace_average=1)
            tic = time.time()
            self.na.curve()
            duration = (time.time() - tic) / self.na.points
            assert duration < maxduration, "Na w/o gui should take at most %.1f ms per point, but actually needs %.1f ms. This won't compromise functionality but it is recommended that establish a more direct ethernet connectionto you Red Pitaya module" % (
             maxduration * 1000.0, duration * 1000.0)

    def test_benchmark_gui(self):
        """
        test na speed with gui
        """
        with self.pyrpl.networkanalyzer as (self.na):
            try:
                reads_per_na_cycle = global_config.test.reads_per_na_cycle
            except:
                reads_per_na_cycle = 2.9
                logger.info("Could not find global config file entry 'test.reads_per_na_cycle. Assuming default value %.1f.", reads_per_na_cycle)

            maxduration = self.communication_time * reads_per_na_cycle
            points = int(round(10.0 / maxduration))
            self.na.setup(start_freq=1000.0, stop_freq=10000.0, rbw=1000000.0, points=points // 2, running_state='stopped', average_per_point=1, trace_average=1)
            tic = time.time()
            self.pyrpl.rp.client._sound_debug = False
            sine(1200, 0.5)
            result = self.na.single_async()
            old_read = self.pyrpl.rp.client._read_counter
            old_write = self.pyrpl.rp.client._write_counter
            sine(1400, 0.5)
            result.await_result()
            sine(1500, 0.5)
            while self.na.running_state == 'running_single':
                async_sleep(0.1)

            sine(1600, 0.5)
            max_rw_points = self.na.points
            print 'Reads: %d %d %d. ' % (self.pyrpl.rp.client._read_counter, old_read, max_rw_points)
            assert self.pyrpl.rp.client._read_counter - old_read <= max_rw_points, (
             self.pyrpl.rp.client._read_counter, old_read, max_rw_points)
            print 'Writes: %d %d %d. ' % (self.pyrpl.rp.client._write_counter, old_write, max_rw_points)
            assert self.pyrpl.rp.client._write_counter - old_write <= max_rw_points, (
             self.pyrpl.rp.client._write_counter, old_write, max_rw_points)
            sine(1700, 0.5)
            self.pyrpl.rp.client._sound_debug = False
            duration = (time.time() - tic) / self.na.points
            maxduration *= 2
            assert duration < maxduration, "Na gui should take at most %.1f ms per point, but actually needs %.1f ms. This won't compromise functionality but it is recommended that establish a more direct ethernet connectionto you Red Pitaya module" % (
             maxduration * 1000.0, duration * 1000.0)
            sine(1600, 0.5)

    def coucou(self):
        self.count += 1
        if self.count < self.total:
            self.timer.start()

    def test_stupid_timer(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(2)
        self.timer.setSingleShot(True)
        self.count = 0
        self.timer.timeout.connect(self.coucou)
        async_sleep(0.5)
        tic = time.time()
        self.total = 1000
        self.timer.start()
        while self.count < self.total:
            async_sleep(0.05)

        duration = time.time() - tic
        assert duration < 3.0, duration

    def test_get_curve(self):
        with self.pyrpl.networkanalyzer as (self.na):
            self.na.iq.output_signal = 'quadrature'
            self.na.setup(amplitude=1.0, start_freq=100000.0, stop_freq=200000.0, rbw=10000, points=100, avg_per_point=10, input=self.na.iq, acbandwidth=0)
            y = self.na.curve()
            assert all(abs(y - 1) < 0.1)

    def test_iq_stopped_when_paused(self):
        with self.pyrpl.networkanalyzer as (self.na):
            self.na.setup(start_freq=100000.0, stop_freq=200000.0, rbw=100000, points=100, output_direct='out1', input='out1', running_state='stopped', trace_average=1, amplitude=0.01)
            self.na.continuous()
            async_sleep(0.05)
            self.na.pause()
            async_sleep(0.05)
            assert self.na.iq.amplitude == 0
            self.na.continuous()
            async_sleep(0.05)
            assert self.na.iq.amplitude != 0
            self.na.stop()
            async_sleep(0.05)
            assert self.na.iq.amplitude == 0

    def test_iq_autosave_active(self):
        """
        At some point, iq._autosave_active was reinitialized by iq
        create_widget...
        """
        assert self.na.iq._autosave_active == False

    def test_no_write_in_config(self):
        """
        Make sure the na isn't continuously writing to config file,
        even in running mode.
        :return:
        """
        with self.pyrpl.networkanalyzer as (self.na):
            self.na.setup(start_freq=100000.0, stop_freq=200000.0, rbw=100000, points=10, output_direct='out1', input='out1', amplitude=0.01, trace_average=1, running_state='running_continuous')
            old = self.pyrpl.c._save_counter
            for i in range(10):
                async_sleep(0.01)

            new = self.pyrpl.c._save_counter
            self.na.stop()
            assert old == new, (old, new)

    def test_save_curve(self):
        self.na.setup(start_freq=100000.0, stop_freq=200000.0, rbw=100000, points=10, output_direct='out1', input='out1', amplitude=0.01, trace_average=1, running_state='running_continuous')
        self.na.single()
        curve = self.na.save_curve()
        self.na.stop()
        assert len(curve.data[0]) == self.na.points
        assert len(curve.data[1]) == self.na.points
        self.curves.append(curve)