# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pylon\solver.py
# Compiled at: 2010-12-26 13:36:33
""" Defines a DC OPF solver and an AC OPF solver.

Based on dcopf_solver.m  and mipsopf_solver.m from MATPOWER by Ray Zimmerman,
developed at  Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more
information.
"""
import logging
from numpy import array, pi, polyder, polyval, exp, conj, Inf, ones, r_, zeros, asarray
from scipy.sparse import lil_matrix, csr_matrix, hstack, vstack
from case import REFERENCE
from generator import POLYNOMIAL, PW_LINEAR
from pips import pips, qps_pips
SFLOW = 'Sflow'
PFLOW = 'Pflow'
IFLOW = 'Iflow'
logger = logging.getLogger(__name__)

class _Solver(object):
    """ Defines a base class for many solvers.
    """

    def __init__(self, om):
        self.om = om
        self._nieq = 0

    def solve(self):
        """ Solves optimal power flow and returns a results dict.
        """
        raise NotImplementedError

    def _unpack_model(self, om):
        """ Returns data from the OPF model.
        """
        buses = om.case.connected_buses
        branches = om.case.online_branches
        gens = om.case.online_generators
        cp = om.get_cost_params()
        return (
         buses, branches, gens, cp)

    def _dimension_data(self, buses, branches, generators):
        """ Returns the problem dimensions.
        """
        ipol = [ i for (i, g) in enumerate(generators) if g.pcost_model == POLYNOMIAL
               ]
        ipwl = [ i for (i, g) in enumerate(generators) if g.pcost_model == PW_LINEAR
               ]
        nb = len(buses)
        nl = len(branches)
        nw = self.om.cost_N
        if 'y' in [ v.name for v in self.om.vars ]:
            ny = self.om.get_var_N('y')
        else:
            ny = 0
        nxyz = self.om.var_N
        return (
         ipol, ipwl, nb, nl, nw, ny, nxyz)

    def _linear_constraints(self, om):
        """ Returns the linear problem constraints.
        """
        (A, l, u) = om.linear_constraints()
        return (
         A, l, u)

    def _var_bounds(self):
        """ Returns bounds on the optimisation variables.
        """
        x0 = array([])
        xmin = array([])
        xmax = array([])
        for var in self.om.vars:
            x0 = r_[(x0, var.v0)]
            xmin = r_[(xmin, var.vl)]
            xmax = r_[(xmax, var.vu)]

        return (x0, xmin, xmax)

    def _initial_interior_point(self, buses, generators, xmin, xmax, ny):
        """ Selects an interior initial point for interior point solver.
        """
        Va = self.om.get_var('Va')
        va_refs = [ b.v_angle * pi / 180.0 for b in buses if b.type == REFERENCE
                  ]
        x0 = (xmin + xmax) / 2.0
        x0[(Va.i1):(Va.iN + 1)] = va_refs[0]
        if ny > 0:
            yvar = self.om.get_var('y')
            c = []
            for g in generators:
                if g.pcost_model == PW_LINEAR:
                    for (_, y) in g.p_cost:
                        c.append(y)

            x0[(yvar.i1):(yvar.iN + 1)] = max(c) * 1.1
        return x0


