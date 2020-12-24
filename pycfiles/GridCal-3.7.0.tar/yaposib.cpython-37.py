# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/santi/Documentos/GitHub/GridCal/src/GridCal/ThirdParty/pulp/solver_interfaces/yaposib.py
# Compiled at: 2019-08-27 13:05:03
# Size of source mod 2**32: 8878 bytes
from GridCal.ThirdParty.pulp.solvers import *
yaposib = None

class YAPOSIB(LpSolver):
    global yaposib
    __doc__ = '\n    COIN OSI (via its python interface)\n\n    Copyright Christophe-Marie Duquesne 2012\n\n    The yaposib variables are available (after a solve) in var.solverVar\n    The yaposib constraints are available in constraint.solverConstraint\n    The Model is in prob.solverModel\n    '
    try:
        import yaposib
    except ImportError:

        def available(self):
            """
            True if the solver is available
            """
            return False

        def actualSolve(self, lp, callback=None):
            """
            Solve a well formulated lp problem
            """
            raise PulpSolverError('YAPOSIB: Not Available')

    else:

        def __init__(self, mip=True, msg=True, timeLimit=None, epgap=None, solverName=None, **solverParams):
            """
            Initializes the yaposib solver.

            @param mip:          if False the solver will solve a MIP as
                                 an LP
            @param msg:          displays information from the solver to
                                 stdout
            @param timeLimit:    not supported
            @param epgap:        not supported
            @param solverParams: not supported
            """
            global yaposib
            LpSolver.__init__(self, mip, msg)
            if solverName:
                self.solverName = solverName
            else:
                self.solverName = yaposib.available_solvers()[0]

        def findSolutionValues(self, lp):
            model = lp.solverModel
            solutionStatus = model.status
            yaposibLpStatus = {'optimal':LpStatusOptimal,  'undefined':LpStatusUndefined, 
             'abandoned':LpStatusInfeasible, 
             'infeasible':LpStatusInfeasible, 
             'limitreached':LpStatusInfeasible}
            for var in lp.variables():
                var.varValue = var.solverVar.solution
                var.dj = var.solverVar.reducedcost

            for constr in lp.constraints.values():
                constr.pi = constr.solverConstraint.dual
                constr.slack = -constr.constant - constr.solverConstraint.activity

            if self.msg:
                print('yaposib status=', solutionStatus)
            lp.resolveOK = True
            for var in lp.variables():
                var.isModified = False

            lp.status = yaposibLpStatus.get(solutionStatus, LpStatusUndefined)
            return lp.status

        def available(self):
            """True if the solver is available"""
            return True

        def callSolver(self, lp, callback=None):
            """Solves the problem with yaposib
            """
            if self.msg == 0:
                tempfile = open(mktemp(), 'w')
                savestdout = os.dup(1)
                os.close(1)
                if os.dup(tempfile.fileno()) != 1:
                    raise PulpSolverError("couldn't redirect stdout - dup() error")
            self.solveTime = -clock()
            lp.solverModel.solve(self.mip)
            self.solveTime += clock()
            if self.msg == 0:
                os.close(1)
                os.dup(savestdout)
                os.close(savestdout)

        def buildSolverModel(self, lp):
            """
            Takes the pulp lp model and translates it into a yaposib model
            """
            log.debug('create the yaposib model')
            lp.solverModel = yaposib.Problem(self.solverName)
            prob = lp.solverModel
            prob.name = lp.name
            log.debug('set the sense of the problem')
            if lp.sense == LpMaximize:
                prob.obj.maximize = True
            log.debug('add the variables to the problem')
            for var in lp.variables():
                col = prob.cols.add(yaposib.vec([]))
                col.name = var.name
                if var.lowBound is not None:
                    col.lowerbound = var.lowBound
                if var.upBound is not None:
                    col.upperbound = var.upBound
                if var.cat == LpInteger:
                    col.integer = True
                prob.obj[col.index] = lp.objective.get(var, 0.0)
                var.solverVar = col

            log.debug('add the Constraints to the problem')
            for name, constraint in lp.constraints.items():
                row = prob.rows.add(yaposib.vec([(var.solverVar.index, value) for var, value in constraint.items()]))
                if constraint.sense == LpConstraintLE:
                    row.upperbound = -constraint.constant
                else:
                    if constraint.sense == LpConstraintGE:
                        row.lowerbound = -constraint.constant
                    else:
                        if constraint.sense == LpConstraintEQ:
                            row.upperbound = -constraint.constant
                            row.lowerbound = -constraint.constant
                        else:
                            raise PulpSolverError('Detected an invalid constraint type')
                row.name = name
                constraint.solverConstraint = row

        def actualSolve(self, lp, callback=None):
            """
            Solve a well formulated lp problem

            creates a yaposib model, variables and constraints and attaches
            them to the lp model which it then solves
            """
            self.buildSolverModel(lp)
            log.debug('Solve the model using yaposib')
            self.callSolver(lp, callback=callback)
            solution_status = self.findSolutionValues(lp)
            for var in lp.variables():
                var.modified = False

            for constraint in lp.constraints.values():
                constraint.modified = False

            return solution_status

        def actualResolve(self, lp, callback=None):
            """
            Solve a well formulated lp problem

            uses the old solver and modifies the rhs of the modified
            constraints
            """
            log.debug('Resolve the model using yaposib')
            for constraint in lp.constraints.values():
                row = constraint.solverConstraint
                if constraint.modified:
                    if constraint.sense == LpConstraintLE:
                        row.upperbound = -constraint.constant
                    elif constraint.sense == LpConstraintGE:
                        row.lowerbound = -constraint.constant
                    elif constraint.sense == LpConstraintEQ:
                        row.upperbound = -constraint.constant
                        row.lowerbound = -constraint.constant
                    else:
                        raise PulpSolverError('Detected an invalid constraint type')

            self.callSolver(lp, callback=callback)
            solution_status = self.findSolutionValues(lp)
            for var in lp.variables():
                var.modified = False

            for constraint in lp.constraints.values():
                constraint.modified = False

            return solution_status