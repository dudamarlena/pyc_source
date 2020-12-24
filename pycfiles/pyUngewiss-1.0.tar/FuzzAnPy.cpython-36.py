# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wehrle/opt/FuzzAnPy/FuzzAnPy/FuzzAnPy.py
# Compiled at: 2018-03-26 10:25:10
# Size of source mod 2**32: 30372 bytes
"""
-------------------------------------------------------------------------------
Title:          FuzzAn.py
Version:        1.0
Units:          Unitless
Author:         E. J. Wehrle
Date:           July 24, 2016
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
Description
-------------------------------------------------------------------------------
FuzzAnPy -- FUZZy ANalysis in PYthon -- is an fuzzy and interval toolbox for
Python

-------------------------------------------------------------------------------
Change log
-------------------------------------------------------------------------------
1.0:    October 26, 2015 -- Initial public release

α1.1:
        PyGMO as solver
α1.0:
        PEP8ish

-------------------------------------------------------------------------------
To do and ideas
-------------------------------------------------------------------------------
TODO pickle ptilde and use as start values of next iteration?
TODO pseudo gradients via fuzzy number?
TODO descretisize fuzzy number in FuzzAn? Object oriented scripting of fuzzy
numbers?
-------------------------------------------------------------------------------
"""
from __future__ import absolute_import, division, print_function
import pyOpt, cma, numpy as np, pickle
from sklearn.gaussian_process import GaussianProcess
import pyDOE
__title__ = 'FUZZy ANalysis in PYthon'
__shorttitle__ = 'FuzzAnPy'
__version__ = '1.0 - Initial public release'
__all__ = ['FuzzAn']
__author__ = 'E. J. Wehrle'
__copyright__ = 'Copyright 2015, 2016: E. J. Wehrle'
__email__ = 'wehrle(a)tum.de'
__license__ = 'GNU Lesser General Public License'
__url__ = 'www.FuzzAnPy.org'

def PrintFuzzAnPy():
    print(__title__ + ' - ' + __shorttitle__)
    print('Version:                 ' + __version__)
    print('Internet:                ' + __url__)
    print('License:                 ' + __license__)
    print('Copyright:               ' + __copyright__)
    print('')


