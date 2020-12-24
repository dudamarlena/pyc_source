# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/plugins/PALMA.py
# Compiled at: 2020-01-31 02:54:08
# Size of source mod 2**32: 22681 bytes
"""complete DOSY processing, using the PALMA algorithm

This program uses the PALMA algorithm, presented in the manuscript

Cherni, A., Chouzenoux, E., & Delsuc, M.-A. (2017).
PALMA, an improved algorithm for DOSY signal processing.
Analyst, 142(5), 772–779. http://doi.org/10.1039/c6an01902a

see manuscript for details.

Authors:
Afef Cherni, Emilie Chouzenoux, and Marc-André Delsuc

Licence: CC-BY-NC-SA   https://creativecommons.org/licenses/by-nc-sa/4.0/
"""
from __future__ import print_function, division
import sys
import os.path as op
import unittest, re, numpy as np, scipy
from spike import NPKError
from spike.NPKData import NPKData_plugin
from spike.NPKData import LaplaceAxis
from spike.File.BrukerNMR import Import_2D, Import_2D_proc
import spike.Algo.savitzky_golay as sgm
import spike.util.signal_tools
debug = True
version = 1.1

def residus(x, K, y):
    """computes distance between y and Kx"""
    return np.linalg.norm(np.dot(K, x) - y, 2)


def L1(x):
    """computes L1 norm of x"""
    absx = np.abs(x)
    return np.sum(absx)


def ent(x, a):
    """computes Entropy of x"""
    xpos = x[(x > 0)] / a
    return -np.sum(xpos * np.log(xpos))


def criterion(x, K, y, lamda, a):
    """
    Compute regularization function, (not used during iteration without full_output)
    """
    f = 0.5 * residus(x, K, y) ** 2
    if 1 - lamda > 0:
        rl1 = (1 - lamda) * L1(x)
    else:
        rl1 = 0
    if lamda > 0:
        rent = -lamda * ent(x, a)
    else:
        rent = 0
    return f + rl1 + rent


def lambert_w(x):
    """
    W Lambert function
    """
    d = scipy.special.lambertw(x, k=0, tol=1e-08)
    return np.real(d)


def approx_lambert(x):
    """
    approximation of W( exp(x) )
    no error below 50, and  less than 0.2% error for x>50 and converges toward 0 for x->inf
    does not overflow !     does not NaN
    """
    limit = 50
    nz = np.nonzero(x < limit)[0]
    A = 0.00303583748046
    s = x * (1 - np.log(x) / (1 + x)) + A / (1 + x - limit) ** 0.75
    s[nz] = lambert_w(np.exp(x[nz]))
    return np.nan_to_num(s)


def prox_l1(x, w):
    """
    Compute proximity operator of L1 norm"
    """
    p = np.zeros_like(x)
    pos = np.nonzero(x > w)[0]
    p[pos] = x[pos] - w
    neg = np.nonzero(x < -w)[0]
    p[neg] = x[neg] + w
    return p


def prox_l2(x, dx, eta):
    """
    Compute projection of x onto l2 ball ||z-dx||<=eta
    x and dx are image vectors  
    """
    t = x - dx
    s = t * np.minimum(eta / np.linalg.norm(t), 1)
    return x + s - t


def prox_l1_Sent(x, lamda, a):
    """
    Compute the proximity operator of L1 + Shannon Entropy
    """
    if lamda == 0:
        p = prox_l1(x, 1)
    else:
        loga = np.log(a)
        loglamda = np.log(lamda)
        c = (a * x - a * (1 - lamda)) / lamda - 1 - loglamda + 2 * loga
        p = lamda / a * approx_lambert(c)
    return p


debug = False

