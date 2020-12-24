# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fdasrsf/regression.py
# Compiled at: 2019-08-08 11:30:55
# Size of source mod 2**32: 24195 bytes
"""
Warping Invariant Regression using SRSF

moduleauthor:: Derek Tucker <jdtuck@sandia.gov>

"""
import numpy as np
import fdasrsf.utility_functions as uf
from scipy import dot
from scipy.optimize import fmin_l_bfgs_b
from scipy.integrate import trapz
from scipy.linalg import inv, norm
from patsy import bs
from joblib import Parallel, delayed
import mlogit_warp as mw, collections

def elastic_regression(f, y, time, B=None, lam=0, df=20, max_itr=20, cores=-1, smooth=False):
    """
    This function identifies a regression model with phase-variablity
    using elastic methods

    :param f: numpy ndarray of shape (M,N) of N functions with M samples
    :param y: numpy array of N responses
    :param time: vector of size M describing the sample points
    :param B: optional matrix describing Basis elements
    :param lam: regularization parameter (default 0)
    :param df: number of degrees of freedom B-spline (default 20)
    :param max_itr: maximum number of iterations (default 20)
    :param cores: number of cores for parallel processing (default all)
    :type f: np.ndarray
    :type time: np.ndarray

    :rtype: tuple of numpy array
    :return alpha: alpha parameter of model
    :return beta: beta(t) of model
    :return fn: aligned functions - numpy ndarray of shape (M,N) of M
    functions with N samples
    :return qn: aligned srvfs - similar structure to fn
    :return gamma: calculated warping functions
    :return q: original training SRSFs
    :return B: basis matrix
    :return b: basis coefficients
    :return SSE: sum of squared error

    """
    M = f.shape[0]
    N = f.shape[1]
    if M > 500:
        parallel = True
    else:
        if N > 100:
            parallel = True
        else:
            parallel = False
    binsize = np.diff(time)
    binsize = binsize.mean()
    if B is None:
        B = bs(time, df=df, degree=4, include_intercept=True)
    Nb = B.shape[1]
    Bdiff = np.zeros((M, Nb))
    for ii in range(0, Nb):
        Bdiff[:, ii] = np.gradient(np.gradient(B[:, ii], binsize), binsize)

    q = uf.f_to_srsf(f, time, smooth)
    gamma = np.tile(np.linspace(0, 1, M), (N, 1))
    gamma = gamma.transpose()
    itr = 1
    SSE = np.zeros(max_itr)
    while itr <= max_itr:
        print('Iteration: %d' % itr)
        fn = np.zeros((M, N))
        qn = np.zeros((M, N))
        for ii in range(0, N):
            fn[:, ii] = np.interp((time[(-1)] - time[0]) * gamma[:, ii] + time[0], time, f[:, ii])
            qn[:, ii] = uf.warp_q_gamma(time, q[:, ii], gamma[:, ii])

        Phi = np.ones((N, Nb + 1))
        for ii in range(0, N):
            for jj in range(1, Nb + 1):
                Phi[(ii, jj)] = trapz(qn[:, ii] * B[:, jj - 1], time)

        R = np.zeros((Nb + 1, Nb + 1))
        for ii in range(1, Nb + 1):
            for jj in range(1, Nb + 1):
                R[(ii, jj)] = trapz(Bdiff[:, ii - 1] * Bdiff[:, jj - 1], time)

        xx = dot(Phi.T, Phi)
        inv_xx = inv(xx + lam * R)
        xy = dot(Phi.T, y)
        b = dot(inv_xx, xy)
        alpha = b[0]
        beta = B.dot(b[1:Nb + 1])
        beta = beta.reshape(M)
        int_X = np.zeros(N)
        for ii in range(0, N):
            int_X[ii] = trapz(qn[:, ii] * beta, time)

        SSE[itr - 1] = sum((y.reshape(N) - alpha - int_X) ** 2)
        gamma_new = np.zeros((M, N))
        if parallel:
            out = Parallel(n_jobs=cores)((delayed(regression_warp)(beta, time, q[:, n], y[n], alpha) for n in range(N)))
            gamma_new = np.array(out)
            gamma_new = gamma_new.transpose()
        else:
            for ii in range(0, N):
                gamma_new[:, ii] = regression_warp(beta, time, q[:, ii], y[ii], alpha)

        if norm(gamma - gamma_new) < 1e-05:
            break
        else:
            gamma = gamma_new
        itr += 1

    gamI = uf.SqrtMeanInverse(gamma_new)
    gamI_dev = np.gradient(gamI, 1 / float(M - 1))
    beta = np.interp((time[(-1)] - time[0]) * gamI + time[0], time, beta) * np.sqrt(gamI_dev)
    for ii in range(0, N):
        qn[:, ii] = np.interp((time[(-1)] - time[0]) * gamI + time[0], time, qn[:, ii]) * np.sqrt(gamI_dev)
        fn[:, ii] = np.interp((time[(-1)] - time[0]) * gamI + time[0], time, fn[:, ii])
        gamma[:, ii] = np.interp((time[(-1)] - time[0]) * gamI + time[0], time, gamma_new[:, ii])

    model = collections.namedtuple('model', ['alpha', 'beta', 'fn',
     'qn', 'gamma', 'q', 'B', 'b',
     'SSE', 'type'])
    out = model(alpha, beta, fn, qn, gamma, q, B, b[1:-1], SSE[0:itr], 'linear')
    return out


