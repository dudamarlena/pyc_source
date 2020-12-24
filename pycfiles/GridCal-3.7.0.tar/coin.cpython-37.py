# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/santi/Documentos/GitHub/GridCal/src/GridCal/ThirdParty/pulp/solver_interfaces/coin.py
# Compiled at: 2019-09-06 14:06:32
# Size of source mod 2**32: 18506 bytes
from GridCal.ThirdParty.pulp.solvers import *

class COIN_CMD(LpSolver_CMD):
    __doc__ = '\n    The COIN CLP/CBC LP solver\n    now only uses cbc\n    '

    def defaultPath(self):
        return self.executableExtension(cbc_path)

    def __init__(self, path=None, keepFiles=0, mip=1, msg=0, cuts=None, presolve=None, dual=None, strong=None, options=[], fracGap=None, maxSeconds=None, threads=None):
        """

        :param path:
        :param keepFiles:
        :param mip:
        :param msg:
        :param cuts:
        :param presolve:
        :param dual:
        :param strong:
        :param options:
        :param fracGap:
        :param maxSeconds:
        :param threads:
        """
        LpSolver_CMD.__init__(self, path, keepFiles, mip, msg, options)
        self.cuts = cuts
        self.presolve = presolve
        self.dual = dual
        self.strong = strong
        self.fracGap = fracGap
        self.maxSeconds = maxSeconds
        self.threads = threads
        if os.name == 'nt':
            self.tmpDir = ''

    def copy(self):
        """
        Make a copy of self
        """
        aCopy = LpSolver_CMD.copy(self)
        aCopy.cuts = self.cuts
        aCopy.presolve = self.presolve
        aCopy.dual = self.dual
        aCopy.strong = self.strong
        return aCopy

    def actualSolve(self, lp, **kwargs):
        """Solve a well formulated lp problem"""
        return (self.solve_CBC)(lp, **kwargs)

    def available(self):
        """True if the solver is available"""
        return self.executable(self.path)

    def solve_CBC(self, lp, use_mps=True):
        """
        Solve a MIP problem using CBC
        :param lp:
        :param use_mps:
        :return:
        """
        if not self.executable(self.path):
            raise PulpSolverError('Pulp: cannot execute %s cwd: %s' % (self.path, os.getcwd()))
        else:
            if not self.keepFiles:
                uuid = uuid4().hex
                tmpLp = os.path.join(self.tmpDir, '%s-pulp.lp' % uuid)
                tmpMps = os.path.join(self.tmpDir, '%s-pulp.mps' % uuid)
                tmpSol = os.path.join(self.tmpDir, '%s-pulp.sol' % uuid)
            else:
                tmpLp = lp.name + '-pulp.lp'
                tmpMps = lp.name + '-pulp.mps'
                tmpSol = lp.name + '-pulp.sol'
            if use_mps:
                vs, variablesNames, constraintsNames, objectiveName = lp.writeMPS(tmpMps, rename=1)
                cmds = ' ' + tmpMps + ' '
                if lp.sense == LpMaximize:
                    cmds += 'max '
            else:
                lp.writeLP(tmpLp)
                cmds = ' ' + tmpLp + ' '
            if self.threads:
                cmds += 'threads %s ' % self.threads
            else:
                if self.fracGap is not None:
                    cmds += 'ratio %s ' % self.fracGap
                else:
                    if self.maxSeconds is not None:
                        cmds += 'sec %s ' % self.maxSeconds
                    if self.presolve:
                        cmds += 'presolve on '
                    if self.strong:
                        cmds += 'strong %d ' % self.strong
                    if self.cuts:
                        cmds += 'gomory on '
                        cmds += 'knapsack on '
                        cmds += 'probing on '
                    for option in self.options:
                        cmds += option + ' '

                    if self.mip:
                        cmds += 'branch '
                    else:
                        cmds += 'initialSolve '
                cmds += 'printingOptions all '
                cmds += 'solution ' + tmpSol + ' '
                if self.msg:
                    pipe = None
                else:
                    pipe = open(os.devnull, 'w')
            log.debug(self.path + cmds)
            args = list()
            args.append(self.path)
            args.extend(cmds[1:].split())
            cbc = subprocess.Popen(args, stdout=pipe, stderr=pipe)
            if cbc.wait() != 0:
                raise PulpSolverError('Pulp: Error while trying to execute ' + self.path)
            if pipe:
                pipe.close()
            else:
                if not os.path.exists(tmpSol):
                    raise PulpSolverError('Pulp: Error while executing ' + self.path)
                if use_mps:
                    lp.status, values, reducedCosts, shadowPrices, slacks = self.readsol_MPS(tmpSol, lp, lp.variables(), variablesNames, constraintsNames, objectiveName)
                else:
                    lp.status, values, reducedCosts, shadowPrices, slacks = self.readsol_LP(tmpSol, lp, lp.variables())
            lp.assignVarsVals(values)
            lp.assignVarsDj(reducedCosts)
            lp.assignConsPi(shadowPrices)
            lp.assignConsSlack(slacks, activity=True)
            if not self.keepFiles:
                try:
                    os.remove(tmpMps)
                except:
                    pass

                try:
                    os.remove(tmpLp)
                except:
                    pass

                try:
                    os.remove(tmpSol)
                except:
                    pass

        return lp.status

    def readsol_MPS(self, filename, lp, vs, variablesNames, constraintsNames, objectiveName):
        """
        Read a CBC solution file generated from an mps file (different names)
        """
        values = {}
        reverseVn = {}
        for k, n in variablesNames.items():
            reverseVn[n] = k

        reverseCn = {}
        for k, n in constraintsNames.items():
            reverseCn[n] = k

        for v in vs:
            values[v.name] = 0.0

        reducedCosts = {}
        shadowPrices = {}
        slacks = {}
        cbcStatus = {'Optimal':LpStatusOptimal,  'Infeasible':LpStatusInfeasible, 
         'Integer':LpStatusInfeasible, 
         'Unbounded':LpStatusUnbounded, 
         'Stopped':LpStatusNotSolved}
        with open(filename) as (f):
            statusstr = f.readline().split()[0]
            status = cbcStatus.get(statusstr, LpStatusUndefined)
            for l in f:
                if len(l) <= 2:
                    break
                l = l.split()
                if l[0] == '**':
                    l = l[1:]
                vn = l[1]
                val = l[2]
                dj = l[3]
                if vn in reverseVn:
                    values[reverseVn[vn]] = float(val)
                    reducedCosts[reverseVn[vn]] = float(dj)
                if vn in reverseCn:
                    slacks[reverseCn[vn]] = float(val)
                    shadowPrices[reverseCn[vn]] = float(dj)

        return (
         status, values, reducedCosts, shadowPrices, slacks)

    def readsol_LP(self, filename, lp, vs):
        """
        Read a CBC solution file generated from an lp (good names)
        """
        values = {}
        reduced_costs = {}
        shadow_prices = {}
        slacks = {}
        for v in vs:
            values[v.name] = 0.0

        cbc_status = {'Optimal':LpStatusOptimal, 
         'Infeasible':LpStatusInfeasible, 
         'Integer':LpStatusInfeasible, 
         'Unbounded':LpStatusUnbounded, 
         'Stopped':LpStatusNotSolved}
        with open(filename) as (f):
            status_str = f.readline().split()[0]
            status = cbc_status.get(status_str, LpStatusUndefined)
            for l in f:
                if len(l) <= 2:
                    break
                l = l.split()
                if l[0] == '**':
                    l = l[1:]
                vn = l[1]
                val = l[2]
                dj = l[3]
                if vn in values:
                    values[vn] = float(val)
                    reduced_costs[vn] = float(dj)
                if vn in lp.constraints:
                    slacks[vn] = float(val)
                    shadow_prices[vn] = float(dj)

        return (
         status, values, reduced_costs, shadow_prices, slacks)