def PPXAplus(K, Binv, y, eta, nbiter=1000, lamda=0.1, prec=1e-12, full_output=False):
    r"""
    performs the PPXA+ algorithm
    K : a MxN matrix which transform from data space to image space
    Binv : inverse of (Id + K.t K)
    y : a M vector containing the data
    a : an estimate of $\sum{x}$ where x is final image - used as a bayesian prior of x
    eta : an estimate of the standard deviation of the noise in y
    nbiter : maximum number of iteration to do
    lamda: is in [0..1], the weigth of l1 vs MaxEnt regularisation
        lamda = 0 is full L1
        lamda = 1 is full MaxEnt
    prec: precision of the result, algo will stop if steps are below this evel
    full_output: if True, will compute additional terms during convergence (slower):
        parameters =  (lcrit, lent, lL1, lresidus)
            with lcrit: the optimized criterion
            len: evolution of -entropy
            lL1: evolution of L1(x)
            lresidus: evolution of the distance ||Kx-y||
        if False, returns the number of performed iterations
    returns
    (x, parameters), where x is the computed optimal image
    
    """
    scale = y[0]
    y = y / scale
    eta = eta / scale
    a = y[0]
    gamma = 1.99
    M, N = K.shape
    x0 = np.ones((N, 1))
    x0 *= np.sum(y) / (M * N)
    lcrit = []
    lent = []
    lL1 = []
    lresidus = []
    Kt = K.T
    x_n_old = x0.copy()
    tmp1 = x0.copy()
    tmp2 = np.dot(K, x0)
    x_n = np.dot(Binv, tmp1 + np.dot(Kt, tmp2))
    n = 0
    for n in range(0, nbiter):
        xx1 = prox_l1_Sent(tmp1, lamda, a)
        xx2 = prox_l2(tmp2, y, eta)
        c = np.dot(Binv, xx1 + np.dot(Kt, xx2))
        cmxn = c - x_n
        c2mxn = c + cmxn
        tmp1 += gamma * (c2mxn - xx1)
        tmp2 += gamma * (np.dot(K, c2mxn) - xx2)
        x_n += gamma * cmxn
        n_x_n = np.linalg.norm(x_n - x_n_old, 2) / np.linalg.norm(x_n)
        if np.isnan(x_n.sum()):
            break
        if n_x_n < prec:
            break
        x_n_old[:, :] = x_n[:, :]
        if full_output is True:
            lcrit.append(criterion(x_n, K, y, lamda, a))
            lent.append(ent(x_n, a))
            lL1.append(L1(x_n))
            lresidus.append(residus(x_n, K, y))

    x_n = x_n * scale
    if full_output:
        comp = [
         lcrit, lent, lL1, lresidus]
    else:
        comp = n
    return (
     x_n, comp)


def eval_dosy_noise(x, window_size=9, order=3):
    """
    we estimate the noise in x by computing difference from polynomial fitting
    input: x - a real vector
    return: the noise level
    """
    m = sgm.sgolay_coef(window_size, order, deriv=0)
    noise = (sgm.sgolay_comp(x, m, window_size) - x).std()
    return noise


def auto_damp_width(d):
    """
    uses the tab buffer to determine the optimum dmin and dmax for ILT processing
    """
    import math
    mn = min(d.axis1.qvalues)
    mx = max(d.axis1.qvalues)
    idmax = d.axis1.dfactor * 2 / mn
    idmin = d.axis1.dfactor * 0.5 / mx
    logidmin = int(math.log(idmin) / math.log(10))
    edmin = math.exp(math.log(10) * logidmin)
    dmin = int(int(idmin / edmin) * edmin)
    logidmax = int(math.log(idmax) / math.log(10))
    edmax = math.exp(math.log(10) * logidmax)
    dmax = int((int(idmax / edmax) + 1) * edmax)
    return (
     dmin, dmax)


