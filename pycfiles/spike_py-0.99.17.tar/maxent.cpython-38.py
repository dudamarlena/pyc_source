# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/Algo/maxent.py
# Compiled at: 2018-03-07 03:29:07
# Size of source mod 2**32: 23394 bytes
"""
maxent.py

Created by Marc-André on 2012-03-06.
Copyright (c) 2012 IGBMC. All rights reserved.
"""
from __future__ import print_function
import sys, os, math, numpy as np, scipy, scipy.optimize, unittest
from util.counter import counting, timeit
from ..Display import testplot
plt = testplot.plot()
__version__ = 0.3
__date__ = 'march 2013'

def br():
    plt.show()
    os._exit(0)


def initial_scene_delta(size=100, sc=1.0):
    """draw test scene"""
    Ideal = np.zeros((size,))
    Ideal[25] = sc
    return Ideal


def initial_scene_2delta(size=100, sc=1.0):
    """draw test scene"""
    Ideal = np.zeros((size,))
    Ideal[25] = sc
    Ideal[40] = sc
    return Ideal


def initial_scene(size=100, sc=1.0):
    """draw test scene"""
    Ideal = np.zeros((size,))
    Ideal[15] = 5 * sc
    for i in range(10):
        Ideal[i + 30] = sc
    else:
        for i in range(20):
            Ideal[i + 65] = i * sc / 20.0
        else:
            return Ideal


figdef = 0

def plot(buf, text=None, fig=0, logy=False):
    """plot with a text and return the figure number"""
    global figdef
    if fig == 0:
        figdef += 1
        lfig = figdef
    else:
        lfig = fig
    plt.figure(lfig)
    if logy:
        plt.semilogy(buf, label=text)
    else:
        plt.plot(buf, label=text)
    if text:
        if fig == 0:
            plt.title(text)
    plt.legend()
    return lfig


def estimate_SNR(estim_s, true_s):
    err = true_s - estim_s
    return 10 * np.log10(sum(abs(true_s) ** 2) / sum(abs(err) ** 2))


class ExpData(object):
    __doc__ = '\n    Implement an experimental data to be analysed\n    Combined with the definition of the transform ( TransferFunction ), defines the scene for the MaxEnt solver\n    '

    def __init__(self, data):
        """
        defines
        data : an array that contains the experimental data
        noise : the value of the noise, in the same unit as data
        window : allows to define error on data for each data point - initialized to 1.0
                error in data[i] is noise/window[i]
        """
        self.data = data
        self.window = np.ones(data.shape)
        self.noise = 0


class TransferFunction(object):
    __doc__ = " defines the transfert functions for a given problem to be solved by MaxEnt\n    data    <-- transform --  image         The experimental transfer function\n    data     -- t_transform -->  image      The transpose of `transform'\n\n    must implement\n        transform()         // defined above\n        t_transform()\n        init_transform()\n        norm                // the norm of the transform operator, defined as ||tr(x)|| / ||x||\n    "

    def __init__(self):
        """
        sets-up the default function, which should be overloaded by a sub classer
        """
        self.init_transform()

    def t_transform(self, datain):
        """
        default method for transform
        here, simple convolution by a 5 pixel rectangle
        """
        return np.convolve(datain, (self.convol_kernel), mode='full')

    def transform(self, datain):
        """
        default method for transform
        here, simple convolution by a 5 pixel rectangle
        """
        return np.convolve(datain, (self.convol_kernel), mode='valid')

    def init_transform(self, size=5):
        """each transform/ttransform pair should have its initialisation code"""
        k = np.concatenate((np.arange(float(size)), np.arange(float(size))[::-1]))
        self.convol_kernel = k / np.sum(k)
        self.norm = 1.0


def entropy(F, sc):
    """
    compute the entropy of the ndarray a, given scaling value sc
    S =  sum of -Z(i)*LOG(Z(i)), where  Z(i) = a(i)/sc )
    """
    l = np.abs(F) / sc
    S = -np.sum(l * np.log(l))
    return S


def entropy_prior(F, A):
    """
    compute the entropy of the ndarray F, given a prior knowledge in ndarray A
    S =  - sum  [F(i) - A(i) + F(i)*LOG(F(i)/A(i)) ]
    """
    l = np.abs(F / A)
    S = -np.sum(F - A + F * np.log(l))
    return S


def d_entropy_Gifa(F, S, sc):
    """
    compute the derivative of entropy of the ndarray a, given entropy S and scaling value sc
    Gifa  : dS/dFi = -1/sc (S+log(Fi/A))
    """
    l = np.abs(F) / sc
    return (-S - np.log(l)) / sc


