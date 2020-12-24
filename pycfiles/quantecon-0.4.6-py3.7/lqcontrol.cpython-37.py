# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/lqcontrol.py
# Compiled at: 2019-11-04 18:33:25
# Size of source mod 2**32: 21470 bytes
"""
Provides a class called LQ for solving linear quadratic control
problems, and a class called LQMarkov for solving Markov jump
linear quadratic control problems.

"""
from textwrap import dedent
import numpy as np
from numpy import dot
from scipy.linalg import solve
from .matrix_eqn import solve_discrete_riccati, solve_discrete_riccati_system
from .util import check_random_state
from .markov import MarkovChain

class LQ:
    __doc__ = "\n    This class is for analyzing linear quadratic optimal control\n    problems of either the infinite horizon form\n\n    .. math::\n\n        \\min \\mathbb{E}\n        \\Big[ \\sum_{t=0}^{\\infty} \\beta^t r(x_t, u_t) \\Big]\n\n    with\n\n    .. math::\n\n         r(x_t, u_t) := x_t' R x_t + u_t' Q u_t + 2 u_t' N x_t\n\n    or the finite horizon form\n\n    .. math::\n\n         \\min \\mathbb{E}\n         \\Big[\n         \\sum_{t=0}^{T-1} \\beta^t r(x_t, u_t) + \\beta^T x_T' R_f x_T\n         \\Big]\n\n    Both are minimized subject to the law of motion\n\n    .. math::\n\n         x_{t+1} = A x_t + B u_t + C w_{t+1}\n\n    Here :math:`x` is n x 1, :math:`u` is k x 1, :math:`w` is j x 1 and the\n    matrices are conformable for these dimensions.  The sequence :math:`{w_t}`\n    is assumed to be white noise, with zero mean and\n    :math:`\\mathbb{E} [ w_t' w_t ] = I`, the j x j identity.\n\n    If :math:`C` is not supplied as a parameter, the model is assumed to be\n    deterministic (and :math:`C` is set to a zero matrix of appropriate\n    dimension).\n\n    For this model, the time t value (i.e., cost-to-go) function :math:`V_t`\n    takes the form\n\n    .. math::\n\n         x' P_T x + d_T\n\n    and the optimal policy is of the form :math:`u_T = -F_T x_T`. In the\n    infinite horizon case, :math:`V, P, d` and :math:`F` are all stationary.\n\n    Parameters\n    ----------\n    Q : array_like(float)\n        Q is the payoff (or cost) matrix that corresponds with the\n        control variable u and is k x k. Should be symmetric and\n        non-negative definite\n    R : array_like(float)\n        R is the payoff (or cost) matrix that corresponds with the\n        state variable x and is n x n. Should be symetric and\n        non-negative definite\n    A : array_like(float)\n        A is part of the state transition as described above. It should\n        be n x n\n    B : array_like(float)\n        B is part of the state transition as described above. It should\n        be n x k\n    C : array_like(float), optional(default=None)\n        C is part of the state transition as described above and\n        corresponds to the random variable today.  If the model is\n        deterministic then C should take default value of None\n    N : array_like(float), optional(default=None)\n        N is the cross product term in the payoff, as above. It should\n        be k x n.\n    beta : scalar(float), optional(default=1)\n        beta is the discount parameter\n    T : scalar(int), optional(default=None)\n        T is the number of periods in a finite horizon problem.\n    Rf : array_like(float), optional(default=None)\n        Rf is the final (in a finite horizon model) payoff(or cost)\n        matrix that corresponds with the control variable u and is n x\n        n.  Should be symetric and non-negative definite\n\n    Attributes\n    ----------\n    Q, R, N, A, B, C, beta, T, Rf : see Parameters\n    P : array_like(float)\n        P is part of the value function representation of\n        :math:`V(x) = x'Px + d`\n    d : array_like(float)\n        d is part of the value function representation of\n        :math:`V(x) = x'Px + d`\n    F : array_like(float)\n        F is the policy rule that determines the choice of control in\n        each period.\n    k, n, j : scalar(int)\n        The dimensions of the matrices as presented above\n\n    "

    def __init__(self, Q, R, A, B, C=None, N=None, beta=1, T=None, Rf=None):
        converter = lambda X: np.atleast_2d(np.asarray(X, dtype='float'))
        self.A, self.B, self.Q, self.R, self.N = list(map(converter, (
         A, B, Q, R, N)))
        self.k, self.n = self.Q.shape[0], self.R.shape[0]
        self.beta = beta
        if C is None:
            self.j = 1
            self.C = np.zeros((self.n, self.j))
        else:
            self.C = converter(C)
            self.j = self.C.shape[1]
        if N is None:
            self.N = np.zeros((self.k, self.n))
        if T:
            self.T = T
            self.Rf = np.asarray(Rf, dtype='float')
            self.P = self.Rf
            self.d = 0
        else:
            self.P = None
            self.d = None
            self.T = None
            if (self.C != 0).any():
                if beta >= 1:
                    raise ValueError('beta must be strictly smaller than 1 if T = None and C != 0.')
            self.F = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        m = '        Linear Quadratic control system\n          - beta (discount parameter)       : {b}\n          - T (time horizon)                : {t}\n          - n (number of state variables)   : {n}\n          - k (number of control variables) : {k}\n          - j (number of shocks)            : {j}\n        '
        t = 'infinite' if self.T is None else self.T
        return dedent(m.format(b=(self.beta), n=(self.n), k=(self.k), j=(self.j), t=t))

    def update_values(self):
        """
        This method is for updating in the finite horizon case.  It
        shifts the current value function

        .. math::

             V_t(x) = x' P_t x + d_t

        and the optimal policy :math:`F_t` one step *back* in time,
        replacing the pair :math:`P_t` and :math:`d_t` with
        :math:`P_{t-1}` and :math:`d_{t-1}`, and :math:`F_t` with
        :math:`F_{t-1}`

        """
        Q, R, A, B, N, C = (
         self.Q, self.R, self.A, self.B, self.N, self.C)
        P, d = self.P, self.d
        S1 = Q + self.beta * dot(B.T, dot(P, B))
        S2 = self.beta * dot(B.T, dot(P, A)) + N
        S3 = self.beta * dot(A.T, dot(P, A))
        self.F = solve(S1, S2)
        new_P = R - dot(S2.T, self.F) + S3
        new_d = self.beta * (d + np.trace(dot(P, dot(C, C.T))))
        self.P, self.d = new_P, new_d

    def stationary_values(self, method='doubling'):
        """
        Computes the matrix :math:`P` and scalar :math:`d` that represent
        the value function

        .. math::

             V(x) = x' P x + d

        in the infinite horizon case.  Also computes the control matrix
        :math:`F` from :math:`u = - Fx`. Computation is via the solution
        algorithm as specified by the `method` option (default to the
        doubling algorithm) (see the documentation in
        `matrix_eqn.solve_discrete_riccati`).

        Parameters
        ----------
        method : str, optional(default='doubling')
            Solution method used in solving the associated Riccati
            equation, str in {'doubling', 'qz'}.

        Returns
        -------
        P : array_like(float)
            P is part of the value function representation of
            :math:`V(x) = x'Px + d`
        F : array_like(float)
            F is the policy rule that determines the choice of control
            in each period.
        d : array_like(float)
            d is part of the value function representation of
            :math:`V(x) = x'Px + d`

        """
        Q, R, A, B, N, C = (
         self.Q, self.R, self.A, self.B, self.N, self.C)
        A0, B0 = np.sqrt(self.beta) * A, np.sqrt(self.beta) * B
        P = solve_discrete_riccati(A0, B0, R, Q, N, method=method)
        S1 = Q + self.beta * dot(B.T, dot(P, B))
        S2 = self.beta * dot(B.T, dot(P, A)) + N
        F = solve(S1, S2)
        if self.beta == 1:
            d = 0
        else:
            d = self.beta * np.trace(dot(P, dot(C, C.T))) / (1 - self.beta)
        self.P, self.F, self.d = P, F, d
        return (
         P, F, d)

    def compute_sequence(self, x0, ts_length=None, method='doubling', random_state=None):
        """
        Compute and return the optimal state and control sequences
        :math:`x_0, ..., x_T` and :math:`u_0,..., u_T`  under the
        assumption that :math:`{w_t}` is iid and :math:`N(0, 1)`.

        Parameters
        ----------
        x0 : array_like(float)
            The initial state, a vector of length n

        ts_length : scalar(int)
            Length of the simulation -- defaults to T in finite case

        method : str, optional(default='doubling')
            Solution method used in solving the associated Riccati
            equation, str in {'doubling', 'qz'}. Only relevant when the
            `T` attribute is `None` (i.e., the horizon is infinite).

        random_state : int or np.random.RandomState, optional
            Random seed (integer) or np.random.RandomState instance to set
            the initial state of the random number generator for
            reproducibility. If None, a randomly initialized RandomState is
            used.

        Returns
        -------
        x_path : array_like(float)
            An n x T+1 matrix, where the t-th column represents :math:`x_t`

        u_path : array_like(float)
            A k x T matrix, where the t-th column represents :math:`u_t`

        w_path : array_like(float)
            A j x T+1 matrix, where the t-th column represent :math:`w_t`

        """
        A, B, C = self.A, self.B, self.C
        if self.T:
            T = self.T if not ts_length else min(ts_length, self.T)
            self.P, self.d = self.Rf, 0
        else:
            T = ts_length if ts_length else 100
            if self.P is None:
                self.stationary_values(method=method)
        random_state = check_random_state(random_state)
        x0 = np.asarray(x0)
        x0 = x0.reshape(self.n, 1)
        x_path = np.empty((self.n, T + 1))
        u_path = np.empty((self.k, T))
        w_path = random_state.randn(self.j, T + 1)
        Cw_path = dot(C, w_path)
        policies = []
        for t in range(T):
            if self.T:
                self.update_values()
            policies.append(self.F)

        F = policies.pop()
        x_path[:, 0] = x0.flatten()
        u_path[:, 0] = -dot(F, x0).flatten()
        for t in range(1, T):
            F = policies.pop()
            Ax, Bu = dot(A, x_path[:, t - 1]), dot(B, u_path[:, t - 1])
            x_path[:, t] = Ax + Bu + Cw_path[:, t]
            u_path[:, t] = -dot(F, x_path[:, t])

        Ax, Bu = dot(A, x_path[:, T - 1]), dot(B, u_path[:, T - 1])
        x_path[:, T] = Ax + Bu + Cw_path[:, T]
        return (
         x_path, u_path, w_path)


