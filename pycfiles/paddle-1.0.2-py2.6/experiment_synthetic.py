# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paddle/examples/experiment_synthetic.py
# Compiled at: 2011-02-28 10:31:21
"""
This is the script to run the experiments reported in section 4.1 of
the techical report:

C.Basso, M.Santoro, A.Verri and S.Villa. "PADDLE: Proximal Algorithm for
Dual Dictionaries LEarning", DISI-TR-2010-XX, 2010.
"""
import scipy as sp
from scipy import linalg as la
from paddle import dual, tframes, common
import pylab, os

def principal_angle(A, B):
    """
    Returns the largest angle between the linear subspaces spanned by
    the columns of 'A' and 'B'.
    'A' and 'B' must already be orthogonal matrices.
    """
    svd = la.svd(sp.dot(sp.transpose(A), B))
    return sp.arccos(min(svd[1].min(), 1.0))


def add_noise(X, level):
    noise = sp.random.normal(0, level, size=X.shape)
    SNR = la.norm(X) / la.norm(noise)
    print 'SNR (dB) = %d' % (20 * sp.log10(SNR),)
    return X + noise


def run_experiment_1(d, d0, N, K, noise, exp1fn):
    B = sp.random.uniform(size=(d, d0))
    B /= sp.sqrt(sp.sum(B ** 2, 0)).reshape((1, -1))
    X = sp.random.normal(size=(d0, N))
    X -= sp.mean(X, 1).reshape((-1, 1))
    X = sp.dot(B, X)
    print 'Generated %d examples with dimension %d and using %d basis' % (N, d, d0)
    X = add_noise(X, noise)
    (ew, ev) = la.eigh(sp.dot(X, X.T) / N)
    assert sp.all(sp.argsort(ew) == sp.arange(d)), ew
    ev = ev[:, -K:]
    ew = ew[-K:]
    Erec_pca = la.norm(X - sp.dot(ev, sp.dot(ev.T, X))) / la.norm(X)

    def test_callback(D, C, U, X):
        Erec = la.norm(X - sp.dot(D, sp.dot(C, X))) / la.norm(X)
        Ecod = la.norm(U - sp.dot(C, X)) / la.norm(U)
        nC = sp.sqrt(sp.sum(C * C, 1))
        nD = sp.sqrt(sp.sum(D * D, 0))
        Etrn = (1 - sp.absolute(sp.sum(D * C.T, 0) / (nD * nC))).mean()
        angle = principal_angle(la.qr(D, econ=True)[0], ev)
        return (Erec, Ecod, Etrn, angle)

    pars = {'tau': 0, 
       'mu': 1e-05, 
       'eta': 1, 
       'maxiter': 500, 
       'minused': 1, 
       'verbose': False, 
       'rtol': 1e-08}
    (D0, C0, U0) = dual.init(X, K, det=False)
    (D, C, U, full_out) = dual.learn(X, D0, C0, U0, callable=test_callback, **pars)
    call_res = sp.array(full_out['call_res']).T
    sp.savez(exp1fn, X=X, D=D, C=C, U=U, call_res=call_res, Erec_pca=Erec_pca)


def plot_figure_1(call_res, figfn, Erec_pca):
    Erec, Etrn = call_res[0], call_res[2]
    fonts = {'fontsize': 20}
    fig = pylab.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(Erec, 'k-', lw=1.5, label='Rec. error')
    ax1.plot(Etrn, 'k--', lw=1.5, label='Duality')
    ax1.hlines([Erec_pca], 0, len(Erec) - 1, lw=2.0, linestyle='dashdot', label='PCA error')
    ax1.set_xlabel('Iteration', fontdict=fonts)
    ax1.set_ylabel('Error', fontdict=fonts)
    ax1.semilogy()
    ax1.set_yticks((0.01, 0.02, 0.1, 1))
    ax1.set_yticklabels(('1%', '2%', '10%', '100%'), fontdict=fonts)
    pylab.legend()
    pylab.savefig(figfn, dpi=300, transparent=True, bbox_inches='tight')