def d_entropy_Skilling(F, sc):
    """
    compute the derivative of entropy of the ndarray a, given entropy S and scaling value sc
    Skilling  : dS/dFi = -1/sc (1+log(Fi/A))
    """
    l = np.abs(F) / sc
    return -1.0 / sc * (1.0 + np.log(l))


def d_entropy_prior(F, A):
    """
    compute the derivative of entropy of the ndarray F, given a prior knowledge in ndarray A
    """
    return -np.log(F / A)


class MaxEnt(object):
    __doc__ = '\n    implements the Maximum Entropy solver\n    \n    given M \n    finds the minimum of Q = S(M) - lamb*Chi2(M)\n    with lamb such that Chi2(M) is normalized\n    '

    def __init__(self, transferfunction, expdata, iterations=10, debug=0):
        """
        initialize a MaxEnt minimiser
        
        sets expdata and transferfunction attributes from arguments
        
        expdata should be a ExpData instance
        transferfunction should be a TransferFunction instance
        
        debug == 0 : production code
        debug == 1 : display evolution
        debug == 2 : full debug        
        
        """
        self.debug = debug
        self.expdata = expdata
        if self.expdata.noise > 0:
            self.sigma = self.expdata.noise
        else:
            self.sigma = 0.01 * max(self.expdata.buffer)
        self.tf = transferfunction
        self.iterations = iterations
        self.setup()
        self.iter = 0
        self.lchi2 = []
        self.lentropy = []
        self.llamb = []
        tt = self.tf.t_transform(self.expdata.data)
        mm = max(tt) / tt.size
        self.image = mm * np.ones(tt.shape)
        self.sum = np.sum(self.image)
        if self.debug > 2:
            plot(self.image, 'image initiale')
        self.chi2 = self.do_chisquare((self.image), mode='none')
        self.S = self.do_entropy((self.image), mode='none')
        self.lamb = self.S / self.chi2
        self.true_s = None

    def report(self):
        """report internal state values"""
        for i in dir(self):
            att = getattr(self, i)
            if not callable(att):
                if not i.startswith('_'):
                    print('%s\t:\t%s' % (i, att))

    def setup(self, mode='default'):
        """ 
        Set-up internal MaxEnt parameters so that a kind of optimal state is given
        
        mode can be (case insensitive)
            "Descent"
            "Newton"
            "Gifa"
            "default"   : currently sets to Descent
        modifies (M the MaxEnt instance):
            M.algo M.exptang M.lambdacont M.lambdamax M.lambdasp M.miniter M.stepmax

        """
        if mode.lower() in ('descent', 'default'):
            self.algo = 'steepest'
            self.stepmax = 2.0
            self.miniter = 10
            self.exptang = 1.0
            self.chi2target = 1.0
            self.lambdacont = 'increment'
            self.lambdasp = 1.1
            self.lambdamax = 1.3
        else:
            if mode.lower() == 'gifa':
                self.algo = 'Gifa'
                self.stepmax = 2.0
                self.miniter = 10
                self.exptang = 0.0
                self.chi2target = 1.0
                self.lambdacont = 'cosine'
                self.lambdasp = 2.0
                self.lambdamax = 1.5
            else:
                raise Exception('Wrong mode in MaxEnt.setup()')

    def do_chisquare(self, image, mode='derivative'):
        """
        computes chi2 (scalar) and its derivative (array),
        computed between     the current image
                    and     self.expdata which is the experimental data
        returned as (chi2, dchi2)
        if mode != 'derivative'  then only chi2 is computed, and returned
        """
        residu = (self.tf.transform(image) - self.expdata.data) / self.sigma
        chi2 = np.dot(residu, residu) / residu.size
        if mode == 'derivative':
            dchi2 = 2.0 / residu.size * self.tf.t_transform(residu)
        if mode == 'derivative':
            return (
             chi2, dchi2)
        return chi2

    def do_entropy(self, image, mode='derivative'):
        """
        computes the entropy S (scalar) and its derivative (array),
        computed on image
        returned as (S, dS)
        if mode != 'derivative'  then only S is computed, and returned
        """
        S = entropy(image, self.sum)
        if mode == 'derivative':
            dS = d_entropy_Gifa(self.image, S, self.sum)
            return (S, dS)
        return S

    def Q(self, im):
        """
        the Q function returns the value of -Q for a given image
        -Q so that it can be minimized
        """
        imclp = im.clip(1e-08)
        S = self.do_entropy(imclp, mode='entropy')
        Chi2 = self.do_chisquare(imclp, mode='Chi2')
        Q = S - self.lamb * Chi2
        if self.debug > 2:
            print('in Qfunc     S=%f, Chi2=%f,  Q=%f' % (S, Chi2, Q))
        return -Q

    def sexp(self, x):
        """
        a local and linearized version of the exponential
        exptang is the tangent point
        """
        return np.where(x < self.exptang, np.exp(x), math.exp(self.exptang) * (x + 1.0 - self.exptang))

    def drive_conv(self, dchi, dS):
        """
        returns (conv, lambda_optim)
        given the derivative dchi and dS, and the current settings
        """
        if self.iter == 0:
            conv = 0.0
            lambda_optim = self.lamb
        else:
            dSsq = np.dot(dS, dS)
            dCsq = np.dot(dchi, dchi)
            dSdC = np.dot(dchi, dS)
            if dSsq * dCsq != 0.0:
                conv = dSdC / math.sqrt(dSsq * dCsq)
                SCratio = math.sqrt(dSsq / dCsq)
            else:
                if self.debug > 0:
                    print('*** WARNING in drive_conv, dSsq*dCsq == 0.0')
                conv = 0.0
                SCratio = 1.0
            if self.lambdacont == 'none':
                lambda_optim = self.lamb
            else:
                if self.lambdacont == 'increment':
                    lambda_optim = self.lamb * self.lambdamax
                else:
                    if self.lambdacont == 'angle':
                        if conv > 0.0:
                            lambda_optim = dSsq / dSdC
                        else:
                            lambda_optim = 0.0
                            print('Warning : Inverse geometry in Angle')
                    else:
                        if self.lambdacont == 'cosine':
                            lambda_optim = (SCratio * dSdC + dSsq) / (SCratio * dCsq + dSdC)
                            sqdSsq = np.sqrt(dSsq)
                            sqdCsq = np.sqrt(dCsq)
                        else:
                            raise Exception('error in lambdacont value')
            if lambda_optim < 0.0:
                if self.debug > 1:
                    print('lambda_optim neg', lambda_optim)
                lambda_optim = 0.0
            return (
             conv, lambda_optim)

    def update_lambda(self, newlambda, inc=0.5):
        """
        moves self.lamb to new value, using new value newlambda as internal control
        typically : l = l (1-inc) * l inc
        restricted to +/- lambdamax
        """
        if self.iter > 0:
            new_lamb = (1.0 - inc) * self.lamb + inc * self.lambdasp * newlambda
            self.lamb = min(new_lamb, self.lambdamax * self.lamb)
        else:
            self.lamb = newlambda
        if self.debug > 0:
            self.llamb.append(self.lamb)

    def concentring(self):
        """used when no valid step is found"""
        self.image *= 0.99
        if self.debug > 0:
            print('concentring')

    @timeit
    def solve--- This code section failed: ---

 L. 416         0  LOAD_CODE                <code_object clp>
                2  LOAD_STR                 'MaxEnt.solve.<locals>.clp'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_DEREF              'clp'

 L. 420         8  LOAD_CLOSURE             'clp'
               10  LOAD_CLOSURE             'dQ'
               12  LOAD_CLOSURE             'self'
               14  BUILD_TUPLE_3         3 
               16  LOAD_CODE                <code_object foptim>
               18  LOAD_STR                 'MaxEnt.solve.<locals>.foptim'
               20  MAKE_FUNCTION_8          'closure'
               22  STORE_FAST               'foptim'

 L. 428        24  LOAD_CLOSURE             'self'
               26  BUILD_TUPLE_1         1 
               28  LOAD_CODE                <code_object Qprime>
               30  LOAD_STR                 'MaxEnt.solve.<locals>.Qprime'
               32  MAKE_FUNCTION_8          'closure'
               34  STORE_FAST               'Qprime'

 L. 434        36  LOAD_CLOSURE             'self'
               38  BUILD_TUPLE_1         1 
               40  LOAD_CODE                <code_object Qhess_p>
               42  LOAD_STR                 'MaxEnt.solve.<locals>.Qhess_p'
               44  MAKE_FUNCTION_8          'closure'
               46  STORE_FAST               'Qhess_p'

 L. 442        48  LOAD_DEREF               'self'
               50  LOAD_ATTR                debug
               52  LOAD_CONST               1
               54  COMPARE_OP               >
               56  POP_JUMP_IF_FALSE    70  'to 70'

 L. 443        58  LOAD_GLOBAL              plot
               60  LOAD_DEREF               'self'
               62  LOAD_ATTR                image
               64  LOAD_STR                 'iter 0'
               66  CALL_FUNCTION_2       2  ''
               68  STORE_FAST               'fig'
             70_0  COME_FROM           862  '862'
             70_1  COME_FROM            56  '56'

 L. 444        70  LOAD_DEREF               'self'
               72  LOAD_ATTR                iter
               74  LOAD_DEREF               'self'
               76  LOAD_ATTR                iterations
               78  COMPARE_OP               <=
            80_82  POP_JUMP_IF_FALSE   886  'to 886'
               84  LOAD_DEREF               'self'
               86  LOAD_ATTR                chi2
               88  LOAD_DEREF               'self'
               90  LOAD_ATTR                chi2target
               92  COMPARE_OP               >
            94_96  POP_JUMP_IF_FALSE   886  'to 886'

 L. 447        98  LOAD_GLOBAL              np
              100  LOAD_METHOD              sum
              102  LOAD_DEREF               'self'
              104  LOAD_ATTR                image
              106  CALL_METHOD_1         1  ''
              108  LOAD_DEREF               'self'
              110  STORE_ATTR               sum

 L. 448       112  LOAD_GLOBAL              print
              114  LOAD_STR                 '----------- ITER:'
              116  LOAD_DEREF               'self'
              118  LOAD_ATTR                iter
              120  CALL_FUNCTION_2       2  ''
              122  POP_TOP          

 L. 449       124  LOAD_DEREF               'self'
              126  LOAD_ATTR                debug
              128  LOAD_CONST               1
              130  COMPARE_OP               >
              132  POP_JUMP_IF_FALSE   148  'to 148'

 L. 450       134  LOAD_GLOBAL              print
              136  LOAD_STR                 'Sum : %f'
              138  LOAD_DEREF               'self'
              140  LOAD_ATTR                sum
              142  BINARY_MODULO    
              144  CALL_FUNCTION_1       1  ''
              146  POP_TOP          
            148_0  COME_FROM           132  '132'

 L. 452       148  LOAD_DEREF               'self'
              150  LOAD_METHOD              do_chisquare
              152  LOAD_DEREF               'self'
              154  LOAD_ATTR                image
              156  CALL_METHOD_1         1  ''
              158  UNPACK_SEQUENCE_2     2 
              160  STORE_FAST               'chi2'
              162  STORE_FAST               'dchi'

 L. 453       164  LOAD_FAST                'chi2'
              166  LOAD_DEREF               'self'
              168  STORE_ATTR               chi2

 L. 454       170  LOAD_DEREF               'self'
              172  LOAD_METHOD              do_entropy
              174  LOAD_DEREF               'self'
              176  LOAD_ATTR                image
              178  CALL_METHOD_1         1  ''
              180  UNPACK_SEQUENCE_2     2 
              182  STORE_FAST               'S'
              184  STORE_FAST               'dS'

 L. 455       186  LOAD_FAST                'S'
              188  LOAD_DEREF               'self'
              190  STORE_ATTR               S

 L. 456       192  LOAD_FAST                'dchi'
              194  LOAD_DEREF               'self'
              196  STORE_ATTR               dchi2

 L. 457       198  LOAD_FAST                'dS'
              200  LOAD_DEREF               'self'
              202  STORE_ATTR               dS

 L. 458       204  LOAD_DEREF               'self'
              206  LOAD_ATTR                debug
              208  LOAD_CONST               0
              210  COMPARE_OP               >
          212_214  POP_JUMP_IF_FALSE   260  'to 260'

 L. 459       216  LOAD_GLOBAL              print
              218  LOAD_STR                 'S : %f   Chi2 : %f'
              220  LOAD_DEREF               'self'
              222  LOAD_ATTR                S
              224  LOAD_DEREF               'self'
              226  LOAD_ATTR                chi2
              228  BUILD_TUPLE_2         2 
              230  BINARY_MODULO    
              232  CALL_FUNCTION_1       1  ''
              234  POP_TOP          

 L. 460       236  LOAD_DEREF               'self'
              238  LOAD_ATTR                lchi2
              240  LOAD_METHOD              append
              242  LOAD_FAST                'chi2'
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          

 L. 461       248  LOAD_DEREF               'self'
              250  LOAD_ATTR                lentropy
              252  LOAD_METHOD              append
              254  LOAD_FAST                'S'
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          
            260_0  COME_FROM           212  '212'

 L. 463       260  LOAD_DEREF               'self'
              262  LOAD_METHOD              drive_conv
              264  LOAD_FAST                'dchi'
              266  LOAD_FAST                'dS'
              268  CALL_METHOD_2         2  ''
              270  UNPACK_SEQUENCE_2     2 
              272  STORE_FAST               'conv'
              274  STORE_FAST               'lambda_optim'

 L. 464       276  LOAD_DEREF               'self'
              278  LOAD_METHOD              update_lambda
              280  LOAD_FAST                'lambda_optim'
              282  CALL_METHOD_1         1  ''
              284  POP_TOP          

 L. 465       286  LOAD_GLOBAL              print
              288  LOAD_STR                 'convergence : %F   lambda : %f'
              290  LOAD_FAST                'conv'
              292  LOAD_DEREF               'self'
              294  LOAD_ATTR                lamb
              296  BUILD_TUPLE_2         2 
              298  BINARY_MODULO    
              300  CALL_FUNCTION_1       1  ''
              302  POP_TOP          

 L. 466       304  LOAD_CONST               0.0
              306  STORE_FAST               'step'

 L. 467       308  LOAD_DEREF               'self'
              310  LOAD_ATTR                debug
              312  LOAD_CONST               0
              314  COMPARE_OP               >
          316_318  POP_JUMP_IF_FALSE   350  'to 350'

 L. 468       320  LOAD_GLOBAL              print
              322  LOAD_STR                 'lambda_optim : %f,    new_lambda : %f'
              324  LOAD_FAST                'lambda_optim'
              326  LOAD_DEREF               'self'
              328  LOAD_ATTR                lamb
              330  BUILD_TUPLE_2         2 
              332  BINARY_MODULO    
              334  CALL_FUNCTION_1       1  ''
              336  POP_TOP          

 L. 469       338  LOAD_DEREF               'self'
              340  LOAD_METHOD              Q
              342  LOAD_DEREF               'self'
              344  LOAD_ATTR                image
              346  CALL_METHOD_1         1  ''
              348  STORE_FAST               'Q0'
            350_0  COME_FROM           316  '316'

 L. 471       350  LOAD_DEREF               'self'
              352  LOAD_ATTR                algo
              354  LOAD_STR                 'steepest'
              356  COMPARE_OP               ==
          358_360  POP_JUMP_IF_FALSE   448  'to 448'

 L. 472       362  LOAD_DEREF               'self'
              364  LOAD_ATTR                lamb
              366  LOAD_FAST                'dchi'
              368  BINARY_MULTIPLY  
              370  LOAD_FAST                'dS'
              372  BINARY_SUBTRACT  
              374  STORE_DEREF              'dQ'

 L. 473       376  LOAD_GLOBAL              scipy
              378  LOAD_ATTR                optimize
              380  LOAD_ATTR                brent
              382  LOAD_FAST                'foptim'
              384  LOAD_CONST               0.0
              386  LOAD_DEREF               'self'
              388  LOAD_ATTR                stepmax
              390  BUILD_TUPLE_2         2 
              392  LOAD_DEREF               'self'
              394  LOAD_ATTR                miniter
              396  LOAD_CONST               0
              398  LOAD_CONST               ('brack', 'maxiter', 'full_output')
              400  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              402  STORE_FAST               'step'

 L. 474       404  LOAD_FAST                'step'
              406  LOAD_CONST               0
              408  COMPARE_OP               !=
          410_412  POP_JUMP_IF_FALSE   436  'to 436'

 L. 475       414  LOAD_DEREF               'clp'
              416  LOAD_DEREF               'self'
              418  LOAD_ATTR                image
              420  LOAD_FAST                'step'
              422  LOAD_DEREF               'dQ'
              424  BINARY_MULTIPLY  
              426  BINARY_ADD       
              428  CALL_FUNCTION_1       1  ''
              430  LOAD_DEREF               'self'
              432  STORE_ATTR               image
              434  JUMP_FORWARD        768  'to 768'
            436_0  COME_FROM           410  '410'

 L. 477       436  LOAD_DEREF               'self'
              438  LOAD_METHOD              concentring
              440  CALL_METHOD_0         0  ''
              442  POP_TOP          
          444_446  JUMP_FORWARD        768  'to 768'
            448_0  COME_FROM           358  '358'

 L. 478       448  LOAD_DEREF               'self'
              450  LOAD_ATTR                algo
              452  LOAD_STR                 'Gifa'
              454  COMPARE_OP               ==
          456_458  POP_JUMP_IF_FALSE   566  'to 566'

 L. 479       460  LOAD_DEREF               'self'
              462  LOAD_ATTR                sum
              464  LOAD_DEREF               'self'
              466  LOAD_METHOD              sexp
              468  LOAD_DEREF               'self'
              470  LOAD_ATTR                sum
              472  UNARY_NEGATIVE   
              474  LOAD_FAST                'dchi'
              476  BINARY_MULTIPLY  
              478  LOAD_DEREF               'self'
              480  LOAD_ATTR                S
              482  BINARY_SUBTRACT  
              484  CALL_METHOD_1         1  ''
              486  BINARY_MULTIPLY  
              488  LOAD_DEREF               'self'
              490  LOAD_ATTR                image
              492  BINARY_SUBTRACT  
              494  STORE_DEREF              'dQ'

 L. 480       496  LOAD_GLOBAL              scipy
              498  LOAD_ATTR                optimize
              500  LOAD_ATTR                brent
              502  LOAD_FAST                'foptim'
              504  LOAD_CONST               0.0
              506  LOAD_DEREF               'self'
              508  LOAD_ATTR                stepmax
              510  BUILD_TUPLE_2         2 
              512  LOAD_DEREF               'self'
              514  LOAD_ATTR                miniter
              516  LOAD_CONST               0
              518  LOAD_CONST               ('brack', 'maxiter', 'full_output')
              520  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              522  STORE_FAST               'step'

 L. 482       524  LOAD_FAST                'step'
              526  LOAD_CONST               0
              528  COMPARE_OP               !=
          530_532  POP_JUMP_IF_FALSE   556  'to 556'

 L. 483       534  LOAD_DEREF               'clp'
              536  LOAD_DEREF               'self'
              538  LOAD_ATTR                image
              540  LOAD_FAST                'step'
              542  LOAD_DEREF               'dQ'
              544  BINARY_MULTIPLY  
              546  BINARY_ADD       
              548  CALL_FUNCTION_1       1  ''
              550  LOAD_DEREF               'self'
              552  STORE_ATTR               image
              554  JUMP_FORWARD        564  'to 564'
            556_0  COME_FROM           530  '530'

 L. 485       556  LOAD_DEREF               'self'
              558  LOAD_METHOD              concentring
              560  CALL_METHOD_0         0  ''
              562  POP_TOP          
            564_0  COME_FROM           554  '554'
              564  JUMP_FORWARD        768  'to 768'
            566_0  COME_FROM           456  '456'

 L. 487       566  LOAD_DEREF               'self'
              568  LOAD_ATTR                algo
              570  LOAD_STR                 'cg'
              572  COMPARE_OP               ==
          574_576  POP_JUMP_IF_FALSE   614  'to 614'

 L. 488       578  LOAD_GLOBAL              scipy
              580  LOAD_ATTR                optimize
              582  LOAD_ATTR                fmin_cg
              584  LOAD_DEREF               'self'
              586  LOAD_ATTR                Q
              588  LOAD_DEREF               'self'
              590  LOAD_ATTR                image
              592  LOAD_FAST                'Qprime'
              594  LOAD_CONST               0.0001
              596  LOAD_DEREF               'self'
              598  LOAD_ATTR                miniter
              600  LOAD_CONST               0
              602  LOAD_DEREF               'clp'
              604  LOAD_CONST               ('fprime', 'gtol', 'maxiter', 'disp', 'callback')
              606  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              608  LOAD_DEREF               'self'
              610  STORE_ATTR               image
              612  JUMP_FORWARD        768  'to 768'
            614_0  COME_FROM           574  '574'

 L. 489       614  LOAD_DEREF               'self'
              616  LOAD_ATTR                algo
              618  LOAD_STR                 'bfgs'
              620  COMPARE_OP               ==
          622_624  POP_JUMP_IF_FALSE   662  'to 662'

 L. 490       626  LOAD_GLOBAL              scipy
              628  LOAD_ATTR                optimize
              630  LOAD_ATTR                fmin_bfgs
              632  LOAD_DEREF               'self'
              634  LOAD_ATTR                Q
              636  LOAD_DEREF               'self'
              638  LOAD_ATTR                image
              640  LOAD_FAST                'Qprime'
              642  LOAD_CONST               0.0001
              644  LOAD_DEREF               'self'
              646  LOAD_ATTR                miniter
              648  LOAD_CONST               0
              650  LOAD_DEREF               'clp'
              652  LOAD_CONST               ('gtol', 'maxiter', 'disp', 'callback')
              654  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              656  LOAD_DEREF               'self'
              658  STORE_ATTR               image
              660  JUMP_FORWARD        768  'to 768'
            662_0  COME_FROM           622  '622'

 L. 491       662  LOAD_DEREF               'self'
              664  LOAD_ATTR                algo
              666  LOAD_STR                 'ncg'
              668  COMPARE_OP               ==
          670_672  POP_JUMP_IF_FALSE   712  'to 712'

 L. 492       674  LOAD_GLOBAL              scipy
              676  LOAD_ATTR                optimize
              678  LOAD_ATTR                fmin_ncg
              680  LOAD_DEREF               'self'
              682  LOAD_ATTR                Q
              684  LOAD_DEREF               'self'
              686  LOAD_ATTR                image
              688  LOAD_FAST                'Qprime'
              690  LOAD_FAST                'Qhess_p'
              692  LOAD_CONST               None
              694  LOAD_DEREF               'self'
              696  LOAD_ATTR                miniter
              698  LOAD_CONST               1
              700  LOAD_DEREF               'clp'
              702  LOAD_CONST               ('fhess_p', 'fhess', 'maxiter', 'disp', 'callback')
              704  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              706  LOAD_DEREF               'self'
              708  STORE_ATTR               image
              710  JUMP_FORWARD        768  'to 768'
            712_0  COME_FROM           670  '670'

 L. 493       712  LOAD_DEREF               'self'
              714  LOAD_ATTR                algo
              716  LOAD_STR                 'slsqp'
              718  COMPARE_OP               ==
          720_722  POP_JUMP_IF_FALSE   760  'to 760'

 L. 494       724  LOAD_GLOBAL              scipy
              726  LOAD_ATTR                optimize
              728  LOAD_ATTR                fmin_bfgs
              730  LOAD_DEREF               'self'
              732  LOAD_ATTR                Q
              734  LOAD_DEREF               'self'
              736  LOAD_ATTR                image
              738  LOAD_FAST                'Qprime'
              740  LOAD_CONST               0.0001
              742  LOAD_DEREF               'self'
              744  LOAD_ATTR                miniter
              746  LOAD_CONST               0
              748  LOAD_DEREF               'clp'
              750  LOAD_CONST               ('gtol', 'maxiter', 'disp', 'callback')
              752  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              754  LOAD_DEREF               'self'
            756_0  COME_FROM           434  '434'
              756  STORE_ATTR               image
              758  JUMP_FORWARD        768  'to 768'
            760_0  COME_FROM           720  '720'

 L. 496       760  LOAD_GLOBAL              Exception
              762  LOAD_STR                 'Error with algo'
              764  CALL_FUNCTION_1       1  ''
              766  RAISE_VARARGS_1       1  'exception instance'
            768_0  COME_FROM           758  '758'
            768_1  COME_FROM           710  '710'
            768_2  COME_FROM           660  '660'
            768_3  COME_FROM           612  '612'
            768_4  COME_FROM           564  '564'
            768_5  COME_FROM           444  '444'

 L. 498       768  LOAD_DEREF               'self'
              770  LOAD_ATTR                debug
              772  LOAD_CONST               0
              774  COMPARE_OP               >
          776_778  POP_JUMP_IF_FALSE   806  'to 806'

 L. 499       780  LOAD_GLOBAL              print
              782  LOAD_STR                 'Q avant %f    Q apres %f    inc %f'
              784  LOAD_FAST                'Q0'
              786  LOAD_DEREF               'self'
              788  LOAD_METHOD              Q
              790  LOAD_DEREF               'self'
              792  LOAD_ATTR                image
              794  CALL_METHOD_1         1  ''
              796  LOAD_FAST                'step'
              798  BUILD_TUPLE_3         3 
              800  BINARY_MODULO    
              802  CALL_FUNCTION_1       1  ''
              804  POP_TOP          
            806_0  COME_FROM           776  '776'

 L. 500       806  LOAD_DEREF               'self'
              808  DUP_TOP          
              810  LOAD_ATTR                iter
              812  LOAD_CONST               1
              814  INPLACE_ADD      
              816  ROT_TWO          
              818  STORE_ATTR               iter

 L. 501       820  LOAD_DEREF               'self'
              822  LOAD_ATTR                debug
              824  LOAD_CONST               1
              826  COMPARE_OP               >
          828_830  POP_JUMP_IF_FALSE   854  'to 854'

 L. 502       832  LOAD_GLOBAL              plot
              834  LOAD_DEREF               'self'
              836  LOAD_ATTR                image
              838  LOAD_STR                 'iter %d'
              840  LOAD_DEREF               'self'
              842  LOAD_ATTR                iter
              844  BINARY_MODULO    
              846  LOAD_FAST                'fig'
              848  LOAD_CONST               ('fig',)
              850  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              852  POP_TOP          
            854_0  COME_FROM           828  '828'

 L. 503       854  LOAD_DEREF               'self'
              856  LOAD_ATTR                true_s
              858  LOAD_CONST               None
              860  COMPARE_OP               is-not
              862  POP_JUMP_IF_FALSE    70  'to 70'

 L. 504       864  LOAD_GLOBAL              print
              866  LOAD_STR                 'SNR '
              868  LOAD_GLOBAL              estimate_SNR
              870  LOAD_DEREF               'self'
              872  LOAD_ATTR                image
              874  LOAD_DEREF               'self'
              876  LOAD_ATTR                true_s
              878  CALL_FUNCTION_2       2  ''
              880  CALL_FUNCTION_2       2  ''
              882  POP_TOP          
              884  JUMP_BACK            70  'to 70'
            886_0  COME_FROM            94  '94'
            886_1  COME_FROM            80  '80'

 L. 505       886  LOAD_DEREF               'self'
              888  LOAD_ATTR                debug
              890  LOAD_CONST               0
              892  COMPARE_OP               >
          894_896  POP_JUMP_IF_FALSE   938  'to 938'

 L. 506       898  LOAD_GLOBAL              plot
              900  LOAD_DEREF               'self'
              902  LOAD_ATTR                lentropy
              904  LOAD_STR                 'Entropy'
              906  CALL_FUNCTION_2       2  ''
              908  POP_TOP          

 L. 507       910  LOAD_GLOBAL              plot
              912  LOAD_DEREF               'self'
              914  LOAD_ATTR                lchi2
              916  LOAD_STR                 '$\\chi^2$'
              918  LOAD_CONST               True
              920  LOAD_CONST               ('logy',)
              922  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              924  POP_TOP          

 L. 508       926  LOAD_GLOBAL              plot
              928  LOAD_DEREF               'self'
              930  LOAD_ATTR                llamb
              932  LOAD_STR                 '$\\lambda$ evolution'
              934  CALL_FUNCTION_2       2  ''
              936  POP_TOP          
            938_0  COME_FROM           894  '894'

