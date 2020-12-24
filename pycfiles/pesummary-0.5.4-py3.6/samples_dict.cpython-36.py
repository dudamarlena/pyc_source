# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/utils/samples_dict.py
# Compiled at: 2020-05-08 05:31:08
# Size of source mod 2**32: 33714 bytes
import copy, numpy as np
from pesummary.utils.utils import resample_posterior_distribution, logger
from pesummary.core.plots.latex_labels import latex_labels
from pesummary.gw.plots.latex_labels import GWlatex_labels
import importlib
latex_labels.update(GWlatex_labels)

class SamplesDict(dict):
    __doc__ = 'Class to store the samples from a single run\n\n    Parameters\n    ----------\n    parameters: list\n        list of parameters\n    samples: nd list\n        list of samples for each parameter\n    autoscale: Bool, optional\n        If True, the posterior samples for each parameter are scaled to the\n        same length\n\n    Attributes\n    ----------\n    maxL: pesummary.utils.samples_dict.SamplesDict\n        SamplesDict object containing the maximum likelihood sample keyed by\n        the parameter\n    minimum: pesummary.utils.samples_dict.SamplesDict\n        SamplesDict object containing the minimum sample for each parameter\n    maximum: pesummary.utils.samples_dict.SamplesDict\n        SamplesDict object containing the maximum sample for each parameter\n    median: pesummary.utils.samples_dict.SamplesDict\n        SamplesDict object containining the median of each marginalized\n        posterior distribution\n    mean: pesummary.utils.samples_dict.SamplesDict\n        SamplesDict object containing the mean of each marginalized posterior\n        distribution\n    number_of_samples: int\n        Number of samples stored in the SamplesDict object\n    latex_labels: dict\n        Dictionary of latex labels for each parameter\n\n    Methods\n    -------\n    to_pandas:\n        Convert the SamplesDict object to a pandas DataFrame\n    to_structured_array:\n        Convert the SamplesDict object to a numpy structured array\n    pop:\n        Remove an entry from the SamplesDict object\n    downsample:\n        Downsample the samples stored in the SamplesDict object. See the\n        pesummary.utils.utils.resample_posterior_distribution method\n    discard_samples:\n        Remove the first N samples from each distribution\n    plot:\n        Generate a plot based on the posterior samples stored\n\n    Examples\n    --------\n    How the initialize the SamplesDict class\n\n    >>> from pesummary.utils.samples_dict import SamplesDict\n    >>> data = {\n    ...     "a": [1, 1.2, 1.7, 1.1, 1.4, 0.8, 1.6],\n    ...     "b": [10.2, 11.3, 11.6, 9.5, 8.6, 10.8, 10.9]\n    ... }\n    >>> dataset = SamplesDict(data)\n    >>> parameters = ["a", "b"]\n    >>> samples = [\n    ...     [1, 1.2, 1.7, 1.1, 1.4, 0.8, 1.6],\n    ...     [10.2, 11.3, 11.6, 9.5, 8.6, 10.8, 10.9]\n    ... }\n    >>> dataset = SamplesDict(parameters, samples)\n    >>> fig = dataset.plot("a", type="hist", bins=30)\n    >>> fig.show()\n    '

    def __init__(self, *args, logger_warn='warn', autoscale=True):
        super(SamplesDict, self).__init__()
        if len(args) == 1:
            if isinstance(args[0], dict):
                self.parameters = list(args[0].keys())
                self.samples = np.array([args[0][param] for param in self.parameters])
                for key, item in args[0].items():
                    self[key] = Array(item)

        else:
            self.parameters, self.samples = args
            lengths = [len(i) for i in self.samples]
            if len(np.unique(lengths)) > 1:
                if autoscale:
                    nsamples = np.min(lengths)
                    getattr(logger, logger_warn)('Unequal number of samples for each parameter. Restricting all posterior samples to have {} samples'.format(nsamples))
                    self.samples = [dataset[:nsamples] for dataset in self.samples]
            self.make_dictionary()
        self.latex_labels = {param:latex_labels[param] if param in latex_labels.keys() else param for param in self.parameters}

    def __getitem__(self, key):
        if isinstance(key, slice):
            return SamplesDict(self.parameters, [i[key.start:key.stop:key.step] for i in self.samples])
        else:
            if isinstance(key, str):
                if key not in self.keys():
                    raise KeyError('{} not in dictionary. The list of available keys are {}'.format(key, self.keys()))
            return super(SamplesDict, self).__getitem__(key)

    def __str__(self):
        """Print a summary of the information stored in the dictionary
        """

        def format_string(string, row):
            """Format a list into a table

            Parameters
            ----------
            string: str
                existing table
            row: list
                the row you wish to be written to a table
            """
            string += '{:<8}'.format(row[0])
            for i in range(1, len(row)):
                if isinstance(row[i], str):
                    string += '{:<15}'.format(row[i])
                else:
                    if isinstance(row[i], (float, int, np.int64, np.int32)):
                        string += '{:<15.6f}'.format(row[i])

            string += '\n'
            return string

        string = ''
        string = format_string(string, ['idx'] + list(self.keys()))
        if self.number_of_samples < 8:
            for i in range(self.number_of_samples):
                string = format_string(string, [i] + [item[i] for key, item in self.items()])

        else:
            for i in range(4):
                string = format_string(string, [i] + [item[i] for key, item in self.items()])

            for i in range(2):
                string = format_string(string, ['.'] * (len(self.keys()) + 1))

            for i in range(self.number_of_samples - 2, self.number_of_samples):
                string = format_string(string, [i] + [item[i] for key, item in self.items()])

        return string

    @property
    def maxL(self):
        return SamplesDict(self.parameters, [[item.maxL] for key, item in self.items()])

    @property
    def minimum(self):
        return SamplesDict(self.parameters, [[item.minimum] for key, item in self.items()])

    @property
    def maximum(self):
        return SamplesDict(self.parameters, [[item.maximum] for key, item in self.items()])

    @property
    def median(self):
        return SamplesDict(self.parameters, [[item.average(type='median')] for key, item in self.items()])

    @property
    def mean(self):
        return SamplesDict(self.parameters, [[item.average(type='mean')] for key, item in self.items()])

    @property
    def number_of_samples(self):
        return len(self[self.parameters[0]])

    def to_pandas(self):
        """Convert a SamplesDict object to a pandas dataframe
        """
        from pandas import DataFrame
        return DataFrame(self)

    def to_structured_array(self):
        """Convert a SamplesDict object to a structured numpy array
        """
        return self.to_pandas().to_records(index=False, column_dtypes=(np.float))

    def pop(self, parameter):
        if parameter not in self.parameters:
            logger.info('{} not in SamplesDict. Unable to remove {}'.format(parameter, parameter))
            return
        else:
            ind = self.parameters.index(parameter)
            self.parameters.remove(parameter)
            remove = self.samples[ind]
            samples = self.samples
            if isinstance(self.samples, np.ndarray):
                samples = self.samples.tolist()
                remove = self.samples[ind].tolist()
            samples.remove(remove)
            if isinstance(self.samples, np.ndarray):
                self.samples = np.array(samples)
            return super(SamplesDict, self).pop(parameter)

    def downsample(self, number):
        """Downsample the samples stored in the SamplesDict class

        Parameters
        ----------
        number: int
            Number of samples you wish to downsample to
        """
        self.samples = resample_posterior_distribution(self.samples, number)
        self.make_dictionary()
        return self

    def discard_samples(self, number):
        """Remove the first n samples

        Parameters
        ----------
        number: int
            Number of samples that you wish to remove
        """
        self.make_dictionary(discard_samples=number)
        return self

    def make_dictionary(self, discard_samples=None):
        """Add the parameters and samples to the class
        """
        if 'log_likelihood' in self.parameters:
            likelihoods = self.samples[self.parameters.index('log_likelihood')]
            likelihoods = likelihoods[discard_samples:]
        else:
            likelihoods = None
        if any(i in self.parameters for i in ('weights', 'weight')):
            ind = self.parameters.index('weights') if 'weights' in self.parameters else self.parameters.index('weight')
            weights = self.samples[ind][discard_samples:]
        else:
            weights = None
        for key, val in zip(self.parameters, self.samples):
            self[key] = Array((val[discard_samples:]),
              likelihood=likelihoods, weights=weights)

    def plot(self, *args, type='marginalized_posterior', **kwargs):
        """Generate a plot for the posterior samples stored in SamplesDict

        Parameters
        ----------
        *args: tuple
            all arguments are passed to the plotting function
        type: str
            name of the plot you wish to make
        **kwargs: dict
            all additional kwargs are passed to the plotting function
        """
        plotting_map = {'marginalized_posterior':self._marginalized_posterior, 
         'skymap':self._skymap, 
         'hist':self._marginalized_posterior}
        if type not in plotting_map.keys():
            raise NotImplementedError('The {} method is not currently implemented. The allowed plotting methods are {}'.format(type, ', '.join(plotting_map.keys())))
        return (plotting_map[type])(*args, **kwargs)

    def _marginalized_posterior(self, parameter, module='core', **kwargs):
        """Wrapper for the `pesummary.core.plots.plot._1d_histogram_plot` or
        `pesummary.gw.plots.plot._1d_histogram_plot`

        Parameters
        ----------
        parameter: str
            name of the parameter you wish to plot
        module: str, optional
            module you wish to use for the plotting
        **kwargs: dict
            all additional kwargs are passed to the `_1d_histogram_plot`
            function
        """
        module = importlib.import_module('pesummary.{}.plots.plot'.format(module))
        return (getattr(module, '_1d_histogram_plot'))(
         parameter, (self[parameter]), (self.latex_labels[parameter]), **kwargs)

    def _skymap(self, **kwargs):
        """Wrapper for the `pesummary.gw.plots.plot._ligo_skymap_plot`
        function

        Parameters
        ----------
        **kwargs: dict
            All kwargs are passed to the `_ligo_skymap_plot` function
        """
        from pesummary.gw.plots.plot import _ligo_skymap_plot
        if 'luminosity_distance' in self.keys():
            dist = self['luminosity_distance']
        else:
            dist = None
        return _ligo_skymap_plot(self['ra'], self['dec'], dist=dist, **kwargs)


