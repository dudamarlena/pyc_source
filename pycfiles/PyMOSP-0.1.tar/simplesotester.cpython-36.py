# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/testers/simplesotester.py
# Compiled at: 2019-03-26 15:39:40
# Size of source mod 2**32: 1617 bytes
__doc__ = '\nSummary\n-------\nProvide the tester for Test Simple SO problem\n'
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
    return (
     obj1,)


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
    """SimpleSOTester"""

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