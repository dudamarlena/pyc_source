# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/tests/solvers/test_rungekutta.py
# Compiled at: 2017-12-28 04:09:42
import nose
from assimulo import testattr
from assimulo.solvers.runge_kutta import *
from assimulo.problem import Explicit_Problem
from assimulo.exception import *

class Test_Dopri5:

    def setUp(self):
        """
        This function sets up the test case.
        """
        f = lambda t, y: 1.0
        y0 = 1
        self.problem = Explicit_Problem(f, y0)
        self.simulator = Dopri5(self.problem)

    @testattr(stddist=True)
    def test_integrator(self):
        """
        This tests the functionality of the method integrate.
        """
        values = self.simulator.simulate(1)
        nose.tools.assert_almost_equal(self.simulator.t_sol[(-1)], 1.0)
        nose.tools.assert_almost_equal(float(self.simulator.y_sol[(-1)]), 2.0)

    @testattr(stddist=True)
    @testattr(stddist=True)
    def test_time_event(self):
        global nevent
        global tnext
        f = lambda t, y: [1.0]
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
        exp_sim = Dopri5(exp_mod)
        exp_sim(5.0, 100)
        assert nevent == 5

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
        sim = Dopri5(mod)
        assert sim.sw[0] == True
        sim.simulate(3)
        assert sim.sw[0] == False


class Test_RungeKutta34:

    def setUp(self):
        """
        This function sets up the test case.
        """
        f = lambda t, y: 1.0
        y0 = 1
        self.problem = Explicit_Problem(f, y0)
        self.simulator = RungeKutta34(self.problem)

    @testattr(stddist=True)
    def test_integrator(self):
        """
        This tests the functionality of the method integrate.
        """
        values = self.simulator.simulate(1)
        nose.tools.assert_almost_equal(self.simulator.t_sol[(-1)], 1.0)
        nose.tools.assert_almost_equal(self.simulator.y_sol[(-1)], 2.0)

    @testattr(stddist=True)
    def test_step(self):
        """
        This tests the functionality of the method step.
        """
        self.simulator.report_continuously = True
        self.simulator.h = 0.1
        self.simulator.simulate(1)
        nose.tools.assert_almost_equal(self.simulator.t_sol[(-1)], 1.0)
        nose.tools.assert_almost_equal(self.simulator.y_sol[(-1)], 2.0)

    @testattr(stddist=True)
    def test_time_event(self):
        global nevent
        global tnext
        f = lambda t, y: [1.0]
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
        exp_sim = RungeKutta34(exp_mod)
        exp_sim(5.0, 100)
        assert nevent == 5

    @testattr(stddist=True)
    def test_tolerance(self):
        """
        This tests the functionality of the tolerances.
        """
        nose.tools.assert_raises(Explicit_ODE_Exception, self.simulator._set_rtol, 'hej')
        nose.tools.assert_raises(Explicit_ODE_Exception, self.simulator._set_atol, 'hej')
        nose.tools.assert_raises(Explicit_ODE_Exception, self.simulator._set_rtol, -1)
        self.simulator.rtol = 1.0
        assert self.simulator._get_rtol() == 1.0
        self.simulator.rtol = 1
        assert self.simulator._get_rtol() == 1
        self.simulator.atol = 1.0
        assert self.simulator.atol == 1.0
        nose.tools.assert_raises(Explicit_ODE_Exception, self.simulator._set_atol, [1.0, 1.0])

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
        sim = RungeKutta34(mod)
        assert sim.sw[0] == True
        sim.simulate(3)
        assert sim.sw[0] == False


class Test_RungeKutta4:

    def setUp(self):
        """
        This function sets up the test case.
        """
        f = lambda t, y: 1.0
        y0 = 1
        self.problem = Explicit_Problem(f, y0)
        self.simulator = RungeKutta4(self.problem)

    @testattr(stddist=True)
    def test_time_event(self):
        global nevent
        global tnext
        f = lambda t, y: [1.0]
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
        exp_sim = RungeKutta4(exp_mod)
        exp_sim(5.0, 100)
        assert nevent == 5

    @testattr(stddist=True)
    def test_integrate(self):
        values = self.simulator.simulate(1)
        nose.tools.assert_almost_equal(self.simulator.t_sol[(-1)], 1.0)
        nose.tools.assert_almost_equal(float(self.simulator.y_sol[(-1)]), 2.0)

    @testattr(stddist=True)
    def test_step(self):
        self.simulator.report_continuously = True
        self.simulator.h = 0.1
        self.simulator.simulate(1)
        nose.tools.assert_almost_equal(self.simulator.t_sol[(-1)], 1.0)
        nose.tools.assert_almost_equal(float(self.simulator.y_sol[(-1)]), 2.0)