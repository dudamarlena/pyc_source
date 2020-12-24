# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paddle/examples/experiment_MNIST.py
# Compiled at: 2010-10-13 08:57:25
"""
This is the script to run the experiment on the MNIST dataset, reported
in section 4.2 of the techical report:

C.Basso, M.Santoro, A.Verri and S.Villa. "PADDLE: Proximal Algorithm for
Dual Dictionaries LEarning", DISI-TR-2010-XX, 2010.
"""
import sys, os, glob, pylab, scipy as sp, scipy.stats, cPickle, gzip
from paddle import dual, common

def loadMNIST(path):
    """
    Loads the MNIST dataset ...
    ...
    It returns the absolute paths of the test and training directories.
    """
    print 'Loading MNIST dataset from', path
    print ' ...',
    if not os.access(path, os.F_OK):
        print 'the file does not exist. Exiting.'
        sys.exit(0)
    f = gzip.open(path, 'rb')
    (train_set, valid_set, test_set) = cPickle.load(f)
    f.close()
    print 'OK!'
    return (train_set, valid_set, test_set)


def drawDecomposedDigit(x, D, U, Ncols, outfn):
    m = 2
    imgCOMP = sp.ones((2 * W + m, W * (4 + Ncols) + m * (4 + Ncols)))
    vmaxCOMP = sp.stats.scoreatpercentile(D.flatten(), 98)
    vminCOMP = sp.stats.scoreatpercentile(D.flatten(), 2)
    imgCOMP *= vmaxCOMP
    imgCOMP[W + m:2 * W + m, 0:W] = vmaxCOMP * x.reshape((W, W))
    for i in sp.arange(2, Ncols + 2):
        x = i * (W + m)
        imgCOMP[0:W, x:x + W] = D[:, i - 2].reshape((W, W))
        imgCOMP[W + m:2 * W + m, x:x + W] = vmaxCOMP * D[:, i - 2].reshape((W, W)) * U[(i - 2)]

    x = (3 + Ncols) * (W + m)
    imgCOMP[W + m:2 * W + m, x:x + W] = vmaxCOMP * sp.dot(D, U).reshape((W, W))
    dpi = 50.0
    pylab.figure(figsize=(imgCOMP.shape[1] / dpi, imgCOMP.shape[0] / dpi), dpi=dpi)
    pylab.imshow(imgCOMP, interpolation='nearest', vmin=vminCOMP, vmax=vmaxCOMP)
    pylab.gray()
    pylab.xticks(())
    pylab.yticks(())
    pylab.savefig(outfn, dpi=300, bbox_inches='tight', transparent=True)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: python %s MNIST_dataset_path (output_path)'
        sys.exit(0)
    W = 28
    K = 64
    M = 10000
    path = sys.argv[1]
    if len(sys.argv) < 3:
        outpath = './results/'
    else:
        outpath = sys.argv[2]
    if not os.access(outpath, os.W_OK):
        print 'creating output directory %s' % outpath
        os.mkdir(outpath)
    patchesfn = 'MNIST_patches_%dx%d_%dk.npz' % (W, W, M)
    if os.access(patchesfn, os.R_OK):
        print 'Loading a previously drawn sample from', patchesfn
        print 'REMOVE the file IF you want a NEW SAMPLE'
        npz = sp.load(patchesfn)
        X = npz['X']
    else:
        (train_set, validation_set, test_set) = loadMNIST(path)
        X = train_set[0].T
        X = X[:, sp.random.permutation(X.shape[1])[:M]]
        assert X.max() <= 1 and X.min() >= 0
        X -= sp.mean(X, 0).reshape((1, -1))
        sp.savez(patchesfn, X=X)
    N = X.shape[1]
    d = X.shape[0]
    assert W == sp.sqrt(d)
    pars = {'tau': 0.05, 
       'mu': 0, 
       'eta': 0.001, 
       'maxiter': 50, 
       'minused': 1, 
       'verbose': False, 
       'rtol': 1e-05, 
       'save_dict': True, 
       'save_path': outpath, 
       'save_sorted': False, 
       'save_shape': (8, 8)}
    dicfn = 'MNIST_dict_%dx%d_%dk.npz' % (W, W, M)
    if os.access(dicfn, os.R_OK):
        npz = sp.load(dicfn)
        D = npz['D']
        C = npz['C']
        U = npz['U']
    else:
        (D0, C0, U0) = dual.init(X, K, rnd=False)
        (D, C, U, full_out) = dual.learn(X, D0, C0, U0, **pars)
        sp.savez(dicfn, D=D, C=C, U=U)
    (rows, cols) = pars['save_shape']
    common._saveDict(D, U, rows, cols, path=outpath + 'dictD_final', sorted=False)
    common._saveDict(C.T, U, rows, cols, path=outpath + 'dictC_final', sorted=False)
    indexOfDigit = sp.around(sp.random.rand() * X.shape[1])
    print ' using digit with index %d' % indexOfDigit
    nonzeroindices = sp.where(sp.absolute(U[:, indexOfDigit]) > 0)[0]
    print '   atoms used:', nonzeroindices
    print '   with weights:', U[(nonzeroindices, indexOfDigit)]
    weights = U[(nonzeroindices, indexOfDigit)]
    i = sp.argsort(sp.absolute(weights))[::-1]
    nonzeroindices = nonzeroindices[i]
    x = X[:, indexOfDigit]
    D = D[:, nonzeroindices]
    U = U[(nonzeroindices, indexOfDigit)]
    Ncols = len(nonzeroindices)
    outfn = 'mnistCOMP.png'
    drawDecomposedDigit(x, D, U, Ncols, outfn)