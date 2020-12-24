# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pylon\test\opf_test.py
# Compiled at: 2010-12-26 13:36:33
__doc__ = ' Defines a test case for AC power flow.\n'
import unittest
from os.path import join, dirname
from scipy.io.mmio import mmread
from pylon import Case, OPF
from pylon.opf import DCOPFSolver, PIPSSolver
from pylon.util import mfeq2, mfeq1
DATA_DIR = join(dirname(__file__), 'data')

class DCOPFTest(unittest.TestCase):
    """ Defines a test case for DC OPF.
    """

    def __init__(self, methodName='runTest'):
        super(DCOPFTest, self).__init__(methodName)
        self.case_name = 'case6ww'
        self.case = None
        self.opf = None
        return

    def setUp(self):
        """ The test runner will execute this method prior to each test.
        """
        self.case = Case.load(join(DATA_DIR, self.case_name, self.case_name + '.pkl'))
        self.opf = OPF(self.case, dc=True)

    def testVa(self):
        """ Test voltage angle variable.
        """
        msg = self.case_name
        (bs, _, _) = self.opf._remove_isolated(self.case)
        (_, refs) = self.opf._ref_check(self.case)
        Va = self.opf._get_voltage_angle_var(refs, bs)
        mpVa0 = mmread(join(DATA_DIR, self.case_name, 'opf', 'Va0.mtx'))
        mpVal = mmread(join(DATA_DIR, self.case_name, 'opf', 'Val.mtx'))
        mpVau = mmread(join(DATA_DIR, self.case_name, 'opf', 'Vau.mtx'))
        self.assertTrue(mfeq1(Va.v0, mpVa0.flatten()), msg)
        self.assertTrue(mfeq1(Va.vl, mpVal.flatten()), msg)
        self.assertTrue(mfeq1(Va.vu, mpVau.flatten()), msg)

    def testVm(self):
        """ Test voltage magnitude variable.
        """
        (bs, _, gn) = self.opf._remove_isolated(self.case)
        Vm = self.opf._get_voltage_magnitude_var(bs, gn)
        mpVm0 = mmread(join(DATA_DIR, self.case_name, 'opf', 'Vm0.mtx'))
        self.assertTrue(mfeq1(Vm.v0, mpVm0.flatten()), self.case_name)

    def testPg(self):
        """ Test active power variable.
        """
        msg = self.case_name
        self.case.sort_generators()
        (_, _, gn) = self.opf._remove_isolated(self.case)
        Pg = self.opf._get_pgen_var(gn, self.case.base_mva)
        mpPg0 = mmread(join(DATA_DIR, self.case_name, 'opf', 'Pg0.mtx'))
        mpPmin = mmread(join(DATA_DIR, self.case_name, 'opf', 'Pmin.mtx'))
        mpPmax = mmread(join(DATA_DIR, self.case_name, 'opf', 'Pmax.mtx'))
        self.assertTrue(mfeq1(Pg.v0, mpPg0.flatten()), msg)
        self.assertTrue(mfeq1(Pg.vl, mpPmin.flatten()), msg)
        self.assertTrue(mfeq1(Pg.vu, mpPmax.flatten()), msg)

    def testQg(self):
        """ Test reactive power variable.
        """
        msg = self.case_name
        self.case.sort_generators()
        (_, _, gn) = self.opf._remove_isolated(self.case)
        Qg = self.opf._get_qgen_var(gn, self.case.base_mva)
        mpQg0 = mmread(join(DATA_DIR, self.case_name, 'opf', 'Qg0.mtx'))
        mpQmin = mmread(join(DATA_DIR, self.case_name, 'opf', 'Qmin.mtx'))
        mpQmax = mmread(join(DATA_DIR, self.case_name, 'opf', 'Qmax.mtx'))
        self.assertTrue(mfeq1(Qg.v0, mpQg0.flatten()), msg)
        self.assertTrue(mfeq1(Qg.vl, mpQmin.flatten()), msg)
        self.assertTrue(mfeq1(Qg.vu, mpQmax.flatten()), msg)

    def testPmis(self):
        """ Test active power mismatch constraints.
        """
        msg = self.case_name
        case = self.case
        case.sort_generators()
        (B, _, Pbusinj, _) = case.Bdc
        (bs, _, gn) = self.opf._remove_isolated(case)
        Pmis = self.opf._power_mismatch_dc(bs, gn, B, Pbusinj, case.base_mva)
        mpAmis = mmread(join(DATA_DIR, self.case_name, 'opf', 'Amis.mtx'))
        mpbmis = mmread(join(DATA_DIR, self.case_name, 'opf', 'bmis.mtx'))
        self.assertTrue(mfeq2(Pmis.A, mpAmis.tocsr(), 1e-12), msg)
        self.assertTrue(mfeq1(Pmis.l, mpbmis.flatten()), msg)
        self.assertTrue(mfeq1(Pmis.u, mpbmis.flatten()), msg)

    def testPfPt(self):
        """ Test branch flow limit constraints.
        """
        msg = self.case_name
        (_, ln, _) = self.opf._remove_isolated(self.case)
        (_, Bf, _, Pfinj) = self.case.Bdc
        (Pf, Pt) = self.opf._branch_flow_dc(ln, Bf, Pfinj, self.case.base_mva)
        lpf = mmread(join(DATA_DIR, self.case_name, 'opf', 'lpf.mtx'))
        upf = mmread(join(DATA_DIR, self.case_name, 'opf', 'upf.mtx'))
        upt = mmread(join(DATA_DIR, self.case_name, 'opf', 'upt.mtx'))
        self.assertTrue(mfeq1(Pf.l, lpf.flatten()), msg)
        self.assertTrue(mfeq1(Pf.u, upf.flatten()), msg)
        self.assertTrue(mfeq1(Pt.l, lpf.flatten()), msg)
        self.assertTrue(mfeq1(Pt.u, upt.flatten()), msg)

    def testVang(self):
        """ Test voltage angle difference limit constraint.
        """
        msg = self.case_name
        self.opf.ignore_ang_lim = False
        (bs, ln, _) = self.opf._remove_isolated(self.case)
        ang = self.opf._voltage_angle_diff_limit(bs, ln)
        if ang.A.shape[0] != 0:
            Aang = mmread(join(DATA_DIR, self.case_name, 'opf', 'Aang.mtx'))
        else:
            Aang = None
        lang = mmread(join(DATA_DIR, self.case_name, 'opf', 'lang.mtx'))
        uang = mmread(join(DATA_DIR, self.case_name, 'opf', 'uang.mtx'))
        if Aang is not None:
            self.assertTrue(mfeq2(ang.A, Aang.tocsr()), msg)
        self.assertTrue(mfeq1(ang.l, lang.flatten()), msg)
        self.assertTrue(mfeq1(ang.u, uang.flatten()), msg)
        return

    def testVLConstPF(self):
        """ Test dispatchable load, constant power factor constraints.
        """
        msg = self.case_name
        (_, _, gn) = self.opf._remove_isolated(self.case)
        vl = self.opf._const_pf_constraints(gn, self.case.base_mva)
        if vl.A.shape[0] != 0:
            Avl = mmread(join(DATA_DIR, self.case_name, 'opf', 'Avl.mtx'))
            self.assertTrue(mfeq2(vl.A, Avl.tocsr()), msg)
        lvl = mmread(join(DATA_DIR, self.case_name, 'opf', 'lang.mtx'))
        self.assertTrue(mfeq1(vl.l, lvl.flatten()), msg)
        uvl = mmread(join(DATA_DIR, self.case_name, 'opf', 'uang.mtx'))
        self.assertTrue(mfeq1(vl.u, uvl.flatten()), msg)

    def testAy(self):
        """ Test basin constraints for piece-wise linear gen cost variables.
        """
        msg = self.case_name
        self.case.sort_generators()
        (_, _, gn) = self.opf._remove_isolated(self.case)
        (_, ycon) = self.opf._pwl_gen_costs(gn, self.case.base_mva)
        if ycon is not None:
            Ay = mmread(join(DATA_DIR, self.case_name, 'opf', 'Ay_DC.mtx'))
            by = mmread(join(DATA_DIR, self.case_name, 'opf', 'by_DC.mtx'))
            self.assertTrue(mfeq2(ycon.A, Ay.tocsr()), msg)
            self.assertTrue(mfeq1(ycon.u, by.flatten()), msg)
        return


