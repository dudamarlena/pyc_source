# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paddle/examples/oneimagergb.py
# Compiled at: 2010-07-23 05:10:32
import scipy, sys, numpy as NP, paddle
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: python %s imagefile [Nmax]' % sys.argv[0]
        sys.exit(0)
    if len(sys.argv) > 2:
        Nmax = int(sys.argv[2])
    else:
        Nmax = 0
    img = scipy.misc.imread(sys.argv[1])
    assert img.ndim == 3, img.shape
    assert img.shape[2] == 3, img.shape
    (h, w) = (10, 10)
    X = paddle.common.img2patches(img, size=(h, w), Nmax=Nmax)
    assert X.shape[0] == img.shape[2] * h * w, X.shape
    X = X.astype(NP.float)
    X /= 255.0
    paddle.common._saveDict(X, None, Nrows=10, Ncols=25, path='patches.png', sorted=False, channels=3)
    K = img.shape[2] * h * w + 1
    (D0, C0, U0) = paddle.dual.init(X, K)
    (D, C, U, full_out) = paddle.dual.learn(X, D0, C0, U0, tau=5.0, rtol=1e-08)
    paddle.common._saveDict(D, U, Nrows=10, Ncols=20, path='atoms.png', sorted=True, channels=3)
    paddle.common._saveDict(C.T, U, Nrows=10, Ncols=20, path='filters.png', sorted=True, channels=3)