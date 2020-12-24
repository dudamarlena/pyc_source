# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/examples/kinsol_ors.py
# Compiled at: 2017-12-28 04:09:42
import numpy as N, pylab as P, scipy as S, scipy.linalg as LIN, scipy.io as IO, scipy.sparse as SPARSE, scipy.sparse.linalg as LINSP, nose, os
from assimulo.solvers import KINSOL
from assimulo.problem import Algebraic_Problem
import warnings, scipy.sparse
warnings.simplefilter('ignore', scipy.sparse.SparseEfficiencyWarning)
file_path = os.path.dirname(os.path.realpath(__file__))

def run_example(with_plots=True):
    """
    Example to demonstrate the use of the Sundials solver Kinsol with
    a user provided Jacobian and a preconditioner. The example is the 
    'Problem 4' taken from the book by Saad:
    Iterative Methods for Sparse Linear Systems.
    
    on return:
    
       - :dfn:`alg_mod`    problem instance
    
       - :dfn:`alg_solver`    solver instance
    
    """
    A_original = IO.mmread(os.path.join(file_path, 'kinsol_ors_matrix.mtx'))
    A = SPARSE.spdiags(1.0 / A_original.diagonal(), 0, len(A_original.diagonal()), len(A_original.diagonal())) * A_original
    if True:
        D = SPARSE.spdiags(A.diagonal(), 0, len(A_original.diagonal()), len(A_original.diagonal()))
        Dinv = SPARSE.spdiags(1.0 / A.diagonal(), 0, len(A_original.diagonal()), len(A_original.diagonal()))
        E = -SPARSE.tril(A, k=-1)
        F = -SPARSE.triu(A, k=1)
        L = (D - E).dot(Dinv)
        U = D - F
        Prec = L.dot(U)
        solvePrec = LINSP.factorized(Prec)
    b = A.dot(N.ones((A.shape[0], 1)))

    def res(x):
        return A.dot(x.reshape(len(x), 1)) - b

    def jac(x):
        return A.todense()

    def jacv(x, v):
        return A.dot(v.reshape(len(v), 1))

    def prec_setup(u, f, uscale, fscale):
        pass

    def prec_solve(r):
        return solvePrec(r)

    y0 = S.rand(A.shape[0])
    alg_mod = Algebraic_Problem(res, y0=y0, jac=jac, jacv=jacv, name='ORS Example')
    alg_mod_prec = Algebraic_Problem(res, y0=y0, jac=jac, jacv=jacv, prec_solve=prec_solve, prec_setup=prec_setup, name='ORS Example (Preconditioned)')
    alg_solver = KINSOL(alg_mod)
    alg_solver_prec = KINSOL(alg_mod_prec)

    def setup_param(solver):
        solver.linear_solver = 'spgmr'
        solver.max_dim_krylov_subspace = 10
        solver.ftol = LIN.norm(res(solver.y0)) * 1e-09
        solver.max_iter = 300
        solver.verbosity = 10
        solver.globalization_strategy = 'none'

    setup_param(alg_solver)
    setup_param(alg_solver_prec)
    y = alg_solver.solve()
    y_prec = alg_solver_prec.solve()
    print (
     'Error                 , in y: ', LIN.norm(y - N.ones(len(y))))
    print ('Error (preconditioned), in y: ', LIN.norm(y_prec - N.ones(len(y_prec))))
    if with_plots:
        P.figure(4)
        P.semilogy(alg_solver.get_residual_norm_nonlinear_iterations(), label='Original')
        P.semilogy(alg_solver_prec.get_residual_norm_nonlinear_iterations(), label='Preconditioned')
        P.xlabel('Number of Iterations')
        P.ylabel('Residual Norm')
        P.title('Solution Progress')
        P.legend()
        P.grid()
        P.figure(5)
        P.plot(y, label='Original')
        P.plot(y_prec, label='Preconditioned')
        P.legend()
        P.grid()
        P.show()
    for j in range(len(y)):
        nose.tools.assert_almost_equal(y[j], 1.0, 4)

    return ([alg_mod, alg_mod_prec], [alg_solver, alg_solver_prec])


if __name__ == '__main__':
    mod, solv = run_example()