def FuzzAn(FuzzySysEq, pFuzz, FuzzySensEq=[], nr=1, Alg='NLPQLP', nAlpha=1, deltax=0.01, paraNorm=True, para=[], SBFA=False, Surr='Kriging', SensCalc='FD', epsStop=0.0001, FuzzyModel='NewName', PrintOut=True):
    global nEval
    if hasattr(FuzzySensEq, '__call__'):
        SensCalc = 'OptSensEq'
    nEval = 0

    def MinSysEq(x):
        global nEval
        x = np.array(x)
        if not SBFA:
            r = FuzzySysEq(x, para, ir)
        else:
            r = Surrogate(x, ir)
        if Alg == 'MMA':
            g = np.array([0.0])
        else:
            g = []
        nEval += 1
        if np.size(r) == 1:
            f = r
        else:
            if np.size(r) > 1:
                f = r[ir]
            else:
                f = r
        fail = 0
        return (f, g, fail)

    def MaxSysEq(x):
        f, g, fail = MinSysEq(x)
        f = -f
        return (f, g, fail)

    def MinSysEqNorm(xNorm):
        xNorm = np.array(xNorm)
        x = denormalize(xNorm, xL, xU)
        f, g, fail = MinSysEq(x)
        return (f, g, fail)

    def MaxSysEqNorm(xNorm):
        f, g, fail = MinSysEqNorm(xNorm)
        f = -f
        return (f, g, fail)

    def MinSensEq(x, f, g):
        dfdx = FuzzySensEq(x, f, g, para, ir)
        if Alg == 'MMA':
            dgdx = np.zeros([1, np.size(x)])
        else:
            dgdx = []
        fail = 0
        return (dfdx.reshape([1, len(x)]), dgdx, fail)

    def MinSensEqNorm(xNorm, f, g):
        x = denormalize(xNorm, xL, xU)
        dfxdx, dgdx, fail = MinSensEq(x, f, g)
        dfdx = dfxdx * (xU - xL)
        return (dfdx, dgdx, fail)

    def MaxSensEq(x, f, g):
        dfdx, dgdx, fail = MinSensEq(x, f, g)
        dfdx *= -1
        return (dfdx, dgdx, fail)

    def MaxSensEqNorm(xNorm, f, g):
        dfdx, dgdx, fail = MinSensEqNorm(xNorm, f, g)
        dfdx *= -1
        return (dfdx, dgdx, fail)

    def normalize(x, xL, xU):
        xNorm = (x - xL) / (xU - xL)
        return xNorm

    def denormalize(xNorm, xL, xU):
        x = xNorm[0:np.size(xL),] * (xU - xL) + xL
        return x

    def DefineProb(x0min, x0max, xL, xU, OptModel, DesVarNorm):
        if DesVarNorm == 1:
            x0minnorm = normalize(x0min, xL, xU)
            x0maxnorm = normalize(x0max, xL, xU)
            MinProb = pyOpt.Optimization(OptModel, MinSysEqNorm, obj_set=None)
            MaxProb = pyOpt.Optimization(OptModel, MaxSysEqNorm, obj_set=None)
            if np.size(x0min) == 1:
                MinProb.addVar('x', 'c', value=x0minnorm, lower=0.0, upper=1.0)
                MaxProb.addVar('x', 'c', value=x0maxnorm, lower=0.0, upper=1.0)
                nx = 1
            elif np.size(x0min) > 1:
                for ii in range(np.size(x0min)):
                    MinProb.addVar(('x' + str(ii + 1)), 'c', value=(x0minnorm[ii]), lower=0.0,
                      upper=1.0)
                    MaxProb.addVar(('x' + str(ii + 1)), 'c', value=(x0maxnorm[ii]), lower=0.0,
                      upper=1.0)

                nx = ii + 1
        else:
            if DesVarNorm == 0:
                MinProb = pyOpt.Optimization(OptModel, MinSysEq)
                MaxProb = pyOpt.Optimization(OptModel, MaxSysEq)
                if np.size(x0min) == 1:
                    MinProb.addVar('x', 'c', value=x0min, lower=xL, upper=xU)
                    MaxProb.addVar('x', 'c', value=x0max, lower=xL, upper=xU)
                    nx = 1
                elif np.size(x0min) > 1:
                    for ii in range(np.size(x0min)):
                        MinProb.addVar(('x' + str(ii + 1)), 'c', value=(x0min[ii]), lower=(xL[ii]),
                          upper=(xU[ii]))
                        MaxProb.addVar(('x' + str(ii + 1)), 'c', value=(x0max[ii]), lower=(xL[ii]),
                          upper=(xU[ii]))

                    nx = ii + 1
            MinProb.addObj('f')
            MaxProb.addObj('f')
            if Alg == 'MMA':
                MinProb.addCon('g', type='i')
                MaxProb.addCon('g', type='i')
            return (
             MinProb, MaxProb)

    def ShadowUncertainty(Name, xOpt, xL, xU):
        epsBorder = 0.001
        Hist = pyOpt.History(Name, 'r')
        dfdxAll = Hist.read([0, -1], ['grad_obj'])[0]['grad_obj']
        dfdxOpt = dfdxAll[(-1)]
        xL_ActiveIndex = np.abs((xOpt.T - xL) / xL) < epsBorder
        xU_ActiveIndex = np.abs((xU - xOpt.T) / xU) < epsBorder
        nx = np.size(xL)
        xL_Grad = -np.eye(nx)
        xU_Grad = np.eye(nx)
        xL_GradActive = xL_Grad * xL_ActiveIndex
        xU_GradActive = xU_Grad * xU_ActiveIndex
        xGradActive = np.concatenate((xL_GradActive, xU_GradActive), axis=1)
        lambda_rp, blah0, blah1, blah2 = np.linalg.lstsq(xGradActive, (-dfdxOpt), rcond=None)
        if Name[(-1)] == 'x':
            lambda_rp *= -1
        else:
            if paraNorm:
                if np.size(xL) == 1:
                    denorm = np.array([xU - xL, xU - xL])
                else:
                    denorm = np.concatenate((xU - xL, xU - xL), axis=0)
                SPrp = lambda_rp / denorm
            else:
                SPrp = lambda_rp
        return (
         SPrp, lambda_rp)

    def AlphaLevelOpt(OptProb, OptAlg, Alg, SensCalc, Name):
        if Alg in ('MMA', 'GCMMA', 'CONMIN', 'KSOPT', 'SLSQP', 'PSQP', 'KSOPT', 'SOLVOPT',
                   'ALGENCAN', 'NLPQLP'):
            if SensCalc == 'OptSensEq':
                if paraNorm:
                    if Name[-3:] == 'Min':
                        fOpt, xOpt, inform = OptAlg(OptProb, sens_type=MinSensEqNorm,
                          store_hst=Name)
                    else:
                        fOpt, xOpt, inform = OptAlg(OptProb, sens_type=MaxSensEqNorm,
                          store_hst=Name)
                else:
                    if Name[-3:] == 'Min':
                        fOpt, xOpt, inform = OptAlg(OptProb, sens_type=MinSensEq,
                          store_hst=Name)
                    else:
                        fOpt, xOpt, inform = OptAlg(OptProb, sens_type=MaxSensEq,
                          store_hst=Name)
            else:
                fOpt, xOpt, inform = OptAlg(OptProb, sens_type=SensCalc, sens_step=deltax,
                  store_hst=Name)
        else:
            if Alg[:5] == 'PyGMO':
                import PyGMO
                from PyGMO.problem import base
                ngen = 50
                nindiv = 10
                dim = np.size(x0)
                prob = OptSysEqPyGMO(SysEq=SysEq, xL=xL, xU=xU, gc=gc, dim=dim)
                if Alg[6:] in ('de', 'bee_colony', 'nsga_II', 'pso', 'pso_gen', 'cmaes',
                               'py_cmaes', 'spea2', 'nspso', 'pade', 'sea', 'vega',
                               'sga', 'sga_gray', 'de_1220', 'mde_pbx', 'jde'):
                    algo = eval('PyGMO.algorithm.' + Alg[6:] + '(gen=ngen)')
                else:
                    if Alg[6:] in ('ihs', 'monte_carlo', 'sa_corana'):
                        algo = eval('PyGMO.algorithm.' + Alg[6:] + '(iter=ngen)')
                    else:
                        if Alg[6:] == 'sms_emoa':
                            print('sms_emoa not working')
                if Alg is 'PyGMO_de':
                    algo = PyGMO.algorithm.de(gen=ngen, f=1, cr=1, variant=2, ftol=0.001,
                      xtol=0.001,
                      screen_output=False)
                isl = PyGMO.island(algo, prob, nindiv)
                isl.evolve(1)
                isl.join()
                xOpt = isl.population.champion.x
                fOpt = isl.population.champion.f[0]
                nEval = isl.population.problem.fevals
                n_threads = 4
                xIter = []
            else:
                fOpt, xOpt, inform = OptAlg(OptProb, store_hst=Name)
            return (
             fOpt, xOpt)

    def OptAlgOptions(Alg, alphaLevelOptAlg):
        if Alg == 'MMA':
            alphaLevelOptAlg.setOption('GEPS', epsStop)
            alphaLevelOptAlg.setOption('DABOBJ', epsStop)
            alphaLevelOptAlg.setOption('DELOBJ', epsStop)
            alphaLevelOptAlg.setOption('ITRM', 1)
            alphaLevelOptAlg.setOption('MAXIT', 30)
        else:
            if Alg == 'GCMMA':
                alphaLevelOptAlg.setOption('GEPS', epsStop)
                alphaLevelOptAlg.setOption('DABOBJ', epsStop)
                alphaLevelOptAlg.setOption('DELOBJ', epsStop)
                alphaLevelOptAlg.setOption('ITRM', 1)
                alphaLevelOptAlg.setOption('MAXIT', 30)
                alphaLevelOptAlg.setOption('INNMAX', 5)
            else:
                if Alg == 'SLSQP':
                    alphaLevelOptAlg.setOption('ACC', epsStop)
                    alphaLevelOptAlg.setOption('MAXIT', 50)
                else:
                    if Alg == 'NLPQLP':
                        alphaLevelOptAlg.setOption('ACC', epsStop)
                        alphaLevelOptAlg.setOption('ACCQP', epsStop)
                        alphaLevelOptAlg.setOption('STPMIN', epsStop)
                        alphaLevelOptAlg.setOption('MAXFUN', 5)
                        alphaLevelOptAlg.setOption('MAXIT', 50)
                        alphaLevelOptAlg.setOption('RHOB', 0.0)
                        alphaLevelOptAlg.setOption('MODE', 0)
                        alphaLevelOptAlg.setOption('LQL', True)
                    else:
                        if Alg == 'PSQP':
                            alphaLevelOptAlg.setOption('XMAX', 10.0)
                            alphaLevelOptAlg.setOption('TOLX', epsStop)
                            alphaLevelOptAlg.setOption('TOLC', epsStop)
                            alphaLevelOptAlg.setOption('TOLG', epsStop)
                            alphaLevelOptAlg.setOption('RPF', epsStop)
                            alphaLevelOptAlg.setOption('MIT', 350)
                            alphaLevelOptAlg.setOption('MFV', 1000)
                            alphaLevelOptAlg.setOption('MET', 1)
                            alphaLevelOptAlg.setOption('MEC', 2)
                        else:
                            if Alg == 'COBYLA':
                                alphaLevelOptAlg.setOption('RHOBEG', 0.25)
                                alphaLevelOptAlg.setOption('RHOEND', epsStop)
                                alphaLevelOptAlg.setOption('MAXFUN', 15000)
                            else:
                                if Alg == 'CONMIN':
                                    alphaLevelOptAlg.setOption('ITMAX', 500)
                                    alphaLevelOptAlg.setOption('DELFUN', epsStop)
                                    alphaLevelOptAlg.setOption('DABFUN', epsStop)
                                    alphaLevelOptAlg.setOption('ITRM', 2)
                                    alphaLevelOptAlg.setOption('NFEASCT', 20)
                                else:
                                    if Alg == 'KSOPT':
                                        alphaLevelOptAlg.setOption('ITMAX', 30)
                                        alphaLevelOptAlg.setOption('RDFUN', epsStop)
                                        alphaLevelOptAlg.setOption('RHOMIN', 5.0)
                                        alphaLevelOptAlg.setOption('RHOMAX', 100.0)
                                    else:
                                        if Alg == 'SOLVOPT':
                                            alphaLevelOptAlg.setOption('xtol', epsStop)
                                            alphaLevelOptAlg.setOption('ftol', epsStop)
                                            alphaLevelOptAlg.setOption('maxit', 30)
                                            alphaLevelOptAlg.setOption('gtol', epsStop)
                                            alphaLevelOptAlg.setOption('spcdil', 2.5)
                                        else:
                                            if Alg == 'ALGENCAN':
                                                alphaLevelOptAlg.setOption('epsfeas', epsStop)
                                                alphaLevelOptAlg.setOption('epsopt', epsStop)
                                            else:
                                                if Alg == 'NSGA2':
                                                    alphaLevelOptAlg.setOption('PopSize', 100)
                                                    alphaLevelOptAlg.setOption('maxGen', 10)
                                                    alphaLevelOptAlg.setOption('pCross_real', 0.6)
                                                    alphaLevelOptAlg.setOption('pMut_real', 0.2)
                                                    alphaLevelOptAlg.setOption('eta_c', 10.0)
                                                    alphaLevelOptAlg.setOption('eta_m', 20.0)
                                                    alphaLevelOptAlg.setOption('pCross_bin', 0.0)
                                                    alphaLevelOptAlg.setOption('pMut_bin', 0.0)
                                                    alphaLevelOptAlg.setOption('seed', 0.0)
                                                    alphaLevelOptAlg.setOption('PrintOut', 2)
                    if Alg == 'ALPSO':
                        alphaLevelOptAlg.setOption('SwarmSize', 20)
                        alphaLevelOptAlg.setOption('maxOuterIter', 10)
                        alphaLevelOptAlg.setOption('maxInnerIter', 5)
                        alphaLevelOptAlg.setOption('minInnerIter', 1)
                        alphaLevelOptAlg.setOption('dynInnerIter', 0)
                        alphaLevelOptAlg.setOption('stopCriteria', 1)
                        alphaLevelOptAlg.setOption('stopIters', 2)
                        alphaLevelOptAlg.setOption('etol', epsStop)
                        alphaLevelOptAlg.setOption('itol', epsStop)
                        alphaLevelOptAlg.setOption('rtol', epsStop)
                        alphaLevelOptAlg.setOption('atol', epsStop)
                        alphaLevelOptAlg.setOption('dtol', epsStop)
                        alphaLevelOptAlg.setOption('rinit', 1.0)
                        alphaLevelOptAlg.setOption('xinit', 0)
                        alphaLevelOptAlg.setOption('vinit', 1.0)
                        alphaLevelOptAlg.setOption('vmax', 2.0)
                        alphaLevelOptAlg.setOption('c1', 2.0)
                        alphaLevelOptAlg.setOption('c2', 1.0)
                        alphaLevelOptAlg.setOption('w1', 0.99)
                        alphaLevelOptAlg.setOption('w2', 0.55)
                        alphaLevelOptAlg.setOption('ns', 15)
                        alphaLevelOptAlg.setOption('nf', 5)
                        alphaLevelOptAlg.setOption('vcrazy', 0.0001)
                        alphaLevelOptAlg.setOption('HoodSize', 40)
                        alphaLevelOptAlg.setOption('HoodModel', 'gbest')
                        alphaLevelOptAlg.setOption('HoodSelf', 1)
                        alphaLevelOptAlg.setOption('Scaling', 1)
                    else:
                        if Alg == 'ALHSO':
                            alphaLevelOptAlg.setOption('hms', 5)
                            alphaLevelOptAlg.setOption('hmcr', 0.95)
                            alphaLevelOptAlg.setOption('par', 0.65)
                            alphaLevelOptAlg.setOption('dbw', 2000)
                            alphaLevelOptAlg.setOption('maxoutiter', 200)
                            alphaLevelOptAlg.setOption('maxinniter', 50)
                            alphaLevelOptAlg.setOption('stopcriteria', 0)
                            alphaLevelOptAlg.setOption('stopiters', 2)
                            alphaLevelOptAlg.setOption('etol', epsStop)
                            alphaLevelOptAlg.setOption('itol', epsStop)
                            alphaLevelOptAlg.setOption('rtol', epsStop)
                            alphaLevelOptAlg.setOption('atol', epsStop)
                            alphaLevelOptAlg.setOption('prtoutiter', 0)
                            alphaLevelOptAlg.setOption('prtinniter', 0)
                            alphaLevelOptAlg.setOption('xinit', 0)
                            alphaLevelOptAlg.setOption('rinit', 1.0)
                            alphaLevelOptAlg.setOption('seed', 0.0)
                            alphaLevelOptAlg.setOption('scaling', 1)
                        elif Alg == 'MIDACO':
                            alphaLevelOptAlg.setOption('ACC', epsStop)
                            alphaLevelOptAlg.setOption('ISEED', 3)
                            alphaLevelOptAlg.setOption('QSTART', 1)
                            alphaLevelOptAlg.setOption('AUTOSTOP', 0)
                            alphaLevelOptAlg.setOption('ORACLE', 0.0)
                            alphaLevelOptAlg.setOption('ANTS', 0)
                            alphaLevelOptAlg.setOption('KERNEL', 0)
                            alphaLevelOptAlg.setOption('CHARACTER', 0)
                            alphaLevelOptAlg.setOption('MAXEVAL', 10000)
                            alphaLevelOptAlg.setOption('MAXTIME', 100000.0)
        return alphaLevelOptAlg

    if SBFA is not False:
        nSamp = SBFA
        xL = pFuzz[:, nAlpha - 1, 0]
        xU = pFuzz[:, nAlpha - 1, 1]
        xTemp = np.ones(np.size(xL)) * 2
        xSampFF = pyDOE.fullfact(np.array(xTemp, dtype=int))
        xSampLH = pyDOE.lhs(np.size(xL), nSamp)
        xDoE_Norm = np.concatenate((xSampFF, xSampLH), axis=0)
        nSamp = np.size(xDoE_Norm, 0)
        rDoE = np.zeros([nSamp, nr])
        xDoE = np.zeros(np.shape(xDoE_Norm))
        for ii in range(nSamp):
            xDoE[ii] = denormalize(xDoE_Norm[ii].T, xL, xU)
            rDoEii = FuzzySysEq(xDoE[ii], para, nr)
            rDoE[ii, :] = rDoEii.T

        rDoEr = np.zeros(nSamp)
        gp_r = [[]] * nr
        for ii in range(nr):
            for iii in range(nSamp):
                rDoEii = rDoE[iii]
                rDoEr[iii] = rDoEii[ii]
                if Surr in ('poly1', 'poly2', 'poly3', 'poly4'):
                    gp_r[ii] = np.polyfit(rDoEr, xDoE, np.int(Surr[4]))
                elif Surr == 'Kriging':
                    gp_r[ii] = GaussianProcess(regr='quadratic', corr='cubic', theta0=0.1,
                      thetaL=0.0001,
                      thetaU=10.0,
                      optimizer='fmin_cobyla')
                    gp_r[ii].fit(xDoE, rDoEr)

        DoE_Data = {}
        DoE_Data['rDoE'] = xDoE
        DoE_Data['rDoE'] = rDoE
        output = open(FuzzyModel + '_DoE.pkl', 'wb')
        pickle.dump(DoE_Data, output)
        output.close()

        def Surrogate(x, ir):
            if Surr in ('poly1', 'poly2', 'poly3', 'poly4'):
                rii = [[]] * np.size(gp_r[ir], 0)
                r = gp_r[ir][0] * x ** 1 + gp_r[ir][2] * x ** 2 + gp_r[ir][2]
            else:
                if Surr == 'Kriging':
                    r = gp_r[ir].predict(x, eval_MSE=False)
            fail = 0
            return r

    rFuzz = np.zeros([nr, nAlpha, 2])
    ptilde = np.zeros([nr, np.size(pFuzz, 0), nAlpha, 2])
    SU = np.zeros([nr, np.size(pFuzz, 0) * 2, nAlpha, 2])
    lambdaR = np.zeros([nr, np.size(pFuzz, 0) * 2, nAlpha, 2])
    for ir in range(nr):
        for ialpha in reversed(range(nAlpha)):
            if np.size(pFuzz) == 2:
                xL = pFuzz[(ialpha, 0)]
                xU = pFuzz[(ialpha, 1)]
            else:
                xL = pFuzz[:, ialpha, 0]
                xU = pFuzz[:, ialpha, 1]
            if abs(np.sum(abs(xU - xL) / (xL + np.spacing(1)))) < 0.001:
                f, g, fail = MinSysEq(xL)
                rFuzz[(ir, ialpha, 0)] = f
                rFuzz[(ir, ialpha, 1)] = f
                pMin = xU
                pMax = xU
            else:
                if ialpha == nAlpha - 1:
                    x0min = (xU + xL) / 2
                    x0max = x0min
                else:
                    for jj in range(len(pMin)):
                        if abs(pMin[jj] - pFuzz[(jj, ialpha + 1, 0)]) / (pMax[jj] + np.spacing(1)) < 0.01:
                            x0min[jj] = pFuzz[(jj, ialpha, 0)]
                        if abs(pMin[jj] - pFuzz[(jj, ialpha + 1, 1)]) / (pMax[jj] + np.spacing(1)) < 0.01:
                            x0min[jj] = pFuzz[(jj, ialpha, 1)]

                    for jj in range(len(pMax)):
                        if abs(pMax[jj] - pFuzz[(jj, ialpha + 1, 0)]) / (pMax[jj] + np.spacing(1)) < 0.01:
                            x0max[jj] = pFuzz[(jj, ialpha, 0)]
                        if abs(pMax[jj] - pFuzz[(jj, ialpha + 1, 1)]) / (pMax[jj] + np.spacing(1)) < 0.01:
                            x0max[jj] = pFuzz[(jj, ialpha, 1)]

                Name = 'alphaOpt_p' + str(ir + 1) + '_alpha' + str(ialpha)
                if Alg == 'CMAES':
                    ResMin = cma.CMAEvolutionStrategy(x0min, 0.5, {'bounds': [xL, xU]}).optimize(MinSysEq, min_iterations=25, iterations=100, verb_disp=0)
                    ResMax = cma.CMAEvolutionStrategy(x0max, 0.5, {'bounds': [xL, xU]}).optimize(MaxSysEq, min_iterations=25, iterations=100, verb_disp=0)
                    rMin = ResMin[1]
                    pMin = ResMin[0]
                    rMax = ResMax[1]
                    pMax = ResMax[0]
                else:
                    if Alg == '2Step':
                        Alg = 'ALHSO'
                        alphaLevelOptAlg = eval('pyOpt.' + Alg + '()')
                        alphaLevelOptAlg = OptAlgOptions(Alg, alphaLevelOptAlg)
                        MinProb, MaxProb = DefineProb(x0min, x0max, xL, xU, FuzzyModel, paraNorm)
                        rMin, pMin = AlphaLevelOpt(MinProb, alphaLevelOptAlg, Alg, SensCalc, Name + 'Min')
                        rMax, pMax = AlphaLevelOpt(MaxProb, alphaLevelOptAlg, Alg, SensCalc, Name + 'Max')
                        Alg = 'NLPQLP'
                        alphaLevelOptAlg = eval('pyOpt.' + Alg + '()')
                        alphaLevelOptAlg = OptAlgOptions(Alg, alphaLevelOptAlg)
                        MinProb, MaxProb = DefineProb(pMin, pMax, xL, xU, FuzzyModel, paraNorm)
                        rMin, pMin = AlphaLevelOpt(MinProb, alphaLevelOptAlg, Alg, SensCalc, Name + 'Min')
                        rMax, pMax = AlphaLevelOpt(MaxProb, alphaLevelOptAlg, Alg, SensCalc, Name + 'Max')
                    else:
                        alphaLevelOptAlg = eval('pyOpt.' + Alg + '()')
                        alphaLevelOptAlg = OptAlgOptions(Alg, alphaLevelOptAlg)
                        MinProb, MaxProb = DefineProb(x0min, x0max, xL, xU, FuzzyModel, paraNorm)
                        rMin, pMin = AlphaLevelOpt(MinProb, alphaLevelOptAlg, Alg, SensCalc, Name + 'Min')
                        rMax, pMax = AlphaLevelOpt(MaxProb, alphaLevelOptAlg, Alg, SensCalc, Name + 'Max')
                    pMin = pMin[0:np.size(xL)]
                    pMax = pMax[0:np.size(xL)]
                    pMin = np.resize(pMin, [np.size(xL)])
                    pMax = np.resize(pMax, [np.size(xL)])
                    if paraNorm:
                        pMinNorm = pMin
                        pMaxNorm = pMax
                        pMin = denormalize(pMinNorm, xL, xU)
                        pMax = denormalize(pMaxNorm, xL, xU)
                    rMax = -rMax
                    rFuzz[(ir, ialpha, 0)] = rMin
                    rFuzz[(ir, ialpha, 1)] = rMax
                    ptilde[ir, :, ialpha, 0] = pMin
                    ptilde[ir, :, ialpha, 1] = pMax
                    if Alg in ('NLPQLP', 'SLSQP', 'MMA'):
                        SU[ir, :, ialpha, 0], lambdaR[ir, :, ialpha, 0] = ShadowUncertainty(Name + 'Min', pMin, xL, xU)
                        try:
                            SU[ir, :, ialpha, 0], lambdaR[ir, :, ialpha, 0] = ShadowUncertainty(Name + 'Min', pMin, xL, xU)
                            SU[ir, :, ialpha, 1], lambdaR[ir, :, ialpha, 1] = ShadowUncertainty(Name + 'Max', pMax, xL, xU)
                        except:
                            for jj in range(np.size(SU, 1)):
                                SU[(ir, jj, ialpha, 0)] = 0
                                SU[(ir, jj, ialpha, 1)] = 0

                    else:
                        SU = []

    OutputData = {}
    OutputData['pFuzz'] = ptilde
    OutputData['nEval'] = nEval
    OutputData['SU'] = SU
    OutputData['lambdaR'] = lambdaR
    return (rFuzz, OutputData)


