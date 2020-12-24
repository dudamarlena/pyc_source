# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ambhas/errlib.py
# Compiled at: 2013-02-19 05:23:06
__doc__ = "\nCreated on Thu Jan 20 15:36:37 2011\n@ author:                  Sat Kumar Tomer \n@ author's webpage:        http://civil.iisc.ernet.in/~satkumar/\n@ author's email id:       satkumartomer@gmail.com\n@ author's website:        www.ambhas.com\n\nA libray with Python functions for calculations of \nmicrometeorological parameters and some miscellaneous\nutilities.\n\nfunctions:\n    pc_bias : percentage bias\n    apb :     absolute percent bias\n    rmse :    root mean square error\n    mae :     mean absolute error\n    bias :    bias\n    NS :      Nash-Sutcliffe Coefficient\n    L:        likelihood estimation\n    correlation: correlation\n    \n"
import numpy as np
from random import randrange
import matplotlib.pyplot as plt

def filter_nan(s, o):
    """
    this functions removed the data  from simulated and observed data
    whereever the observed data contains nan
    
    this is used by all other functions, otherwise they will produce nan as 
    output
    """
    data = np.array([s.flatten(), o.flatten()])
    data = np.transpose(data)
    data = data[(~np.isnan(data).any(1))]
    return (
     data[:, 0], data[:, 1])


def pc_bias(s, o):
    """
    Percent Bias
    input:
        s: simulated
        o: observed
    output:
        pc_bias: percent bias
    """
    s, o = filter_nan(s, o)
    return 100.0 * sum(s - o) / sum(o)


def apb(s, o):
    """
    Absolute Percent Bias
    input:
        s: simulated
        o: observed
    output:
        apb_bias: absolute percent bias
    """
    s, o = filter_nan(s, o)
    return 100.0 * sum(abs(s - o)) / sum(o)


def rmse(s, o):
    """
    Root Mean Squared Error
    input:
        s: simulated
        o: observed
    output:
        rmses: root mean squared error
    """
    s, o = filter_nan(s, o)
    return np.sqrt(np.mean((s - o) ** 2))


def mae(s, o):
    """
    Mean Absolute Error
    input:
        s: simulated
        o: observed
    output:
        maes: mean absolute error
    """
    s, o = filter_nan(s, o)
    return np.mean(abs(s - o))


def bias(s, o):
    """
    Bias
    input:
        s: simulated
        o: observed
    output:
        bias: bias
    """
    s, o = filter_nan(s, o)
    return np.mean(s - o)


def NS(s, o):
    """
    Nash Sutcliffe efficiency coefficient
    input:
        s: simulated
        o: observed
    output:
        ns: Nash Sutcliffe efficient coefficient
    """
    s, o = filter_nan(s, o)
    return 1 - sum((s - o) ** 2) / sum((o - np.mean(o)) ** 2)


def L(s, o, N=5):
    """
    Likelihood 
    input:
        s: simulated
        o: observed
    output:
        L: likelihood
    """
    s, o = filter_nan(s, o)
    return np.exp(-N * sum((s - o) ** 2) / sum((o - np.mean(o)) ** 2))


def correlation(s, o):
    """
    correlation coefficient
    input:
        s: simulated
        o: observed
    output:
        correlation: correlation coefficient
    """
    s, o = filter_nan(s, o)
    if s.size == 0:
        corr = np.NaN
    else:
        corr = np.corrcoef(o, s)[(0, 1)]
    return corr


def index_agreement(s, o):
    """
        index of agreement
        input:
        s: simulated
        o: observed
    output:
        ia: index of agreement
    """
    s, o = filter_nan(s, o)
    ia = 1 - np.sum((o - s) ** 2) / np.sum((np.abs(s - np.mean(o)) + np.abs(o - np.mean(o))) ** 2)
    return ia


class KAPPA:

    def __init__(self, s, o):
        s = s.flatten()
        o = o.flatten()
        if len(s) != len(o):
            raise Exception('Length of both the vectors must be same')
        self.s = s.astype(int)
        self.o = o.astype(int)

    def kappa_coeff(self):
        s = self.s
        o = self.o
        n = len(s)
        foo1 = np.unique(s)
        foo2 = np.unique(o)
        unique_data = np.unique(np.hstack([foo1, foo2]).flatten())
        self.unique_data = unique_data
        kappa_mat = np.zeros((len(unique_data), len(unique_data)))
        ind1 = np.empty(n, dtype=int)
        ind2 = np.empty(n, dtype=int)
        for i in range(len(unique_data)):
            ind1[s == unique_data[i]] = i
            ind2[o == unique_data[i]] = i

        for i in range(n):
            kappa_mat[(ind1[i], ind2[i])] += 1

        self.kappa_mat = kappa_mat
        tot = np.sum(kappa_mat)
        Pa = np.sum(np.diag(kappa_mat)) / tot
        PA = np.sum(kappa_mat, axis=0) / tot
        PB = np.sum(kappa_mat, axis=1) / tot
        Pe = np.sum(PA * PB)
        kappa_coeff = (Pa - Pe) / (1 - Pe)
        return (
         kappa_mat, kappa_coeff)

    def kappa_figure(self, fname, data, data_name):
        data = np.array(data)
        data = data.astype(int)
        try:
            self.kappa_mat
        except:
            self.kappa_coeff()

        kappa_mat = self.kappa_coeff()
        unique_data = self.unique_data
        tick_labels = []
        for i in range(len(unique_data)):
            unique_data[i] == data
            tick_labels.append(data_name[find(data == unique_data[i])])

        plt.subplots_adjust(left=0.3, top=0.8)
        plt.imshow(kappa_mat, interpolation='nearest', origin='upper')
        plt.xticks(range(len(unique_data)), tick_labels, rotation='vertical')
        plt.yticks(range(len(unique_data)), tick_labels)
        plt.colorbar(shrink=0.8)
        plt.savefig(fname)
        plt.close()


if __name__ == '__main__':
    obs = np.random.normal(size=100)
    sim = np.random.normal(size=100)
    print pc_bias(sim, obs)
    print apb(sim, obs)
    print rmse(sim, obs)
    print mae(sim, obs)
    print bias(sim, obs)
    print NS(sim, obs)
    print L(sim, obs)
    print correlation(sim, obs)
    kappa_class = KAPPA(soil_sat, soil_obs)
    kappa_mat, kappa_coeff = kappa_class.kappa_coeff()
    data = range(1, 14)
    data_name = ['silty_loam', 'sand', 'silty_clay_loam', 'loam', 'clay_loam',
     'sandy_loam', 'silty_clay', 'sandy_clay_loam', 'loamy_sand ',
     'clay', 'silt', 'sandy_clay', 'gravelly_sandy_loam']
    fname = '/home/tomer/svn/ambhas/examples/kappa.png'