class DCOPFSolver(_Solver):
    """ Defines a solver for DC optimal power flow [3].

    Based on dcopf_solver.m from MATPOWER by Ray Zimmerman, developed at PSERC
    Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more info.
    """

    def __init__(self, om, opt=None):
        """ Initialises a new DCOPFSolver instance.
        """
        super(DCOPFSolver, self).__init__(om)
        self.N = None
        self.H = None
        self.Cw = zeros((0, 0))
        self.fparm = zeros((0, 0))
        self.opt = {} if opt is None else opt
        return

    def solve(self):
        """ Solves DC optimal power flow and returns a results dict.
        """
        base_mva = self.om.case.base_mva
        Bf = self.om._Bf
        Pfinj = self.om._Pfinj
        (bs, ln, gn, cp) = self._unpack_model(self.om)
        (ipol, ipwl, nb, nl, nw, ny, nxyz) = self._dimension_data(bs, ln, gn)
        (AA, ll, uu) = self._linear_constraints(self.om)
        (Npwl, Hpwl, Cpwl, fparm_pwl, any_pwl) = self._pwl_costs(ny, nxyz, ipwl)
        (Npol, Hpol, Cpol, fparm_pol, polycf, npol) = self._quadratic_costs(gn, ipol, nxyz, base_mva)
        (NN, HHw, CCw, ffparm) = self._combine_costs(Npwl, Hpwl, Cpwl, fparm_pwl, any_pwl, Npol, Hpol, Cpol, fparm_pol, npol, nw)
        (HH, CC, C0) = self._transform_coefficients(NN, HHw, CCw, ffparm, polycf, any_pwl, npol, nw)
        (_, xmin, xmax) = self._var_bounds()
        x0 = self._initial_interior_point(bs, gn, xmin, xmax, ny)
        s = self._run_opf(HH, CC, AA, ll, uu, xmin, xmax, x0, self.opt)
        (Va, Pg) = self._update_solution_data(s, HH, CC, C0)
        self._update_case(bs, ln, gn, base_mva, Bf, Pfinj, Va, Pg, s['lmbda'])
        return s

    def _pwl_costs(self, ny, nxyz, ipwl):
        """ Returns the piece-wise linear components of the objective function.
        """
        any_pwl = int(ny > 0)
        if any_pwl:
            y = self.om.get_var('y')
            Npwl = csr_matrix((ones(ny), (zeros(ny), array(ipwl) + y.i1)))
            Hpwl = csr_matrix((1, 1))
            Cpwl = array([1])
            fparm_pwl = array([[1.0, 0.0, 0.0, 1.0]])
        else:
            Npwl = None
            Hpwl = None
            Cpwl = array([])
            fparm_pwl = zeros((0, 4))
        return (Npwl, Hpwl, Cpwl, fparm_pwl, any_pwl)

    def _quadratic_costs(self, generators, ipol, nxyz, base_mva):
        """ Returns the quadratic cost components of the objective function.
        """
        npol = len(ipol)
        rnpol = range(npol)
        gpol = [ g for g in generators if g.pcost_model == POLYNOMIAL ]
        if [ g for g in gpol if len(g.p_cost) > 3 ]:
            logger.error('Order of polynomial cost greater than quadratic.')
        iqdr = [ i for (i, g) in enumerate(generators) if g.pcost_model == POLYNOMIAL if len(g.p_cost) == 3
               ]
        ilin = [ i for (i, g) in enumerate(generators) if g.pcost_model == POLYNOMIAL if len(g.p_cost) == 2
               ]
        polycf = zeros((npol, 3))
        if npol > 0:
            if len(iqdr) > 0:
                polycf[iqdr, :] = array([ list(g.p_cost) for g in generators
                                        ])
            if len(ilin) > 0:
                polycf[ilin, 1:] = array([ list(g.p_cost[:2]) for g in generators
                                         ])
            polycf = polycf * array([base_mva ** 2, base_mva, 1])
            Pg = self.om.get_var('Pg')
            Npol = csr_matrix((ones(npol), (rnpol, Pg.i1 + array(ipol))), (
             npol, nxyz))
            Hpol = csr_matrix((2 * polycf[:, 0], (rnpol, rnpol)), (npol, npol))
            Cpol = polycf[:, 1]
            fparm_pol = (ones(npol) * array([[1], [0], [0], [1]])).T
        else:
            Npol = Hpol = None
            Cpol = array([])
            fparm_pol = zeros((0, 4))
        return (Npol, Hpol, Cpol, fparm_pol, polycf, npol)

    def _combine_costs(self, Npwl, Hpwl, Cpwl, fparm_pwl, any_pwl, Npol, Hpol, Cpol, fparm_pol, npol, nw):
        """ Combines pwl, polynomial and user-defined costs.
        """
        NN = vstack([ n for n in [Npwl, Npol] if n is not None ], 'csr')
        if Hpwl is not None and Hpol is not None:
            Hpwl = hstack([Hpwl, csr_matrix((any_pwl, npol))])
            Hpol = hstack([csr_matrix((npol, any_pwl)), Hpol])
        HHw = vstack([ h for h in [Hpwl, Hpol] if h is not None ], 'csr')
        CCw = r_[(Cpwl, Cpol)]
        ffparm = r_[(fparm_pwl, fparm_pol)]
        return (
         NN, HHw, CCw, ffparm)

    def _transform_coefficients(self, NN, HHw, CCw, ffparm, polycf, any_pwl, npol, nw):
        """ Transforms quadratic coefficients for w into coefficients for x.
        """
        nnw = any_pwl + npol + nw
        M = csr_matrix((ffparm[:, 3], (range(nnw), range(nnw))))
        MR = M * ffparm[:, 2]
        HMR = HHw * MR
        MN = M * NN
        HH = MN.T * HHw * MN
        CC = MN.T * (CCw - HMR)
        C0 = 1.0 / 2.0 * MR.T * HMR + sum(polycf[:, 2])
        return (
         HH, CC, C0[0])

    def _run_opf(self, HH, CC, AA, ll, uu, xmin, xmax, x0, opt):
        """ Solves the either quadratic or linear program.
        """
        N = self._nieq
        if HH.nnz > 0:
            solution = qps_pips(HH, CC, AA, ll, uu, xmin, xmax, x0, opt)
        else:
            solution = qps_pips(None, CC, AA, ll, uu, xmin, xmax, x0, opt)
        return solution

    def _update_solution_data(self, s, HH, CC, C0):
        """ Returns the voltage angle and generator set-point vectors.
        """
        x = s['x']
        Va_v = self.om.get_var('Va')
        Pg_v = self.om.get_var('Pg')
        Va = x[Va_v.i1:Va_v.iN + 1]
        Pg = x[Pg_v.i1:Pg_v.iN + 1]
        s['f'] = s['f'] + C0
        return (
         Va, Pg)

    def _update_case(self, bs, ln, gn, base_mva, Bf, Pfinj, Va, Pg, lmbda):
        """ Calculates the result attribute values.
        """
        Pmis = self.om.get_lin_constraint('Pmis')
        Pf = self.om.get_lin_constraint('Pf')
        Pt = self.om.get_lin_constraint('Pt')
        Pg_v = self.om.get_var('Pg')
        mu_l = lmbda['mu_l']
        mu_u = lmbda['mu_u']
        lower = lmbda['lower']
        upper = lmbda['upper']
        for (i, bus) in enumerate(bs):
            bus.v_angle = Va[i] * 180.0 / pi
            bus.p_lmbda = (mu_u[Pmis.i1:Pmis.iN + 1][i] - mu_l[Pmis.i1:Pmis.iN + 1][i]) / base_mva

        for (l, branch) in enumerate(ln):
            branch.p_from = (Bf * Va + Pfinj)[l] * base_mva
            branch.p_to = -branch.p_from
            branch.mu_s_from = mu_u[Pf.i1:Pf.iN + 1][l] / base_mva
            branch.mu_s_to = mu_u[Pt.i1:Pt.iN + 1][l] / base_mva

        for (k, generator) in enumerate(gn):
            generator.p = Pg[k] * base_mva
            generator.mu_pmin = lower[Pg_v.i1:Pg_v.iN + 1][k] / base_mva
            generator.mu_pmax = upper[Pg_v.i1:Pg_v.iN + 1][k] / base_mva


