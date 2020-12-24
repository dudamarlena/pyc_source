# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/santi/Documentos/GitHub/GridCal/src/GridCal/ThirdParty/pulp/tests.py
# Compiled at: 2019-07-13 06:16:34
# Size of source mod 2**32: 21504 bytes
"""
Tests for pulp
"""
from .pulp import *

def dumpTestProblem(prob):
    try:
        prob.writeLP('debug.lp')
        prob.writeMPS('debug.mps')
    except:
        print('(Failed to write the test problem.)')


def pulpTestCheck(prob, solver, okstatus, sol={}, reducedcosts=None, duals=None, slacks=None, eps=0.001, status=None, objective=None, **kwargs):
    if status is None:
        status = (prob.solve)(solver, **kwargs)
    else:
        if status not in okstatus:
            dumpTestProblem(prob)
            print('Failure: status ==', status, 'not in', okstatus)
            print('Failure: status ==', LpStatus[status], 'not in', [LpStatus[s] for s in okstatus])
            raise PulpError('Tests failed for solver %s' % solver)
        if sol:
            for v, x in sol.items():
                if abs(v.varValue - x) > eps:
                    dumpTestProblem(prob)
                    print('Test failed: var', v, '==', v.varValue, '!=', x)
                    raise PulpError('Tests failed for solver %s' % solver)

        if reducedcosts:
            for v, dj in reducedcosts.items():
                if abs(v.dj - dj) > eps:
                    dumpTestProblem(prob)
                    print('Test failed: var.dj', v, '==', v.dj, '!=', dj)
                    raise PulpError('Tests failed for solver %s' % solver)

        if duals:
            for cname, p in duals.items():
                c = prob.constraints[cname]
                if abs(c.pi - p) > eps:
                    dumpTestProblem(prob)
                    print('Test failed: constraint.pi', cname, '==', c.pi, '!=', p)
                    raise PulpError('Tests failed for solver %s' % solver)

        if slacks:
            for cname, slack in slacks.items():
                c = prob.constraints[cname]
                if abs(c.slack - slack) > eps:
                    dumpTestProblem(prob)
                    print('Test failed: constraint.slack', cname, '==', c.slack, '!=', slack)
                    raise PulpError('Tests failed for solver %s' % solver)

        if objective is not None:
            z = prob.objective.value()
            if abs(z - objective) > eps:
                dumpTestProblem(prob)
                print('Test failed: objective ', z, ' != ', objective)
                raise PulpError('Tests failed for solver %s' % solver)


def pulpTest001(solver):
    """
    Test that a variable is deleted when it is suptracted to 0
    """
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0)
    c1 = x + y <= 5
    c2 = c1 + z - z
    print('\t Testing zero subtraction')
    assert str(c2)


def pulpTest009(solver):
    prob = LpProblem('test09', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0)
    w = LpVariable('w', 0)
    prob += (x + 4 * y + 9 * z, 'obj')
    prob += (lpSum([v for v in [x] if False]) >= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7, 'c3')
    prob += (w >= 0, 'c4')
    print('\t Testing inconsistant lp solution')
    if solver.__class__ in [PULP_CBC_CMD, COIN_CMD]:
        pulpTestCheck(prob, solver, [LpStatusInfeasible], {x: 4, y: -1, z: 6, w: 0}, use_mps=False)
    else:
        pulpTestCheck(prob, solver, [LpStatusInfeasible, LpStatusNotSolved,
         LpStatusUndefined])


def pulpTest010(solver):
    prob = LpProblem('test010', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0)
    w = LpVariable('w', 0)
    prob += (x + 4 * y + 9 * z, 'obj')
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7, 'c3')
    prob += (w >= 0, 'c4')
    print('\t Testing continuous LP solution')
    pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 4, y: -1, z: 6, w: 0})


def pulpTest011(solver):
    prob = LpProblem('test011', LpMaximize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0)
    w = LpVariable('w', 0)
    prob += (x + 4 * y + 9 * z, 'obj')
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7, 'c3')
    prob += (w >= 0, 'c4')
    print('\t Testing maximize continuous LP solution')
    pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 4, y: 1, z: 8, w: 0})


