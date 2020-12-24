# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: lo/iterative/iterative_thresholding.py
# Compiled at: 2010-09-30 09:46:26
"""
Use the pywt package to perform iterative thresholding algorithms.
"""
import lo, pywt
from pywt import thresholding

def landweber(A, W, y, mu=1.0, nu=None, threshold=thresholding.hard, x0=None, maxiter=100, callback=None):
    """Landweber algorithm
    
    Input
    -----
    A : measurement matrix
    W : wavelet transform
    y : data
    mu : step of the gradient update
    nu : thresholding coefficient
    threshold : thresholding function
    maxiter : number of iterations
    callback : callback function
    
    Output
    ------
    
    x : solution
    
    """
    if callback is None:
        callback = lo.CallbackFactory(verbose=True)
    if x0 is None:
        x = A.T * y
    else:
        x = copy(x0)
    for iter_ in xrange(maxiter):
        r = A * x - y
        x += 0.5 * mu * A.T * r
        x = W.T * threshold(W * x, nu)
        resid = lo.norm2(r) + 1 / (2 * nu) * lo.normp(p=1)(x)
        callback(x)

    return x


def fista(A, W, y, mu=1.0, nu=None, threshold=thresholding.hard, x0=None, maxiter=100, callback=None):
    """ Fista algorithm
    
    """
    if callback is None:
        callback = lo.CallbackFactory(verbose=True)
    if x0 is None:
        x = A.T * y
    else:
        x = copy(x0)
    x_old = np.zeros(x.shape)
    t_old = 1.0
    for iter_ in xrange(maxiter):
        t = (1 + np.sqrt(1 + 4 * t_old ** 2)) / 2
        a = (t_old - 1) / t
        t_old = copy(t)
        z = x + a * (x - x_old)
        g = A.T * (A * z - y)
        x = z - 0.5 * mu * g
        x = W.T * threshold(W * x, nu)
        x_old = copy(x)
        resid = lo.norm2(A * x - y) + 1 / (2 * nu) * lo.normp(p=1)(x)
        callback(x)

    return x