def NormFuzzyNumber(pFuzz):
    pFuzzNorm = np.zeros(np.shape(pFuzz))
    for ii in range(np.size(pFuzz, 0)):
        pFuzzNorm[ii, :, :] = pFuzz[ii, :, :] / (pFuzz[(ii, 0, 0)] + pFuzz[(ii, 0, 1)]) / 2

    return pFuzzNorm


def FuzzyRobustness(pFuzz, rFuzz):
    nAlpha = np.size(pFuzz, 1)
    pFuzzNorm = NormFuzzyNumber(pFuzz)
    rFuzzNorm = NormFuzzyNumber(rFuzz)
    A_pFuzz = np.zeros([np.size(pFuzzNorm, 0), 1])
    A_rFuzz = np.zeros([np.size(rFuzzNorm, 0), 1])
    A_pFuzzNorm = np.zeros([np.size(pFuzzNorm, 0), 1])
    A_rFuzzNorm = np.zeros([np.size(rFuzzNorm, 0), 1])
    FuzzRobust = np.zeros([np.size(rFuzzNorm, 0), 1])
    mu = np.linspace(0, 1, nAlpha)
    mu1 = np.linspace(1, 0, nAlpha)
    ymu = [mu, mu1]
    ymu = np.resize(ymu, [nAlpha * 2])
    for ii in range(np.size(pFuzz, 0)):
        xVal = [
         pFuzz[ii, :, 0], pFuzz[ii, :, 1]] + np.min(pFuzz[ii, :, :])
        xVal = np.resize(xVal, [nAlpha * 2])
        A_pFuzz[ii] = np.abs(np.trapz(y=ymu, x=xVal))
        xValNorm = [pFuzzNorm[ii, :, 0], pFuzzNorm[ii, :, 1]]
        xValNorm = np.resize(xValNorm, [nAlpha * 2])
        A_pFuzzNorm[ii] = np.abs(np.trapz(y=ymu, x=xValNorm))

    Ap = np.sum(A_pFuzzNorm)
    for ii in range(np.size(rFuzz, 0)):
        xVal = [
         rFuzz[ii, :, 0], rFuzz[ii, :, 1]]
        xVal = np.resize(xVal, [nAlpha * 2])
        A_rFuzz[ii] = np.abs(np.trapz(y=ymu, x=xVal))
        xValNorm = [rFuzzNorm[ii, :, 0], rFuzzNorm[ii, :, 1]]
        xValNorm = np.resize(xValNorm, [nAlpha * 2])
        A_rFuzzNorm[ii] = np.abs(np.trapz(y=ymu, x=xValNorm))
        FuzzRobust[ii] = Ap / A_rFuzzNorm[ii]

    Ar = np.sum(A_rFuzzNorm)
    FuzzRobustSys = Ap / Ar
    return (FuzzRobust, FuzzRobustSys, A_rFuzzNorm, A_pFuzzNorm, A_rFuzz,
     A_pFuzz)


