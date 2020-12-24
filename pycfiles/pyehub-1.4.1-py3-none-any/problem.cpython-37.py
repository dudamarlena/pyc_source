# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/pylp/problem.py
# Compiled at: 2019-07-22 13:01:58
# Size of source mod 2**32: 1618 bytes
__doc__ = '\nContains functionality for dealing with a linear programming model.\n'
from typing import Iterable
from collections import namedtuple
import pulp, pulp.solvers
from contexttimer import Timer
from pylp.constraint import Constraint
Status = namedtuple('Status', ['status', 'time'])

def solve(*, objective=None, constraints: Iterable[Constraint]=None, minimize: bool=False, solver: str='glpk', verbose: bool=False) -> Status:
    """
    Solve the linear programming problem.

    Args:
        objective: The objective function
        constraints: The collection of constraints
        minimize: True for minimizing; False for maximizing
        solver: The solver to use. Current supports 'glpk' and 'cplex'.
        verbose: If True, output the results of the solver

    Returns:
        A tuple of the status (eg: Optimal, Unbounded, etc.) and the elapsed
        time
    """
    if minimize:
        sense = pulp.LpMinimize
    else:
        sense = pulp.LpMaximize
    problem = pulp.LpProblem(sense=sense)
    problem += objective.construct()
    if constraints:
        for constraint in constraints:
            problem += constraint.construct()

    elif solver == 'glpk':
        solver = pulp.solvers.GLPK(msg=verbose)
    elif solver == 'cplex':
        solver = pulp.solvers.CPLEX(msg=verbose)
    else:
        raise ValueError(f"Unsupported solver: {solver}")
    with Timer() as (time):
        results = problem.solve(solver)
    status = pulp.LpStatus[results]
    return Status(status=status, time=(time.elapsed))