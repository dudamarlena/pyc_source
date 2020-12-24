# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/covar/breakpoint.py
# Compiled at: 2013-04-10 06:45:39
__doc__ = '\nSquared Exponential CF with breakpoint detection\n================================================\n\nDetects breakpoint T where two timeseries diverge.\n'
import scipy as SP, logging as LG
from scipy import special
from pygp.covar.covar_base import CovarianceFunction

class DivergeCF(CovarianceFunction):
    """
    Squared Exponential Covariance function, detecting breakpoint
    where two timeseries diverge.

    **Parameters:**
    
    replicate_indices : [int]

        The indices of the respective replicates, corresponding to
        the inputs. For instance: An input with three replicates:

        ===================== ========= ========= =========
        /                     rep1      rep2      rep3
        ===================== ========= ========= =========
        input = [             -1,0,1,2, -1,0,1,2, -1,0,1,2]
        replicate_indices = [ 0,0,0,0,  1,1,1,1,  2,2,2,2]
        ===================== ========= ========= =========

            
        Thus, the replicate indices represent
        which inputs correspond to which replicate.

    group_indices : [bool]

        Indices of group of each x. Thus this array depicts the
        group which each x belongs to. Only for two groups
        implemented yet!
        
    """

    def __init__(self, *args, **kw_args):
        super(DivergeCF, self).__init__(*args, **kw_args)
        self.n_hyperparameters = 2
        assert self.n_hyperparameters == 2, 'Not implemented yet for %i groups' % self.n_hyperparameters

    def get_hyperparameter_names(self):
        """
        return the names of hyperparameters to
        make identification easier
        """
        names = [
         'Breakpoint', 'Breakpoint Length-Scale']
        return names

    def get_number_of_parameters(self):
        """
        Return the number of hyperparameters this CF holds.
        """
        return self.n_hyperparameters

    def K(self, logtheta, x1, x2=None, k=10):
        r"""
        Get Covariance matrix K with given hyperparameter BP
        and inputs X=x1 and X\`*`=x2.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        x1_f, x2_f = self._filter_input_dimensions(x1, x2)
        BP = logtheta[0]
        L = logtheta[1]
        return -0.5 * special.erf(1.0 / L * SP.dot(x1_f, x2_f.T) - BP) + 0.5

    def Kgrad_theta(self, theta, x1, i):
        """
        The derivatives of the covariance matrix for
        each hyperparameter, respectively.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        return self.K(theta, x1)[i]

    def Kdiag(self, logtheta, x1):
        """
        Get diagonal of the (squared) covariance matrix.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        LG.debug('SEARDCF: Kdiag: Default unefficient implementation!')
        return self.K(logtheta, x1).diagonal()

    def Kgrad_x(self, logtheta, x, d):
        """
        The partial derivative of the covariance matrix with
        respect to x, given hyperparameters `logtheta`.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        L = SP.exp(logtheta[1:1 + self.get_n_dimensions()])
        dd = self._pointwise_distance(x, x, -L ** 2)
        return self.K(logtheta, x) * dd.transpose(2, 0, 1)

    def get_default_hyperparameters(self, x=None, y=None):
        """
        Return default parameters for a particular
        dataset (optional).
        """
        rv = SP.ones(self.n_hyperparameters)
        rv[-1] = 0.1
        if y is not None:
            rv[0] = (y.max() - y.min()) / 2
        if x is not None:
            rv[1:(-1)] = (x.max(axis=0) - x.min(axis=0)) / 4
        return SP.log(rv)

    def get_Iexp(self, logtheta):
        """
        Return indices of which hyperparameters are to be exponentiated
        for optimization. Here we do not want
        
        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        return [
         0]


def softmax(x, y):
    ma = max(x, y)
    mi = min(x, y)
    return ma + SP.log(1 + SP.exp(mi - ma))


def pointwise_softmax(x, y):
    return SP.array([ [ softmax(xi, yi) for xi in x ] for yi in y ])