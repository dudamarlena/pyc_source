# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wehrle/opt/pyUngewiss/pyUngewiss/UncertainAnalysis.py
# Compiled at: 2019-08-28 07:20:33
# Size of source mod 2**32: 30231 bytes
"""
pyUngewiss - Python library for UNcertainty analysis in liGhtwEight dsiGn with
IntervalS and fuzzy numberS

Previously called FuzzAnPy, but now renamed to current name to represent
concentration beyond fuzzy numbers, making intervals default.

This is based on the following work:
Wehrle (2015) Design optimization of lightweight space-frame structures
considering crashworthiness and parameter uncertainty

TODO Check calculation of shadow uncertainty with DesOptPy!
Save convergence and further information
Pretty plots
Hook up with complicated example

TODO pyGMO
TODO shadow uncertainty
TODO shadow prices
"""
import pyUngewiss.UncertainNumber as UncertainNumber
from pyUngewiss.OptAlgOptions import AlgOptions
import pyOpt, cma, numpy as np
np.seterr(divide='ignore')
__title__ = 'Python library for UNcertainty analysis in liGhtwEight desiGn with IntervalS and fuzzy numberS'
__shorttitle__ = 'pyUngewiss'
__version__ = '1.0 - Initial public release'
__all__ = 'pyUngewiss'
__author__ = 'E. J. Wehrle'
__copyright__ = 'Copyright 2019: E. J. Wehrle'
__email__ = 'Erich.Wehrle(a)unibz.it'
__license__ = 'GNU General Public License v3.0'
__url__ = 'github.org/e-dub/pyUngewiss'

def printSplash():
    print('')
    print(__shorttitle__ + ' - ' + __title__)
    print('')
    print('Version:     ' + __version__)
    print('Internet:    ' + __url__)
    print('License:     ' + __license__)
    print('Copyright:   ' + __copyright__)
    print('')