class _MultiDimensionalSamplesDict(dict):
    __doc__ = "Class to store multiple SamplesDict objects\n\n    Parameters\n    ----------\n    parameters: list\n        list of parameters\n    samples: nd list\n        list of samples for each parameter for each chain\n    label_prefix: str, optional\n        prefix to use when distinguishing different analyses. The label is then\n        '{label_prefix}_{num}' where num is the result file index. Default\n        is 'dataset'\n    transpose: Bool, optional\n        True if the input is a transposed dictionary\n    labels: list, optional\n        the labels to use to distinguish different analyses. If provided\n        label_prefix is ignored\n\n    Attributes\n    ----------\n    T: pesummary.utils.samples_dict._MultiDimensionalSamplesDict\n        Transposed _MultiDimensionalSamplesDict object keyed by parameters\n        rather than label\n    combine: pesummary.utils.samples_dict.SamplesDict\n        Combine all samples from all analyses into a single SamplesDict object\n    nsamples: int\n        Total number of analyses stored in the _MultiDimensionalSamplesDict\n        object\n    number_of_samples: dict\n        Number of samples stored in the _MultiDimensionalSamplesDict for each\n        analysis\n    total_number_of_samples: int\n        Total number of samples stored across the multiple analyses\n    minimum_number_of_samples: int\n        The number of samples in the smallest analysis\n\n    Methods\n    -------\n    samples:\n        Return a list of samples stored in the _MultiDimensionalSamplesDict\n        object for a given parameter\n    "

    def __init__(self, *args, label_prefix='dataset', transpose=False, labels=None):
        if labels is not None:
            if len(np.unique(labels)) != len(labels):
                raise ValueError('Please provide a unique set of labels for each analysis')
        else:
            invalid_label_number_error = 'Please provide a label for each analysis'
            self.labels = labels
            self.name = _MultiDimensionalSamplesDict
            self.transpose = transpose
            if len(args) == 1 and isinstance(args[0], dict):
                if transpose:
                    parameters = list(args[0].keys())
                    _labels = list(args[0][parameters[0]].keys())
                    outer_iterator, inner_iterator = parameters, _labels
                else:
                    _labels = list(args[0].keys())
                    parameters = {label:list(args[0][label].keys()) for label in _labels}
                    outer_iterator, inner_iterator = _labels, parameters
                if labels is None:
                    self.labels = _labels
                for num, dataset in enumerate(outer_iterator):
                    if isinstance(inner_iterator, dict):
                        samples = np.array([args[0][dataset][param] for param in inner_iterator[dataset]])
                    else:
                        samples = np.array([args[0][dataset][param] for param in inner_iterator])
                    if transpose:
                        desc = parameters[num]
                        self[desc] = SamplesDict((self.labels),
                          samples, logger_warn='debug', autoscale=False)
                    else:
                        if self.labels is not None:
                            desc = self.labels[num]
                        else:
                            desc = '{}_{}'.format(label_prefix, num)
                        self[desc] = SamplesDict(parameters[self.labels[num]], samples)

            else:
                parameters, samples = args
                if labels is not None:
                    if len(labels) != len(samples):
                        raise ValueError(invalid_label_number_error)
                for num, dataset in enumerate(samples):
                    if labels is not None:
                        desc = labels[num]
                    else:
                        desc = '{}_{}'.format(label_prefix, num)
                    self[desc] = SamplesDict(parameters, dataset)

        if self.labels is None:
            self.labels = ['{}_{}'.format(label_prefix, num) for num, _ in enumerate(samples)]
        self.parameters = parameters

    @property
    def T(self):
        _params = sorted([param for param in self[self.labels[0]].keys()])
        if not all(sorted(self[label].keys()) == _params for label in self.labels):
            raise ValueError('Unable to transpose as not all samples have the same parameters')
        return self.name({param:{label:dataset[param] for label, dataset in self.items()} for param in self[self.labels[0]].keys()},
          transpose=True)

    @property
    def combine(self):
        if self.transpose:
            data = SamplesDict({param:np.concatenate([self[param][key] for key in self[param].keys()]) for param in self.parameters},
              logger_warn='debug')
        else:
            data = SamplesDict({param:np.concatenate([self[key][param] for key in self.keys()]) for param in self.parameters},
              logger_warn='debug')
        return data

    @property
    def nsamples(self):
        if self.transpose:
            parameters = list(self.keys())
            return len(self[parameters[0]])
        else:
            return len(self)

    @property
    def number_of_samples(self):
        if self.transpose:
            return {label:len(self[iterator][label]) for iterator, label in zip(self.keys(), self.labels)}
        else:
            return {label:self[iterator].number_of_samples for iterator, label in zip(self.keys(), self.labels)}

    @property
    def total_number_of_samples(self):
        return np.sum([length for length in self.number_of_samples.values()])

    @property
    def minimum_number_of_samples(self):
        return np.min([length for length in self.number_of_samples.values()])

    def samples(self, parameter):
        if self.transpose:
            samples = [self[parameter][label] for label in self.labels]
        else:
            samples = [self[label][parameter] for label in self.labels]
        return samples