COIN = COIN_CMD

class PULP_CBC_CMD(COIN_CMD):
    __doc__ = '\n    This solver uses a precompiled version of cbc provided with the package\n    '
    pulp_cbc_path = pulp_cbc_path
    try:
        if os.name != 'nt':
            if not os.access(pulp_cbc_path, os.X_OK):
                import stat
                os.chmod(pulp_cbc_path, stat.S_IXUSR + stat.S_IXOTH)
    except:

        def available(self):
            """True if the solver is available"""
            return False

        def actualSolve(self, lp, callback=None):
            """
            Solve a well formulated lp problem
            """
            raise PulpSolverError('PULP_CBC_CMD: Not Available (check permissions on %s)' % self.pulp_cbc_path)

    else:

        def __init__(self, path=None, *args, **kwargs):
            """
            just loads up COIN_CMD with the path set
            """
            if path is not None:
                raise PulpSolverError('Use COIN_CMD if you want to set a path')
            (COIN_CMD.__init__)(self, *args, path=self.pulp_cbc_path, **kwargs)


def COINMP_DLL_load_dll(path):
    """
    function that loads the DLL useful for debugging installation problems
    """
    import ctypes
    if os.name == 'nt':
        lib = ctypes.windll.LoadLibrary(str(path[(-1)]))
    else:
        mode = ctypes.RTLD_GLOBAL
        for libpath in path[:-1]:
            ctypes.CDLL(libpath, mode=mode)

        lib = ctypes.CDLL((path[(-1)]), mode=mode)
    return lib


