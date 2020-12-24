# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/math/testmath.py
# Compiled at: 2010-04-22 06:03:43
import unittest
from scipysim.actors import SisoTestHelper, Channel
import numpy
from scipysim.actors.math import Abs

class AbsTests(unittest.TestCase):
    """Test the absolute actor"""

    def setUp(self):
        """
        Unit test setup code
        """
        self.q_in = Channel()
        self.q_out = Channel()

    def test_positive_integers(self):
        """Test a simple positive integer signal.
        """
        inp = [ {'value': i, 'tag': i} for i in xrange(0, 100, 1) ]
        expected_outputs = inp[:]
        abs = Abs(self.q_in, self.q_out)
        abs.start()
        [ self.q_in.put(val) for val in inp ]
        self.q_in.put(None)
        abs.join()
        for expected_output in expected_outputs:
            out = self.q_out.get()
            self.assertEquals(out['value'], expected_output['value'])
            self.assertEquals(out['tag'], expected_output['tag'])

        self.assertEquals(self.q_out.get(), None)
        return


from ct_integrator_de1 import CTintegratorTest
from dt_integrator import DTIntegratorTests
from derivative import BundleDerivativeTests
from proportional import ProportionalTests
from subtract import SubtractionTests
from summer import SummerTests
if __name__ == '__main__':
    unittest.main()