class DCOPFCase24RTSTest(DCOPFTest):

    def __init__(self, methodName='runTest'):
        super(DCOPFCase24RTSTest, self).__init__(methodName)
        self.case_name = 'case24_ieee_rts'


class DCOPFCaseIEEE30Test(DCOPFTest):

    def __init__(self, methodName='runTest'):
        super(DCOPFCaseIEEE30Test, self).__init__(methodName)
        self.case_name = 'case_ieee30'


class DCOPFCase30PWLTest(DCOPFTest):

    def __init__(self, methodName='runTest'):
        super(DCOPFCase30PWLTest, self).__init__(methodName)
        self.case_name = 'case30pwl'


class DCOPFSolverTest(unittest.TestCase):
    """ Defines a test case for the DC OPF solver.
    """

    def __init__(self, methodName='runTest'):
        super(DCOPFSolverTest, self).__init__(methodName)
        self.case_name = 'case6ww'
        self.case = None
        self.opf = None
        self.om = None
        self.solver = None
        return

    def setUp(self):
        """ The test runner will execute this method prior to each test.
        """
        self.case = Case.load(join(DATA_DIR, self.case_name, self.case_name + '.pkl'))
        self.case.sort_generators()
        self.opf = OPF(self.case, dc=True)
        self.om = self.opf._construct_opf_model(self.case)
        self.solver = DCOPFSolver(self.om)

    def test_constraints(self):
        """ Test equality and inequality constraints.
        """
        (AA, ll, uu) = self.solver._linear_constraints(self.om)
        mpA = mmread(join(DATA_DIR, self.case_name, 'opf', 'A_DC.mtx'))
        mpl = mmread(join(DATA_DIR, self.case_name, 'opf', 'l_DC.mtx'))
        mpu = mmread(join(DATA_DIR, self.case_name, 'opf', 'u_DC.mtx'))
        self.assertTrue(mfeq2(AA, mpA.tocsr()), self.case_name)
        self.assertTrue(mfeq1(ll, mpl.flatten()), self.case_name)
        self.assertTrue(mfeq1(uu, mpu.flatten()), self.case_name)

    def test_var_bounds(self):
        """ Test bounds on optimisation variables.
        """
        (_, xmin, xmax) = self.solver._var_bounds()
        mpxmin = mmread(join(DATA_DIR, self.case_name, 'opf', 'xmin_DC.mtx'))
        mpxmax = mmread(join(DATA_DIR, self.case_name, 'opf', 'xmax_DC.mtx'))
        self.assertTrue(mfeq1(xmin, mpxmin.flatten()), self.case_name)
        self.assertTrue(mfeq1(xmax, mpxmax.flatten()), self.case_name)

    def test_initial_point(self):
        """ Test selection of an initial interior point.
        """
        (b, l, g, _) = self.solver._unpack_model(self.om)
        (_, LB, UB) = self.solver._var_bounds()
        (_, _, _, _, _, ny, _) = self.solver._dimension_data(b, l, g)
        x0 = self.solver._initial_interior_point(b, g, LB, UB, ny)
        mpx0 = mmread(join(DATA_DIR, self.case_name, 'opf', 'x0_DC.mtx'))
        self.assertTrue(mfeq1(x0, mpx0.flatten(), 1e-09), self.case_name)

    def test_pwl_costs(self):
        """ Test piecewise linear costs.
        """
        msg = self.case_name
        (b, l, g, _) = self.solver._unpack_model(self.om)
        (_, ipwl, _, _, _, ny, nxyz) = self.solver._dimension_data(b, l, g)
        (Npwl, Hpwl, Cpwl, fparm_pwl, _) = self.solver._pwl_costs(ny, nxyz, ipwl)
        if Npwl is not None:
            mpNpwl = mmread(join(DATA_DIR, self.case_name, 'opf', 'Npwl.mtx'))
            mpHpwl = mmread(join(DATA_DIR, self.case_name, 'opf', 'Hpwl.mtx'))
            mpCpwl = mmread(join(DATA_DIR, self.case_name, 'opf', 'Cpwl.mtx'))
            mpfparm = mmread(join(DATA_DIR, self.case_name, 'opf', 'fparm_pwl.mtx'))
            self.assertTrue(mfeq2(Npwl, mpNpwl.tocsr()), msg)
            self.assertTrue(mfeq2(Hpwl.todense(), mpHpwl), msg)
            self.assertTrue(mfeq1(Cpwl, mpCpwl.flatten()), msg)
            self.assertTrue(mfeq1(fparm_pwl.flatten(), mpfparm.flatten()), msg)
        return

    def test_poly_costs(self):
        """ Test quadratic costs.
        """
        msg = self.case_name
        base_mva = self.om.case.base_mva
        (b, l, g, _) = self.solver._unpack_model(self.om)
        (ipol, _, _, _, _, _, nxyz) = self.solver._dimension_data(b, l, g)
        (Npol, Hpol, Cpol, fparm_pol, _, _) = self.solver._quadratic_costs(g, ipol, nxyz, base_mva)
        if Npol is not None:
            mpNpol = mmread(join(DATA_DIR, self.case_name, 'opf', 'Npol.mtx'))
            mpHpol = mmread(join(DATA_DIR, self.case_name, 'opf', 'Hpol.mtx'))
            mpCpol = mmread(join(DATA_DIR, self.case_name, 'opf', 'Cpol.mtx'))
            mpfparm = mmread(join(DATA_DIR, self.case_name, 'opf', 'fparm_pol.mtx'))
            self.assertTrue(mfeq2(Npol, mpNpol.tocsr()), msg)
            self.assertTrue(mfeq2(Hpol, mpHpol.tocsr()), msg)
            self.assertTrue(mfeq1(Cpol, mpCpol.flatten()), msg)
            self.assertTrue(mfeq2(fparm_pol, mpfparm), msg)
        return

    def test_combine_costs(self):
        """ Test combination of pwl and poly costs.
        """
        msg = self.case_name
        base_mva = self.om.case.base_mva
        (b, l, g, _) = self.solver._unpack_model(self.om)
        (ipol, ipwl, _, _, nw, ny, nxyz) = self.solver._dimension_data(b, l, g)
        (Npwl, Hpwl, Cpwl, fparm_pwl, any_pwl) = self.solver._pwl_costs(ny, nxyz, ipwl)
        (Npol, Hpol, Cpol, fparm_pol, _, npol) = self.solver._quadratic_costs(g, ipol, nxyz, base_mva)
        (NN, HHw, CCw, ffparm) = self.solver._combine_costs(Npwl, Hpwl, Cpwl, fparm_pwl, any_pwl, Npol, Hpol, Cpol, fparm_pol, npol, nw)
        mpNN = mmread(join(DATA_DIR, self.case_name, 'opf', 'NN.mtx'))
        mpHHw = mmread(join(DATA_DIR, self.case_name, 'opf', 'HHw.mtx'))
        mpCCw = mmread(join(DATA_DIR, self.case_name, 'opf', 'CCw.mtx'))
        mpffparm = mmread(join(DATA_DIR, self.case_name, 'opf', 'ffparm.mtx'))
        self.assertTrue(mfeq2(NN, mpNN.tocsr()), msg)
        self.assertTrue(mfeq2(HHw, mpHHw.tocsr()), msg)
        self.assertTrue(mfeq1(CCw, mpCCw.flatten()), msg)
        self.assertTrue(mfeq2(ffparm, mpffparm), msg)

    def test_coefficient_transformation(self):
        """ Test transformation of quadratic coefficients for w into
            coefficients for X.
        """
        msg = self.case_name
        base_mva = self.om.case.base_mva
        (b, l, g, _) = self.solver._unpack_model(self.om)
        (ipol, ipwl, _, _, nw, ny, nxyz) = self.solver._dimension_data(b, l, g)
        (Npwl, Hpwl, Cpwl, fparm_pwl, any_pwl) = self.solver._pwl_costs(ny, nxyz, ipwl)
        (Npol, Hpol, Cpol, fparm_pol, polycf, npol) = self.solver._quadratic_costs(g, ipol, nxyz, base_mva)
        (NN, HHw, CCw, ffparm) = self.solver._combine_costs(Npwl, Hpwl, Cpwl, fparm_pwl, any_pwl, Npol, Hpol, Cpol, fparm_pol, npol, nw)
        (HH, CC, _) = self.solver._transform_coefficients(NN, HHw, CCw, ffparm, polycf, any_pwl, npol, nw)
        mpHH = mmread(join(DATA_DIR, self.case_name, 'opf', 'HH.mtx'))
        mpCC = mmread(join(DATA_DIR, self.case_name, 'opf', 'CC.mtx'))
        self.assertTrue(mfeq2(HH, mpHH.tocsr()), msg)
        self.assertTrue(mfeq1(CC, mpCC.flatten()), msg)

    def test_solution(self):
        """ Test DC OPF solution.
        """
        msg = self.case_name
        solution = self.solver.solve()
        lmbda = solution['lmbda']
        mpf = mmread(join(DATA_DIR, self.case_name, 'opf', 'f_DC.mtx'))
        mpx = mmread(join(DATA_DIR, self.case_name, 'opf', 'x_DC.mtx'))
        mpmu_l = mmread(join(DATA_DIR, self.case_name, 'opf', 'mu_l_DC.mtx'))
        mpmu_u = mmread(join(DATA_DIR, self.case_name, 'opf', 'mu_u_DC.mtx'))
        mpmuLB = mmread(join(DATA_DIR, self.case_name, 'opf', 'muLB_DC.mtx'))
        mpmuUB = mmread(join(DATA_DIR, self.case_name, 'opf', 'muUB_DC.mtx'))
        diff = 1e-09
        self.assertAlmostEqual(solution['f'], mpf[0], places=6)
        self.assertTrue(mfeq1(solution['x'], mpx.flatten(), diff), msg)
        self.assertTrue(mfeq1(lmbda['mu_l'], mpmu_l.flatten(), diff), msg)
        self.assertTrue(mfeq1(lmbda['mu_u'], mpmu_u.flatten(), diff), msg)
        self.assertTrue(mfeq1(lmbda['lower'], mpmuLB.flatten(), diff), msg)
        self.assertTrue(mfeq1(lmbda['upper'], mpmuUB.flatten(), diff), msg)

    def test_integrate_solution(self):
        """ Test integration of DC OPF solution.
        """
        self.solver.solve()
        bus = mmread(join(DATA_DIR, self.case_name, 'opf', 'Bus_DC.mtx'))
        gen = mmread(join(DATA_DIR, self.case_name, 'opf', 'Gen_DC.mtx'))
        branch = mmread(join(DATA_DIR, self.case_name, 'opf', 'Branch_DC.mtx'))
        pl = 2
        for (i, bs) in enumerate(self.case.buses):
            self.assertAlmostEqual(bs.v_magnitude, bus[(i, 7)], pl)
            self.assertAlmostEqual(bs.v_angle, bus[(i, 8)], pl)
            self.assertAlmostEqual(bs.p_lmbda, bus[(i, 13)], pl)
            self.assertAlmostEqual(bs.q_lmbda, bus[(i, 14)], pl)
            self.assertAlmostEqual(bs.mu_vmax, bus[(i, 15)], pl)
            self.assertAlmostEqual(bs.mu_vmin, bus[(i, 16)], pl)

        for (i, gn) in enumerate(self.case.generators):
            self.assertAlmostEqual(gn.p, gen[(i, 1)], pl)
            self.assertAlmostEqual(gn.q, gen[(i, 2)], pl)
            self.assertAlmostEqual(gn.v_magnitude, gen[(i, 5)], pl)
            self.assertAlmostEqual(gn.mu_pmax, gen[(i, 21)], pl)
            self.assertAlmostEqual(gn.mu_pmin, gen[(i, 22)], pl)
            self.assertAlmostEqual(gn.mu_qmax, gen[(i, 23)], pl)
            self.assertAlmostEqual(gn.mu_qmin, gen[(i, 24)], pl)

        for (i, ln) in enumerate(self.case.branches):
            self.assertAlmostEqual(ln.p_from, branch[(i, 13)], pl)
            self.assertAlmostEqual(ln.q_from, branch[(i, 14)], pl)
            self.assertAlmostEqual(ln.p_to, branch[(i, 15)], pl)
            self.assertAlmostEqual(ln.q_to, branch[(i, 16)], pl)
            self.assertAlmostEqual(ln.mu_s_from, branch[(i, 17)], pl)
            self.assertAlmostEqual(ln.mu_s_to, branch[(i, 18)], pl)
            self.assertAlmostEqual(ln.mu_angmin, branch[(i, 19)], pl)
            self.assertAlmostEqual(ln.mu_angmax, branch[(i, 20)], pl)


