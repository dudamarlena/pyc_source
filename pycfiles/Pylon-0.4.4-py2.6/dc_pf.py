# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pylon\dc_pf.py
# Compiled at: 2010-12-26 13:36:33
""" Defines a solver for DC power flow.
"""
import time, logging, math
from numpy import array, linalg, pi, r_, ix_
from scipy.sparse.linalg import spsolve
from pylon.case import REFERENCE, PV, PQ
logger = logging.getLogger(__name__)

class DCPF(object):
    """ Solves DC power flow.

    Based on dcpf.m from MATPOWER by Ray Zimmerman, developed at PSERC
    Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more info.
    """

    def __init__(self, case):
        """ Initialises a DCPF instance.
        """
        self.case = case
        self.v_angle = None
        return

    def solve(self):
        """ Solves a DC power flow.
        """
        case = self.case
        logger.info('Starting DC power flow [%s].' % case.name)
        t0 = time.time()
        self.case.index_buses()
        ref_idx = self._get_reference_index(case)
        if ref_idx < 0:
            return False
        (B, Bsrc, p_businj, p_srcinj) = case.Bdc
        v_angle_guess = self._get_v_angle_guess(case)
        (v_angle, p_ref) = self._get_v_angle(case, B, v_angle_guess, p_businj, ref_idx)
        logger.debug('Bus voltage phase angles: \n%s' % v_angle)
        self.v_angle = v_angle
        self._update_model(case, B, Bsrc, v_angle, p_srcinj, p_ref, ref_idx)
        logger.info('DC power flow completed in %.3fs.' % (time.time() - t0))
        return True

    def _get_reference_index(self, case):
        """ Returns the index of the reference bus.
        """
        refs = [ bus._i for bus in case.connected_buses if bus.type == REFERENCE ]
        if len(refs) == 1:
            return refs[0]
        else:
            logger.error('Single swing bus required for DCPF.')
            return -1

    def _get_v_angle_guess(self, case):
        """ Make the vector of voltage phase guesses.
        """
        v_angle = array([ bus.v_angle * (pi / 180.0) for bus in case.connected_buses
                        ])
        return v_angle

    def _get_v_angle(self, case, B, v_angle_guess, p_businj, iref):
        """ Calculates the voltage phase angles.
        """
        buses = case.connected_buses
        pv_idxs = [ bus._i for bus in buses if bus.type == PV ]
        pq_idxs = [ bus._i for bus in buses if bus.type == PQ ]
        pvpq_idxs = pv_idxs + pq_idxs
        pvpq_rows = [ [i] for i in pvpq_idxs ]
        Bpvpq = B[(pvpq_rows, pvpq_idxs)]
        Bref = B[(pvpq_rows, [iref])]
        p_surplus = array([ case.s_surplus(v).real for v in buses ])
        g_shunt = array([ bus.g_shunt for bus in buses ])
        Pbus = (p_surplus - p_businj - g_shunt) / case.base_mva
        Pbus.shape = (
         len(Pbus), 1)
        A = Bpvpq
        b = Pbus[pvpq_idxs] - Bref * v_angle_guess[iref]
        x = spsolve(A, b)
        v_angle = r_[(x[:iref], v_angle_guess[iref], x[iref:])]
        return (
         v_angle, Pbus[iref])

    def _update_model(self, case, B, Bsrc, v_angle, p_srcinj, p_ref, ref_idx):
        """ Updates the case with values computed from the voltage phase
            angle solution.
        """
        iref = ref_idx
        base_mva = case.base_mva
        buses = case.connected_buses
        branches = case.online_branches
        p_from = (Bsrc * v_angle + p_srcinj) * base_mva
        p_to = -p_from
        for (i, branch) in enumerate(branches):
            branch.p_from = p_from[i]
            branch.p_to = p_to[i]
            branch.q_from = 0.0
            branch.q_to = 0.0

        for (j, bus) in enumerate(buses):
            bus.v_angle = v_angle[j] * (180 / pi)
            bus.v_magnitude = 1.0

        g_ref = [ g for g in case.generators if g.bus == buses[iref] ][0]
        p_inj = (B[iref, :] * v_angle - p_ref) * base_mva
        g_ref.p += p_inj[0]