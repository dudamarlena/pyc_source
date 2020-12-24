# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cbayes/sample.py
# Compiled at: 2018-08-09 17:21:53
# Size of source mod 2**32: 19609 bytes
"""
This module defines the data structure classes for ConsistentBayes. They are: 
    :class:`cbayes.sample.sample_set`
    :class:`cbayes.sample.problem_set`
"""
import numpy as np, logging, cbayes.distributions as distributions

def generate_sample_set_from_dict(U, num_samples=1, seed=None):
    """
     This module takes a nested dictionary (one inside another) 
     which contains the description of the distribution in that parameter
     and generates the samples described therein and generates a sample set.
     Descriptions of each parameter name are in `sample_set.dist.names`, which
     describes the keys in the outer dictionary, and `sample_set.dist.vars`, 
     which descirbes the inner layers (assumed to match). 
     :returns: samples ordered by columns, `sample_set.dist.params` contains the ordering as strings
     :returns: :class:`~np.array` 
    """
    unit_names = list(U.keys())
    try:
        assert len(np.unique([len(U[n].keys()) for n in unit_names])) == 1
    except AssertionError:
        print('Something is amiss in your dictionary. Perhaps extra or missing variables.')

    unit_variables = list(U[unit_names[0]].keys())
    dim = len(unit_variables) * len(unit_names)
    P = distributions.parametric_dist(dim)
    param_names = []
    di = 0
    for n in unit_names:
        for v in unit_variables:
            (P.set_dist)(dim=di, **U[n][v])
            param_names.append(v + '-' + n)
            di += 1

    P.names = unit_names
    P.vars = unit_variables
    P.params = param_names
    S = sample_set((num_samples, dim))
    S.dist = P
    S.generate_samples(seed=seed)
    return S


def generate_sample_dict(S):
    P = S.dist
    lam = S.samples
    V = {n:{v:None for v in P.vars} for n in P.names}
    for d in range(S.dim):
        p_info = P.params[d].rsplit('-')
        V[p_info[1]][p_info[0]] = lam[:, d]

    return V


def MSE_generator(model, observed_data, sigma=None):
    """
     Defines Mean Squared Error as quantity of interest. 
     uses `observed_data` with assumed N(0, sigma) noise model. 
    
    :param model: function to which input samples will be passed
    :type input_sample_set: :class:`~cbayes.sample_set` input samples
    :observed_data: data or observations you are trying to match
    :type observed_data: :ckass:`~np.array` with same shape as the output of `model`
    :param sigma: vector or constant assumed std. dev of `observed_data`
    :type sigma: :class:`~np.array` or :class:`float`
    """

    def QoI_fun(inputs):
        M = len(observed_data)
        predictions = model(inputs)
        if not predictions.shape[1] == M:
            raise AssertionError
        else:
            residuals = predictions - observed_data
            if sigma is not None:
                QoI = 1.0 / M * np.sum(((residuals / sigma) ** 2), axis=1)
            else:
                QoI = 1.0 / M * np.sum(((residuals / observed_data) ** 2), axis=1)
        return QoI

    return QoI_fun


def map_samples_and_create_problem(input_sample_set, QoI_fun):
    """
    TODO: full description, check type conformity
    
    :param input_sample_set:
    :type input_sample_set: :class:`~cbayes.sample_set` input samples
    """
    input_samples = input_sample_set.samples
    if input_samples is None:
        raise AttributeError(' `input_sample_set.samples` cannot be None.')
    output_samples = QoI_fun(input_samples)
    if len(output_samples.shape) == 1:
        output_samples = output_samples[:, np.newaxis]
    if output_samples.shape[0] != input_samples.shape[0]:
        logging.warn('Your model returns the wrong shape. Attempting transpose...')
        output_samples = output_samples.transpose()
    if output_samples.shape[0] != input_samples.shape[0]:
        raise AssertionError(' Model provided does not conform to shape requirements. Please return (n,d) `numpy.ndarray`.')
    output_sample_set = sample_set(size=(output_samples.shape))
    output_sample_set.samples = output_samples
    pset = problem_set(input_sample_set, output_sample_set)
    pset.model = QoI_fun
    return pset


