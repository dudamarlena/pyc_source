# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/santi/Documentos/GitHub/GridCal/src/GridCal/ThirdParty/pulp/solver_interfaces/scip.py
# Compiled at: 2019-09-06 15:19:00
# Size of source mod 2**32: 5333 bytes
from GridCal.ThirdParty.pulp.solvers import *

class SCIP_CMD(LpSolver_CMD):
    __doc__ = '\n    The SCIP optimization solver\n    '
    SCIP_STATUSES = {'unknown':LpStatusUndefined, 
     'user interrupt':LpStatusNotSolved, 
     'node limit reached':LpStatusNotSolved, 
     'total node limit reached':LpStatusNotSolved, 
     'stall node limit reached':LpStatusNotSolved, 
     'time limit reached':LpStatusNotSolved, 
     'memory limit reached':LpStatusNotSolved, 
     'gap limit reached':LpStatusNotSolved, 
     'solution limit reached':LpStatusNotSolved, 
     'solution improvement limit reached':LpStatusNotSolved, 
     'restart limit reached':LpStatusNotSolved, 
     'optimal solution found':LpStatusOptimal, 
     'infeasible':LpStatusInfeasible, 
     'unbounded':LpStatusUnbounded, 
     'infeasible or unbounded':LpStatusNotSolved}

    def defaultPath(self):
        return self.executableExtension(scip_path)

    def available(self):
        """
        True if the solver is available
        """
        return self.executable(self.path)

    def actualSolve(self, lp):
        """
        Solve a well formulated lp problem
        """
        if not self.executable(self.path):
            raise PulpSolverError('PuLP: cannot execute ' + self.path)
        else:
            if not self.keepFiles:
                uuid = uuid4().hex
                tmpLp = os.path.join(self.tmpDir, '%s-pulp.lp' % uuid)
                tmpSol = os.path.join(self.tmpDir, '%s-pulp.sol' % uuid)
            else:
                tmpLp = lp.name + '-pulp.lp'
                tmpSol = lp.name + '-pulp.sol'
            lp.writeLP(tmpLp)
            proc = [
             'scip', '-c', 'read "%s"' % tmpLp, '-c', 'optimize',
             '-c', 'write solution "%s"' % tmpSol, '-c', 'quit']
            proc.extend(self.options)
            if not self.msg:
                proc.append('-q')
            self.solution_time = clock()
            subprocess.check_call(proc, stdout=(sys.stdout), stderr=(sys.stderr))
            self.solution_time += clock()
            assert os.path.exists(tmpSol), 'PuLP: Error while executing ' + self.path
        lp.status, values = self.readsol(tmpSol)
        final_vals = {}
        for v in lp.variables():
            final_vals[v.name] = values.get(v.name, 0.0)

        lp.assignVarsVals(final_vals)
        if not self.keepFiles:
            for f in (tmpLp, tmpSol):
                try:
                    os.remove(f)
                except:
                    pass

        return lp.status

    def readsol(self, filename):
        """
        Read a SCIP solution file
        """
        with open(filename) as (f):
            try:
                line = f.readline()
                comps = line.split(': ')
                assert comps[0] == 'solution status'
                assert len(comps) == 2
            except:
                raise PulpSolverError("Can't read SCIP solver output: %r" % line)

            status = SCIP_CMD.SCIP_STATUSES.get(comps[1].strip(), LpStatusUndefined)
            try:
                line = f.readline()
                comps = line.split(': ')
                assert comps[0] == 'objective value'
                assert len(comps) == 2
                float(comps[1].strip())
            except:
                raise PulpSolverError("Can't read SCIP solver output: %r" % line)

            values = {}
            for line in f:
                try:
                    comps = line.split()
                    values[comps[0]] = float(comps[1])
                except:
                    raise PulpSolverError("Can't read SCIP solver output: %r" % line)

        return (
         status, values)


SCIP = SCIP_CMD