class UncertainAnalysis(object):

    def __init__(self, SysEq=[], pUnc=[], SensEq=[]):
        self.SysEq = SysEq
        self.pUnc = pUnc
        self.SensEq = SensEq
        self.nr = 1
        self.Alg = 'NLPQLP'
        if not pUnc:
            self.nAlpha = 1
        else:
            if isinstance(pUnc, list):
                self.nAlpha = np.shape(pUnc[0].Value)[1]
            else:
                self.nAlpha = np.shape(pUnc.Value)[1]
        self.deltax = 0.01
        self.paraNorm = True
        self.para = []
        self.SBFA = False
        self.Surr = 'Kriging'
        self.SensCalc = 'FD'
        self.epsStop = 0.0001
        self.UncertainModel = 'UncertainSystem'
        self.PrintOut = True
        self.nEval = 0

    def calculate(self):
        if hasattr(self.SensEq, '__call__'):
            self.SensCalc = 'OptSensEq'

        def MinSysEq(x):
            x = np.array(x)
            if not self.SBFA:
                r = self.SysEq(x, self.para)
            else:
                r = Surrogate(x, ir)
            if self.Alg == 'MMA':
                g = np.array([0.0])
            else:
                g = []
            self.nEval += 1
            if np.size(r) > 1 or type(r) is list:
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
            drdx = self.SensEq(x, f, g, self.para)
            if self.Alg == 'MMA':
                dgdx = np.zeros([1, np.size(x)])
            else:
                dgdx = []
            if np.size(self.nr) > 1:
                dfdx = np.array(drdx)[:, ir].reshape([1, len(x)])
            else:
                dfdx = np.array(drdx).reshape([1, len(x)])
            fail = 0
            return (dfdx, dgdx, fail)

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
                    self.nx = 1
                else:
                    if np.size(x0min) > 1:
                        for ii in range(np.size(x0min)):
                            MinProb.addVar(('x' + str(ii + 1)), 'c', value=(x0minnorm[ii]), lower=0.0,
                              upper=1.0)
                            MaxProb.addVar(('x' + str(ii + 1)), 'c', value=(x0maxnorm[ii]), lower=0.0,
                              upper=1.0)

                        self.nx = ii + 1
            else:
                if DesVarNorm == 0:
                    MinProb = pyOpt.Optimization(OptModel, MinSysEq)
                    MaxProb = pyOpt.Optimization(OptModel, MaxSysEq)
                    if np.size(x0min) == 1:
                        MinProb.addVar('x', 'c', value=x0min, lower=xL, upper=xU)
                        MaxProb.addVar('x', 'c', value=x0max, lower=xL, upper=xU)
                        self.nx = 1
                    else:
                        if np.size(x0min) > 1:
                            for ii in range(np.size(x0min)):
                                MinProb.addVar(('x' + str(ii + 1)), 'c', value=(x0min[ii]), lower=(xL[ii]),
                                  upper=(xU[ii]))
                                MaxProb.addVar(('x' + str(ii + 1)), 'c', value=(x0max[ii]), lower=(xL[ii]),
                                  upper=(xU[ii]))

                            self.nx = ii + 1
                MinProb.addObj('f')
                MaxProb.addObj('f')
                if self.Alg == 'MMA':
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
            lambda_rp, blah0, blah1, blah2 = np.linalg.lstsq(xGradActive, (-dfdxOpt),
              rcond=None)
            if Name[(-1)] == 'x':
                lambda_rp *= -1
            elif self.paraNorm:
                if np.size(xL) == 1:
                    denorm = np.array([xU - xL, xU - xL])
                else:
                    denorm = np.concatenate((xU - xL, xU - xL), axis=0)
                SPrp = lambda_rp / denorm
            else:
                SPrp = lambda_rp
            return (
             SPrp, lambda_rp)

        def AlphaLevelOpt--- This code section failed: ---

 L. 228         0  LOAD_FAST                'Alg'
                2  LOAD_CONST               ('MMA', 'GCMMA', 'CONMIN', 'KSOPT', 'SLSQP', 'PSQP', 'KSOPT', 'SOLVOPT', 'ALGENCAN', 'NLPQLP')
                4  COMPARE_OP               in
                6  POP_JUMP_IF_FALSE   200  'to 200'

 L. 230         8  LOAD_FAST                'SensCalc'
               10  LOAD_STR                 'OptSensEq'
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_FALSE   174  'to 174'

 L. 231        16  LOAD_DEREF               'self'
               18  LOAD_ATTR                paraNorm
               20  POP_JUMP_IF_FALSE    98  'to 98'

 L. 232        22  LOAD_FAST                'Name'
               24  LOAD_CONST               -3
               26  LOAD_CONST               None
               28  BUILD_SLICE_2         2 
               30  BINARY_SUBSCR    
               32  LOAD_STR                 'Min'
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    60  'to 60'

 L. 233        38  LOAD_FAST                'OptAlg'
               40  LOAD_FAST                'OptProb'

 L. 234        42  LOAD_DEREF               'MinSensEqNorm'

 L. 235        44  LOAD_FAST                'Name'
               46  LOAD_CONST               ('sens_type', 'store_hst')
               48  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               50  UNPACK_SEQUENCE_3     3 
               52  STORE_FAST               'fOpt'
               54  STORE_FAST               'xOpt'
               56  STORE_FAST               'info'
               58  JUMP_ABSOLUTE       172  'to 172'
             60_0  COME_FROM            36  '36'

 L. 236        60  LOAD_FAST                'Name'
               62  LOAD_CONST               -3
               64  LOAD_CONST               None
               66  BUILD_SLICE_2         2 
               68  BINARY_SUBSCR    
               70  LOAD_STR                 'Max'
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_FALSE   172  'to 172'

 L. 237        76  LOAD_FAST                'OptAlg'
               78  LOAD_FAST                'OptProb'

 L. 238        80  LOAD_DEREF               'MaxSensEqNorm'

 L. 239        82  LOAD_FAST                'Name'
               84  LOAD_CONST               ('sens_type', 'store_hst')
               86  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               88  UNPACK_SEQUENCE_3     3 
               90  STORE_FAST               'fOpt'
               92  STORE_FAST               'xOpt'
               94  STORE_FAST               'info'
               96  JUMP_ABSOLUTE       198  'to 198'
             98_0  COME_FROM            20  '20'

 L. 241        98  LOAD_FAST                'Name'
              100  LOAD_CONST               -3
              102  LOAD_CONST               None
              104  BUILD_SLICE_2         2 
              106  BINARY_SUBSCR    
              108  LOAD_STR                 'Min'
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   136  'to 136'

 L. 242       114  LOAD_FAST                'OptAlg'
              116  LOAD_FAST                'OptProb'

 L. 243       118  LOAD_DEREF               'MinSensEq'

 L. 244       120  LOAD_FAST                'Name'
              122  LOAD_CONST               ('sens_type', 'store_hst')
              124  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              126  UNPACK_SEQUENCE_3     3 
              128  STORE_FAST               'fOpt'
              130  STORE_FAST               'xOpt'
              132  STORE_FAST               'info'
              134  JUMP_ABSOLUTE       198  'to 198'
            136_0  COME_FROM           112  '112'

 L. 245       136  LOAD_FAST                'Name'
              138  LOAD_CONST               -3
              140  LOAD_CONST               None
              142  BUILD_SLICE_2         2 
              144  BINARY_SUBSCR    
              146  LOAD_STR                 'Max'
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE   198  'to 198'

 L. 246       152  LOAD_FAST                'OptAlg'
              154  LOAD_FAST                'OptProb'

 L. 247       156  LOAD_DEREF               'MaxSensEq'

 L. 248       158  LOAD_FAST                'Name'
              160  LOAD_CONST               ('sens_type', 'store_hst')
              162  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              164  UNPACK_SEQUENCE_3     3 
              166  STORE_FAST               'fOpt'
              168  STORE_FAST               'xOpt'
              170  STORE_FAST               'info'
            172_0  COME_FROM            74  '74'
              172  JUMP_ABSOLUTE       218  'to 218'
            174_0  COME_FROM            14  '14'

 L. 250       174  LOAD_FAST                'OptAlg'
              176  LOAD_FAST                'OptProb'
              178  LOAD_FAST                'SensCalc'

 L. 251       180  LOAD_DEREF               'self'
              182  LOAD_ATTR                deltax

 L. 252       184  LOAD_FAST                'Name'
              186  LOAD_CONST               ('sens_type', 'sens_step', 'store_hst')
              188  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              190  UNPACK_SEQUENCE_3     3 
              192  STORE_FAST               'fOpt'
              194  STORE_FAST               'xOpt'
              196  STORE_FAST               'info'
            198_0  COME_FROM           150  '150'
              198  JUMP_FORWARD        218  'to 218'
            200_0  COME_FROM             6  '6'

 L. 255       200  LOAD_FAST                'OptAlg'
              202  LOAD_FAST                'OptProb'
              204  LOAD_FAST                'Name'
              206  LOAD_CONST               ('store_hst',)
              208  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              210  UNPACK_SEQUENCE_3     3 
              212  STORE_FAST               'fOpt'
              214  STORE_FAST               'xOpt'
              216  STORE_FAST               'info'
            218_0  COME_FROM           198  '198'

 L. 256       218  LOAD_FAST                'fOpt'
              220  LOAD_FAST                'xOpt'
              222  BUILD_TUPLE_2         2 
              224  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 224

        def OptAlgOptionsOld(Alg, alphaLevelOptAlg):
            if self.Alg == 'MMA':
                alphaLevelOptAlg.setOption('GEPS', self.epsStop)
                alphaLevelOptAlg.setOption('DABOBJ', self.epsStop)
                alphaLevelOptAlg.setOption('DELOBJ', self.epsStop)
                alphaLevelOptAlg.setOption('ITRM', 1)
                alphaLevelOptAlg.setOption('MAXIT', 30)
            else:
                if self.Alg == 'GCMMA':
                    alphaLevelOptAlg.setOption('GEPS', self.epsStop)
                    alphaLevelOptAlg.setOption('DABOBJ', self.epsStop)
                    alphaLevelOptAlg.setOption('DELOBJ', self.epsStop)
                    alphaLevelOptAlg.setOption('ITRM', 1)
                    alphaLevelOptAlg.setOption('MAXIT', 30)
                    alphaLevelOptAlg.setOption('INNMAX', 5)
                else:
                    if self.Alg == 'SLSQP':
                        alphaLevelOptAlg.setOption('ACC', self.epsStop)
                        alphaLevelOptAlg.setOption('MAXIT', 50)
                    else:
                        if self.Alg == 'NLPQLP':
                            alphaLevelOptAlg.setOption('ACC', self.epsStop)
                            alphaLevelOptAlg.setOption('ACCQP', self.epsStop)
                            alphaLevelOptAlg.setOption('STPMIN', self.epsStop)
                            alphaLevelOptAlg.setOption('MAXFUN', 5)
                            alphaLevelOptAlg.setOption('MAXIT', 50)
                            alphaLevelOptAlg.setOption('RHOB', 0.0)
                            alphaLevelOptAlg.setOption('MODE', 0)
                            alphaLevelOptAlg.setOption('LQL', True)
                        else:
                            if self.Alg == 'PSQP':
                                alphaLevelOptAlg.setOption('XMAX', 10.0)
                                alphaLevelOptAlg.setOption('TOLX', self.epsStop)
                                alphaLevelOptAlg.setOption('TOLC', self.epsStop)
                                alphaLevelOptAlg.setOption('TOLG', self.epsStop)
                                alphaLevelOptAlg.setOption('RPF', self.epsStop)
                                alphaLevelOptAlg.setOption('MIT', 350)
                                alphaLevelOptAlg.setOption('MFV', 1000)
                                alphaLevelOptAlg.setOption('MET', 1)
                                alphaLevelOptAlg.setOption('MEC', 2)
                            else:
                                if self.Alg == 'COBYLA':
                                    alphaLevelOptAlg.setOption('RHOBEG', 0.25)
                                    alphaLevelOptAlg.setOption('RHOEND', self.epsStop)
                                    alphaLevelOptAlg.setOption('MAXFUN', 15000)
                                else:
                                    if self.Alg == 'CONMIN':
                                        alphaLevelOptAlg.setOption('ITMAX', 500)
                                        alphaLevelOptAlg.setOption('DELFUN', self.epsStop)
                                        alphaLevelOptAlg.setOption('DABFUN', self.epsStop)
                                        alphaLevelOptAlg.setOption('ITRM', 2)
                                        alphaLevelOptAlg.setOption('NFEASCT', 20)
                                    else:
                                        if self.Alg == 'KSOPT':
                                            alphaLevelOptAlg.setOption('ITMAX', 30)
                                            alphaLevelOptAlg.setOption('RDFUN', self.epsStop)
                                            alphaLevelOptAlg.setOption('RHOMIN', 5.0)
                                            alphaLevelOptAlg.setOption('RHOMAX', 100.0)
                                        else:
                                            if self.Alg == 'SOLVOPT':
                                                alphaLevelOptAlg.setOption('xtol', self.epsStop)
                                                alphaLevelOptAlg.setOption('ftol', self.epsStop)
                                                alphaLevelOptAlg.setOption('maxit', 30)
                                                alphaLevelOptAlg.setOption('gtol', self.epsStop)
                                                alphaLevelOptAlg.setOption('spcdil', 2.5)
                                            else:
                                                if self.Alg == 'ALGENCAN':
                                                    alphaLevelOptAlg.setOption('epsfeas', self.epsStop)
                                                    alphaLevelOptAlg.setOption('epsopt', self.epsStop)
                                                else:
                                                    if self.Alg == 'NSGA2':
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
                                                    if self.Alg == 'ALPSO':
                                                        alphaLevelOptAlg.setOption('SwarmSize', 20)
                                                        alphaLevelOptAlg.setOption('maxOuterIter', 10)
                                                        alphaLevelOptAlg.setOption('maxInnerIter', 5)
                                                        alphaLevelOptAlg.setOption('minInnerIter', 1)
                                                        alphaLevelOptAlg.setOption('dynInnerIter', 0)
                                                        alphaLevelOptAlg.setOption('stopCriteria', 1)
                                                        alphaLevelOptAlg.setOption('stopIters', 2)
                                                        alphaLevelOptAlg.setOption('etol', self.epsStop)
                                                        alphaLevelOptAlg.setOption('itol', self.epsStop)
                                                        alphaLevelOptAlg.setOption('rtol', self.epsStop)
                                                        alphaLevelOptAlg.setOption('atol', self.epsStop)
                                                        alphaLevelOptAlg.setOption('dtol', self.epsStop)
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
                                                        if self.Alg == 'ALHSO':
                                                            alphaLevelOptAlg.setOption('hms', 5)
                                                            alphaLevelOptAlg.setOption('hmcr', 0.95)
                                                            alphaLevelOptAlg.setOption('par', 0.65)
                                                            alphaLevelOptAlg.setOption('dbw', 2000)
                                                            alphaLevelOptAlg.setOption('maxoutiter', 200)
                                                            alphaLevelOptAlg.setOption('maxinniter', 50)
                                                            alphaLevelOptAlg.setOption('stopcriteria', 0)
                                                            alphaLevelOptAlg.setOption('stopiters', 2)
                                                            alphaLevelOptAlg.setOption('etol', self.epsStop)
                                                            alphaLevelOptAlg.setOption('itol', self.epsStop)
                                                            alphaLevelOptAlg.setOption('rtol', self.epsStop)
                                                            alphaLevelOptAlg.setOption('atol', self.epsStop)
                                                            alphaLevelOptAlg.setOption('prtoutiter', 0)
                                                            alphaLevelOptAlg.setOption('prtinniter', 0)
                                                            alphaLevelOptAlg.setOption('xinit', 0)
                                                            alphaLevelOptAlg.setOption('rinit', 1.0)
                                                            alphaLevelOptAlg.setOption('seed', 0.0)
                                                            alphaLevelOptAlg.setOption('scaling', 1)
                                                        else:
                                                            if self.Alg == 'MIDACO':
                                                                alphaLevelOptAlg.setOption('ACC', self.epsStop)
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

        rUnc = np.zeros([self.nr, self.nAlpha, 2])
        if type(self.pUnc) is list:
            pUnc = np.zeros((len(self.pUnc), self.nAlpha, 2))
            for i, val in enumerate(self.pUnc):
                if type(val) == np.ndarray:
                    pUnc[i] = val
                elif type(val) == UncertainNumber:
                    pUnc[i] = val.Value
                else:
                    if type(self.pUnc) == UncertainNumber:
                        pUnc = self.pUnc.Value

        else:
            pUnc = np.zeros((1, self.nAlpha, 2))
            pUnc[0, :, :] = self.pUnc.Value
        ptilde = np.zeros([self.nr, np.size(pUnc, 0), self.nAlpha, 2])
        SU = np.zeros([self.nr, np.size(pUnc, 0) * 2, self.nAlpha, 2])
        lambdaR = np.zeros([self.nr, np.size(pUnc, 0) * 2, self.nAlpha, 2])
        for ir in range(self.nr):
            for ialpha in reversed(range(self.nAlpha)):
                xL = pUnc[:, ialpha, 0]
                xU = pUnc[:, ialpha, 1]
                if abs(np.sum(abs(xU - xL) / (xL + np.spacing(1)))) < 0.001:
                    f, g, fail = MinSysEq(xL)
                    rUnc[(ir, ialpha, 0)] = f
                    rUnc[(ir, ialpha, 1)] = f
                    pMin = xU
                    pMax = xU
                else:
                    if ialpha == self.nAlpha - 1:
                        x0min = (xU + xL) / 2
                        x0max = x0min
                    else:
                        for j, val in enumerate(pMin):
                            if abs(val - pUnc[(j, ialpha + 1, 0)]) / (pMax[j] + np.spacing(1)) < 0.01:
                                x0min[j] = pUnc[(j, ialpha, 0)]
                            if abs(val - pUnc[(j, ialpha + 1, 1)]) / (pMax[j] + np.spacing(1)) < 0.01:
                                x0min[j] = pUnc[(j, ialpha, 1)]

                        for j, val in enumerate(pMax):
                            if abs(val - pUnc[(j, ialpha + 1, 0)]) / (pMax[j] + np.spacing(1)) < 0.01:
                                x0max[j] = pUnc[(j, ialpha, 0)]
                            if abs(val - pUnc[(j, ialpha + 1, 1)]) / (pMax[j] + np.spacing(1)) < 0.01:
                                x0max[j] = pUnc[(j, ialpha, 1)]

                    Name = 'alphaOpt_p' + str(ir + 1) + '_alpha' + str(ialpha)
                    if self.Alg == 'CMAES':
                        ResMin = cma.CMAEvolutionStrategy(x0min, 0.5, {'bounds': [xL, xU]}).optimize(MinSysEq, min_iterations=25,
                          iterations=100,
                          verb_disp=0)
                        ResMax = cma.CMAEvolutionStrategy(x0max, 0.5, {'bounds': [xL, xU]}).optimize(MaxSysEq, min_iterations=25,
                          iterations=100,
                          verb_disp=0)
                        rMin = ResMin[1]
                        pMin = ResMin[0]
                        rMax = ResMax[1]
                        pMax = ResMax[0]
                    else:
                        if self.Alg == '2Step':
                            self.Alg = 'ALHSO'
                            alphaLevelOptAlg = eval('pyOpt.' + self.Alg + '()')
                            alphaLevelOptAlg = AlgOptions(alphaLevelOptAlg, self.Alg, self.epsStop)
                            MinProb, MaxProb = DefineProb(x0min, x0max, xL, xU, self.UncertainModel, self.paraNorm)
                            rMin, pMin = AlphaLevelOpt(MinProb, alphaLevelOptAlg, self.Alg, self.SensCalc, Name + 'Min')
                            rMax, pMax = AlphaLevelOpt(MaxProb, alphaLevelOptAlg, self.Alg, self.SensCalc, Name + 'Max')
                            self.Alg = 'NLPQLP'
                            alphaLevelOptAlg = eval('pyOpt.' + self.Alg + '()')
                            alphaLevelOptAlg = AlgOptions(alphaLevelOptAlg, self.Alg, self.epsStop)
                            MinProb, MaxProb = DefineProb(pMin, pMax, xL, xU, self.UncertainModel, self.paraNorm)
                            rMin, pMin = AlphaLevelOpt(MinProb, alphaLevelOptAlg, self.Alg, self.SensCalc, Name + 'Min')
                            rMax, pMax = AlphaLevelOpt(MaxProb, alphaLevelOptAlg, self.Alg, self.SensCalc, Name + 'Max')
                        else:
                            alphaLevelOptAlg = eval('pyOpt.' + self.Alg + '()')
                            alphaLevelOptAlg = AlgOptions(alphaLevelOptAlg, self.Alg, self.epsStop)
                            MinProb, MaxProb = DefineProb(x0min, x0max, xL, xU, self.UncertainModel, self.paraNorm)
                            rMin, pMin = AlphaLevelOpt(MinProb, alphaLevelOptAlg, self.Alg, self.SensCalc, Name + 'Min')
                            rMax, pMax = AlphaLevelOpt(MaxProb, alphaLevelOptAlg, self.Alg, self.SensCalc, Name + 'Max')
                    pMin = pMin[0:np.size(xL)]
                    pMax = pMax[0:np.size(xL)]
                    pMin = np.resize(pMin, [np.size(xL)])
                    pMax = np.resize(pMax, [np.size(xL)])
                    if self.paraNorm:
                        pMinNorm = pMin
                        pMaxNorm = pMax
                        pMin = denormalize(pMinNorm, xL, xU)
                        pMax = denormalize(pMaxNorm, xL, xU)
                    rMax = -rMax
                    rUnc[(ir, ialpha, 0)] = rMin
                    rUnc[(ir, ialpha, 1)] = rMax
                    ptilde[ir, :, ialpha, 0] = pMin
                    ptilde[ir, :, ialpha, 1] = pMax
                    if self.Alg in ('NLPQLP', 'SLSQP', 'MMA'):
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
        OutputData['pUnc'] = ptilde
        OutputData['nEval'] = self.nEval
        OutputData['lambdaR'] = lambdaR
        self.SU = SU
        if self.nr > 1:
            self.rUnc = [[]] * len(rUnc)
            for i, val in enumerate(rUnc):
                self.rUnc[i] = UncertainNumber(val, Form='empirical', nalpha=(self.nAlpha))

        else:
            self.rUnc = UncertainNumber((rUnc[0]), Form='empirical', nalpha=(self.nAlpha))
        self.OutputData = OutputData

    def calcRobustness--- This code section failed: ---

 L. 536         0  LOAD_CONST               0
                2  LOAD_FAST                'self'
                4  STORE_ATTR               pAreaSum

 L. 537         6  LOAD_CONST               0
                8  LOAD_FAST                'self'
               10  STORE_ATTR               pAreaNormSum

 L. 538        12  LOAD_CONST               0
               14  LOAD_FAST                'self'
               16  STORE_ATTR               rAreaSum

 L. 539        18  LOAD_CONST               0
               20  LOAD_FAST                'self'
               22  STORE_ATTR               rAreaNormSum

 L. 540        24  LOAD_GLOBAL              type
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                pUnc
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  LOAD_GLOBAL              list
               34  COMPARE_OP               is
               36  POP_JUMP_IF_FALSE    96  'to 96'

 L. 541        38  SETUP_LOOP          140  'to 140'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                pUnc
               44  GET_ITER         
               46  FOR_ITER             92  'to 92'
               48  STORE_FAST               'val'

 L. 542        50  LOAD_FAST                'val'
               52  LOAD_METHOD              calcArea
               54  CALL_METHOD_0         0  '0 positional arguments'
               56  POP_TOP          

 L. 543        58  LOAD_FAST                'self'
               60  DUP_TOP          
               62  LOAD_ATTR                pAreaSum
               64  LOAD_FAST                'val'
               66  LOAD_ATTR                Area
               68  INPLACE_ADD      
               70  ROT_TWO          
               72  STORE_ATTR               pAreaSum

 L. 544        74  LOAD_FAST                'self'
               76  DUP_TOP          
               78  LOAD_ATTR                pAreaNormSum
               80  LOAD_FAST                'val'
               82  LOAD_ATTR                AreaNorm
               84  INPLACE_ADD      
               86  ROT_TWO          
               88  STORE_ATTR               pAreaNormSum
               90  JUMP_BACK            46  'to 46'
               92  POP_BLOCK        
               94  JUMP_FORWARD        140  'to 140'
             96_0  COME_FROM            36  '36'

 L. 545        96  LOAD_GLOBAL              type
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                pUnc
              102  CALL_FUNCTION_1       1  '1 positional argument'
              104  LOAD_GLOBAL              UncertainNumber
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   140  'to 140'

 L. 546       110  LOAD_FAST                'self'
              112  LOAD_ATTR                pUnc
              114  LOAD_METHOD              calcArea
              116  CALL_METHOD_0         0  '0 positional arguments'
              118  POP_TOP          

 L. 547       120  LOAD_FAST                'self'
              122  LOAD_ATTR                pUnc
              124  LOAD_ATTR                Area
              126  LOAD_FAST                'self'
              128  STORE_ATTR               pAreaSum

 L. 548       130  LOAD_FAST                'self'
              132  LOAD_ATTR                pUnc
              134  LOAD_ATTR                AreaNorm
              136  LOAD_FAST                'self'
              138  STORE_ATTR               pAreaNormSum
            140_0  COME_FROM           108  '108'
            140_1  COME_FROM            94  '94'
            140_2  COME_FROM_LOOP       38  '38'

 L. 549       140  LOAD_GLOBAL              type
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                rUnc
              146  CALL_FUNCTION_1       1  '1 positional argument'
              148  LOAD_GLOBAL              list
              150  COMPARE_OP               is
              152  POP_JUMP_IF_FALSE   212  'to 212'

 L. 550       154  SETUP_LOOP          258  'to 258'
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                rUnc
              160  GET_ITER         
              162  FOR_ITER            208  'to 208'
              164  STORE_FAST               'val'

 L. 551       166  LOAD_FAST                'val'
              168  LOAD_METHOD              calcArea
              170  CALL_METHOD_0         0  '0 positional arguments'
              172  POP_TOP          

 L. 552       174  LOAD_FAST                'self'
              176  DUP_TOP          
              178  LOAD_ATTR                rAreaSum
              180  LOAD_FAST                'val'
              182  LOAD_ATTR                Area
              184  INPLACE_ADD      
              186  ROT_TWO          
              188  STORE_ATTR               rAreaSum

 L. 553       190  LOAD_FAST                'self'
              192  DUP_TOP          
              194  LOAD_ATTR                rAreaNormSum
              196  LOAD_FAST                'val'
              198  LOAD_ATTR                AreaNorm
              200  INPLACE_ADD      
              202  ROT_TWO          
              204  STORE_ATTR               rAreaNormSum
              206  JUMP_BACK           162  'to 162'
              208  POP_BLOCK        
              210  JUMP_FORWARD        258  'to 258'
            212_0  COME_FROM           152  '152'

 L. 554       212  LOAD_GLOBAL              type
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                rUnc
              218  CALL_FUNCTION_1       1  '1 positional argument'
              220  LOAD_GLOBAL              UncertainNumber
              222  COMPARE_OP               ==
          224_226  POP_JUMP_IF_FALSE   258  'to 258'

 L. 555       228  LOAD_FAST                'self'
              230  LOAD_ATTR                rUnc
              232  LOAD_METHOD              calcArea
              234  CALL_METHOD_0         0  '0 positional arguments'
              236  POP_TOP          

 L. 556       238  LOAD_FAST                'self'
              240  LOAD_ATTR                rUnc
              242  LOAD_ATTR                Area
              244  LOAD_FAST                'self'
              246  STORE_ATTR               rAreaSum

 L. 557       248  LOAD_FAST                'self'
              250  LOAD_ATTR                rUnc
              252  LOAD_ATTR                AreaNorm
              254  LOAD_FAST                'self'
              256  STORE_ATTR               rAreaNormSum
            258_0  COME_FROM           224  '224'
            258_1  COME_FROM           210  '210'
            258_2  COME_FROM_LOOP      154  '154'

 L. 558       258  LOAD_GLOBAL              np
              260  LOAD_METHOD              divide
              262  LOAD_FAST                'self'
              264  LOAD_ATTR                pAreaSum
              266  LOAD_FAST                'self'
              268  LOAD_ATTR                rAreaSum
              270  CALL_METHOD_2         2  '2 positional arguments'
              272  LOAD_FAST                'self'
              274  STORE_ATTR               SystemRobustness

 L. 559       276  LOAD_GLOBAL              np
              278  LOAD_METHOD              divide
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                pAreaNormSum

 L. 560       284  LOAD_FAST                'self'
              286  LOAD_ATTR                rAreaNormSum
              288  CALL_METHOD_2         2  '2 positional arguments'
              290  LOAD_FAST                'self'
              292  STORE_ATTR               SystemRobustnessNorm

