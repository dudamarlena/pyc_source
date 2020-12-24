# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arf_tools/src/classifiers/logistic_regression.py
# Compiled at: 2018-04-07 22:01:38
# Size of source mod 2**32: 2397 bytes
""" Ce module contient toutes les fonctions nécessaires pour effectuer une
régression logistique et appliquer un algorithme de descente de gradient.
"""
import numpy as np

class LogisticRegression:
    __doc__ = ' Classifieur effectuant une regression logistique grâce à une descente\n    de gradient.\n    '

    def __init__(self, eps=0.001, max_iter=1000, label_neg=0, label_pos=1):
        self.eps = eps
        self.max_iter = max_iter
        self.label_neg = label_neg
        self.label_pos = label_pos

    def fit(self, datax, datay):
        self.w = self.optimize(datax=datax, datay=datay, winit=np.random.random((1, datax.shape[1])), eps=self.eps, max_iter=self.max_iter)

    def predict(self, datax):
        if sigmoide(self.w.dot(datax.T)) >= 0.5:
            return self.label_pos
        return self.label_neg

    def score(self, datax, datay):
        y_hat = np.array([self.predict(x) for x in datax])
        return (y_hat == datay).mean()

    def optimize(self, datax, datay, winit, eps, max_iter):
        w = winit
        for _ in range(max_iter):
            w += eps * self.cost_d(w, datax, datay)

        return w

    def cost_d(self, w, x, y):
        return (y - sigmoide(w.dot(x.T))).dot(x)


def optimize(fonc, dfonc, xinit, eps=0.001, max_iter=1000):
    """ Applique l'algorithme de la descente de gradient.
    :param: fonc, la fonction à optimiser.
    :param: dfonc, le gradient de cette fonction.
    :param: xinit, le point initial.
    :param: eps, le pas du gradient.
    :param: max_iter, le nombre d'itérations.
    :return: un tuple (x_histo, f_histo, grad_histo).
    """
    x_histo, f_histo, grad_histo = np.array([xinit]), np.array([fonc(*xinit)]), np.array([np.array(dfonc(*xinit))])
    for _ in range(max_iter):
        x = x_histo[(-1)] - eps * grad_histo[(-1)]
        x_histo = np.vstack((x_histo, x))
        f_histo = np.vstack((f_histo, fonc(*x.T)))
        grad_histo = np.vstack((grad_histo, np.array([dfonc(*x.T)])))

    return (x_histo, f_histo, grad_histo)


def sigmoide(x):
    return 1 / (1 + np.exp(-x))


if __name__ == '__main__':
    pass