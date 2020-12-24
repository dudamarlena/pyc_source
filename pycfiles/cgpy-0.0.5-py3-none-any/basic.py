# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\examples\basic.py
# Compiled at: 2012-02-14 07:44:45
__doc__ = '\nBasic example of cGP study of the FitzHugh-Nagumo model of nerve membrane.\n\n.. plot::\n    :width: 400\n    :include-source:\n        \n    from cgp.examples.basic import fitzhugh\n    import scipy.integrate\n    \n    t = np.arange(0, 50, 0.1)\n    y = scipy.integrate.odeint(fitzhugh, [-0.6, -0.6], t)\n    plt.plot(t, y)\n    plt.legend(["V (transmembrane potential)", "W (recovery variable)"])\n\n..  plot::\n    \n    from cgp.examples.basic import cgpstudy\n    cgpstudy()\n\nThe code in this file is ready to run, but is primarily written to be *read*.\nIt exemplifies the building blocks of a cGP model study:\n\n..  list-table::\n    :header-rows: 1\n\n    * * Component\n      * Description\n      * Example\n    * * Generation of genotypes\n      * Genotypic variation whose phenotypic effects are to be estimated.\n      * Full enumeration feasible if the genotype space is small.\n        Other options include pedigrees or statistical experimental designs.\n    * * Genotype-to-parameter map\n      * Lumping together lower-level physiology such as gene regulation\n      * Maximum conductances of ion channels\n    * * Parameter-to-phenotype map\n      * Physiological model\n      * Heart cell electrophysiology\n    * * Virtual experiment\n      * Manipulating the physiological model\n      * Pacing with electrical stimuli\n    * * Aggregate phenotypes\n      * Summarizing the raw model output\n      * Action potential duration\n    * * Analysis, summary, visualization\n      *\n      *\n\nThis very simple example defines most components in one file for illustration. \nReal applications will typically draw upon existing code libraries, model \nrepositories and databases. Linking these together may require a lot of code, \na complication which we ignore here to make the main concepts stand out more\nclearly.\n\nOur example system is the :func:`FitzHugh-Nagumo model <fitzhugh>` of an \nexcitable heart muscle cell. It has four parameters, one of which represents \na stimulus current. Virtual pacing of the cell can be implemented by setting \nthe stimulus current to a nonzero value at regular intervals. The resulting \n"action potential" (time-course of transmembrane voltage) is often \ncharacterized by its duration, for instance APD90 for the action potential \nduration to 90 % repolarization.\n\nHere, we assume that each parameter is governed by a single gene of which \nthere are two alleles. This trivial genotype-to-parameter map is a caricature \nin the absence of actual data, but is a minimal assumption to make the model \namenable to cGP analysis.\n\nHere we can compute phenotypes for all 27 genotypes (three loci with three \npossibilities each gives \naa bb cc, aa bb Cc, aa bb CC, aa Bb cc, ..., AA BB CC). In higher-dimensional \ncases, the genotype space must be sampled according to some experimental \ndesign, possibly constrained by pedigree information.\n\n\nReferences:\n\n* FitzHugh R (1961) \n  :doi:`Impulses and physiological states\n  in theoretical models of nerve membrane \n  <10.1016/S0006-3495(61)86902-6>`. \n  Biophysical J. 1:445-466\n* FitzHugh R (1969) \n  Mathematical models of excitation and propagation in nerve. \n  In: :isbn:`Biological engineering <978-0070557345>`, \n  ed. H. P. Schwan, 1-85. New York: McGraw-Hill.\n\nIn the original version (FitzHugh 1961), the definition of the transmembrane\npotential is such that it decreases during depolarization, so that the\naction potential starts with a downstroke, contrary to the convention used\nin FitzHugh 1969 and in most other work. The equations are also somewhat\nrearranged. However, figure 1 of FitzHugh 1961 gives a very good overview of\nthe phase plane of the model.\n'
import numpy as np, scipy.integrate
from matplotlib import pyplot as plt
from cgp.gt.genotype import Genotype
from cgp.gt.gt2par import monogenicpar
from cgp.utils.extrema import extrema
from cgp.utils.splom import spij
from cgp.utils.recfun import cbind, restruct
par0 = np.rec.array([(0.7, 0.8, 0.08, 0.0)], names=('a b theta I').split())
absvar = np.array([(0.5, 0.5, 0.05, 0.05)])
genotypes = Genotype(names=par0.dtype.names)

