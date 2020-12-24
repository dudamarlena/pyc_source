# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/testers/simplesotester.py
# Compiled at: 2019-03-26 15:39:40
# Size of source mod 2**32: 1617 bytes
"""
Summary
-------
Provide the tester for Test Simple SO problem
"""
from ..problems import probsimpleso
from ..chnutils import edist

def true_g(x):
    """
    Compute the expected values of a point.

    Parameters
    ----------
    x : tuple of int
        A feasible point

    Returns
    -------
    tuple of float
        The objective values
    """
    obj1 = x[0] ** 2
    return (obj1,)


def get_ranx0(rng):
    """
    Uniformly sample from the feasible space.

    Parameters
    ----------
    rng : prng.MRG32k3a object

    Returns
    -------
    x0 : tuple of int
        The randomly chosen point
    """
    xr = range(-100, 101)
    x1 = rng.choice(xr)
    x0 = (x1,)
    return x0


soln = (0, )

class SimpleSOTester(object):
    __doc__ = "\n    Store useful data for working with Test Simple SO problem.\n\n    Attributes\n    ----------\n    ranorc : chnbase.Oracle class\n    true_g : function\n    soln : list of set of tuple of int\n        The set of LES's which solve TPC locally\n    get_ranx0 : function\n    "

    def __init__(self):
        self.ranorc = probsimpleso.ProbSimpleSO
        self.true_g = true_g
        self.soln = soln
        self.get_ranx0 = get_ranx0

    def metric(self, eles):
        """
        Compute a metric from a simulated solution to the true solution.

        Parameters
        ----------
        eles : set of tuple of numbers
            Simulated solution

        Returns
        -------
        float
            The performance metric
        """
        point = eles.pop()
        dist = edist(point, self.soln)
        return dist