# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paddle/examples/experiment_BSD.py
# Compiled at: 2010-12-21 06:15:25
"""
This is the script to run the experiment on the BSd dataset, reported in
section 4.2 of the techical report:

C.Basso, M.Santoro, A.Verri and S.Villa. "PADDLE: Proximal Algorithm for
Dual Dictionaries LEarning", DISI-TR-2010-XX, 2010.
"""
import sys, os, glob, pylab, scipy.linalg as la, scipy.stats, scipy as sp
from paddle import dual, common, data
if __name__ == '__main__':
    W = 12
    N = 10000.0
    tau = 1.0
    eta = 1.0
    K = 200
    R = 1
    pca = True
    if len(sys.argv) < 2:
        print 'usage: python %s BSD_root_path [tau eta K]' % sys.argv[0]
        sys.exit(0)
    if len(sys.argv) > 2:
        if len(sys.argv) != 5:
            print 'usage: python %s BSD_root_path [tau eta K]' % sys.argv[0]
            sys.exit(0)
        tau = float(sys.argv[2])
        eta = float(sys.argv[3])
        K = int(sys.argv[4])
    path = sys.argv[1]
    (testdir, traindir) = data.checkBSD(path)
    (Xtrn, Xtst) = data.draw_patches(traindir, W, N)
    Xtrn -= sp.mean(Xtrn, 0).reshape((1, -1))
    Xtst -= sp.mean(Xtst, 0).reshape((1, -1))
    pars = {'tau': tau, 
       'mu': 0, 
       'eta': eta, 
       'maxiter': 200, 
       'minused': 1, 
       'verbose': False, 
       'rtol': 1e-05}
    dicfn = 'BSD_dict_%dx%d_%dk_tau%.1e_eta%d_K%d.npz' % (W, W, N / 1000.0, pars['tau'], pars['eta'], K)
    if not os.access(dicfn, os.R_OK):
        (D0, C0, U0) = dual.init(Xtrn, K, det=False)
        (D, C, U, full_out) = dual.learn(Xtrn, D0, C0, U0, **pars)
        print
        print ' whole computation took %.1f secs' % full_out['time'][(-1)]
        timing = sp.sum(sp.array(full_out['time'][:-1]), 0)
        print ' ... time spent optimizing U = %6.1f secs (%.1f%%)' % (timing[0], 100 * timing[0] / full_out['time'][(-1)])
        print ' ... time spent optimizing D = %6.1f secs (%.1f%%)' % (timing[1], 100 * timing[1] / full_out['time'][(-1)])
        print ' ... time spent optimizing C = %6.1f secs (%.1f%%)' % (timing[2], 100 * timing[2] / full_out['time'][(-1)])
        sp.savez(dicfn, D=D, C=C, U=U)
    if pca:
        pcafn = 'BSD_pca_%dx%d_%dk.npz' % (W, W, N / 1000.0)
        if not os.access(pcafn, os.R_OK):
            Cov = sp.dot(Xtrn, Xtrn.T) / (Xtrn.shape[1] - 1)
            (ew, ev) = la.eigh(Cov)
            order = sp.argsort(ew)[::-1]
            ew = ew[order]
            ev = ev[:, order]
            assert sp.allclose(sp.sum(ev ** 2, 0), 1)
            Erec_pca, Erec_pca_tst = [], []
            for i in xrange(1, ev.shape[1] - 1):
                Xr = sp.dot(ev[:, :i], sp.dot(ev[:, :i].T, Xtrn))
                erec = la.norm(Xtrn - Xr) / la.norm(Xtrn)
                Erec_pca.append(erec)
                Xr = sp.dot(ev[:, :i], sp.dot(ev[:, :i].T, Xtst))
                erec = la.norm(Xtst - Xr) / la.norm(Xtst)
                Erec_pca_tst.append(erec)

            Erec_pca, Erec_pca_tst = sp.array(Erec_pca), sp.array(Erec_pca_tst)
            sp.savez(pcafn, Erec_pca=Erec_pca, Erec_pca_tst=Erec_pca_tst)
        else:
            npz = sp.load(pcafn)
            Erec_pca = npz['Erec_pca']
            Erec_pca_tst = npz['Erec_pca_tst']
    dicfn = 'BSD_dict_%dx%d_%dk_tau%.1e_eta%d_K%d.npz' % (W, W, N / 1000.0, tau, eta, K)
    assert os.access(dicfn, os.R_OK), 'output dictionary file %s not found' % dicfn
    npz = sp.load(dicfn)
    figfn = 'BSD_atoms_%dx%d_%dk_tau%.0e_eta%d_K%d' % (W, W, N / 1000.0, tau, eta, K)
    (Nrows, Ncols) = (20, 10)
    assert Nrows * Ncols <= K, 'reduce the number of rows or columns'
    U, D, C = npz['U'], npz['D'], npz['C']
    common._saveDict(D, U, Nrows, Ncols, path=figfn + '_D.png', sorted=True)
    common._saveDict(C.T, U, Nrows, Ncols, path=figfn + '_C.png', sorted=True)