def calibdosy(litdelta, bigdelta, recovery=0.0, seq_type='ste', nucleus='1H', maxgrad=50.0, maxtab=50.0, gradshape=1.0, unbalancing=0.2, os_tau=None, os_version=1):
    """
    returns the DOSY calibrating factor from the parameters
    
      bigdelta float
       "Big Delta"  : diffusion delay in msec

      litdelta float
       "little Delta"  : gradient duration in msec

      seq_type enum "pgse","ste","bpp_ste","ste_2echoes","bpp_ste_2echoes","oneshot" / default ste
       the type of DOSY sequence used
        pgse : the standard hahn echoe sequence
        ste : the standard stimulated echoe sequence
        bpp_ste : ste with bipolar gradient pulses
        ste_2echoes : ste compensated for convection
        bpp_ste_2echoes : bpp_ste compensated for convection
        oneshot : the oneshot sequence from Pelta, Morris, Stchedroff, Hammond, 2002, Magn.Reson.Chem. 40, p147
            uses unbalancing=0.2, os_tau=None, os_version=1
            unbalancing is called alpha in the publication
            os_tau is called tau in the publication
            os_version=1 corresponds to equation(1) / os_version=2 to (2)
      nucleus enum "1H","2H","13C","15N","17O","19F","31P" / default 1H
       the observed nucleus

     recovery float
       Gradient recovery delay

     maxgrad float
       Maximum Amplificator Gradient Intensity, in G/cm    / default 50.0

     maxtab float
       Maximum Tabulated Gradient Value in the tabulated file. / default 50.0
       Bruker users with gradient list in G/cm (difflist) use maxgrad here
       Bruker users with gradient list in % use 100 here
       Varian users use 32768 here

     gradshape float
       integral factor depending on the gradient shape used / default 1.0
       typical values are :
           1.0 for rectangular gradients
           0.6366 = 2/pi for sine bell gradients
           0.4839496 for 4% truncated gaussian (Bruker gauss.100 file)
       Bruker users using difflist use 1.0 here, as it is already included in difflist

    """
    g = maxgrad / maxtab * 0.0001
    aire = g * gradshape * litdelta
    if nucleus == '1H':
        gama = 267500000.0
    else:
        if nucleus == '2H':
            gama = 41100000.0
        else:
            if nucleus == '13C':
                gama = 67300000.0
            else:
                if nucleus == '15N':
                    gama = -27100000.0
                else:
                    if nucleus == '17O':
                        gama = -36300000.0
                    else:
                        if nucleus == '19F':
                            gama = 251700000.0
                        else:
                            if nucleus == '31P':
                                gama = 108300000.0
                            else:
                                raise Exception('Unknown nucleus')
    K = (gama * aire) ** 2
    if seq_type == 'ste':
        K = K * (bigdelta + 2 * litdelta / 3 + recovery)
    else:
        if seq_type == 'bpp_ste':
            K = K * (bigdelta + 2 * litdelta / 3 + 3 * recovery / 4)
        else:
            if seq_type == 'ste_2echoes':
                K = K * (bigdelta + 4 * litdelta / 3 + 2 * recovery)
            else:
                if seq_type == 'bpp_ste_2echoes':
                    K = K * (bigdelta + 4 * litdelta / 3 + 3 * recovery / 2)
                else:
                    if seq_type == 'oneshot':
                        if os_version == 1:
                            K = K * (bigdelta + litdelta * (unbalancing ** 2 - 2) / 6 + os_tau * (unbalancing ** 2 - 1) / 2)
                        else:
                            if os_version == 2:
                                K = K * (bigdelta + litdelta * (unbalancing ** 2 + 3 * unbalancing - 2) / 6 + os_tau * (unbalancing ** 2 + 2 * unbalancing - 1) / 2)
                            else:
                                raise Exception('Unknown sequence: ' + str(seq_type) + str(os_version))
                    else:
                        if seq_type == 'pgse':
                            K = K * bigdelta + 2 * litdelta / 3
                        else:
                            raise Exception('Unknown sequence: ' + str(seq_type))
    K = K * 1e-08
    return 1 / K


def determine_seqtype(pulprog):
    """
    given the PULPROG name, determines which seq_type is to be used
    PULPROG should be follow the standard Bruker naming scheme
    """
    if re.search('dstebp', pulprog):
        sequence = 'bpp_ste_2echoes'
    else:
        if re.search('dstegp', pulprog):
            sequence = 'ste_2echoes'
        else:
            if re.search('stebp|stegpbp|ledbp', pulprog):
                sequence = 'bpp_ste'
            else:
                if re.search('stegp|led', pulprog):
                    sequence = 'ste'
                else:
                    if re.search('oneshot', pulprog):
                        sequence = 'oneshot'
                    else:
                        print('<%s> : Unsupported pulse program.' % pulprog)
                        sequence = 'None'
    print(sequence)
    return sequence


