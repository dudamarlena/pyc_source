# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/plsre/PlsRegression.py
# Compiled at: 2020-04-30 14:50:26
# Size of source mod 2**32: 3415 bytes
import numpy as np
from numpy import linalg as LA
from numba import jit

def data_preprocessing(X, Y):
    """Function to mean-center and scale the orignal dataset."""
    X = (X - np.mean(X)) / np.std(X)
    Y = (Y - np.mean(Y)) / np.std(Y)
    return (
     X, Y)


def plsr_block(X, Y, max_iter, tol):
    """This function helps to find outer relation between blocks."""
    X, Y = data_preprocessing(X, Y)
    y = Y[:, np.random.randint(Y.shape[1])]
    u = y
    ite = 0
    old_t = 0
    while ite < max_iter:
        w_t = u.T @ X / (u.T @ u)
        w_t = w_t / LA.norm(w_t)
        t = X @ w_t.T / (w_t @ w_t.T)
        q_t = t.T @ Y / (t.T @ t)
        q_t = q_t / LA.norm(q_t)
        u = Y @ q_t.T / LA.norm(q_t @ q_t.T)
        if abs(LA.norm(t) - LA.norm(old_t)) < tol:
            break
        old_t = t
        ite = ite + 1

    p_t = t.T @ X / LA.norm(t)
    p_t = p_t / LA.norm(p_t)
    t = t * LA.norm(p_t)
    w_t = w_t * LA.norm(w_t)
    return (
     p_t, q_t, w_t, t, u)


def plsr_train(X, Y, num_comp=2, max_iter=600, tol=1e-07):
    """This funtion trains plsr by finding inner relation."""
    X, Y = data_preprocessing(X, Y)
    E = np.zeros([num_comp, X.shape[0], X.shape[1]])
    F = np.zeros([num_comp, Y.shape[0], Y.shape[1]])
    B = np.zeros([num_comp])
    W_T = np.zeros([X.shape[1], num_comp])
    P_T = np.zeros([X.shape[1], num_comp])
    Q_T = np.zeros([Y.shape[1], num_comp])
    T = np.zeros([X.shape[0], num_comp])
    E[0], F[0] = X, Y
    for h in range(num_comp):
        p_t, q_t, w_t, t, u = plsr_block(E[h], F[h], max_iter, tol)
        b = u.T @ t / LA.norm(t)
        if h < num_comp - 1:
            E[h + 1] = E[h] - t.reshape(-1, 1) @ p_t.reshape(1, -1)
            F[h + 1] = F[h] - b * (t.reshape(-1, 1) @ q_t.reshape(1, -1))
        P_T[:, h] = p_t
        Q_T[:, h] = q_t
        W_T[:, h] = w_t
        T[:, h] = t
        B[h] = b

    return (
     P_T, Q_T, W_T, T, B)


def plsr_predict(X, Y, P, Q, W, B, num_comp=2):
    """Function used to predict new data ."""
    X_ = X.copy()
    Y_hat = np.zeros_like(Y)
    for h in range(num_comp):
        t = X_ @ W[:, h]
        for i in range(X_.shape[0]):
            for j in range(P.shape[0]):
                X_[(i, j)] = X_[(i, j)] - t[i] * P[(j, h)]

            for m in range(Q.shape[0]):
                Y_hat[(i, m)] = Y_hat[(i, m)] + B[h] * t[i] * Q[(m, h)]

    return Y_hat


@jit(nopython=True, cache=True)
def plsr_predict_numba(X, Y, P, Q, W, B, num_comp=2):
    """Function used to predict new data using numba."""
    X_ = X.copy()
    Y_hat = np.zeros_like(Y)
    for h in range(num_comp):
        t = X_ @ W[:, h]
        for i in range(X_.shape[0]):
            for j in range(P.shape[0]):
                X_[(i, j)] = X_[(i, j)] - t[i] * P[(j, h)]

            for m in range(Q.shape[0]):
                Y_hat[(i, m)] = Y_hat[(i, m)] + B[h] * t[i] * Q[(m, h)]

    return Y_hat


def plsr_predict_numpy(X, Y, P, Q, W, B, num_comp=2):
    """Function used to predict new data using vectorization and broadcasting."""
    X_ = X.copy()
    Y_hat = np.zeros_like(Y)
    for h in range(num_comp):
        t = X_ @ W[:, h]
        X_ = X_ - t.reshape(-1, 1) @ P[:, h].reshape(1, -1)
        Y_hat = Y_hat + B[h] * t.reshape(-1, 1) @ Q[:, h].reshape(1, -1)

    return Y_hat