def elastic_logistic(f, y, time, B=None, df=20, max_itr=20, cores=-1, smooth=False):
    """
    This function identifies a logistic regression model with
    phase-variablity using elastic methods

    :param f: numpy ndarray of shape (M,N) of N functions with M samples
    :param y: numpy array of labels (1/-1)
    :param time: vector of size M describing the sample points
    :param B: optional matrix describing Basis elements
    :param df: number of degrees of freedom B-spline (default 20)
    :param max_itr: maximum number of iterations (default 20)
    :param cores: number of cores for parallel processing (default all)
    :type f: np.ndarray
    :type time: np.ndarray

    :rtype: tuple of numpy array
    :return alpha: alpha parameter of model
    :return beta: beta(t) of model
    :return fn: aligned functions - numpy ndarray of shape (M,N) of M
    functions with N samples
    :return qn: aligned srvfs - similar structure to fn
    :return gamma: calculated warping functions
    :return q: original training SRSFs
    :return B: basis matrix
    :return b: basis coefficients
    :return Loss: logistic loss

    """
    M = f.shape[0]
    N = f.shape[1]
    if M > 500:
        parallel = True
    else:
        if N > 100:
            parallel = True
        else:
            parallel = False
    binsize = np.diff(time)
    binsize = binsize.mean()
    if B is None:
        B = bs(time, df=df, degree=4, include_intercept=True)
    Nb = B.shape[1]
    q = uf.f_to_srsf(f, time, smooth)
    gamma = np.tile(np.linspace(0, 1, M), (N, 1))
    gamma = gamma.transpose()
    itr = 1
    LL = np.zeros(max_itr)
    while itr <= max_itr:
        print('Iteration: %d' % itr)
        fn = np.zeros((M, N))
        qn = np.zeros((M, N))
        for ii in range(0, N):
            fn[:, ii] = np.interp((time[(-1)] - time[0]) * gamma[:, ii] + time[0], time, f[:, ii])
            qn[:, ii] = uf.warp_q_gamma(time, q[:, ii], gamma[:, ii])

        Phi = np.ones((N, Nb + 1))
        for ii in range(0, N):
            for jj in range(1, Nb + 1):
                Phi[(ii, jj)] = trapz(qn[:, ii] * B[:, jj - 1], time)

        b0 = np.zeros(Nb + 1)
        out = fmin_l_bfgs_b(logit_loss, b0, fprime=logit_gradient, args=(
         Phi, y),
          pgtol=1e-10,
          maxiter=200,
          maxfun=250,
          factr=1e-30)
        b = out[0]
        alpha = b[0]
        beta = B.dot(b[1:Nb + 1])
        beta = beta.reshape(M)
        LL[itr - 1] = logit_loss(b, Phi, y)
        gamma_new = np.zeros((M, N))
        if parallel:
            out = Parallel(n_jobs=cores)((delayed(logistic_warp)(beta, time, q[:, n], y[n]) for n in range(N)))
            gamma_new = np.array(out)
            gamma_new = gamma_new.transpose()
        else:
            for ii in range(0, N):
                gamma_new[:, ii] = logistic_warp(beta, time, q[:, ii], y[ii])

        if norm(gamma - gamma_new) < 1e-05:
            break
        else:
            gamma = gamma_new
        itr += 1

    gamma = gamma_new
    model = collections.namedtuple('model', ['alpha', 'beta', 'fn',
     'qn', 'gamma', 'q', 'B', 'b',
     'Loss', 'type'])
    out = model(alpha, beta, fn, qn, gamma, q, B, b[1:-1], LL[0:itr], 'logistic')
    return out


def elastic_mlogistic(f, y, time, B=None, df=20, max_itr=20, cores=-1, delta=0.01, parallel=True, smooth=False):
    """
    This function identifies a multinomial logistic regression model with
    phase-variablity using elastic methods

    :param f: numpy ndarray of shape (M,N) of N functions with M samples
    :param y: numpy array of labels {1,2,...,m} for m classes
    :param time: vector of size M describing the sample points
    :param B: optional matrix describing Basis elements
    :param df: number of degrees of freedom B-spline (default 20)
    :param max_itr: maximum number of iterations (default 20)
    :param cores: number of cores for parallel processing (default all)
    :type f: np.ndarray
    :type time: np.ndarray

    :rtype: tuple of numpy array
    :return alpha: alpha parameter of model
    :return beta: beta(t) of model
    :return fn: aligned functions - numpy ndarray of shape (M,N) of N
    functions with M samples
    :return qn: aligned srvfs - similar structure to fn
    :return gamma: calculated warping functions
    :return q: original training SRSFs
    :return B: basis matrix
    :return b: basis coefficients
    :return Loss: logistic loss

    """
    M = f.shape[0]
    N = f.shape[1]
    m = y.max()
    Y = np.zeros((N, m), dtype=int)
    for ii in range(0, N):
        Y[(ii, y[ii] - 1)] = 1

    binsize = np.diff(time)
    binsize = binsize.mean()
    if B is None:
        B = bs(time, df=df, degree=4, include_intercept=True)
    Nb = B.shape[1]
    q = uf.f_to_srsf(f, time, smooth)
    gamma = np.tile(np.linspace(0, 1, M), (N, 1))
    gamma = gamma.transpose()
    itr = 1
    LL = np.zeros(max_itr)
    while itr <= max_itr:
        print('Iteration: %d' % itr)
        fn = np.zeros((M, N))
        qn = np.zeros((M, N))
        for ii in range(0, N):
            fn[:, ii] = np.interp((time[(-1)] - time[0]) * gamma[:, ii] + time[0], time, f[:, ii])
            qn[:, ii] = uf.warp_q_gamma(time, q[:, ii], gamma[:, ii])

        Phi = np.ones((N, Nb + 1))
        for ii in range(0, N):
            for jj in range(1, Nb + 1):
                Phi[(ii, jj)] = trapz(qn[:, ii] * B[:, jj - 1], time)

        b0 = np.zeros(m * (Nb + 1))
        out = fmin_l_bfgs_b(mlogit_loss, b0, fprime=mlogit_gradient, args=(
         Phi, Y),
          pgtol=1e-10,
          maxiter=200,
          maxfun=250,
          factr=1e-30)
        b = out[0]
        B0 = b.reshape(Nb + 1, m)
        alpha = B0[0, :]
        beta = np.zeros((M, m))
        for i in range(0, m):
            beta[:, i] = B.dot(B0[1:Nb + 1, i])

        LL[itr - 1] = mlogit_loss(b, Phi, Y)
        gamma_new = np.zeros((M, N))
        if parallel:
            out = Parallel(n_jobs=cores)((delayed(mlogit_warp_grad)(alpha, beta, time, (q[:, n]), (Y[n, :]), delta=delta) for n in range(N)))
            gamma_new = np.array(out)
            gamma_new = gamma_new.transpose()
        else:
            for ii in range(0, N):
                gamma_new[:, ii] = mlogit_warp_grad(alpha, beta, time, (q[:, ii]),
                  (Y[ii, :]), delta=delta)

        if norm(gamma - gamma_new) < 1e-05:
            break
        else:
            gamma = gamma_new
        itr += 1

    gamma = gamma_new
    model = collections.namedtuple('model', ['alpha', 'beta', 'fn',
     'qn', 'gamma', 'q', 'B', 'b',
     'Loss', 'n_classes', 'type'])
    out = model(alpha, beta, fn, qn, gamma, q, B, b[1:-1], LL[0:itr], m, 'mlogistic')
    return out


