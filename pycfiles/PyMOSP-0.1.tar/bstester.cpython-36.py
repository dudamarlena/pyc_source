# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/testers/bstester.py
# Compiled at: 2019-03-26 15:52:14
# Size of source mod 2**32: 1684 bytes
__doc__ = '\nSummary\n-------\nProvide the tester for the Bus Scheduling problem.\n'
from ..problems import bsprob
from math import sqrt

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
    tau = 100
    q = 9
    mr = range(tau)
    x0 = tuple(rng.choice(mr) for i in range(q))
    return x0


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
    lambd = 10
    q = 9
    c0 = 100
    tau = 100
    xext = list(x).extend([0, tau])
    xsrt = sorted(xext)
    obj1 = 0
    obj2 = 0
    for i in range(1, q + 1):
        indic = xsrt[i] - xsrt[(i - 1)]
        pass_cost = sqrt(lamd * indic) if indic > 0 else 0
        fixed_cost = c0 * indic if indic > 0 else 0
        obj1 += pass_cost + fixed_cost
        obj2 += indic ** 2

    return (obj1, obj2 * (lambd / 2.0))


class BSTester(object):
    """BSTester"""

    def __init__(self):
        self.ranorc = bsprob.BSProb
        self.true_g = true_g
        self.get_ranx0 = get_ranx0

    def metric(self, eles):
        """
                Compute a metric from a simulated solution to the true solution. For
                the Bus scheduling problem, the true solution is unkown and this
                function exists to allow using the testsolve command.

                Parameters
                ----------
                eles : set of tuple of numbers
                        Simulated solution

                Returns
                -------
                float
                        The performance metric
                """
        return 0