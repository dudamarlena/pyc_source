# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/epscComp/epscOptimizer.py
# Compiled at: 2009-05-29 13:49:17
import wx
from scipy import optimize
from scipy import *
import time, sys
from epscEngine import EpscEngine
from setParameters import SetParameters
from collectData import CollectData
from plotEngine import PlotEngine
import config, optimize as optimize2
from mystic.differential_evolution import DifferentialEvolutionSolver
from mystic.termination import ChangeOverGeneration, VTR
from mystic.strategy import Best1Exp, Rand1Exp, Best2Exp, Best2Exp
from mystic import getch, random_seed, VerboseSow
from mystic.scipy_optimize import NelderMeadSimplexSolver
from mystic.tools import Sow
from mystic.termination import CandidateRelativeTolerance as CRT

class EpscOptimizer:
    """ class which configure optimization and call optimizer
    """

    def __init__(self, epscData):
        self.epscData = epscData
        self.modlPar = SetParameters()
        self.colData = CollectData(self.epscData)
        self.epscEngine = EpscEngine()
        self.firstDraw = True
        self.flagKill = False
        self.flagConsole = False
        self.parNameList = []
        self.resultList = []
        self.errorList = []

    def setModelParameters(self):
        """ function which set up model parameters for optimization
        """
        for i in range(8):
            for j in range(4):
                self.modlPar.addPar(config.voce[i][j], 0, self.epscData.matParam['Phase1'].voce[i][j], comment='Voce parameter for slip systems #' + str(i))
                self.modlPar.parDict[config.voce[i][j]].setActive(self.epscData.optData.voceFlag[i][j])

    def collectData(self, typeOptimizer):
        """ Collect both the experimental data and model data and compare them
        """
        if self.epscData.optData.getData('expData') == 'macro':
            if self.colData.collectMacroData() == -1:
                if not self.flagConsole:
                    self.tempQueue.put('Kill')
                    self.flagKill = True
            self.colData.collectMacroData()
            listError = self.colData.getErrorMacro(typeOptimizer)
        elif self.epscData.optData.getData('expData') == 'hkl':
            self.colData.collectHKLData()
            listError = self.colData.getErrorHKL(typeOptimizer)
        else:
            self.colData.collectMacroData()
            self.colData.collectHKLData()
            listError = self.colData.getErrorBoth(typeOptimizer)
        self.error = listError[0]
        self.tempQueue.put('error')
        self.tempQueue.put(listError[1])
        if not self.flagConsole:
            if self.flagKill == False:
                if self.firstDraw == True:
                    self.tempQueue.put('FirstDraw')
                    self.firstDraw = False
                else:
                    self.tempQueue.put('Draw')
                self.tempQueue.put(self.resultList.pop())
            time.sleep(1)

    def func_leastsq(self, p0, opt):
        """ function which is required for optimizer
            what 'func' do is :
            1. setting up model parameters for optimization
            2. run epsc engine
            3. collect experimental data and modeling result and calculate error

            return : error between exp. and modeling data
        """
        self.parNameList = self.modlPar.setParVals(p0)
        print p0
        self.resultList.append(p0)
        self.modlPar.updateFiles()
        self.epscEngine.callEngine(mode='opt')
        self.collectData(0)
        print 'Error:', self.error
        self.errorList.append(self.error)
        return self.error

    def func_fmin(self, p0):
        """ function which is required for optimizer
            what 'func' do is :
            1. setting up model parameters for optimization
            2. run epsc engine
            3. collect experimental data and modeling result and calculate error

            return : error between exp. and modeling data
        """
        self.parNameList = self.modlPar.setParVals(p0)
        print p0
        self.resultList.append(p0)
        self.modlPar.updateFiles()
        self.epscEngine.callEngine(mode='opt')
        self.collectData(1)
        print 'Error:', self.error
        self.errorList.append(self.error)
        return self.error

    def func_mystic(self, p0):
        """ function which is required for optimizer
            what 'func' do is :
            1. setting up model parameters for optimization
            2. run epsc engine
            3. collect experimental data and modeling result and calculate error

            return : error between exp. and modeling data
        """
        self.modlPar.setParVals(array(p0))
        print p0
        self.resultList.append(p0)
        self.modlPar.updateFiles()
        self.epscEngine.callEngine(mode='opt')
        self.collectData(1)
        print 'Error:', self.error
        self.errorList.append(self.error)
        return self.error

    def callOptimizer(self):
        """ function:
            1. select model parameters for optimization
            2. prepare parameters for calling optimizer
            3. call optimization function from scipy
        """
        self.setModelParameters()
        self.modlPar.selectPars()
        p0 = self.modlPar.getParVals()
        print p0
        lo = []
        hi = []
        for i in range(8):
            for j in range(4):
                if self.epscData.optData.voceFlag[i][j] == 1:
                    lo.append(float(self.epscData.optData.lowVoce[i][j]))
                    hi.append(float(self.epscData.optData.highVoce[i][j]))

        if self.epscData.optData.nameAlgorithm == 'leastsq':
            self.optResult = optimize.leastsq(self.func_leastsq, p0, self.epscData.optData.getData('expData'), epsfcn=0.001, ftol=0.2)
        elif self.epscData.optData.nameAlgorithm == 'fmin':
            self.optResult = optimize.fmin(self.func_fmin, p0)
        elif self.epscData.optData.nameAlgorithm == 'boxmin':
            if self.epscData.optData.checkFlagOn('range') == False:
                return
            else:
                self.optResult = optimize2.simplex(self.func_fmin, p0, (lo, hi), ftol=0.0001)
        elif self.epscData.optData.nameAlgorithm == 'fmin-mystic':
            stepmon = Sow()
            evalmon = Sow()
            solver = NelderMeadSimplexSolver(len(p0))
            solver.SetInitialPoints(p0)
            solver.SetStrictRanges(lo, hi)
            solver.enable_signal_handler()
            xtol = 0.0001
            ftol = 0.0001
            disp = 1
            solver.Solve(self.func_mystic, termination=CRT(xtol, ftol), EvaluationMonitor=evalmon, StepMonitor=stepmon, disp=disp, ExtraArgs=(), callback=None)
            solution = solver.Solution()
            self.optResult = solution
        elif self.epscData.optData.nameAlgorithm == 'de':
            xtol = 0.0001
            ftol = 0.0001
            NP = 50
            MAX_GENERATIONS = 2500
            solver = DifferentialEvolutionSolver(len(p0), NP)
            stepmon = Sow()
            solver.SetInitialPoints(p0)
            solver.Solve(self.func_mystic, termination=CRT(xtol, ftol), maxiter=MAX_GENERATIONS, CrossProbability=0.5, ScalingFactor=0.5, StepMonitor=stepmon)
            self.optResult = solver.Solution()
        self.printResultFile()
        return self.optResult

    def callOptimizer2(self, tempQueue):
        """ function:
            1. select model parameters for optimization
            2. prepare parameters for calling optimizer
            3. call optimization function from scipy
        """
        self.tempQueue = tempQueue
        self.firstDraw = True
        self.setModelParameters()
        self.modlPar.selectPars()
        p0 = self.modlPar.getParVals()
        print p0
        lo = []
        hi = []
        for i in range(8):
            for j in range(4):
                if self.epscData.optData.voceFlag[i][j] == 1:
                    lo.append(float(self.epscData.optData.lowVoce[i][j]))
                    hi.append(float(self.epscData.optData.highVoce[i][j]))

        if self.epscData.optData.nameAlgorithm == 'leastsq':
            self.optResult = optimize.leastsq(self.func_leastsq, p0, self.epscData.optData.getData('expData'), epsfcn=0.001, ftol=0.2)
        elif self.epscData.optData.nameAlgorithm == 'fmin':
            self.optResult = optimize.fmin(self.func_fmin, p0)
        elif self.epscData.optData.nameAlgorithm == 'boxmin':
            if self.epscData.optData.checkFlagOn('range') == False:
                return
            else:
                self.optResult = optimize2.simplex(self.func_fmin, p0, (lo, hi), ftol=0.0001)
        elif self.epscData.optData.nameAlgorithm == 'fmin-mystic':
            stepmon = Sow()
            evalmon = Sow()
            solver = NelderMeadSimplexSolver(len(p0))
            solver.SetInitialPoints(p0)
            solver.SetStrictRanges(lo, hi)
            solver.enable_signal_handler()
            xtol = 0.0001
            ftol = 0.0001
            disp = 1
            solver.Solve(self.func_mystic, termination=CRT(xtol, ftol), EvaluationMonitor=evalmon, StepMonitor=stepmon, disp=disp, ExtraArgs=(), callback=None)
            solution = solver.Solution()
            self.optResult = solution
        elif self.epscData.optData.nameAlgorithm == 'de':
            xtol = 0.0001
            ftol = 0.0001
            NP = 50
            MAX_GENERATIONS = 2500
            solver = DifferentialEvolutionSolver(len(p0), NP)
            stepmon = Sow()
            solver.SetInitialPoints(p0)
            solver.Solve(self.func_mystic, termination=CRT(xtol, ftol), maxiter=MAX_GENERATIONS, CrossProbability=0.5, ScalingFactor=0.5, StepMonitor=stepmon)
            self.optResult = solver.Solution()
        self.printResultFile()
        return self.optResult

    def printResultFile(self):
        fid = open(config.dirTemp + 'optLog.txt', 'w')
        fid.write((' ').join(self.parNameList))
        fid.write('\n')
        for i in range(len(self.resultList)):
            fid.write(str(i + 1) + ' ')
            fid.write(str(self.resultList[i]))
            fid.write('\n')

        fid.write('Error:\n')
        for i in range(len(self.errorList)):
            fid.write(str(i + 1) + ' ')
            fid.write(str(self.errorList[i]))
            fid.write('\n')

        fid.write('Final result:')
        fid.write('\n')
        fid.close()