def elastic_prediction--- This code section failed: ---

 L. 429         0  LOAD_GLOBAL              uf
                2  LOAD_METHOD              f_to_srsf
                4  LOAD_FAST                'f'
                6  LOAD_FAST                'time'
                8  LOAD_FAST                'smooth'
               10  CALL_METHOD_3         3  '3 positional arguments'
               12  STORE_FAST               'q'

 L. 430        14  LOAD_FAST                'q'
               16  LOAD_ATTR                shape
               18  LOAD_CONST               1
               20  BINARY_SUBSCR    
               22  STORE_FAST               'n'

 L. 432        24  LOAD_FAST                'model'
               26  LOAD_ATTR                type
               28  LOAD_STR                 'linear'
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_TRUE     44  'to 44'
               34  LOAD_FAST                'model'
               36  LOAD_ATTR                type
               38  LOAD_STR                 'logistic'
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    56  'to 56'
             44_0  COME_FROM            32  '32'

 L. 433        44  LOAD_GLOBAL              np
               46  LOAD_METHOD              zeros
               48  LOAD_FAST                'n'
               50  CALL_METHOD_1         1  '1 positional argument'
               52  STORE_FAST               'y_pred'
               54  JUMP_FORWARD         86  'to 86'
             56_0  COME_FROM            42  '42'

 L. 434        56  LOAD_FAST                'model'
               58  LOAD_ATTR                type
               60  LOAD_STR                 'mlogistic'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    86  'to 86'

 L. 435        66  LOAD_FAST                'model'
               68  LOAD_ATTR                n_classes
               70  STORE_FAST               'm'

 L. 436        72  LOAD_GLOBAL              np
               74  LOAD_METHOD              zeros
               76  LOAD_FAST                'n'
               78  LOAD_FAST                'm'
               80  BUILD_TUPLE_2         2 
               82  CALL_METHOD_1         1  '1 positional argument'
               84  STORE_FAST               'y_pred'
             86_0  COME_FROM            64  '64'
             86_1  COME_FROM            54  '54'

 L. 438     86_88  SETUP_LOOP          374  'to 374'
               90  LOAD_GLOBAL              range
               92  LOAD_CONST               0
               94  LOAD_FAST                'n'
               96  CALL_FUNCTION_2       2  '2 positional arguments'
               98  GET_ITER         
            100_0  COME_FROM           300  '300'
          100_102  FOR_ITER            372  'to 372'
              104  STORE_FAST               'ii'

 L. 439       106  LOAD_FAST                'model'
              108  LOAD_ATTR                q
              110  LOAD_FAST                'q'
              112  LOAD_CONST               None
              114  LOAD_CONST               None
              116  BUILD_SLICE_2         2 
              118  LOAD_FAST                'ii'
              120  BUILD_TUPLE_2         2 
              122  BINARY_SUBSCR    
              124  LOAD_CONST               None
              126  LOAD_CONST               None
              128  BUILD_SLICE_2         2 
              130  LOAD_GLOBAL              np
              132  LOAD_ATTR                newaxis
              134  BUILD_TUPLE_2         2 
              136  BINARY_SUBSCR    
              138  BINARY_SUBTRACT  
              140  STORE_FAST               'diff'

 L. 440       142  LOAD_GLOBAL              np
              144  LOAD_ATTR                sum
              146  LOAD_GLOBAL              np
              148  LOAD_METHOD              abs
              150  LOAD_FAST                'diff'
              152  CALL_METHOD_1         1  '1 positional argument'
              154  LOAD_CONST               2
              156  BINARY_POWER     
              158  LOAD_CONST               0
              160  LOAD_CONST               ('axis',)
              162  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              164  LOAD_CONST               0.5
              166  BINARY_POWER     
              168  STORE_FAST               'dist'

 L. 441       170  LOAD_GLOBAL              uf
              172  LOAD_METHOD              warp_q_gamma
              174  LOAD_FAST                'time'
              176  LOAD_FAST                'q'
              178  LOAD_CONST               None
              180  LOAD_CONST               None
              182  BUILD_SLICE_2         2 
              184  LOAD_FAST                'ii'
              186  BUILD_TUPLE_2         2 
              188  BINARY_SUBSCR    

 L. 442       190  LOAD_FAST                'model'
              192  LOAD_ATTR                gamma
              194  LOAD_CONST               None
              196  LOAD_CONST               None
              198  BUILD_SLICE_2         2 
              200  LOAD_FAST                'dist'
              202  LOAD_METHOD              argmin
              204  CALL_METHOD_0         0  '0 positional arguments'
              206  BUILD_TUPLE_2         2 
              208  BINARY_SUBSCR    
              210  CALL_METHOD_3         3  '3 positional arguments'
              212  STORE_FAST               'q_tmp'

 L. 443       214  LOAD_FAST                'model'
              216  LOAD_ATTR                type
              218  LOAD_STR                 'linear'
              220  COMPARE_OP               ==
              222  POP_JUMP_IF_FALSE   252  'to 252'

 L. 444       224  LOAD_FAST                'model'
              226  LOAD_ATTR                alpha
              228  LOAD_GLOBAL              trapz
              230  LOAD_FAST                'q_tmp'
              232  LOAD_FAST                'model'
              234  LOAD_ATTR                beta
              236  BINARY_MULTIPLY  
              238  LOAD_FAST                'time'
              240  CALL_FUNCTION_2       2  '2 positional arguments'
              242  BINARY_ADD       
              244  LOAD_FAST                'y_pred'
              246  LOAD_FAST                'ii'
              248  STORE_SUBSCR     
              250  JUMP_BACK           100  'to 100'
            252_0  COME_FROM           222  '222'

 L. 445       252  LOAD_FAST                'model'
              254  LOAD_ATTR                type
              256  LOAD_STR                 'logistic'
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_FALSE   292  'to 292'

 L. 446       264  LOAD_FAST                'model'
              266  LOAD_ATTR                alpha
              268  LOAD_GLOBAL              trapz
              270  LOAD_FAST                'q_tmp'
              272  LOAD_FAST                'model'
              274  LOAD_ATTR                beta
              276  BINARY_MULTIPLY  
              278  LOAD_FAST                'time'
              280  CALL_FUNCTION_2       2  '2 positional arguments'
              282  BINARY_ADD       
              284  LOAD_FAST                'y_pred'
              286  LOAD_FAST                'ii'
              288  STORE_SUBSCR     
              290  JUMP_BACK           100  'to 100'
            292_0  COME_FROM           260  '260'

 L. 447       292  LOAD_FAST                'model'
              294  LOAD_ATTR                type
              296  LOAD_STR                 'mlogistic'
              298  COMPARE_OP               ==
              300  POP_JUMP_IF_FALSE   100  'to 100'

 L. 448       302  SETUP_LOOP          370  'to 370'
              304  LOAD_GLOBAL              range
              306  LOAD_CONST               0
              308  LOAD_FAST                'm'
              310  CALL_FUNCTION_2       2  '2 positional arguments'
              312  GET_ITER         
              314  FOR_ITER            368  'to 368'
              316  STORE_FAST               'jj'

 L. 449       318  LOAD_FAST                'model'
              320  LOAD_ATTR                alpha
              322  LOAD_FAST                'jj'
              324  BINARY_SUBSCR    
              326  LOAD_GLOBAL              trapz
              328  LOAD_FAST                'q_tmp'
              330  LOAD_FAST                'model'
              332  LOAD_ATTR                beta
              334  LOAD_CONST               None
              336  LOAD_CONST               None
              338  BUILD_SLICE_2         2 
              340  LOAD_FAST                'jj'
              342  BUILD_TUPLE_2         2 
              344  BINARY_SUBSCR    
              346  BINARY_MULTIPLY  
              348  LOAD_FAST                'time'
              350  CALL_FUNCTION_2       2  '2 positional arguments'
              352  BINARY_ADD       
              354  LOAD_FAST                'y_pred'
              356  LOAD_FAST                'ii'
              358  LOAD_FAST                'jj'
              360  BUILD_TUPLE_2         2 
              362  STORE_SUBSCR     
          364_366  JUMP_BACK           314  'to 314'
              368  POP_BLOCK        
            370_0  COME_FROM_LOOP      302  '302'
              370  JUMP_BACK           100  'to 100'
              372  POP_BLOCK        
            374_0  COME_FROM_LOOP       86  '86'

 L. 451       374  LOAD_FAST                'y'
              376  LOAD_CONST               None
              378  COMPARE_OP               is
          380_382  POP_JUMP_IF_FALSE   510  'to 510'

 L. 452       384  LOAD_FAST                'model'
              386  LOAD_ATTR                type
              388  LOAD_STR                 'linear'
              390  COMPARE_OP               ==
          392_394  POP_JUMP_IF_FALSE   402  'to 402'

 L. 453       396  LOAD_CONST               None
              398  STORE_FAST               'SSE'
              400  JUMP_FORWARD        982  'to 982'
            402_0  COME_FROM           392  '392'

 L. 454       402  LOAD_FAST                'model'
              404  LOAD_ATTR                type
              406  LOAD_STR                 'logistic'
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   450  'to 450'

 L. 455       414  LOAD_GLOBAL              phi
              416  LOAD_FAST                'y_pred'
              418  CALL_FUNCTION_1       1  '1 positional argument'
              420  STORE_FAST               'y_pred'

 L. 456       422  LOAD_GLOBAL              np
              424  LOAD_METHOD              ones
              426  LOAD_FAST                'n'
              428  CALL_METHOD_1         1  '1 positional argument'
              430  STORE_FAST               'y_labels'

 L. 457       432  LOAD_CONST               -1
              434  LOAD_FAST                'y_labels'
              436  LOAD_FAST                'y_pred'
              438  LOAD_CONST               0.5
              440  COMPARE_OP               <
              442  STORE_SUBSCR     

 L. 458       444  LOAD_CONST               None
              446  STORE_FAST               'PC'
              448  JUMP_FORWARD        982  'to 982'
            450_0  COME_FROM           410  '410'

 L. 459       450  LOAD_FAST                'model'
              452  LOAD_ATTR                type
              454  LOAD_STR                 'mlogistic'
              456  COMPARE_OP               ==
          458_460  POP_JUMP_IF_FALSE   982  'to 982'

 L. 460       462  LOAD_GLOBAL              phi
              464  LOAD_FAST                'y_pred'
              466  LOAD_METHOD              ravel
              468  CALL_METHOD_0         0  '0 positional arguments'
              470  CALL_FUNCTION_1       1  '1 positional argument'
              472  STORE_FAST               'y_pred'

 L. 461       474  LOAD_FAST                'y_pred'
              476  LOAD_METHOD              reshape
              478  LOAD_FAST                'n'
              480  LOAD_FAST                'm'
              482  CALL_METHOD_2         2  '2 positional arguments'
              484  STORE_FAST               'y_pred'

 L. 462       486  LOAD_FAST                'y_pred'
              488  LOAD_ATTR                argmax
              490  LOAD_CONST               1
              492  LOAD_CONST               ('axis',)
              494  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              496  LOAD_CONST               1
              498  BINARY_ADD       
              500  STORE_FAST               'y_labels'

 L. 463       502  LOAD_CONST               None
              504  STORE_FAST               'PC'
          506_508  JUMP_FORWARD        982  'to 982'
            510_0  COME_FROM           380  '380'

 L. 465       510  LOAD_FAST                'model'
              512  LOAD_ATTR                type
              514  LOAD_STR                 'linear'
              516  COMPARE_OP               ==
          518_520  POP_JUMP_IF_FALSE   542  'to 542'

 L. 466       522  LOAD_GLOBAL              sum
              524  LOAD_FAST                'y'
              526  LOAD_FAST                'y_pred'
              528  BINARY_SUBTRACT  
              530  LOAD_CONST               2
              532  BINARY_POWER     
              534  CALL_FUNCTION_1       1  '1 positional argument'
              536  STORE_FAST               'SSE'
          538_540  JUMP_FORWARD        982  'to 982'
            542_0  COME_FROM           518  '518'

 L. 467       542  LOAD_FAST                'model'
              544  LOAD_ATTR                type
              546  LOAD_STR                 'logistic'
              548  COMPARE_OP               ==
          550_552  POP_JUMP_IF_FALSE   696  'to 696'

 L. 468       554  LOAD_GLOBAL              phi
              556  LOAD_FAST                'y_pred'
              558  CALL_FUNCTION_1       1  '1 positional argument'
              560  STORE_FAST               'y_pred'

 L. 469       562  LOAD_GLOBAL              np
              564  LOAD_METHOD              ones
              566  LOAD_FAST                'n'
              568  CALL_METHOD_1         1  '1 positional argument'
              570  STORE_FAST               'y_labels'

 L. 470       572  LOAD_CONST               -1
              574  LOAD_FAST                'y_labels'
              576  LOAD_FAST                'y_pred'
              578  LOAD_CONST               0.5
              580  COMPARE_OP               <
              582  STORE_SUBSCR     

 L. 471       584  LOAD_GLOBAL              sum
              586  LOAD_FAST                'y'
              588  LOAD_FAST                'y_labels'
              590  LOAD_CONST               1
              592  COMPARE_OP               ==
              594  BINARY_SUBSCR    
              596  LOAD_CONST               1
              598  COMPARE_OP               ==
              600  CALL_FUNCTION_1       1  '1 positional argument'
              602  STORE_FAST               'TP'

 L. 472       604  LOAD_GLOBAL              sum
              606  LOAD_FAST                'y'
              608  LOAD_FAST                'y_labels'
              610  LOAD_CONST               -1
              612  COMPARE_OP               ==
              614  BINARY_SUBSCR    
              616  LOAD_CONST               1
              618  COMPARE_OP               ==
              620  CALL_FUNCTION_1       1  '1 positional argument'
              622  STORE_FAST               'FP'

 L. 473       624  LOAD_GLOBAL              sum
              626  LOAD_FAST                'y'
              628  LOAD_FAST                'y_labels'
              630  LOAD_CONST               -1
              632  COMPARE_OP               ==
              634  BINARY_SUBSCR    
              636  LOAD_CONST               -1
              638  COMPARE_OP               ==
              640  CALL_FUNCTION_1       1  '1 positional argument'
              642  STORE_FAST               'TN'

 L. 474       644  LOAD_GLOBAL              sum
              646  LOAD_FAST                'y'
              648  LOAD_FAST                'y_labels'
              650  LOAD_CONST               1
              652  COMPARE_OP               ==
              654  BINARY_SUBSCR    
              656  LOAD_CONST               -1
              658  COMPARE_OP               ==
              660  CALL_FUNCTION_1       1  '1 positional argument'
              662  STORE_FAST               'FN'

 L. 475       664  LOAD_FAST                'TP'
              666  LOAD_FAST                'TN'
              668  BINARY_ADD       
              670  LOAD_GLOBAL              float
              672  LOAD_FAST                'TP'
              674  LOAD_FAST                'FP'
              676  BINARY_ADD       
              678  LOAD_FAST                'FN'
              680  BINARY_ADD       
              682  LOAD_FAST                'TN'
              684  BINARY_ADD       
              686  CALL_FUNCTION_1       1  '1 positional argument'
              688  BINARY_TRUE_DIVIDE
              690  STORE_FAST               'PC'
          692_694  JUMP_FORWARD        982  'to 982'
            696_0  COME_FROM           550  '550'

 L. 476       696  LOAD_FAST                'model'
              698  LOAD_ATTR                type
              700  LOAD_STR                 'mlogistic'
              702  COMPARE_OP               ==
          704_706  POP_JUMP_IF_FALSE   982  'to 982'

 L. 477       708  LOAD_GLOBAL              phi
              710  LOAD_FAST                'y_pred'
              712  LOAD_METHOD              ravel
              714  CALL_METHOD_0         0  '0 positional arguments'
              716  CALL_FUNCTION_1       1  '1 positional argument'
              718  STORE_FAST               'y_pred'

 L. 478       720  LOAD_FAST                'y_pred'
              722  LOAD_METHOD              reshape
              724  LOAD_FAST                'n'
              726  LOAD_FAST                'm'
              728  CALL_METHOD_2         2  '2 positional arguments'
              730  STORE_FAST               'y_pred'

 L. 479       732  LOAD_FAST                'y_pred'
              734  LOAD_ATTR                argmax
              736  LOAD_CONST               1
              738  LOAD_CONST               ('axis',)
              740  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              742  LOAD_CONST               1
              744  BINARY_ADD       
              746  STORE_FAST               'y_labels'

 L. 480       748  LOAD_GLOBAL              np
              750  LOAD_METHOD              zeros
              752  LOAD_FAST                'm'
              754  CALL_METHOD_1         1  '1 positional argument'
              756  STORE_FAST               'PC'

 L. 481       758  LOAD_GLOBAL              np
              760  LOAD_METHOD              arange
              762  LOAD_CONST               1
              764  LOAD_FAST                'm'
              766  LOAD_CONST               1
              768  BINARY_ADD       
              770  CALL_METHOD_2         2  '2 positional arguments'
              772  STORE_FAST               'cls_set'

 L. 482       774  SETUP_LOOP          960  'to 960'
              776  LOAD_GLOBAL              range
              778  LOAD_CONST               0
              780  LOAD_FAST                'm'
              782  CALL_FUNCTION_2       2  '2 positional arguments'
              784  GET_ITER         
              786  FOR_ITER            958  'to 958'
              788  STORE_FAST               'ii'

 L. 483       790  LOAD_GLOBAL              np
              792  LOAD_METHOD              delete
              794  LOAD_FAST                'cls_set'
              796  LOAD_FAST                'ii'
              798  CALL_METHOD_2         2  '2 positional arguments'
              800  STORE_FAST               'cls_sub'

 L. 484       802  LOAD_GLOBAL              sum
              804  LOAD_FAST                'y'
              806  LOAD_FAST                'y_labels'
              808  LOAD_FAST                'ii'
              810  LOAD_CONST               1
              812  BINARY_ADD       
              814  COMPARE_OP               ==
              816  BINARY_SUBSCR    
              818  LOAD_FAST                'ii'
              820  LOAD_CONST               1
              822  BINARY_ADD       
              824  COMPARE_OP               ==
              826  CALL_FUNCTION_1       1  '1 positional argument'
              828  STORE_FAST               'TP'

 L. 485       830  LOAD_GLOBAL              sum
              832  LOAD_FAST                'y'
              834  LOAD_GLOBAL              np
              836  LOAD_METHOD              in1d
              838  LOAD_FAST                'y_labels'
              840  LOAD_FAST                'cls_sub'
              842  CALL_METHOD_2         2  '2 positional arguments'
              844  BINARY_SUBSCR    
              846  LOAD_FAST                'ii'
              848  LOAD_CONST               1
              850  BINARY_ADD       
              852  COMPARE_OP               ==
              854  CALL_FUNCTION_1       1  '1 positional argument'
              856  STORE_FAST               'FP'

 L. 486       858  LOAD_GLOBAL              sum
              860  LOAD_FAST                'y'
              862  LOAD_GLOBAL              np
              864  LOAD_METHOD              in1d
              866  LOAD_FAST                'y_labels'
              868  LOAD_FAST                'cls_sub'
              870  CALL_METHOD_2         2  '2 positional arguments'
              872  BINARY_SUBSCR    
            874_0  COME_FROM           400  '400'

 L. 487       874  LOAD_FAST                'y_labels'
              876  LOAD_GLOBAL              np
              878  LOAD_METHOD              in1d
              880  LOAD_FAST                'y_labels'
              882  LOAD_FAST                'cls_sub'
              884  CALL_METHOD_2         2  '2 positional arguments'
              886  BINARY_SUBSCR    
              888  COMPARE_OP               ==
              890  CALL_FUNCTION_1       1  '1 positional argument'
              892  STORE_FAST               'TN'

 L. 488       894  LOAD_GLOBAL              sum
              896  LOAD_GLOBAL              np
              898  LOAD_METHOD              in1d
              900  LOAD_FAST                'y'
              902  LOAD_FAST                'y_labels'
              904  LOAD_FAST                'ii'
              906  LOAD_CONST               1
              908  BINARY_ADD       
              910  COMPARE_OP               ==
              912  BINARY_SUBSCR    
              914  LOAD_FAST                'cls_sub'
              916  CALL_METHOD_2         2  '2 positional arguments'
              918  CALL_FUNCTION_1       1  '1 positional argument'
              920  STORE_FAST               'FN'
            922_0  COME_FROM           448  '448'

 L. 489       922  LOAD_FAST                'TP'
              924  LOAD_FAST                'TN'
              926  BINARY_ADD       
              928  LOAD_GLOBAL              float
              930  LOAD_FAST                'TP'
              932  LOAD_FAST                'FP'
              934  BINARY_ADD       
              936  LOAD_FAST                'FN'
              938  BINARY_ADD       
              940  LOAD_FAST                'TN'
              942  BINARY_ADD       
              944  CALL_FUNCTION_1       1  '1 positional argument'
              946  BINARY_TRUE_DIVIDE
              948  LOAD_FAST                'PC'
              950  LOAD_FAST                'ii'
              952  STORE_SUBSCR     
          954_956  JUMP_BACK           786  'to 786'
              958  POP_BLOCK        
            960_0  COME_FROM_LOOP      774  '774'

 L. 491       960  LOAD_GLOBAL              sum
              962  LOAD_FAST                'y'
              964  LOAD_FAST                'y_labels'
              966  COMPARE_OP               ==
              968  CALL_FUNCTION_1       1  '1 positional argument'
              970  LOAD_GLOBAL              float
              972  LOAD_FAST                'y_labels'
              974  LOAD_ATTR                size
              976  CALL_FUNCTION_1       1  '1 positional argument'
              978  BINARY_TRUE_DIVIDE
              980  STORE_FAST               'PC'
            982_0  COME_FROM           704  '704'
            982_1  COME_FROM           692  '692'
            982_2  COME_FROM           538  '538'
            982_3  COME_FROM           506  '506'
            982_4  COME_FROM           458  '458'

 L. 493       982  LOAD_FAST                'model'
              984  LOAD_ATTR                type
              986  LOAD_STR                 'linear'
              988  COMPARE_OP               ==
          990_992  POP_JUMP_IF_FALSE  1022  'to 1022'

 L. 494       994  LOAD_GLOBAL              collections
              996  LOAD_METHOD              namedtuple
              998  LOAD_STR                 'prediction'
             1000  LOAD_STR                 'y_pred'
             1002  LOAD_STR                 'SSE'
             1004  BUILD_LIST_2          2 
             1006  CALL_METHOD_2         2  '2 positional arguments'
             1008  STORE_FAST               'prediction'

 L. 495      1010  LOAD_FAST                'prediction'
             1012  LOAD_FAST                'y_pred'
             1014  LOAD_FAST                'SSE'
             1016  CALL_FUNCTION_2       2  '2 positional arguments'
             1018  STORE_FAST               'out'
             1020  JUMP_FORWARD       1108  'to 1108'
           1022_0  COME_FROM           990  '990'

 L. 496      1022  LOAD_FAST                'model'
             1024  LOAD_ATTR                type
             1026  LOAD_STR                 'logistic'
             1028  COMPARE_OP               ==
         1030_1032  POP_JUMP_IF_FALSE  1066  'to 1066'

 L. 497      1034  LOAD_GLOBAL              collections
             1036  LOAD_METHOD              namedtuple
             1038  LOAD_STR                 'prediction'
             1040  LOAD_STR                 'y_prob'

 L. 498      1042  LOAD_STR                 'y_labels'
             1044  LOAD_STR                 'PC'
             1046  BUILD_LIST_3          3 
             1048  CALL_METHOD_2         2  '2 positional arguments'
             1050  STORE_FAST               'prediction'

 L. 499      1052  LOAD_FAST                'prediction'
             1054  LOAD_FAST                'y_pred'
             1056  LOAD_FAST                'y_labels'
             1058  LOAD_FAST                'PC'
             1060  CALL_FUNCTION_3       3  '3 positional arguments'
             1062  STORE_FAST               'out'
             1064  JUMP_FORWARD       1108  'to 1108'
           1066_0  COME_FROM          1030  '1030'

 L. 500      1066  LOAD_FAST                'model'
             1068  LOAD_ATTR                type
             1070  LOAD_STR                 'mlogistic'
             1072  COMPARE_OP               ==
         1074_1076  POP_JUMP_IF_FALSE  1108  'to 1108'

 L. 501      1078  LOAD_GLOBAL              collections
             1080  LOAD_METHOD              namedtuple
             1082  LOAD_STR                 'prediction'
             1084  LOAD_STR                 'y_prob'

 L. 502      1086  LOAD_STR                 'y_labels'
             1088  LOAD_STR                 'PC'
             1090  BUILD_LIST_3          3 
             1092  CALL_METHOD_2         2  '2 positional arguments'
             1094  STORE_FAST               'prediction'

 L. 503      1096  LOAD_FAST                'prediction'
             1098  LOAD_FAST                'y_pred'
             1100  LOAD_FAST                'y_labels'
             1102  LOAD_FAST                'PC'
             1104  CALL_FUNCTION_3       3  '3 positional arguments'
             1106  STORE_FAST               'out'
           1108_0  COME_FROM          1074  '1074'
           1108_1  COME_FROM          1064  '1064'
           1108_2  COME_FROM          1020  '1020'

 L. 505      1108  LOAD_FAST                'out'
             1110  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 874_0