def run_experiment_2(d, k, N, K, noise, exp2fn):
    A = tframes.get(d, K)
    Utrue = sp.zeros((K, N), sp.float32)
    for i in xrange(N):
        Utrue[(sp.random.permutation(K)[:k], i)] = sp.random.uniform(-1, 1, size=(k,))

    X = sp.dot(A, Utrue)
    X = add_noise(X, noise)

    def test_callback(D, C, U, X):
        Erec = la.norm(X - sp.dot(D, sp.dot(C, X))) / la.norm(X)
        Einv = la.norm(sp.identity(d) - sp.dot(D, C)) / d
        nC = sp.sqrt(sp.sum(C * C, 1))
        nD = sp.sqrt(sp.sum(D * D, 0))
        Etrn = (1 - sp.absolute(sp.sum(D * C.T, 0) / (nD * nC))).mean()
        return (Erec, Einv, Etrn)

    pars = {'tau': 0.5, 
       'mu': 1e-08, 
       'eta': 1, 
       'maxiter': 50, 
       'minused': 10, 
       'verbose': False, 
       'rtol': 1e-08}
    U0 = sp.zeros((K, N), sp.float32)
    (Uopt, full_out) = dual._ist(X, U0, A, A.T, pars, maxiter=1000)
    Erec_ntf = la.norm(X - sp.dot(A, Uopt)) / la.norm(X)
    (D0, C0, U0) = dual.init(X, K, det=False)
    (D, C, U, full_out) = dual.learn(X, D0, C0, U0, callable=test_callback, **pars)
    call_res = sp.array(full_out['call_res']).T
    sp.savez(exp2fn, X=X, D=D, C=C, U=U, A=A, call_res=call_res, Erec_ntf=Erec_ntf)


def plot_figure_2(call_res, figfn, Erec_opt):
    Erec, Etrn = call_res[0], call_res[2]
    fonts = {'fontsize': 20}
    fig = pylab.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(Erec, 'k-', lw=1.5, label='Rec. error')
    ax1.plot(Etrn, 'k--', lw=1.5, label='Duality')
    ax1.hlines([Erec_opt], 0, len(Erec) - 1, linestyle='dashdot', label='Optimal')
    ax1.set_xlabel('Iteration', fontdict=fonts)
    ax1.set_ylabel('Error', fontdict=fonts)
    ax1.semilogy()
    ax1.set_xlim((0, 100))
    ax1.set_ylim((0.001, 1))
    ax1.set_yticks((0.001, 0.01, 0.1, 1))
    ax1.set_yticklabels(('0.1%', '1%', '10%', '100%'), fontdict=fonts)
    pylab.legend()
    pylab.savefig(figfn, dpi=300, transparent=True, bbox_inches='tight')


if __name__ == '__main__':
    d = 25
    N = 10000
    k1 = 15
    K1 = 15
    k2 = 3
    K2 = 2 * d
    noise = 0.02
    runExp1 = True
    runExp2 = True
    print
    exp1fn = 'exp_synth_fig1.npz'
    if runExp1:
        if not os.access(exp1fn, os.R_OK):
            run_experiment_1(d, k1, N, K1, noise, exp1fn)
        else:
            print '[!!] loading results of experiment #1 from file %s' % exp1fn
            print '[!!] delete the file is you want to repeat the experiment'
        assert os.access(exp1fn, os.R_OK), exp1fn
        npz = sp.load(exp1fn)
        figfn = 'exp_synth_fig1.png'
        plot_figure_1(npz['call_res'], figfn, npz['Erec_pca'])
    print
    exp2fn = 'exp_synth_fig2.npz'
    if runExp2:
        if not os.access(exp2fn, os.R_OK):
            run_experiment_2(d, k2, N, K2, noise, exp2fn)
        else:
            print '[!!] loading results of experiment #2 from file %s' % exp2fn
            print '[!!] delete the file is you want to repeat the experiment'
        assert os.access(exp2fn, os.R_OK), exp2fn
        npz = sp.load(exp2fn)
        figfn = 'exp_synth_fig2.png'
        plot_figure_2(npz['call_res'], figfn, npz['Erec_ntf'])
        A = npz['A']
        D = npz['D']
        C = npz['C']
        for i in xrange(D.shape[1]):
            diff = sp.absolute(sp.sum(A[:, i, sp.newaxis] * D[:, i:], 0))
            order = sp.argsort(diff)[::-1] + i
            D = sp.concatenate((D[:, :i], D[:, order]), 1)
            C = sp.concatenate((C[:i], C[order]), 0)
            if sp.sum(A[:, i] * D[:, i]) < 0:
                D[:, i] *= -1
                C[i] *= -1

        common._saveDict(A, None, Nrows=5, Ncols=10, path='./tightframeA.png', sorted=False)
        common._saveDict(D, None, Nrows=5, Ncols=10, path='./tightframeD.png', sorted=False)
        common._saveDict(C.T, None, Nrows=5, Ncols=10, path='./tightframeCt.png', sorted=False)
        pylab.matshow(sp.absolute(sp.sum(A[:, :, sp.newaxis] * D[:, sp.newaxis, :], 0)))