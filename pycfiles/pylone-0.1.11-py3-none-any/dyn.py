# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pylon\dyn.py
# Compiled at: 2010-12-26 13:36:33
__doc__ = ' Defines classes for dynamic simulation.\n\nBased on MatDyn by Stijn Cole, developed at Katholieke Universiteit Leuven.\nSee U{http://www.esat.kuleuven.be/electa/teaching/matdyn/} for more info.\n'
import math, logging
from time import time
from numpy import array, zeros, ones, exp, conj, pi, angle, abs, sin, cos, c_, r_, flatnonzero, finfo
from scipy.sparse.linalg import spsolve, splu
from pylon import NewtonPF
from util import _Named, _Serializable
logger = logging.getLogger(__name__)
EPS = finfo(float).eps
CLASSICAL = 'classical'
FOURTH_ORDER = 'fourth_order'
CONST_EXCITATION = 'constant excitation'
IEEE_DC1A = 'IEEE DC1A'
CONST_POWER = 'constant power'
GENERAL_IEEE = 'IEEE general speed-governing system'
BUS_CHANGE = 'bus change'
BRANCH_CHANGE = 'branch change'

class DynamicCase(_Named, _Serializable):
    """ Defines a dynamic simulation case.
    """

    def __init__(self, case, frequency=50.0, stepsize=0.01, stoptime=1):
        """ Constructs a new DynamicCase instance.
        """
        self.case = case
        self.dyn_generators = []
        self.exciters = []
        self.governors = []
        self.freq = frequency
        self.stepsize = stepsize
        self.stoptime = stoptime

    def getAugYbus(self, U0, gbus):
        """ Based on AugYbus.m from MatDyn by Stijn Cole, developed at
        Katholieke Universiteit Leuven. See U{http://www.esat.kuleuven.be/
        electa/teaching/matdyn/} for more information.

        @rtype: csr_matrix
        @return: The augmented bus admittance matrix.
        """
        j = complex(0.0, 1.0)
        buses = self.case.connected_buses
        nb = len(buses)
        (Ybus, _, _) = self.case.getYbus()
        Sd = array([ self.case.s_demand(bus) for bus in buses ])
        Yd = conj(Sd) / abs(U0) ** 2
        xd_tr = array([ g.xd_tr for g in self.dyn_generators ])
        Yg = zeros(nb)
        Yg[gbus] = 1 / (j * xd_tr)
        for i in range(nb):
            Ybus[(i, i)] = Ybus[(i, i)] + Yg[i] + Yd[i]

        return Ybus

    def generatorInit(self, U0):
        """ Based on GeneratorInit.m from MatDyn by Stijn Cole, developed at
        Katholieke Universiteit Leuven. See U{http://www.esat.kuleuven.be/
        electa/teaching/matdyn/} for more information.

        @rtype: tuple
        @return: Initial generator conditions.
        """
        j = complex(0.0, 1.0)
        generators = self.dyn_generators
        Efd0 = zeros(len(generators))
        Xgen0 = zeros((len(generators), 4))
        typ1 = [ g._i for g in generators if g.model == CLASSICAL ]
        typ2 = [ g._i for g in generators if g.model == FOURTH_ORDER ]
        x_tr = array([ g.x_tr for g in generators ])
        omega0 = ones(len(typ1)) * 2 * pi * self.freq
        Sg = array([ g.p + j * g.q for g in generators ])
        Ia0 = conj(Sg[typ1]) / conj(U0) / self.base_mva
        Eq_tr0 = U0[typ1] + j * x_tr * Ia0
        delta0 = angle(Eq_tr0)
        Eq_tr0 = abs(Eq_tr0)
        Xgen0[typ1, :] = c_[(delta0, omega0, Eq_tr0)]
        xd = array([ g.xd for g in generators ])
        xq = array([ g.xq for g in generators ])
        xd_tr = array([ g.xd_tr for g in generators ])
        xq_tr = array([ g.xq_tr for g in generators ])
        omega0 = ones(len(typ2)) * 2 * pi * self.freq
        Ia0 = conj(Sg[typ2]) / conj(U0[typ2]) / self.base_mva
        phi0 = angle(Ia0)
        Eq0 = U0[typ2] + j * xq * Ia0
        delta0 = angle(Eq0)
        Id0 = -abs(Ia0) * sin(delta0 - phi0)
        Iq0 = abs(Ia0) * cos(delta0 - phi0)
        Efd0[typ2] = abs(Eq0) - (xd - xq) * Id0
        Eq_tr0 = Efd0[typ2] + (xd - xd_tr) * Id0
        Ed_tr0 = -(xq - xq_tr) * Iq0
        Xgen0[typ2, :] = c_[(delta0, omega0, Eq_tr0, Ed_tr0)]
        return (
         Efd0, Xgen0)

    def exciterInit(self, Xexc, Vexc):
        """ Based on ExciterInit.m from MatDyn by Stijn Cole, developed at
        Katholieke Universiteit Leuven. See U{http://www.esat.kuleuven.be/
        electa/teaching/matdyn/} for more information.

        @rtype: tuple
        @return: Exciter initial conditions.
        """
        exciters = self.exciters
        Xexc0 = zeros(Xexc.shape)
        Pexc0 = zeros(len(exciters))
        typ1 = [ e.generator._i for e in exciters if e.model == CONST_EXCITATION ]
        typ2 = [ e.generator._i for e in exciters if e.model == IEEE_DC1A ]
        Efd0 = Xexc[(typ1, 0)]
        Xexc0[(typ1, 0)] = Efd0
        Efd0 = Xexc[(typ2, 0)]
        Ka = array([ e.ka for e in exciters ])
        Ta = array([ e.ta for e in exciters ])
        Ke = array([ e.ke for e in exciters ])
        Te = array([ e.te for e in exciters ])
        Kf = array([ e.kf for e in exciters ])
        Tf = array([ e.tf for e in exciters ])
        Aex = array([ e.aex for e in exciters ])
        Bex = array([ e.bex for e in exciters ])
        Ur_min = array([ e.ur_min for e in exciters ])
        Ur_max = array([ e.ur_max for e in exciters ])
        U = Vexc[(typ2, 0)]
        Uf = zeros(len(typ2))
        Ux = Aex * exp(Bex * Efd0)
        Ur = Ux + Ke * Efd0
        Uref2 = U + (Ux + Ke * Efd0) / Ka - U
        Uref = U
        Xexc0[typ2, :] = c_[(Efd0, Uf, Ur)]
        Pexc0[typ2, :] = c_[(Ka, Ta, Ke, Te, Kf, Tf, Aex, Bex,
         Ur_min, Ur_max, Uref, Uref2)]
        return (
         Xexc0, Pexc0)

    def governorInit(self, Xgov, Vgov):
        """ Based on GovernorInit.m from MatDyn by Stijn Cole, developed at
        Katholieke Universiteit Leuven. See U{http://www.esat.kuleuven.be/
        electa/teaching/matdyn/} for more information.

        @rtype: tuple
        @return: Initial governor conditions.
        """
        governors = self.governors
        Xgov0 = zeros(Xgov.shape)
        Pgov0 = zeros(len(governors))
        typ1 = [ g.generator._i for g in governors if g.model == CONST_POWER ]
        typ2 = [ g.generator._i for g in governors if g.model == GENERAL_IEEE ]
        Pm0 = Xgov[(typ1, 0)]
        Xgov0[(typ1, 0)] = Pm0
        Pm0 = Xgov[(typ2, 0)]
        K = array([ g.k for g in governors ])
        T1 = array([ g.t1 for g in governors ])
        T2 = array([ g.t2 for g in governors ])
        T3 = array([ g.t3 for g in governors ])
        Pup = array([ g.p_up for g in governors ])
        Pdown = array([ g.p_down for g in governors ])
        Pmax = array([ g.p_max for g in governors ])
        Pmin = array([ g.p_min for g in governors ])
        omega0 = Vgov[(typ2, 0)]
        zz0 = Pm0
        PP0 = Pm0
        P0 = K * (2 * pi * self.freq - omega0)
        xx0 = T1 * (1 - T2 / T1) * (2 * pi * self.freq - omega0)
        Xgov0[typ2, :] = c_[(Pm0, P0, xx0, zz0)]
        Pgov0[typ2, :] = c_[(K, T1, T2, T3, Pup, Pdown, Pmax, Pmin, PP0)]
        return (
         Xgov0, Pgov0)

    def machineCurrents(self, Xg, U):
        """ Based on MachineCurrents.m from MatDyn by Stijn Cole, developed at
        Katholieke Universiteit Leuven. See U{http://www.esat.kuleuven.be/
        electa/teaching/matdyn/} for more information.

        @param Xg: Generator state variables.
        @param U: Generator voltages.

        @rtype: tuple
        @return: Currents and electric power of generators.
        """
        generators = self.dyn_generators
        ng = len(generators)
        Id = zeros(ng)
        Iq = zeros(ng)
        Pe = zeros(ng)
        typ1 = [ g._i for g in generators if g.model == CLASSICAL ]
        typ2 = [ g._i for g in generators if g.model == FOURTH_ORDER ]
        delta = Xg[(typ1, 0)]
        Eq_tr = Xg[(typ1, 2)]
        xd = array([ g.xd for g in generators ])
        Pe[typ1] = 1 / xd * abs(U[typ1]) * abs(Eq_tr) * sin(delta - angle(U[typ1]))
        delta = Xg[(typ1, 0)]
        Eq_tr = Xg[(typ1, 2)]
        Ed_tr = Xg[(typ1, 3)]
        xd_tr = array([ g.xd_tr for g in generators ])
        xq_tr = array([ g.xq_tr for g in generators ])
        theta = angle(U)
        vd = -abs(U[typ2]) * sin(delta - theta[typ2])
        vq = abs(U[typ2]) * cos(delta - theta[typ2])
        Id[typ2] = (vq - Eq_tr) / xd_tr
        Iq[typ2] = -(vd - Ed_tr) / xq_tr
        Pe[typ2] = Eq_tr * Iq[typ2] + Ed_tr * Id[typ2] + (xd_tr - xq_tr) * Id[typ2] * Iq[typ2]
        return (
         Id, Iq, Pe)

    def solveNetwork(self, Xgen, augYbus_solver, gbus):
        """ Based on SolveNetwork.m from MatDyn by Stijn Cole, developed at
        Katholieke Universiteit Leuven. See U{http://www.esat.kuleuven.be/
        electa/teaching/matdyn/} for more information.

        @rtype: array
        @return: Bus voltages.
        """
        generators = self.dyn_generators
        j = complex(0.0, 1.0)
        ng = len(gbus)
        Igen = zeros(ng)
        s = len(augYbus_solver)
        Ig = zeros(s)
        typ1 = [ g._i for g in generators if g.model == CLASSICAL ]
        typ2 = [ g._i for g in generators if g.model == FOURTH_ORDER ]
        delta = Xgen[(typ1, 0)]
        Eq_tr = Xgen[(typ1, 2)]
        xd_tr = array([ g.xd_tr for g in generators ])[typ1]
        Igen[typ1] = Eq_tr * exp(j * delta) / (j * xd_tr)
        delta = Xgen[(typ2, 0)]
        Eq_tr = Xgen[(typ2, 2)]
        Ed_tr = Xgen[(typ2, 3)]
        xd_tr = array([ g.xd_tr for g in generators ])[typ2]
        Igen[typ2] = (Eq_tr + j * Ed_tr) * exp(j * delta) / (j * xd_tr)
        Ig[gbus] = Igen
        U = augYbus_solver.solve(Ig)
        return U

    def exciter(self, Xexc, Pexc, Vexc):
        """ Exciter model.

        Based on Exciter.m from MatDyn by Stijn Cole, developed at Katholieke
        Universiteit Leuven. See U{http://www.esat.kuleuven.be/electa/teaching/
        matdyn/} for more information.
        """
        exciters = self.exciters
        F = zeros(Xexc.shape)
        typ1 = [ e.generator._i for e in exciters if e.model == CONST_EXCITATION ]
        typ2 = [ e.generator._i for e in exciters if e.model == IEEE_DC1A ]
        F[typ1, :] = 0.0
        Efd = Xexc[(typ2, 0)]
        Uf = Xexc[(typ2, 1)]
        Ur = Xexc[(typ2, 2)]
        Ka = Pexc[(typ2, 0)]
        Ta = Pexc[(typ2, 1)]
        Ke = Pexc[(typ2, 2)]
        Te = Pexc[(typ2, 3)]
        Kf = Pexc[(typ2, 4)]
        Tf = Pexc[(typ2, 5)]
        Aex = Pexc[(typ2, 6)]
        Bex = Pexc[(typ2, 7)]
        Ur_min = Pexc[(typ2, 8)]
        Ur_max = Pexc[(typ2, 9)]
        Uref = Pexc[(typ2, 10)]
        Uref2 = Pexc[(typ2, 11)]
        U = Vexc[(typ2, 1)]
        Ux = Aex * exp(Bex * Efd)
        dUr = 1 / Ta * (Ka * (Uref - U + Uref2 - Uf) - Ur)
        dUf = 1 / Tf * (Kf / Te * (Ur - Ux - Ke * Efd) - Uf)
        if sum(flatnonzero(Ur > Ur_max)) >= 1:
            Ur2 = Ur_max
        elif sum(flatnonzero(Ur < Ur_max)) >= 1:
            Ur2 = Ur_min
        else:
            Ur2 = Ur
        dEfd = 1 / Te * (Ur2 - Ux - Ke * Efd)
        F[typ2, :] = c_[(dEfd, dUf, dUr)]
        return F

    def governor(self, Xgov, Pgov, Vgov):
        """ Governor model.

        Based on Governor.m from MatDyn by Stijn Cole, developed at Katholieke
        Universiteit Leuven. See U{http://www.esat.kuleuven.be/electa/teaching/
        matdyn/} for more information.
        """
        governors = self.governors
        omegas = 2 * pi * self.freq
        F = zeros(Xgov.shape)
        typ1 = [ g.generator._i for g in governors if g.model == CONST_POWER ]
        typ2 = [ g.generator._i for g in governors if g.model == GENERAL_IEEE ]
        F[(typ1, 0)] = 0
        Pm = Xgov[(typ2, 0)]
        P = Xgov[(typ2, 1)]
        x = Xgov[(typ2, 2)]
        z = Xgov[(typ2, 3)]
        K = Pgov[(typ2, 0)]
        T1 = Pgov[(typ2, 1)]
        T2 = Pgov[(typ2, 2)]
        T3 = Pgov[(typ2, 3)]
        Pup = Pgov[(typ2, 4)]
        Pdown = Pgov[(typ2, 5)]
        Pmax = Pgov[(typ2, 6)]
        Pmin = Pgov[(typ2, 7)]
        P0 = Pgov[(typ2, 8)]
        omega = Vgov[(typ2, 0)]
        dx = K * (-1 / T1 * x + (1 - T2 / T1) * (omega - omegas))
        dP = 1 / T1 * x + T2 / T1 * (omega - omegas)
        y = 1 / T3 * (P0 - P - Pm)
        y2 = y
        if sum(flatnonzero(y > Pup)) >= 1:
            y2 = (1 - flatnonzero(y > Pup)) * y2 + flatnonzero(y > Pup) * Pup
        if sum(flatnonzero(y < Pdown)) >= 1:
            y2 = (1 - flatnonzero(y < Pdown)) * y2 + flatnonzero(y < Pdown) * Pdown
        dz = y2
        dPm = y2
        if sum(flatnonzero(z > Pmax)) >= 1:
            dPm = (1 - flatnonzero(z > Pmax)) * dPm + flatnonzero(z > Pmax) * 0
        if sum(flatnonzero(z < Pmin)) >= 1:
            dPm = (1 - flatnonzero(z < Pmin)) * dPm + flatnonzero(z < Pmin) * 0
        F[typ2, :] = c_[(dPm, dP, dx, dz)]
        return F

    def generator(self, Xgen, Xexc, Xgov, Vgen):
        """ Generator model.

        Based on Generator.m from MatDyn by Stijn Cole, developed at Katholieke
        Universiteit Leuven. See U{http://www.esat.kuleuven.be/electa/teaching/
        matdyn/} for more information.
        """
        generators = self.dyn_generators
        omegas = 2 * pi * self.freq
        F = zeros(Xgen.shape)
        typ1 = [ g._i for g in generators if g.model == CLASSICAL ]
        typ2 = [ g._i for g in generators if g.model == FOURTH_ORDER ]
        omega = Xgen[(typ1, 1)]
        Pm0 = Xgov[(typ1, 0)]
        H = array([ g.h for g in generators ])[typ1]
        D = array([ g.d for g in generators ])[typ1]
        Pe = Vgen[(typ1, 2)]
        ddelta = omega = omegas
        domega = pi * self.freq / H * (-D * (omega - omegas) + Pm0 - Pe)
        dEq = zeros(len(typ1))
        F[typ1, :] = c_[(ddelta, domega, dEq)]
        omega = Xgen[(typ2, 1)]
        Eq_tr = Xgen[(typ2, 2)]
        Ed_tr = Xgen[(typ2, 3)]
        H = array([ g.h for g in generators ])
        D = array([ g.d for g in generators ])
        xd = array([ g.xd for g in generators ])
        xq = array([ g.xq for g in generators ])
        xd_tr = array([ g.xd_tr for g in generators ])
        xq_tr = array([ g.xq_tr for g in generators ])
        Td0_tr = array([ g.td for g in generators ])
        Tq0_tr = array([ g.tq for g in generators ])
        Id = Vgen[(typ2, 0)]
        Iq = Vgen[(typ2, 1)]
        Pe = Vgen[(typ2, 2)]
        Efd = Xexc[(typ2, 0)]
        Pm = Xgov[(typ2, 0)]
        ddelta = omega - omegas
        domega = pi * self.freq / H * (-D * (omega - omegas) + Pm - Pe)
        dEq = 1 / Td0_tr * (Efd - Eq_tr + (xd - xd_tr) * Id)
        dEd = 1 / Tq0_tr * (-Ed_tr - (xq - xq_tr) * Iq)
        F[typ2, :] = c_[(ddelta, domega, dEq, dEd)]
        return F