def regression_warp(beta, time, q, y, alpha):
    """
    calculates optimal warping for function linear regression

    :param beta: numpy ndarray of shape (M,N) of M functions with N samples
    :param time: vector of size N describing the sample points
    :param q: numpy ndarray of shape (M,N) of M functions with N samples
    :param y: numpy ndarray of shape (1,N) of M functions with N samples
    responses
    :param alpha: numpy scalar

    :rtype: numpy array
    :return gamma_new: warping function

    """
    gam_M = uf.optimum_reparam(beta, time, q)
    qM = uf.warp_q_gamma(time, q, gam_M)
    y_M = trapz(qM * beta, time)
    gam_m = uf.optimum_reparam(-1 * beta, time, q)
    qm = uf.warp_q_gamma(time, q, gam_m)
    y_m = trapz(qm * beta, time)
    if y > alpha + y_M:
        gamma_new = gam_M
    else:
        if y < alpha + y_m:
            gamma_new = gam_m
        else:
            gamma_new = uf.zero_crossing(y - alpha, q, beta, time, y_M, y_m, gam_M, gam_m)
    return gamma_new


def logistic_warp(beta, time, q, y):
    """
    calculates optimal warping for function logistic regression

    :param beta: numpy ndarray of shape (M,N) of N functions with M samples
    :param time: vector of size N describing the sample points
    :param q: numpy ndarray of shape (M,N) of N functions with M samples
    :param y: numpy ndarray of shape (1,N) responses

    :rtype: numpy array
    :return gamma: warping function

    """
    if y == 1:
        gamma = uf.optimum_reparam(beta, time, q)
    else:
        if y == -1:
            gamma = uf.optimum_reparam(-1 * beta, time, q)
    return gamma