def pulpTest012(solver):
    prob = LpProblem('test012', LpMaximize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0)
    w = LpVariable('w', 0)
    prob += (x + 4 * y + 9 * z + w, 'obj')
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7, 'c3')
    prob += (w >= 0, 'c4')
    print('\t Testing unbounded continuous LP solution')
    if solver.__class__ in [GUROBI, CPLEX_CMD, YAPOSIB, CPLEX_PY]:
        pulpTestCheck(prob, solver, [LpStatusInfeasible])
    else:
        if solver.__class__ in [COINMP_DLL]:
            print('\t\t Error in CoinMP it reports Optimal')
            pulpTestCheck(prob, solver, [LpStatusOptimal])
        else:
            if solver.__class__ is GLPK_CMD:
                pulpTestCheck(prob, solver, [LpStatusUndefined])
            else:
                if solver.__class__ in [CPLEX_DLL, GUROBI_CMD]:
                    pulpTestCheck(prob, solver, [LpStatusNotSolved])
                else:
                    pulpTestCheck(prob, solver, [LpStatusUnbounded])


def pulpTest013(solver):
    prob = LpProblem('test013', LpMinimize)
    x = LpVariable('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0)
    w = LpVariable('w', 0)
    prob += (x + 4 * y + 9 * z, 'obj')
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7, 'c3')
    prob += (w >= 0, 'c4')
    print('\t Testing Long Names')
    if solver.__class__ in [CPLEX_CMD, GLPK_CMD, GUROBI_CMD]:
        try:
            pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 4, y: -1, z: 6, w: 0})
        except PulpError:
            pass

    else:
        pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 4, y: -1, z: 6, w: 0})


def pulpTest014(solver):
    prob = LpProblem('test014', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('x', -1, 1)
    z = LpVariable('z', 0)
    w = LpVariable('w', 0)
    prob += (x + 4 * y + 9 * z, 'obj')
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7, 'c3')
    prob += (w >= 0, 'c4')
    print('\t Testing repeated Names')
    if solver.__class__ in [COIN_CMD, COINMP_DLL, PULP_CBC_CMD,
     CPLEX_CMD, CPLEX_DLL, CPLEX_PY,
     GLPK_CMD, GUROBI_CMD]:
        try:
            pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 4, y: -1, z: 6, w: 0})
        except PulpError:
            pass

    else:
        pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 4, y: -1, z: 6, w: 0})


def pulpTest015(solver):
    prob = LpProblem('test015', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0)
    w = LpVariable('w', 0)
    prob += (x + 4 * y + 9 * z, 'obj')
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7, 'c3')
    prob += (w >= 0, 'c4')
    prob += (lpSum([0, 0]) <= 0, 'c5')
    print('\t Testing zero constraint')
    pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 4, y: -1, z: 6, w: 0})


def pulpTest016(solver):
    prob = LpProblem('test016', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0)
    w = LpVariable('w', 0)
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7, 'c3')
    prob += (w >= 0, 'c4')
    prob += (lpSum([0, 0]) <= 0, 'c5')
    print('\t Testing zero objective')
    pulpTestCheck(prob, solver, [LpStatusOptimal])


def pulpTest017(solver):
    prob = LpProblem('test017', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0)
    w = LpVariable('w', 0)
    prob.setObjective(x)
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7, 'c3')
    prob += (w >= 0, 'c4')
    prob += (lpSum([0, 0]) <= 0, 'c5')
    print('\t Testing LpVariable (not LpAffineExpression) objective')
    pulpTestCheck(prob, solver, [LpStatusOptimal])