Parse error at or near `COME_FROM' instruction at offset 756_0

    def report_convergence(self):
        """
        returns a set of array, which describe the way convergence was handled
        returns
        self.iter   The number of iteration performed so far
        self.image  The final image obtained on the last iteration
        self.chi2   The chi2 obtained on the last iteration
        self.S      The entropy obtained on the last iteration
        self.sum    The integral of self.image
        self.lamb   The lambda obtained on the last iteration
        self.dchi2      The derivative of chi2 obtained on the last iteration
        self.dS         The derivative of S obtained on the last iteration
        (following are [] if self.debug==0 )
        self.lchi2      The list of chi2 values since the beginning
        self.lentropy   The list of S values since the beginning
        self.llamb      The list of lambda values since the beginning
        """
        if self.iter > 0:
            r = [
             self.iter, self.image, self.chi2, self.S, self.sum, self.lamb, self.dchi2, self.dS, self.lchi2, self.lentropy, self.llamb]
        else:
            r = [
             self.iter, self.image]
        return r


class maxent_Tests(unittest.TestCase):

    def setup(self, size=100, noise=0.1, sc=1):
        """set-up scene"""
        T = TransferFunction()
        Ideal = initial_scene(size, sc)
        Exp = T.transform(Ideal)
        Exp += noise * np.random.randn(Exp.size)
        D = ExpData(Exp)
        D.noise = noise
        return (Ideal, D, T)

    def test_sexp(self):
        """draw sexp()"""
        Ideal, D, T = self.setup()
        M = MaxEnt(T, D)
        x = np.linspace(-5, 5)
        for i in range(5):
            M.exptang = float(i)
            plt.plot(x, (M.sexp(x)), label=('exptang=' + str(i)))
        else:
            plt.legend()

    def setup_test(self, M):
        """set-up M fr tests"""
        M.algo = 'Gifa'
        M.exptang = 0.0
        M.lambdacont = 'cosine'
        M.lambdamax = 1.5
        M.lambdasp = 2.0
        M.miniter = 100

    def test_MaxEnt(self):
        """run MaxEnt test"""
        Ideal, D, T = self.setup(noise=0.03)
        M = MaxEnt(T, D, debug=1, iterations=500)
        M.true_s = Ideal
        self.setup_test(M)
        M.report()
        M.solve()
        f = plot(Ideal, 'ideal')
        plt.subplot(411)
        plot(Ideal, 'ideal', fig=f)
        plt.subplot(412)
        plot((D.data), 'experimental (convoluted, noised)', fig=f)
        plt.subplot(413)
        plot((M.image), 'finale', fig=f)
        residu = T.transform(M.image) - D.data
        plt.subplot(414)
        plot(residu, 'residu', fig=f)
        print('Noise in residu :', np.sum(residu ** 2), M.chi2)
        return M.report_convergence()


if __name__ == '__main__':
    unittest.main()