def phi(t):
    """
    calculates logistic function, returns 1 / (1 + exp(-t))

    :param t: scalar

    :rtype: numpy array
    :return out: return value

    """
    idx = t > 0
    out = np.empty((t.size), dtype=(np.float))
    out[idx] = 1.0 / (1 + np.exp(-t[idx]))
    exp_t = np.exp(t[(~idx)])
    out[~idx] = exp_t / (1.0 + exp_t)
    return out


def logit_loss(b, X, y):
    """
    logistic loss function, returns Sum{-log(phi(t))}

    :param b: numpy ndarray of shape (M,N) of N functions with M samples
    :param X: numpy ndarray of shape (M,N) of N functions with M samples
    :param y: numpy ndarray of shape (1,N) of N responses

    :rtype: numpy array
    :return out: loss value

    """
    z = X.dot(b)
    yz = y * z
    idx = yz > 0
    out = np.zeros_like(yz)
    out[idx] = np.log(1 + np.exp(-yz[idx]))
    out[~idx] = -yz[(~idx)] + np.log(1 + np.exp(yz[(~idx)]))
    out = out.sum()
    return out


def logit_gradient(b, X, y):
    """
    calculates gradient of the logistic loss

    :param b: numpy ndarray of shape (M,N) of N functions with M samples
    :param X: numpy ndarray of shape (M,N) of N functions with M samples
    :param y: numpy ndarray of shape (1,N) responses

    :rtype: numpy array
    :return grad: gradient of logisitc loss

    """
    z = X.dot(b)
    z = phi(y * z)
    z0 = (z - 1) * y
    grad = X.T.dot(z0)
    return grad


