# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/tests/solvers/test_euler.py
# Compiled at: 2018-10-13 05:07:25
import nose
from assimulo import testattr
from assimulo.solvers.euler import *
from assimulo.problem import Explicit_Problem
from assimulo.exception import *
import scipy.sparse as sp

class Test_Explicit_Euler:

    def setUp(self):
        """
        This function sets up the test case.
        """
        f = lambda t, y: 1.0
        y0 = 1.0
        self.problem = Explicit_Problem(f, y0)
        self.simulator = ExplicitEuler(self.problem)

    @testattr(stddist=True)
    def test_h(self):
        nose.tools.assert_almost_equal(self.simulator.h, 0.01)
        self.simulator.h = 1.0
        nose.tools.assert_almost_equal(self.simulator.h, 1.0)
        nose.tools.assert_raises(AssimuloException, self.simulator._set_h, [1])

    @testattr(stddist=True)
    def test_time_event(self):
        global nevent
        global tnext
        f = lambda t, y: N.array(1.0)
        tnext = 0.0
        nevent = 0

        def time_events(t, y, sw):
            global nevent
            global tnext
            events = [
             1.0, 2.0, 2.5, 3.0]
            for ev in events:
                if t < ev:
                    tnext = ev
                    break
                else:
                    tnext = None

            nevent += 1
            return tnext

        def handle_event(solver, event_info):
            solver.y += 1.0
            nose.tools.assert_almost_equal(solver.t, tnext)
            assert event_info[0] == []
            assert event_info[1] == True

        exp_mod = Explicit_Problem(f, 0.0)
        exp_mod.time_events = time_events
        exp_mod.handle_event = handle_event
        exp_sim = ExplicitEuler(exp_mod)
        exp_sim(5.0, 100)
        assert nevent == 5

    @testattr(stddist=True)
    def test_integrator(self):
        """
        This tests the functionality of using the normal mode.
        """
        values = self.simulator.simulate(1)
        nose.tools.assert_almost_equal(self.simulator.t_sol[(-1)], 1.0)
        nose.tools.assert_almost_equal(float(self.simulator.y_sol[(-1)]), 2.0)

    @testattr(stddist=True)
    def test_step(self):
        """
        This tests the functionality of using one step mode.
        """
        self.simulator.report_continuously = True
        self.simulator.h = 0.1
        self.simulator.simulate(1)
        nose.tools.assert_almost_equal(self.simulator.t_sol[(-1)], 1.0)
        nose.tools.assert_almost_equal(float(self.simulator.y_sol[(-1)]), 2.0)

    @testattr(stddist=True)
    def test_exception(self):
        """
        This tests that exceptions are no caught when evaluating the RHS in ExpEuler.
        """

        def f(t, y):
            raise NotImplementedError

        prob = Explicit_Problem(f, 0.0)
        sim = ExplicitEuler(prob)
        nose.tools.assert_raises(NotImplementedError, sim.simulate, 1.0)

    @testattr(stddist=True)
    def test_switches(self):
        """
        This tests that the switches are actually turned when override.
        """
        f = lambda t, x, sw: N.array([1.0])
        state_events = lambda t, x, sw: N.array([x[0] - 1.0])

        def handle_event(solver, event_info):
            solver.sw = [False]

        mod = Explicit_Problem(f, [0.0])
        mod.sw0 = [True]
        mod.state_events = state_events
        mod.handle_event = handle_event
        sim = ExplicitEuler(mod)
        assert sim.sw[0] == True
        sim.simulate(3)
        assert sim.sw[0] == False