def pulpTest018(solver):
    prob = LpProblem('test018', LpMinimize)
    x = LpVariable('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 0, 4)
    y = LpVariable('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy', -1, 1)
    z = LpVariable('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz', 0)
    w = LpVariable('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww', 0)
    prob += (x + 4 * y + 9 * z, 'obj')
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7, 'c3')
    prob += (w >= 0, 'c4')
    if solver.__class__ in [PULP_CBC_CMD, COIN_CMD]:
        print('\t Testing Long lines in LP')
        pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 4, y: -1, z: 6, w: 0}, use_mps=False)


def pulpTest019(solver):
    prob = LpProblem('test019', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0)
    w = LpVariable('w', 0)
    prob += (x + 4 * y + 9 * z, 'obj')
    prob += ((2 * x + 2 * y).__div__(2.0) <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7, 'c3')
    prob += (w >= 0, 'c4')
    print('\t Testing LpAffineExpression divide')
    pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 4, y: -1, z: 6, w: 0})


def pulpTest020(solver):
    prob = LpProblem('test020', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0, None, LpInteger)
    prob += (x + 4 * y + 9 * z, 'obj')
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7.5, 'c3')
    print('\t Testing MIP solution')
    pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 3, y: -0.5, z: 7})


def pulpTest021(solver):
    prob = LpProblem('test021', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0, None, LpInteger)
    prob += (1.1 * x + 4.1 * y + 9.1 * z, 'obj')
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7.5, 'c3')
    print('\t Testing MIP solution with floats in objective')
    pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 3, y: -0.5, z: 7}, objective=64.95)


def pulpTest030(solver):
    prob = LpProblem('test030', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0, None, LpInteger)
    prob += (x + 4 * y + 9 * z, 'obj')
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7.5, 'c3')
    solver.mip = 0
    print('\t Testing MIP relaxation')
    if solver.__class__ in [GUROBI_CMD]:
        pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 3.0, y: -0.5, z: 7})
    else:
        pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 3.5, y: -1, z: 6.5})


def pulpTest040(solver):
    prob = LpProblem('test040', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0, None, LpInteger)
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7.5, 'c3')
    print('\t Testing feasibility problem (no objective)')
    pulpTestCheck(prob, solver, [LpStatusOptimal])


def pulpTest050(solver):
    prob = LpProblem('test050', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0, 10)
    prob += (x + y <= 5.2, 'c1')
    prob += (x + z >= 10.3, 'c2')
    prob += (-y + z == 17.5, 'c3')
    print('\t Testing an infeasible problem')
    if solver.__class__ is GLPK_CMD:
        pulpTestCheck(prob, solver, [LpStatusUndefined])
    else:
        if solver.__class__ in [CPLEX_DLL, GUROBI_CMD]:
            pulpTestCheck(prob, solver, [LpStatusNotSolved])
        else:
            pulpTestCheck(prob, solver, [LpStatusInfeasible])


def pulpTest060(solver):
    prob = LpProblem('test060', LpMinimize)
    x = LpVariable('x', 0, 4, LpInteger)
    y = LpVariable('y', -1, 1, LpInteger)
    z = LpVariable('z', 0, 10, LpInteger)
    prob += (x + y <= 5.2, 'c1')
    prob += (x + z >= 10.3, 'c2')
    prob += (-y + z == 7.4, 'c3')
    print('\t Testing an integer infeasible problem')
    if solver.__class__ in [GLPK_CMD, COIN_CMD, PULP_CBC_CMD]:
        pulpTestCheck(prob, solver, [LpStatusInfeasible, LpStatusUndefined])
    else:
        if solver.__class__ in [COINMP_DLL]:
            print('\t\t Error in CoinMP to be fixed, reports Optimal')
            pulpTestCheck(prob, solver, [LpStatusOptimal])
        else:
            if solver.__class__ in [GUROBI_CMD]:
                pulpTestCheck(prob, solver, [LpStatusNotSolved])
            else:
                pulpTestCheck(prob, solver, [LpStatusInfeasible])


