# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/builder/problem.py
# Compiled at: 2019-10-29 02:46:28
# Size of source mod 2**32: 5557 bytes
import casadi.casadi as cs
from .set_y_calculator import SetYCalculator
from ..constraints.no_constraints import NoConstraints

class Problem:
    __doc__ = 'Definition of an optimization problem\n\n    Provides the cost function, constraints and additional\n    ALM/penalty-type constraints.\n    '

    def __init__(self, u, p, cost):
        """Construct an optimization problem

            :param u: decision variable (CasADi variable)
            :param p: parameter (CasADi variable)
            :param cost: cost function (CasADi function of u and p)

        Example:
            >>> import casadi.casadi as cs
            >>> import opengen as og
            >>> # Define u and p
            >>> u = cs.SX.sym('u', 5)
            >>> p = cs.SX.sym('p', 2)
            >>> # Cost function
            >>> phi = og.functions.rosenbrock(u, p)
            >>> # Define optimization problem
            >>> problem = og.builder.Problem(u, p, phi)

        """
        self._Problem__u = u
        self._Problem__p = p
        self._Problem__cost = cost
        self._Problem__u_constraints = NoConstraints()
        self._Problem__alm_mapping_f1 = None
        self._Problem__alm_set_c = None
        self._Problem__alm_set_y = None
        self._Problem__penalty_mapping_f2 = None
        self._Problem__penalty_function = None

    def with_constraints(self, u_constraints):
        """Specify or update the constraints of the problem

        Args:
            u_constraints: constraints on the decision variable; must
                           be a Constraint object (such as
                           opengen.constraints.ball2.Ball2
                           and opengen.constraints.rectangle.Rectangle)

        Returns:
            Current object

        """
        self._Problem__u_constraints = u_constraints
        return self

    def with_penalty_constraints(self, penalty_constraints):
        """Constraints to for the penalty method

        Specify the constraints to be treated with the penalty method (that is,
        function F2(u; p))

        :param penalty_constraints: a function <code>c(u, p)</code>, of the decision
                variable <code>u</code> and the parameter vector <code>p</code>, which
                corresponds to the constraints <code>c(u, p)</code>

        :return: self
        """
        self._Problem__penalty_mapping_f2 = penalty_constraints
        return self

    def with_aug_lagrangian_constraints(self, mapping_f1, set_c, set_y=None):
        """
        Constraints: F1(u, p) in C

        :param mapping_f1: mapping of the form `F1: R^{n} x R^{p} --> R^{n1}`
        :param set_c: a convex closed set C
        :param set_y: a compact subset of C*, the convex conjugate of C

        :return: self
        """
        if not set_c.is_convex():
            raise Exception('Set C must be convex')
        else:
            self._Problem__alm_mapping_f1 = mapping_f1
            self._Problem__alm_set_c = set_c
            if set_y is not None:
                self._Problem__alm_set_y = set_y
            else:
                c = SetYCalculator(set_c)
            self._Problem__alm_set_y = c.obtain()
        return self

    def dim_decision_variables(self):
        """Number of decision variables

        :return: number of decision variables
        """
        return self._Problem__u.size(1)

    def dim_parameters(self):
        """Number of parameters"""
        return self._Problem__p.size(1)

    def dim_constraints_penalty(self):
        """Number of penalty-type constraints"""
        if self._Problem__penalty_mapping_f2 is None:
            return 0
        else:
            return self._Problem__penalty_mapping_f2.size(1)

    def dim_constraints_aug_lagrangian(self):
        """Not implemented yet"""
        if self._Problem__alm_mapping_f1 is None:
            return 0
        else:
            return self._Problem__alm_mapping_f1.size(1)

    @property
    def cost_function(self):
        """Cost function as a CaADi symbol"""
        return self._Problem__cost

    @property
    def penalty_mapping_f2(self):
        """Penalty-type mapping F2 as a CasADi symbol"""
        return self._Problem__penalty_mapping_f2

    @property
    def penalty_mapping_f1(self):
        """ALM mapping F1 as a CasADi symbol"""
        return self._Problem__alm_mapping_f1

    @property
    def alm_set_c(self):
        """Set C in the definition of constraints: F1(u, p) in C"""
        return self._Problem__alm_set_c

    @property
    def alm_set_y(self):
        """Set Y for the Lagrange multipliers"""
        return self._Problem__alm_set_y

    @property
    def penalty_function(self):
        """Penalty function, g"""
        return self._Problem__penalty_function

    @property
    def constraints(self):
        """Hard constraints; set U"""
        return self._Problem__u_constraints

    @property
    def decision_variables(self):
        """Decision variables (CasADi symbol)"""
        return self._Problem__u

    @property
    def parameter_variables(self):
        """Parameter variables (CasADi symbol)"""
        return self._Problem__p