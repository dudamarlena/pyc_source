# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/covar/dist.py
# Compiled at: 2013-04-10 06:45:39
"""helper module for distances"""
import scipy as SP

def dist(X, Y=None):
    """calcualte disntance of all inputs:
    dist(X)     : Matrix of all combinations of distances of Xi with Xj
    dist(X1,X2) : Matrix of all combinations of distances of X1i with X2j"""
    if Y is None:
        Y = X.copy()
    rv = Y[None] - X[:, None]
    return rv


def sq_dist(*args):
    """calcualte square-distance of all inputs:
    sq_dist(X)     : Matrix of all combinations of distances of Xi with Xj
    sq_dist(X1,X2) : Matrix of all combinations of distances of X1i with X2j"""
    rv = dist(*args)
    rv = rv * rv
    rv = rv.sum(-1)
    return rv


def Bdist(*args):
    """binary distance matrix:
    dist(X)    -  return matrix of size (len(X),len(X)) all True!
    dist(X1,X2)-  return matrix of size (len(X1),len(X2)) with (xi==xj)"""
    if len(args) == 1:
        X = args[0]
        Y = args[0]
    elif len(args) >= 2:
        X = args[0]
        Y = args[1]
    A = SP.repeat(X, 1, len(Y))
    B = SP.repeat(Y.T, len(X), 1)
    rv = A & B
    return rv


if __name__ == '__main__':
    X = SP.array([[1, 2], [5, 6]], dtype='double')
    Y = SP.array([[1, 2], [8, 7], [0, 0]], dtype='double')
    print sq_dist(X, Y)