class sample_set(object):

    def __init__(self, size=(None, None), seed=121):
        """

        Initialization
        
        :param size: Dimension of the space in which these samples reside.
        :type size: :class:`numpy.ndarray` of sample values of shape (num, dim)
        
        :param int seed: random number generator seed
        """
        if type(size) is tuple:
            self.num_samples = size[0]
            if len(size) == 1:
                self.dim = 1
            else:
                self.dim = size[1]
        else:
            if type(size) is int:
                self.dim = size
                self.num_samples = None
            else:
                logging.warning(' Please specify a valid size parameter. Defaulting to None.')
                self.dim = None
                self.num_samples = None
            if self.dim is not None:
                self.dist = distributions.parametric_dist(self.dim)
            else:
                self.dist = None
        self.samples = None
        self.seed = seed

    def set_dim(self, dimension=None):
        """
        TODO: Add this.
        """
        if self.dim is None:
            if dimension is not None:
                self.dim = int(abs(dimension))
            else:
                self.dim = 1
        else:
            if self.dim is not None:
                if dimension is not None:
                    self.dim = int(abs(dimension))
            else:
                assert TypeError('Please specify an integer-valued `dimension` greater than zero.')
        self.dist = distributions.parametric_dist(self.dim)

    def set_num_samples(self, num_samples=None):
        """
        TODO: Add this.
        """
        if self.num_samples is None:
            if num_samples is not None:
                self.num_samples = int(abs(num_samples))
            else:
                self.num_samples = 1000
        else:
            if self.num_samples is not None:
                if num_samples is not None:
                    self.num_samples = int(abs(num_samples))
            elif not TypeError('Please specify an integer-valued `num_samples` greater than zero.'):
                raise AssertionError

    def set_dist(self, dist='uniform', kwds=None, dim=None):
        """
        TODO: Add this.
        """
        distribution = dist
        if kwds is not None:
            if dim is not None:
                self.dist.set_dist(distribution, kwds, dim)
        if kwds is None and dim is not None:
            self.dist.set_dist(dist=distribution, dim=dim)
        elif kwds is None and distributions.supported_distributions(distribution) is 'chi2':
            raise AttributeError("If you are using a chi2 distribution, please pass `df` as a key-value pair in a dictionary. Ex: {'df': 20}.")
        elif kwds is None and distributions.supported_distributions(distribution) is 'beta':
            raise AttributeError("If you are using a Beta dist, please pass `a` and `b` as key-value pairs in a dictionary. Ex: {'a': 1, 'b': 1}")
        elif dim is None:
            logging.warn('INPUT: No dimension specified. You will be using `scipy.stats` for your distributions instead of the parametric object. Be warned that functions like `.pdf` may not work as expected.')
            if kwds is not None:
                self.dist = (distributions.assign_dist)(distribution, **kwds)
            else:
                self.dist = distributions.assign_dist(distribution)

    def setup(self):
        """
        TODO: Add this.
        """
        self.set_dim()
        self.set_num_samples()
        self.set_dist()

    def generate_samples(self, num_samples=None, seed=None, verbose=True):
        """
        TODO: Add this.
        """
        if self.dim is None:
            if verbose:
                print('Dimension unspecified. Assuming 1D')
            self.dim = 1
        else:
            if num_samples is not None:
                if verbose:
                    logging.warning('Number of samples declared, written to `sample_set.num_samples`.')
                self.num_samples = num_samples
            elif self.num_samples is None:
                if verbose:
                    logging.warning('Number of samples undeclared, choosing 1000 by default.')
                self.num_samples = 1000
        self.samples = self.dist.rvs(size=(self.num_samples, self.dim))
        return self.samples