class MCMCSamplesDict(_MultiDimensionalSamplesDict):
    __doc__ = 'Class to store the mcmc chains from a single run\n\n    Parameters\n    ----------\n    parameters: list\n        list of parameters\n    samples: nd list\n        list of samples for each parameter for each chain\n    transpose: Bool, optional\n        True if the input is a transposed dictionary\n\n    Attributes\n    ----------\n    T: pesummary.utils.samples_dict.MCMCSamplesDict\n        Transposed MCMCSamplesDict object keyed by parameters rather than\n        chain\n    average: pesummary.utils.samples_dict.SamplesDict\n        The mean of each sample across multiple chains. If the chains are of\n        different lengths, all chains are resized to the minimum number of\n        samples\n    combine: pesummary.utils.samples_dict.SamplesDict\n        Combine all samples from all chains into a single SamplesDict object\n    nchains: int\n        Total number of chains stored in the MCMCSamplesDict object\n    number_of_samples: dict\n        Number of samples stored in the MCMCSamplesDict for each chain\n    total_number_of_samples: int\n        Total number of samples stored across the multiple chains\n    minimum_number_of_samples: int\n        The number of samples in the smallest chain\n\n    Methods\n    -------\n    discard_samples:\n        Discard the first N samples for each chain\n    burnin:\n        Remove the first N samples as burnin. For different algorithms\n        see pesummary.core.file.mcmc.algorithms\n    gelman_rubin: float\n        Return the Gelman-Rubin statistic between the chains for a given\n        parameter. See pesummary.utils.utils.gelman_rubin\n    samples:\n        Return a list of samples stored in the MCMCSamplesDict object for a\n        given parameter\n\n    Examples\n    --------\n    Initializing the MCMCSamplesDict class\n\n    >>> from pesummary.utils.samplesdict import MCMCSamplesDict\n    >>> data = {\n    ...     "chain_0": {\n    ...         "a": [1, 1.2, 1.7, 1.1, 1.4, 0.8, 1.6],\n    ...         "b": [10.2, 11.3, 11.6, 9.5, 8.6, 10.8, 10.9]\n    ...     },\n    ...     "chain_1": {\n    ...         "a": [0.8, 0.5, 1.7, 1.4, 1.2, 1.7, 0.9],\n    ...         "b": [10, 10.5, 10.4, 9.6, 8.6, 11.6, 16.2]\n    ...     }\n    ... }\n    >>> dataset = MCMCSamplesDict(data)\n    >>> parameters = ["a", "b"]\n    >>> samples = [\n    ...     [\n    ...         [1, 1.2, 1.7, 1.1, 1.4, 0.8, 1.6],\n    ...         [10.2, 11.3, 11.6, 9.5, 8.6, 10.8, 10.9]\n    ...     ], [\n    ...         [0.8, 0.5, 1.7, 1.4, 1.2, 1.7, 0.9],\n    ...         [10, 10.5, 10.4, 9.6, 8.6, 11.6, 16.2]\n    ...     ]\n    ... ]\n    >>> dataset = MCMCSamplesDict(parameter, samples)\n    '

    def __init__(self, *args, transpose=False):
        single_chain_error = 'This class requires more than one mcmc chain to be passed. As only one dataset is available, please use the SamplesDict class.'
        (super(MCMCSamplesDict, self).__init__)(*args, transpose=transpose, label_prefix='chain')
        self.name = MCMCSamplesDict
        if len(self.labels) == 1:
            raise ValueError(single_chain_error)
        self.chains = self.labels
        self.nchains = self.nsamples

    @property
    def average(self):
        if self.transpose:
            data = SamplesDict({param:np.mean([self[param][key][:self.minimum_number_of_samples] for key in self[param].keys()],
              axis=0) for param in self.parameters},
              logger_warn='debug')
        else:
            data = SamplesDict({param:np.mean([self[key][param][:self.minimum_number_of_samples] for key in self.keys()],
              axis=0) for param in self.parameters},
              logger_warn='debug')
        return data

    def discard_samples(self, number):
        """Remove the first n samples

        Parameters
        ----------
        number: int/dict
            Number of samples that you wish to remove across all chains or a
            dictionary containing the number of samples to remove per chain
        """
        if isinstance(number, int):
            number = {chain:number for chain in self.keys()}
        for chain in self.keys():
            self[chain].discard_samples(number[chain])

        return self

    def burnin(self, *args, algorithm='burnin_by_step_number', **kwargs):
        """Remove the first N samples as burnin

        Parameters
        ----------
        algorithm: str, optional
            The algorithm you wish to use to remove samples as burnin. Default
            is 'burnin_by_step_number'. See
            `pesummary.core.file.mcmc.algorithms` for list of available
            algorithms
        """
        from pesummary.core.file import mcmc
        if algorithm not in mcmc.algorithms:
            raise ValueError('{} is not a valid algorithm for removing samples as burnin'.format(algorithm))
        arguments = [self] + [i for i in args]
        return (getattr(mcmc, algorithm))(*arguments, **kwargs)

    def gelman_rubin(self, parameter, decimal=5):
        """Return the gelman rubin statistic between chains for a given
        parameter

        Parameters
        ----------
        parameter: str
            name of the parameter you wish to return the gelman rubin statistic
            for
        decimal: int
            number of decimal places to keep when rounding
        """
        from pesummary.utils.utils import gelman_rubin as _gelman_rubin
        return _gelman_rubin((self.samples(parameter)), decimal=decimal)


