# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fdasrsf/curve_regression.py
# Compiled at: 2019-04-10 18:31:59
# Size of source mod 2**32: 26301 bytes
"""
Warping Invariant Regression using SRVF

moduleauthor:: Derek Tucker <jdtuck@sandia.gov>

"""
import numpy as np
import fdasrsf.utility_functions as uf
import fdasrsf.curve_functions as cf
from scipy import dot
from scipy.interpolate import interp1d
from scipy.optimize import fmin_l_bfgs_b
from scipy.integrate import trapz, cumtrapz
from scipy.linalg import inv, norm, expm
from patsy import bs
from joblib import Parallel, delayed
import ocmlogit_warp as mw, oclogit_warp as lw, collections
from IPython.core.debugger import Tracer

def oc_elastic_regression(beta, y, B=None, df=40, T=200, max_itr=20, cores=-1):
    """
    This function identifies a regression model for open curves
    using elastic methods

    :param beta: numpy ndarray of shape (n, M, N) describing N curves
    in R^M
    :param y: numpy array of N responses
    :param B: optional matrix describing Basis elements
    :param df: number of degrees of freedom B-spline (default 20)
    :param T: number of desired samples along curve (default 100)
    :param max_itr: maximum number of iterations (default 20)
    :param cores: number of cores for parallel processing (default all)
    :type beta: np.ndarray

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
    n = beta.shape[0]
    N = beta.shape[2]
    time = np.linspace(0, 1, T)
    if n > 500:
        parallel = True
    else:
        if T > 100:
            parallel = True
        else:
            parallel = False
    if B is None:
        B = bs(time, df=df, degree=4, include_intercept=True)
    Nb = B.shape[1]
    q, beta = preproc_open_curve(beta, T)
    beta0 = beta.copy()
    qn = q.copy()
    gamma = np.tile(np.linspace(0, 1, T), (N, 1))
    gamma = gamma.transpose()
    O_hat = np.tile(np.eye(n), (N, 1, 1)).T
    itr = 1
    SSE = np.zeros(max_itr)
    while itr <= max_itr:
        print('Iteration: %d' % itr)
        Phi = np.ones((N, n * Nb + 1))
        for ii in range(0, N):
            for jj in range(0, n):
                for kk in range(1, Nb + 1):
                    Phi[(ii, jj * Nb + kk)] = trapz(qn[jj, :, ii] * B[:, kk - 1], time)

        xx = dot(Phi.T, Phi)
        inv_xx = inv(xx)
        xy = dot(Phi.T, y)
        b = dot(inv_xx, xy)
        alpha = b[0]
        nu = np.zeros((n, T))
        for ii in range(0, n):
            nu[ii, :] = B.dot(b[ii * Nb + 1:(ii + 1) * Nb + 1])

        int_X = np.zeros(N)
        for ii in range(0, N):
            int_X[ii] = cf.innerprod_q2(qn[:, :, ii], nu)

        SSE[itr - 1] = sum((y.reshape(N) - alpha - int_X) ** 2)
        gamma_new = np.zeros((T, N))
        if parallel:
            out = Parallel(n_jobs=cores)((delayed(regression_warp)(nu, beta0[:, :, n], y[n], alpha) for n in range(N)))
            for ii in range(0, N):
                gamma_new[:, ii] = out[ii][0]
                beta1n = cf.group_action_by_gamma_coord(out[ii][1].dot(beta0[:, :, ii]), out[ii][0])
                beta[:, :, ii] = beta1n
                O_hat[:, :, ii] = out[ii][1]
                qn[:, :, ii] = cf.curve_to_q(beta[:, :, ii])

        else:
            for ii in range(0, N):
                beta1 = beta0[:, :, ii]
                gammatmp, Otmp, tau = regression_warp(nu, beta1, y[ii], alpha)
                gamma_new[:, ii] = gammatmp
                beta1n = cf.group_action_by_gamma_coord(Otmp.dot(beta0[:, :, ii]), gammatmp)
                beta[:, :, ii] = beta1n
                O_hat[:, :, ii] = Otmp
                qn[:, :, ii] = cf.curve_to_q(beta[:, :, ii])

        if np.abs(SSE[(itr - 1)] - SSE[(itr - 2)]) < 1e-15:
            break
        else:
            gamma = gamma_new
        itr += 1

    tau = np.zeros(N)
    model = collections.namedtuple('model', ['alpha', 'nu', 'betanq', 'gamma',
     'O', 'tau', 'B', 'b', 'SSE', 'type'])
    out = model(alpha, nu, beta, q, gamma, O_hat, tau, B, b[1:-1], SSE[0:itr], 'oclinear')
    return out


def oc_elastic_logistic(beta, y, B=None, df=60, T=100, max_itr=40, cores=-1, deltaO=0.1, deltag=0.05, method=1):
    """
    This function identifies a logistic regression model with
    phase-variablity using elastic methods for open curves

    :param beta: numpy ndarray of shape (n, M, N) describing N curves
    in R^M
    :param y: numpy array of N responses
    :param B: optional matrix describing Basis elements
    :param df: number of degrees of freedom B-spline (default 20)
    :param T: number of desired samples along curve (default 100)
    :param max_itr: maximum number of iterations (default 20)
    :param cores: number of cores for parallel processing (default all)
    :type beta: np.ndarray

    :rtype: tuple of numpy array
    :return alpha: alpha parameter of model
    :return nu: nu(t) of model
    :return betan: aligned curves - numpy ndarray of shape (n,T,N)
    :return O: calulated rotation matrices
    :return gamma: calculated warping functions
    :return B: basis matrix
    :return b: basis coefficients
    :return Loss: logistic loss

    """
    n = beta.shape[0]
    N = beta.shape[2]
    time = np.linspace(0, 1, T)
    if n > 500:
        parallel = True
    else:
        if T > 100:
            parallel = True
        else:
            parallel = True
    if B is None:
        B = bs(time, df=df, degree=4, include_intercept=True)
    Nb = B.shape[1]
    q, beta = preproc_open_curve(beta, T)
    beta0 = beta.copy()
    qn = q.copy()
    gamma = np.tile(np.linspace(0, 1, T), (N, 1))
    gamma = gamma.transpose()
    O_hat = np.tile(np.eye(n), (N, 1, 1)).T
    itr = 1
    LL = np.zeros(max_itr + 1)
    while itr <= max_itr:
        print('Iteration: %d' % itr)
        Phi = np.ones((N, n * Nb + 1))
        for ii in range(0, N):
            for jj in range(0, n):
                for kk in range(1, Nb + 1):
                    Phi[(ii, jj * Nb + kk)] = trapz(qn[jj, :, ii] * B[:, kk - 1], time)

        b0 = np.zeros(n * Nb + 1)
        out = fmin_l_bfgs_b(logit_loss, b0, fprime=logit_gradient, args=(
         Phi, y),
          pgtol=1e-10,
          maxiter=200,
          maxfun=250,
          factr=1e-30)
        b = out[0]
        b = b / norm(b)
        alpha = b[0]
        nu = np.zeros((n, T))
        for ii in range(0, n):
            nu[ii, :] = B.dot(b[ii * Nb + 1:(ii + 1) * Nb + 1])

        LL[itr] = logit_loss(b, Phi, y)
        gamma_new = np.zeros((T, N))
        if parallel:
            out = Parallel(n_jobs=cores)((delayed(logistic_warp)(alpha, nu, (q[:, :, ii]), (y[ii]), deltaO=deltaO, deltag=deltag, method=method) for ii in range(N)))
            for ii in range(0, N):
                gamma_new[:, ii] = out[ii][0]
                beta1n = cf.group_action_by_gamma_coord(out[ii][1].dot(beta0[:, :, ii]), out[ii][0])
                beta[:, :, ii] = beta1n
                O_hat[:, :, ii] = out[ii][1]
                if not np.isinf(beta1n).any():
                    if np.isnan(beta1n).any():
                        Tracer()()
                    qn[:, :, ii] = cf.curve_to_q(beta[:, :, ii])

        else:
            for ii in range(0, N):
                q1 = q[:, :, ii]
                gammatmp, Otmp, tautmp = logistic_warp(alpha, nu, q1, (y[ii]), deltaO=deltaO, deltag=deltag, method=method)
                gamma_new[:, ii] = gammatmp
                beta1n = cf.group_action_by_gamma_coord(Otmp.dot(beta0[:, :, ii]), gammatmp)
                beta[:, :, ii] = beta1n
                O_hat[:, :, ii] = Otmp
                qn[:, :, ii] = cf.curve_to_q(beta[:, :, ii])

        if norm(gamma - gamma_new) < 1e-05:
            break
        else:
            gamma = gamma_new.copy()
        itr += 1

    tau = np.zeros(N)
    model = collections.namedtuple('model', ['alpha', 'nu', 'betan', 'q',
     'gamma', 'O', 'tau', 'B', 'b', 'Loss',
     'type'])
    out = model(alpha, nu, beta, q, gamma_new, O_hat, tau, B, b[1:-1], LL[1:itr], 'oclogistic')
    return out


def oc_elastic_mlogistic(beta, y, B=None, df=20, T=100, max_itr=30, cores=-1, deltaO=0.003, deltag=0.003):
    """
    This function identifies a multinomial logistic regression model with
    phase-variability using elastic methods for open curves

    :param beta: numpy ndarray of shape (n, M, N) describing N curves
    in R^M
    :param y: numpy array of labels {1,2,...,m} for m classes
    :param B: optional matrix describing Basis elements
    :param df: number of degrees of freedom B-spline (default 20)
    :param T: number of desired samples along curve (default 100)
    :param max_itr: maximum number of iterations (default 20)
    :param cores: number of cores for parallel processing (default all)
    :type beta: np.ndarray

    :rtype: tuple of numpy array
    :return alpha: alpha parameter of model
    :return nu: nu(t) of model
    :return betan: aligned curves - numpy ndarray of shape (n,T,N)
    :return O: calculated rotation matrices
    :return gamma: calculated warping functions
    :return B: basis matrix
    :return b: basis coefficients
    :return Loss: logistic loss

    """
    n = beta.shape[0]
    N = beta.shape[2]
    time = np.linspace(0, 1, T)
    if n > 500:
        parallel = True
    else:
        if T > 100:
            parallel = True
        else:
            parallel = True
    m = y.max()
    Y = np.zeros((N, m), dtype=int)
    for ii in range(0, N):
        Y[(ii, y[ii] - 1)] = 1

    if B is None:
        B = bs(time, df=df, degree=4, include_intercept=True)
    Nb = B.shape[1]
    q, beta = preproc_open_curve(beta, T)
    qn = q.copy()
    beta0 = beta.copy()
    gamma = np.tile(np.linspace(0, 1, T), (N, 1))
    gamma = gamma.transpose()
    O_hat = np.tile(np.eye(n), (N, 1, 1)).T
    itr = 1
    LL = np.zeros(max_itr + 1)
    while itr <= max_itr:
        print('Iteration: %d' % itr)
        Phi = np.ones((N, n * Nb + 1))
        for ii in range(0, N):
            for jj in range(0, n):
                for kk in range(1, Nb + 1):
                    Phi[(ii, jj * Nb + kk)] = trapz(qn[jj, :, ii] * B[:, kk - 1], time)

        b0 = np.zeros(m * (n * Nb + 1))
        out = fmin_l_bfgs_b(mlogit_loss, b0, fprime=mlogit_gradient, args=(
         Phi, Y),
          pgtol=1e-10,
          maxiter=200,
          maxfun=250,
          factr=1e-30)
        b = out[0]
        B0 = b.reshape(n * Nb + 1, m)
        alpha = B0[0, :]
        nu = np.zeros((n, T, m))
        for i in range(0, m):
            for j in range(0, n):
                nu[j, :, i] = B.dot(B0[j * Nb + 1:(j + 1) * Nb + 1, i])

        LL[itr] = mlogit_loss(b, Phi, Y)
        gamma_new = np.zeros((T, N))
        if parallel:
            out = Parallel(n_jobs=cores)((delayed(mlogit_warp_grad)(alpha, nu, (q[:, :, n]), (Y[n, :]), deltaO=deltaO, deltag=deltag) for n in range(N)))
            for ii in range(0, N):
                gamma_new[:, ii] = out[ii][0]
                beta1n = cf.group_action_by_gamma_coord(out[ii][1].dot(beta0[:, :, ii]), out[ii][0])
                beta[:, :, ii] = beta1n
                O_hat[:, :, ii] = out[ii][1]
                qn[:, :, ii] = cf.curve_to_q(beta[:, :, ii])

        else:
            for ii in range(0, N):
                gammatmp, Otmp = mlogit_warp_grad(alpha, nu, (q[:, :, ii]), (Y[ii, :]), deltaO=deltaO, deltag=deltag)
                gamma_new[:, ii] = gammatmp
                beta1n = cf.group_action_by_gamma_coord(Otmp.dot(beta0[:, :, ii]), gammatmp)
                beta[:, :, ii] = beta1n
                O_hat[:, :, ii] = Otmp
                qn[:, :, ii] = cf.curve_to_q(beta[:, :, ii])

        if norm(gamma - gamma_new) < 1e-05:
            break
        else:
            gamma = gamma_new.copy()
        itr += 1

    model = collections.namedtuple('model', ['alpha', 'nu', 'betan', 'q',
     'gamma', 'O', 'B', 'b',
     'Loss', 'n_classes', 'type'])
    out = model(alpha, nu, beta, q, gamma_new, O_hat, B, b[1:-1], LL[1:itr], m, 'ocmlogistic')
    return out


def oc_elastic_prediction--- This code section failed: ---

 L. 399         0  LOAD_FAST                'model'
                2  LOAD_ATTR                q
                4  LOAD_ATTR                shape
                6  LOAD_CONST               1
                8  BINARY_SUBSCR    
               10  STORE_FAST               'T'

 L. 400        12  LOAD_FAST                'beta'
               14  LOAD_ATTR                shape
               16  LOAD_CONST               2
               18  BINARY_SUBSCR    
               20  STORE_FAST               'n'

 L. 401        22  LOAD_FAST                'model'
               24  LOAD_ATTR                q
               26  LOAD_ATTR                shape
               28  LOAD_CONST               2
               30  BINARY_SUBSCR    
               32  STORE_FAST               'N'

 L. 403        34  LOAD_GLOBAL              preproc_open_curve
               36  LOAD_FAST                'beta'
               38  LOAD_FAST                'T'
               40  CALL_FUNCTION_2       2  '2 positional arguments'
               42  UNPACK_SEQUENCE_2     2 
               44  STORE_FAST               'q'
               46  STORE_FAST               'beta'

 L. 405        48  LOAD_FAST                'model'
               50  LOAD_ATTR                type
               52  LOAD_STR                 'oclinear'
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_TRUE     68  'to 68'
               58  LOAD_FAST                'model'
               60  LOAD_ATTR                type
               62  LOAD_STR                 'oclogistic'
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    80  'to 80'
             68_0  COME_FROM            56  '56'

 L. 406        68  LOAD_GLOBAL              np
               70  LOAD_METHOD              zeros
               72  LOAD_FAST                'n'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               'y_pred'
               78  JUMP_FORWARD        110  'to 110'
             80_0  COME_FROM            66  '66'

 L. 407        80  LOAD_FAST                'model'
               82  LOAD_ATTR                type
               84  LOAD_STR                 'ocmlogistic'
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   110  'to 110'

 L. 408        90  LOAD_FAST                'model'
               92  LOAD_ATTR                n_classes
               94  STORE_FAST               'm'

 L. 409        96  LOAD_GLOBAL              np
               98  LOAD_METHOD              zeros
              100  LOAD_FAST                'n'
              102  LOAD_FAST                'm'
              104  BUILD_TUPLE_2         2 
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               'y_pred'
            110_0  COME_FROM            88  '88'
            110_1  COME_FROM            78  '78'

 L. 411   110_112  SETUP_LOOP          558  'to 558'
              114  LOAD_GLOBAL              range
              116  LOAD_CONST               0
              118  LOAD_FAST                'n'
              120  CALL_FUNCTION_2       2  '2 positional arguments'
              122  GET_ITER         
            124_0  COME_FROM           480  '480'
          124_126  FOR_ITER            556  'to 556'
              128  STORE_FAST               'ii'

 L. 412       130  LOAD_FAST                'model'
              132  LOAD_ATTR                q
              134  LOAD_FAST                'q'
              136  LOAD_CONST               None
              138  LOAD_CONST               None
              140  BUILD_SLICE_2         2 
              142  LOAD_CONST               None
              144  LOAD_CONST               None
              146  BUILD_SLICE_2         2 
              148  LOAD_FAST                'ii'
              150  BUILD_TUPLE_3         3 
              152  BINARY_SUBSCR    
              154  LOAD_CONST               None
              156  LOAD_CONST               None
              158  BUILD_SLICE_2         2 
              160  LOAD_CONST               None
              162  LOAD_CONST               None
              164  BUILD_SLICE_2         2 
              166  LOAD_GLOBAL              np
              168  LOAD_ATTR                newaxis
              170  BUILD_TUPLE_3         3 
              172  BINARY_SUBSCR    
              174  BINARY_SUBTRACT  
              176  STORE_FAST               'diff'

 L. 414       178  LOAD_GLOBAL              np
              180  LOAD_METHOD              zeros
              182  LOAD_FAST                'N'
              184  CALL_METHOD_1         1  '1 positional argument'
              186  STORE_FAST               'dist'

 L. 415       188  SETUP_LOOP          252  'to 252'
              190  LOAD_GLOBAL              range
              192  LOAD_CONST               0
              194  LOAD_FAST                'N'
              196  CALL_FUNCTION_2       2  '2 positional arguments'
              198  GET_ITER         
              200  FOR_ITER            250  'to 250'
              202  STORE_FAST               'jj'

 L. 416       204  LOAD_GLOBAL              np
              206  LOAD_ATTR                linalg
              208  LOAD_METHOD              norm
              210  LOAD_GLOBAL              np
              212  LOAD_METHOD              abs
              214  LOAD_FAST                'diff'
              216  LOAD_CONST               None
              218  LOAD_CONST               None
              220  BUILD_SLICE_2         2 
              222  LOAD_CONST               None
              224  LOAD_CONST               None
              226  BUILD_SLICE_2         2 
              228  LOAD_FAST                'jj'
              230  BUILD_TUPLE_3         3 
              232  BINARY_SUBSCR    
              234  CALL_METHOD_1         1  '1 positional argument'
              236  CALL_METHOD_1         1  '1 positional argument'
              238  LOAD_CONST               2
              240  BINARY_POWER     
              242  LOAD_FAST                'dist'
              244  LOAD_FAST                'jj'
              246  STORE_SUBSCR     
              248  JUMP_BACK           200  'to 200'
              250  POP_BLOCK        
            252_0  COME_FROM_LOOP      188  '188'

 L. 417       252  LOAD_FAST                'model'
              254  LOAD_ATTR                type
              256  LOAD_STR                 'oclinear'
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_TRUE    276  'to 276'
              264  LOAD_FAST                'model'
              266  LOAD_ATTR                type
              268  LOAD_STR                 'oclogistic'
              270  COMPARE_OP               ==
          272_274  POP_JUMP_IF_FALSE   300  'to 300'
            276_0  COME_FROM           260  '260'

 L. 419       276  LOAD_FAST                'beta'
              278  LOAD_CONST               None
              280  LOAD_CONST               None
              282  BUILD_SLICE_2         2 
              284  LOAD_CONST               None
              286  LOAD_CONST               None
              288  BUILD_SLICE_2         2 
              290  LOAD_FAST                'ii'
              292  BUILD_TUPLE_3         3 
              294  BINARY_SUBSCR    
              296  STORE_FAST               'beta1'
              298  JUMP_FORWARD        322  'to 322'
            300_0  COME_FROM           272  '272'

 L. 421       300  LOAD_FAST                'beta'
              302  LOAD_CONST               None
              304  LOAD_CONST               None
              306  BUILD_SLICE_2         2 
              308  LOAD_CONST               None
              310  LOAD_CONST               None
              312  BUILD_SLICE_2         2 
              314  LOAD_FAST                'ii'
              316  BUILD_TUPLE_3         3 
              318  BINARY_SUBSCR    
              320  STORE_FAST               'beta1'
            322_0  COME_FROM           298  '298'

 L. 422       322  LOAD_FAST                'model'
              324  LOAD_ATTR                O
              326  LOAD_CONST               None
              328  LOAD_CONST               None
              330  BUILD_SLICE_2         2 
              332  LOAD_CONST               None
              334  LOAD_CONST               None
              336  BUILD_SLICE_2         2 
              338  LOAD_FAST                'dist'
              340  LOAD_METHOD              argmin
              342  CALL_METHOD_0         0  '0 positional arguments'
              344  BUILD_TUPLE_3         3 
              346  BINARY_SUBSCR    
              348  LOAD_METHOD              dot
              350  LOAD_FAST                'beta1'
              352  CALL_METHOD_1         1  '1 positional argument'
              354  STORE_FAST               'beta1'

 L. 423       356  LOAD_GLOBAL              cf
              358  LOAD_METHOD              group_action_by_gamma_coord
              360  LOAD_FAST                'beta1'

 L. 424       362  LOAD_FAST                'model'
              364  LOAD_ATTR                gamma
              366  LOAD_CONST               None
              368  LOAD_CONST               None
              370  BUILD_SLICE_2         2 
              372  LOAD_FAST                'dist'
              374  LOAD_METHOD              argmin
              376  CALL_METHOD_0         0  '0 positional arguments'
              378  BUILD_TUPLE_2         2 
              380  BINARY_SUBSCR    
              382  CALL_METHOD_2         2  '2 positional arguments'
              384  STORE_FAST               'beta1'

 L. 425       386  LOAD_GLOBAL              cf
              388  LOAD_METHOD              curve_to_q
              390  LOAD_FAST                'beta1'
              392  CALL_METHOD_1         1  '1 positional argument'
              394  STORE_FAST               'q_tmp'

 L. 427       396  LOAD_FAST                'model'
              398  LOAD_ATTR                type
              400  LOAD_STR                 'oclinear'
              402  COMPARE_OP               ==
          404_406  POP_JUMP_IF_FALSE   434  'to 434'

 L. 428       408  LOAD_FAST                'model'
              410  LOAD_ATTR                alpha
              412  LOAD_GLOBAL              cf
              414  LOAD_METHOD              innerprod_q2
              416  LOAD_FAST                'q_tmp'
              418  LOAD_FAST                'model'
              420  LOAD_ATTR                nu
              422  CALL_METHOD_2         2  '2 positional arguments'
              424  BINARY_ADD       
              426  LOAD_FAST                'y_pred'
              428  LOAD_FAST                'ii'
              430  STORE_SUBSCR     
              432  JUMP_BACK           124  'to 124'
            434_0  COME_FROM           404  '404'

 L. 429       434  LOAD_FAST                'model'
              436  LOAD_ATTR                type
              438  LOAD_STR                 'oclogistic'
              440  COMPARE_OP               ==
          442_444  POP_JUMP_IF_FALSE   472  'to 472'

 L. 430       446  LOAD_FAST                'model'
              448  LOAD_ATTR                alpha
              450  LOAD_GLOBAL              cf
              452  LOAD_METHOD              innerprod_q2
              454  LOAD_FAST                'q_tmp'
              456  LOAD_FAST                'model'
              458  LOAD_ATTR                nu
              460  CALL_METHOD_2         2  '2 positional arguments'
              462  BINARY_ADD       
              464  LOAD_FAST                'y_pred'
              466  LOAD_FAST                'ii'
              468  STORE_SUBSCR     
              470  JUMP_BACK           124  'to 124'
            472_0  COME_FROM           442  '442'

 L. 431       472  LOAD_FAST                'model'
              474  LOAD_ATTR                type
              476  LOAD_STR                 'ocmlogistic'
              478  COMPARE_OP               ==
              480  POP_JUMP_IF_FALSE   124  'to 124'

 L. 432       482  SETUP_LOOP          554  'to 554'
              484  LOAD_GLOBAL              range
              486  LOAD_CONST               0
              488  LOAD_FAST                'm'
              490  CALL_FUNCTION_2       2  '2 positional arguments'
              492  GET_ITER         
              494  FOR_ITER            552  'to 552'
              496  STORE_FAST               'jj'

 L. 433       498  LOAD_FAST                'model'
              500  LOAD_ATTR                alpha
              502  LOAD_FAST                'jj'
              504  BINARY_SUBSCR    
              506  LOAD_GLOBAL              cf
              508  LOAD_METHOD              innerprod_q2
              510  LOAD_FAST                'q_tmp'
              512  LOAD_FAST                'model'
              514  LOAD_ATTR                nu
              516  LOAD_CONST               None
              518  LOAD_CONST               None
              520  BUILD_SLICE_2         2 
              522  LOAD_CONST               None
              524  LOAD_CONST               None
              526  BUILD_SLICE_2         2 
              528  LOAD_FAST                'jj'
              530  BUILD_TUPLE_3         3 
              532  BINARY_SUBSCR    
              534  CALL_METHOD_2         2  '2 positional arguments'
              536  BINARY_ADD       
              538  LOAD_FAST                'y_pred'
              540  LOAD_FAST                'ii'
              542  LOAD_FAST                'jj'
              544  BUILD_TUPLE_2         2 
              546  STORE_SUBSCR     
          548_550  JUMP_BACK           494  'to 494'
              552  POP_BLOCK        
            554_0  COME_FROM_LOOP      482  '482'
              554  JUMP_BACK           124  'to 124'
              556  POP_BLOCK        
            558_0  COME_FROM_LOOP      110  '110'

 L. 435       558  LOAD_FAST                'y'
              560  LOAD_CONST               None
              562  COMPARE_OP               is
          564_566  POP_JUMP_IF_FALSE   694  'to 694'

 L. 436       568  LOAD_FAST                'model'
              570  LOAD_ATTR                type
              572  LOAD_STR                 'oclinear'
              574  COMPARE_OP               ==
          576_578  POP_JUMP_IF_FALSE   586  'to 586'

 L. 437       580  LOAD_CONST               None
              582  STORE_FAST               'SSE'
              584  JUMP_FORWARD       1166  'to 1166'
            586_0  COME_FROM           576  '576'

 L. 438       586  LOAD_FAST                'model'
              588  LOAD_ATTR                type
              590  LOAD_STR                 'oclogistic'
              592  COMPARE_OP               ==
          594_596  POP_JUMP_IF_FALSE   634  'to 634'

 L. 439       598  LOAD_GLOBAL              phi
              600  LOAD_FAST                'y_pred'
              602  CALL_FUNCTION_1       1  '1 positional argument'
              604  STORE_FAST               'y_pred'

 L. 440       606  LOAD_GLOBAL              np
              608  LOAD_METHOD              ones
              610  LOAD_FAST                'n'
              612  CALL_METHOD_1         1  '1 positional argument'
              614  STORE_FAST               'y_labels'

 L. 441       616  LOAD_CONST               -1
              618  LOAD_FAST                'y_labels'
              620  LOAD_FAST                'y_pred'
              622  LOAD_CONST               0.5
              624  COMPARE_OP               <
              626  STORE_SUBSCR     

 L. 442       628  LOAD_CONST               None
              630  STORE_FAST               'PC'
              632  JUMP_FORWARD       1166  'to 1166'
            634_0  COME_FROM           594  '594'

 L. 443       634  LOAD_FAST                'model'
              636  LOAD_ATTR                type
              638  LOAD_STR                 'ocmlogistic'
              640  COMPARE_OP               ==
          642_644  POP_JUMP_IF_FALSE  1166  'to 1166'

 L. 444       646  LOAD_GLOBAL              phi
              648  LOAD_FAST                'y_pred'
              650  LOAD_METHOD              ravel
              652  CALL_METHOD_0         0  '0 positional arguments'
              654  CALL_FUNCTION_1       1  '1 positional argument'
              656  STORE_FAST               'y_pred'

 L. 445       658  LOAD_FAST                'y_pred'
              660  LOAD_METHOD              reshape
              662  LOAD_FAST                'n'
              664  LOAD_FAST                'm'
              666  CALL_METHOD_2         2  '2 positional arguments'
              668  STORE_FAST               'y_pred'

 L. 446       670  LOAD_FAST                'y_pred'
              672  LOAD_ATTR                argmax
              674  LOAD_CONST               1
              676  LOAD_CONST               ('axis',)
              678  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              680  LOAD_CONST               1
              682  BINARY_ADD       
              684  STORE_FAST               'y_labels'

 L. 447       686  LOAD_CONST               None
              688  STORE_FAST               'PC'
          690_692  JUMP_FORWARD       1166  'to 1166'
            694_0  COME_FROM           564  '564'

 L. 449       694  LOAD_FAST                'model'
              696  LOAD_ATTR                type
              698  LOAD_STR                 'oclinear'
              700  COMPARE_OP               ==
          702_704  POP_JUMP_IF_FALSE   726  'to 726'

 L. 450       706  LOAD_GLOBAL              sum
              708  LOAD_FAST                'y'
              710  LOAD_FAST                'y_pred'
              712  BINARY_SUBTRACT  
              714  LOAD_CONST               2
              716  BINARY_POWER     
              718  CALL_FUNCTION_1       1  '1 positional argument'
              720  STORE_FAST               'SSE'
          722_724  JUMP_FORWARD       1166  'to 1166'
            726_0  COME_FROM           702  '702'

 L. 451       726  LOAD_FAST                'model'
              728  LOAD_ATTR                type
              730  LOAD_STR                 'oclogistic'
              732  COMPARE_OP               ==
          734_736  POP_JUMP_IF_FALSE   880  'to 880'

 L. 452       738  LOAD_GLOBAL              phi
              740  LOAD_FAST                'y_pred'
              742  CALL_FUNCTION_1       1  '1 positional argument'
              744  STORE_FAST               'y_pred'

 L. 453       746  LOAD_GLOBAL              np
              748  LOAD_METHOD              ones
              750  LOAD_FAST                'n'
              752  CALL_METHOD_1         1  '1 positional argument'
              754  STORE_FAST               'y_labels'

 L. 454       756  LOAD_CONST               -1
              758  LOAD_FAST                'y_labels'
              760  LOAD_FAST                'y_pred'
              762  LOAD_CONST               0.5
              764  COMPARE_OP               <
              766  STORE_SUBSCR     

 L. 455       768  LOAD_GLOBAL              sum
              770  LOAD_FAST                'y'
              772  LOAD_FAST                'y_labels'
              774  LOAD_CONST               1
              776  COMPARE_OP               ==
              778  BINARY_SUBSCR    
              780  LOAD_CONST               1
              782  COMPARE_OP               ==
              784  CALL_FUNCTION_1       1  '1 positional argument'
              786  STORE_FAST               'TP'

 L. 456       788  LOAD_GLOBAL              sum
              790  LOAD_FAST                'y'
              792  LOAD_FAST                'y_labels'
              794  LOAD_CONST               -1
              796  COMPARE_OP               ==
              798  BINARY_SUBSCR    
              800  LOAD_CONST               1
              802  COMPARE_OP               ==
              804  CALL_FUNCTION_1       1  '1 positional argument'
              806  STORE_FAST               'FP'

 L. 457       808  LOAD_GLOBAL              sum
              810  LOAD_FAST                'y'
              812  LOAD_FAST                'y_labels'
              814  LOAD_CONST               -1
              816  COMPARE_OP               ==
              818  BINARY_SUBSCR    
              820  LOAD_CONST               -1
              822  COMPARE_OP               ==
              824  CALL_FUNCTION_1       1  '1 positional argument'
              826  STORE_FAST               'TN'

 L. 458       828  LOAD_GLOBAL              sum
              830  LOAD_FAST                'y'
              832  LOAD_FAST                'y_labels'
              834  LOAD_CONST               1
              836  COMPARE_OP               ==
              838  BINARY_SUBSCR    
              840  LOAD_CONST               -1
              842  COMPARE_OP               ==
              844  CALL_FUNCTION_1       1  '1 positional argument'
              846  STORE_FAST               'FN'

 L. 459       848  LOAD_FAST                'TP'
              850  LOAD_FAST                'TN'
              852  BINARY_ADD       
              854  LOAD_GLOBAL              float
              856  LOAD_FAST                'TP'
              858  LOAD_FAST                'FP'
              860  BINARY_ADD       
              862  LOAD_FAST                'FN'
              864  BINARY_ADD       
              866  LOAD_FAST                'TN'
              868  BINARY_ADD       
              870  CALL_FUNCTION_1       1  '1 positional argument'
              872  BINARY_TRUE_DIVIDE
              874  STORE_FAST               'PC'
          876_878  JUMP_FORWARD       1166  'to 1166'
            880_0  COME_FROM           734  '734'

 L. 460       880  LOAD_FAST                'model'
              882  LOAD_ATTR                type
              884  LOAD_STR                 'ocmlogistic'
              886  COMPARE_OP               ==
          888_890  POP_JUMP_IF_FALSE  1166  'to 1166'

 L. 461       892  LOAD_GLOBAL              phi
              894  LOAD_FAST                'y_pred'
              896  LOAD_METHOD              ravel
              898  CALL_METHOD_0         0  '0 positional arguments'
              900  CALL_FUNCTION_1       1  '1 positional argument'
              902  STORE_FAST               'y_pred'

 L. 462       904  LOAD_FAST                'y_pred'
              906  LOAD_METHOD              reshape
              908  LOAD_FAST                'n'
              910  LOAD_FAST                'm'
              912  CALL_METHOD_2         2  '2 positional arguments'
              914  STORE_FAST               'y_pred'

 L. 463       916  LOAD_FAST                'y_pred'
              918  LOAD_ATTR                argmax
              920  LOAD_CONST               1
              922  LOAD_CONST               ('axis',)
              924  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              926  LOAD_CONST               1
              928  BINARY_ADD       
              930  STORE_FAST               'y_labels'

 L. 464       932  LOAD_GLOBAL              np
              934  LOAD_METHOD              zeros
              936  LOAD_FAST                'm'
              938  CALL_METHOD_1         1  '1 positional argument'
              940  STORE_FAST               'PC'

 L. 465       942  LOAD_GLOBAL              np
              944  LOAD_METHOD              arange
              946  LOAD_CONST               1
              948  LOAD_FAST                'm'
              950  LOAD_CONST               1
              952  BINARY_ADD       
              954  CALL_METHOD_2         2  '2 positional arguments'
              956  STORE_FAST               'cls_set'

 L. 466       958  SETUP_LOOP         1144  'to 1144'
              960  LOAD_GLOBAL              range
              962  LOAD_CONST               0
              964  LOAD_FAST                'm'
              966  CALL_FUNCTION_2       2  '2 positional arguments'
              968  GET_ITER         
              970  FOR_ITER           1142  'to 1142'
              972  STORE_FAST               'ii'

 L. 467       974  LOAD_GLOBAL              np
              976  LOAD_METHOD              delete
              978  LOAD_FAST                'cls_set'
              980  LOAD_FAST                'ii'
              982  CALL_METHOD_2         2  '2 positional arguments'
              984  STORE_FAST               'cls_sub'

 L. 468       986  LOAD_GLOBAL              sum
              988  LOAD_FAST                'y'
              990  LOAD_FAST                'y_labels'
              992  LOAD_FAST                'ii'
              994  LOAD_CONST               1
              996  BINARY_ADD       
              998  COMPARE_OP               ==
             1000  BINARY_SUBSCR    
             1002  LOAD_FAST                'ii'
             1004  LOAD_CONST               1
             1006  BINARY_ADD       
             1008  COMPARE_OP               ==
             1010  CALL_FUNCTION_1       1  '1 positional argument'
             1012  STORE_FAST               'TP'

 L. 469      1014  LOAD_GLOBAL              sum
             1016  LOAD_FAST                'y'
             1018  LOAD_GLOBAL              np
             1020  LOAD_METHOD              in1d
             1022  LOAD_FAST                'y_labels'
             1024  LOAD_FAST                'cls_sub'
             1026  CALL_METHOD_2         2  '2 positional arguments'
             1028  BINARY_SUBSCR    
             1030  LOAD_FAST                'ii'
             1032  LOAD_CONST               1
             1034  BINARY_ADD       
             1036  COMPARE_OP               ==
             1038  CALL_FUNCTION_1       1  '1 positional argument'
             1040  STORE_FAST               'FP'

 L. 470      1042  LOAD_GLOBAL              sum
             1044  LOAD_FAST                'y'
             1046  LOAD_GLOBAL              np
             1048  LOAD_METHOD              in1d
             1050  LOAD_FAST                'y_labels'
             1052  LOAD_FAST                'cls_sub'
             1054  CALL_METHOD_2         2  '2 positional arguments'
             1056  BINARY_SUBSCR    
           1058_0  COME_FROM           584  '584'

 L. 471      1058  LOAD_FAST                'y_labels'
             1060  LOAD_GLOBAL              np
             1062  LOAD_METHOD              in1d
             1064  LOAD_FAST                'y_labels'
             1066  LOAD_FAST                'cls_sub'
             1068  CALL_METHOD_2         2  '2 positional arguments'
             1070  BINARY_SUBSCR    
             1072  COMPARE_OP               ==
             1074  CALL_FUNCTION_1       1  '1 positional argument'
             1076  STORE_FAST               'TN'

 L. 472      1078  LOAD_GLOBAL              sum
             1080  LOAD_GLOBAL              np
             1082  LOAD_METHOD              in1d
             1084  LOAD_FAST                'y'
             1086  LOAD_FAST                'y_labels'
             1088  LOAD_FAST                'ii'
             1090  LOAD_CONST               1
             1092  BINARY_ADD       
             1094  COMPARE_OP               ==
             1096  BINARY_SUBSCR    
             1098  LOAD_FAST                'cls_sub'
             1100  CALL_METHOD_2         2  '2 positional arguments'
             1102  CALL_FUNCTION_1       1  '1 positional argument'
             1104  STORE_FAST               'FN'
           1106_0  COME_FROM           632  '632'

 L. 473      1106  LOAD_FAST                'TP'
             1108  LOAD_FAST                'TN'
             1110  BINARY_ADD       
             1112  LOAD_GLOBAL              float
             1114  LOAD_FAST                'TP'
             1116  LOAD_FAST                'FP'
             1118  BINARY_ADD       
             1120  LOAD_FAST                'FN'
             1122  BINARY_ADD       
             1124  LOAD_FAST                'TN'
             1126  BINARY_ADD       
             1128  CALL_FUNCTION_1       1  '1 positional argument'
             1130  BINARY_TRUE_DIVIDE
             1132  LOAD_FAST                'PC'
             1134  LOAD_FAST                'ii'
             1136  STORE_SUBSCR     
         1138_1140  JUMP_BACK           970  'to 970'
             1142  POP_BLOCK        
           1144_0  COME_FROM_LOOP      958  '958'

 L. 475      1144  LOAD_GLOBAL              sum
             1146  LOAD_FAST                'y'
             1148  LOAD_FAST                'y_labels'
             1150  COMPARE_OP               ==
             1152  CALL_FUNCTION_1       1  '1 positional argument'
             1154  LOAD_GLOBAL              float
             1156  LOAD_FAST                'y_labels'
             1158  LOAD_ATTR                size
             1160  CALL_FUNCTION_1       1  '1 positional argument'
             1162  BINARY_TRUE_DIVIDE
             1164  STORE_FAST               'PC'
           1166_0  COME_FROM           888  '888'
           1166_1  COME_FROM           876  '876'
           1166_2  COME_FROM           722  '722'
           1166_3  COME_FROM           690  '690'
           1166_4  COME_FROM           642  '642'

 L. 477      1166  LOAD_FAST                'model'
             1168  LOAD_ATTR                type
             1170  LOAD_STR                 'oclinear'
             1172  COMPARE_OP               ==
         1174_1176  POP_JUMP_IF_FALSE  1206  'to 1206'

 L. 478      1178  LOAD_GLOBAL              collections
             1180  LOAD_METHOD              namedtuple
             1182  LOAD_STR                 'prediction'
             1184  LOAD_STR                 'y_pred'
             1186  LOAD_STR                 'SSE'
             1188  BUILD_LIST_2          2 
             1190  CALL_METHOD_2         2  '2 positional arguments'
             1192  STORE_FAST               'prediction'

 L. 479      1194  LOAD_FAST                'prediction'
             1196  LOAD_FAST                'y_pred'
             1198  LOAD_FAST                'SSE'
             1200  CALL_FUNCTION_2       2  '2 positional arguments'
             1202  STORE_FAST               'out'
             1204  JUMP_FORWARD       1292  'to 1292'
           1206_0  COME_FROM          1174  '1174'

 L. 480      1206  LOAD_FAST                'model'
             1208  LOAD_ATTR                type
             1210  LOAD_STR                 'oclogistic'
             1212  COMPARE_OP               ==
         1214_1216  POP_JUMP_IF_FALSE  1250  'to 1250'

 L. 481      1218  LOAD_GLOBAL              collections
             1220  LOAD_METHOD              namedtuple
             1222  LOAD_STR                 'prediction'
             1224  LOAD_STR                 'y_prob'

 L. 482      1226  LOAD_STR                 'y_labels'
             1228  LOAD_STR                 'PC'
             1230  BUILD_LIST_3          3 
             1232  CALL_METHOD_2         2  '2 positional arguments'
             1234  STORE_FAST               'prediction'

 L. 483      1236  LOAD_FAST                'prediction'
             1238  LOAD_FAST                'y_pred'
             1240  LOAD_FAST                'y_labels'
             1242  LOAD_FAST                'PC'
             1244  CALL_FUNCTION_3       3  '3 positional arguments'
             1246  STORE_FAST               'out'
             1248  JUMP_FORWARD       1292  'to 1292'
           1250_0  COME_FROM          1214  '1214'

 L. 484      1250  LOAD_FAST                'model'
             1252  LOAD_ATTR                type
             1254  LOAD_STR                 'ocmlogistic'
             1256  COMPARE_OP               ==
         1258_1260  POP_JUMP_IF_FALSE  1292  'to 1292'

 L. 485      1262  LOAD_GLOBAL              collections
             1264  LOAD_METHOD              namedtuple
             1266  LOAD_STR                 'prediction'
             1268  LOAD_STR                 'y_prob'

 L. 486      1270  LOAD_STR                 'y_labels'
             1272  LOAD_STR                 'PC'
             1274  BUILD_LIST_3          3 
             1276  CALL_METHOD_2         2  '2 positional arguments'
             1278  STORE_FAST               'prediction'

 L. 487      1280  LOAD_FAST                'prediction'
             1282  LOAD_FAST                'y_pred'
             1284  LOAD_FAST                'y_labels'
             1286  LOAD_FAST                'PC'
             1288  CALL_FUNCTION_3       3  '3 positional arguments'
             1290  STORE_FAST               'out'
           1292_0  COME_FROM          1258  '1258'
           1292_1  COME_FROM          1248  '1248'
           1292_2  COME_FROM          1204  '1204'

 L. 489      1292  LOAD_FAST                'out'
             1294  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 1058_0


def preproc_open_curve(beta, T=100):
    n, M, k = beta.shape
    q = np.zeros((n, T, k))
    beta2 = np.zeros((n, T, k))
    for i in range(0, k):
        beta1 = beta[:, :, i]
        beta1, scale = cf.scale_curve(beta1)
        beta1 = cf.resamplecurve(beta1, T)
        centroid1 = cf.calculatecentroid(beta1)
        beta1 = beta1 - np.tile(centroid1, [T, 1]).T
        beta2[:, :, i] = beta1
        q[:, :, i] = cf.curve_to_q(beta1)

    return (q, beta2)


def regression_warp(nu, beta, y, alpha):
    """
    calculates optimal warping for function linear regression

    :param nu: numpy ndarray of shape (M,N) of M functions with N samples
    :param beta: numpy ndarray of shape (M,N) of M functions with N samples
    :param y: numpy ndarray of shape (1,N) of M functions with N samples
    responses
    :param alpha: numpy scalar

    :rtype: numpy array
    :return gamma_new: warping function

    """
    T = beta.shape[1]
    betanu = cf.q_to_curve(nu)
    betaM, O_M, tauM = cf.find_rotation_and_seed_coord(betanu, beta)
    q = cf.curve_to_q(betaM)
    gam_M = cf.optimum_reparam_curve(nu, q)
    betaM = cf.group_action_by_gamma_coord(betaM, gam_M)
    qM = cf.curve_to_q(betaM)
    y_M = cf.innerprod_q2(qM, nu)
    betam, O_m, taum = cf.find_rotation_and_seed_coord(-1 * betanu, beta)
    q = cf.curve_to_q(betam)
    gam_m = cf.optimum_reparam_curve(-1 * nu, q)
    betam = cf.group_action_by_gamma_coord(betam, gam_m)
    qm = cf.curve_to_q(betam)
    y_m = cf.innerprod_q2(qm, nu)
    if y > alpha + y_M:
        O_hat = O_M
        gamma_new = gam_M
        tau = tauM
    else:
        if y < alpha + y_m:
            O_hat = O_m
            gamma_new = gam_m
            tau = taum
        else:
            gamma_new, O_hat, tau = cf.curve_zero_crossing(y - alpha, beta, nu, y_M, y_m, gam_M, gam_m)
    return (
     gamma_new, O_hat, tau)


def logistic_warp(alpha, nu, q, y, deltaO=0.1, deltag=0.05, max_itr=8000, tol=0.0001, display=0, method=1):
    """
    calculates optimal warping for function logistic regression

    :param alpha: scalar
    :param nu: numpy ndarray of shape (M,N) of M functions with N samples
    :param q: numpy ndarray of shape (M,N) of M functions with N samples
    :param y: numpy ndarray of shape (1,N) of M functions with N samples
    responses

    :rtype: numpy array
    :return gamma: warping function

    """
    if method == 1:
        tau = 0
        q = q / norm(q)
        gam_old, O_old = lw.oclogit_warp(np.ascontiguousarray(alpha), np.ascontiguousarray(nu), np.ascontiguousarray(q), np.ascontiguousarray(y, dtype=(np.int32)), max_itr, tol, deltaO, deltag, display)
    else:
        if method == 2:
            betanu = cf.q_to_curve(nu)
            beta = cf.q_to_curve(q)
            T = beta.shape[1]
            if y == 1:
                beta1, O_old, tau = cf.find_rotation_and_seed_coord(betanu, beta)
                q = cf.curve_to_q(beta1)
                gam_old = cf.optimum_reparam_curve(nu, q)
            else:
                if y == -1:
                    beta1, O_old, tau = cf.find_rotation_and_seed_coord(-1 * betanu, beta)
                    q = cf.curve_to_q(beta1)
                    gam_old = cf.optimum_reparam_curve(-1 * nu, q)
    return (
     gam_old, O_old, tau)


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


def logit_loss(b, X, y, lam=0.0):
    """
    logistic loss function, returns Sum{-log(phi(t))}

    :param b: numpy ndarray of shape (M,N) of M functions with N samples
    :param X: numpy ndarray of shape (M,N) of M functions with N samples
    :param y: numpy ndarray of shape (1,N) of M functions with N samples
    responses

    :rtype: numpy array
    :return out: loss value

    """
    z = X.dot(b)
    yz = y * z
    idx = yz > 0
    out = np.zeros_like(yz)
    out[idx] = np.log(1 + np.exp(-yz[idx]))
    out[~idx] = -yz[(~idx)] + np.log(1 + np.exp(yz[(~idx)]))
    out = out.sum() + 0.5 * lam * b.dot(b)
    return out


def logit_gradient(b, X, y, lam=0.0):
    """
    calculates gradient of the logistic loss

    :param b: numpy ndarray of shape (M,N) of M functions with N samples
    :param X: numpy ndarray of shape (M,N) of M functions with N samples
    :param y: numpy ndarray of shape (1,N) of M functions with N samples
    responses

    :rtype: numpy array
    :return grad: gradient of logisitc loss

    """
    z = X.dot(b)
    z = phi(y * z)
    z0 = (z - 1) * y
    grad = X.T.dot(z0) + lam * b
    return grad


def logit_hessian(s, b, X, y):
    """
    calculates hessian of the logistic loss

    :param s: numpy ndarray of shape (M,N) of M functions with N samples
    :param b: numpy ndarray of shape (M,N) of M functions with N samples
    :param X: numpy ndarray of shape (M,N) of M functions with N samples
    :param y: numpy ndarray of shape (1,N) of M functions with N samples
    responses

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