def dcalibdosy--- This code section failed: ---

 L. 363         0  LOAD_GLOBAL              float
                2  LOAD_FAST                'npk'
                4  LOAD_ATTR                params
                6  LOAD_STR                 'acqu'
                8  BINARY_SUBSCR    
               10  LOAD_STR                 '$D'
               12  BINARY_SUBSCR    
               14  LOAD_CONST               20
               16  BINARY_SUBSCR    
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  STORE_FAST               'd20'

 L. 364        22  LOAD_GLOBAL              float
               24  LOAD_FAST                'npk'
               26  LOAD_ATTR                params
               28  LOAD_STR                 'acqu'
               30  BINARY_SUBSCR    
               32  LOAD_STR                 '$D'
               34  BINARY_SUBSCR    
               36  LOAD_CONST               16
               38  BINARY_SUBSCR    
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  STORE_FAST               'd16'

 L. 365        44  LOAD_GLOBAL              float
               46  LOAD_FAST                'npk'
               48  LOAD_ATTR                params
               50  LOAD_STR                 'acqu'
               52  BINARY_SUBSCR    
               54  LOAD_STR                 '$D'
               56  BINARY_SUBSCR    
               58  LOAD_CONST               17
               60  BINARY_SUBSCR    
               62  CALL_FUNCTION_1       1  '1 positional argument'
               64  STORE_FAST               'd17'

 L. 366        66  LOAD_GLOBAL              float
               68  LOAD_FAST                'npk'
               70  LOAD_ATTR                params
               72  LOAD_STR                 'acqu'
               74  BINARY_SUBSCR    
               76  LOAD_STR                 '$P'
               78  BINARY_SUBSCR    
               80  LOAD_CONST               1
               82  BINARY_SUBSCR    
               84  CALL_FUNCTION_1       1  '1 positional argument'
               86  LOAD_CONST               1e-06
               88  BINARY_MULTIPLY  
               90  STORE_FAST               'p1'

 L. 367        92  LOAD_GLOBAL              float
               94  LOAD_FAST                'npk'
               96  LOAD_ATTR                params
               98  LOAD_STR                 'acqu'
              100  BINARY_SUBSCR    
              102  LOAD_STR                 '$P'
              104  BINARY_SUBSCR    
              106  LOAD_CONST               19
              108  BINARY_SUBSCR    
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  LOAD_CONST               1e-06
              114  BINARY_MULTIPLY  
              116  STORE_FAST               'p19'

 L. 368       118  LOAD_GLOBAL              float
              120  LOAD_FAST                'npk'
              122  LOAD_ATTR                params
              124  LOAD_STR                 'acqu'
              126  BINARY_SUBSCR    
              128  LOAD_STR                 '$P'
              130  BINARY_SUBSCR    
              132  LOAD_CONST               30
              134  BINARY_SUBSCR    
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  LOAD_CONST               1e-06
              140  BINARY_MULTIPLY  
              142  STORE_FAST               'p30'

 L. 370       144  LOAD_FAST                'npk'
              146  LOAD_ATTR                params
              148  LOAD_STR                 'acqu'
              150  BINARY_SUBSCR    
              152  LOAD_STR                 '$NUC1'
              154  BINARY_SUBSCR    
              156  STORE_FAST               'nuc1'

 L. 371       158  LOAD_FAST                'nucleus'
              160  LOAD_CONST               None
              162  COMPARE_OP               is
              164  POP_JUMP_IF_FALSE   224  'to 224'

 L. 372       166  LOAD_FAST                'nuc1'
              168  LOAD_STR                 '1H'
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_TRUE    214  'to 214'
              174  LOAD_FAST                'nuc1'
              176  LOAD_STR                 '15N'
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_TRUE    214  'to 214'
              182  LOAD_FAST                'nuc1'
              184  LOAD_STR                 '13C'
              186  COMPARE_OP               ==
              188  POP_JUMP_IF_TRUE    214  'to 214'
              190  LOAD_FAST                'nuc1'
              192  LOAD_STR                 '31P'
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_TRUE    214  'to 214'
              198  LOAD_FAST                'nuc1'
              200  LOAD_STR                 '19F'
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_TRUE    214  'to 214'
              206  LOAD_FAST                'nuc1'
              208  LOAD_STR                 '17O'
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_FALSE   220  'to 220'
            214_0  COME_FROM           204  '204'
            214_1  COME_FROM           196  '196'
            214_2  COME_FROM           188  '188'
            214_3  COME_FROM           180  '180'
            214_4  COME_FROM           172  '172'

 L. 373       214  LOAD_FAST                'nuc1'
              216  STORE_FAST               'nucleus'
              218  JUMP_FORWARD        224  'to 224'
            220_0  COME_FROM           212  '212'

 L. 375       220  LOAD_STR                 '1H'
              222  STORE_FAST               'nucleus'
            224_0  COME_FROM           218  '218'
            224_1  COME_FROM           164  '164'

 L. 376       224  LOAD_GLOBAL              print
              226  LOAD_STR                 'DOSY performed on %s'
              228  LOAD_FAST                'nucleus'
              230  BUILD_TUPLE_1         1 
              232  BINARY_MODULO    
              234  CALL_FUNCTION_1       1  '1 positional argument'
              236  POP_TOP          

 L. 377       238  LOAD_FAST                'npk'
              240  LOAD_ATTR                params
              242  LOAD_STR                 'acqu'
              244  BINARY_SUBSCR    
              246  LOAD_STR                 '$PULPROG'
              248  BINARY_SUBSCR    
              250  STORE_FAST               'pulprog'

 L. 378       252  LOAD_GLOBAL              determine_seqtype
              254  LOAD_FAST                'pulprog'
              256  LOAD_CONST               1
              258  LOAD_CONST               -1
              260  BUILD_SLICE_2         2 
              262  BINARY_SUBSCR    
              264  CALL_FUNCTION_1       1  '1 positional argument'
              266  STORE_FAST               'seq_type'

 L. 381       268  LOAD_FAST                'seq_type'
              270  LOAD_STR                 'bpp_ste_2echoes'
              272  COMPARE_OP               ==
          274_276  POP_JUMP_IF_FALSE   336  'to 336'

 L. 382       278  LOAD_CONST               2
              280  LOAD_FAST                'p30'
              282  BINARY_MULTIPLY  
              284  STORE_FAST               'litdelta'

 L. 383       286  LOAD_FAST                'd20'
              288  LOAD_CONST               10
              290  LOAD_FAST                'p1'
              292  BINARY_MULTIPLY  
              294  BINARY_SUBTRACT  
              296  LOAD_CONST               8
              298  LOAD_FAST                'p30'
              300  BINARY_MULTIPLY  
              302  BINARY_SUBTRACT  
              304  LOAD_CONST               8
              306  LOAD_FAST                'd16'
              308  BINARY_MULTIPLY  
              310  BINARY_SUBTRACT  
              312  LOAD_CONST               8
              314  LOAD_FAST                'd17'
              316  BINARY_MULTIPLY  
              318  BINARY_SUBTRACT  
              320  LOAD_CONST               2
              322  LOAD_FAST                'p19'
              324  BINARY_MULTIPLY  
              326  BINARY_SUBTRACT  
              328  STORE_FAST               'bigdelta'

 L. 384       330  LOAD_FAST                'd16'
              332  STORE_FAST               'recovery'
              334  JUMP_FORWARD        568  'to 568'
            336_0  COME_FROM           274  '274'

 L. 386       336  LOAD_FAST                'seq_type'
              338  LOAD_STR                 'ste_2echoes'
              340  COMPARE_OP               ==
          342_344  POP_JUMP_IF_FALSE   388  'to 388'

 L. 387       346  LOAD_FAST                'p30'
              348  STORE_FAST               'litdelta'

 L. 388       350  LOAD_CONST               2
              352  LOAD_FAST                'd20'
              354  LOAD_CONST               2
              356  LOAD_FAST                'p1'
              358  BINARY_MULTIPLY  
              360  BINARY_SUBTRACT  
              362  LOAD_FAST                'p30'
              364  BINARY_SUBTRACT  
              366  LOAD_CONST               2
              368  LOAD_FAST                'd16'
              370  BINARY_MULTIPLY  
              372  BINARY_SUBTRACT  
              374  LOAD_FAST                'p19'
              376  BINARY_SUBTRACT  
              378  BINARY_MULTIPLY  
              380  STORE_FAST               'bigdelta'

 L. 389       382  LOAD_FAST                'd16'
              384  STORE_FAST               'recovery'
              386  JUMP_FORWARD        568  'to 568'
            388_0  COME_FROM           342  '342'

 L. 391       388  LOAD_FAST                'seq_type'
              390  LOAD_STR                 'bpp_ste'
              392  COMPARE_OP               ==
          394_396  POP_JUMP_IF_FALSE   448  'to 448'

 L. 392       398  LOAD_CONST               2
              400  LOAD_FAST                'p30'
              402  BINARY_MULTIPLY  
              404  STORE_FAST               'litdelta'

 L. 393       406  LOAD_FAST                'd20'
              408  LOAD_CONST               4
              410  LOAD_FAST                'p1'
              412  BINARY_MULTIPLY  
              414  BINARY_SUBTRACT  
              416  LOAD_CONST               2
              418  LOAD_FAST                'p30'
              420  BINARY_MULTIPLY  
              422  BINARY_SUBTRACT  
              424  LOAD_CONST               3
              426  LOAD_FAST                'd16'
              428  BINARY_MULTIPLY  
              430  BINARY_SUBTRACT  
              432  LOAD_FAST                'p19'
              434  BINARY_SUBTRACT  
              436  STORE_FAST               'bigdelta'

 L. 394       438  LOAD_CONST               2
              440  LOAD_FAST                'd16'
              442  BINARY_MULTIPLY  
              444  STORE_FAST               'recovery'
              446  JUMP_FORWARD        568  'to 568'
            448_0  COME_FROM           394  '394'

 L. 396       448  LOAD_FAST                'seq_type'
              450  LOAD_STR                 'ste'
              452  COMPARE_OP               ==
          454_456  POP_JUMP_IF_FALSE   496  'to 496'

 L. 397       458  LOAD_FAST                'p30'
              460  STORE_FAST               'litdelta'

 L. 398       462  LOAD_FAST                'd20'
              464  LOAD_CONST               2
              466  LOAD_FAST                'p1'
              468  BINARY_MULTIPLY  
              470  BINARY_SUBTRACT  
              472  LOAD_FAST                'p30'
              474  BINARY_SUBTRACT  
              476  LOAD_CONST               2
              478  LOAD_FAST                'd16'
              480  BINARY_MULTIPLY  
              482  BINARY_SUBTRACT  
              484  LOAD_FAST                'p19'
              486  BINARY_SUBTRACT  
              488  STORE_FAST               'bigdelta'

 L. 399       490  LOAD_FAST                'd16'
              492  STORE_FAST               'recovery'
              494  JUMP_FORWARD        568  'to 568'
            496_0  COME_FROM           454  '454'

 L. 401       496  LOAD_FAST                'seq_type'
              498  LOAD_STR                 'oneshot'
              500  COMPARE_OP               ==
          502_504  POP_JUMP_IF_FALSE   556  'to 556'

 L. 402       506  LOAD_CONST               2
              508  LOAD_FAST                'p30'
              510  BINARY_MULTIPLY  
              512  STORE_FAST               'litdelta'

 L. 403       514  LOAD_FAST                'd20'
              516  LOAD_CONST               4
              518  LOAD_FAST                'p1'
              520  BINARY_MULTIPLY  
              522  BINARY_SUBTRACT  
              524  LOAD_CONST               2
              526  LOAD_FAST                'p30'
              528  BINARY_MULTIPLY  
              530  BINARY_SUBTRACT  
              532  LOAD_CONST               3
              534  LOAD_FAST                'd16'
              536  BINARY_MULTIPLY  
              538  BINARY_SUBTRACT  
              540  LOAD_FAST                'p19'
              542  BINARY_SUBTRACT  
              544  STORE_FAST               'bigdelta'

 L. 404       546  LOAD_CONST               2
              548  LOAD_FAST                'd16'
              550  BINARY_MULTIPLY  
              552  STORE_FAST               'recovery'
              554  JUMP_FORWARD        568  'to 568'
            556_0  COME_FROM           502  '502'

 L. 406       556  LOAD_FAST                'p30'
              558  STORE_FAST               'litdelta'

 L. 407       560  LOAD_FAST                'd20'
              562  STORE_FAST               'bigdelta'

 L. 408       564  LOAD_FAST                'd16'
              566  STORE_FAST               'recovery'
            568_0  COME_FROM           554  '554'
            568_1  COME_FROM           494  '494'
            568_2  COME_FROM           446  '446'
            568_3  COME_FROM           386  '386'
            568_4  COME_FROM           334  '334'

 L. 410       568  LOAD_GLOBAL              print
              570  LOAD_FAST                'litdelta'
              572  LOAD_FAST                'bigdelta'
              574  LOAD_FAST                'recovery'
              576  LOAD_FAST                'seq_type'
              578  LOAD_FAST                'nucleus'
              580  CALL_FUNCTION_5       5  '5 positional arguments'
              582  POP_TOP          

 L. 411       584  LOAD_GLOBAL              calibdosy
              586  LOAD_FAST                'litdelta'
              588  LOAD_FAST                'bigdelta'
              590  LOAD_FAST                'recovery'
              592  LOAD_FAST                'seq_type'
              594  LOAD_FAST                'nucleus'
              596  LOAD_CONST               ('seq_type', 'nucleus')
              598  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              600  LOAD_FAST                'npk'
              602  LOAD_ATTR                axis1
              604  STORE_ATTR               dfactor

 L. 412       606  LOAD_FAST                'npk'
              608  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 218