class DynamicSolver(object):
    """ Defines a solver for dynamic simulation.

    The adaptive step size methods start with minimal step size. It is of
    interest to increase minimum step size as it speeds up the calculations.
    Generally, tolerance must be increased as well, or the integration will
    fail.

    Based on rundyn.m from MatDyn by Stijn Cole, developed at Katholieke
    Universiteit Leuven. See U{http://www.esat.kuleuven.be/electa/teaching/
    matdyn/} for more information.
    """

    def __init__(self, dyn_case, method=None, tol=0.0001, minstep=0.001, maxstep=100.0, verbose=True, plot=True):
        self.dyn_case = dyn_case
        self.method = ModifiedEuler() if method is None else method
        self.tol = tol
        self.minstep = minstep
        self.maxstep = maxstep
        self.verbose = verbose
        self.plot = plot
        return

    def solve(self):
        """ Runs dynamic simulation.

        @rtype: dict
        @return: Solution dictionary with the following keys:
                   - C{angles} - generator angles
                   - C{speeds} - generator speeds
                   - C{eq_tr} - q component of transient voltage behind
                     reactance
                   - C{ed_tr} - d component of transient voltage behind
                     reactance
                   - C{efd} - Excitation voltage
                   - C{pm} - mechanical power
                   - C{voltages} - bus voltages
                   - C{stepsize} - step size integration method
                   - C{errest} - estimation of integration error
                   - C{failed} - failed steps
                   - C{time} - time points
        """
        t0 = time()
        buses = self.dyn_case.buses
        solution = NewtonPF(self.case).solve()
        if not solution['converged']:
            logger.error('Power flow did not converge. Exiting...')
            return {}
        if self.verbose:
            logger.info('Power flow converged.')
        if self.verbose:
            logger.info('Constructing augmented admittance matrix...')
        gbus = [ g.bus._i for g in self.dyn_generators ]
        ng = len(gbus)
        Um = array([ bus.v_magnitude for bus in buses ])
        Ua = array([ bus.v_angle * (pi / 180.0) for bus in buses ])
        U0 = Um * exp(complex(0.0, 1.0) * Ua)
        U00 = U0
        augYbus = self.dyn_case.getAugYbus(U0, gbus)
        augYbus_solver = splu(augYbus)
        if self.verbose:
            logger.info('Calculating initial state...')
        (Efd0, Xgen0) = self.dyn_case.generatorInit(U0)
        omega0 = Xgen0[:, 1]
        (Id0, Iq0, Pe0) = self.dyn_case.machineCurrents(Xgen0, U0)
        Vgen0 = r_[(Id0, Iq0, Pe0)]
        Vexc0 = abs(U0[gbus])
        (Xexc0, Pexc0) = self.dyn_case.exciterInit(Efd0, Vexc0)
        Pm0 = Pe0
        (Xgov0, Pgov0) = self.dyn_case.governorInit(Pm0, omega0)
        Vgov0 = omega0
        Fexc0 = self.dyn_case.exciter(Xexc0, Pexc0, Vexc0)
        Fgov0 = self.dyn_case.governor(Xgov0, Pgov0, Vgov0)
        Fgen0 = self.dyn_case.generator(Xgen0, Xexc0, Xgov0, Vgen0)
        if sum(abs(Fgen0)) > 1e-06:
            logger.error('Generator not in steady-state. Exiting...')
            return {}
        if sum(abs(Fexc0)) > 1e-06:
            logger.error('Exciter not in steady-state. Exiting...')
            return {}
        if sum(abs(Fgov0)) > 1e-06:
            logger.error('Governor not in steady-state. Exiting...')
            return {}
        if self.verbose:
            logger.info('System in steady-state.')
        t = -0.02
        erst = False
        failed = False
        eulerfailed = False
        stoptime = self.dyn_case.stoptime
        if isinstance(self.method, RungeKuttaFehlberg) or isinstance(self.method, RungeKuttaHighamHall):
            stepsize = self.minstep
        else:
            stepsize = self.dyn_case.stepsize
        ev = 0
        eventhappened = False
        i = 0
        if self.verbose:
            logger.info('Allocating memory...')
        chunk = 5000
        time = zeros(chunk)
        time[0, :] = t
        errest = zeros(chunk)
        errest[0, :] = erst
        stepsizes = zeros(chunk)
        stepsizes[0, :] = stepsize
        voltages = zeros(chunk)
        voltages[0, :] = U0.H
        angles = zeros((chunk, ng))
        angles[0, :] = Xgen0[:, 0] * 180.0 / pi
        speeds = zeros((chunk, ng))
        speeds[0, :] = Xgen0[:, 0] / 2 * pi * self.dyn_case.freq
        Eq_tr = zeros((chunk, ng))
        Eq_tr[0, :] = Xgen0[:, 2]
        Ed_tr = zeros((chunk, ng))
        Ed_tr[0, :] = Xgen0[:, 3]
        Efd = zeros((chunk, ng))
        Efd[0, :] = Efd0[:, 0]
        PM = zeros((chunk, ng))
        PM[0, :] = Pm0[:, 0]
        while t < stoptime + stepsize:
            i += 1
            if i % 45 == 0 and self.verbose:
                logger.info('%6.2f%% completed.' % t / stoptime * 100)
            (Xgen0, self.Pgen0, Vgen0, Xexc0, Pexc0, Vexc0, Xgov0, Pgov0, Vgov0, U0, t, newstepsize) = self.method.solve(t, Xgen0, self.Pgen0, Vgen0, Xexc0, Pexc0, Vexc0, Xgov0, Pgov0, Vgov0, augYbus_solver, gbus, stepsize)
            if eulerfailed:
                logger.info('No solution found. Exiting... ')
                return {}
            if failed:
                t = t - stepsize
            if t + newstepsize > stoptime:
                newstepsize = stoptime - t
            elif stepsize < self.minstep:
                logger.info('No solution found with minimum step size. Exiting... ')
                return {}
            if i > time.shape[0]:
                time = zeros(chunk)
                errest = zeros(chunk)
                stepsize = zeros(chunk)
                voltages = zeros(chunk)
                angles = zeros((chunk, ng))
                speeds = zeros((chunk, ng))
                Eq_tr = zeros((chunk, ng))
                Ed_tr = zeros((chunk, ng))
                Efd = zeros((chunk, ng))
                PM = zeros((chunk, ng))
            stepsizes[i, :] = stepsize
            errest[i, :] = erst
            time[i, :] = t
            voltages[i, :] = U0
            Efd[i, :] = Xexc0[:, 0]
            PM[i, :] = Xgov0[:, 0]
            angles[i, :] = Xgen0[:, 0] * 180.0 / pi
            speeds[i, :] = Xgen0[:, 1] * (2 * pi * self.dyn_case.freq)
            Eq_tr[i, :] = Xgen0[:, 2]
            Ed_tr[i, :] = Xgen0[:, 3]
            if len(self.events) > 0 and ev <= len(self.events) and isinstance(self.method, RungeKuttaFehlberg) and isinstance(self.method, RungeKutta):
                if t + newstepsize >= self.events[ev].t:
                    if self.events[ev] - t < newstepsize:
                        newstepsize = self.events[ev].t - t
            if len(self.events) > 0 and ev <= len(self.events):
                for event in self.events:
                    if abs(t - self.events[ev].t) > 10 * EPS or ev > len(self.events):
                        break
                    else:
                        eventhappened = True
                    event.obj.set_attr(event.param, event.newval)
                    ev += 1

                if eventhappened:
                    self.dyn_case.getAugYbus(U00, gbus)
                    U0 = self.dyn_case.solveNetwork(Xgen0, self.Pgen0, augYbus_solver, gbus)
                    (Id0, Iq0, Pe0) = self.dyn_case.machineCurrents(Xgen0, self.Pgen0, U0[gbus])
                    Vgen0 = r_[(Id0, Iq0, Pe0)]
                    Vexc0 = abs(U0[gbus])
                    if isinstance(self.method, RungeKuttaFehlberg) or isinstance(self.method, RungeKuttaHighamHall):
                        newstepsize = self.minstepsize
                    i += 1
                    stepsize[i, :] = stepsize.T
                    errest[i, :] = erst.T
                    time[i, :] = t
                    voltages[i, :] = U0.T
                    PM[i, :] = Xgov0[:, 1]
                    angles[i, :] = Xgen0[:, 0] * 180.0 / pi
                    speeds[i, :] = Xgen0[:, 1] / (2.0 * pi * self.freq)
                    Eq_tr[i, :] = Xgen0[:, 2]
                    Ed_tr[i, :] = Xgen0[:, 3]
                    eventhappened = False
            stepsize = newstepsize
            t += stepsize

        if self.verbose:
            logger.info('100%% completed')
            elapsed = time() - t0
            logger.info('Simulation completed in %5.2f seconds.' % elapsed)
        angles = angles[0:i, :]
        speeds = speeds[0:i, :]
        Eq_tr = Eq_tr[0:i, :]
        Ed_tr = Ed_tr[0:i, :]
        Efd = Efd[0:i, :]
        PM = PM[0:i, :]
        voltages = voltages[0:i, :]
        stepsize = stepsize[0:i, :]
        errest = errest[0:i, :]
        time = time[0:i, :]
        if self.plot:
            raise NotImplementedError
        return {}


