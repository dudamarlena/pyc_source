# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/__init__.py
# Compiled at: 2020-04-22 01:04:47
# Size of source mod 2**32: 1323 bytes
__doc__ = '\npyEQL\n=====\n\npyEQL is a python package for calculating the properties of aqueous solutions\nand performing chemical thermodynamics computations.\n\n:copyright: 2013-2020 by Ryan S. Kingsbury\n:license: LGPL, see LICENSE for more details.\n\n'
from pyEQL.database import Paramsdb
paramsDB = Paramsdb()
from pyEQL.parameter import unit
from pyEQL.functions import *
from pyEQL.solution import Solution

class CustomAssertions:

    def assertWithinExperimentalError(self, result, expected, tol=0.05):
        """
        Test whether 'result' is within 'tol' relative error of
        'expected'
        """
        rel_error = abs(result - expected) / expected
        assert rel_error < tol, 'Result {:} differs from expected value by {:.2f}%'.format(result, rel_error * 100)


def test():
    """Run all tests.
    :return: a :class:`unittest.TestResult` object
    """
    from .tests import run
    return run()