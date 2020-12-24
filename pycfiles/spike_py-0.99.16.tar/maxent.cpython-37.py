# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
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

    for i in range(20):
        Ideal[i + 65] = i * sc / 20.0

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
                i.startswith('_') or print('%s\t:\t%s' % (i, att))

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
               66  CALL_FUNCTION_2       2  '2 positional arguments'
               68  STORE_FAST               'fig'
             70_0  COME_FROM            56  '56'

 L. 444     70_72  SETUP_LOOP          892  'to 892'
             74_0  COME_FROM           866  '866'
               74  LOAD_DEREF               'self'
               76  LOAD_ATTR                iter
               78  LOAD_DEREF               'self'
               80  LOAD_ATTR                iterations
               82  COMPARE_OP               <=
            84_86  POP_JUMP_IF_FALSE   890  'to 890'
               88  LOAD_DEREF               'self'
               90  LOAD_ATTR                chi2
               92  LOAD_DEREF               'self'
               94  LOAD_ATTR                chi2target
               96  COMPARE_OP               >
           98_100  POP_JUMP_IF_FALSE   890  'to 890'

 L. 447       102  LOAD_GLOBAL              np
              104  LOAD_METHOD              sum
              106  LOAD_DEREF               'self'
              108  LOAD_ATTR                image
              110  CALL_METHOD_1         1  '1 positional argument'
              112  LOAD_DEREF               'self'
              114  STORE_ATTR               sum

 L. 448       116  LOAD_GLOBAL              print
              118  LOAD_STR                 '----------- ITER:'
              120  LOAD_DEREF               'self'
              122  LOAD_ATTR                iter
              124  CALL_FUNCTION_2       2  '2 positional arguments'
              126  POP_TOP          

 L. 449       128  LOAD_DEREF               'self'
              130  LOAD_ATTR                debug
              132  LOAD_CONST               1
              134  COMPARE_OP               >
              136  POP_JUMP_IF_FALSE   152  'to 152'

 L. 450       138  LOAD_GLOBAL              print
              140  LOAD_STR                 'Sum : %f'
              142  LOAD_DEREF               'self'
              144  LOAD_ATTR                sum
              146  BINARY_MODULO    
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  POP_TOP          
            152_0  COME_FROM           136  '136'

 L. 452       152  LOAD_DEREF               'self'
              154  LOAD_METHOD              do_chisquare
              156  LOAD_DEREF               'self'
              158  LOAD_ATTR                image
              160  CALL_METHOD_1         1  '1 positional argument'
              162  UNPACK_SEQUENCE_2     2 
              164  STORE_FAST               'chi2'
              166  STORE_FAST               'dchi'

 L. 453       168  LOAD_FAST                'chi2'
              170  LOAD_DEREF               'self'
              172  STORE_ATTR               chi2

 L. 454       174  LOAD_DEREF               'self'
              176  LOAD_METHOD              do_entropy
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                image
              182  CALL_METHOD_1         1  '1 positional argument'
              184  UNPACK_SEQUENCE_2     2 
              186  STORE_FAST               'S'
              188  STORE_FAST               'dS'

 L. 455       190  LOAD_FAST                'S'
              192  LOAD_DEREF               'self'
              194  STORE_ATTR               S

 L. 456       196  LOAD_FAST                'dchi'
              198  LOAD_DEREF               'self'
              200  STORE_ATTR               dchi2

 L. 457       202  LOAD_FAST                'dS'
              204  LOAD_DEREF               'self'
              206  STORE_ATTR               dS

 L. 458       208  LOAD_DEREF               'self'
              210  LOAD_ATTR                debug
              212  LOAD_CONST               0
              214  COMPARE_OP               >
          216_218  POP_JUMP_IF_FALSE   264  'to 264'

 L. 459       220  LOAD_GLOBAL              print
              222  LOAD_STR                 'S : %f   Chi2 : %f'
              224  LOAD_DEREF               'self'
              226  LOAD_ATTR                S
              228  LOAD_DEREF               'self'
              230  LOAD_ATTR                chi2
              232  BUILD_TUPLE_2         2 
              234  BINARY_MODULO    
              236  CALL_FUNCTION_1       1  '1 positional argument'
              238  POP_TOP          

 L. 460       240  LOAD_DEREF               'self'
              242  LOAD_ATTR                lchi2
              244  LOAD_METHOD              append
              246  LOAD_FAST                'chi2'
              248  CALL_METHOD_1         1  '1 positional argument'
              250  POP_TOP          

 L. 461       252  LOAD_DEREF               'self'
              254  LOAD_ATTR                lentropy
              256  LOAD_METHOD              append
              258  LOAD_FAST                'S'
              260  CALL_METHOD_1         1  '1 positional argument'
              262  POP_TOP          
            264_0  COME_FROM           216  '216'

 L. 463       264  LOAD_DEREF               'self'
              266  LOAD_METHOD              drive_conv
              268  LOAD_FAST                'dchi'
              270  LOAD_FAST                'dS'
              272  CALL_METHOD_2         2  '2 positional arguments'
              274  UNPACK_SEQUENCE_2     2 
              276  STORE_FAST               'conv'
              278  STORE_FAST               'lambda_optim'

 L. 464       280  LOAD_DEREF               'self'
              282  LOAD_METHOD              update_lambda
              284  LOAD_FAST                'lambda_optim'
              286  CALL_METHOD_1         1  '1 positional argument'
              288  POP_TOP          

 L. 465       290  LOAD_GLOBAL              print
              292  LOAD_STR                 'convergence : %F   lambda : %f'
              294  LOAD_FAST                'conv'
              296  LOAD_DEREF               'self'
              298  LOAD_ATTR                lamb
              300  BUILD_TUPLE_2         2 
              302  BINARY_MODULO    
              304  CALL_FUNCTION_1       1  '1 positional argument'
              306  POP_TOP          

 L. 466       308  LOAD_CONST               0.0
              310  STORE_FAST               'step'

 L. 467       312  LOAD_DEREF               'self'
              314  LOAD_ATTR                debug
              316  LOAD_CONST               0
              318  COMPARE_OP               >
          320_322  POP_JUMP_IF_FALSE   354  'to 354'

 L. 468       324  LOAD_GLOBAL              print
              326  LOAD_STR                 'lambda_optim : %f,    new_lambda : %f'
              328  LOAD_FAST                'lambda_optim'
              330  LOAD_DEREF               'self'
              332  LOAD_ATTR                lamb
              334  BUILD_TUPLE_2         2 
              336  BINARY_MODULO    
              338  CALL_FUNCTION_1       1  '1 positional argument'
              340  POP_TOP          

 L. 469       342  LOAD_DEREF               'self'
              344  LOAD_METHOD              Q
              346  LOAD_DEREF               'self'
              348  LOAD_ATTR                image
              350  CALL_METHOD_1         1  '1 positional argument'
              352  STORE_FAST               'Q0'
            354_0  COME_FROM           320  '320'

 L. 471       354  LOAD_DEREF               'self'
              356  LOAD_ATTR                algo
              358  LOAD_STR                 'steepest'
              360  COMPARE_OP               ==
          362_364  POP_JUMP_IF_FALSE   452  'to 452'

 L. 472       366  LOAD_DEREF               'self'
              368  LOAD_ATTR                lamb
              370  LOAD_FAST                'dchi'
              372  BINARY_MULTIPLY  
              374  LOAD_FAST                'dS'
              376  BINARY_SUBTRACT  
              378  STORE_DEREF              'dQ'

 L. 473       380  LOAD_GLOBAL              scipy
              382  LOAD_ATTR                optimize
              384  LOAD_ATTR                brent
              386  LOAD_FAST                'foptim'
              388  LOAD_CONST               0.0
              390  LOAD_DEREF               'self'
              392  LOAD_ATTR                stepmax
              394  BUILD_TUPLE_2         2 
              396  LOAD_DEREF               'self'
              398  LOAD_ATTR                miniter
              400  LOAD_CONST               0
              402  LOAD_CONST               ('brack', 'maxiter', 'full_output')
              404  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              406  STORE_FAST               'step'

 L. 474       408  LOAD_FAST                'step'
              410  LOAD_CONST               0
              412  COMPARE_OP               !=
          414_416  POP_JUMP_IF_FALSE   440  'to 440'

 L. 475       418  LOAD_DEREF               'clp'
              420  LOAD_DEREF               'self'
              422  LOAD_ATTR                image
              424  LOAD_FAST                'step'
              426  LOAD_DEREF               'dQ'
              428  BINARY_MULTIPLY  
              430  BINARY_ADD       
              432  CALL_FUNCTION_1       1  '1 positional argument'
              434  LOAD_DEREF               'self'
              436  STORE_ATTR               image
              438  JUMP_FORWARD        772  'to 772'
            440_0  COME_FROM           414  '414'

 L. 477       440  LOAD_DEREF               'self'
              442  LOAD_METHOD              concentring
              444  CALL_METHOD_0         0  '0 positional arguments'
              446  POP_TOP          
          448_450  JUMP_FORWARD        772  'to 772'
            452_0  COME_FROM           362  '362'

 L. 478       452  LOAD_DEREF               'self'
              454  LOAD_ATTR                algo
              456  LOAD_STR                 'Gifa'
              458  COMPARE_OP               ==
          460_462  POP_JUMP_IF_FALSE   570  'to 570'

 L. 479       464  LOAD_DEREF               'self'
              466  LOAD_ATTR                sum
              468  LOAD_DEREF               'self'
              470  LOAD_METHOD              sexp
              472  LOAD_DEREF               'self'
              474  LOAD_ATTR                sum
              476  UNARY_NEGATIVE   
              478  LOAD_FAST                'dchi'
              480  BINARY_MULTIPLY  
              482  LOAD_DEREF               'self'
              484  LOAD_ATTR                S
              486  BINARY_SUBTRACT  
              488  CALL_METHOD_1         1  '1 positional argument'
              490  BINARY_MULTIPLY  
              492  LOAD_DEREF               'self'
              494  LOAD_ATTR                image
              496  BINARY_SUBTRACT  
              498  STORE_DEREF              'dQ'

 L. 480       500  LOAD_GLOBAL              scipy
              502  LOAD_ATTR                optimize
              504  LOAD_ATTR                brent
              506  LOAD_FAST                'foptim'
              508  LOAD_CONST               0.0
              510  LOAD_DEREF               'self'
              512  LOAD_ATTR                stepmax
              514  BUILD_TUPLE_2         2 
              516  LOAD_DEREF               'self'
              518  LOAD_ATTR                miniter
              520  LOAD_CONST               0
              522  LOAD_CONST               ('brack', 'maxiter', 'full_output')
              524  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              526  STORE_FAST               'step'

 L. 482       528  LOAD_FAST                'step'
              530  LOAD_CONST               0
              532  COMPARE_OP               !=
          534_536  POP_JUMP_IF_FALSE   560  'to 560'

 L. 483       538  LOAD_DEREF               'clp'
              540  LOAD_DEREF               'self'
              542  LOAD_ATTR                image
              544  LOAD_FAST                'step'
              546  LOAD_DEREF               'dQ'
              548  BINARY_MULTIPLY  
              550  BINARY_ADD       
              552  CALL_FUNCTION_1       1  '1 positional argument'
              554  LOAD_DEREF               'self'
              556  STORE_ATTR               image
              558  JUMP_FORWARD        568  'to 568'
            560_0  COME_FROM           534  '534'

 L. 485       560  LOAD_DEREF               'self'
              562  LOAD_METHOD              concentring
              564  CALL_METHOD_0         0  '0 positional arguments'
              566  POP_TOP          
            568_0  COME_FROM           558  '558'
              568  JUMP_FORWARD        772  'to 772'
            570_0  COME_FROM           460  '460'

 L. 487       570  LOAD_DEREF               'self'
              572  LOAD_ATTR                algo
              574  LOAD_STR                 'cg'
              576  COMPARE_OP               ==
          578_580  POP_JUMP_IF_FALSE   618  'to 618'

 L. 488       582  LOAD_GLOBAL              scipy
              584  LOAD_ATTR                optimize
              586  LOAD_ATTR                fmin_cg
              588  LOAD_DEREF               'self'
              590  LOAD_ATTR                Q
              592  LOAD_DEREF               'self'
              594  LOAD_ATTR                image
              596  LOAD_FAST                'Qprime'
              598  LOAD_CONST               0.0001
              600  LOAD_DEREF               'self'
              602  LOAD_ATTR                miniter
              604  LOAD_CONST               0
              606  LOAD_DEREF               'clp'
              608  LOAD_CONST               ('fprime', 'gtol', 'maxiter', 'disp', 'callback')
              610  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              612  LOAD_DEREF               'self'
              614  STORE_ATTR               image
              616  JUMP_FORWARD        772  'to 772'
            618_0  COME_FROM           578  '578'

 L. 489       618  LOAD_DEREF               'self'
              620  LOAD_ATTR                algo
              622  LOAD_STR                 'bfgs'
              624  COMPARE_OP               ==
          626_628  POP_JUMP_IF_FALSE   666  'to 666'

 L. 490       630  LOAD_GLOBAL              scipy
              632  LOAD_ATTR                optimize
              634  LOAD_ATTR                fmin_bfgs
              636  LOAD_DEREF               'self'
              638  LOAD_ATTR                Q
              640  LOAD_DEREF               'self'
              642  LOAD_ATTR                image
              644  LOAD_FAST                'Qprime'
              646  LOAD_CONST               0.0001
              648  LOAD_DEREF               'self'
              650  LOAD_ATTR                miniter
              652  LOAD_CONST               0
              654  LOAD_DEREF               'clp'
              656  LOAD_CONST               ('gtol', 'maxiter', 'disp', 'callback')
              658  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              660  LOAD_DEREF               'self'
              662  STORE_ATTR               image
              664  JUMP_FORWARD        772  'to 772'
            666_0  COME_FROM           626  '626'

 L. 491       666  LOAD_DEREF               'self'
              668  LOAD_ATTR                algo
              670  LOAD_STR                 'ncg'
              672  COMPARE_OP               ==
          674_676  POP_JUMP_IF_FALSE   716  'to 716'

 L. 492       678  LOAD_GLOBAL              scipy
              680  LOAD_ATTR                optimize
              682  LOAD_ATTR                fmin_ncg
              684  LOAD_DEREF               'self'
              686  LOAD_ATTR                Q
              688  LOAD_DEREF               'self'
              690  LOAD_ATTR                image
              692  LOAD_FAST                'Qprime'
              694  LOAD_FAST                'Qhess_p'
              696  LOAD_CONST               None
              698  LOAD_DEREF               'self'
              700  LOAD_ATTR                miniter
              702  LOAD_CONST               1
              704  LOAD_DEREF               'clp'
              706  LOAD_CONST               ('fhess_p', 'fhess', 'maxiter', 'disp', 'callback')
              708  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              710  LOAD_DEREF               'self'
              712  STORE_ATTR               image
              714  JUMP_FORWARD        772  'to 772'
            716_0  COME_FROM           674  '674'

 L. 493       716  LOAD_DEREF               'self'
              718  LOAD_ATTR                algo
              720  LOAD_STR                 'slsqp'
              722  COMPARE_OP               ==
          724_726  POP_JUMP_IF_FALSE   764  'to 764'

 L. 494       728  LOAD_GLOBAL              scipy
              730  LOAD_ATTR                optimize
              732  LOAD_ATTR                fmin_bfgs
              734  LOAD_DEREF               'self'
              736  LOAD_ATTR                Q
              738  LOAD_DEREF               'self'
              740  LOAD_ATTR                image
              742  LOAD_FAST                'Qprime'
              744  LOAD_CONST               0.0001
              746  LOAD_DEREF               'self'
              748  LOAD_ATTR                miniter
              750  LOAD_CONST               0
              752  LOAD_DEREF               'clp'
              754  LOAD_CONST               ('gtol', 'maxiter', 'disp', 'callback')
              756  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              758  LOAD_DEREF               'self'
            760_0  COME_FROM           438  '438'
              760  STORE_ATTR               image
              762  JUMP_FORWARD        772  'to 772'
            764_0  COME_FROM           724  '724'

 L. 496       764  LOAD_GLOBAL              Exception
              766  LOAD_STR                 'Error with algo'
              768  CALL_FUNCTION_1       1  '1 positional argument'
              770  RAISE_VARARGS_1       1  'exception instance'
            772_0  COME_FROM           762  '762'
            772_1  COME_FROM           714  '714'
            772_2  COME_FROM           664  '664'
            772_3  COME_FROM           616  '616'
            772_4  COME_FROM           568  '568'
            772_5  COME_FROM           448  '448'

 L. 498       772  LOAD_DEREF               'self'
              774  LOAD_ATTR                debug
              776  LOAD_CONST               0
              778  COMPARE_OP               >
          780_782  POP_JUMP_IF_FALSE   810  'to 810'

 L. 499       784  LOAD_GLOBAL              print
              786  LOAD_STR                 'Q avant %f    Q apres %f    inc %f'
              788  LOAD_FAST                'Q0'
              790  LOAD_DEREF               'self'
              792  LOAD_METHOD              Q
              794  LOAD_DEREF               'self'
              796  LOAD_ATTR                image
              798  CALL_METHOD_1         1  '1 positional argument'
              800  LOAD_FAST                'step'
              802  BUILD_TUPLE_3         3 
              804  BINARY_MODULO    
              806  CALL_FUNCTION_1       1  '1 positional argument'
              808  POP_TOP          
            810_0  COME_FROM           780  '780'

 L. 500       810  LOAD_DEREF               'self'
              812  DUP_TOP          
              814  LOAD_ATTR                iter
              816  LOAD_CONST               1
              818  INPLACE_ADD      
              820  ROT_TWO          
              822  STORE_ATTR               iter

 L. 501       824  LOAD_DEREF               'self'
              826  LOAD_ATTR                debug
              828  LOAD_CONST               1
              830  COMPARE_OP               >
          832_834  POP_JUMP_IF_FALSE   858  'to 858'

 L. 502       836  LOAD_GLOBAL              plot
              838  LOAD_DEREF               'self'
              840  LOAD_ATTR                image
              842  LOAD_STR                 'iter %d'
              844  LOAD_DEREF               'self'
              846  LOAD_ATTR                iter
              848  BINARY_MODULO    
              850  LOAD_FAST                'fig'
              852  LOAD_CONST               ('fig',)
              854  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              856  POP_TOP          
            858_0  COME_FROM           832  '832'

 L. 503       858  LOAD_DEREF               'self'
              860  LOAD_ATTR                true_s
              862  LOAD_CONST               None
              864  COMPARE_OP               is-not
              866  POP_JUMP_IF_FALSE    74  'to 74'

 L. 504       868  LOAD_GLOBAL              print
              870  LOAD_STR                 'SNR '
              872  LOAD_GLOBAL              estimate_SNR
              874  LOAD_DEREF               'self'
              876  LOAD_ATTR                image
              878  LOAD_DEREF               'self'
              880  LOAD_ATTR                true_s
              882  CALL_FUNCTION_2       2  '2 positional arguments'
              884  CALL_FUNCTION_2       2  '2 positional arguments'
              886  POP_TOP          
              888  JUMP_BACK            74  'to 74'
            890_0  COME_FROM            98  '98'
            890_1  COME_FROM            84  '84'
              890  POP_BLOCK        
            892_0  COME_FROM_LOOP       70  '70'

 L. 505       892  LOAD_DEREF               'self'
              894  LOAD_ATTR                debug
              896  LOAD_CONST               0
              898  COMPARE_OP               >
          900_902  POP_JUMP_IF_FALSE   944  'to 944'

 L. 506       904  LOAD_GLOBAL              plot
              906  LOAD_DEREF               'self'
              908  LOAD_ATTR                lentropy
              910  LOAD_STR                 'Entropy'
              912  CALL_FUNCTION_2       2  '2 positional arguments'
              914  POP_TOP          

 L. 507       916  LOAD_GLOBAL              plot
              918  LOAD_DEREF               'self'
              920  LOAD_ATTR                lchi2
              922  LOAD_STR                 '$\\chi^2$'
              924  LOAD_CONST               True
              926  LOAD_CONST               ('logy',)
              928  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              930  POP_TOP          

 L. 508       932  LOAD_GLOBAL              plot
              934  LOAD_DEREF               'self'
              936  LOAD_ATTR                llamb
              938  LOAD_STR                 '$\\lambda$ evolution'
              940  CALL_FUNCTION_2       2  '2 positional arguments'
              942  POP_TOP          
            944_0  COME_FROM           900  '900'

Parse error at or near `COME_FROM' instruction at offset 760_0

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