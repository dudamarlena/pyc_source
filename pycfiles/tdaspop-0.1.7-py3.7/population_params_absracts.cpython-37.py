# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tdaspop/population_params_absracts.py
# Compiled at: 2019-04-30 16:41:20
# Size of source mod 2**32: 4744 bytes
from __future__ import absolute_import, print_function, division
__all__ = [
 'BaseRateDistributions', 'BasePopulation',
 'BaseSpatialPopulation']
from future.utils import with_metaclass
import abc, numpy as np
from collections import OrderedDict

class BasePopulation(with_metaclass(abc.ABCMeta, object)):
    __doc__ = '\n    The base class used describing the population of objects of interest. This\n    population is defined in terms of model parameters, and each object in the\n    population is specified by a unique index idx. The model parameters for an\n    object (ie. index) is obtained as a dictionary using the method modelparams.\n\n    \n    Attributes\n    ----------\n    paramsTable : `pd.DataFrame`\n        a dataframe with parameters of the model index by a set of index values.\n\n    .. note : this is a general enough class to deal with any population. \n    '

    @abc.abstractproperty
    def mjdmin(self):
        pass

    @abc.abstractproperty
    def mjdmax(self):
        pass

    @abc.abstractproperty
    def paramsTable(self):
        pass

    def modelParams(self, idx):
        """
        Ordered dictionary of model parameter names and parameters for the
        object with index `idx`. The model parameters should include sufficient
        information to return noise (sky/Poisson) free model fluxes.
        """
        return OrderedDict(self.paramsTable.loc[idx])

    @abc.abstractproperty
    def idxvalues(self):
        """
        sequence of index values 
        """
        pass

    @property
    def numSources(self):
        """
        integer number of sources 
        """
        return len(self.idxvalues)

    @abc.abstractproperty
    def rng_model(self):
        """
        instance of `np.random.RandomState`
        """
        pass


class BaseSpatialPopulation(with_metaclass(abc.ABCMeta, BasePopulation)):
    __doc__ = '\n    A population class that has positions associated with each object\n    '

    @abc.abstractmethod
    def positions(self, idx):
        pass

    @abc.abstractproperty
    def hasPositionArray(self):
        """
        bool which is true if a sequence exists
        """
        pass

    @abc.abstractproperty
    def positionArray(self):
        """
        Designed to be an array of idx, ra, dec (degrees)
        """
        pass


class BaseRateDistributions(with_metaclass(abc.ABCMeta, object)):
    __doc__ = '\n    Populations of objects occur with different abundances or rates at\n    different redshifts. This is a base class to describe the numbers of\n    objects at different redshifts, and provide samples of redshifts.\n    The redshifts should go upto a maximum redshift determined by the\n    values of interest for a particular survey. The number of objects\n    also depends on the cosmological volume, and usually depends on\n    the cosmology. Finally, the area of the sky is also encoded in\n    skyFraction.\n    '

    @abc.abstractproperty
    def randomState(self):
        """
        Instance of `np.random.RandomState` for the pseudo-number generators
        for reproducibility
        """
        pass

    @abc.abstractproperty
    def cosmology(self):
        """
        `~astropy.Cosmology` instance describing the cosmological model and
        the cosmological parameters used. For example, this could be used to
        evaluate the comoving volumes as a function of redshift.
        """
        pass

    @abc.abstractproperty
    def sky_fraction(self):
        """
        The sky fraction required for this. This is related to the `sky_area`.
        """
        pass

    abc.abstractproperty

    def sky_area(self):
        """ The area of the sky in sq degrees over which the sample is studies"""
        pass

    @abc.abstractproperty
    def z_sample_sizes(self):
        """
        Given a collection of edges of redshift bins, and a skyFraction
        return a collection of expected (possibly non-integral) numbers of
        TDO. Since this is an expected number, the number is a float and it is
        perfectly fine to get 3.45 TODs in a redshift bin.
        """
        pass

    @abc.abstractproperty
    def num_sources_realized(self):
        """ A Poisson realization of the number of sources in each redshift bin
        with expected values given by `z_sample_sizes`.
        """
        pass

    @abc.abstractproperty
    def z_samples(self):
        """
        Actual samples of redshift according to the distribution implied. The
        approximation applied is that the redshifts are uniformly sampled on
        each redhift bin, so they should be chosen to be narrow.
        """
        pass