class ModifiedEuler(object):
    """ Modified Euler ODE solver.

    Based on ModifiedEuler.m from MatDyn by Stijn Cole, developed at Katholieke
    Universiteit Leuven. See U{http://www.esat.kuleuven.be/electa/teaching/
    matdyn/} for more information.
    """

    def solve(self, t, Xgen0, Pgen, Vgen0, Xexc0, Pexc, Vexc0, Xgov0, Pgov, Vgov0, augYbus_solver, gbus, stepsize):
        case = self.dyn_case
        dFexc0 = case.exciter(Xexc0, Pexc, Vexc0)
        Xexc1 = Xexc0 + case.stepsize * dFexc0
        dFgov0 = case.governor(Xgov0, Pgov, Vgov0)
        Xgov1 = Xgov0 + case.stepsize * dFgov0
        dFgen0 = case.generator(Xgen0, Xexc1, Xgov1, Pgen, Vgen0)
        Xgen1 = Xgen0 + case.stepsize * dFgen0
        U1 = case.solveNetwork(Xgen1, Pgen, augYbus_solver, gbus)
        (Id1, Iq1, Pe1) = case.machineCurrents(Xgen1, Pgen, U1[gbus])
        Vexc1 = abs(U1[gbus])
        Vgen1 = r_[(Id1, Iq1, Pe1)]
        Vgov1 = Xgen1[:, 2]
        dFexc1 = case.exciter(Xexc1, Pexc, Vexc1)
        Xexc2 = Xexc0 + case.stepsize / 2 * (dFexc0 + dFexc1)
        dFgov1 = case.governor(Xgov1, Pgov, Vgov1)
        Xgov2 = Xgov0 + case.stepsize / 2 * (dFgov0 + dFgov1)
        dFgen1 = case.generator(Xgen1, Xexc2, Xgov2, Pgen, Vgen1)
        Xgen2 = Xgen0 + case.stepsize / 2 * (dFgen0 + dFgen1)
        U2 = case.solveNetwork(Xgen2, Pgen, augYbus_solver, gbus)
        (Id2, Iq2, Pe2) = case.machineCurrents(Xgen2, Pgen, U2[gbus])
        Vgen2 = r_[(Id2, Iq2, Pe2)]
        Vexc2 = abs(U2[gbus])
        Vgov2 = Xgen2[:, 2]
        return (
         Xgen2, Pgen, Vgen2, Xexc2, Pexc, Vexc2,
         Xgov2, Pgov, Vgov2, U2, t, stepsize)


