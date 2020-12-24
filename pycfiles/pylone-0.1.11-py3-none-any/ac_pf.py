# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pylon\ac_pf.py
# Compiled at: 2010-12-26 13:36:33
__doc__ = ' Defines solvers for AC power flow.\n\nBased on runpf.m from MATPOWER by Ray Zimmerman, developed at PSERC Cornell.\nSee U{http://www.pserc.cornell.edu/matpower/} for more information.\n'
import logging
from time import time
from numpy import array, angle, pi, exp, linalg, multiply, conj, r_, Inf
from scipy.sparse import hstack, vstack
from scipy.sparse.linalg import spsolve, splu
from pylon.case import PQ, PV, REFERENCE
logger = logging.getLogger(__name__)
BX = 'BX'
XB = 'XB'

class SlackBusError(Exception):
    """ No single slack bus error. """


class _ACPF(object):
    """ Defines a base class for AC power flow solvers.

    Based on runpf.m from MATPOWER by Ray Zimmerman, developed at PSERC
    Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more info.
    """

    def __init__(self, case, qlimit=False, tolerance=1e-08, iter_max=10, verbose=True):
        self.case = case
        self.qlimit = qlimit
        self.tolerance = tolerance
        self.iter_max = iter_max
        self.verbose = verbose

    def solve(self):
        """ Runs a power flow

        @rtype: dict
        @return: Solution dictionary with the following keys:
                   - C{V} - final complex voltages
                   - C{converged} - boolean value indicating if the solver
                     converged or not
                   - C{iterations} - the number of iterations performed
        """
        self.case.reset()
        (b, l, g, _, _, _, _) = self._unpack_case(self.case)
        self.case.index_buses(b)
        (refs, pq, pv, pvpq) = self._index_buses(b)
        if len(refs) != 1:
            logger.error('Swing bus required for DCPF.')
            return {'converged': False}
        t0 = time()
        V0 = self._initial_voltage(b, g)
        repeat = True
        while repeat:
            (Ybus, Yf, Yt) = self.case.getYbus(b, l)
            Sbus = self.case.getSbus(b)
            (V, converged, i) = self._run_power_flow(Ybus, Sbus, V0, pv, pq, pvpq)
            self.case.pf_solution(Ybus, Yf, Yt, V)
            if self.qlimit:
                raise NotImplementedError
            else:
                repeat = False

        elapsed = time() - t0
        if converged and self.verbose:
            logger.info('AC power flow converged in %.3fs' % elapsed)
        return {'converged': converged, 'elapsed': elapsed, 'iterations': i, 'V': V}

    def _unpack_case(self, case):
        """ Returns the contents of the case to be used in the OPF.
        """
        base_mva = case.base_mva
        b = case.connected_buses
        l = case.online_branches
        g = case.online_generators
        nb = len(b)
        nl = len(l)
        ng = len(g)
        return (
         b, l, g, nb, nl, ng, base_mva)

    def _index_buses(self, buses):
        """ Set up indexing for updating v.
        """
        refs = [ bus._i for bus in buses if bus.type == REFERENCE ]
        pv = [ bus._i for bus in buses if bus.type == PV ]
        pq = [ bus._i for bus in buses if bus.type == PQ ]
        pvpq = pv + pq
        return (
         refs, pq, pv, pvpq)

    def _initial_voltage(self, buses, generators):
        """ Returns the initial vector of complex bus voltages.

        The bus voltage vector contains the set point for generator
        (including ref bus) buses, and the reference angle of the swing
        bus, as well as an initial guess for remaining magnitudes and
        angles.
        """
        Vm = array([ bus.v_magnitude for bus in buses ])
        Va = array([ bus.v_angle * (pi / 180.0) for bus in buses ])
        V = Vm * exp(complex(0.0, 1.0) * Va)
        for g in generators:
            i = g.bus._i
            V[i] = g.v_magnitude / abs(V[i]) * V[i]

        return V

    def _run_power_flow(self, Ybus, Sbus, V0):
        """ Override this method in subclasses.
        """
        raise NotImplementedError


class NewtonPF(_ACPF):
    """ Solves the power flow using full Newton's method.

    Based on newtonpf.m from MATPOWER by Ray Zimmerman, developed at PSERC
    Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more info.
    """

    def _run_power_flow(self, Ybus, Sbus, V, pv, pq, pvpq, **kw_args):
        """ Solves the power flow using a full Newton's method.
        """
        Va = angle(V)
        Vm = abs(V)
        F = self._evaluate_function(Ybus, V, Sbus, pv, pq)
        converged = self._check_convergence(F)
        i = 0
        while not converged and i < self.iter_max:
            (V, Vm, Va) = self._one_iteration(F, Ybus, V, Vm, Va, pv, pq, pvpq)
            F = self._evaluate_function(Ybus, V, Sbus, pv, pq)
            converged = self._check_convergence(F)
            i += 1

        if converged:
            if self.verbose:
                logger.info("Newton's method power flow converged in %d iterations." % i)
        else:
            logger.error("Newton's method power flow did not converge in %d iterations." % i)
        return (
         V, converged, i)

    def _one_iteration(self, F, Ybus, V, Vm, Va, pv, pq, pvpq):
        """ Performs one Newton iteration.
        """
        J = self._build_jacobian(Ybus, V, pv, pq, pvpq)
        dx = -1 * spsolve(J, F)
        npv = len(pv)
        npq = len(pq)
        if npv > 0:
            Va[pv] = Va[pv] + dx[range(npv)]
        if npq > 0:
            Va[pq] = Va[pq] + dx[range(npv, npv + npq)]
            Vm[pq] = Vm[pq] + dx[range(npv + npq, npv + npq + npq)]
        V = Vm * exp(complex(0.0, 1.0) * Va)
        Vm = abs(V)
        Va = angle(V)
        return (
         V, Vm, Va)

    def _evaluate_function(self, Ybus, V, Sbus, pv, pq):
        """ Evaluates F(x).
        """
        mis = multiply(V, conj(Ybus * V)) - Sbus
        F = r_[(mis[pv].real, mis[pq].real, mis[pq].imag)]
        return F

    def _check_convergence(self, F):
        """ Checks if the solution has converged to within the specified
            tolerance.
        """
        normF = linalg.norm(F, Inf)
        if normF < self.tolerance:
            converged = True
        else:
            converged = False
            if self.verbose:
                logger.info('Difference: %.3f' % (normF - self.tolerance))
        return converged

    def _build_jacobian(self, Ybus, V, pv, pq, pvpq):
        """ Returns the Jacobian matrix.
        """
        pq_col = [ [i] for i in pq ]
        pvpq_col = [ [i] for i in pvpq ]
        (dS_dVm, dS_dVa) = self.case.dSbus_dV(Ybus, V)
        J11 = dS_dVa[(pvpq_col, pvpq)].real
        J12 = dS_dVm[(pvpq_col, pq)].real
        J21 = dS_dVa[(pq_col, pvpq)].imag
        J22 = dS_dVm[(pq_col, pq)].imag
        J = vstack([
         hstack([J11, J12]),
         hstack([J21, J22])], format='csr')
        return J


