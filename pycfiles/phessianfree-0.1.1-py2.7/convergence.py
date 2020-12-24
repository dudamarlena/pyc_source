# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/phessianfree/convergence.py
# Compiled at: 2012-10-30 20:31:17
import numpy
from numpy import *
import matplotlib, matplotlib.pyplot as plt

def plot(methods, objRange=None):
    """
    Plots test objective and gradient norms for the passed optimization traces.
    
    :param list methods: PlottingCallback objects, containing the trace of 
        optimization for the methods you want to plot against each other.
    """
    linestyles = [
     '-', '--', ':', '-.', '-', '--', '-.', ':']
    colors = ['k', 'r', 'b', 'g', 'DarkOrange', 'm', 'y', 'c', 'Pink']
    captions = [ m.mname for m in methods ]
    fig = plt.figure(figsize=(8, 3))
    axg = fig.add_subplot(1, 2, 1)
    axl = fig.add_subplot(1, 2, 2)
    for i in range(len(methods)):
        kargs = {'linestyle': linestyles[i], 'color': colors[i]}
        axg.plot(methods[i].iterEquiv, methods[i].gs, **kargs)
        axl.plot(methods[i].iterEquiv, methods[i].fvals, **kargs)

    axg.set_yscale('log')
    axg.set_ylabel('Gradient norm')
    axg.set_xlabel('Effective iterations')
    axl.set_ylabel('Training objective value')
    axl.set_xlabel('Effective iterations')
    axl.legend(captions, 'upper right', prop={'size': 10})
    if objRange is not None:
        axl.set_ylim(objRange)
    plt.tight_layout()
    plt.show()
    return


class PlottingCallback(object):

    def __init__(self, mname, ndata):
        self.xs = []
        self.fvals = []
        self.gs = []
        self.pps = []
        self.iterEquiv = []
        self.pp_total = 0
        self.mname = mname
        self.ndata = ndata

    def __call__(self, x, fval, g, pp):
        self.xs.append(x)
        self.fvals.append(fval)
        self.gs.append(linalg.norm(g))
        self.pps.append(pp)
        self.iterEquiv.append(pp / float(self.ndata))
        self.pp_total = pp


class PlottingWrapper(PlottingCallback):
    """ 
        This provides the same tracking of intermediate gradients and function 
        values as the PlottingCallback, but by wrapping the objective function.
        Mainly of use for gathering convergence stats for plotting of scipy's
        optimization functions.
    """

    def __init__(self, f, mname, ndata):
        self.f = f
        super(PlottingWrapper, self).__init__(mname, ndata)

    def __call__(self, x):
        fval, g = self.f(x)
        if len(self.fvals) == 0 or self.fvals[(-1)] >= fval:
            super(PlottingWrapper, self).__call__(x, fval, g, self.pp_total + self.ndata)
        return (
         fval, g)