class MultiAnalysisSamplesDict(_MultiDimensionalSamplesDict):
    __doc__ = 'Class to samples from multiple analyses\n\n    Parameters\n    ----------\n    parameters: list\n        list of parameters\n    samples: nd list\n        list of samples for each parameter for each chain\n    labels: list, optional\n        the labels to use to distinguish different analyses.\n    transpose: Bool, optional\n        True if the input is a transposed dictionary\n\n    Attributes\n    ----------\n    T: pesummary.utils.samples_dict.MultiAnalysisSamplesDict\n        Transposed MultiAnalysisSamplesDict object keyed by parameters\n        rather than label\n    combine: pesummary.utils.samples_dict.SamplesDict\n        Combine all samples from all analyses into a single SamplesDict object\n    nsamples: int\n        Total number of analyses stored in the MultiAnalysisSamplesDict\n        object\n    number_of_samples: dict\n        Number of samples stored in the MultiAnalysisSamplesDict for each\n        analysis\n    total_number_of_samples: int\n        Total number of samples stored across the multiple analyses\n    minimum_number_of_samples: int\n        The number of samples in the smallest analysis\n\n    Methods\n    -------\n    js_divergence: float\n        Return the JS divergence between two posterior distributions for a\n        given parameter. See pesummary.utils.utils.jension_shannon_divergence\n    ks_statistic: float\n        Return the KS statistic between two posterior distributions for a\n        given parameter. See pesummary.utils.utils.kolmogorov_smirnov_test\n    samples:\n        Return a list of samples stored in the MCMCSamplesDict object for a\n        given parameter\n    '

    def __init__(self, *args, labels=None, transpose=False):
        if labels is None:
            if not isinstance(args[0], dict):
                raise ValueError('Please provide a unique label for each analysis')
        (super(MultiAnalysisSamplesDict, self).__init__)(*args, labels=labels, transpose=transpose)
        self.name = MultiAnalysisSamplesDict

    def js_divergence(self, parameter, decimal=5):
        """Return the JS divergence between the posterior samples for
        a given parameter

        Parameters
        ----------
        parameter: str
            name of the parameter you wish to return the gelman rubin statistic
            for
        decimal: int
            number of decimal places to keep when rounding
        """
        from pesummary.utils.utils import jension_shannon_divergence
        return jension_shannon_divergence((self.samples(parameter)),
          decimal=decimal)

    def ks_statistic(self, parameter, decimal=5):
        """Return the KS statistic between the posterior samples for
        a given parameter

        Parameters
        ----------
        parameter: str
            name of the parameter you wish to return the gelman rubin statistic
            for
        decimal: int
            number of decimal places to keep when rounding
        """
        from pesummary.utils.utils import kolmogorov_smirnov_test
        return kolmogorov_smirnov_test((self.samples(parameter)),
          decimal=decimal)