class problem_set(object):
    __doc__ = '\n    TODO: Add this.\n    '

    def __init__(self, input_set=None, output_set=None, seed=None):
        self.input = input_set
        self.output = output_set
        self.model = None
        self.prior_dist = self.input.dist
        self.pushforward_dist = self.output.dist
        self.posterior_dist = None
        if self.output.dim is not None:
            self.observed_dist = distributions.parametric_dist(self.output.dim)
        else:
            self.observed_dist = None
        self.accept_inds = None
        self.ratio = None
        self.pf_pr_eval = None
        if seed is None:
            self.seed = 12112
        else:
            self.seed = seed

    def get_problem(self):
        """
        TODO: Add this.
        """
        if type(self.input.samples) is __main__.sample_set:
            print('Your input space is %d-dimensional' % self.input.dim)
            print('\t and is (%d, %d)' % self.input.samples.shape)
            if type(self.output.samples) is __main__.sample_set:
                print('Your output space is %d-dimensional' % self.output.dim)
                print('\t and is (%d, %d)' % self.output.samples.shape)
                if self.pushforward_dist is None:
                    print('WARNING: attribute `pushforward_dist` undefined. Necessary for `solve()`')
            else:
                if self.observed_dist is None:
                    print('WARNING: attribute `observed_dist` undefined. Necessary for `solve()`')
                if self.posterior_dist is None:
                    print('Posterior distribution is empty. Inverse Problem not yet solved.')
                else:
                    print('You have yet to specify an output set.                         Please do so (either manually or with the `problem_set.mapper` module)')
        else:
            print('You have yet to specify an input set.                     Please generate a `sample_set` object and pass it to                     `problem_set` when instantiating the class.')

    def compute_pushforward_dist(self, method='sc', mirror=False, kwds=None):
        """
        TODO: Add this.
        """
        self.pf_pr_eval = None
        if method in ('sklearn', 'sk', 'k', 'skl', 'scikit', 'sckitlearn'):
            if kwds is not None:
                self.output.dist = (distributions.skde)((self.output.samples), mirror, **kwds)
            else:
                self.output.dist = distributions.skde(self.output.samples, mirror)
        else:
            self.output.dist = distributions.gkde(self.output.samples)
        if mirror is True:
            print('Warning: You specified mirroring with the scipy gaussian kde. This is currently unsupported. Ignoring.')
        self.pushforward_dist = self.output.dist

    def set_observed_dist(self, dist=None, kwds=None, dim=None):
        """
        TODO: Add this.
        """
        if dist is not None:
            if kwds is not None:
                if dim is not None:
                    self.observed_dist.set_dist(dist, kwds, dim)
                elif kwds is None and dim is not None:
                    self.observed_dist.set_dist(dist, dim)
                else:
                    if kwds is None and distributions.supported_distributions(dist) is 'chi2':
                        raise AttributeError("If you are using a chi2 distribution, please pass `df` as a key-value pair in a dictionary. Ex: {'df': 20}.")
            else:
                if kwds is None and distributions.supported_distributions(dist) is 'beta':
                    raise AttributeError("If you are using a Beta dist, please pass `a` and `b` as key-value pairs in a dictionary. Ex: {'a': 1, 'b': 1}")
            if dim is None:
                logging.warn('OBS: No dimension specified. You will be using `scipy.stats` for your distributions instead of the parametric object. Be warned that functions like `.pdf` may not work as expected.')
                if kwds is not None:
                    self.observed_dist = (distributions.assign_dist)(dist, **kwds)
                else:
                    self.observed_dist = distributions.assign_dist(dist)
        else:
            logging.warn('No distribution specified. \n            Defaulting to normal around data_means with 0.5*data_standard_deviation')
            loc = np.mean((self.output.samples), axis=0)
            scale = 0.5 * np.std((self.output.samples), axis=0)
            self.observed_dist = (distributions.assign_dist)(*('normal', ), loc=loc, scale=scale)

    def eval_pf_prior(self):
        """
        TODO
        """
        if self.pushforward_dist is None:
            raise AttributeError('You are missing a defined pushforward distribution')
        else:
            pf = self.pushforward_dist.pdf(self.output.samples)
            self.pf_pr_eval = pf
        return pf

    def compute_ratio(self, samples):
        """
        Evaluates the ratio at a given set of samples 
        These samples should be the outputs of your map.
        
        :param sample_set: 
        :type sample_set: :class:`~/cbayes.sample.sample_set`
        
        :rtype: :class:`numpy.ndarray` of shape(num,)
        :returns: ratio of observed to pushforward density evaluations
        """
        n = samples.shape[0]
        try:
            obs = self.observed_dist.pdf(samples).prod(axis=1).reshape(n)
        except ValueError:
            obs = self.observed_dist.pdf(samples).reshape(n)

        if len(samples) == len(self.output.samples):
            if np.allclose(samples.ravel(), self.output.samples.ravel()):
                if self.pf_pr_eval is not None:
                    logging.warn('Detected stored evaluation. Reusing.')
                    pf = self.pf_pr_eval
                else:
                    pf = self.eval_pf_prior()
            else:
                pf = self.pushforward_dist.pdf(samples).reshape(n)
        else:
            pf = self.pushforward_dist.pdf(samples).reshape(n)
        ratio = np.divide(obs, pf)
        ratio = ratio.ravel()
        return ratio

    def set_ratio(self):
        """
        TODO: rewrite description
        Runs compute_ratio and stores value in place.
        """
        data = self.output.samples
        ratio = self.compute_ratio(data)
        self.ratio = ratio

    def evaluate_posterior(self, samples):
        """
        TODO: rewrite description
        Evaluates but does not store an evaluation of the posterior.
        """
        return self.input.dist.pdf(samples) * self.compute_ratio(self.model(samples))


def save_sample_set():
    """
    TODO: Add this.
    """
    pass


def save_sample_set():
    """
    TODO: Add this.
    """
    pass


def save_problem_set():
    """
    TODO: Add this.
    """
    pass


def save_problem_set():
    """
    TODO: Add this.
    """
    pass