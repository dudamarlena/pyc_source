# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/linalg/linalg_matrix.py
# Compiled at: 2013-04-10 06:45:39
"""Matrix linear algebra routines needed for GP models"""
import scipy as SP, scipy.linalg as linalg, logging

def solve_chol(A, B):
    r"""
    Solve cholesky decomposition::
    
        return A\(A'\B)

    """
    X = linalg.cho_solve((A, True), B)
    return X


def jitChol(A, maxTries=10, warning=True):
    """Do a Cholesky decomposition with jitter.
    
    Description:
    
    
    U, jitter = jitChol(A, maxTries, warning) attempts a Cholesky
     decomposition on the given matrix, if matrix isn't positive
     definite the function adds 'jitter' and tries again. Thereafter
     the amount of jitter is multiplied by 10 each time it is added
     again. This is continued for a maximum of 10 times.  The amount of
     jitter added is returned.
     Returns:
      U - the Cholesky decomposition for the matrix.
      jitter - the amount of jitter that was added to the matrix.
     Arguments:
      A - the matrix for which the Cholesky decomposition is required.
      maxTries - the maximum number of times that jitter is added before
       giving up (default 10).
      warning - whether to give a warning for adding jitter (default is True)

    See also
    CHOL, PDINV, LOGDET

    Copyright (c) 2005, 2006 Neil D. Lawrence
    
    """
    warning = True
    jitter = 0
    i = 0
    while True:
        try:
            if jitter == 0:
                jitter = abs(SP.trace(A)) / A.shape[0] * 1e-06
                LC = linalg.cholesky(A, lower=True)
                return (
                 LC.T, 0.0)
            else:
                if warning:
                    logging.warning('Adding jitter of %f in jitChol().' % jitter)
                LC = linalg.cholesky(A + jitter * SP.eye(A.shape[0]), lower=True)
                return (
                 LC.T, jitter)

        except linalg.LinAlgError:
            if i < maxTries:
                jitter = jitter * 10
            else:
                raise linalg.LinAlgError, 'Matrix non positive definite, jitter of ' + str(jitter) + ' added but failed after ' + str(i) + ' trials.'

        i += 1