# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/numeric/tests/test_variators.py
# Compiled at: 2006-08-10 03:59:18
import unittest
from zope.interface.verify import verifyClass
from numpy import array, square
from math import sqrt
from evogrid.interfaces import IVariator
from evogrid.common.replicators import Replicator
from evogrid.numeric.dejong import DeJongEvaluator
from evogrid.numeric.variators import SimplexVariator, BfgsVariator, CgVariator, PowellVariator
variator_klasses = (
 SimplexVariator, BfgsVariator, CgVariator, PowellVariator)

def make_test_case(klass):

    class BaseVariatorTestCase(unittest.TestCase):
        __module__ = __name__
        klass = None

        def setUp(self):
            self.evaluator = DeJongEvaluator(4)
            self.variator = self.klass(self.evaluator)
            cs0 = array([-1.0, -1.0])
            self.rep = Replicator(cs=cs0)
            self.ev0 = self.evaluator.compute_fitness(cs0)

        def test_interface(self):
            self.assert_(verifyClass(IVariator, self.klass))

        def test_default_maxiter(self):
            rep = self.rep
            self.assertEquals(self.variator.maxiter, 10)
            result = self.variator.combine(rep)
            expected = (rep,)
            self.assertEquals(result, expected)
            ev = self.evaluator.compute_fitness(rep.candidate_solution)
            self.assert_(ev < self.ev0, 'fitness was not minimized')

        def test_maxiter_none(self):
            rep = self.rep
            self.variator = self.klass(self.evaluator, maxiter=None)
            maxiter = self.variator.maxiter
            self.assert_(maxiter is None)
            result = self.variator.combine(rep)
            expected = (rep,)
            self.assertEquals(result, expected)
            ev = self.evaluator.compute_fitness(rep.candidate_solution)
            self.assert_(ev < self.ev0, 'fitness was not minimized')
            cs = rep.candidate_solution
            d = sqrt(square(cs - array([1.0, 1.0])).sum())
            self.assert_(d < 0.001, 'algorithm stopped at %r' % cs)
            return

    name = klass.__name__ + 'TestCase'
    return type(name, (BaseVariatorTestCase,), {'klass': klass})


def test_suite():
    suite = unittest.TestSuite()
    for variator_klass in variator_klasses:
        suite.addTests(unittest.makeSuite(make_test_case(variator_klass)))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')