Parse error at or near `COME_FROM_LOOP' instruction at offset 140_2


def FuzzySensitivitiy(rUnc, SP):
    n_r = np.size(SP, 0)
    n_p = np.size(SP, 1) / 2
    rUncDelta = np.zeros([n_r, n_p, np.size(rUnc, -2), np.size(rUnc, -1)])
    rUncNew = np.zeros([n_r, n_p, np.size(rUnc, -2), np.size(rUnc, -1)])
    A_rUncDelta = np.zeros([n_r, n_p])
    A_rUncNew = np.zeros([n_r, n_p])
    A_rUncDeltaNorm = np.zeros([n_r, n_p])
    A_rUncNewNorm = np.zeros([n_r, n_p])
    abc = np.zeros([1, n_p])
    abcNorm = np.zeros([1, n_p])
    for ir in range(n_r):
        for ip in range(n_p):
            rUncDelta[ir, ip, :, :] = -(SP[ir, ip, :, :] + SP[ir, ip + n_p, :, :])
            rUncNew[ir, ip, :, :] = rUnc[ir, :, :] + rUncDelta[ir, ip, :, :]

        A_Delta, A_DeltaNorm = FuzzyArea(rUncDelta[ir, :, :, :])
        A_New, A_NewNorm = FuzzyArea(rUncNew[ir, :, :, :])
        A_rUncDelta[ir, :] = np.reshape(A_Delta, [n_p])
        A_rUncDeltaNorm[ir, :] = np.reshape(A_DeltaNorm, [n_p])
        A_rUncNew[ir, :] = np.reshape(A_New, [n_p])
        A_rUncNewNorm[ir, :] = np.reshape(A_NewNorm, [n_p])

    return (rUncNew, rUncDelta, A_rUncNew, A_rUncDelta, A_rUncNewNorm,
     A_rUncDeltaNorm)


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
    printSplash()
    print('Start FuzzAnPy from file containing system equations!')
    print('See documentation for further help.')
    print()
    print('Quick test 1')
    print('--------------------------------------------------')
    print()
    pInt = UncertainNumber([1, 5])

    def SysEq1(p, x):
        return p - p


    UncertainProblem = UncertainAnalysis()
    UncertainProblem.pUnc = pInt
    UncertainProblem.SysEq = SysEq1
    UncertainProblem.calculate()
    print('rUnc = pUnc - pUnc')
    print('rUnc = ' + str(UncertainProblem.rUnc.Value))
    UncertainProblem.calcRobustness()
    print('Quick test 2')
    print('--------------------------------------------------')
    print()
    from scipy.optimize import rosen, rosen_der

    def SysEq2(p, x):
        return rosen(p)


    def SensEq2(p, r, g, x):
        return rosen_der(p)


    nAlpha = 3
    pFuzz = [[]] * 2
    pFuzz[0] = UncertainNumber([1, 2, 3, 4], Form='trapazoid', nalpha=nAlpha)
    pFuzz[1] = UncertainNumber([1, 2, 3, 4], Form='trapazoid', nalpha=nAlpha)
    Prob = UncertainAnalysis(SysEq2, pUnc=pFuzz, SensEq=SensEq2)
    Prob.Alg = 'NLPQLP'
    Prob.nAlpha = nAlpha
    Prob.paraNorm = 0
    Prob.epsStop = 1e-06
    Prob.para = 1
    Prob.calculate()
    print('rUnc = ' + str(Prob.rUnc.Value))