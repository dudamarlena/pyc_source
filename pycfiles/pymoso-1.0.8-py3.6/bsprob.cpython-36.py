# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/problems/bsprob.py
# Compiled at: 2019-09-10 14:12:51
# Size of source mod 2**32: 4091 bytes
"""
Summary
-------
Provides implementation of the Bus Scheduling problem for use in PyMOSO.
"""
from ..chnbase import Oracle

class BSProb(Oracle):
    __doc__ = '\n    An Oracle that simulates the Test Simple SO problem.\n\n    Attributes\n    ----------\n    num_obj : int, 2\n    dim : int\n        The maximum number of buses to schedule between 0 and tau. Default is 9.\n    tau : int\n        The amount of time to simulate passenger arrivals and schedule buses.\n    lambd : float\n        The rate of passenger arrivals. Default is 10.\n    gamma : float\n        Exponential factor of the cost of passengers. Default is 0.5.\n    c0 : float\n        The flat cost of scheduling a bus. Default is 100.\n\n    Parameters\n    ----------\n    rng : prng.MRG32k3a object\n\n    See also\n    --------\n    chnbase.Oracle\n    '

    def __init__(self, rng):
        self.num_obj = 2
        self.dim = 9
        self.tau = 100
        self.lambd = 10
        self.gamma = 0.5
        self.c0 = 100
        super().__init__(rng)

    def g(self, x, rng):
        """
        Simulates one replication of the Bus Scheduling problem. PyMOSO requires
        that all valid Oracles implement an Oracle.g.

        Parameters
        ----------
        x : tuple of int
        rng : prng.MRG32k3a object

        Returns
        -------
        isfeas : bool
        tuple of float
            simulated objective values
        """
        tau = self.tau
        arrlambda = self.lambd
        c0 = self.c0
        gamma = self.gamma
        isfeas = True
        for i in x:
            if i < 0 or i > tau:
                isfeas = False

        waitsum = None
        buscost = None
        if isfeas:
            newx = list(set(sorted(tuple(xi for xi in x if xi > 0 if not xi == tau))))
            if newx:
                num_buses = len(newx)
                numperbus = [0 for bus in newx]
                bustime = newx[0]
            else:
                bustime = tau
            tarrive = 0
            tarrive += rng.expovariate(arrlambda)
            currbus = 0
            waitsum = 0
            numlastbus = 0
            numarrive = 0
            while tarrive <= tau:
                numarrive += 1
                bus_not_found = True
                if tarrive < bustime:
                    if not bustime == tau:
                        numperbus[currbus] += 1
                        bus_not_found = False
                if tarrive > bustime:
                    if bus_not_found:
                        bustime = tau
                        bus_i = 0
                        while bus_i < num_buses and bus_not_found:
                            if newx[bus_i] >= tarrive:
                                if newx[bus_i] < bustime:
                                    bus_not_found = False
                                    bustime = newx[bus_i]
                                    currbus = bus_i
                                    numperbus[bus_i] += 1
                            bus_i += 1

                if bustime == tau:
                    if bus_not_found:
                        numlastbus += 1
                        bus_not_found = True
                waitsum += bustime - tarrive
                tarrive += rng.expovariate(arrlambda)

            if newx:
                buscost1 = sum([c0 + numperbus[bus] ** gamma for bus in range(num_buses)])
            else:
                buscost1 = 0
            buscost2 = c0 + numlastbus ** gamma
            buscost = buscost1 + buscost2
        return (isfeas, (buscost, waitsum))