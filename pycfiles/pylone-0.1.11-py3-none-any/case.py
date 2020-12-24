# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pylon\case.py
# Compiled at: 2010-12-26 13:36:33
__doc__ = ' Defines a bus-branch power system model.\n'
import logging, copy
from numpy import array, angle, pi, exp, ones, r_, complex64, conj, int32
from scipy.sparse import csc_matrix, csr_matrix
from util import _Named, _Serializable
PV = 'PV'
PQ = 'PQ'
REFERENCE = 'ref'
ISOLATED = 'isolated'
LINE = 'line'
TRANSFORMER = 'transformer'
logger = logging.getLogger(__name__)

class Bus(_Named):
    """ Defines a power system busbar.
    """

    def __init__(self, name=None, type=PQ, v_base=100.0, v_magnitude=1.0, v_angle=0.0, v_max=1.1, v_min=0.9, p_demand=0.0, q_demand=0.0, g_shunt=0.0, b_shunt=0.0, position=None):
        self.name = name
        self.type = type
        self.v_base = v_base
        self.v_magnitude = v_magnitude
        self.v_angle = v_angle
        self.v_max = v_max
        self.v_min = v_min
        self.p_demand = p_demand
        self.q_demand = q_demand
        self.g_shunt = g_shunt
        self.b_shunt = b_shunt
        self.area = 1
        self.zone = 1
        self.p_lmbda = 0.0
        self.q_lmbda = 0.0
        self.mu_vmin = 0.0
        self.mu_vmax = 0.0
        self._i = 0

    def reset(self):
        """ Resets the readonly variables.
        """
        self.p_lmbda = 0.0
        self.q_lmbda = 0.0
        self.mu_vmin = 0.0
        self.mu_vmax = 0.0


class Branch(_Named):
    """ Branches are modelled as a medium length transmission line (pi-model)
    in series with a regulating transformer at the "from" end.
    """

    def __init__(self, from_bus, to_bus, name=None, online=True, r=0.0, x=0.0, b=0.0, rate_a=999.0, rate_b=999.0, rate_c=999.0, ratio=0.0, phase_shift=0.0, ang_min=-360.0, ang_max=360.0):
        self.from_bus = from_bus
        self.to_bus = to_bus
        self.name = name
        self.online = online
        self.r = r
        self.x = x
        self.b = b
        self.rate_a = rate_a
        self.rate_b = rate_b
        self.rate_c = rate_c
        self.ratio = ratio
        self.phase_shift = phase_shift
        self.ang_min = ang_min
        self.ang_max = ang_max
        self.p_from = 0.0
        self.p_to = 0.0
        self.q_from = 0.0
        self.q_to = 0.0
        self.mu_s_from = 0.0
        self.mu_s_to = 0.0
        self.mu_angmin = 0.0
        self.mu_angmax = 0.0
        self._i = 0

    def reset(self):
        """ Resets the readonly variables.
        """
        self.p_from = 0.0
        self.p_to = 0.0
        self.q_from = 0.0
        self.q_to = 0.0
        self.mu_s_from = 0.0
        self.mu_s_to = 0.0
        self.mu_angmin = 0.0
        self.mu_angmax = 0.0


