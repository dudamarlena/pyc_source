# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/tests/test_ode.py
# Compiled at: 2017-12-28 04:09:42
import nose
from assimulo import testattr
from assimulo.ode import *
from assimulo.problem import Explicit_Problem
from assimulo.exception import *

class Test_ODE:

    def setUp(self):
        self.problem = Explicit_Problem(y0=4.0)
        self.simulator = ODE(self.problem)

    @testattr(stddist=True)
    def test_init(self):
        """
        This tests the functionality of the method __init__.
        """
        assert self.simulator.verbosity == NORMAL
        assert self.simulator.report_continuously == False

    @testattr(stddist=True)
    def test_verbosity(self):
        """
        This tests the functionality of the property verbosity.
        """
        nose.tools.assert_raises(AssimuloException, self.simulator._set_verbosity, 'Test')
        nose.tools.assert_raises(AssimuloException, self.simulator._set_verbosity, [1, 31])
        nose.tools.assert_raises(AssimuloException, self.simulator._set_verbosity, [1])
        self.simulator.verbosity = 1
        assert self.simulator.verbosity == 1
        assert self.simulator.options['verbosity'] == 1
        self.simulator.verbosity = 4
        assert self.simulator.verbosity == 4
        assert self.simulator.options['verbosity'] == 4

    @testattr(stddist=True)
    def test_report_continuously(self):
        """
        This tests the functionality of the property report_continuously.
        """
        assert self.simulator.report_continuously == False
        self.simulator.report_continuously = True
        assert self.simulator.report_continuously == True
        assert self.simulator.options['report_continuously'] == True

    def test_step_events_report_continuously(self):
        """
        This test tests if report_continuously is set correctly, when step_events are present.
        """
        self.simulator.supports['report_continuously'] = True
        self.simulator.supports['interpolated_output'] = True
        self.simulator.problem_info['step_events'] = True
        self.simulator.problem = self.problem
        self.simulator(10.0, ncp=10)
        assert self.simulator.report_continuously == True