class RungeKutta(object):
    """ Standard 4th order Runge-Kutta ODE solver.

    Based on RundeKutta.m from MatDyn by Stijn Cole, developed at Katholieke
    Universiteit Leuven. See U{http://www.esat.kuleuven.be/electa/teaching/
    matdyn/} for more information.
    """

    def __init__(self):
        self._a = array([0.0, 0.0, 0.0, 0.0, 1.0 / 2.0, 0.0, 0.0, 0.0, 0.0,
         1.0 / 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0])
        self._b = array([1.0 / 6.0, 2.0 / 6.0, 2.0 / 6.0, 1.0 / 6.0])

    def solve(self, t, Xgen0, Pgen, Vgen0, Xexc0, Pexc, Vexc0, Xgov0, Pgov, Vgov0, augYbus_solver, gbus, stepsize):
        (Xexc1, Vexc1, Kexc1, Xgov1, Vgov1, Kgov1, Xgen1, Vgen1, Kgen1, _) = self._k1()
        (Xexc2, Vexc2, Kexc2, Xgov2, Vgov2, Kgov2, Xgen2, Vgen2, Kgen2, _) = self._k2(Xexc1, Vexc1, Kexc1, Xgov1, Vgov1, Kgov1, Xgen1, Vgen1, Kgen1)
        (Xexc3, Vexc3, Kexc3, Xgov3, Vgov3, Kgov3, Xgen3, Vgen3, Kgen3, _) = self._k3(Xexc2, Vexc2, Kexc2, Kexc1, Xgov2, Vgov2, Kgov2, Kgov1, Xgen2, Vgen2, Kgen2, Kgen1)
        (Xexc4, Vexc4, _, Xgov4, Vgov4, _, Xgen4, Vgen4, _, U4) = self._k4(Xexc3, Vexc3, Kexc3, Kexc2, Kexc1, Xgov3, Vgov3, Kgov3, Kgov2, Kgov1, Xgen3, Vgen3, Kgen3, Kgen2, Kgen1)
        return (
         Xgen4, Vgen4, Xexc4, Vexc4, Xgov4, Vgov4, U4)

    def _k1(self, Xexc0, Pexc, Vexc0, Xgov0, Pgov, Vgov0, Xgen0, Pgen, Vgen0, augYbus_solver, gbus):
        case = self.dyn_case
        a = self._a
        Kexc1 = case.exciter(Xexc0, Pexc, Vexc0)
        Xexc1 = Xexc0 + case.stepsize * a[(1, 0)] * Kexc1
        Kgov1 = case.governor(Xgov0, Pgov, Vgov0)
        Xgov1 = Xgov0 + case.stepsize * a[(1, 0)] * Kgov1
        Kgen1 = case.generator(Xgen0, Xexc1, Xgov1, Pgen, Vgen0)
        Xgen1 = Xgen0 + case.stepsize * a[(1, 0)] * Kgen1
        U1 = case.solveNetwork(Xgen1, Pgen, augYbus_solver, gbus)
        (Id1, Iq1, Pe1) = case.machineCurrents(Xgen1, Pgen, U1[gbus])
        Vexc1 = abs(U1[gbus])
        Vgen1 = r_[(Id1, Iq1, Pe1)]
        Vgov1 = Xgen1[:, 1]
        return (
         Xexc1, Vexc1, Kexc1, Xgov1, Vgov1, Kgov1, Xgen1, Vgen1, Kgen1, U1)

    def _k2(self, Xexc1, Xexc0, Pexc, Vexc1, Kexc1, Xgov1, Xgov0, Pgov, Vgov1, Kgov1, Xgen1, Xgen0, Pgen, Vgen1, Kgen1, augYbus_solver, gbus):
        case = self.dyn_case
        a = self._a
        Kexc2 = case.exciter(Xexc1, Pexc, Vexc1)
        Xexc2 = Xexc0 + case.stepsize * (a[(2, 0)] * Kexc1 + a[(2, 1)] * Kexc2)
        Kgov2 = case.governor(Xgov1, Pgov, Vgov1)
        Xgov2 = Xgov0 + case.stepsize * (a[(2, 0)] * Kgov1 + a[(2, 1)] * Kgov2)
        Kgen2 = case.generator(Xgen1, Xexc2, Xgov2, Pgen, Vgen1)
        Xgen2 = Xgen0 + case.stepsize * (a[(2, 0)] * Kgen1 + a[(2, 1)] * Kgen2)
        U2 = case.solveNetwork(Xgen2, Pgen, augYbus_solver, gbus)
        (Id2, Iq2, Pe2) = case.machineCurrents(Xgen2, Pgen, U2[gbus])
        Vexc2 = abs(U2[gbus])
        Vgen2 = r_[(Id2, Iq2, Pe2)]
        Vgov2 = Xgen2[:, 1]
        return (
         Xexc2, Vexc2, Kexc2, Xgov2, Vgov2, Kgov2, Xgen2, Vgen2, Kgen2, U2)

    def _k3(self, Xexc2, Xexc0, Pexc, Vexc2, Kexc2, Kexc1, Xgov2, Xgov0, Pgov, Vgov2, Kgov2, Kgov1, Xgen2, Xgen0, Pgen, Vgen2, Kgen2, Kgen1, augYbus_solver, gbus):
        case = self.dyn_case
        a = self._a
        Kexc3 = case.exciter(Xexc2, Pexc, Vexc2)
        Xexc3 = Xexc0 + case.stepsize * (a[(3, 0)] * Kexc1 + a[(3, 1)] * Kexc2 + a[(3,
                                                                                    2)] * Kexc3)
        Kgov3 = case.governor(Xgov2, Pgov, Vgov2)
        Xgov3 = Xgov0 + case.stepsize * (a[(3, 0)] * Kgov1 + a[(3, 1)] * Kgov2 + a[(3,
                                                                                    2)] * Kgov3)
        Kgen3 = case.generator(Xgen2, Xexc3, Xgov3, Pgen, Vgen2)
        Xgen3 = Xgen0 + case.stepsize * (a[(3, 0)] * Kgen1 + a[(3, 1)] * Kgen2 + a[(3,
                                                                                    2)] * Kgen3)
        U3 = case.solveNetwork(Xgen3, Pgen, augYbus_solver, gbus)
        (Id3, Iq3, Pe3) = case.machineCurrents(Xgen3, Pgen, U3[gbus])
        Vexc3 = abs(U3[gbus])
        Vgen3 = r_[(Id3, Iq3, Pe3)]
        Vgov3 = Xgen3[:, 1]
        return (
         Xexc3, Vexc3, Kexc3, Xgov3, Vgov3, Kgov3, Xgen3, Vgen3, Kgen3, U3)

    def _k4(self, Xexc3, Xexc0, Pexc, Vexc3, Kexc3, Kexc2, Kexc1, Xgov3, Xgov0, Pgov, Vgov3, Kgov3, Kgov2, Kgov1, Xgen3, Xgen0, Pgen, Vgen3, Kgen3, Kgen2, Kgen1, augYbus_solver, gbus):
        case = self.dyn_case
        b = self._b
        Kexc4 = case.exciter(Xexc3, Pexc, Vexc3)
        Xexc4 = Xexc0 + case.stepsize * (b[0] * Kexc1 + b[1] * Kexc2 + b[2] * Kexc3 + b[3] * Kexc4)
        Kgov4 = case.governor(Xgov3, Pgov, Vgov3)
        Xgov4 = Xgov0 + case.stepsize * (b[0] * Kgov1 + b[1] * Kgov2 + b[2] * Kgov3 + b[3] * Kgov4)
        Kgen4 = case.generator(Xgen3, Xexc4, Xgov4, Pgen, Vgen3)
        Xgen4 = Xgen0 + case.stepsize * (b[0] * Kgen1 + b[1] * Kgen2 + b[2] * Kgen3 + b[3] * Kgen4)
        U4 = case.solveNetwork(Xgen4, Pgen, augYbus_solver, gbus)
        (Id4, Iq4, Pe4) = case.machineCurrents(Xgen4, Pgen, U4[gbus])
        Vexc4 = abs(U4[gbus])
        Vgen4 = r_[(Id4, Iq4, Pe4)]
        Vgov4 = Xgen4[:, 1]
        return (
         Xexc4, Vexc4, Kexc4, Xgov4, Vgov4, Kgov4, Xgen4, Vgen4, Kgen4, U4)


