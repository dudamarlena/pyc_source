# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arf_tools/src/classifiers/density_estimation.py
# Compiled at: 2018-04-13 18:35:52
# Size of source mod 2**32: 2654 bytes
""" This module contains all methods used for evaluating density functions.

Authors :
* BIZZOZZERO Nicolas
* ADOUM Robert
"""
import numpy as np, utils.kernels as kernels

class EstimateurHistogramme:

    def __init__(self, steps=100):
        self.steps = steps
        self.tab = np.array([np.array([0 for _ in range(self.steps)]) for _ in range(self.steps)])

    def fit(self, data):
        self.xmin, self.xmax = data[:, 0].min(), data[:, 0].max()
        self.ymin, self.ymax = data[:, 1].min(), data[:, 1].max()
        self.step_x = (self.xmax - self.xmin) / self.steps
        self.step_y = (self.ymax - self.ymin) / self.steps
        for poi_x, poi_y in data:
            bin_x = self._bin_x(poi_x)
            bin_y = self._bin_y(poi_y)
            self.tab[(bin_y, bin_x)] += 1

        self.tab = self.tab / len(data)

    def predict(self, liste_points):
        tab = []
        for poi_x, poi_y in liste_points:
            bin_x = self._bin_x(poi_x)
            bin_y = self._bin_y(poi_y)
            tab.append(self.tab[bin_y][bin_x])

        return np.array(tab)

    def _bin_x(self, poi_x):
        """ Transforme un echantillon en dehors du domaine de l'estimateur en
        un echantillon dans le domaine de l'estimateur.
        Applicable sur l'axe X.
        """
        if poi_x < self.xmin:
            return 0
        else:
            if poi_x >= self.xmax:
                return -1
            return int((poi_x - self.xmin) // self.step_x)

    def _bin_y(self, poi_y):
        """ Transforme un echantillon en dehors du domaine de l'estimateur en
        un echantillon dans le domaine de l'estimateur.
        Applicable sur l'axe Y.
        """
        if poi_y < self.ymin:
            return 0
        else:
            if poi_y >= self.ymax:
                return -1
            return int((poi_y - self.ymin) // self.step_y)


class EstimateurNoyau:

    def __init__(self, noyau=kernels.parzen_ND, fenetre=0.8):
        self.noyau = noyau
        self.fenetre = fenetre

    def fit(self, data):
        self.data = data
        self.N, self.d = data.shape

    def predict(self, liste_points):
        tab = []
        for point in liste_points:
            somme = np.array([self.noyau((point - xi) / self.fenetre) for xi in self.data]).sum()
            somme /= self.N
            tab.append(somme)

        return np.array(tab)


if __name__ == '__main__':
    pass