def pulpTest070(solver):
    prob = LpProblem('test070', LpMinimize)
    obj = LpConstraintVar('obj')
    a = LpConstraintVar('C1', LpConstraintLE, 5)
    b = LpConstraintVar('C2', LpConstraintGE, 10)
    c = LpConstraintVar('C3', LpConstraintEQ, 7)
    prob.setObjective(obj)
    prob += a
    prob += b
    prob += c
    x = LpVariable('x', 0, 4, LpContinuous, obj + a + b)
    y = LpVariable('y', -1, 1, LpContinuous, 4 * obj + a - c)
    z = LpVariable('z', 0, None, LpContinuous, 9 * obj + b + c)
    print('\t Testing column based modelling')
    pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 4, y: -1, z: 6})


def pulpTest075(solver):
    prob = LpProblem('test075', LpMinimize)
    obj = LpConstraintVar('obj')
    a = LpConstraintVar('C1', LpConstraintLE, 5)
    b = LpConstraintVar('C2', LpConstraintGE, 10)
    c = LpConstraintVar('C3', LpConstraintEQ, 7)
    prob.setObjective(obj)
    prob += a
    prob += b
    prob += c
    x = LpVariable('x', 0, 4, LpContinuous, obj + b)
    y = LpVariable('y', -1, 1, LpContinuous, 4 * obj - c)
    z = LpVariable('z', 0, None, LpContinuous, 9 * obj + b + c)
    if solver.__class__ in [CPLEX_DLL, CPLEX_CMD, COINMP_DLL, YAPOSIB,
     PYGLPK]:
        print('\t Testing column based modelling with empty constraints')
        pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 4, y: -1, z: 6})


def pulpTest080(solver):
    """
    Test the reporting of dual variables slacks and reduced costs
    """
    prob = LpProblem('test080', LpMinimize)
    x = LpVariable('x', 0, 5)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0)
    c1 = x + y <= 5
    c2 = x + z >= 10
    c3 = -y + z == 7
    prob += (x + 4 * y + 9 * z, 'obj')
    prob += (c1, 'c1')
    prob += (c2, 'c2')
    prob += (c3, 'c3')
    if solver.__class__ in [CPLEX_DLL, CPLEX_CMD, COINMP_DLL,
     PULP_CBC_CMD, YAPOSIB, PYGLPK]:
        print('\t Testing dual variables and slacks reporting')
        pulpTestCheck(prob, solver, [LpStatusOptimal], sol={x: 4, y: -1, z: 6},
          reducedcosts={x: 0, y: 12, z: 0},
          duals={'c1':0, 
         'c2':1,  'c3':8},
          slacks={'c1':2, 
         'c2':0,  'c3':0})


def pulpTest090(solver):
    prob = LpProblem('test090', LpMinimize)
    obj = LpConstraintVar('obj')
    a = LpConstraintVar('C1', LpConstraintLE, 5)
    b = LpConstraintVar('C2', LpConstraintGE, 10)
    c = LpConstraintVar('C3', LpConstraintEQ, 7)
    prob.setObjective(obj)
    prob += a
    prob += b
    prob += c
    prob.setSolver(solver)
    x = LpVariable('x', 0, 4, LpContinuous, obj + a + b)
    y = LpVariable('y', -1, 1, LpContinuous, 4 * obj + a - c)
    prob.resolve()
    z = LpVariable('z', 0, None, LpContinuous, 9 * obj + b + c)
    if solver.__class__ in [CPLEX_DLL, COINMP_DLL]:
        print('\t Testing resolve of problem')
        prob.resolve()


def pulpTest100(solver):
    """
    Test the ability to sequentially solve a problem
    """
    prob = LpProblem('test100', LpMinimize)
    x = LpVariable('x', 0, 1)
    y = LpVariable('y', 0, 1)
    z = LpVariable('z', 0, 1)
    obj1 = x + 0 * y + 0 * z
    obj2 = 0 * x - 1 * y + 0 * z
    prob += (x <= 1, 'c1')
    if solver.__class__ in [CPLEX_DLL, COINMP_DLL, GUROBI]:
        print('\t Testing Sequential Solves')
        status = prob.sequentialSolve([obj1, obj2], solver=solver)
        pulpTestCheck(prob, solver, [[LpStatusOptimal, LpStatusOptimal]], sol={x: 0, y: 1},
          status=status)