class RungeKuttaFehlberg(RungeKutta):
    """ Runge-Kutta Fehlberg ODE solver.

    Based on RungeKuttaFehlberg.m from MatDyn by Stijn Cole, developed at
    Katholieke Universiteit Leuven. See U{http://www.esat.kuleuven.be/electa/
    teaching/matdyn/} for more information.
    """

    def __init__(self, t, Xgen0, Pgen, Vgen0, Xexc0, Pexc, Vexc0, Xgov0, Pgov, Vgov0, augYbus_solver, gbus, stepsize):
        super(self, RungeKuttaFehlberg).__init__(t, Xgen0, Pgen, Vgen0, Xexc0, Pexc, Vexc0, Xgov0, Pgov, Vgov0, augYbus_solver, gbus, stepsize)
        self._a = array([0.0, 0.0, 0.0, 0.0, 0.0, 1.0 / 4.0, 0.0, 0.0, 0.0, 0.0,
         3.0 / 32.0, 9.0 / 32.0, 0.0, 0.0, 0.0, 1932.0 / 2197.0,
         -7200.0 / 2197.0, 7296.0 / 2197.0, 0.0, 0.0, 439.0 / 216.0,
         -8.0, 3680.0 / 513.0, -845.0 / 4104.0, 0.0, -8.0 / 27.0,
         2.0, -3544.0 / 2565.0, 1859.0 / 4104.0, -11.0 / 40.0])
        self._b1 = array([25.0 / 216.0, 0.0, 1408.0 / 2565.0, 2197.0 / 4104.0,
         -1.0 / 5.0, 0.0])
        self._b2 = array([16.0 / 135.0, 0.0, 6656.0 / 12825.0, 28561.0 / 56430.0,
         -9.0 / 50.0, 2.0 / 55.0])

    def solve(self):
        case = self.dyn_case
        b2 = self._b2
        accept = False
        facmax = 4
        failed = False
        i = 0
        while accept == False:
            i += 1
            (Xexc1, Vexc1, Kexc1, Xgov1, Vgov1, Kgov1, Xgen1, Vgen1, Kgen1, _) = self._k1()
            (Xexc2, Vexc2, Kexc2, Xgov2, Vgov2, Kgov2, Xgen2, Vgen2, Kgen2, _) = self._k2(Xexc1, Vexc1, Kexc1, Xgov1, Vgov1, Kgov1, Xgen1, Vgen1, Kgen1)
            (Xexc3, Vexc3, Kexc3, Xgov3, Vgov3, Kgov3, Xgen3, Vgen3, Kgen3, _) = self._k3(Xexc2, Vexc2, Kexc2, Kexc1, Xgov2, Vgov2, Kgov2, Kgov1, Xgen2, Vgen2, Kgen2, Kgen1)
            (Xexc4, Vexc4, Kexc4, Xgov4, Vgov4, Kgov4, Xgen4, Vgen4, Kgen4, _) = self._k4(Xexc3, Vexc3, Kexc3, Kexc2, Kexc1, Xgov3, Vgov3, Kgov3, Kgov2, Kgov1, Xgen3, Vgen3, Kgen3, Kgen2, Kgen1)
            (Xexc5, Vexc5, Kexc5, Xgov5, Vgov5, Kgov5, Xgen5, Vgen5, Kgen5, _) = self._k5(Xexc4, Vexc4, Kexc4, Kexc3, Kexc2, Kexc1, Xgov4, Vgov4, Kgov4, Kgov3, Kgov2, Kgov1, Xgen4, Vgen4, Kgen4, Kgen3, Kgen2, Kgen1)
            (Xexc6, Vexc6, Kexc6, Xgov6, Vgov6, Kgov6, Xgen6, Vgen6, Kgen6, U6) = self._k6(Xexc5, Vexc5, Kexc5, Kexc4, Kexc3, Kexc2, Kexc1, Xgov5, Vgov5, Kgov5, Kgov4, Kgov3, Kgov2, Kgov1, Xgen5, Vgen5, Kgen5, Kgen4, Kgen3, Kgen2, Kgen1)
            Xexc62 = self.Xexc0 + case.stepsize * (b2[0] * Kexc1 + b2[1] * Kexc2 + b2[2] * Kexc3 + b2[3] * Kexc4 + b2[4] * Kexc5 + b2[5] * Kexc6)
            Xgov62 = self.Xgov0 + case.stepsize * (b2[0] * Kgov1 + b2[1] * Kgov2 + b2[2] * Kgov3 + b2[3] * Kgov4 + b2[4] * Kgov5 + b2[5] * Kgov6)
            Xgen62 = self.Xgen0 + case.stepsize * (b2[0] * Kgen1 + b2[1] * Kgen2 + b2[2] * Kgen3 + b2[3] * Kgen4 + b2[4] * Kgen5 + b2[5] * Kgen6)
            Xexc = abs((Xexc62 - Xexc6).T)
            Xgov = abs((Xgov62 - Xgov6).T)
            Xgen = abs((Xgen62 - Xgen6).T)
            errest = max(r_[(max(max(Xexc)), max(max(Xgov)), max(max(Xgen)))])
            if errest < EPS:
                errest = EPS
            q = 0.84 * (self.tol / errest) ^ 1.0 / 4.0
            if errest < self.tol:
                accept = True
                U0 = U6
                Vgen0 = Vgen6
                Vgov0 = Vgov6
                Vexc0 = Vexc6
                Xgen0 = Xgen6
                Xexc0 = Xexc6
                Xgov0 = Xgov6
                Pgen0 = self.Pgen
                Pexc0 = self.Pexc
                Pgov0 = self.Pgov
            else:
                failed += 1
                facmax = 1
                Pgen0 = self.Pgen
                Pexc0 = self.Pexc
                Pgov0 = self.Pgov
                stepsize = min(max(q, 0.1), facmax) * case.stepsize
                return
            stepsize = min(max(q, 0.1), facmax) * case.stepsize
            if stepsize > self.maxstepsize:
                stepsize = self.maxstepsize

        return (Xgen0, Pgen0, Vgen0, Xexc0, Pexc0, Vexc0, Xgov0, Pgov0, Vgov0,
         U0, errest, failed, self.t, stepsize)

    def _k4(self, Xexc3, Vexc3, Kexc3, Kexc2, Kexc1, Xgov3, Vgov3, Kgov3, Kgov2, Kgov1, Xgen3, Vgen3, Kgen3, Kgen2, Kgen1):
        case = self.dyn_case
        a = self._a
        Kexc4 = case.exciter(Xexc3, self.Pexc, Vexc3)
        Xexc4 = self.Xexc0 + case.stepsize * (a[(4, 0)] * Kexc1 + a[(4, 1)] * Kexc2 + a[(4,
                                                                                         2)] * Kexc3 + a[(4,
                                                                                                          3)] * Kexc4)
        Kgov4 = case.governor(Xgov3, self.Pgov, Vgov3)
        Xgov4 = self.Xgov0 + case.stepsize * (a[(4, 0)] * Kgov1 + a[(4, 1)] * Kgov2 + a[(4,
                                                                                         2)] * Kgov3 + a[(4,
                                                                                                          3)] * Kgov4)
        Kgen4 = case.generator(Xgen3, Xexc4, Xgov4, self.Pgen, Vgen3)
        Xgen4 = self.Xgen0 + case.stepsize * (a[(4, 0)] * Kgen1 + a[(4, 1)] * Kgen2 + a[(4,
                                                                                         2)] * Kgen3 + a[(4,
                                                                                                          3)] * Kgen4)
        U4 = case.solveNetwork(Xgen4, self.Pgen, self.augYbus_solver, self.gbus)
        (Id4, Iq4, Pe4) = case.machineCurrents(Xgen4, self.Pgen, U4[self.gbus])
        Vexc4 = abs(U4[self.gbus])
        Vgen4 = r_[(Id4, Iq4, Pe4)]
        Vgov4 = Xgen4[:, 1]
        return (
         Xexc4, Vexc4, Kexc4, Xgov4, Vgov4, Kgov4, Xgen4, Vgen4, Kgen4, U4)

    def _k5(self, Xexc4, Vexc4, Kexc4, Kexc3, Kexc2, Kexc1, Xgov4, Vgov4, Kgov4, Kgov3, Kgov2, Kgov1, Xgen4, Vgen4, Kgen4, Kgen3, Kgen2, Kgen1):
        case = self.dyn_case
        a = self._a
        Kexc5 = case.exciter(Xexc4, self.Pexc, Vexc4)
        Xexc5 = self.Xexc0 + case.stepsize * (a[(5, 0)] * Kexc1 + a[(5, 1)] * Kexc2 + a[(5,
                                                                                         2)] * Kexc3 + a[(5,
                                                                                                          3)] * Kexc4 + a[(5,
                                                                                                                           4)] * Kexc5)
        Kgov5 = case.governor(Xgov4, self.Pgov, Vgov4)
        Xgov5 = self.Xgov0 + case.stepsize * (a[(5, 0)] * Kgov1 + a[(5, 1)] * Kgov2 + a[(5,
                                                                                         2)] * Kgov3 + a[(5,
                                                                                                          3)] * Kgov4 + a[(5,
                                                                                                                           4)] * Kgov5)
        Kgen5 = case.generator(Xgen4, Xexc5, Xgov5, self.Pgen, Vgen4)
        Xgen5 = self.Xgen0 + case.stepsize * (a[(5, 0)] * Kgen1 + a[(5, 1)] * Kgen2 + a[(5,
                                                                                         2)] * Kgen3 + a[(5,
                                                                                                          3)] * Kgen4 + a[(5,
                                                                                                                           4)] * Kgen5)
        U5 = case.solveNetwork(Xgen5, self.Pgen, self.augYbus_solver, self.gbus)
        (Id5, Iq5, Pe5) = case.machineCurrents(Xgen5, self.Pgen, U5[self.gbus])
        Vexc5 = abs(U5[self.gbus])
        Vgen5 = r_[(Id5, Iq5, Pe5)]
        Vgov5 = Xgen5[:, 1]
        return (
         Xexc5, Vexc5, Kexc5, Xgov5, Vgov5, Kgov5, Xgen5, Vgen5, Kgen5, U5)

    def _k6(self, Xexc5, Vexc5, Kexc5, Kexc4, Kexc3, Kexc2, Kexc1, Xgov5, Vgov5, Kgov5, Kgov4, Kgov3, Kgov2, Kgov1, Xgen5, Vgen5, Kgen5, Kgen4, Kgen3, Kgen2, Kgen1):
        case = self.dyn_case
        b1 = self._b1
        Kexc6 = case.exciter(Xexc5, self.Pexc, Vexc5)
        Xexc6 = self.Xexc0 + case.stepsize * (b1[0] * Kexc1 + b1[1] * Kexc2 + b1[2] * Kexc3 + b1[3] * Kexc4 + b1[4] * Kexc5 + b1[5] * Kexc6)
        Kgov6 = case.governor(Xgov5, self.Pgov, Vgov5)
        Xgov6 = self.Xgov0 + case.stepsize * (b1[0] * Kgov1 + b1[1] * Kgov2 + b1[2] * Kgov3 + b1[3] * Kgov4 + b1[4] * Kgov5 + b1[5] * Kgov6)
        Kgen6 = case.generator(Xgen5, Xexc6, Xgov6, self.Pgen, Vgen5)
        Xgen6 = self.Xgen0 + case.stepsize * (b1[0] * Kgen1 + b1[1] * Kgen2 + b1[2] * Kgen3 + b1[3] * Kgen4 + b1[4] * Kgen5 + b1[5] * Kgen6)
        U6 = case.solveNetwork(Xgen6, self.Pgen, self.augYbus_solver, self.gbus)
        (Id6, Iq6, Pe6) = case.machineCurrents(Xgen6, self.Pgen, U6[self.gbus])
        Vexc6 = abs(U6[self.gbus])
        Vgen6 = r_[(Id6, Iq6, Pe6)]
        Vgov6 = Xgen6[:, 1]
        return (
         Xexc6, Vexc6, Kexc6, Xgov6, Vgov6, Kgov6, Xgen6, Vgen6, Kgen6, U6)