class Test_Implicit_Euler:

    def setUp(self):
        """
        This function sets up the test case.
        """
        f = lambda t, y: 1.0
        y0 = 1.0
        self.problem = Explicit_Problem(f, y0)
        self.simulator = ImplicitEuler(self.problem)

    @testattr(stddist=True)
    def test_reset_statistics(self):
        assert self.simulator.statistics['nsteps'] == 0
        self.simulator.simulate(5)
        nsteps = self.simulator.statistics['nsteps']
        self.simulator.simulate(6)
        assert self.simulator.statistics['nsteps'] < nsteps

    @testattr(stddist=True)
    def test_usejac_csc_matrix(self):
        """
        This tests the functionality of the property usejac.
        """
        f = lambda t, x: N.array([x[1], -9.82])
        jac = lambda t, x: sp.csc_matrix(N.array([[0.0, 1.0], [0.0, 0.0]]))
        exp_mod = Explicit_Problem(f, [1.0, 0.0])
        exp_mod.jac = jac
        exp_sim = ImplicitEuler(exp_mod)
        exp_sim.simulate(5.0, 100)
        assert exp_sim.statistics['nfcnjacs'] == 0
        nose.tools.assert_almost_equal(exp_sim.y_sol[(-1)][0], -121.9955, 4)
        exp_sim.reset()
        exp_sim.usejac = False
        exp_sim.simulate(5.0, 100)
        nose.tools.assert_almost_equal(exp_sim.y_sol[(-1)][0], -121.9955, 4)
        assert exp_sim.statistics['nfcnjacs'] > 0

    @testattr(stddist=True)
    def test_h(self):
        nose.tools.assert_almost_equal(self.simulator.h, 0.01)
        self.simulator.h = 1.0
        nose.tools.assert_almost_equal(self.simulator.h, 1.0)
        nose.tools.assert_raises(AssimuloException, self.simulator._set_h, [1])

    @testattr(stddist=True)
    def test_time_event(self):
        global nevent
        global tnext
        f = lambda t, y: N.array(1.0)
        tnext = 0.0
        nevent = 0

        def time_events(t, y, sw):
            global nevent
            global tnext
            events = [
             1.0, 2.0, 2.5, 3.0]
            for ev in events:
                if t < ev:
                    tnext = ev
                    break
                else:
                    tnext = None

            nevent += 1
            return tnext

        def handle_event(solver, event_info):
            solver.y += 1.0
            nose.tools.assert_almost_equal(solver.t, tnext)
            assert event_info[0] == []
            assert event_info[1] == True

        exp_mod = Explicit_Problem(f, 0.0)
        exp_mod.time_events = time_events
        exp_mod.handle_event = handle_event
        exp_sim = ImplicitEuler(exp_mod)
        exp_sim(5.0, 100)
        assert nevent == 5

    @testattr(stddist=True)
    def test_integrator(self):
        """
        This tests the functionality of using the normal mode.
        """
        values = self.simulator.simulate(1)
        nose.tools.assert_almost_equal(self.simulator.t_sol[(-1)], 1.0)
        nose.tools.assert_almost_equal(float(self.simulator.y_sol[(-1)]), 2.0)

    @testattr(stddist=True)
    def test_step(self):
        """
        This tests the functionality of using one step mode.
        """
        self.simulator.report_continuously = True
        self.simulator.h = 0.1
        self.simulator.simulate(1)
        nose.tools.assert_almost_equal(self.simulator.t_sol[(-1)], 1.0)
        nose.tools.assert_almost_equal(float(self.simulator.y_sol[(-1)]), 2.0)

    @testattr(stddist=True)
    def test_stiff_problem(self):
        f = lambda t, y: -15.0 * y
        y0 = 1.0
        problem = Explicit_Problem(f, y0)
        simulator = ImplicitEuler(problem)
        t, y = simulator.simulate(1)
        y_correct = lambda t: N.exp(-15 * t)
        abs_err = N.abs(y[:, 0] - y_correct(N.array(t)))
        assert N.max(abs_err) < 0.1

    @testattr(stddist=True)
    def test_switches(self):
        """
        This tests that the switches are actually turned when override.
        """
        f = lambda t, x, sw: N.array([1.0])
        state_events = lambda t, x, sw: N.array([x[0] - 1.0])

        def handle_event(solver, event_info):
            solver.sw = [False]

        mod = Explicit_Problem(f, [0.0])
        mod.sw0 = [True]
        mod.state_events = state_events
        mod.handle_event = handle_event
        sim = ImplicitEuler(mod)
        assert sim.sw[0] == True
        sim.simulate(3)
        assert sim.sw[0] == False