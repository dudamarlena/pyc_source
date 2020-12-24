# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_hardware_modules/test_na_iir.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
from pyrpl.attributes import *
from pyrpl import CurveDB
from pyrpl.test.test_base import TestPyrpl

class TestIir(TestPyrpl):

    def setup(self):
        self.extradelay = 4.8e-09
        self.pyrpl.na = self.pyrpl.networkanalyzer
        self.na = self.pyrpl.networkanalyzer

    def teardown(self):
        self.na.stop()

    def test_pz_interface(self):
        """ tests that poles and real/comples_poles remain sync'ed"""
        iir = self.pyrpl.rp.iir
        p = iir.poles = [complex(-2032.0, -1000.0), complex(-3424.0, -34343.0), -1221, -43254.4]
        rp = iir.real_poles
        cp = iir.complex_poles
        assert iir.real_poles == [-1221, -43254.4], iir.real_poles
        assert iir.complex_poles == [complex(-2032.0, 1000.0), complex(-3424.0, 34343.0)], iir.complex_poles
        iir.real_poles = []
        assert iir.complex_poles == [complex(-2032.0, 1000.0), complex(-3424.0, 34343.0)], iir.complex_poles
        assert iir.poles == iir.complex_poles, iir.poles
        iir.complex_poles = []
        assert iir.poles == []
        assert iir.real_poles == []
        assert iir.complex_poles == []
        p = iir.zeros = [
         complex(-2032.0, -1000.0), complex(-3424.0, -34343.0), -1221, -43254.4]
        rp = iir.real_zeros
        cp = iir.complex_zeros
        assert iir.real_zeros == [-1221, -43254.4], iir.real_zeros
        assert iir.complex_zeros == [complex(-2032.0, 1000.0), complex(-3424.0, 34343.0)], iir.complex_zeros
        iir.real_zeros = []
        assert iir.complex_zeros == [complex(-2032.0, 1000.0), complex(-3424.0, 34343.0)], iir.complex_zeros
        assert iir.zeros == iir.complex_zeros, iir.zeros
        iir.complex_zeros = []
        assert iir.zeros == []
        assert iir.real_zeros == []
        assert iir.complex_zeros == []

    def test_iirsimple_na_generator(self):
        extradelay = 0
        error_threshold = 0.25
        na = self.pyrpl.networkanalyzer
        iir = self.pyrpl.rp.iir
        na.setup(start_freq=3000.0, stop_freq=1000000.0, points=301, rbw=[
         500, 500], average_per_point=1, running_state='stopped', trace_average=1, amplitude=0.005, input=iir, output_direct='off', logscale=True)
        zeros = [
         complex(-3000.0, 100000.0)]
        poles = [complex(-3000.0, 50000.0)]
        gain = 1.0
        iir.setup(zeros=zeros, poles=poles, gain=gain, loops=35, input=na.iq, output_direct='off')
        for setting in range(iir._IIRSTAGES):
            iir.on = False
            iir.coefficients = np.roll(iir.coefficients, 6)
            iir.iirfilter._fcoefficients = iir.coefficients
            iir.on = True
            yield (
             self.na_assertion,
             setting, iir, error_threshold, extradelay, True)

    def test_iircomplicated_na_generator(self):
        """
        This test defines a number of complicated IIR transfer functions
        and tests whether the NA response of the filter corresponds to what's
        expected.

        sorry for the ugly code - the test works though
        if there is a problem, no need to try to understand what the code
        does at first (rather read the iir module code):
        Just check the latest new CurveDB curves and for each failed test
        you should find a set of curves whose names indicate the failed
        test, whose parameters show the error between measurement and
        theory, and by comparing the measurement and theory curve you
        should be able to figure out what went wrong in the iir filter...
        """
        extradelay = 0
        error_threshold = 0.005
        if self.r is None:
            return
        else:
            pyrpl = self.pyrpl
            na = self.pyrpl.networkanalyzer
            self.pyrpl.na = na
            iir = pyrpl.rp.iir
            params = []
            z, p, g, loops = (
             np.array([complex(-1510.0000001, 10101.36145285),
              complex(-2100.0000001, 21828.90817759),
              complex(-1000.0000001, 30156.73583005),
              complex(-7100.0000002, 76717.88856012)]),
             np.array([complex(-151.0000001, 16271.51686739),
              complex(-51.0000001, 22342.54324816),
              complex(-10.0000001, 30884.30406145),
              complex(-41.0000001, 32732.52445066),
              complex(-51.0000001, 46953.00496993)]),
             0.03,
             400)
            naset = dict(start_freq=3000.0, stop_freq=50000.0, points=501, rbw=[
             500, 500], average_per_point=1, running_state='stopped', trace_average=1, amplitude=0.05, input=iir, output_direct='off', logscale=True)
            error_threshold = 0.08
            params.append((z, p, g, loops, naset, '0 - low_sampling', error_threshold,
             [
              'final', 'continuous']))
            z = [
             complex(-3000.0, 100000.0)]
            p = [complex(-3000.0, 50000.0)]
            g = 0.5
            loops = None
            naset = dict(start_freq=3000.0, stop_freq=10000000.0, points=301, rbw=[
             500, 500], average_per_point=1, running_state='stopped', trace_average=1, amplitude=0.05, input=iir, output_direct='off', logscale=True)
            error_threshold = 0.05
            params.append((z, p, g, loops, naset, '1 - loops_None', error_threshold,
             [
              'final', 'continuous']))
            z, p, g = np.array([complex(-151.0000001, 10101.36145285),
             complex(-210.0000001, 21828.90817759),
             complex(-100.0000001, 30156.73583005),
             complex(-100.0000001, 32063.2533145),
             complex(-610.0000001, 44654.63524562)]), np.array([complex(-151.0000001, 16271.51686739),
             complex(-51.0000001, 22342.54324816),
             complex(-50.0000001, 30884.30406145),
             complex(-41.0000001, 32732.52445066),
             complex(-51.0000001, 46953.00496993)]), 0.5
            loops = 80
            naset = dict(start_freq=3000.0, stop_freq=50000.0, points=2501, rbw=[
             1000, 1000], average_per_point=5, running_state='stopped', trace_average=1, amplitude=0.02, input=iir, output_direct='off', logscale=True)
            error_threshold = 0.03
            params.append((z, p, g, loops, naset, '2 - loops=80', error_threshold,
             [
              'final', 'continuous']))
            z = [
             +complex(0.0, 40000.0) - 300,
             +complex(0.0, 200000.0) - 3000]
            p = [+complex(0.0, 50000.0) - 300,
             +complex(0.0, 100000.0) - 3000,
             +complex(0.0, 1000000.0) - 30000,
             -500000.0]
            g = 1.0
            loops = None
            naset = dict(start_freq=10000.0, stop_freq=500000.0, points=301, rbw=1000, average_per_point=1, running_state='stopped', trace_average=1, amplitude=0.01, input='iir', output_direct='off', logscale=True)
            error_threshold = [0.04, 0.04]
            params.append((z, p, g, loops, naset, '3 - medium', error_threshold,
             [
              'final', 'continuous']))
            for param in params[2:3]:
                print '\nComplex Iir test with the following params: %s\n' % str(params)
                z, p, g, loops, naset, name, maxerror, kinds = param
                self.pyrpl.na.setup(**naset)
                iir.setup(zeros=z, poles=p, gain=g, loops=loops, input=na.iq, output_direct='off')
                yield (self.na_assertion, name, iir, maxerror, 0, True, True, kinds)

            return

    def na_assertion(self, setting, module, error_threshold=0.1, extradelay=0, relative=False, mean=False, kinds=None):
        """
        helper function: tests if module.transfer_function is within
        error_threshold of the measured transfer function of the module
        """
        na = self.pyrpl.na
        na.input = module
        na._logger.info('Starting NA acquisition...')
        data = na.curve()
        na._logger.info('NA acquisition finished...')
        f = na.data_x
        extrastring = str(setting)
        if not kinds:
            kinds = [
             None]
        for kind in kinds:
            if kind is None:
                theory = module.transfer_function(f, extradelay=extradelay)
                eth = error_threshold
            else:
                extrastring += '_' + kind + '_'
                theory = module.transfer_function(f, extradelay=extradelay, kind=kind)
                try:
                    eth = error_threshold[kinds.index(kind)]
                except:
                    eth = error_threshold

            if relative:
                error = np.abs((data - theory) / theory)
            else:
                error = np.abs(data - theory)
            if mean:
                maxerror = np.mean(error)
            else:
                maxerror = np.max(error)
            if maxerror > eth:
                c = CurveDB.create(f, data, name='test_' + module.name + '_' + extrastring + '_na-failed-data')
                c.params['unittest_relative'] = relative
                c.params['unittest_maxerror'] = maxerror
                c.params['unittest_error_threshold'] = eth
                c.params['unittest_setting'] = setting
                c.save()
                c.add_child(CurveDB.create(f, theory, name='test_' + module.name + '_na-failed-theory'))
                c.add_child(CurveDB.create(f, error, name='test_' + module.name + '_na-failed-error'))
                assert False, (maxerror, setting)

        return