class RungeKuttaHighamHall(RungeKuttaFehlberg):
    """ Runge-Kutta Higham and Hall ODE solver.

    Based on RungeKuttaHighamHall.m from MatDyn by Stijn Cole, developed at
    Katholieke Universiteit Leuven. See U{http://www.esat.kuleuven.be/electa/
    teaching/matdyn/} for more information.
    """

    def __init__(self, t, Xgen0, Pgen, Vgen0, Xexc0, Pexc, Vexc0, Xgov0, Pgov, Vgov0, augYbus_solver, gbus, stepsize):
        super(self, RungeKuttaHighamHall).__init__(t, Xgen0, Pgen, Vgen0, Xexc0, Pexc, Vexc0, Xgov0, Pgov, Vgov0, augYbus_solver, gbus, stepsize)
        self._a = array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0 / 9.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 1.0 / 12.0, 1.0 / 4.0, 0.0, 0.0, 0.0, 0.0,
         1.0 / 8.0, 0.0, 3.0 / 8.0, 0.0, 0.0, 0.0, 91.0 / 500.0,
         -27.0 / 100.0, 78.0 / 125.0, 8.0 / 125.0, 0.0, 0.0,
         -11.0 / 20.0, 27.0 / 20.0, 12.0 / 5.0, -36.0 / 5.0, 5.0, 0.0,
         1.0 / 12.0, 0.0, 27.0 / 32.0, -4.0 / 3.0, 125.0 / 96.0,
         5.0 / 48.0])
        self._b1 = array([1.0 / 12.0, 0.0, 27.0 / 32.0, -4.0 / 3.0, 125.0 / 96.0,
         5.0 / 48.0, 0.0])
        self._b2 = array([2.0 / 15.0, 0.0, 27.0 / 80.0, -2.0 / 15.0, 25.0 / 48.0,
         1.0 / 24.0, 1.0 / 10.0])

    def solve(self):
        case = self.dyn_case
        b2 = self._b2
        accept = False
        facmax = 4
        failed = False
        i = 0
        while accept == False:
            i += 1
            (Xexc1, Vexc1, Kexc1, Xgov1, Vgov1, Kgov1, Xgen1, Vgen1, Kgen1, _) = self._k1()
            (Xexc2, Vexc2, Kexc2, Xgov2, Vgov2, Kgov2, Xgen2, Vgen2, Kgen2, _) = self._k2(Xexc1, Vexc1, Kexc1, Xgov1, Vgov1, Kgov1, Xgen1, Vgen1, Kgen1)
            (Xexc3, Vexc3, Kexc3, Xgov3, Vgov3, Kgov3, Xgen3, Vgen3, Kgen3, _) = self._k3(Xexc2, Vexc2, Kexc2, Kexc1, Xgov2, Vgov2, Kgov2, Kgov1, Xgen2, Vgen2, Kgen2, Kgen1)
            (Xexc4, Vexc4, Kexc4, Xgov4, Vgov4, Kgov4, Xgen4, Vgen4, Kgen4, _) = self._k4(Xexc3, Vexc3, Kexc3, Kexc2, Kexc1, Xgov3, Vgov3, Kgov3, Kgov2, Kgov1, Xgen3, Vgen3, Kgen3, Kgen2, Kgen1)
            (Xexc5, Vexc5, Kexc5, Xgov5, Vgov5, Kgov5, Xgen5, Vgen5, Kgen5, _) = self._k5(Xexc4, Vexc4, Kexc4, Kexc3, Kexc2, Kexc1, Xgov4, Vgov4, Kgov4, Kgov3, Kgov2, Kgov1, Xgen4, Vgen4, Kgen4, Kgen3, Kgen2, Kgen1)
            (Xexc6, Vexc6, Kexc6, Xgov6, Vgov6, Kgov6, Xgen6, Vgen6, Kgen6, _) = self._k6(Xexc5, Vexc5, Kexc5, Kexc4, Kexc3, Kexc2, Kexc1, Xgov5, Vgov5, Kgov5, Kgov4, Kgov3, Kgov2, Kgov1, Xgen5, Vgen5, Kgen5, Kgen4, Kgen3, Kgen2, Kgen1)
            (Xexc7, _, Kexc7, Xgov7, _, Kgov7, Xgen7, _, Kgen7, U7) = self._k6(Xexc6, Vexc6, Kexc6, Kexc5, Kexc4, Kexc3, Kexc2, Kexc1, Xgov6, Vgov6, Kgov6, Kgov5, Kgov4, Kgov3, Kgov2, Kgov1, Xgen6, Vgen6, Kgen6, Kgen5, Kgen4, Kgen3, Kgen2, Kgen1)
            Xexc72 = self.Xexc0 + case.stepsize * (b2[0] * Kexc1 + b2[1] * Kexc2 + b2[2] * Kexc3 + b2[3] * Kexc4 + b2[4] * Kexc5 + b2[5] * Kexc6 + b2[6] * Kexc7)
            Xgov72 = self.Xgov0 + case.stepsize * (b2[0] * Kgov1 + b2[1] * Kgov2 + b2[2] * Kgov3 + b2[3] * Kgov4 + b2[4] * Kgov5 + b2[5] * Kgov6 + b2[6] * Kgov7)
            Xgen72 = self.Xgen0 + case.stepsize * (b2[0] * Kgen1 + b2[1] * Kgen2 + b2[2] * Kgen3 + b2[3] * Kgen4 + b2[4] * Kgen5 + b2[5] * Kgen6 + b2[6] * Kgen7)
            Xexc = abs((Xexc72 - Xexc7).T)
            Xgov = abs((Xgov72 - Xgov7).T)
            Xgen = abs((Xgen72 - Xgen7).T)
            errest = max(r_[(max(max(Xexc)), max(max(Xgov)), max(max(Xgen)))])
            if errest < EPS:
                errest = EPS
            q = 0.84 * (self.tol / errest) ^ 1.0 / 4.0
            if errest < self.tol:
                accept = True
                U0 = U7
                Vgen0 = Vgen6
                Vgov0 = Vgov6
                Vexc0 = Vexc6
                Xgen0 = Xgen6
                Xexc0 = Xexc6
                Xgov0 = Xgov6
                Pgen0 = self.Pgen
                Pexc0 = self.Pexc
                Pgov0 = self.Pgov
            else:
                failed += 1
                facmax = 1
                Pgen0 = self.Pgen
                Pexc0 = self.Pexc
                Pgov0 = self.Pgov
                stepsize = min(max(q, 0.1), facmax) * case.stepsize
                return
            stepsize = min(max(q, 0.1), facmax) * case.stepsize
            if stepsize > self.maxstepsize:
                stepsize = self.maxstepsize

        return (Xgen0, Pgen0, Vgen0, Xexc0, Pexc0, Vexc0, Xgov0, Pgov0, Vgov0,
         U0, errest, failed, self.t, stepsize)

    def _k6(self, Xexc5, Vexc5, Kexc5, Kexc4, Kexc3, Kexc2, Kexc1, Xgov5, Vgov5, Kgov5, Kgov4, Kgov3, Kgov2, Kgov1, Xgen5, Vgen5, Kgen5, Kgen4, Kgen3, Kgen2, Kgen1):
        case = self.dyn_case
        a = self._a
        Kexc6 = case.exciter(Xexc5, self.Pexc, Vexc5)
        Xexc6 = self.Xexc0 + case.stepsize * (a[(6, 0)] * Kexc1 + a[(6, 1)] * Kexc2 + a[(6,
                                                                                         2)] * Kexc3 + a[(6,
                                                                                                          3)] * Kexc4 + a[(6,
                                                                                                                           4)] * Kexc5 + a[(6,
                                                                                                                                            5)] * Kexc6)
        Kgov6 = case.governor(Xgov5, self.Pgov, Vgov5)
        Xgov6 = self.Xgov0 + case.stepsize * (a[(6, 0)] * Kgov1 + a[(6, 1)] * Kgov2 + a[(6,
                                                                                         2)] * Kgov3 + a[(6,
                                                                                                          3)] * Kgov4 + a[(6,
                                                                                                                           4)] * Kgov5 + a[(6,
                                                                                                                                            5)] * Kgov6)
        Kgen6 = case.generator(Xgen5, Xexc6, Xgov6, self.Pgen, Vgen5)
        Xgen6 = self.Xgen0 + case.stepsize * (a[(6, 0)] * Kgen1 + a[(6, 1)] * Kgen2 + a[(6,
                                                                                         2)] * Kgen3 + a[(6,
                                                                                                          3)] * Kgen4 + a[(6,
                                                                                                                           4)] * Kgen5 + a[(6,
                                                                                                                                            5)] * Kgen6)
        U6 = case.solveNetwork(Xgen6, self.Pgen, self.augYbus_solver, self.gbus)
        (Id6, Iq6, Pe6) = case.machineCurrents(Xgen6, self.Pgen, U6[self.gbus])
        Vexc6 = abs(U6[self.gbus])
        Vgen6 = r_[(Id6, Iq6, Pe6)]
        Vgov6 = Xgen6[:, 1]
        return (
         Xexc6, Vexc6, Kexc6, Xgov6, Vgov6, Kgov6, Xgen6, Vgen6, Kgen6, U6)

    def _k7(self, Xexc6, Vexc6, Kexc6, Kexc5, Kexc4, Kexc3, Kexc2, Kexc1, Xgov6, Vgov6, Kgov6, Kgov5, Kgov4, Kgov3, Kgov2, Kgov1, Xgen6, Vgen6, Kgen6, Kgen5, Kgen4, Kgen3, Kgen2, Kgen1):
        case = self.dyn_case
        b1 = self.b1
        Kexc7 = case.exciter(Xexc6, self.Pexc, Vexc6)
        Xexc7 = self.Xexc0 + case.stepsize * (b1[0] * Kexc1 + b1[1] * Kexc2 + b1[2] * Kexc3 + b1[3] * Kexc4 + b1[4] * Kexc5 + b1[5] * Kexc6 + b1[6] * Kexc7)
        Kgov7 = case.governor(Xgov6, self.Pgov, Vgov6)
        Xgov7 = self.Xgov0 + case.stepsize * (b1[0] * Kgov1 + b1[1] * Kgov2 + b1[2] * Kgov3 + b1[3] * Kgov4 + b1[4] * Kgov5 + b1[5] * Kgov6 + b1[6] * Kgov7)
        Kgen7 = case.generator(Xgen6, Xexc7, Xgov7, self.Pgen, Vgen6)
        Xgen7 = self.Xgen0 + case.stepsize * (b1[0] * Kgen1 + b1[1] * Kgen2 + b1[2] * Kgen3 + b1[3] * Kgen4 + b1[4] * Kgen5 + b1[5] * Kgen6 + b1[6] * Kgen7)
        U7 = case.solveNetwork(Xgen7, self.Pgen, self.augYbus_solver, self.gbus)
        (Id7, Iq7, Pe7) = case.machineCurrents(Xgen7, self.Pgen, U7[self.gbus])
        Vexc7 = abs(U7[self.gbus])
        Vgen7 = r_[(Id7, Iq7, Pe7)]
        Vgov7 = Xgen7[:, 1]
        return (
         Xexc7, Vexc7, Kexc7, Xgov7, Vgov7, Kgov7, Xgen7, Vgen7, Kgen7, U7)


