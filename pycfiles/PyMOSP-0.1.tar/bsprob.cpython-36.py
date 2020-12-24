# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/problems/bsprob.py
# Compiled at: 2019-09-10 14:12:51
# Size of source mod 2**32: 4091 bytes
__doc__ = '\nSummary\n-------\nProvides implementation of the Bus Scheduling problem for use in PyMOSO.\n'
from ..chnbase import Oracle

class BSProb(Oracle):
    """BSProb"""

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
        return (
         isfeas, (buscost, waitsum))