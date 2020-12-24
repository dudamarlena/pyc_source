# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arf_tools/src/classifiers/naive_bayes.py
# Compiled at: 2018-04-07 21:39:03
# Size of source mod 2**32: 2090 bytes
""" Ce module contient toutes les fonctions nécessaires pour implémenter un
classifieur bayésien naïf.
"""
import numpy as np

def gaussian(x, mu, sigma):
    return 1 / np.sqrt(2 * np.pi * sigma) * np.exp(-(x - mu) ** 2 / (2 * sigma))


class NaiveBayes:
    __doc__ = " Classifieur bayésien naïf gaussien.\n\n    all_labels: Tous les labels possibles\n    P_y: dictionnaire mappant chaque classe à sa probabilité d'apparition.\n    P_X_Y_mean: dictionnaire mappant chaque classe à la moyenne de chaque\n                exemple.\n    P_X_Y_std: dictionnaire mappant chaque classe à la variance de chaque\n               exemple.\n    "

    def __init__(self, label_neg=0, label_pos=1, density=gaussian):
        self.label_neg = label_neg
        self.label_pos = label_pos
        self.density = gaussian
        self.P_y = dict()
        self.P_X_Y_mean = dict()
        self.P_X_Y_std = dict()
        self.all_labels = np.array()

    def fit(self, datax, datay):
        self.all_labels = np.array(list(set(datay)))
        for label in self.all_labels:
            self.P_y[label] = len(np.where(datay == label)[0]) / len(datay)
            self.P_X_Y_mean[label] = datax[np.where(datay == label)[0]].mean(axis=0)
            self.P_X_Y_std[label] = datax[np.where(datay == label)[0]].std(axis=0)

    def predict(self, datax):
        max_y = None
        max_value = None
        for y in self.all_labels:
            value = np.log(self.P_y[y]) + self.p_x_given_y(datax, y)
            if max_y is None or value > max_value:
                max_y, max_value = y, value

        return max_y

    def score(self, datax, datay):
        y_hat = np.array([self.predict(x) for x in datax])
        return (y_hat == datay).mean()

    def p_x_given_y(self, datax, y):
        return sum([np.log(self.density(x, mean, std)) for x, mean, std in zip(datax, self.P_X_Y_mean[y], self.P_X_Y_std[y])])


if __name__ == '__main__':
    pass