def FuzzyArea(pFuzz):
    nAlpha = np.size(pFuzz, 1)
    pFuzzNorm = NormFuzzyNumber(pFuzz)
    A_pFuzz = np.zeros([np.size(pFuzzNorm, 0), 1])
    A_pFuzzNorm = np.zeros([np.size(pFuzzNorm, 0), 1])
    mu = np.linspace(0, 1, nAlpha)
    mu1 = np.linspace(1, 0, nAlpha)
    ymu = [mu, mu1]
    ymu = np.resize(ymu, [nAlpha * 2])
    for ii in range(np.size(pFuzz, 0)):
        xVal = [
         pFuzz[ii, :, 0], pFuzz[ii, :, 1]] + np.min(pFuzz[ii, :, :])
        xVal = np.resize(xVal, [nAlpha * 2])
        A_pFuzz[ii] = np.abs(np.trapz(y=ymu, x=xVal))
        xValNorm = [pFuzzNorm[ii, :, 0], pFuzzNorm[ii, :, 1]]
        xValNorm = np.resize(xValNorm, [nAlpha * 2])
        A_pFuzzNorm[ii] = np.abs(np.trapz(y=ymu, x=xValNorm))

    return (
     A_pFuzz, A_pFuzzNorm)


def FuzzyRobust(Ap, Ar):
    ApSum = np.sum(Ap)
    ArSum = np.sum(Ar)
    FuzzRobustSys = ApSum / ArSum
    return FuzzRobustSys