class DCOPFSolverCase24RTSTest(DCOPFSolverTest):

    def __init__(self, methodName='runTest'):
        super(DCOPFSolverCase24RTSTest, self).__init__(methodName)
        self.case_name = 'case24_ieee_rts'


class DCOPFSolverCaseIEEE30Test(DCOPFSolverTest):

    def __init__(self, methodName='runTest'):
        super(DCOPFSolverCaseIEEE30Test, self).__init__(methodName)
        self.case_name = 'case_ieee30'


class DCOPFSolverCase30PWLTest(DCOPFSolverTest):

    def __init__(self, methodName='runTest'):
        super(DCOPFSolverCase30PWLTest, self).__init__(methodName)
        self.case_name = 'case30pwl'


class PIPSSolverTest(unittest.TestCase):
    """ Defines a test case for the PIPS AC OPF solver.
    """

    def __init__(self, methodName='runTest'):
        super(PIPSSolverTest, self).__init__(methodName)
        self.case_name = 'case6ww'
        self.case = None
        self.opf = None
        self.om = None
        self.solver = None
        return

    def setUp(self):
        """ The test runner will execute this method prior to each test.
        """
        self.case = Case.load(join(DATA_DIR, self.case_name, self.case_name + '.pkl'))
        self.case.sort_generators()
        self.opf = OPF(self.case, dc=False)
        self.om = self.opf._construct_opf_model(self.case)
        self.solver = PIPSSolver(self.om)

    def test_constraints(self):
        """ Test equality and inequality constraints.
        """
        msg = self.case_name
        (AA, ll, uu) = self.solver._linear_constraints(self.om)
        if AA is not None:
            mpA = mmread(join(DATA_DIR, self.case_name, 'opf', 'A_AC.mtx'))
            mpl = mmread(join(DATA_DIR, self.case_name, 'opf', 'l_AC.mtx'))
            mpu = mmread(join(DATA_DIR, self.case_name, 'opf', 'u_AC.mtx'))
            self.assertTrue(mfeq2(AA, mpA.tocsr()), msg)
            self.assertTrue(mfeq1(ll, mpl.flatten()), msg)
            self.assertTrue(mfeq1(uu, mpu.flatten()), msg)
        return

    def test_var_bounds(self):
        """ Test bounds on optimisation variables.
        """
        msg = self.case_name
        (_, xmin, xmax) = self.solver._var_bounds()
        mpxmin = mmread(join(DATA_DIR, self.case_name, 'opf', 'xmin_AC.mtx'))
        mpxmax = mmread(join(DATA_DIR, self.case_name, 'opf', 'xmax_AC.mtx'))
        self.assertTrue(mfeq1(xmin, mpxmin.flatten()), msg)
        self.assertTrue(mfeq1(xmax, mpxmax.flatten()), msg)

    def test_initial_point(self):
        """ Test selection of an initial interior point.
        """
        (b, l, g, _) = self.solver._unpack_model(self.om)
        (_, LB, UB) = self.solver._var_bounds()
        (_, _, _, _, _, ny, _) = self.solver._dimension_data(b, l, g)
        x0 = self.solver._initial_interior_point(b, g, LB, UB, ny)
        mpx0 = mmread(join(DATA_DIR, self.case_name, 'opf', 'x0_AC.mtx'))
        self.assertTrue(mfeq1(x0, mpx0.flatten()), self.case_name)

    def test_solution(self):
        """ Test AC OPF solution.
        """
        msg = self.case_name
        solution = self.solver.solve()
        lmbda = solution['lmbda']
        f = mmread(join(DATA_DIR, self.case_name, 'opf', 'f_AC.mtx'))
        x = mmread(join(DATA_DIR, self.case_name, 'opf', 'x_AC.mtx'))
        diff = 0.0001
        self.assertAlmostEqual(solution['f'], f[0], places=3)
        self.assertTrue(mfeq1(solution['x'], x.flatten(), diff))
        if len(lmbda['mu_l']) > 0:
            mu_l = mmread(join(DATA_DIR, self.case_name, 'opf', 'mu_l_AC.mtx'))
            self.assertTrue(mfeq1(lmbda['mu_l'], mu_l.flatten(), diff), msg)
        if len(lmbda['mu_u']) > 0:
            mu_u = mmread(join(DATA_DIR, self.case_name, 'opf', 'mu_u_AC.mtx'))
            self.assertTrue(mfeq1(lmbda['mu_u'], mu_u.flatten(), diff), msg)
        if len(lmbda['lower']) > 0:
            muLB = mmread(join(DATA_DIR, self.case_name, 'opf', 'muLB_AC.mtx'))
            self.assertTrue(mfeq1(lmbda['lower'], muLB.flatten(), diff), msg)
        if len(lmbda['upper']) > 0:
            muUB = mmread(join(DATA_DIR, self.case_name, 'opf', 'muUB_AC.mtx'))
            self.assertTrue(mfeq1(lmbda['upper'], muUB.flatten(), diff), msg)

    def test_integrate_solution(self):
        """ Test integration of AC OPF solution.
        """
        self.solver.solve()
        bus = mmread(join(DATA_DIR, self.case_name, 'opf', 'Bus_AC.mtx'))
        gen = mmread(join(DATA_DIR, self.case_name, 'opf', 'Gen_AC.mtx'))
        branch = mmread(join(DATA_DIR, self.case_name, 'opf', 'Branch_AC.mtx'))
        pl = 4
        for (i, bs) in enumerate(self.case.buses):
            self.assertAlmostEqual(bs.v_magnitude, bus[(i, 7)], pl)
            self.assertAlmostEqual(bs.v_angle, bus[(i, 8)], pl)
            self.assertAlmostEqual(bs.p_lmbda, bus[(i, 13)], pl)
            self.assertAlmostEqual(bs.q_lmbda, bus[(i, 14)], pl)
            self.assertAlmostEqual(bs.mu_vmax, bus[(i, 15)], pl)
            self.assertAlmostEqual(bs.mu_vmin, bus[(i, 16)], pl)

        for (i, gn) in enumerate(self.case.generators):
            self.assertAlmostEqual(gn.p, gen[(i, 1)], pl)
            self.assertAlmostEqual(gn.q, gen[(i, 2)], pl)
            self.assertAlmostEqual(gn.v_magnitude, gen[(i, 5)], pl)
            self.assertAlmostEqual(gn.mu_pmax, gen[(i, 21)], pl)
            self.assertAlmostEqual(gn.mu_pmin, gen[(i, 22)], pl)
            self.assertAlmostEqual(gn.mu_qmax, gen[(i, 23)], pl)
            self.assertAlmostEqual(gn.mu_qmin, gen[(i, 24)], pl)

        for (i, ln) in enumerate(self.case.branches):
            self.assertAlmostEqual(ln.p_from, branch[(i, 13)], pl)
            self.assertAlmostEqual(ln.q_from, branch[(i, 14)], pl)
            self.assertAlmostEqual(ln.p_to, branch[(i, 15)], pl)
            self.assertAlmostEqual(ln.q_to, branch[(i, 16)], pl)
            self.assertAlmostEqual(ln.mu_s_from, branch[(i, 17)], pl)
            self.assertAlmostEqual(ln.mu_s_to, branch[(i, 18)], pl)
            self.assertAlmostEqual(ln.mu_angmin, branch[(i, 19)], pl)
            self.assertAlmostEqual(ln.mu_angmax, branch[(i, 20)], pl)


class PIPSSolverCase24RTSTest(PIPSSolverTest):

    def __init__(self, methodName='runTest'):
        super(PIPSSolverCase24RTSTest, self).__init__(methodName)
        self.case_name = 'case24_ieee_rts'


class PIPSSolvercaseIEEE30Test(PIPSSolverTest):

    def __init__(self, methodName='runTest'):
        super(PIPSSolvercaseIEEE30Test, self).__init__(methodName)
        self.case_name = 'case_ieee30'


class PIPSSolvercase30PWLTest(PIPSSolverTest):

    def __init__(self, methodName='runTest'):
        super(PIPSSolvercase30PWLTest, self).__init__(methodName)
        self.case_name = 'case30pwl'


if __name__ == '__main__':
    import logging, sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(levelname)s: %(message)s')
    unittest.main()