def Import_DOSY(fname, nucleus=None, verbose=False):
    """
    Import and calibrate DOSY data-set from a Bruker ser file
    """
    d = Import_2D(fname)
    d.axis1 = LaplaceAxis(size=(d.size1))
    dire = op.dirname(fname)
    d.axis1.load_qvalues(op.join(dire, 'difflist'))
    if d.axis1.size != len(d.axis1.qvalues):
        l = min(d.axis1.size, len(d.axis1.qvalues))
        print('WARNING in Import_DOSY(), size missmatch data is %d while difflist is %d' % (d.axis1.size, len(d.axis1.qvalues)))
        print('truncating to %d' % (l,))
        d.chsize(sz1=l)
        d.axis1.qvalues = d.axis1.qvalues[:l]
    d.calibdosy()
    if verbose:
        print('imported 2D DOSY, size = %d x %d\n%s' % (d.axis1.size, d.axis2.size, d.params['acqu']['title']))
    return d


def Import_DOSY_proc(fname, nucleus='1H', verbose=False):
    """
    Import and calibrate DOSY data-set from a Bruker 2rr file
    """
    d = Import_2D_proc(fname)
    d.axis1 = LaplaceAxis(size=(d.size1))
    dire = op.dirname(op.dirname(op.dirname(fname)))
    d.axis1.load_qvalues(op.join(dire, 'difflist'))
    d.calibdosy()
    Dmax = 10 ** (float(d.params['proc2']['$OFFSET']) + 12)
    width = float(d.params['proc2']['$SW_p']) / float(d.params['proc2']['$SF'])
    Dmin = Dmax * 10 ** (-width)
    d.reverse(axis=1)
    d.axis1.dmin = Dmin
    d.axis1.dmax = Dmax
    if verbose:
        print('imported 2D DOSY spectrum, size = %d x %d\n%s' % (d.axis1.size, d.axis2.size, d.params['acqu']['title']))
    return d