def mlogit_warp_grad(alpha, nu, q, y, max_itr=8000, tol=0.0001, deltaO=0.008, deltag=0.008, display=0):
    """
    calculates optimal warping for functional multinomial logistic regression

    :param alpha: scalar
    :param nu: numpy ndarray of shape (M,N) of M functions with N samples
    :param q: numpy ndarray of shape (M,N) of M functions with N samples
    :param y: numpy ndarray of shape (1,N) of M functions with N samples
    responses
    :param max_itr: maximum number of iterations (Default=8000)
    :param tol: stopping tolerance (Default=1e-10)
    :param deltaO: gradient step size for rotation (Default=0.008)
    :param deltag: gradient step size for warping (Default=0.008)
    :param display: display iterations (Default=0)

    :rtype: tuple of numpy array
    :return gam_old: warping function

    """
    alpha = alpha / norm(alpha)
    q, scale = cf.scale_curve(q)
    for ii in range(0, nu.shape[2]):
        nu[:, :, ii], scale = cf.scale_curve(nu[:, :, ii])

    gam_old, O_old = mw.ocmlogit_warp(np.ascontiguousarray(alpha), np.ascontiguousarray(nu), np.ascontiguousarray(q), np.ascontiguousarray(y, dtype=(np.int32)), max_itr, tol, deltaO, deltag, display)
    return (
     gam_old, O_old)


def mlogit_loss(b, X, Y):
    """
    calculates multinomial logistic loss (negative log-likelihood)

    :param b: numpy ndarray of shape (M,N) of M functions with N samples
    :param X: numpy ndarray of shape (M,N) of M functions with N samples
    :param y: numpy ndarray of shape (1,N) of M functions with N samples
    responses

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

    :param b: numpy ndarray of shape (M,N) of M functions with N samples
    :param X: numpy ndarray of shape (M,N) of M functions with N samples
    :param y: numpy ndarray of shape (1,N) of M functions with N samples
    responses

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