class FastDecoupledPF(_ACPF):
    """ Solves the power flow using fast decoupled method.

    Based on fdpf.m from MATPOWER by Ray Zimmerman, developed at PSERC
    Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more info.
    """

    def __init__(self, case, qlimit=False, tolerance=1e-08, iter_max=20, verbose=True, method=XB):
        """ Initialises a new ACPF instance.
        """
        super(FastDecoupledPF, self).__init__(case, qlimit, tolerance, iter_max, verbose)
        self.method = method

    def _run_power_flow(self, Ybus, Sbus, V, pv, pq, pvpq):
        """ Solves the power flow using a full Newton's method.
        """
        i = 0
        Va = angle(V)
        Vm = abs(V)
        (Bp, Bpp) = self.case.makeB(method=self.method)
        (P, Q) = self._evaluate_mismatch(Ybus, V, Sbus, pq, pvpq)
        if self.verbose:
            logger.info('iteration     max mismatch (p.u.)  \n')
            logger.info('type   #        P            Q     \n')
            logger.info('---- ----  -----------  -----------\n')
        converged = self._check_convergence(P, Q, i, 'P')
        if converged and self.verbose:
            logger.info('Converged!')
        pq_col = [ [k] for k in pq ]
        pvpq_col = [ [k] for k in pvpq ]
        Bp = Bp[(pvpq_col, pvpq)].tocsc()
        Bpp = Bpp[(pq_col, pq)].tocsc()
        Bp_solver = splu(Bp)
        Bpp_solver = splu(Bpp)
        while not converged and i < self.iter_max:
            i += 1
            (V, Vm, Va) = self._p_iteration(P, Bp_solver, Vm, Va, pvpq)
            (P, Q) = self._evaluate_mismatch(Ybus, V, Sbus, pq, pvpq)
            converged = self._check_convergence(P, Q, i, 'P')
            if self.verbose and converged:
                logger.info('Fast-decoupled power flow converged in %d P-iterations and %d Q-iterations.' % (
                 i, i - 1))
                break
            (V, Vm, Va) = self._q_iteration(Q, Bpp_solver, Vm, Va, pq)
            (P, Q) = self._evaluate_mismatch(Ybus, V, Sbus, pq, pvpq)
            converged = self._check_convergence(P, Q, i, 'Q')
            if self.verbose and converged:
                logger.info('Fast-decoupled power flow converged in %d P-iterations and %d Q-iterations.' % (
                 i, i))
                break

        if self.verbose and not converged:
            logger.error('FDPF did not converge in %d iterations.' % i)
        return (
         V, converged, i)

    def _evaluate_mismatch(self, Ybus, V, Sbus, pq, pvpq):
        """ Evaluates the mismatch.
        """
        mis = (multiply(V, conj(Ybus * V)) - Sbus) / abs(V)
        P = mis[pvpq].real
        Q = mis[pq].imag
        return (
         P, Q)

    def _check_convergence(self, P, Q, i, type):
        """ Checks if the solution has converged to within the specified
        tolerance.
        """
        normP = linalg.norm(P, Inf)
        normQ = linalg.norm(Q, Inf)
        if self.verbose:
            logger.info('  %s  %3d   %10.3e   %10.3e' % (type, i, normP, normQ))
        if normP < self.tolerance and normQ < self.tolerance:
            converged = True
        else:
            converged = False
        return converged

    def _p_iteration(self, P, Bp_solver, Vm, Va, pvpq):
        """ Performs a P iteration, updates Va.
        """
        dVa = -Bp_solver.solve(P)
        Va[pvpq] = Va[pvpq] + dVa
        V = Vm * exp(complex(0.0, 1.0) * Va)
        return (
         V, Vm, Va)

    def _q_iteration(self, Q, Bpp_solver, Vm, Va, pq):
        """ Performs a Q iteration, updates Vm.
        """
        dVm = -Bpp_solver.solve(Q)
        Vm[pq] = Vm[pq] + dVm
        V = Vm * exp(complex(0.0, 1.0) * Va)
        return (
         V, Vm, Va)