class ModifiedEuler2(object):
    """ Modified Euler ODE solver with check on interface errors.

    Based on ModifiedEuler2.m from MatDyn by Stijn Cole, developed at
    Katholieke Universiteit Leuven. See U{http://www.esat.kuleuven.be/electa/
    teaching/matdyn/} for more information.
    """

    def __init__(self, t, Xgen0, Pgen, Vgen0, Xexc0, Pexc, Vexc0, Xgov0, Pgov, Vgov0, augYbus_solver, gbus, stepsize):
        self.dyn_case = None
        self.t = t
        self.Xgen0
        self.Pgen
        self.Vgen0
        self.Xexc0
        self.Pexc
        self.Vexc0
        self.Xgov0
        self.Pgov
        self.Vgov0
        self.augYbus_solver
        self.gbus
        self.stepsize
        return

    def solve(self):
        case = self.dyn_case
        eulerfailed = False
        dFexc0 = case.exciter(self.Xexc0, self.Pexc, self.Vexc0)
        Xexc_new = self.Xexc0 + case.stepsize * dFexc0
        dFgov0 = case.governor(self.Xgov0, self.Pgov, self.Vgov0)
        Xgov_new = self.Xgov0 + case.stepsize * dFgov0
        dFgen0 = case.generator(self.Xgen0, Xexc_new, Xgov_new, self.Pgen, self.Vgen0)
        Xgen_new = self.Xgen0 + case.stepsize * dFgen0
        Vexc_new = self.Vexc0
        Vgov_new = self.Vgov0
        Vgen_new = self.Vgen0
        for i in range(self.maxit):
            Xexc_old = Xexc_new
            Xgov_old = Xgov_new
            Xgen_old = Xgen_new
            Vexc_old = Vexc_new
            Vgov_old = Vgov_new
            Vgen_old = Vgen_new
            U_new = case.solveNetwork(Xgen_new, self.Pgen, self.augYbus_solver, self.gbus)
            (Id_new, Iq_new, Pe_new) = case.machineCurrents(Xgen_new, self.Pgen, U_new[self.gbus])
            Vgen_new = r_[(Id_new, Iq_new, Pe_new)]
            Vexc_new = abs(U_new[self.gbus])
            Vgov_new = Xgen_new[:, 1]
            dFexc1 = case.exciter(Xexc_old, self.Pexc, Vexc_new)
            Xexc_new = self.Xexc0 + case.stepsize / 2.0 * (dFexc0 + dFexc1)
            dFgov1 = case.governor(Xgov_old, self.Pgov, Vgov_new)
            Xgov_new = self.Xgov0 + case.stepsize / 2.0 * (dFgov0 + dFgov1)
            dFgen1 = case.generator(Xgen_old, Xexc_new, Xgov_new, self.Pgen, Vgen_new)
            Xgen_new = self.Xgen0 + case.stepsize / 2.0 * (dFgen0 + dFgen1)
            Xexc_d = abs((Xexc_new - Xexc_old).T)
            Xgov_d = abs((Xgov_new - Xgov_old).T)
            Xgen_d = abs((Xgen_new - Xgen_old).T)
            Vexc_d = abs((Vexc_new - Vexc_old).T)
            Vgov_d = abs((Vgov_new - Vgov_old).T)
            Vgen_d = abs((Vgen_new - Vgen_old).T)
            errest = max(r_[(max(max(Vexc_d)), max(max(Vgov_d)), max(max(Vgen_d)), max(max(Xexc_d)), max(max(Xgov_d)), max(max(Xgen_d)))])
            if errest < self.tol:
                break
            elif i == self.maxit:
                U0 = U_new
                Vexc0 = Vexc_new
                Vgov0 = Vgov_new
                Vgen0 = Vgen_new
                Xgen0 = Xgen_new
                Xexc0 = Xexc_new
                Xgov0 = Xgov_new
                Pgen0 = self.Pgen
                Pexc0 = self.Pexc
                Pgov0 = self.Pgov
                eulerfailed = True
                return (
                 Xgen0, Pgen0, Vgen0, Xexc0, Pexc0, Vexc0, Xgov0,
                 Pgov0, Vgov0, U0, self.t, eulerfailed, case.stepsize)

        U0 = U_new
        Vexc0 = Vexc_new
        Vgov0 = Vgov_new
        Vgen0 = Vgen_new
        Xgen0 = Xgen_new
        Xexc0 = Xexc_new
        Xgov0 = Xgov_new
        Pgen0 = self.Pgen
        Pexc0 = self.Pexc
        Pgov0 = self.Pgov
        return (
         Xgen0, Pgen0, Vgen0, Xexc0, Pexc0, Vexc0, Xgov0, Pgov0, Vgov0,
         U0, self.t, eulerfailed, case.stepsize)