def fitzhugh(y, t=None, par=par0):
    """
    FitzHugh (1969) version of FitzHugh-Nagumo model of nerve membrane.
    
    Default parameter values are from FitzHugh (1969), figure 3-2.
    
    :param array_like y: State vector [V, W],where V is the transmembrane 
        potential and W is a "recovery variable".
    :param scalar t: Time. Ignored, but required by scipy.integrate.odeint.
    :param float a, b, theta: Positive constants.
    :param float I: Transmembrane stimulus current.
    
    References: see :mod:`module docstring <cgp.examples.basic>`.
    
    .. seealso:: :class:`cgp.virtexp.examples.Fitz`.
    """
    V, W = y
    a, b, theta, I = par.item()
    Vdot = V - V * V * V / 3.0 - W + I
    Wdot = theta * (V + a - b * W)
    return (
     Vdot, Wdot)


def gt2par(gt):
    """Genotype-to-parameter mapping."""
    return monogenicpar(gt, hetpar=par0, absvar=absvar)


def par2ph(par):
    """Parameter-to-phenotype mapping."""
    y0 = np.rec.array([(-0.5, -0.5)], dtype=[('V', float), ('W', float)])
    t = np.rec.fromarrays([np.arange(0, 1000, 0.1)], names='t')
    y = scipy.integrate.odeint(fitzhugh, y0.item(), t.t, args=(par,))
    return restruct(cbind(t, y.view(y0.dtype)))


def ph2agg(ph, tol=0.001):
    """Phenotype aggregation."""
    e = extrema(ph['V'], withend=False)
    peak = e[(e.curv < 0)]
    trough = e[(e.curv > 0)]
    if len(peak.index) >= 2:
        t0, t1 = ph['t'].squeeze()[peak.index[-2:]]
        period = t1 - t0
        amplitude = peak.value[(-1)] - trough.value[(-1)]
        if amplitude < tol:
            period = amplitude = 0.0
    else:
        period = amplitude = 0.0
    return np.rec.fromrecords([(period, amplitude)], names=[
     'period', 'amplitude'])


def summarize(gt, agg):
    """Scatterplot matrix of aggregated phenotypes vs genotypes."""
    for i, ai in enumerate(agg.dtype.names):
        for j, gj in enumerate(gt.dtype.names):
            spij(len(agg.dtype.names), len(gt.dtype.names), i, j)
            plt.plot(gt[gj], agg[ai], 'o')
            xmin, xmax, ymin, ymax = plt.axis()
            ypad = 0.1 * (ymax - ymin)
            plt.axis([xmin - 0.5, xmax + 0.5, -ypad, ymax + ypad])
            plt.axis()
            if i == len(agg.dtype) - 1:
                plt.xlabel(gj)
            if j == 0:
                plt.ylabel(ai)


def pad_plot():
    """Adjust axis limits to fully show markers."""
    for ax in plt.gcf().axes:
        plt.axes(ax)
        ymin, ymax = plt.ylim()
        ypad = 0.1 * (ymax - ymin)
        plt.axis([-0.5, 2.5, -ypad, ymax + ypad])


def cgpstudy():
    """
    Basic example of connecting the building blocks of a cGP study.
    
    This top-level orchestration can be done in many different ways, depending 
    on personal preference and on the need for features such as storage, 
    caching, memory management or parallelization. Some examples are given in 
    :mod:`cgp.examples.hpc`.
    """
    from numpy import concatenate as cat
    gt = np.array(genotypes)
    par = cat([ monogenicpar(g, hetpar=par0, absvar=absvar) for g in gt ])
    ph = cat([ par2ph(p) for p in par ])
    agg = cat([ ph2agg(p) for p in ph ])
    summarize(gt, agg)
    plt.show()


if __name__ == '__main__':
    cgpstudy()