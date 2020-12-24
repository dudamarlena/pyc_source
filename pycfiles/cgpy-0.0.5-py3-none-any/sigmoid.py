# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\examples\sigmoid.py
# Compiled at: 2013-01-14 06:47:43
__doc__ = '\nBasic example of cGP study using sigmoid model of gene regulatory networks.\n\nThis example is taken from Gjuvsland et al. (2011), the gene regulatory model \nis eq.(15) in that paper, and the example code reproduces figure 4a.\n\n.. plot::\n    :width: 400\n    :include-source:\n\n    from cgp.examples.sigmoid import cgpstudy, plot_gpmap\n    gt, par, ph = cgpstudy()\n    plot_gpmap(gt, ph)\n\nThe gene regulatory model is a\n:class:`~cgp.sigmoidmodels.sigmoid_cvode.Sigmoidmodel`. It is a diploid model,\nin the sense that there is two differential equations per gene, one for each\nallele. This calls for a genotype-to-parameter map where the two alleles are\nmapped to two independent sets of parameter values. The function\n:func:`~cgp.gt.gt2par.geno2par_diploid` offers such genotype-to-parameter\nmapping with allele-specific parameters .\n\n:class:`~cgp.sigmoidmodels.sigmoid_cvode.Sigmoidmodel` encodes a system with\nthree genes and the parameter *adjmatrix* is used to specify connetivity and\nmode of regulation. The model in Gjuvsland et al. (2011) only has two genes, so\nwe focus only on gene 1 and 2, and make sure that gene 3 is not regulating any\nof them.\n\nFor a given parameter set the resulting phenotype is the equilibrium expression\nlevel of gene 2. In order to find the equilibrium we combine\n:class:`~cgp.sigmoidmodels.sigmoid_cvode.Sigmoidmodel` with\n:class:`~cgp.phenotyping.attractor.AttractorMixin`.\n\nReference:\n\n    * Gjuvsland AB, Vik JO, Wooliams JA, Omholt SW (2011)\n      `Order-preserving principles underlying genotype-phenotype maps ensure\n      high additive proportions of genetic variance <http://onlinelibrary.wiley.\n      com/doi/10.1111/j.1420-9101.2011.02358.x/full>`_ Journal of Evolutionary\n      Biology 24(10):2269-2279.\n'
import numpy as np, matplotlib.pyplot as plt
from cgp.utils.placevalue import Placevalue
from cgp.gt.gt2par import geno2par_diploid
from cgp.sigmoidmodels.sigmoid_cvode import Sigmoidmodel
from cgp.phenotyping.attractor import AttractorMixin
from cgp.utils.rec2dict import dict2rec

class Model(Sigmoidmodel, AttractorMixin):
    """
    Class that combines a sigmoid model with the ability to find equilibria.
    
    .. inheritance-diagram:: Model cgp.sigmoidmodels.sigmoid_cvode.Sigmoidmodel cgp.phenotyping.attractor.AttractorMixin
       :parts: 1
    """


model = Model(adjmatrix=np.array([[0, 0, 0], [1, 0, 0], [0, 0, 0]]))
names = [
 'Gene1', 'Gene2']
genotypes = Placevalue([3, 3], names=names, msd_first=False)
gt2par = geno2par_diploid
hetpar = model.p
hetpar.alpha1 = [182.04, 159.72]
hetpar.alpha2 = [190.58, 135.08]
hetpar.theta21 = [32.06, 20.86]
hetpar.p21 = [8.84, 7.91]
loc2par = np.zeros((2, 18))
loc2par[0, 0:6] = 1
loc2par[1, 6:12] = 1

def par2ph(par):
    """
    Phenotype: Equilibrium expression level of gene 2.
    
    This maps a parameter value to a phenotype value.
    """
    model._ReInit_if_required(y=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
    model.pr[:] = par
    _t, y = model.eq(tmax=100, tol=1e-06)
    return dict2rec(dict(Y2=y[2] + y[3]))


def cgpstudy():
    """
    Connecting the building blocks of a cGP study.
    
    This implements the simulation pipeline in Gjuvsland et al. (2011).
    """
    from numpy import concatenate as cat
    gt = np.array(genotypes)
    par = cat([ gt2par(list(g), hetpar, loc2par) for g in gt ])
    ph = cat([ par2ph(p) for p in par ])
    return (
     gt, par, ph)


def plot_gpmap(gt, ph):
    """Lineplot of genotypes and corresponding phenotypes."""
    plt.plot(gt['Gene1'][(gt['Gene2'] == 0)], ph[(gt['Gene2'] == 0)], 'ro-')
    plt.plot(gt['Gene1'][(gt['Gene2'] == 1)], ph[(gt['Gene2'] == 1)], 'go-')
    plt.plot(gt['Gene1'][(gt['Gene2'] == 2)], ph[(gt['Gene2'] == 2)], 'bo-')
    plt.xlabel('Genotype gene 1')
    plt.xticks(range(3), ('11', '12', '22'))
    plt.ylabel('Expression level gene 2')
    plt.legend(('11', '12', '22'), title='Genotype gene 2')
    plt.grid(b='on', axis='y')
    plt.show()


if __name__ == '__main__':
    gt, par, ph = cgpstudy()
    plot_gpmap(gt, ph)