class COINMP_DLL(LpSolver):
    __doc__ = '\n    The COIN_MP LP MIP solver (via a DLL or linux so)\n\n    :param timeLimit: The number of seconds before forcing the solver to exit\n    :param epgap: The fractional mip tolerance\n    '
    try:
        lib = COINMP_DLL_load_dll(coinMP_path)
    except (ImportError, OSError):

        @classmethod
        def available(cls):
            """
            True if the solver is available
            """
            return False

        def actualSolve(self, lp):
            """
            Solve a well formulated lp problem
            """
            raise PulpSolverError('COINMP_DLL: Not Available')

    else:
        COIN_INT_LOGLEVEL = 7
        COIN_REAL_MAXSECONDS = 16
        COIN_REAL_MIPMAXSEC = 19
        COIN_REAL_MIPFRACGAP = 34
        lib.CoinGetInfinity.restype = ctypes.c_double
        lib.CoinGetVersionStr.restype = ctypes.c_char_p
        lib.CoinGetSolutionText.restype = ctypes.c_char_p
        lib.CoinGetObjectValue.restype = ctypes.c_double
        lib.CoinGetMipBestBound.restype = ctypes.c_double

        def __init__(self, mip=1, msg=1, cuts=1, presolve=1, dual=1, crash=0, scale=1, rounding=1, integerPresolve=1, strong=5, timeLimit=None, epgap=None):
            LpSolver.__init__(self, mip, msg)
            self.maxSeconds = None
            if timeLimit is not None:
                self.maxSeconds = float(timeLimit)
            self.fracGap = None
            if epgap is not None:
                self.fracGap = float(epgap)
            self.cuts = cuts
            self.presolve = presolve
            self.dual = dual
            self.crash = crash
            self.scale = scale
            self.rounding = rounding
            self.integer_presolve = integerPresolve
            self.strong = strong
            self.debug = 0
            self.coin_time = 0
            self.hProb = None

        def copy(self):
            """Make a copy of self"""
            cpy = LpSolver.copy()
            cpy.cuts = self.cuts
            cpy.presolve = self.presolve
            cpy.dual = self.dual
            cpy.crash = self.crash
            cpy.scale = self.scale
            cpy.rounding = self.rounding
            cpy.integer_presolve = self.integer_presolve
            cpy.strong = self.strong
            return cpy

        @classmethod
        def available(cls):
            """True if the solver is available"""
            return True

        def getSolverVersion(self):
            """
            returns a solver version string

            example:
            >>> COINMP_DLL().getSolverVersion() # doctest: +ELLIPSIS
            '...'
            """
            return self.lib.CoinGetVersionStr()

        def actualSolve(self, lp):
            """
            Solve a well formulated lp problem
            """
            self.debug = 0
            self.lib.CoinInitSolver('')
            self.hProb = hProb = self.lib.CoinCreateProblem(lp.name)
            self.lib.CoinSetIntOption(hProb, self.COIN_INT_LOGLEVEL, ctypes.c_int(self.msg))
            if self.maxSeconds:
                if self.mip:
                    self.lib.CoinSetRealOption(hProb, self.COIN_REAL_MIPMAXSEC, ctypes.c_double(self.maxSeconds))
                else:
                    self.lib.CoinSetRealOption(hProb, self.COIN_REAL_MAXSECONDS, ctypes.c_double(self.maxSeconds))
            if self.fracGap:
                self.lib.CoinSetRealOption(hProb, self.COIN_REAL_MIPFRACGAP, ctypes.c_double(self.fracGap))
            coinDblMax = self.lib.CoinGetInfinity()
            if self.debug:
                print('Before getCoinMPArrays')
            numVars, numRows, numels, rangeCount, objectSense, objectCoeffs, objectConst, rhsValues, rangeValues, rowType, startsBase, lenBase, indBase, elemBase, lowerBounds, upperBounds, initValues, colNames, rowNames, columnType, n2v, n2c = self.getCplexStyleArrays(lp)
            self.lib.CoinLoadProblem(hProb, numVars, numRows, numels, rangeCount, objectSense, objectConst, objectCoeffs, lowerBounds, upperBounds, rowType, rhsValues, rangeValues, startsBase, lenBase, indBase, elemBase, colNames, rowNames, 'Objective')
            if lp.isMIP():
                if self.mip:
                    self.lib.CoinLoadInteger(hProb, columnType)
            if self.msg == 0:
                self.lib.CoinRegisterMsgLogCallback(hProb, ctypes.c_char_p(''), ctypes.POINTER(ctypes.c_int)())
            self.coin_time = -clock()
            self.lib.CoinOptimizeProblem(hProb, 0)
            self.coin_time += clock()
            coin_lp_status = {0:LpStatusOptimal, 
             1:LpStatusInfeasible, 
             2:LpStatusInfeasible, 
             3:LpStatusNotSolved, 
             4:LpStatusNotSolved, 
             5:LpStatusNotSolved, 
             -1:LpStatusUndefined}
            solutionStatus = self.lib.CoinGetSolutionStatus(hProb)
            solutionText = self.lib.CoinGetSolutionText(hProb)
            objectValue = self.lib.CoinGetObjectValue(hProb)
            num_var_double_array = ctypes.c_double * numVars
            num_rows_double_array = ctypes.c_double * numRows
            c_activity = num_var_double_array()
            c_reduced_cost = num_var_double_array()
            c_slack_values = num_rows_double_array()
            c_shadow_prices = num_rows_double_array()
            self.lib.CoinGetSolutionValues(hProb, ctypes.byref(c_activity), ctypes.byref(c_reduced_cost), ctypes.byref(c_slack_values), ctypes.byref(c_shadow_prices))
            variable_values = {}
            variable_dj_values = {}
            constraint_pi_values = {}
            constraint_slack_values = {}
            if lp.isMIP():
                if self.mip:
                    lp.bestBound = self.lib.CoinGetMipBestBound(hProb)
            for i in range(numVars):
                variable_values[self.n2v[i].name] = c_activity[i]
                variable_dj_values[self.n2v[i].name] = c_reduced_cost[i]

            lp.assignVarsVals(variable_values)
            lp.assignVarsDj(variable_dj_values)
            for i in range(numRows):
                constraint_pi_values[self.n2c[i]] = c_shadow_prices[i]
                constraint_slack_values[self.n2c[i]] = c_slack_values[i]

            lp.assignConsPi(constraint_pi_values)
            lp.assignConsSlack(constraint_slack_values)
            self.lib.CoinFreeSolver()
            lp.status = coin_lp_status[self.lib.CoinGetSolutionStatus(hProb)]
            return lp.status


if COINMP_DLL.available():
    COIN = COINMP_DLL