def pulpTest110(solver):
    """
    Test the ability to use fractional constraints
    """
    prob = LpProblem('test110', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0)
    w = LpVariable('w', 0)
    prob += (x + 4 * y + 9 * z, 'obj')
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7, 'c3')
    prob += (w >= 0, 'c4')
    prob += LpFractionConstraint(x, z, LpConstraintEQ, 0.5, name='c5')
    print('\t Testing fractional constraints')
    pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 3.3333333333333335, y: -0.3333333333333333, z: 6.666666666666667, w: 0})


def pulpTest120(solver):
    """
    Test the ability to use Elastic constraints
    """
    prob = LpProblem('test120', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0)
    w = LpVariable('w')
    prob += (x + 4 * y + 9 * z + w, 'obj')
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7, 'c3')
    prob.extend((w >= -1).makeElasticSubProblem())
    print('\t Testing elastic constraints (no change)')
    pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 4, y: -1, z: 6, w: -1})


def pulpTest121(solver):
    """
    Test the ability to use Elastic constraints
    """
    prob = LpProblem('test121', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0)
    w = LpVariable('w')
    prob += (x + 4 * y + 9 * z + w, 'obj')
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7, 'c3')
    prob.extend((w >= -1).makeElasticSubProblem(proportionFreeBound=0.1))
    print('\t Testing elastic constraints (freebound)')
    pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 4, y: -1, z: 6, w: -1.1})


def pulpTest122(solver):
    """
    Test the ability to use Elastic constraints (penalty unchanged)
    """
    prob = LpProblem('test122', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0)
    w = LpVariable('w')
    prob += (x + 4 * y + 9 * z + w, 'obj')
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7, 'c3')
    prob.extend((w >= -1).makeElasticSubProblem(penalty=1.1))
    print('\t Testing elastic constraints (penalty unchanged)')
    pulpTestCheck(prob, solver, [LpStatusOptimal], {x: 4, y: -1, z: 6, w: -1.0})


def pulpTest123(solver):
    """
    Test the ability to use Elastic constraints (penalty unbounded)
    """
    prob = LpProblem('test123', LpMinimize)
    x = LpVariable('x', 0, 4)
    y = LpVariable('y', -1, 1)
    z = LpVariable('z', 0)
    w = LpVariable('w')
    prob += (x + 4 * y + 9 * z + w, 'obj')
    prob += (x + y <= 5, 'c1')
    prob += (x + z >= 10, 'c2')
    prob += (-y + z == 7, 'c3')
    prob.extend((w >= -1).makeElasticSubProblem(penalty=0.9))
    print('\t Testing elastic constraints (penalty unbounded)')
    if solver.__class__ in [COINMP_DLL, GUROBI, CPLEX_CMD, CPLEX_PY, YAPOSIB]:
        pulpTestCheck(prob, solver, [LpStatusInfeasible])
    else:
        if solver.__class__ is GLPK_CMD:
            pulpTestCheck(prob, solver, [LpStatusUndefined])
        else:
            if solver.__class__ in [CPLEX_DLL, GUROBI_CMD]:
                pulpTestCheck(prob, solver, [LpStatusNotSolved])
            else:
                pulpTestCheck(prob, solver, [LpStatusUnbounded])


def pulpTestSolver(solver, msg=0):
    tests = [pulpTest001,
     pulpTest009,
     pulpTest010, pulpTest011, pulpTest012, pulpTest013, pulpTest014,
     pulpTest015, pulpTest016, pulpTest017,
     pulpTest018, pulpTest019,
     pulpTest020, pulpTest021,
     pulpTest030,
     pulpTest040,
     pulpTest050,
     pulpTest060,
     pulpTest070, pulpTest075,
     pulpTest080,
     pulpTest090,
     pulpTest100,
     pulpTest110,
     pulpTest120, pulpTest121, pulpTest122, pulpTest123]
    for t in tests:
        t(solver(msg=msg))