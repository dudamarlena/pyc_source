# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/__init__.py
# Compiled at: 2020-04-22 01:04:47
# Size of source mod 2**32: 1323 bytes
"""
pyEQL
=====

pyEQL is a python package for calculating the properties of aqueous solutions
and performing chemical thermodynamics computations.

:copyright: 2013-2020 by Ryan S. Kingsbury
:license: LGPL, see LICENSE for more details.

"""
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