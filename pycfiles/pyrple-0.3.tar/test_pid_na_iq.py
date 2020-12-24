# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_hardware_modules/test_pid_na_iq.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
from pyrpl.attributes import *
from pyrpl import CurveDB
from pyrpl.test.test_base import TestPyrpl

class TestPidNaIq(TestPyrpl):

    def setup(self):
        self.extradelay = 4.8e-09
        self.pyrpl.na = self.pyrpl.networkanalyzer
        self.na = self.pyrpl.networkanalyzer

    def teardown(self):
        self.na.stop()

    def test_na(self):
        error_threshold = 0.03
        if self.r is None:
            return
        else:
            r = self.r
            extradelay = self.extradelay
            na = self.pyrpl.na
            for iq in [r.iq0, r.iq1, r.iq2]:
                na._iq = iq
                na.setup(start_freq=3000, stop_freq=10000000.0, points=101, rbw=1000, average_per_point=1, trace_average=1, amplitude=0.1, input=na.iq, output_direct='off', acbandwidth=1000, logscale=True)
                data = na.curve()
                f = na.data_x
                theory = np.array(f * 0 + 1.0, dtype=np.complex)
                relerror = np.abs((data - theory) / theory)
                maxerror = np.max(relerror)
                if maxerror > error_threshold:
                    print maxerror
                    c = CurveDB.create(f, data, name='test_na-failed-data')
                    c.add_child(CurveDB.create(f, theory, name='test_na-failed-theory'))
                    c.add_child(CurveDB.create(f, relerror, name='test_na-failed-relerror'))
                    assert False, maxerror

            return

    def test_inputfilter(self):
        """
        tests whether the modeled transfer function of pid module with
        any possible inputfilter (firstorder) corresponds to measured tf
        """
        error_threshold = 0.3
        pid = self.pyrpl.rp.pid0
        na = self.pyrpl.na
        na.setup(start_freq=10000.0, stop_freq=5000000.0, points=11, rbw=1000, average_per_point=1, trace_average=1, amplitude=0.1, input=pid, output_direct='off', acbandwidth=0, logscale=True)
        pid.input = na.iq
        pid.setpoint = 0
        extradelay = self.extradelay
        pid.p = 1.0
        pid.i = 0
        pid.d = 0
        pid.ival = 0
        pid.inputfilter
        inputfilters = pid.inputfilter_options
        for bw in reversed(inputfilters):
            pid.inputfilter = [
             bw]
            data = na.curve()
            f = na.data_x
            theory = pid.transfer_function(f, extradelay=extradelay)
            relerror = np.abs((data - theory) / theory)
            mask = np.asarray(np.abs(theory) > 0.003, dtype=np.float)
            maxerror = np.max(relerror * mask)
            if maxerror > error_threshold:
                print maxerror
                c = CurveDB.create(f, data, name='test_inputfilter-failed-data')
                c.params['bandwidth'] = pid.inputfilter[0]
                c.save()
                c.add_child(CurveDB.create(f, theory, name='test_inputfilter-failed-theory'))
                c.add_child(CurveDB.create(f, relerror, name='test_inputfilter-failed-relerror'))
                assert False, (maxerror, bw)

    def test_pid_na1(self):
        error_threshold = 0.03
        if self.r is None:
            return
        else:
            r = self.r
            plotdata = []
            na = self.pyrpl.na
            for pid in self.pyrpl.pids.all_modules:
                na.setup(start_freq=1000, stop_freq=1000000.0, points=11, rbw=100, average_per_point=1, trace_average=1, amplitude=0.1, input=pid, output_direct='off', acbandwidth=0, logscale=True)
                pid.input = na.iq
                pid.setpoint = 0
                extradelay = self.extradelay
                pid.p = 1.0
                pid.i = 0
                pid.d = 0
                pid.ival = 0
                pid.inputfilter = 0
                data = na.curve()
                f = na.data_x
                plotdata.append((f, data, 'p=1'))
                theory = pid.transfer_function(f, extradelay=extradelay)
                relerror = np.abs((data - theory) / theory)
                maxerror = np.max(relerror)
                if maxerror > error_threshold:
                    print maxerror
                    c = CurveDB.create(f, data, name='test_na_pid-failed-data')
                    c.add_child(CurveDB.create(f, theory, name='test_na_pid-failed-theory'))
                    c.add_child(CurveDB.create(f, relerror, name='test_na_pid-failed-relerror'))
                    assert False, maxerror

            return

    def test_pid_na2(self):
        error_threshold = 0.04
        plotdata = []
        na = self.pyrpl.na
        for pid in self.pyrpl.pids.all_modules:
            na.setup(start_freq=1000, stop_freq=1000000.0, points=11, rbw=100, average_per_point=1, trace_average=1, amplitude=0.1, input=pid, output_direct='off', acbandwidth=0, logscale=True)
            pid.input = na.iq
            pid.setpoint = 0
            extradelay = self.extradelay
            pid.p = 0.025
            pid.i = 250
            pid.d = 0
            pid.ival = 0
            pid.inputfilter = 0
            data = na.curve()
            f = na.data_x
            plotdata.append((f, data, 'p=%.1e, i=%.1e' % (pid.p, pid.i)))
            theory = pid.transfer_function(f, extradelay=extradelay)
            relerror = np.abs((data - theory) / theory)
            maxerror = np.max(relerror)
            if maxerror > error_threshold:
                print maxerror
                c = CurveDB.create(f, data, name='test_na_pid-failed-data')
                c.add_child(CurveDB.create(f, theory, name='test_na_pid-failed-theory'))
                c.add_child(CurveDB.create(f, relerror, name='test_na_pid-failed-relerror'))
                assert False, maxerror
            print ('Integral value after measurement: ', pid.ival)
            if abs(pid.ival) >= 1.0:
                print 'Saturation has occured. Data not reliable.'
            assert abs(pid.ival) <= 1.0, pid.ival

    def test_pid_na3(self):
        error_threshold = 0.1
        if self.r is None:
            return
        else:
            r = self.r
            plotdata = []
            na = self.pyrpl.na
            for pid in self.pyrpl.pids.all_modules:
                na.setup(start_freq=1000, stop_freq=1000000.0, points=11, rbw=100, average_per_point=10, trace_average=1, amplitude=0.1, input=pid, output_direct='off', acbandwidth=0, logscale=True)
                pid.input = na.iq
                pid.setpoint = 0
                extradelay = self.extradelay
                pid.p = 10
                pid.i = 0
                pid.d = 0
                pid.ival = 0
                pid.inputfilter = [-5000.0, -10000.0, 150000.0, 300000.0]
                print ('Actual inputfilter after rounding: ', pid.inputfilter)
                data = na.curve()
                f = na.data_x
                plotdata.append((f, data, 'p=10 + filter'))
                theory = pid.transfer_function(f, extradelay=extradelay)
                relerror = np.abs((data - theory) / theory)
                maxerror = np.max(relerror)
                if maxerror > error_threshold:
                    print maxerror
                    c = CurveDB.create(f, data, name='test_na_pid-failed-data')
                    c.add_child(CurveDB.create(f, theory, name='test_na_pid-failed-theory'))
                    c.add_child(CurveDB.create(f, relerror, name='test_na_pid-failed-relerror'))
                    assert False, maxerror
                pid.setpoint = 0
                pid.p = 0
                pid.i = 0
                pid.d = 0
                pid.ival = 0
                pid.inputfilter = 0

            return

    def test_iq_na(self):
        extradelay = 0
        error_threshold = 0.07
        if self.r is None:
            return
        else:
            r = self.r
            plotdata = []
            na = self.pyrpl.networkanalyzer
            for bpf in [r.iq0, r.iq2]:
                plotdata = []
                na.setup(start_freq=300000.0, stop_freq=700000.0, points=51, rbw=1000, average_per_point=3, trace_average=1, acbandwidth=0, amplitude=0.2, input=bpf, output_direct='off', logscale=False)
                bpf.setup(frequency=500000.0, bandwidth=5000, acbandwidth=500, phase=0, gain=1.0, output_direct='off', output_signal='output_direct', input=na.iq)
                for phase in [-45, 0, 45, 90]:
                    bpf.phase = phase
                    data = na.curve()
                    f = na.data_x
                    theory = bpf.transfer_function(f, extradelay=extradelay)
                    abserror = np.abs(data - theory)
                    maxerror = np.max(abserror)
                    if maxerror > error_threshold:
                        print maxerror
                        c = CurveDB.create(f, data, name='test_iq_na-failed-data')
                        c.add_child(CurveDB.create(f, theory, name='test_iq_na-failed-theory'))
                        c.add_child(CurveDB.create(f, abserror, name='test_iq_na-failed-relerror'))
                        assert False, (maxerror, phase)

            return