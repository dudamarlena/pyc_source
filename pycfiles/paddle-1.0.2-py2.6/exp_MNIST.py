# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paddle/examples/exp_MNIST.py
# Compiled at: 2010-12-21 06:24:38
"""
Experiment on the MNIST dataset for the talk at CBCL.
Note that the following code extends that used for the 
submission to NIPS 2010.
"""
import sys, os, glob, scipy, pylab, numpy as NP, scipy.stats, cPickle, gzip, paddle
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: python %s MNIST_dataset_path (output_path)' % sys.argv[0]
        sys.exit(0)
    W = 28
    K = 64
    M = 10000
    R = 1
    path = sys.argv[1]
    if len(sys.argv) < 3:
        outpath = './results/'
    else:
        outpath = sys.argv[2]
    patchesfn = 'MNIST_patches_%dx%d_%dk.npy' % (W, W, M)
    if os.access(patchesfn, os.R_OK):
        print 'Loading a previously drawn sample from', patchesfn
        print 'REMOVE the file IF you want a NEW SAMPLE'
        X = NP.load(patchesfn)
    else:
        (train_set, validation_set, test_set) = paddle.data.loadMNIST(path)
        X = train_set[0].T
        N = X.shape[1]
        X = X[:, NP.random.permutation(int(N))[:M]]
        X /= 255.0
        m = NP.mean(X, 0).reshape((1, -1))
        X -= m
        NP.save(patchesfn, X)
    N = X.shape[1]
    d = X.shape[0]
    assert W == NP.sqrt(d)
    for rep in xrange(R):
        dicfn = 'MNIST_dict_%dx%d_%dk.npz' % (W, W, M)
        if os.access(dicfn, os.R_OK):
            data = NP.load(dicfn)
            D = data['arr_0']
            C = data['arr_1']
            U = data['arr_2']
        else:
            pars = {'tau': 0.0005, 
               'mu': 0.0001, 
               'eta': 1.0, 
               'maxiter': 15, 
               'minused': 1, 
               'verbose': True, 
               'rtol': 0.001, 
               'save_dict': True, 
               'save_path': outpath, 
               'save_sorted': True, 
               'save_shape': (8, 8)}
            (D0, C0, U0) = paddle.dual.init(X, K)
            (D, C, U, full_out) = paddle.dual.learn(X, D0, C0, U0, callable=None, **pars)
            NP.savez(dicfn, D, C, U)
        usage = NP.sum(NP.where(NP.abs(U) > 1e-06, 1, 0), 1)
        order = NP.argsort(usage)[::-1]
        indexOfDigit = 5017
        print indexOfDigit
        Ncols = len(NP.where(U[:, indexOfDigit] > 0)[0])
        nonzeroindices = NP.where(U[:, indexOfDigit] > 0)[0]
        print nonzeroindices
        print U[(nonzeroindices, indexOfDigit)]
        m = 2
        imgCOMP = NP.ones((2 * W + m, W * (4 + Ncols) + m * (4 + Ncols)))
        vmaxCOMP = scipy.stats.scoreatpercentile(D.flatten(), 98)
        vminCOMP = scipy.stats.scoreatpercentile(D.flatten(), 2)
        imgCOMP *= vmaxCOMP
        imgCOMP[W + m:2 * W + m, 0:W] = 50 * X[:, indexOfDigit].reshape((W, W))
        for i in NP.arange(2, Ncols + 2):
            x = i * (W + m)
            imgCOMP[0:W, x:x + W] = D[:, nonzeroindices[(i - 2)]].reshape((W, W))
            imgCOMP[W + m:2 * W + m, x:x + W] = D[:, nonzeroindices[(i - 2)]].reshape((W, W)) * U[(nonzeroindices[(i - 2)], indexOfDigit)] * 150

        x = (3 + Ncols) * (W + m)
        imgCOMP[W + m:2 * W + m, x:x + W] = 100 * NP.dot(D[:, nonzeroindices], U[(nonzeroindices, indexOfDigit)]).reshape((W, W))
        dpi = 50.0
        pylab.figure(figsize=(imgCOMP.shape[1] / dpi, imgCOMP.shape[0] / dpi), dpi=dpi)
        pylab.imshow(imgCOMP, interpolation='nearest', vmin=vminCOMP, vmax=vmaxCOMP)
        pylab.gray()
        pylab.xticks(())
        pylab.yticks(())
        pylab.savefig('mnistCOMP.png', dpi=300, bbox_inches='tight', transparent=True)