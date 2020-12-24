# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pylon\estimator.py
# Compiled at: 2010-12-26 13:36:33
""" Defines a state estimator.

Based on code in MATPOWER by Rui Bo and James S. Thorp, developed at PSERC
Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more info.
"""
import logging
from time import time
from numpy import array, pi, angle, abs, ones, exp, linalg, conj, zeros, r_, Inf
from scipy.sparse import csr_matrix, vstack, hstack
from scipy.sparse.linalg import spsolve
from case import PV, PQ
logger = logging.getLogger(__name__)
PF = 'Pf'
PT = 'Pt'
QF = 'Qf'
QT = 'Qt'
PG = 'Pg'
QG = 'Qg'
VA = 'Va'
VM = 'Vm'
CASE_GUESS = 'case guess'
FLAT_START = 'flat start'
FROM_INPUT = 'from input'

class StateEstimator(object):
    """ State estimation.

    Based on code in MATPOWER by Rui Bo and James S. Thorp, developed at PSERC
    Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more info.
    """

    def __init__(self, case, measurements, sigma=None, v_mag_guess=None, max_iter=100, tolerance=1e-05, verbose=True):
        """ Initialises a new StateEstimator instance.
        """
        self.case = case
        self.measurements = measurements
        self.sigma = zeros(8) if sigma is None else sigma
        self.v_mag_guess = v_mag_guess
        self.max_iter = max_iter
        self.tolerance = tolerance
        self.verbose = verbose
        return

    def run(self):
        """ Solves a state estimation problem.
        """
        case = self.case
        baseMVA = case.base_mva
        buses = self.case.connected_buses
        branches = case.online_branches
        generators = case.online_generators
        meas = self.measurements
        self.case.index_buses()
        self.case.index_branches()
        pv = [ b._i for b in buses if b.type == PV ]
        pq = [ b._i for b in buses if b.type == PQ ]
        (Ybus, Yf, Yt) = case.Y
        V0 = self.getV0(self.v_mag_guess, buses, generators)
        t0 = time()
        converged = False
        i = 0
        V = V0
        Va = angle(V0)
        Vm = abs(V0)
        nb = Ybus.shape[0]
        f = [ b.from_bus._i for b in branches ]
        t = [ b.to_bus._i for b in branches ]
        nonref = pv + pq
        z = array([ m.value for m in meas ])
        idx_zPf = [ m.b_or_l._i for m in meas if m.type == PF ]
        idx_zPt = [ m.b_or_l._i for m in meas if m.type == PT ]
        idx_zQf = [ m.b_or_l._i for m in meas if m.type == QF ]
        idx_zQt = [ m.b_or_l._i for m in meas if m.type == QT ]
        idx_zPg = [ m.b_or_l._i for m in meas if m.type == PG ]
        idx_zQg = [ m.b_or_l._i for m in meas if m.type == QG ]
        idx_zVm = [ m.b_or_l._i for m in meas if m.type == VM ]
        idx_zVa = [ m.b_or_l._i for m in meas if m.type == VA ]

        def col(seq):
            return [ [k] for k in seq ]

        sigma_vector = r_[(
         self.sigma[0] * ones(len(idx_zPf)),
         self.sigma[1] * ones(len(idx_zPt)),
         self.sigma[2] * ones(len(idx_zQf)),
         self.sigma[3] * ones(len(idx_zQt)),
         self.sigma[4] * ones(len(idx_zPg)),
         self.sigma[5] * ones(len(idx_zQg)),
         self.sigma[6] * ones(len(idx_zVm)),
         self.sigma[7] * ones(len(idx_zVa)))]
        sigma_squared = sigma_vector ** 2
        rsig = range(len(sigma_squared))
        Rinv = csr_matrix((1.0 / sigma_squared, (rsig, rsig)))
        while not converged and i < self.max_iter:
            i += 1
            Sfe = V[f] * conj(Yf * V)
            Ste = V[t] * conj(Yt * V)
            gbus = [ g.bus._i for g in generators ]
            Sgbus = V[gbus] * conj(Ybus[gbus, :] * V)
            Sd = array([ complex(b.p_demand, b.q_demand) for b in buses ])
            Sgen = (Sgbus * baseMVA + Sd) / baseMVA
            z_est = r_[(
             Sfe[idx_zPf].real,
             Ste[idx_zPt].real,
             Sfe[idx_zQf].imag,
             Ste[idx_zQt].imag,
             Sgen[idx_zPg].real,
             Sgen[idx_zQg].imag,
             abs(V[idx_zVm]),
             angle(V[idx_zVa]))]
            (dSbus_dVm, dSbus_dVa) = case.dSbus_dV(Ybus, V)
            (dSf_dVa, dSf_dVm, dSt_dVa, dSt_dVm, _, _) = case.dSbr_dV(Yf, Yt, V)
            dPF_dVa = dSf_dVa.real
            dQF_dVa = dSf_dVa.imag
            dPF_dVm = dSf_dVm.real
            dQF_dVm = dSf_dVm.imag
            dPT_dVa = dSt_dVa.real
            dQT_dVa = dSt_dVa.imag
            dPT_dVm = dSt_dVm.real
            dQT_dVm = dSt_dVm.imag
            dPG_dVa = dSbus_dVa[gbus, :].real
            dQG_dVa = dSbus_dVa[gbus, :].imag
            dPG_dVm = dSbus_dVm[gbus, :].real
            dQG_dVm = dSbus_dVm[gbus, :].imag
            dVa_dVa = csr_matrix((ones(nb), (range(nb), range(nb))))
            dVa_dVm = csr_matrix((nb, nb))
            dVm_dVa = csr_matrix((nb, nb))
            dVm_dVm = csr_matrix((ones(nb), (range(nb), range(nb))))
            h = [
             (
              col(idx_zPf), dPF_dVa, dPF_dVm),
             (
              col(idx_zQf), dQF_dVa, dQF_dVm),
             (
              col(idx_zPt), dPT_dVa, dPT_dVm),
             (
              col(idx_zQt), dQT_dVa, dQT_dVm),
             (
              col(idx_zPg), dPG_dVa, dPG_dVm),
             (
              col(idx_zQg), dQG_dVa, dQG_dVm),
             (
              col(idx_zVm), dVm_dVa, dVm_dVm),
             (
              col(idx_zVa), dVa_dVa, dVa_dVm)]
            H = vstack([ hstack([dVa[(idx, nonref)], dVm[(idx, nonref)]]) for (idx, dVa, dVm) in h if len(idx) > 0
                       ])
            J = H.T * Rinv * H
            F = H.T * Rinv * (z - z_est)
            dx = spsolve(J, F)
            normF = linalg.norm(F, Inf)
            if self.verbose:
                logger.info('Iteration [%d]: Norm of mismatch: %.3f' % (
                 i, normF))
            if normF < self.tolerance:
                converged = True
            npvpq = len(nonref)
            Va[nonref] = Va[nonref] + dx[:npvpq]
            Vm[nonref] = Vm[nonref] + dx[npvpq:2 * npvpq]
            V = Vm * exp(complex(0.0, 1.0) * Va)
            Va = angle(V)
            Vm = abs(V)

        error_sqrsum = sum((z - z_est) ** 2 / sigma_squared)
        case.pf_solution(Ybus, Yf, Yt, V)
        elapsed = time() - t0
        if self.verbose and converged:
            print 'State estimation converged in: %.3fs (%d iterations)' % (
             elapsed, i)
        solution = {'V': V, 'converged': converged, 'iterations': i, 'z': z, 
           'z_est': z_est, 'error_sqrsum': error_sqrsum, 'elapsed': elapsed}
        return solution

    def getV0(self, v_mag_guess, buses, generators, type=CASE_GUESS):
        """ Returns the initial voltage profile.
        """
        if type == CASE_GUESS:
            Va = array([ b.v_angle * (pi / 180.0) for b in buses ])
            Vm = array([ b.v_magnitude for b in buses ])
            V0 = Vm * exp(complex(0.0, 1.0) * Va)
        elif type == FLAT_START:
            V0 = ones(len(buses))
        elif type == FROM_INPUT:
            V0 = v_mag_guess
        else:
            raise ValueError
        gbus = [ g.bus._i for g in generators ]
        Vg = array([ g.v_magnitude for g in generators ])
        V0[gbus] = Vg * abs(V0[gbus]) / V0[gbus]
        return V0

    def output_solution(self, fd, z, z_est, error_sqrsum):
        """ Prints comparison of measurements and their estimations.
        """
        col_width = 11
        sep = ('=' * col_width + ' ') * 4 + '\n'
        fd.write('State Estimation\n')
        fd.write('----------------\n')
        fd.write(sep)
        fd.write(('Type').center(col_width) + ' ')
        fd.write(('Name').center(col_width) + ' ')
        fd.write(('Measurement').center(col_width) + ' ')
        fd.write(('Estimation').center(col_width) + ' ')
        fd.write('\n')
        fd.write(sep)
        c = 0
        for t in [PF, PT, QF, QT, PG, QG, VM, VA]:
            for meas in self.measurements:
                if meas.type == t:
                    n = meas.b_or_l.name[:col_width].ljust(col_width)
                    fd.write(t.ljust(col_width) + ' ')
                    fd.write(n + ' ')
                    fd.write('%11.5f ' % z[c])
                    fd.write('%11.5f\n' % z_est[c])
                    c += 1

        fd.write('\nWeighted sum of error squares = %.4f\n' % error_sqrsum)


class Measurement(object):
    """ Defines a measurement at a bus or a branch.
    """

    def __init__(self, bus_or_line, type, value):
        """ Initialises a new Measurement instance.
        """
        self.b_or_l = bus_or_line
        self.type = type
        self.value = value