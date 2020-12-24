# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/numeric/tests/test_dejong.py
# Compiled at: 2006-08-09 17:08:27
import unittest
from zope.interface.verify import verifyClass
from numpy import array
from scipy.optimize import fmin_cg
from evogrid.numeric.dejong import test_functions
from evogrid.numeric.interfaces import ITestFunction, INDimTestFunction

def make_test_case(f):

    class BaseDeJongTestCase(unittest.TestCase):
        __module__ = __name__

        def _get_bounds(self, default_amplitude=2000.0):
            bounds = self._get_function().bounds
            if bounds:
                return bounds
            else:
                return (
                 -default_amplitude / 2.0, default_amplitude / 2.0)

        def test_interface(self):
            self.assert_(verifyClass(ITestFunction, self._get_function()))

        def test_minimim_value(self):
            f = self._get_function()
            expected = f.minimum_value
            result = f(f.minimum)
            msg = 'Expected %s(%s)=%r, got %r' % (f.__name__, f.minimum, expected, result)
            self.assert_(abs(expected - result) <= 0.0001, msg)

        def test_minimum(self):
            (lb, ub) = self._get_bounds(default_amplitude=20.0)
            f = self._get_function()

            def check_bounds(x):
                do_raise = False
                for i in range(len(x)):
                    xi = x[i]
                    if xi < lb:
                        x[i] = lb
                        do_raise = True
                    elif xi > ub:
                        x[i] = ub
                        do_raise = True

                if do_raise:
                    raise RuntimeError(x)

            step_number = 5
            step = float(ub - lb) / step_number
            x = lb
            results = {}
            for i in xrange(step_number):
                x += step
                y = lb
                for j in xrange(step_number):
                    y += step
                    x0 = array([x, y], dtype='g')
                    try:
                        xopt = fmin_cg(f, x0, disp=0, maxiter=10, callback=check_bounds)
                    except RuntimeError, e:
                        xopt = e.args[0]

                    results[f(xopt)] = xopt

            fopt = min(results.iterkeys())
            xopt = results[fopt]
            f_expected = f(f.minimum)
            name = f.__name__
            error_msg = '%s(%r)=%r is smaller than expected %s(%r)=%r' % (name, xopt, fopt, name, f.minimum, f_expected)
            self.assert_(fopt - f_expected > -0.0001, error_msg)

    class NDimBaseDeJongTestCase(BaseDeJongTestCase):
        __module__ = __name__

        def test_ndim_evaluation(self):
            (min, max) = self._get_bounds()
            f = self._get_function()
            for dim in xrange(3, 100, 5):
                f(array([min] * dim))
                f(array([max] * dim))
                f(array([(max + min) / 2] * dim))

    name = f.__name__.capitalize() + 'DeJongTestCase'
    if INDimTestFunction.implementedBy(f):
        bases = (
         NDimBaseDeJongTestCase,)
    else:
        bases = (
         BaseDeJongTestCase,)
    return type(name, bases, {'_get_function': lambda self: f})


def test_suite():
    suite = unittest.TestSuite()
    for f in test_functions:
        if f.minimum is None:
            print 'skipped tests for %s' % f.__name__
            continue
        suite.addTests(unittest.makeSuite(make_test_case(f)))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')