def logit_hessian(s, b, X, y):
    """
    calculates hessian of the logistic loss

    :param s: numpy ndarray of shape (M,N) of N functions with M samples
    :param b: numpy ndarray of shape (M,N) of N functions with M samples
    :param X: numpy ndarray of shape (M,N) of N functions with M samples
    :param y: numpy ndarray of shape (1,N) responses

    :rtype: numpy array
    :return out: hessian of logistic loss

    """
    z = X.dot(b)
    z = phi(y * z)
    d = z * (1 - z)
    wa = d * X.dot(s)
    Hs = X.T.dot(wa)
    out = Hs
    return out


def mlogit_warp_grad(alpha, beta, time, q, y, max_itr=8000, tol=1e-10, delta=0.008, display=0):
    """
    calculates optimal warping for functional multinomial logistic regression

    :param alpha: scalar
    :param beta: numpy ndarray of shape (M,N) of N functions with M samples
    :param time: vector of size M describing the sample points
    :param q: numpy ndarray of shape (M,N) of N functions with M samples
    :param y: numpy ndarray of shape (1,N) responses
    :param max_itr: maximum number of iterations (Default=8000)
    :param tol: stopping tolerance (Default=1e-10)
    :param delta: gradient step size (Default=0.008)
    :param display: display iterations (Default=0)

    :rtype: tuple of numpy array
    :return gam_old: warping function

    """
    gam_old = mw.mlogit_warp(np.ascontiguousarray(alpha), np.ascontiguousarray(beta), time, np.ascontiguousarray(q), np.ascontiguousarray(y, dtype=(np.int32)), max_itr, tol, delta, display)
    return gam_old