class Array(np.ndarray):
    __doc__ = 'Class to add extra functions and methods to np.ndarray\n\n    Parameters\n    ----------\n    input_aray: list/array\n        input list/array\n\n    Attributes\n    ----------\n    median: float\n        median of the input array\n    mean: float\n        mean of the input array\n    '
    __slots__ = ['standard_deviation', 'minimum', 'maximum', 'maxL', 'weights']

    def __new__(cls, input_array, likelihood=None, weights=None):
        obj = np.asarray(input_array).view(cls)
        obj.standard_deviation = np.std(obj)
        obj.minimum = np.min(obj)
        obj.maximum = np.max(obj)
        obj.maxL = cls._maxL(obj, likelihood)
        obj.weights = weights
        return obj

    def __reduce__(self):
        pickled_state = super(Array, self).__reduce__()
        new_state = pickled_state[2] + tuple([getattr(self, i) for i in self.__slots__])
        return (
         pickled_state[0], pickled_state[1], new_state)

    def __setstate__(self, state):
        self.standard_deviation = state[(-5)]
        self.minimum = state[(-4)]
        self.maximum = state[(-3)]
        self.maxL = state[(-2)]
        self.weights = state[(-1)]
        super(Array, self).__setstate__(state[0:-5])

    def average(self, type='mean'):
        """Return the average of the array

        Parameters
        ----------
        type: str
            the method to average the array
        """
        if type == 'mean':
            return self._mean(self, weights=(self.weights))
        else:
            if type == 'median':
                return self._median(self, weights=(self.weights))
            return

    @staticmethod
    def _mean(array, weights=None):
        """Compute the mean from a set of weighted samples

        Parameters
        ----------
        array: np.ndarray
            input array
        weights: np.ndarray, optional
            list of weights associated with each sample
        """
        if weights is None:
            return np.mean(array)
        else:
            weights = np.array(weights).flatten() / float(sum(weights))
            return float(np.dot(np.array(array), weights))

    @staticmethod
    def _median(array, weights=None):
        """Compute the median from a set of weighted samples

        Parameters
        ----------
        array: np.ndarray
            input array
        weights: np.ndarray, optional
            list of weights associated with each sample
        """
        if weights is None:
            return np.median(array)
        else:
            return Array.percentile(array, weights=weights, percentile=0.5)

    @staticmethod
    def _maxL(array, likelihood=None):
        """Return the maximum likelihood value of the array

        Parameters
        ----------
        array: np.ndarray
            input array
        likelihood: np.ndarray, optional
            likelihoods associated with each sample
        """
        if likelihood is not None:
            likelihood = list(likelihood)
            ind = likelihood.index(np.max(likelihood))
            return array[ind]

    @staticmethod
    def percentile(array, weights=None, percentile=None):
        """Compute the Nth percentile of a set of weighted samples

        Parameters
        ----------
        array: np.ndarray
            input array
        weights: np.ndarray, optional
            list of weights associated with each sample
        percentile: float, list
            list of percentiles to compute
        """
        if weights is None:
            return np.percentile(array, percentile)
        else:
            array, weights = np.array(array), np.array(weights)
            percentile_type = percentile
            if not isinstance(percentile, (list, np.ndarray)):
                percentile = [
                 float(percentile)]
            percentile = np.array([float(i) for i in percentile])
            if not all(i < 1 for i in percentile):
                percentile *= 0.01
            ind_sorted = np.argsort(array)
            sorted_data = array[ind_sorted]
            sorted_weights = weights[ind_sorted]
            Sn = np.cumsum(sorted_weights)
            Pn = (Sn - 0.5 * sorted_weights) / Sn[(-1)]
            data = np.interp(percentile, Pn, sorted_data)
            if isinstance(percentile_type, (int, float, np.float64, np.float32)):
                return float(data[0])
            return data

    def confidence_interval(self, percentile=None):
        """Return the confidence interval of the array

        Parameters
        ----------
        percentile: int/list, optional
            Percentile or sequence of percentiles to compute, which must be
            between 0 and 100 inclusive
        """
        if percentile is not None:
            if isinstance(percentile, int):
                return self.percentile(self, self.weights, percentile)
            return np.array([self.percentile(self, self.weights, i) for i in percentile])
        else:
            return np.array([self.percentile(self, self.weights, i) for i in (5, 95)])

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.standard_deviation = getattr(obj, 'standard_deviation', None)
        self.minimum = getattr(obj, 'minimum', None)
        self.maximum = getattr(obj, 'maximum', None)
        self.maxL = getattr(obj, 'maxL', None)
        self.weights = getattr(obj, 'weights', None)