class LQMarkov:
    __doc__ = "\n    This class is for analyzing Markov jump linear quadratic optimal\n    control problems of the infinite horizon form\n\n    .. math::\n\n        \\min \\mathbb{E}\n        \\Big[ \\sum_{t=0}^{\\infty} \\beta^t r(x_t, s_t, u_t) \\Big]\n\n    with\n\n    .. math::\n\n         r(x_t, s_t, u_t) :=\n            (x_t' R(s_t) x_t + u_t' Q(s_t) u_t + 2 u_t' N(s_t) x_t)\n\n    subject to the law of motion\n\n    .. math::\n\n         x_{t+1} = A(s_t) x_t + B(s_t) u_t + C(s_t) w_{t+1}\n\n    Here :math:`x` is n x 1, :math:`u` is k x 1, :math:`w` is j x 1 and the\n    matrices are conformable for these dimensions.  The sequence :math:`{w_t}`\n    is assumed to be white noise, with zero mean and\n    :math:`\\mathbb{E} [ w_t' w_t ] = I`, the j x j identity.\n\n    If :math:`C` is not supplied as a parameter, the model is assumed to be\n    deterministic (and :math:`C` is set to a zero matrix of appropriate\n    dimension).\n\n    The optimal value function :math:`V(x_t, s_t)` takes the form\n\n    .. math::\n\n         x_t' P(s_t) x_t + d(s_t)\n\n    and the optimal policy is of the form :math:`u_t = -F(s_t) x_t`.\n\n    Parameters\n    ----------\n    Π : array_like(float, ndim=2)\n        The Markov chain transition matrix with dimension m x m.\n    Qs : array_like(float)\n        Consists of m symmetric and non-negative definite payoff\n        matrices Q(s) with dimension k x k that corresponds with\n        the control variable u for each Markov state s\n    Rs : array_like(float)\n        Consists of m symmetric and non-negative definite payoff\n        matrices R(s) with dimension n x n that corresponds with\n        the state variable x for each Markov state s\n    As : array_like(float)\n        Consists of m state transition matrices A(s) with dimension\n        n x n for each Markov state s\n    Bs : array_like(float)\n        Consists of m state transition matrices B(s) with dimension\n        n x k for each Markov state s\n    Cs : array_like(float), optional(default=None)\n        Consists of m state transition matrices C(s) with dimension\n        n x j for each Markov state s. If the model is deterministic\n        then Cs should take default value of None\n    Ns : array_like(float), optional(default=None)\n        Consists of m cross product term matrices N(s) with dimension\n        k x n for each Markov state,\n    beta : scalar(float), optional(default=1)\n        beta is the discount parameter\n\n    Attributes\n    ----------\n    Π, Qs, Rs, Ns, As, Bs, Cs, beta : see Parameters\n    Ps : array_like(float)\n        Ps is part of the value function representation of\n        :math:`V(x, s) = x' P(s) x + d(s)`\n    ds : array_like(float)\n        ds is part of the value function representation of\n        :math:`V(x, s) = x' P(s) x + d(s)`\n    Fs : array_like(float)\n        Fs is the policy rule that determines the choice of control in\n        each period at each Markov state\n    m : scalar(int)\n        The number of Markov states\n    k, n, j : scalar(int)\n        The dimensions of the matrices as presented above\n\n    "

    def __init__(self, Π, Qs, Rs, As, Bs, Cs=None, Ns=None, beta=1):

        def converter(Xs):
            return np.array([np.atleast_2d(np.asarray(X, dtype='float')) for X in Xs])

        self.As, self.Bs, self.Qs, self.Rs = list(map(converter, (
         As, Bs, Qs, Rs)))
        self.m = self.Qs.shape[0]
        self.k, self.n = self.Qs.shape[1], self.Rs.shape[1]
        if Ns is None:
            Ns = [np.zeros((self.k, self.n)) for i in range(self.m)]
        self.Ns = converter(Ns)
        if Cs is None:
            self.j = 1
            Cs = [np.zeros((self.n, self.j)) for i in range(self.m)]
        self.Cs = converter(Cs)
        self.j = self.Cs.shape[2]
        self.beta = beta
        self.Π = np.asarray(Π, dtype='float')
        self.Ps = None
        self.ds = None
        self.Fs = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        m = '        Markov Jump Linear Quadratic control system\n          - beta (discount parameter)       : {b}\n          - T (time horizon)                : {t}\n          - m (number of Markov states)     : {m}\n          - n (number of state variables)   : {n}\n          - k (number of control variables) : {k}\n          - j (number of shocks)            : {j}\n        '
        t = 'infinite'
        return dedent(m.format(b=(self.beta), m=(self.m), n=(self.n), k=(self.k), j=(self.j),
          t=t))

    def stationary_values(self):
        """
        Computes the matrix :math:`P(s)` and scalar :math:`d(s)` that
        represent the value function

        .. math::

             V(x, s) = x' P(s) x + d(s)

        in the infinite horizon case.  Also computes the control matrix
        :math:`F` from :math:`u = - F(s) x`.

        Returns
        -------
        Ps : array_like(float)
            Ps is part of the value function representation of
            :math:`V(x, s) = x' P(s) x + d(s)`
        ds : array_like(float)
            ds is part of the value function representation of
            :math:`V(x, s) = x' P(s) x + d(s)`
        Fs : array_like(float)
            Fs is the policy rule that determines the choice of control in
            each period at each Markov state

        """
        beta, Π = self.beta, self.Π
        m, n, k = self.m, self.n, self.k
        As, Bs, Cs = self.As, self.Bs, self.Cs
        Qs, Rs, Ns = self.Qs, self.Rs, self.Ns
        Ps = solve_discrete_riccati_system(Π, As, Bs, Cs, Qs, Rs, Ns, beta)
        Fs = np.array([np.empty((k, n)) for i in range(m)])
        X = np.empty((m, m))
        sum1, sum2 = np.empty((k, k)), np.empty((k, n))
        for i in range(m):
            CCi = Cs[i] @ Cs[i].T
            sum1[:, :] = 0.0
            sum2[:, :] = 0.0
            for j in range(m):
                sum1 += beta * Π[(i, j)] * Bs[i].T @ Ps[j] @ Bs[i]
                sum2 += beta * Π[(i, j)] * Bs[i].T @ Ps[j] @ As[i]
                X[(j, i)] = np.trace(Ps[j] @ CCi)

            Fs[i][:, :] = solve(Qs[i] + sum1, sum2 + Ns[i])

        ds = solve(np.eye(m) - beta * Π, np.diag(beta * Π @ X).reshape((m, 1))).flatten()
        self.Ps, self.ds, self.Fs = Ps, ds, Fs
        return (
         Ps, ds, Fs)

    def compute_sequence(self, x0, ts_length=None, random_state=None):
        """
        Compute and return the optimal state and control sequences
        :math:`x_0, ..., x_T` and :math:`u_0,..., u_T`  under the
        assumption that :math:`{w_t}` is iid and :math:`N(0, 1)`,
        with Markov states sequence :math:`s_0, ..., s_T`

        Parameters
        ----------
        x0 : array_like(float)
            The initial state, a vector of length n

        ts_length : scalar(int), optional(default=None)
            Length of the simulation. If None, T is set to be 100

        random_state : int or np.random.RandomState, optional
            Random seed (integer) or np.random.RandomState instance to set
            the initial state of the random number generator for
            reproducibility. If None, a randomly initialized RandomState is
            used.

        Returns
        -------
        x_path : array_like(float)
            An n x T+1 matrix, where the t-th column represents :math:`x_t`

        u_path : array_like(float)
            A k x T matrix, where the t-th column represents :math:`u_t`

        w_path : array_like(float)
            A j x T+1 matrix, where the t-th column represent :math:`w_t`

        state : array_like(int)
            Array containing the state values :math:`s_t` of the sample path

        """
        if self.Ps is None:
            self.stationary_values()
        As, Bs, Cs = self.As, self.Bs, self.Cs
        Fs = self.Fs
        random_state = check_random_state(random_state)
        x0 = np.asarray(x0)
        x0 = x0.reshape(self.n, 1)
        T = ts_length if ts_length else 100
        chain = MarkovChain(self.Π)
        state = chain.simulate_indices(ts_length=(T + 1), random_state=random_state)
        x_path = np.empty((self.n, T + 1))
        u_path = np.empty((self.k, T))
        w_path = random_state.randn(self.j, T + 1)
        Cw_path = np.empty((self.n, T + 1))
        for i in range(T + 1):
            Cw_path[:, i] = Cs[state[i]] @ w_path[:, i]

        x_path[:, 0] = x0.flatten()
        u_path[:, 0] = -(Fs[state[0]] @ x0).flatten()
        for t in range(1, T):
            Ax = As[state[t]] @ x_path[:, t - 1]
            Bu = Bs[state[t]] @ u_path[:, t - 1]
            x_path[:, t] = Ax + Bu + Cw_path[:, t]
            u_path[:, t] = -(Fs[state[t]] @ x_path[:, t])

        Ax = As[state[T]] @ x_path[:, T - 1]
        Bu = Bs[state[T]] @ u_path[:, T - 1]
        x_path[:, T] = Ax + Bu + Cw_path[:, T]
        return (
         x_path, u_path, w_path, state)