def process(param):
    """ do the elemental processing, used by loops"""
    icol, c, N, valmini, nbiter, lamda, precision, uncertainty = param
    if c[0] > valmini:
        y = c.get_buffer()
        c = c.palma(N, nbiter=nbiter, lamda=lamda, precision=precision, uncertainty=uncertainty)
        lchi2 = np.linalg.norm(y - np.dot(c.axis1.K, c.get_buffer()))
    else:
        c = c.set_buffer(np.zeros(N))
        lchi2 = 0
    return (
     icol, c, lchi2)


def do_palma(npkd, miniSNR=32, mppool=None, nbiter=1000, lamda=0.1, uncertainty=1.2, precision=1e-08):
    """
    realize PALMA computation on each column of the 2D datasets
    dataset should have been prepared with prepare_palma()
    
    the noise in the initial spectrum is analysed on the first DOSY increment
    then each column is processed with palma() if its intensity is sufficient

    miniSNR: determines the minimum Signal to Noise Ratio of the signal for allowing the processing
    mppool: if passed as a multiprocessing.Pool, it will be used for parallel processing
    
    the other parameters are transparently passed to palma()

    """
    import multiprocessing as mp
    import spike.util as pg
    from spike.util import widgets
    import sys
    if sys.version_info[0] < 3:
        import itertools
        imap = itertools.imap
    else:
        imap = map

    def palmaiter(npkd):
        for icol in np.random.permutation(npkd.size2):
            c = npkd.col(icol)
            yield (icol, c, N, valmini, nbiter, lamda, precision, uncertainty)

    if mppool is not None:
        if isinstance(mppool, mp.pool.Pool):
            paral = True
        else:
            raise Exception('parameter mpool should be either None or of multiprocessing.Pool type')
    else:
        paral = False
    npkd.check2D()
    K = npkd.axis1.K
    M, N = K.shape
    output = npkd.copy()
    output.chsize(sz1=N)
    chi2 = np.zeros(npkd.size2)
    noise = spike.util.signal_tools.findnoiselevel(npkd.row(0).get_buffer())
    valmini = noise * miniSNR
    xarg = palmaiter(npkd)
    wdg = ['PALMA: ', widgets.Percentage(), ' ', widgets.Bar(marker='-', left='[', right=']'), widgets.ETA()]
    pbar = pg.ProgressBar(widgets=wdg, maxval=(npkd.size2)).start()
    if paral:
        result = mppool.imap(process, xarg)
    else:
        result = imap(process, xarg)
    for ii, res in enumerate(result):
        pbar.update(ii + 1)
        sys.stdout.flush()
        icol, c, lchi2 = res
        chi2[icol] = lchi2
        output.set_col(icol, c)

    pbar.finish()
    output.axis1.chi2 = chi2
    return output