class PIPSSolver(_Solver):
    """ Solves AC optimal power flow using a primal-dual interior point method.

    Based on mipsopf_solver.m from MATPOWER by Ray Zimmerman, developed at
    PSERC Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more info.
    """

    def __init__(self, om, flow_lim=SFLOW, opt=None):
        """ Initialises a new PIPSSolver instance.
        """
        super(PIPSSolver, self).__init__(om)
        self.flow_lim = flow_lim
        self.opt = {} if opt is None else opt
        return

    def _ref_bus_angle_constraint(self, buses, Va, xmin, xmax):
        """ Adds a constraint on the reference bus angles.
        """
        refs = [ bus._i for bus in buses if bus.type == REFERENCE ]
        Varefs = array([ b.v_angle for b in buses if b.type == REFERENCE ])
        xmin[Va.i1 - 1 + refs] = Varefs
        xmax[Va.iN - 1 + refs] = Varefs
        return (
         xmin, xmax)

    def solve(self):
        """ Solves AC optimal power flow.
        """
        case = self.om.case
        self._base_mva = case.base_mva
        self.opt['cost_mult'] = 0.0001
        (self._bs, self._ln, self._gn, _) = self._unpack_model(self.om)
        (self._ipol, _, self._nb, self._nl, _, self._ny, self._nxyz) = self._dimension_data(self._bs, self._ln, self._gn)
        self._ng = len(self._gn)
        (A, l, u) = self.om.linear_constraints()
        (_, xmin, xmax) = self._var_bounds()
        x0 = self._initial_interior_point(self._bs, self._gn, xmin, xmax, self._ny)
        (self._Ybus, self._Yf, self._Yt) = case.Y
        self._Pg = self.om.get_var('Pg')
        self._Qg = self.om.get_var('Qg')
        self._Va = self.om.get_var('Va')
        self._Vm = self.om.get_var('Vm')
        s = self._solve(x0, A, l, u, xmin, xmax)
        (Vang, Vmag, Pgen, Qgen) = self._update_solution_data(s)
        self._update_case(self._bs, self._ln, self._gn, self._base_mva, self._Yf, self._Yt, Vang, Vmag, Pgen, Qgen, s['lmbda'])
        return s

    def _solve(self, x0, A, l, u, xmin, xmax):
        """ Solves using Python Interior Point Solver (PIPS).
        """
        s = pips(self._costfcn, x0, A, l, u, xmin, xmax, self._consfcn, self._hessfcn, self.opt)
        return s

    def _f(self, x, user_data=None):
        """ Evaluates the objective function.
        """
        p_gen = x[self._Pg.i1:self._Pg.iN + 1]
        q_gen = x[self._Qg.i1:self._Qg.iN + 1]
        xx = r_[(p_gen, q_gen)] * self._base_mva
        if len(self._ipol) > 0:
            f = sum([ g.total_cost(xx[i]) for (i, g) in enumerate(self._gn) ])
        else:
            f = 0
        if self._ny:
            y = self.om.get_var('y')
            self._ccost = csr_matrix((ones(self._ny),
             (
              range(y.i1, y.iN + 1), zeros(self._ny))), shape=(
             self._nxyz, 1)).T
            f = f + self._ccost * x
        else:
            self._ccost = zeros((1, self._nxyz))
        return f

    def _df(self, x, user_data=None):
        """ Evaluates the cost gradient.
        """
        p_gen = x[self._Pg.i1:self._Pg.iN + 1]
        q_gen = x[self._Qg.i1:self._Qg.iN + 1]
        xx = r_[(p_gen, q_gen)] * self._base_mva
        iPg = range(self._Pg.i1, self._Pg.iN + 1)
        iQg = range(self._Qg.i1, self._Qg.iN + 1)
        df_dPgQg = zeros((2 * self._ng, 1))
        for i in self._ipol:
            p_cost = list(self._gn[i].p_cost)
            df_dPgQg[i] = self._base_mva * polyval(polyder(p_cost), xx[i])

        df = zeros((self._nxyz, 1))
        df[iPg] = df_dPgQg[:self._ng]
        df[iQg] = df_dPgQg[self._ng:self._ng + self._ng]
        df = df + self._ccost.T
        return asarray(df).flatten()

    def _d2f(self, x):
        """ Evaluates the cost Hessian.
        """
        d2f_dPg2 = lil_matrix((self._ng, 1))
        d2f_dQg2 = lil_matrix((self._ng, 1))
        for i in self._ipol:
            p_cost = list(self._gn[i].p_cost)
            d2f_dPg2[(i, 0)] = polyval(polyder(p_cost, 2), self._Pg.v0[i] * self._base_mva) * self._base_mva ** 2

        i = r_[(range(self._Pg.i1, self._Pg.iN + 1),
         range(self._Qg.i1, self._Qg.iN + 1))]
        d2f = csr_matrix((vstack([d2f_dPg2, d2f_dQg2]).toarray().flatten(),
         (
          i, i)), shape=(self._nxyz, self._nxyz))
        return d2f

    def _gh(self, x):
        """ Evaluates the constraint function values.
        """
        Pgen = x[self._Pg.i1:self._Pg.iN + 1]
        Qgen = x[self._Qg.i1:self._Qg.iN + 1]
        for (i, gen) in enumerate(self._gn):
            gen.p = Pgen[i] * self._base_mva
            gen.q = Qgen[i] * self._base_mva

        Sbus = self.om.case.getSbus(self._bs)
        Vang = x[self._Va.i1:self._Va.iN + 1]
        Vmag = x[self._Vm.i1:self._Vm.iN + 1]
        V = Vmag * exp(complex(0.0, 1.0) * Vang)
        mis = V * conj(self._Ybus * V) - Sbus
        g = r_[(mis.real,
         mis.imag)]
        flow_max = array([ (l.rate_a / self._base_mva) ** 2 for l in self._ln ])
        for (i, v) in enumerate(flow_max):
            if v == 0.0:
                flow_max[i] = Inf

        if self.flow_lim == IFLOW:
            If = self._Yf * V
            It = self._Yt * V
            h = r_[(If * conj(If) - flow_max,
             It * conj(It) - flow_max)]
        else:
            i_fbus = [ e.from_bus._i for e in self._ln ]
            i_tbus = [ e.to_bus._i for e in self._ln ]
            Sf = V[i_fbus] * conj(self._Yf * V)
            St = V[i_tbus] * conj(self._Yt * V)
            if self.flow_lim == PFLOW:
                h = r_[(Sf.real() ** 2 - flow_max,
                 St.real() ** 2 - flow_max)]
            elif self.flow_lim == SFLOW:
                h = r_[(Sf * conj(Sf) - flow_max,
                 St * conj(St) - flow_max)].real
            else:
                raise ValueError
        return (
         h, g)

    def _dgh(self, x):
        iVa = range(self._Va.i1, self._Va.iN + 1)
        iVm = range(self._Vm.i1, self._Vm.iN + 1)
        iPg = range(self._Pg.i1, self._Pg.iN + 1)
        iQg = range(self._Qg.i1, self._Qg.iN + 1)
        iVaVmPgQg = r_[(iVa, iVm, iPg, iQg)].T
        Vang = x[iVa]
        Vmag = x[iVm]
        V = Vmag * exp(complex(0.0, 1.0) * Vang)
        (dSbus_dVm, dSbus_dVa) = self.om.case.dSbus_dV(self._Ybus, V)
        i_gbus = [ gen.bus._i for gen in self._gn ]
        neg_Cg = csr_matrix((-ones(self._ng),
         (
          i_gbus, range(self._ng))), (
         self._nb, self._ng))
        dg = lil_matrix((self._nxyz, 2 * self._nb))
        blank = csr_matrix((self._nb, self._ng))
        dg[iVaVmPgQg, :] = vstack([
         hstack([dSbus_dVa.real, dSbus_dVm.real, neg_Cg, blank]),
         hstack([dSbus_dVa.imag, dSbus_dVm.imag, blank, neg_Cg])], 'csr').T
        if self.flow_lim == IFLOW:
            (dFf_dVa, dFf_dVm, dFt_dVa, dFt_dVm, Ff, Ft) = self.om.case.dIbr_dV(self._Yf, self._Yt, V)
        else:
            (dFf_dVa, dFf_dVm, dFt_dVa, dFt_dVm, Ff, Ft) = self.om.case.dSbr_dV(self._Yf, self._Yt, V, self._bs, self._ln)
        if self.flow_lim == PFLOW:
            dFf_dVa = dFf_dVa.real
            dFf_dVm = dFf_dVm.real
            dFt_dVa = dFt_dVa.real
            dFt_dVm = dFt_dVm.real
            Ff = Ff.real
            Ft = Ft.real
        (df_dVa, df_dVm, dt_dVa, dt_dVm) = self.om.case.dAbr_dV(dFf_dVa, dFf_dVm, dFt_dVa, dFt_dVm, Ff, Ft)
        dh = lil_matrix((self._nxyz, 2 * self._nl))
        dh[r_[(iVa, iVm)].T, :] = vstack([
         hstack([df_dVa, df_dVm]),
         hstack([dt_dVa, dt_dVm])], 'csr').T
        return (
         dh, dg)

    def _costfcn(self, x):
        """ Evaluates the objective function, gradient and Hessian for OPF.
        """
        f = self._f(x)
        df = self._df(x)
        d2f = self._d2f(x)
        return (
         f, df, d2f)

    def _consfcn(self, x):
        """ Evaluates nonlinear constraints and their Jacobian for OPF.
        """
        (h, g) = self._gh(x)
        (dh, dg) = self._dgh(x)
        return (
         h, g, dh, dg)

    def _hessfcn(self, x, lmbda):
        """ Evaluates Hessian of Lagrangian for AC OPF.
        """
        Pgen = x[self._Pg.i1:self._Pg.iN + 1]
        Qgen = x[self._Qg.i1:self._Qg.iN + 1]
        for (i, g) in enumerate(self._gn):
            g.p = Pgen[i] * self._base_mva
            g.q = Qgen[i] * self._base_mva

        Vang = x[self._Va.i1:self._Va.iN + 1]
        Vmag = x[self._Vm.i1:self._Vm.iN + 1]
        V = Vmag * exp(complex(0.0, 1.0) * Vang)
        nxtra = self._nxyz - 2 * self._nb
        d2f = self._d2f(x) * self.opt['cost_mult']
        nlam = len(lmbda['eqnonlin']) / 2
        lamP = lmbda['eqnonlin'][:nlam]
        lamQ = lmbda['eqnonlin'][nlam:nlam + nlam]
        (Gpaa, Gpav, Gpva, Gpvv) = self.om.case.d2Sbus_dV2(self._Ybus, V, lamP)
        (Gqaa, Gqav, Gqva, Gqvv) = self.om.case.d2Sbus_dV2(self._Ybus, V, lamQ)
        d2G = vstack([
         hstack([
          vstack([hstack([Gpaa, Gpav]),
           hstack([Gpva, Gpvv])]).real + vstack([hstack([Gqaa, Gqav]),
           hstack([Gqva, Gqvv])]).imag,
          csr_matrix((2 * self._nb, nxtra))]),
         hstack([
          csr_matrix((nxtra, 2 * self._nb)),
          csr_matrix((nxtra, nxtra))])], 'csr')
        nmu = len(lmbda['ineqnonlin']) / 2
        muF = lmbda['ineqnonlin'][:nmu]
        muT = lmbda['ineqnonlin'][nmu:nmu + nmu]
        if self.flow_lim == 'I':
            (dIf_dVa, dIf_dVm, dIt_dVa, dIt_dVm, If, It) = self.om.case.dIbr_dV(self._Yf, self._Yt, V)
            (Hfaa, Hfav, Hfva, Hfvv) = self.om.case.d2AIbr_dV2(dIf_dVa, dIf_dVm, If, self._Yf, V, muF)
            (Htaa, Htav, Htva, Htvv) = self.om.case.d2AIbr_dV2(dIt_dVa, dIt_dVm, It, self._Yt, V, muT)
        else:
            f = [ e.from_bus._i for e in self._ln ]
            t = [ e.to_bus._i for e in self._ln ]
            Cf = csr_matrix((ones(self._nl), (range(self._nl), f)), (self._nl, self._nb))
            Ct = csr_matrix((ones(self._nl), (range(self._nl), t)), (self._nl, self._nb))
            (dSf_dVa, dSf_dVm, dSt_dVa, dSt_dVm, Sf, St) = self.om.case.dSbr_dV(self._Yf, self._Yt, V)
            if self.flow_lim == PFLOW:
                (Hfaa, Hfav, Hfva, Hfvv) = self.om.case.d2ASbr_dV2(dSf_dVa.real(), dSf_dVm.real(), Sf.real(), Cf, self._Yf, V, muF)
                (Htaa, Htav, Htva, Htvv) = self.om.case.d2ASbr_dV2(dSt_dVa.real(), dSt_dVm.real(), St.real(), Ct, self._Yt, V, muT)
            elif self.flow_lim == SFLOW:
                (Hfaa, Hfav, Hfva, Hfvv) = self.om.case.d2ASbr_dV2(dSf_dVa, dSf_dVm, Sf, Cf, self._Yf, V, muF)
                (Htaa, Htav, Htva, Htvv) = self.om.case.d2ASbr_dV2(dSt_dVa, dSt_dVm, St, Ct, self._Yt, V, muT)
            else:
                raise ValueError
        d2H = vstack([
         hstack([
          vstack([hstack([Hfaa, Hfav]),
           hstack([Hfva, Hfvv])]) + vstack([hstack([Htaa, Htav]),
           hstack([Htva, Htvv])]),
          csr_matrix((2 * self._nb, nxtra))]),
         hstack([
          csr_matrix((nxtra, 2 * self._nb)),
          csr_matrix((nxtra, nxtra))])], 'csr')
        return d2f + d2G + d2H

    def _update_solution_data(self, s):
        """ Returns the voltage angle and generator set-point vectors.
        """
        x = s['x']
        Va = x[self._Va.i1:self._Va.iN + 1]
        Vm = x[self._Vm.i1:self._Vm.iN + 1]
        Pg = x[self._Pg.i1:self._Pg.iN + 1]
        Qg = x[self._Qg.i1:self._Qg.iN + 1]
        return (
         Va, Vm, Pg, Qg)

    def _update_case(self, bs, ln, gn, base_mva, Yf, Yt, Va, Vm, Pg, Qg, lmbda):
        """ Calculates the result attribute values.
        """
        V = Vm * exp(complex(0.0, 1.0) * Va)
        Vm_var = self._Vm
        Pmis = self.om.get_nln_constraint('Pmis')
        Qmis = self.om.get_nln_constraint('Qmis')
        Pg_var = self._Pg
        Qg_var = self._Qg
        lower = lmbda['lower']
        upper = lmbda['upper']
        ineqnonlin = lmbda['ineqnonlin']
        eqnonlin = lmbda['eqnonlin']
        nl2 = len([ i for (i, l) in enumerate(ln) if 0.0 < l.rate_a < 10000000000.0 ])
        for (i, bus) in enumerate(bs):
            bus.v_angle = Va[i] * 180.0 / pi
            bus.v_magnitude = Vm[i]
            bus.p_lmbda = eqnonlin[Pmis.i1:Pmis.iN + 1][i] / base_mva
            bus.q_lmbda = eqnonlin[Qmis.i1:Qmis.iN + 1][i] / base_mva
            bus.mu_vmax = upper[Vm_var.i1:Vm_var.iN + 1][i]
            bus.mu_vmin = lower[Vm_var.i1:Vm_var.iN + 1][i]

        for (l, branch) in enumerate(ln):
            Sf = V[branch.from_bus._i] * conj(Yf[l, :] * V) * base_mva
            St = V[branch.to_bus._i] * conj(Yt[l, :] * V) * base_mva
            branch.p_from = Sf.real[0]
            branch.q_from = Sf.imag[0]
            branch.p_to = St.real[0]
            branch.q_to = St.imag[0]
            if 0.0 < branch.rate_a < 10000000000.0:
                branch.mu_s_from = 2 * ineqnonlin[:nl2][l] * branch.rate_a / base_mva / base_mva
                branch.mu_s_to = 2 * ineqnonlin[nl2:2 * nl2][l] * branch.rate_a / base_mva / base_mva

        for (k, generator) in enumerate(gn):
            generator.p = Pg[k] * base_mva
            generator.q = Qg[k] * base_mva
            generator.v_magnitude = generator.bus.v_magnitude
            generator.mu_pmax = upper[Pg_var.i1:Pg_var.iN + 1][k] / base_mva
            generator.mu_pmin = lower[Pg_var.i1:Pg_var.iN + 1][k] / base_mva
            generator.mu_qmax = upper[Qg_var.i1:Qg_var.iN + 1][k] / base_mva
            generator.mu_qmin = lower[Qg_var.i1:Qg_var.iN + 1][k] / base_mva