class Case(_Named, _Serializable):
    """ Defines an electric power system model as a graph of busbars connected
    by branches.
    """

    def __init__(self, name=None, base_mva=100.0, buses=None, branches=None, generators=None):
        self.name = name
        self.base_mva = base_mva
        self.buses = buses if buses is not None else []
        self.branches = branches if branches is not None else []
        self.generators = generators if generators is not None else []
        return

    @property
    def connected_buses(self):
        """ Returns a list of buses that are connected to one or more branches
        or the first bus in a branchless system.
        """
        return [ bus for bus in self.buses if bus.type != ISOLATED ]

    @property
    def online_generators(self):
        """ Returns all in-service generators connected to non-isolated buses.
        """
        return [ g for g in self.generators if g.online ]

    @property
    def online_branches(self):
        """ Returns all in-service branches connected to non-isolated buses.
        """
        return [ branch for branch in self.branches if branch.online ]

    def getSbus(self, buses=None):
        """ Returns the net complex bus power injection vector in p.u.
        """
        bs = self.buses if buses is None else buses
        s = array([ self.s_surplus(v) / self.base_mva for v in bs ])
        return s

    Sbus = property(getSbus)

    def sort_generators(self):
        """ Reorders the list of generators according to bus index.
        """
        self.generators.sort(key=lambda gn: gn.bus._i)

    def index_buses(self, buses=None, start=0):
        """ Updates the indices of all buses.

        @param start: Starting index, typically 0 or 1.
        @type start: int
        """
        bs = self.connected_buses if buses is None else buses
        for (i, b) in enumerate(bs):
            b._i = start + i

        return

    def index_branches(self, branches=None, start=0):
        """ Updates the indices of all branches.

        @param start: Starting index, typically 0 or 1.
        @type start: int
        """
        ln = self.online_branches if branches is None else branches
        for (i, l) in enumerate(ln):
            l._i = start + i

        return

    def s_supply(self, bus):
        """ Returns the total complex power generation capacity.
        """
        Sg = array([ complex(g.p, g.q) for g in self.generators if g.bus == bus if not g.is_load
                   ], dtype=complex64)
        if len(Sg):
            return sum(Sg)
        else:
            return complex(0.0, 0.0)

    def s_demand(self, bus):
        """ Returns the total complex power demand.
        """
        Svl = array([ complex(g.p, g.q) for g in self.generators if g.bus == bus if g.is_load
                    ], dtype=complex64)
        Sd = complex(bus.p_demand, bus.q_demand)
        return -sum(Svl) + Sd

    def s_surplus(self, bus):
        """ Return the difference between supply and demand.
        """
        return self.s_supply(bus) - self.s_demand(bus)

    def getYbus(self, buses=None, branches=None):
        """ Based on makeYbus.m from MATPOWER by Ray Zimmerman, developed at
        PSERC Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more
        information.

        @rtype: tuple
        @return: A triple consisting of the bus admittance matrix (i.e. for all
        buses) and the matrices Yf and Yt which, when multiplied by a complex
        voltage vector, yield the vector currents injected into each line from
        the "from" and "to" buses respectively of each line.
        """
        buses = self.buses if buses is None else buses
        branches = self.branches if branches is None else branches
        nb = len(buses)
        nl = len(branches)
        ib = array(range(nb), dtype=int32)
        il = array(range(nl), dtype=int32)
        online = array([ e.online for e in branches ])
        r = array([ e.r for e in branches ])
        x = array([ e.x for e in branches ])
        Ys = online / (r + complex(0.0, 1.0) * x)
        b = array([ e.b for e in branches ])
        Bc = online * b
        tap = ones(nl)
        i_trx = array([ i for (i, e) in enumerate(branches) if e.ratio != 0.0 ], dtype=int32)
        ratio = array([ e.ratio for e in branches ])
        if len(i_trx) > 0:
            tap[i_trx] = ratio[i_trx]
        shift = array([ e.phase_shift * pi / 180.0 for e in branches ])
        tap = tap * exp(complex(0.0, 1.0) * shift)
        Ytt = Ys + complex(0.0, 1.0) * Bc / 2.0
        Yff = Ytt / (tap * conj(tap))
        Yft = -Ys / conj(tap)
        Ytf = -Ys / tap
        g_shunt = array([ v.g_shunt for v in buses ])
        b_shunt = array([ v.b_shunt for v in buses ])
        Ysh = (g_shunt + complex(0.0, 1.0) * b_shunt) / self.base_mva
        f = [ e.from_bus._i for e in branches ]
        t = [ e.to_bus._i for e in branches ]
        Cf = csc_matrix((ones(nl), (il, f)), shape=(nl, nb))
        Ct = csc_matrix((ones(nl), (il, t)), shape=(nl, nb))
        i = r_[(il, il)]
        j = r_[(f, t)]
        Yf = csc_matrix((r_[(Yff, Yft)], (i, j)), (nl, nb))
        Yt = csc_matrix((r_[(Ytf, Ytt)], (i, j)), (nl, nb))
        Ysh_diag = csc_matrix((Ysh, (ib, ib)), shape=(nb, nb))
        Ybus = Cf.T * Yf + Ct.T * Yt + Ysh_diag
        assert Ybus.shape == (nb, nb)
        return (
         Ybus, Yf, Yt)

    Y = property(getYbus)

    def makeB(self, buses=None, branches=None, method='XB'):
        """ Based on makeB.m from MATPOWER by Ray Zimmerman, developed at
        PSERC Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more
        information.

        @param method: Specify "XB" or "BX" method.
        @type method: string

        @rtype: tuple
        @return: Two matrices, B prime and B double prime, used in the fast
        decoupled power flow solver.
        """
        buses = self.connected_buses if buses is None else buses
        branches = self.online_branches if branches is None else branches
        B_buses = copy.deepcopy(buses)
        Bp_branches = copy.deepcopy(branches)
        Bpp_branches = copy.deepcopy(branches)
        for bus in B_buses:
            bus.b_shunt = 0.0

        for branch in Bp_branches:
            branch.b = 0.0
            branch.ratio = 1.0
            if method == 'XB':
                branch.r = 0.0

        (Yp, _, _) = self.getYbus(B_buses, Bp_branches)
        for branch in Bpp_branches:
            branch.phase_shift = 0.0
            if method == 'BX':
                branch.r = 0.0

        (Ypp, _, _) = self.getYbus(B_buses, Bpp_branches)
        del B_buses
        del Bp_branches
        return (
         -Yp.imag, -Ypp.imag)

    def makeBdc(self, buses=None, branches=None):
        """ The bus real power injections are related to bus voltage angles
        by::
                P = Bbus * Va + Pbusinj

        The real power flows at the from end the lines are related to the bus
        voltage angles by::

                Pf = Bf * Va + Pfinj

                | Pf |   | Bff  Bft |   | Vaf |   | Pfinj |
                |    | = |          | * |     | + |       |
                | Pt |   | Btf  Btt |   | Vat |   | Ptinj |

        Based on makeBdc.m from MATPOWER by Ray Zimmerman, developed at
        PSERC Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more
        information.

        @return: B matrices and phase shift injection vectors for DC power
                 flow.
        @rtype: tuple
        """
        buses = self.connected_buses if buses is None else buses
        branches = self.online_branches if branches is None else branches
        nb = len(buses)
        nl = len(branches)
        online = array([ br.online for br in branches ])
        b = online / array([ br.x for br in branches ])
        tap = ones(nl)
        for (i, branch) in enumerate(branches):
            if branch.ratio != 0.0:
                tap[i] = branch.ratio

        b = b / tap
        f = [ br.from_bus._i for br in branches ]
        t = [ br.to_bus._i for br in branches ]
        i = r_[(array(range(nl)), array(range(nl)))]
        one = ones(nl)
        Cft = csc_matrix((r_[(one, -one)], (i, r_[(f, t)])), shape=(nl, nb))
        Bf = csc_matrix((r_[(b, -b)], (i, r_[(f, t)])), (nl, nb))
        Bbus = Cft.T * Bf
        shift = array([ br.phase_shift * pi / 180.0 for br in branches ])
        Pfinj = b * shift
        Pbusinj = Cft.T * Pfinj
        return (
         Bbus, Bf, Pbusinj, Pfinj)

    Bdc = property(makeBdc)

    def dSbus_dV(self, Y, V):
        """ Based on dSbus_dV.m from MATPOWER by Ray Zimmerman, developed at
        PSERC Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more
        information.

        @return: The partial derivatives of power injection w.r.t. voltage
                 magnitude and voltage angle.
        @rtype: tuple
        """
        ib = range(len(V))
        I = Y * V
        diagV = csr_matrix((V, (ib, ib)))
        diagIbus = csr_matrix((I, (ib, ib)))
        diagVnorm = csr_matrix((V / abs(V), (ib, ib)))
        dS_dVm = diagV * conj(Y * diagVnorm) + conj(diagIbus) * diagVnorm
        dS_dVa = complex(0.0, 1.0) * diagV * conj(diagIbus - Y * diagV)
        return (
         dS_dVm, dS_dVa)

    def dIbr_dV(self, Yf, Yt, V):
        """ Based on dIbr_dV.m from MATPOWER by Ray Zimmerman, developed at
        PSERC Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more
        information.

        @return: The partial derivatives of branch currents w.r.t. voltage
                 magnitude and voltage angle.
        @rtype: tuple
        """
        i = range(len(V))
        Vnorm = V / abs(V)
        diagV = csr_matrix((V, (i, i)))
        diagVnorm = csr_matrix((Vnorm, (i, i)))
        dIf_dVa = Yf * complex(0.0, 1.0) * diagV
        dIf_dVm = Yf * diagVnorm
        dIt_dVa = Yt * complex(0.0, 1.0) * diagV
        dIt_dVm = Yt * diagVnorm
        If = Yf * V
        It = Yt * V
        return (
         dIf_dVa, dIf_dVm, dIt_dVa, dIt_dVm, If, It)

    def dSbr_dV(self, Yf, Yt, V, buses=None, branches=None):
        """ Based on dSbr_dV.m from MATPOWER by Ray Zimmerman, developed at
        PSERC Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more
        information.

        @return: The branch power flow vectors and the partial derivatives of
                 branch power flow w.r.t voltage magnitude and voltage angle.
        @rtype: tuple
        """
        buses = self.buses if buses is None else buses
        branches = self.branches if branches is None else branches
        nl = len(branches)
        nb = len(V)
        il = range(nl)
        ib = range(nb)
        f = [ l.from_bus._i for l in branches ]
        t = [ l.to_bus._i for l in branches ]
        If = Yf * V
        It = Yt * V
        Vnorm = V / abs(V)
        diagVf = csr_matrix((V[f], (il, il)))
        diagIf = csr_matrix((If, (il, il)))
        diagVt = csr_matrix((V[t], (il, il)))
        diagIt = csr_matrix((It, (il, il)))
        diagV = csr_matrix((V, (ib, ib)))
        diagVnorm = csr_matrix((Vnorm, (ib, ib)))
        shape = (
         nl, nb)
        dSf_dVa = complex(0.0, 1.0) * (conj(diagIf) * csr_matrix((V[f], (il, f)), shape) - diagVf * conj(Yf * diagV))
        dSt_dVa = complex(0.0, 1.0) * (conj(diagIt) * csr_matrix((V[t], (il, t)), shape) - diagVt * conj(Yt * diagV))
        dSf_dVm = diagVf * conj(Yf * diagVnorm) + conj(diagIf) * csr_matrix((Vnorm[f], (il, f)), shape)
        dSt_dVm = diagVt * conj(Yt * diagVnorm) + conj(diagIt) * csr_matrix((Vnorm[t], (il, t)), shape)
        Sf = V[f] * conj(If)
        St = V[t] * conj(It)
        return (
         dSf_dVa, dSf_dVm, dSt_dVa, dSt_dVm, Sf, St)

    def dAbr_dV(self, dSf_dVa, dSf_dVm, dSt_dVa, dSt_dVm, Sf, St):
        """ Based on dAbr_dV.m from MATPOWER by Ray Zimmerman, developed at
        PSERC Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more
        information.

        @rtype: tuple
        @return: The partial derivatives of the squared flow magnitudes w.r.t
                 voltage magnitude and voltage angle given the flows and flow
                 sensitivities. Flows could be complex current or complex or
                 real power.
        """
        il = range(len(Sf))
        dAf_dPf = csr_matrix((2 * Sf.real, (il, il)))
        dAf_dQf = csr_matrix((2 * Sf.imag, (il, il)))
        dAt_dPt = csr_matrix((2 * St.real, (il, il)))
        dAt_dQt = csr_matrix((2 * St.imag, (il, il)))
        dAf_dVa = dAf_dPf * dSf_dVa.real + dAf_dQf * dSf_dVa.imag
        dAt_dVa = dAt_dPt * dSt_dVa.real + dAt_dQt * dSt_dVa.imag
        dAf_dVm = dAf_dPf * dSf_dVm.real + dAf_dQf * dSf_dVm.imag
        dAt_dVm = dAt_dPt * dSt_dVm.real + dAt_dQt * dSt_dVm.imag
        return (
         dAf_dVa, dAf_dVm, dAt_dVa, dAt_dVm)

    def d2Sbus_dV2(self, Ybus, V, lam):
        """ Based on d2Sbus_dV2.m from MATPOWER by Ray Zimmerman, developed
        at PSERC Cornell. See U{http://www.pserc.cornell.edu/matpower/} for
        more information.

        @rtype: tuple
        @return: The 2nd derivatives of power injection w.r.t. voltage.
        """
        nb = len(V)
        ib = range(nb)
        Ibus = Ybus * V
        diaglam = csr_matrix((lam, (ib, ib)))
        diagV = csr_matrix((V, (ib, ib)))
        A = csr_matrix((lam * V, (ib, ib)))
        B = Ybus * diagV
        C = A * conj(B)
        D = Ybus.H * diagV
        E = diagV.conj() * (D * diaglam - csr_matrix((D * lam, (ib, ib))))
        F = C - A * csr_matrix((conj(Ibus), (ib, ib)))
        G = csr_matrix((ones(nb) / abs(V), (ib, ib)))
        Gaa = E + F
        Gva = complex(0.0, 1.0) * G * (E - F)
        Gav = Gva.T
        Gvv = G * (C + C.T) * G
        return (
         Gaa, Gav, Gva, Gvv)

    def d2Ibr_dV2(self, Ybr, V, lam):
        """ Based on d2Ibr_dV2.m from MATPOWER by Ray Zimmerman, developed
        at PSERC Cornell. See U{http://www.pserc.cornell.edu/matpower/} for
        more information.

        @rtype: tuple
        @return: The 2nd derivatives of complex branch current w.r.t. voltage.
        """
        nb = len(V)
        ib = range(nb)
        diaginvVm = csr_matrix((ones(nb) / abs(V), (ib, ib)))
        Haa = csr_matrix((-(Ybr.T * lam) / V, (ib, ib)))
        Hva = complex(0.0, -1.0) * Haa * diaginvVm
        Hav = Hva
        Hvv = csr_matrix((nb, nb))
        return (
         Haa, Hav, Hva, Hvv)

    def d2Sbr_dV2(self, Cbr, Ybr, V, lam):
        """ Based on d2Sbr_dV2.m from MATPOWER by Ray Zimmerman, developed
        at PSERC Cornell. See U{http://www.pserc.cornell.edu/matpower/} for
        more information.

        @rtype: tuple
        @return: The 2nd derivatives of complex power flow w.r.t. voltage.
        """
        nb = len(V)
        nl = len(lam)
        ib = range(nb)
        il = range(nl)
        diaglam = csr_matrix((lam, (il, il)))
        diagV = csr_matrix((V, (ib, ib)))
        A = Ybr.H * diaglam * Cbr
        B = conj(diagV) * A * diagV
        D = csr_matrix((A * V * conj(V), (ib, ib)))
        E = csr_matrix((A.T * conj(V) * V, (ib, ib)))
        F = B + B.T
        G = csr_matrix((ones(nb) / abs(V), (ib, ib)))
        Haa = F - D - E
        Hva = complex(0.0, 1.0) * G * (B - B.T - D + E)
        Hav = Hva.T
        Hvv = G * F * G
        return (
         Haa, Hav, Hva, Hvv)

    def d2ASbr_dV2(self, dSbr_dVa, dSbr_dVm, Sbr, Cbr, Ybr, V, lam):
        """ Based on d2ASbr_dV2.m from MATPOWER by Ray Zimmerman, developed
        at PSERC Cornell. See U{http://www.pserc.cornell.edu/matpower/} for
        more information.

        @rtype: tuple
        @return: The 2nd derivatives of |complex power flow|**2 w.r.t. V.
        """
        il = range(len(lam))
        diaglam = csr_matrix((lam, (il, il)))
        diagSbr_conj = csr_matrix((Sbr.conj(), (il, il)))
        (Saa, Sav, Sva, Svv) = self.d2Sbr_dV2(Cbr, Ybr, V, diagSbr_conj * lam)
        Haa = 2 * (Saa + dSbr_dVa.T * diaglam * dSbr_dVa.conj()).real
        Hva = 2 * (Sva + dSbr_dVm.T * diaglam * dSbr_dVa.conj()).real
        Hav = 2 * (Sav + dSbr_dVa.T * diaglam * dSbr_dVm.conj()).real
        Hvv = 2 * (Svv + dSbr_dVm.T * diaglam * dSbr_dVm.conj()).real
        return (
         Haa, Hav, Hva, Hvv)

    def d2AIbr_dV2(self, dIbr_dVa, dIbr_dVm, Ibr, Ybr, V, lam):
        """ Based on d2AIbr_dV2.m from MATPOWER by Ray Zimmerman, developed
        at PSERC Cornell. See U{http://www.pserc.cornell.edu/matpower/} for
        more information.

        @rtype: tuple
        @return: The 2nd derivatives of |complex current|**2 w.r.t. V.
        """
        il = range(len(lam))
        diaglam = csr_matrix((lam, (il, il)))
        diagIbr_conj = csr_matrix((conj(Ibr), (il, il)))
        (Iaa, Iav, Iva, Ivv) = self.d2Ibr_dV2(Ybr, V, diagIbr_conj * lam)
        Haa = 2 * (Iaa + dIbr_dVa.T * diaglam * dIbr_dVa.conj()).real
        Hva = 2 * (Iva + dIbr_dVm.T * diaglam * dIbr_dVa.conj()).real
        Hav = 2 * (Iav + dIbr_dVa.T * diaglam * dIbr_dVm.conj()).real
        Hvv = 2 * (Ivv + dIbr_dVm.T * diaglam * dIbr_dVm.conj()).real
        return (
         Haa, Hav, Hva, Hvv)

    def pf_solution(self, Ybus, Yf, Yt, V):
        """ Based on pfsoln.m from MATPOWER by Ray Zimmerman, developed
        at PSERC Cornell. See U{http://www.pserc.cornell.edu/matpower/} for
        more information.

        Updates buses, generators and branches to match a power flow solution.
        """
        buses = self.connected_buses
        branches = self.online_branches
        generators = self.online_generators
        self.reset()
        self.index_buses()
        self.index_branches()
        Va = angle(V)
        Vm = abs(V)
        for (i, b) in enumerate(buses):
            b.v_angle = Va[i] * 180.0 / pi
            b.v_magnitude = Vm[i]

        refgen = [ i for (i, g) in enumerate(generators) if g.bus.type == REFERENCE
                 ]
        Sg = V * conj(Ybus * V)
        for g in generators:
            g.q = Sg.imag[g.bus._i] * self.base_mva + g.bus.q_demand

        if generators:
            pass
        for i in refgen:
            g = generators[i]
            g.p = Sg.real[i] * self.base_mva + g.bus.p_demand

        if len(refgen) > 1:
            pass
        br = [ l._i for l in branches ]
        f_idx = [ l.from_bus._i for l in branches ]
        t_idx = [ l.to_bus._i for l in branches ]
        Sf = V[f_idx] * conj(Yf[br, :] * V) * self.base_mva
        St = V[t_idx] * conj(Yt[br, :] * V) * self.base_mva
        for (i, l) in enumerate(branches):
            l.p_from = Sf[i].real
            l.q_from = Sf[i].imag
            l.p_to = St[i].real
            l.q_to = St[i].imag

    def reset(self):
        """ Resets the readonly variables for all of the case components.
        """
        for bus in self.buses:
            bus.reset()

        for branch in self.branches:
            branch.reset()

        for generator in self.generators:
            generator.reset()

    def save_matpower(self, fd):
        """ Serialize the case as a MATPOWER data file.
        """
        from pylon.io import MATPOWERWriter
        MATPOWERWriter(self).write(fd)

    @classmethod
    def load_matpower(cls, fd):
        """ Returns a case from the given MATPOWER file object.
        """
        from pylon.io import MATPOWERReader
        return MATPOWERReader().read(fd)

    def save_psse(self, fd):
        """ Serialize the case as a PSS/E data file.
        """
        from pylon.io import PSSEWriter
        return PSSEWriter(self).write(fd)

    @classmethod
    def load_psse(cls, fd):
        """ Returns a case from the given PSS/E file object.
        """
        from pylon.io import PSSEReader
        return PSSEReader().read(fd)

    def save_psat(self, fd):
        raise NotImplementedError

    @classmethod
    def load_psat(cls, fd):
        """ Returns a case object from the given PSAT data file.
        """
        from pylon.io.psat import PSATReader
        return PSATReader().read(fd)

    def save_rst(self, fd):
        """ Save a reStructuredText representation of the case.
        """
        from pylon.io import ReSTWriter
        ReSTWriter(self).write(fd)

    def save_csv(self, fd):
        """ Saves the case as a series of Comma-Separated Values.
        """
        from pylon.io.excel import CSVWriter
        CSVWriter(self).write(fd)

    def save_excel(self, fd):
        """ Saves the case as an Excel spreadsheet.
        """
        from pylon.io.excel import ExcelWriter
        ExcelWriter(self).write(fd)

    def save_dot(self, fd):
        """ Saves a representation of the case in the Graphviz DOT language.
        """
        from pylon.io import DotWriter
        DotWriter(self).write(fd)