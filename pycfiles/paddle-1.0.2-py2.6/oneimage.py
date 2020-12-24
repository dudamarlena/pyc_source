# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paddle/examples/oneimage.py
# Compiled at: 2010-07-27 12:18:38
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
    if img.ndim == 3:
        assert img.shape[2] <= 3, img.shape
        img = NP.mean(img, 2)
    (h, w) = (12, 12)
    X = paddle.common.img2patches(img, size=(h, w), Nmax=Nmax)
    assert X.shape[0] == h * w, X.shape
    X -= NP.mean(X, 0).reshape((1, -1))
    paddle.common._saveDict(X, None, Nrows=10, Ncols=25, path='patches.png', sorted=False)
    K = 200
    (D0, C0, U0) = paddle.dual.init(X, K)
    (D, C, U, full_out) = paddle.dual.learn(X, D0, C0, U0, tau=5.0, rtol=1e-08)
    paddle.common._saveDict(D, U, Nrows=10, Ncols=20, path='atoms.png', sorted=True)
    paddle.common._saveDict(C.T, U, Nrows=10, Ncols=20, path='filters.png', sorted=True)