class DynamicGenerator(object):
    """ Defines a classical generator model and a fourth order generator model
    for dynamic simulation.
    """

    def __init__(self, generator, exciter, governor, model=CLASSICAL, h=1.0, d=0.01, x=1.0, x_tr=1.0, xd=1.0, xq=1.0, xd_tr=1.0, xq_tr=1.0, td=1.0, tq=1.0):
        self.generator = generator
        self.exciter = exciter
        self.governor = governor
        self.model = model
        self.h = h
        self.d = d
        self.x = x
        self.x_tr = x_tr
        self.xd = xd
        self.xq = xq
        self.xd_tr = xd_tr
        self.xq_tr = xq_tr
        self.td = td
        self.tq = tq


class Exciter(object):
    """ Defines an IEEE DC1A excitation system.
    """

    def __init__(self, generator, model=CONST_EXCITATION, ka=0.0, ta=0.0, ke=0.0, te=0.0, kf=0.0, tf=0.0, aex=0.0, bex=0.0, ur_min=-1.5, ur_max=1.5):
        self.generator = generator
        self.model = model
        self.ka = ka
        self.ta = ta
        self.ke = ke
        self.te = te
        self.kf = kf
        self.tf = tf
        self.aex = aex
        self.bex = bex
        self.ur_min = ur_min
        self.ur_max = ur_max


class Governor(object):
    """ Defines an IEEE model of a general speed-governing system for steam
    turbines. It can represent a mechanical-hydraulic or electro-hydraulic
    system by the appropriate selection of parameters.
    """

    def __init__(self, generator, model=CONST_POWER, k=0.0, t1=0.0, t2=0.0, t3=0.0, p_up=0.0, p_down=0.0, p_max=0.0, p_min=0.0):
        self.generator = generator
        self.model = model
        self.k = k
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.p_up = p_up
        self.p_down = p_down
        self.p_max = p_max
        self.p_min = p_min


class Event(object):
    """ Defines an event.
    """

    def __init__(self, time, type):
        """ Constructs a new Event instance.
        """
        self.time = time
        self.type = type


class BusChange(object):
    """ Defines a bus parameter change event.

    Three-phase bus faults can be simulated by changing the shunt
    susceptance of the bus in a bus change event.
    """

    def __init__(self, bus, time, param, newval):
        self.bus = bus
        self.time = time
        self.param = param
        self.newval = newval


class BranchChange(object):
    """ Defines a branch parameter change event.
    """

    def __init__(self, branch, time, param, newval):
        self.branch = branch
        self.time = time
        self.param = param
        self.newval = newval