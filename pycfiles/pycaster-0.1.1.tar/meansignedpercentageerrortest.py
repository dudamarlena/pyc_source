# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/meansignedpercentageerrortest.py
# Compiled at: 2015-05-28 05:24:14
import unittest
from pycast.errors import MeanSignedPercentageError
import math

class MeanSignedPercentageErrorTest(unittest.TestCase):
    """Test class containing all tests for MeanSignedPercentageError."""

    def setUp(self):
        self.dataOrg = [
         1.0, 2.3, 0.1, -2.0, -1.0, 0.0, -0.2, -0.3, 0.15, -0.2, 0]
        self.dataCalc = [1.2, 2.0, -0.3, -1.5, -1.5, 0.3, 0.0, 0.3, -0.15, 0.3, 0]

    def tearDown(self):
        pass

    def local_error_test(self):
        """Test MeanSignedPercentageError.local_error."""
        localErrors = [
         20, -13.043, -400, -25, 50, None, -100, -200, -200, -250, None]
        mpe = MeanSignedPercentageError()
        for i in xrange(len(self.dataOrg)):
            calc_local_error = mpe.local_error([self.dataOrg[i]], [self.dataCalc[i]])
            if calc_local_error:
                self.assertEquals('%.3f' % calc_local_error, '%.3f' % localErrors[i])
            else:
                self.assertEquals(localErrors[i], None)

        return