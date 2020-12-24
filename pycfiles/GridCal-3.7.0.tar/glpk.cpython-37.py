# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/santi/Documentos/GitHub/GridCal/src/GridCal/ThirdParty/pulp/solver_interfaces/glpk.py
# Compiled at: 2019-08-27 13:05:03
# Size of source mod 2**32: 14936 bytes
from GridCal.ThirdParty.pulp.solvers import *
glpk = None

class GLPK_CMD(LpSolver_CMD):
    __doc__ = 'The GLPK LP solver'

    def defaultPath(self):
        return self.executableExtension(glpk_path)

    def available(self):
        """True if the solver is available"""
        return self.executable(self.path)

    def actualSolve(self, lp):
        """Solve a well formulated lp problem"""
        if not self.executable(self.path):
            raise PulpSolverError('PuLP: cannot execute ' + self.path)
        elif not self.keepFiles:
            uuid = uuid4().hex
            tmpLp = os.path.join(self.tmpDir, '%s-pulp.lp' % uuid)
            tmpSol = os.path.join(self.tmpDir, '%s-pulp.sol' % uuid)
        else:
            tmpLp = lp.name + '-pulp.lp'
            tmpSol = lp.name + '-pulp.sol'
        lp.writeLP(tmpLp, writeSOS=0)
        proc = ['glpsol', '--cpxlp', tmpLp, '-o', tmpSol]
        if not self.mip:
            proc.append('--nomip')
        proc.extend(self.options)
        self.solution_time = clock()
        if not self.msg:
            proc[0] = self.path
            pipe = open(os.devnull, 'w')
            if operating_system == 'win':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                rc = subprocess.call(proc, stdout=pipe, stderr=pipe, startupinfo=startupinfo)
            else:
                rc = subprocess.call(proc, stdout=pipe, stderr=pipe)
            if rc:
                raise PulpSolverError('PuLP: Error while trying to execute ' + self.path)
            pipe.close()
        else:
            if os.name != 'nt':
                rc = os.spawnvp(os.P_WAIT, self.path, proc)
            else:
                rc = os.spawnv(os.P_WAIT, self.executable(self.path), proc)
            if rc == 127:
                raise PulpSolverError('PuLP: Error while trying to execute ' + self.path)
            self.solution_time += clock()
            if not os.path.exists(tmpSol):
                raise PulpSolverError('PuLP: Error while executing ' + self.path)
            lp.status, values = self.readsol(tmpSol)
            lp.assignVarsVals(values)
            if not self.keepFiles:
                try:
                    os.remove(tmpLp)
                except:
                    pass

                try:
                    os.remove(tmpSol)
                except:
                    pass

            return lp.status

    def readsol(self, filename):
        """Read a GLPK solution file"""
        with open(filename) as (f):
            f.readline()
            rows = int(f.readline().split()[1])
            cols = int(f.readline().split()[1])
            f.readline()
            statusString = f.readline()[12:-1]
            glpkStatus = {'INTEGER OPTIMAL':LpStatusOptimal, 
             'INTEGER NON-OPTIMAL':LpStatusOptimal, 
             'OPTIMAL':LpStatusOptimal, 
             'INFEASIBLE (FINAL)':LpStatusInfeasible, 
             'INTEGER UNDEFINED':LpStatusUndefined, 
             'UNBOUNDED':LpStatusUnbounded, 
             'UNDEFINED':LpStatusUndefined, 
             'INTEGER EMPTY':LpStatusInfeasible}
            if statusString not in glpkStatus:
                raise PulpSolverError('Unknown status returned by GLPK')
            status = glpkStatus[statusString]
            isInteger = statusString in ('INTEGER NON-OPTIMAL', 'INTEGER OPTIMAL',
                                         'INTEGER UNDEFINED')
            values = {}
            for i in range(4):
                f.readline()

            for i in range(rows):
                line = f.readline().split()
                if len(line) == 2:
                    f.readline()

            for i in range(3):
                f.readline()

            for i in range(cols):
                line = f.readline().split()
                name = line[1]
                if len(line) == 2:
                    line = [
                     0, 0] + f.readline().split()
                elif isInteger:
                    if line[2] == '*':
                        value = int(float(line[3]))
                    else:
                        value = float(line[2])
                else:
                    value = float(line[3])
                values[name] = value

        return (
         status, values)