def FuzzySensitivitiy(rFuzz, SP):
    n_r = np.size(SP, 0)
    n_p = np.size(SP, 1) / 2
    rFuzzDelta = np.zeros([n_r, n_p, np.size(rFuzz, -2), np.size(rFuzz, -1)])
    rFuzzNew = np.zeros([n_r, n_p, np.size(rFuzz, -2), np.size(rFuzz, -1)])
    A_rFuzzDelta = np.zeros([n_r, n_p])
    A_rFuzzNew = np.zeros([n_r, n_p])
    A_rFuzzDeltaNorm = np.zeros([n_r, n_p])
    A_rFuzzNewNorm = np.zeros([n_r, n_p])
    abc = np.zeros([1, n_p])
    abcNorm = np.zeros([1, n_p])
    for ir in range(n_r):
        for ip in range(n_p):
            rFuzzDelta[ir, ip, :, :] = -(SP[ir, ip, :, :] + SP[ir, ip + n_p, :, :])
            rFuzzNew[ir, ip, :, :] = rFuzz[ir, :, :] + rFuzzDelta[ir, ip, :, :]

        A_Delta, A_DeltaNorm = FuzzyArea(rFuzzDelta[ir, :, :, :])
        A_New, A_NewNorm = FuzzyArea(rFuzzNew[ir, :, :, :])
        A_rFuzzDelta[ir, :] = np.reshape(A_Delta, [n_p])
        A_rFuzzDeltaNorm[ir, :] = np.reshape(A_DeltaNorm, [n_p])
        A_rFuzzNew[ir, :] = np.reshape(A_New, [n_p])
        A_rFuzzNewNorm[ir, :] = np.reshape(A_NewNorm, [n_p])

    return (rFuzzNew, rFuzzDelta, A_rFuzzNew, A_rFuzzDelta, A_rFuzzNewNorm,
     A_rFuzzDeltaNorm)


def AssembleShadowUncertainty(SPalpha):
    n_r = np.shape(SPalpha)[0]
    n_p = np.shape(SPalpha)[1] / 2
    n_alpha = np.shape(SPalpha)[3]
    SU = np.zeros([n_r, n_p, n_alpha, 2])
    for i_r in range(n_r):
        for i_p in range(n_p):
            SU[i_r, i_p, :, :] = SPalpha[i_r, i_p, :, :] + SPalpha[i_r, i_p + n_p, :, :]

    return SU


def ShadowUncertaintyPrices(SP, SU):
    SUP = np.abs(SP * SU)
    return SUP


if __name__ == '__main__':
    PrintFuzzAnPy()
    print('Start FuzzAnPy from file containing system equations!')
    print('See documentation for further help.')