def mlogit_loss(b, X, Y):
    """
    calculates multinomial logistic loss (negative log-likelihood)

    :param b: numpy ndarray of shape (M,N) of N functions with M samples
    :param X: numpy ndarray of shape (M,N) of N functions with M samples
    :param y: numpy ndarray of shape (1,N) responses

    :rtype: numpy array
    :return nll: negative log-likelihood

    """
    N, m = Y.shape
    M = X.shape[1]
    B = b.reshape(M, m)
    Yhat = np.dot(X, B)
    Yhat -= Yhat.min(axis=1)[:, np.newaxis]
    Yhat = np.exp(-Yhat)
    Yhat /= Yhat.sum(axis=1)[:, np.newaxis]
    Yhat = Yhat * Y
    nll = np.sum(np.log(Yhat.sum(axis=1)))
    nll /= -float(N)
    return nll


def mlogit_gradient(b, X, Y):
    """
    calculates gradient of the multinomial logistic loss

    :param b: numpy ndarray of shape (M,N) of N functions with M samples
    :param X: numpy ndarray of shape (M,N) of N functions with M samples
    :param y: numpy ndarray of shape (1,N) responses

    :rtype: numpy array
    :return grad: gradient

    """
    N, m = Y.shape
    M = X.shape[1]
    B = b.reshape(M, m)
    Yhat = np.dot(X, B)
    Yhat -= Yhat.min(axis=1)[:, np.newaxis]
    Yhat = np.exp(-Yhat)
    Yhat /= Yhat.sum(axis=1)[:, np.newaxis]
    _Yhat = Yhat * Y
    _Yhat /= _Yhat.sum(axis=1)[:, np.newaxis]
    Yhat -= _Yhat
    grad = np.dot(X.T, Yhat)
    grad /= -float(N)
    grad = grad.ravel()
    return grad