GLPK = GLPK_CMD

class PYGLPK(LpSolver):
    global glpk
    __doc__ = '\n    The glpk LP/MIP solver (via its python interface)\n\n    Copyright Christophe-Marie Duquesne 2012\n\n    The glpk variables are available (after a solve) in var.solverVar\n    The glpk constraints are available in constraint.solverConstraint\n    The Model is in prob.solverModel\n    '
    try:
        import glpk.glpkpi as glpk
    except:

        def available(self):
            """True if the solver is available"""
            return False

        def actualSolve(self, lp, callback=None):
            """Solve a well formulated lp problem"""
            raise PulpSolverError('GLPK: Not Available')

    else:

        def __init__(self, mip=True, msg=True, timeLimit=None, epgap=None, **solverParams):
            """
            Initializes the glpk solver.

            @param mip: if False the solver will solve a MIP as an LP
            @param msg: displays information from the solver to stdout
            @param timeLimit: not handled
            @param epgap: not handled
            @param solverParams: not handled
            """
            global glpk
            LpSolver.__init__(self, mip, msg)
            if not self.msg:
                glpk.glp_term_out(glpk.GLP_OFF)

        def findSolutionValues(self, lp):
            prob = lp.solverModel
            if self.mip and self.hasMIPConstraints(lp.solverModel):
                solutionStatus = glpk.glp_mip_status(prob)
            else:
                solutionStatus = glpk.glp_get_status(prob)
            glpkLpStatus = {glpk.GLP_OPT: LpStatusOptimal, 
             glpk.GLP_UNDEF: LpStatusUndefined, 
             glpk.GLP_FEAS: LpStatusNotSolved, 
             glpk.GLP_INFEAS: LpStatusInfeasible, 
             glpk.GLP_NOFEAS: LpStatusInfeasible, 
             glpk.GLP_UNBND: LpStatusUnbounded}
            for var in lp.variables():
                if self.mip and self.hasMIPConstraints(lp.solverModel):
                    var.varValue = glpk.glp_mip_col_val(prob, var.glpk_index)
                else:
                    var.varValue = glpk.glp_get_col_prim(prob, var.glpk_index)
                var.dj = glpk.glp_get_col_dual(prob, var.glpk_index)

            for constr in lp.constraints.values():
                if self.mip and self.hasMIPConstraints(lp.solverModel):
                    row_val = glpk.glp_mip_row_val(prob, constr.glpk_index)
                else:
                    row_val = glpk.glp_get_row_prim(prob, constr.glpk_index)
                constr.slack = -constr.constant - row_val
                constr.pi = glpk.glp_get_row_dual(prob, constr.glpk_index)

            lp.resolveOK = True
            for var in lp.variables():
                var.isModified = False

            lp.status = glpkLpStatus.get(solutionStatus, LpStatusUndefined)
            return lp.status

        def available(self):
            """True if the solver is available"""
            return True

        def hasMIPConstraints(self, solverModel):
            return glpk.glp_get_num_int(solverModel) > 0 or glpk.glp_get_num_bin(solverModel) > 0

        def callSolver(self, lp, callback=None):
            """Solves the problem with glpk
            """
            self.solveTime = -clock()
            glpk.glp_adv_basis(lp.solverModel, 0)
            glpk.glp_simplex(lp.solverModel, None)
            if self.mip:
                if self.hasMIPConstraints(lp.solverModel):
                    status = glpk.glp_get_status(lp.solverModel)
                    if status in (glpk.GLP_OPT, glpk.GLP_UNDEF, glpk.GLP_FEAS):
                        glpk.glp_intopt(lp.solverModel, None)
            self.solveTime += clock()

        def buildSolverModel(self, lp):
            """
            Takes the pulp lp model and translates it into a glpk model
            """
            log.debug('create the glpk model')
            prob = glpk.glp_create_prob()
            glpk.glp_set_prob_name(prob, lp.name)
            log.debug('set the sense of the problem')
            if lp.sense == LpMaximize:
                glpk.glp_set_obj_dir(prob, glpk.GLP_MAX)
            log.debug('add the constraints to the problem')
            glpk.glp_add_rows(prob, len(list(lp.constraints.keys())))
            for i, v in enumerate((lp.constraints.items()), start=1):
                name, constraint = v
                glpk.glp_set_row_name(prob, i, name)
                if constraint.sense == LpConstraintLE:
                    glpk.glp_set_row_bnds(prob, i, glpk.GLP_UP, 0.0, -constraint.constant)
                else:
                    if constraint.sense == LpConstraintGE:
                        glpk.glp_set_row_bnds(prob, i, glpk.GLP_LO, -constraint.constant, 0.0)
                    else:
                        if constraint.sense == LpConstraintEQ:
                            glpk.glp_set_row_bnds(prob, i, glpk.GLP_FX, -constraint.constant, -constraint.constant)
                        else:
                            raise PulpSolverError('Detected an invalid constraint type')
                constraint.glpk_index = i

            log.debug('add the variables to the problem')
            glpk.glp_add_cols(prob, len(lp.variables()))
            for j, var in enumerate((lp.variables()), start=1):
                glpk.glp_set_col_name(prob, j, var.name)
                lb = 0.0
                ub = 0.0
                t = glpk.GLP_FR
                if var.lowBound is not None:
                    lb = var.lowBound
                    t = glpk.GLP_LO
                if var.upBound is not None:
                    ub = var.upBound
                    t = glpk.GLP_UP
                if var.upBound is not None:
                    if var.lowBound is not None:
                        if ub == lb:
                            t = glpk.GLP_FX
                        else:
                            t = glpk.GLP_DB
                glpk.glp_set_col_bnds(prob, j, t, lb, ub)
                if var.cat == LpInteger:
                    glpk.glp_set_col_kind(prob, j, glpk.GLP_IV)
                    assert glpk.glp_get_col_kind(prob, j) == glpk.GLP_IV
                var.glpk_index = j

            log.debug('set the objective function')
            for var in lp.variables():
                value = lp.objective.get(var)
                if value:
                    glpk.glp_set_obj_coef(prob, var.glpk_index, value)

            log.debug('set the problem matrix')
            for constraint in lp.constraints.values():
                l = len(list(constraint.items()))
                ind = glpk.intArray(l + 1)
                val = glpk.doubleArray(l + 1)
                for j, v in enumerate((constraint.items()), start=1):
                    var, value = v
                    ind[j] = var.glpk_index
                    val[j] = value

                glpk.glp_set_mat_row(prob, constraint.glpk_index, l, ind, val)

            lp.solverModel = prob

        def actualSolve(self, lp, callback=None):
            """
            Solve a well formulated lp problem

            creates a glpk model, variables and constraints and attaches
            them to the lp model which it then solves
            """
            self.buildSolverModel(lp)
            log.debug('Solve the Model using glpk')
            self.callSolver(lp, callback=callback)
            solutionStatus = self.findSolutionValues(lp)
            for var in lp.variables():
                var.modified = False

            for constraint in lp.constraints.values():
                constraint.modified = False

            return solutionStatus

        def actualResolve(self, lp, callback=None):
            """
            Solve a well formulated lp problem

            uses the old solver and modifies the rhs of the modified
            constraints
            """
            log.debug('Resolve the Model using glpk')
            for constraint in lp.constraints.values():
                i = constraint.glpk_index
                if constraint.modified:
                    if constraint.sense == LpConstraintLE:
                        glpk.glp_set_row_bnds(prob, i, glpk.GLP_UP, 0.0, -constraint.constant)
                    elif constraint.sense == LpConstraintGE:
                        glpk.glp_set_row_bnds(prob, i, glpk.GLP_LO, -constraint.constant, 0.0)
                    elif constraint.sense == LpConstraintEQ:
                        glpk.glp_set_row_bnds(prob, i, glpk.GLP_FX, -constraint.constant, -constraint.constant)
                    else:
                        raise PulpSolverError('Detected an invalid constraint type')

            self.callSolver(lp, callback=callback)
            solutionStatus = self.findSolutionValues(lp)
            for var in lp.variables():
                var.modified = False

            for constraint in lp.constraints.values():
                constraint.modified = False

            return solutionStatus