def prepare_palma(npkd, finalsize, Dmin, Dmax):
    """
    this method prepares a DOSY dataset for processing
    - computes experimental values from imported parameter file
    - prepare DOSY transformation matrix
    """
    npkd.check2D()
    M = npkd.size1
    N = finalsize
    t = npkd.axis1.qvalues ** 2
    t /= npkd.axis1.dfactor
    t = t.reshape((M, 1))
    npkd.axis1.dmin = Dmin
    npkd.axis1.dmax = Dmax
    targetaxis = LaplaceAxis(size=N)
    targetaxis.dmin = Dmin
    targetaxis.dmax = Dmax
    T = targetaxis.itod(np.arange(N))
    T = T.reshape((1, N))
    K = np.exp(-1 * np.kron(t, T))
    npkd.axis1.K = K
    Kt = np.transpose(K)
    KtK = np.dot(Kt, K)
    B = np.identity(N)
    B = B + KtK
    Binv = np.linalg.inv(B)
    npkd.axis1.Binv = Binv
    return npkd


def palma(npkd, N, nbiter=1000, uncertainty=1.0, lamda=0.1, precision=1e-08, full_output=False):
    """
    realize PALMA computation on a 1D dataset containing a decay
    dataset should have been prepared with prepare_palma
    on each column, the noise is estimated, then PPXA+ algorithm is applied
    nbiter: maximum iteration number of the PALMA algo
    
    uncertainty: noise is estimated on the dataset, and then multiplied by this value
        so uncertainty=1 is full confidence in the noise evaluation algo
        uncertainty>1 allows more room for algo when data quality is poor
    lamda is the balance between entropy and L1
        lamda = 0 is full L1
        lamda = 1 is full Ent
    
    precision: is the required precision for the convergence
    full_output is used for debugging purposes, do not use in production
        check PPXAplus() doc for details
    """
    NaN_found = 0
    npkd.check1D()
    K = npkd.axis1.K
    Binv = npkd.axis1.Binv
    y = npkd.get_buffer()
    M, Nk = K.shape
    if debug:
        print(npkd.size1, M, Nk, N)
    if npkd.size1 != M or Nk != N:
        raise Exception('Size missmatch in palma : %d x %d  while data is %d x %d' % (M, Nk, npkd.size1, N))
    evald_noise = eval_dosy_noise(y)
    y = y.reshape((M, 1))
    Ok = False
    while not Ok:
        eta = uncertainty * np.sqrt(M) * evald_noise
        if debug:
            print(' noise: %f  uncertainty: %f  eta: %f' % (evald_noise, uncertainty, eta))
        x, c = PPXAplus(K, Binv, y, eta, nbiter=nbiter, lamda=lamda, prec=precision, full_output=full_output)
        Ok = not np.isnan(x.sum())
        Ok or NaN_found += 1
        uncertainty *= 1.4

    npkd.set_buffer(x[:, 0])
    npkd.noise = eta
    if full_output:
        npkd.full_output = c
    if NaN_found > 0:
        print('%d NaN conditions encountered during PALMA processing' % NaN_found)
    return npkd


def test(npkd):
    print('Not implemented')


NPKData_plugin('palma', palma)
NPKData_plugin('do_palma', do_palma)
NPKData_plugin('prepare_palma', prepare_palma)
NPKData_plugin('calibdosy', dcalibdosy)