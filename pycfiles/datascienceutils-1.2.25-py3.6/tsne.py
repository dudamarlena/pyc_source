# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datascienceutils/tsne.py
# Compiled at: 2017-11-27 01:36:20
# Size of source mod 2**32: 5327 bytes
import numpy as Math, pylab as Plot, os
DATA_DIR = os.path.expanduser('~/DataScientist/data')

def Hbeta(D=Math.array([]), beta=1.0):
    """Compute the perplexity and the P-row for a specific value of the precision of a Gaussian distribution."""
    P = Math.exp(-D.copy() * beta)
    sumP = sum(P)
    H = Math.log(sumP) + beta * Math.sum(D * P) / sumP
    P = P / sumP
    return (H, P)


def x2p(X=Math.array([]), tol=1e-05, perplexity=30.0):
    """Performs a binary search to get P-values in such a way that each conditional Gaussian has the same perplexity."""
    print('Computing pairwise distances...')
    n, d = X.shape
    sum_X = Math.sum(Math.square(X), 1)
    D = Math.add(Math.add(-2 * Math.dot(X, X.T), sum_X).T, sum_X)
    P = Math.zeros((n, n))
    beta = Math.ones((n, 1))
    logU = Math.log(perplexity)
    for i in range(n):
        if i % 500 == 0:
            print('Computing P-values for point ', i, ' of ', n, '...')
        betamin = -Math.inf
        betamax = Math.inf
        Di = D[(i, Math.concatenate((Math.r_[0:i], Math.r_[i + 1:n])))]
        H, thisP = Hbeta(Di, beta[i])
        Hdiff = H - logU
        tries = 0
        while Math.abs(Hdiff) > tol and tries < 50:
            if Hdiff > 0:
                betamin = beta[i].copy()
                if betamax == Math.inf or betamax == -Math.inf:
                    beta[i] = beta[i] * 2
                else:
                    beta[i] = (beta[i] + betamax) / 2
            else:
                betamax = beta[i].copy()
                if betamin == Math.inf or betamin == -Math.inf:
                    beta[i] = beta[i] / 2
                else:
                    beta[i] = (beta[i] + betamin) / 2
                H, thisP = Hbeta(Di, beta[i])
                Hdiff = H - logU
                tries = tries + 1

        P[(i, Math.concatenate((Math.r_[0:i], Math.r_[i + 1:n])))] = thisP

    print('Mean value of sigma: ', Math.mean(Math.sqrt(1 / beta)))
    return P


def pca(X=Math.array([]), no_dims=50):
    """Runs PCA on the NxD array X in order to reduce its dimensionality to no_dims dimensions."""
    print('Preprocessing the data using PCA...')
    n, d = X.shape
    X = X - Math.tile(Math.mean(X, 0), (n, 1))
    l, M = Math.linalg.eig(Math.dot(X.T, X))
    Y = Math.dot(X, M[:, 0:no_dims])
    return Y


def tsne(X=Math.array([]), no_dims=2, initial_dims=50, perplexity=30.0):
    """Runs t-SNE on the dataset in the NxD array X to reduce its dimensionality to no_dims dimensions.
        The syntaxis of the function is Y = tsne.tsne(X, no_dims, perplexity), where X is an NxD NumPy array."""
    if isinstance(no_dims, float):
        print('Error: array X should have type float.')
        return -1
    else:
        if round(no_dims) != no_dims:
            print('Error: number of dimensions should be an integer.')
            return -1
        X = pca(X, initial_dims).real
        n, d = X.shape
        max_iter = 1000
        initial_momentum = 0.5
        final_momentum = 0.8
        eta = 500
        min_gain = 0.01
        Y = Math.random.randn(n, no_dims)
        dY = Math.zeros((n, no_dims))
        iY = Math.zeros((n, no_dims))
        gains = Math.ones((n, no_dims))
        P = x2p(X, 1e-05, perplexity)
        P = P + Math.transpose(P)
        P = P / Math.sum(P)
        P = P * 4
        P = Math.maximum(P, 1e-12)
        for iter in range(max_iter):
            sum_Y = Math.sum(Math.square(Y), 1)
            num = 1 / (1 + Math.add(Math.add(-2 * Math.dot(Y, Y.T), sum_Y).T, sum_Y))
            num[(list(range(n)), list(range(n)))] = 0
            Q = num / Math.sum(num)
            Q = Math.maximum(Q, 1e-12)
            PQ = P - Q
            for i in range(n):
                dY[i, :] = Math.sum(Math.tile(PQ[:, i] * num[:, i], (no_dims, 1)).T * (Y[i, :] - Y), 0)

            if iter < 20:
                momentum = initial_momentum
            else:
                momentum = final_momentum
            gains = (gains + 0.2) * ((dY > 0) != (iY > 0)) + gains * 0.8 * ((dY > 0) == (iY > 0))
            gains[gains < min_gain] = min_gain
            iY = momentum * iY - eta * (gains * dY)
            Y = Y + iY
            Y = Y - Math.tile(Math.mean(Y, 0), (n, 1))
            if (iter + 1) % 10 == 0:
                C = Math.sum(P * Math.log(P / Q))
                print('Iteration ', iter + 1, ': error is ', C)
            if iter == 100:
                P = P / 4

        return Y


if __name__ == '__main__':
    print('Run Y = tsne.tsne(X, no_dims, perplexity) to perform t-SNE on your dataset.')
    print('Running example on 2,500 MNIST digits...')
    X = Math.loadtxt(os.path.join(DATA_DIR, 'mnist2500_X.txt'))
    labels = Math.loadtxt(os.path.join(DATA_DIR, 'mnist2500_labels.txt'))
    Y = tsne(X, 2, 50, 20.0)
    Plot.scatter(Y[:, 0], Y[:, 1], 20, labels)
    Plot.show()