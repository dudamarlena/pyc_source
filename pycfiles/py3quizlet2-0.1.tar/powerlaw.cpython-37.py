# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/statistics/powerlaw.py
# Compiled at: 2019-12-03 00:25:58
# Size of source mod 2**32: 106333 bytes
from __future__ import print_function
import sys
__version__ = '1.4.1'

class Fit(object):
    """Fit"""

    def __init__(self, data, discrete=False, xmin=None, xmax=None, fit_method='Likelihood', estimate_discrete=True, discrete_approximation='round', sigma_threshold=None, parameter_range=None, fit_optimizer=None, xmin_distance='D', **kwargs):
        self.data_original = data
        from numpy import asarray
        self.data = asarray((self.data_original), dtype='float')
        self.discrete = discrete
        self.fit_method = fit_method
        self.estimate_discrete = estimate_discrete
        self.discrete_approximation = discrete_approximation
        self.sigma_threshold = sigma_threshold
        self.parameter_range = parameter_range
        self.given_xmin = xmin
        self.given_xmax = xmax
        self.xmin = self.given_xmin
        self.xmax = self.given_xmax
        self.xmin_distance = xmin_distance
        if 0 in self.data:
            print('Values less than or equal to 0 in data. Throwing out 0 or negative values', file=(sys.stderr))
            self.data = self.data[(self.data > 0)]
        elif self.xmax:
            self.xmax = float(self.xmax)
            self.fixed_xmax = True
            n_above_max = sum(self.data > self.xmax)
            self.data = self.data[(self.data <= self.xmax)]
        else:
            n_above_max = 0
            self.fixed_xmax = False
        if not all((self.data[i] <= self.data[(i + 1)] for i in range(len(self.data) - 1))):
            from numpy import sort
            self.data = sort(self.data)
        self.fitting_cdf_bins, self.fitting_cdf = cdf((self.data), xmin=None, xmax=(self.xmax))
        if xmin and type(xmin) != tuple and type(xmin) != list:
            self.fixed_xmin = True
            self.xmin = float(xmin)
            self.noise_flag = None
            pl = Power_Law(xmin=(self.xmin), xmax=(self.xmax),
              discrete=(self.discrete),
              fit_method=(self.fit_method),
              estimate_discrete=(self.estimate_discrete),
              data=(self.data),
              parameter_range=(self.parameter_range))
            setattr(self, self.xmin_distance, getattr(pl, self.xmin_distance))
            self.alpha = pl.alpha
            self.sigma = pl.sigma
        else:
            self.fixed_xmin = False
            self.find_xmin()
        self.data = self.data[(self.data >= self.xmin)]
        self.n = float(len(self.data))
        self.n_tail = self.n + n_above_max
        self.supported_distributions = {'power_law':Power_Law, 
         'lognormal':Lognormal, 
         'exponential':Exponential, 
         'truncated_power_law':Truncated_Power_Law, 
         'stretched_exponential':Stretched_Exponential, 
         'lognormal_positive':Lognormal_Positive}

    def __getattr__(self, name):
        if name in self.supported_distributions.keys():
            dist = self.supported_distributions[name]
            if dist == Power_Law:
                parameter_range = self.parameter_range
            else:
                parameter_range = None
            setattr(self, name, dist(data=(self.data), xmin=(self.xmin),
              xmax=(self.xmax),
              discrete=(self.discrete),
              fit_method=(self.fit_method),
              estimate_discrete=(self.estimate_discrete),
              discrete_approximation=(self.discrete_approximation),
              parameter_range=parameter_range,
              parent_Fit=self))
            return getattr(self, name)
        raise AttributeError(name)

    def find_xmin(self, xmin_distance=None):
        """
        Returns the optimal xmin beyond which the scaling regime of the power
        law fits best. The attribute self.xmin of the Fit object is also set.

        The optimal xmin beyond which the scaling regime of the power law fits
        best is identified by minimizing the Kolmogorov-Smirnov distance
        between the data and the theoretical power law fit.
        This is the method of Clauset et al. 2007.
        """
        from numpy import unique, asarray, argmin
        if not self.given_xmin:
            possible_xmins = self.data
        else:
            possible_ind = min(self.given_xmin) <= self.data
            possible_ind *= self.data <= max(self.given_xmin)
            possible_xmins = self.data[possible_ind]
        xmins, xmin_indices = unique(possible_xmins, return_index=True)
        xmins = xmins[:-1]
        xmin_indices = xmin_indices[:-1]
        if xmin_distance is None:
            xmin_distance = self.xmin_distance
        if len(xmins) <= 0:
            print('Less than 2 unique data values left after xmin and xmax options! Cannot fit. Returning nans.', file=(sys.stderr))
            from numpy import nan, array
            self.xmin = nan
            self.D = nan
            self.V = nan
            self.Asquare = nan
            self.Kappa = nan
            self.alpha = nan
            self.sigma = nan
            self.n_tail = nan
            setattr(self, xmin_distance + 's', array([nan]))
            self.alphas = array([nan])
            self.sigmas = array([nan])
            self.in_ranges = array([nan])
            self.xmins = array([nan])
            self.noise_flag = True
            return self.xmin

        def fit_function(xmin):
            pl = Power_Law(xmin=xmin, xmax=(self.xmax),
              discrete=(self.discrete),
              estimate_discrete=(self.estimate_discrete),
              fit_method=(self.fit_method),
              data=(self.data),
              parameter_range=(self.parameter_range),
              parent_Fit=self)
            return (
             getattr(pl, xmin_distance), pl.alpha, pl.sigma, pl.in_range())

        fits = asarray(list(map(fit_function, xmins)))
        setattr(self, xmin_distance + 's', fits[:, 0])
        self.alphas = fits[:, 1]
        self.sigmas = fits[:, 2]
        self.in_ranges = fits[:, 3].astype(bool)
        self.xmins = xmins
        good_values = self.in_ranges
        if self.sigma_threshold:
            good_values = good_values * (self.sigmas < self.sigma_threshold)
        if good_values.all():
            min_D_index = argmin(getattr(self, xmin_distance + 's'))
            self.noise_flag = False
        elif not good_values.any():
            min_D_index = argmin(getattr(self, xmin_distance + 's'))
            self.noise_flag = True
        else:
            from numpy.ma import masked_array
            masked_Ds = masked_array((getattr(self, xmin_distance + 's')), mask=(-good_values))
            min_D_index = masked_Ds.argmin()
            self.noise_flag = False
        if self.noise_flag:
            print('No valid fits found.', file=(sys.stderr))
        self.xmin = xmins[min_D_index]
        setattr(self, xmin_distance, getattr(self, xmin_distance + 's')[min_D_index])
        self.alpha = self.alphas[min_D_index]
        self.sigma = self.sigmas[min_D_index]
        self.fitting_cdf_bins, self.fitting_cdf = self.cdf()
        return self.xmin

    def nested_distribution_compare(self, dist1, dist2, nested=True, **kwargs):
        """
        Returns the loglikelihood ratio, and its p-value, between the two
        distribution fits, assuming the candidate distributions are nested.

        Parameters
        ----------
        dist1 : string
            Name of the first candidate distribution (ex. 'power_law')
        dist2 : string
            Name of the second candidate distribution (ex. 'exponential')
        nested : bool or None, optional
            Whether to assume the candidate distributions are nested versions
            of each other. None assumes not unless the name of one distribution
            is a substring of the other. True by default.

        Returns
        -------
        R : float
            Loglikelihood ratio of the two distributions' fit to the data. If
            greater than 0, the first distribution is preferred. If less than
            0, the second distribution is preferred.
        p : float
            Significance of R
        """
        return (self.distribution_compare)(dist1, dist2, nested=nested, **kwargs)

    def distribution_compare(self, dist1, dist2, nested=None, **kwargs):
        """
        Returns the loglikelihood ratio, and its p-value, between the two
        distribution fits, assuming the candidate distributions are nested.

        Parameters
        ----------
        dist1 : string
            Name of the first candidate distribution (ex. 'power_law')
        dist2 : string
            Name of the second candidate distribution (ex. 'exponential')
        nested : bool or None, optional
            Whether to assume the candidate distributions are nested versions
            of each other. None assumes not unless the name of one distribution
            is a substring of the other.

        Returns
        -------
        R : float
            Loglikelihood ratio of the two distributions' fit to the data. If
            greater than 0, the first distribution is preferred. If less than
            0, the second distribution is preferred.
        p : float
            Significance of R
        """
        if (dist1 in dist2 or dist2) in dist1:
            if nested is None:
                print('Assuming nested distributions', file=(sys.stderr))
                nested = True
        dist1 = getattr(self, dist1)
        dist2 = getattr(self, dist2)
        loglikelihoods1 = dist1.loglikelihoods(self.data)
        loglikelihoods2 = dist2.loglikelihoods(self.data)
        return loglikelihood_ratio(
 loglikelihoods1, loglikelihoods2, nested=nested, **kwargs)

    def loglikelihood_ratio(self, dist1, dist2, nested=None, **kwargs):
        """
        Another name for distribution_compare.
        """
        return (self.distribution_compare)(dist1, dist2, nested=nested, **kwargs)

    def cdf(self, original_data=False, survival=False, **kwargs):
        """
        Returns the cumulative distribution function of the data.

        Parameters
        ----------
        original_data : bool, optional
            Whether to use all of the data initially passed to the Fit object.
            If False, uses only the data used for the fit (within xmin and
            xmax.)
        survival : bool, optional
            Whether to return the complementary cumulative distribution
            function, 1-CDF, also known as the survival function.

        Returns
        -------
        X : array
            The sorted, unique values in the data.
        probabilities : array
            The portion of the data that is less than or equal to X.
        """
        if original_data:
            data = self.data_original
            xmin = None
            xmax = None
        else:
            data = self.data
            xmin = self.xmin
            xmax = self.xmax
        return cdf(data, xmin=xmin, xmax=xmax, survival=survival, **kwargs)

    def ccdf(self, original_data=False, survival=True, **kwargs):
        """
        Returns the complementary cumulative distribution function of the data.

        Parameters
        ----------
        original_data : bool, optional
            Whether to use all of the data initially passed to the Fit object.
            If False, uses only the data used for the fit (within xmin and
            xmax.)
        survival : bool, optional
            Whether to return the complementary cumulative distribution
            function, also known as the survival function, or the cumulative
            distribution function, 1-CCDF.

        Returns
        -------
        X : array
            The sorted, unique values in the data.
        probabilities : array
            The portion of the data that is greater than or equal to X.
        """
        if original_data:
            data = self.data_original
            xmin = None
            xmax = None
        else:
            data = self.data
            xmin = self.xmin
            xmax = self.xmax
        return cdf(data, xmin=xmin, xmax=xmax, survival=survival, **kwargs)

    def pdf(self, original_data=False, **kwargs):
        """
        Returns the probability density function (normalized histogram) of the
        data.

        Parameters
        ----------
        original_data : bool, optional
            Whether to use all of the data initially passed to the Fit object.
            If False, uses only the data used for the fit (within xmin and
            xmax.)

        Returns
        -------
        bin_edges : array
            The edges of the bins of the probability density function.
        probabilities : array
            The portion of the data that is within the bin. Length 1 less than
            bin_edges, as it corresponds to the spaces between them.
        """
        if original_data:
            data = self.data_original
            xmin = None
            xmax = None
        else:
            data = self.data
            xmin = self.xmin
            xmax = self.xmax
        edges, hist = pdf(data, xmin=xmin, xmax=xmax, **kwargs)
        return (
         edges, hist)

    def plot_cdf(self, ax=None, original_data=False, survival=False, **kwargs):
        """
        Plots the CDF to a new figure or to axis ax if provided.

        Parameters
        ----------
        ax : matplotlib axis, optional
            The axis to which to plot. If None, a new figure is created.
        original_data : bool, optional
            Whether to use all of the data initially passed to the Fit object.
            If False, uses only the data used for the fit (within xmin and
            xmax.)
        survival : bool, optional
            Whether to plot a CDF (False) or CCDF (True). False by default.

        Returns
        -------
        ax : matplotlib axis
            The axis to which the plot was made.
        """
        if original_data:
            data = self.data_original
        else:
            data = self.data
        return plot_cdf(data, ax=ax, survival=survival, **kwargs)

    def plot_ccdf(self, ax=None, original_data=False, survival=True, **kwargs):
        """
        Plots the CCDF to a new figure or to axis ax if provided.

        Parameters
        ----------
        ax : matplotlib axis, optional
            The axis to which to plot. If None, a new figure is created.
        original_data : bool, optional
            Whether to use all of the data initially passed to the Fit object.
            If False, uses only the data used for the fit (within xmin and
            xmax.)
        survival : bool, optional
            Whether to plot a CDF (False) or CCDF (True). True by default.

        Returns
        -------
        ax : matplotlib axis
            The axis to which the plot was made.
        """
        if original_data:
            data = self.data_original
        else:
            data = self.data
        return plot_cdf(data, ax=ax, survival=survival, **kwargs)

    def plot_pdf(self, ax=None, original_data=False, linear_bins=False, **kwargs):
        """
        Plots the probability density function (PDF) or the data to a new figure
        or to axis ax if provided.

        Parameters
        ----------
        ax : matplotlib axis, optional
            The axis to which to plot. If None, a new figure is created.
        original_data : bool, optional
            Whether to use all of the data initially passed to the Fit object.
            If False, uses only the data used for the fit (within xmin and
            xmax.)
        linear_bins : bool, optional
            Whether to use linearly spaced bins (True) or logarithmically
            spaced bins (False). False by default.

        Returns
        -------
        ax : matplotlib axis
            The axis to which the plot was made.
        """
        if original_data:
            data = self.data_original
        else:
            data = self.data
        return plot_pdf(data, ax=ax, linear_bins=linear_bins, **kwargs)


class Distribution(object):
    """Distribution"""

    def __init__(self, xmin=1, xmax=None, discrete=False, fit_method='Likelihood', data=None, parameters=None, parameter_range=None, initial_parameters=None, discrete_approximation='round', parent_Fit=None, **kwargs):
        self.xmin = xmin
        self.xmax = xmax
        self.discrete = discrete
        self.fit_method = fit_method
        self.discrete_approximation = discrete_approximation
        self.parameter1 = None
        self.parameter2 = None
        self.parameter3 = None
        self.parameter1_name = None
        self.parameter2_name = None
        self.parameter3_name = None
        if parent_Fit:
            self.parent_Fit = parent_Fit
        if parameters is not None:
            self.parameters(parameters)
        if parameter_range:
            self.parameter_range(parameter_range)
        if initial_parameters:
            self._given_initial_parameters(initial_parameters)
        if data is not None:
            parameter_range and self.parent_Fit or 

    def fit(self, data=None, suppress_output=False):
        """
        Fits the parameters of the distribution to the data. Uses options set
        at initialization.
        """
        if data is None:
            if hasattr(self, 'parent_Fit'):
                data = self.parent_Fit.data
        else:
            data = trim_to_range(data, xmin=(self.xmin), xmax=(self.xmax))
            if self.fit_method == 'Likelihood':

                def fit_function(params):
                    self.parameters(params)
                    return -sum(self.loglikelihoods(data))

            elif self.fit_method == 'KS':

                def fit_function(params):
                    self.parameters(params)
                    self.KS(data)
                    return self.D

            from scipy.optimize import fmin
            parameters, negative_loglikelihood, iter, funcalls, warnflag = fmin((lambda params: fit_function(params)),
              (self.initial_parameters(data)),
              full_output=1,
              disp=False)
            self.parameters(parameters)
            if not self.in_range():
                self.noise_flag = True
            else:
                self.noise_flag = False
        if self.noise_flag:
            if not suppress_output:
                print('No valid fits found.', file=(sys.stderr))
        self.loglikelihood = -negative_loglikelihood
        self.KS(data)

    def KS(self, data=None):
        """
        Returns the Kolmogorov-Smirnov distance D between the distribution and
        the data. Also sets the properties D+, D-, V (the Kuiper testing
        statistic), and Kappa (1 + the average difference between the
        theoretical and empirical distributions).

        Parameters
        ----------
        data : list or array, optional
            If not provided, attempts to use the data from the Fit object in
            which the Distribution object is contained.
        """
        if data is None:
            if hasattr(self, 'parent_Fit'):
                data = self.parent_Fit.data
        else:
            data = trim_to_range(data, xmin=(self.xmin), xmax=(self.xmax))
            if len(data) < 2:
                print('Not enough data. Returning nan', file=(sys.stderr))
                from numpy import nan
                self.D = nan
                self.D_plus = nan
                self.D_minus = nan
                self.Kappa = nan
                self.V = nan
                self.Asquare = nan
                return self.D
                if hasattr(self, 'parent_Fit'):
                    bins = self.parent_Fit.fitting_cdf_bins
                    Actual_CDF = self.parent_Fit.fitting_cdf
                    ind = bins >= self.xmin
                    bins = bins[ind]
                    Actual_CDF = Actual_CDF[ind]
                    dropped_probability = Actual_CDF[0]
                    Actual_CDF -= dropped_probability
                    Actual_CDF /= 1 - dropped_probability
            else:
                bins, Actual_CDF = cdf(data)
        Theoretical_CDF = self.cdf(bins)
        CDF_diff = Theoretical_CDF - Actual_CDF
        self.D_plus = CDF_diff.max()
        self.D_minus = -1.0 * CDF_diff.min()
        from numpy import mean
        self.Kappa = 1 + mean(CDF_diff)
        self.V = self.D_plus + self.D_minus
        self.D = max(self.D_plus, self.D_minus)
        denom = Theoretical_CDF * (1 - Theoretical_CDF)
        denom += 1e-09
        self.Asquare = sum((CDF_diff ** 2 / denom)[1:])
        return self.D

    def ccdf(self, data=None, survival=True):
        """
        The complementary cumulative distribution function (CCDF) of the
        theoretical distribution. Calculated for the values given in data
        within xmin and xmax, if present.

        Parameters
        ----------
        data : list or array, optional
            If not provided, attempts to use the data from the Fit object in
            which the Distribution object is contained.
        survival : bool, optional
            Whether to calculate a CDF (False) or CCDF (True).
            True by default.

        Returns
        -------
        X : array
            The sorted, unique values in the data.
        probabilities : array
            The portion of the data that is less than or equal to X.
        """
        return self.cdf(data=data, survival=survival)

    def cdf(self, data=None, survival=False):
        """
        The cumulative distribution function (CDF) of the theoretical
        distribution. Calculated for the values given in data within xmin and
        xmax, if present.

        Parameters
        ----------
        data : list or array, optional
            If not provided, attempts to use the data from the Fit object in
            which the Distribution object is contained.
        survival : bool, optional
            Whether to calculate a CDF (False) or CCDF (True).
            False by default.

        Returns
        -------
        X : array
            The sorted, unique values in the data.
        probabilities : array
            The portion of the data that is less than or equal to X.
        """
        if data is None:
            if hasattr(self, 'parent_Fit'):
                data = self.parent_Fit.data
        data = trim_to_range(data, xmin=(self.xmin), xmax=(self.xmax))
        n = len(data)
        from sys import float_info
        if not self.in_range():
            from numpy import tile
            return tile(10 ** float_info.min_10_exp, n)
        if self._cdf_xmin == 1:
            from numpy import ones
            CDF = ones(n)
            return CDF
        CDF = self._cdf_base_function(data) - self._cdf_xmin
        norm = 1 - self._cdf_xmin
        if self.xmax:
            norm = norm - (1 - self._cdf_base_function(self.xmax))
        CDF = CDF / norm
        if survival:
            CDF = 1 - CDF
        possible_numerical_error = False
        from numpy import isnan, min
        if isnan(min(CDF)):
            print("'nan' in fit cumulative distribution values.", file=(sys.stderr))
            possible_numerical_error = True
        if possible_numerical_error:
            print('Likely underflow or overflow error: the optimal fit for this distribution gives values that are so extreme that we lack the numerical precision to calculate them.', file=(sys.stderr))
        return CDF

    @property
    def _cdf_xmin(self):
        return self._cdf_base_function(self.xmin)

    def pdf(self, data=None):
        """
        Returns the probability density function (normalized histogram) of the
        theoretical distribution for the values in data within xmin and xmax,
        if present.

        Parameters
        ----------
        data : list or array, optional
            If not provided, attempts to use the data from the Fit object in
            which the Distribution object is contained.

        Returns
        -------
        probabilities : array
        """
        if data is None:
            if hasattr(self, 'parent_Fit'):
                data = self.parent_Fit.data
        else:
            data = trim_to_range(data, xmin=(self.xmin), xmax=(self.xmax))
            n = len(data)
            from sys import float_info
            if not self.in_range():
                from numpy import tile
                return tile(10 ** float_info.min_10_exp, n)
            if not self.discrete:
                f = self._pdf_base_function(data)
                C = self._pdf_continuous_normalizer
                likelihoods = f * C
            elif self._pdf_discrete_normalizer:
                f = self._pdf_base_function(data)
                C = self._pdf_discrete_normalizer
                likelihoods = f * C
            elif self.discrete_approximation == 'round':
                lower_data = data - 0.5
                upper_data = data + 0.5
                self.xmin -= 0.5
                if self.xmax:
                    self.xmax += 0.5
                likelihoods = self.cdf(upper_data) - self.cdf(lower_data)
                self.xmin += 0.5
                if self.xmax:
                    self.xmax -= 0.5
            else:
                if self.discrete_approximation == 'xmax':
                    upper_limit = self.xmax
                else:
                    upper_limit = self.discrete_approximation
                from numpy import arange
                X = arange(self.xmin, upper_limit + 1)
                PDF = self._pdf_base_function(X)
                PDF = (PDF / sum(PDF)).astype(float)
                likelihoods = PDF[(data - self.xmin).astype(int)]
        likelihoods[likelihoods == 0] = 10 ** float_info.min_10_exp
        return likelihoods

    @property
    def _pdf_continuous_normalizer(self):
        C = 1 - self._cdf_xmin
        if self.xmax:
            C -= 1 - self._cdf_base_function(self.xmax + 1)
        C = 1.0 / C
        return C

    @property
    def _pdf_discrete_normalizer(self):
        return False

    def parameter_range(self, r, initial_parameters=None):
        """
        Set the limits on the range of valid parameters to be considered while
        fitting.

        Parameters
        ----------
        r : dict
            A dictionary of the parameter range. Restricted parameter 
            names are keys, and with tuples of the form (lower_bound,
            upper_bound) as values.
        initial_parameters : tuple or list, optional
            Initial parameter values to start the fitting search from.
        """
        from types import FunctionType
        if type(r) == FunctionType:
            self._in_given_parameter_range = r
        else:
            self._range_dict = r
        if initial_parameters:
            self._given_initial_parameters = initial_parameters
        if self.parent_Fit:
            self.fit(self.parent_Fit.data)

    def in_range(self):
        """
        Whether the current parameters of the distribution are within the range
        of valid parameters.
        """
        try:
            r = self._range_dict
            result = True
            for k in r.keys():
                lower_bound, upper_bound = r[k]
                if upper_bound is not None:
                    result *= getattr(self, k) < upper_bound
                if lower_bound is not None:
                    result *= getattr(self, k) > lower_bound

            return result
        except AttributeError:
            try:
                in_range = self._in_given_parameter_range(self)
            except AttributeError:
                in_range = self._in_standard_parameter_range()

        return bool(in_range)

    def initial_parameters(self, data):
        """
        Return previously user-provided initial parameters or, if never
        provided,  calculate new ones. Default initial parameter estimates are
        unique to each theoretical distribution.
        """
        try:
            return self._given_initial_parameters
        except AttributeError:
            return self._initial_parameters(data)

    def likelihoods(self, data):
        """
        The likelihoods of the observed data from the theoretical distribution.
        Another name for the probabilities or probability density function.
        """
        return self.pdf(data)

    def loglikelihoods(self, data):
        """
        The logarithm of the likelihoods of the observed data from the
        theoretical distribution.
        """
        from numpy import log
        return log(self.likelihoods(data))

    def plot_ccdf(self, data=None, ax=None, survival=True, **kwargs):
        """
        Plots the complementary cumulative distribution function (CDF) of the
        theoretical distribution for the values given in data within xmin and
        xmax, if present. Plots to a new figure or to axis ax if provided.

        Parameters
        ----------
        data : list or array, optional
            If not provided, attempts to use the data from the Fit object in
            which the Distribution object is contained.
        ax : matplotlib axis, optional
            The axis to which to plot. If None, a new figure is created.
        survival : bool, optional
            Whether to plot a CDF (False) or CCDF (True). True by default.

        Returns
        -------
        ax : matplotlib axis
            The axis to which the plot was made.
        """
        return (self.plot_cdf)(data, ax=ax, survival=survival, **kwargs)

    def plot_cdf(self, data=None, ax=None, survival=False, **kwargs):
        """
        Plots the cumulative distribution function (CDF) of the
        theoretical distribution for the values given in data within xmin and
        xmax, if present. Plots to a new figure or to axis ax if provided.

        Parameters
        ----------
        data : list or array, optional
            If not provided, attempts to use the data from the Fit object in
            which the Distribution object is contained.
        ax : matplotlib axis, optional
            The axis to which to plot. If None, a new figure is created.
        survival : bool, optional
            Whether to plot a CDF (False) or CCDF (True). False by default.

        Returns
        -------
        ax : matplotlib axis
            The axis to which the plot was made.
        """
        if data is None:
            if hasattr(self, 'parent_Fit'):
                data = self.parent_Fit.data
        from numpy import unique
        bins = unique(trim_to_range(data, xmin=(self.xmin), xmax=(self.xmax)))
        CDF = self.cdf(bins, survival=survival)
        if not ax:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
        (ax.plot)(bins, CDF, **kwargs)
        ax.set_xscale('log')
        ax.set_yscale('log')
        return ax

    def plot_pdf(self, data=None, ax=None, **kwargs):
        """
        Plots the probability density function (PDF) of the
        theoretical distribution for the values given in data within xmin and
        xmax, if present. Plots to a new figure or to axis ax if provided.

        Parameters
        ----------
        data : list or array, optional
            If not provided, attempts to use the data from the Fit object in
            which the Distribution object is contained.
        ax : matplotlib axis, optional
            The axis to which to plot. If None, a new figure is created.

        Returns
        -------
        ax : matplotlib axis
            The axis to which the plot was made.
        """
        if data is None:
            if hasattr(self, 'parent_Fit'):
                data = self.parent_Fit.data
        else:
            from numpy import unique
            bins = unique(trim_to_range(data, xmin=(self.xmin), xmax=(self.xmax)))
            PDF = self.pdf(bins)
            from numpy import nan
            PDF[PDF == 0] = nan
            if not ax:
                import matplotlib.pyplot as plt
                (plt.plot)(bins, PDF, **kwargs)
                ax = plt.gca()
            else:
                (ax.plot)(bins, PDF, **kwargs)
        ax.set_xscale('log')
        ax.set_yscale('log')
        return ax

    def generate_random(self, n=1, estimate_discrete=None):
        """
        Generates random numbers from the theoretical probability distribution.
        If xmax is present, it is currently ignored.

        Parameters
        ----------
        n : int or float
            The number of random numbers to generate
        estimate_discrete : boolean
            For discrete distributions, whether to use a faster approximation of
            the random number generator. If None, attempts to inherit
            the estimate_discrete behavior used for fitting from the Distribution
            object or the parent Fit object, if present. Approximations only
            exist for some distributions (namely the power law). If an
            approximation does not exist an estimate_discrete setting of True
            will not be inherited.

        Returns
        -------
        r : array
            Random numbers drawn from the distribution
        """
        from numpy.random import rand
        from numpy import array
        r = rand(n)
        if not self.discrete:
            x = self._generate_random_continuous(r)
        elif estimate_discrete:
            if not hasattr(self, '_generate_random_discrete_estimate'):
                raise AttributeError('This distribution does not have an estimation of the discrete form for generating simulated data. Try the exact form with estimate_discrete=False.')
        else:
            if estimate_discrete is None:
                if not hasattr(self, '_generate_random_discrete_estimate'):
                    estimate_discrete = False
                elif hasattr(self, 'estimate_discrete'):
                    estimate_discrete = self.estimate_discrete
                elif hasattr('parent_Fit'):
                    estimate_discrete = self.parent_Fit.estimate_discrete
                else:
                    estimate_discrete = False
            if estimate_discrete:
                x = self._generate_random_discrete_estimate(r)
            else:
                x = array([self._double_search_discrete(R) for R in r], dtype='float')
        return x

    def _double_search_discrete(self, r):
        x2 = int(self.xmin)
        while self.ccdf(data=[x2]) >= 1 - r:
            x1 = x2
            x2 = 2 * x1

        x = bisect_map(x1, x2, self.ccdf, 1 - r)
        return x


class Power_Law(Distribution):

    def __init__(self, estimate_discrete=True, **kwargs):
        self.estimate_discrete = estimate_discrete
        (Distribution.__init__)(self, **kwargs)

    def parameters(self, params):
        self.alpha = params[0]
        self.parameter1 = self.alpha
        self.parameter1_name = 'alpha'

    @property
    def name(self):
        return 'power_law'

    @property
    def sigma(self):
        from numpy import sqrt
        return (self.alpha - 1) / sqrt(self.n)

    def _in_standard_parameter_range(self):
        return self.alpha > 1

    def fit(self, data=None):
        if data is None:
            if hasattr(self, 'parent_Fit'):
                data = self.parent_Fit.data
        else:
            data = trim_to_range(data, xmin=(self.xmin), xmax=(self.xmax))
            self.n = len(data)
            from numpy import log, sum
            if not self.discrete:
                if not self.xmax:
                    self.alpha = 1 + self.n / sum(log(data / self.xmin))
                    if not self.in_range():
                        Distribution.fit(self, data, suppress_output=True)
                    self.KS(data)
                elif self.discrete and self.estimate_discrete:
                    self.alpha = self.xmax or 1 + self.n / sum(log(data / (self.xmin - 0.5)))
                    if not self.in_range():
                        Distribution.fit(self, data, suppress_output=True)
                    self.KS(data)
                else:
                    Distribution.fit(self, data, suppress_output=True)
                if not self.in_range():
                    self.noise_flag = True
            else:
                self.noise_flag = False

    def _initial_parameters(self, data):
        from numpy import log, sum
        return 1 + len(data) / sum(log(data / self.xmin))

    def _cdf_base_function(self, x):
        if self.discrete:
            from scipy.special import zeta
            CDF = 1 - zeta(self.alpha, x)
        else:
            CDF = 1 - (x / self.xmin) ** (-self.alpha + 1)
        return CDF

    def _pdf_base_function(self, x):
        return x ** (-self.alpha)

    @property
    def _pdf_continuous_normalizer(self):
        return (self.alpha - 1) * self.xmin ** (self.alpha - 1)

    @property
    def _pdf_discrete_normalizer(self):
        C = 1.0 - self._cdf_xmin
        if self.xmax:
            C -= 1 - self._cdf_base_function(self.xmax + 1)
        C = 1.0 / C
        return C

    def _generate_random_continuous(self, r):
        return self.xmin * (1 - r) ** (-1 / (self.alpha - 1))

    def _generate_random_discrete_estimate(self, r):
        x = (self.xmin - 0.5) * (1 - r) ** (-1 / (self.alpha - 1)) + 0.5
        from numpy import around
        return around(x)


class Exponential(Distribution):

    def parameters(self, params):
        self.Lambda = params[0]
        self.parameter1 = self.Lambda
        self.parameter1_name = 'lambda'

    @property
    def name(self):
        return 'exponential'

    def _initial_parameters(self, data):
        from numpy import mean
        return 1 / mean(data)

    def _in_standard_parameter_range(self):
        return self.Lambda > 0

    def _cdf_base_function(self, x):
        from numpy import exp
        CDF = 1 - exp(-self.Lambda * x)
        return CDF

    def _pdf_base_function(self, x):
        from numpy import exp
        return exp(-self.Lambda * x)

    @property
    def _pdf_continuous_normalizer(self):
        from numpy import exp
        return self.Lambda * exp(self.Lambda * self.xmin)

    @property
    def _pdf_discrete_normalizer(self):
        from numpy import exp
        C = (1 - exp(-self.Lambda)) * exp(self.Lambda * self.xmin)
        if self.xmax:
            Cxmax = (1 - exp(-self.Lambda)) * exp(self.Lambda * self.xmax)
            C = 1.0 / C - 1.0 / Cxmax
            C = 1.0 / C
        return C

    def pdf(self, data=None):
        if data is None:
            if hasattr(self, 'parent_Fit'):
                data = self.parent_Fit.data
        elif not self.discrete:
            if self.in_range():
                data = self.xmax or trim_to_range(data, xmin=(self.xmin), xmax=(self.xmax))
                from numpy import exp
                likelihoods = self.Lambda * exp(self.Lambda * (self.xmin - data))
                from sys import float_info
                likelihoods[likelihoods == 0] = 10 ** float_info.min_10_exp
        else:
            likelihoods = Distribution.pdf(self, data)
        return likelihoods

    def loglikelihoods(self, data=None):
        if data is None:
            if hasattr(self, 'parent_Fit'):
                data = self.parent_Fit.data
        elif not self.discrete:
            if self.in_range():
                data = self.xmax or trim_to_range(data, xmin=(self.xmin), xmax=(self.xmax))
                from numpy import log
                loglikelihoods = log(self.Lambda) + self.Lambda * (self.xmin - data)
                from sys import float_info
                loglikelihoods[loglikelihoods == 0] = log(10 ** float_info.min_10_exp)
        else:
            loglikelihoods = Distribution.loglikelihoods(self, data)
        return loglikelihoods

    def _generate_random_continuous(self, r):
        from numpy import log
        return self.xmin - 1 / self.Lambda * log(1 - r)


class Stretched_Exponential(Distribution):

    def parameters(self, params):
        self.Lambda = params[0]
        self.parameter1 = self.Lambda
        self.parameter1_name = 'lambda'
        self.beta = params[1]
        self.parameter2 = self.beta
        self.parameter2_name = 'beta'

    @property
    def name(self):
        return 'stretched_exponential'

    def _initial_parameters(self, data):
        from numpy import mean
        return (
         1 / mean(data), 1)

    def _in_standard_parameter_range(self):
        return self.Lambda > 0 and self.beta > 0

    def _cdf_base_function(self, x):
        from numpy import exp
        CDF = 1 - exp(-(self.Lambda * x) ** self.beta)
        return CDF

    def _pdf_base_function(self, x):
        from numpy import exp
        return (x * self.Lambda) ** (self.beta - 1) * exp(-(self.Lambda * x) ** self.beta)

    @property
    def _pdf_continuous_normalizer(self):
        from numpy import exp
        C = self.beta * self.Lambda * exp((self.Lambda * self.xmin) ** self.beta)
        return C

    @property
    def _pdf_discrete_normalizer(self):
        return False

    def pdf(self, data=None):
        if data is None:
            if hasattr(self, 'parent_Fit'):
                data = self.parent_Fit.data
        elif not self.discrete:
            if self.in_range():
                data = self.xmax or trim_to_range(data, xmin=(self.xmin), xmax=(self.xmax))
                from numpy import exp
                likelihoods = (data * self.Lambda) ** (self.beta - 1) * self.beta * self.Lambda * exp((self.Lambda * self.xmin) ** self.beta - (self.Lambda * data) ** self.beta)
                from sys import float_info
                likelihoods[likelihoods == 0] = 10 ** float_info.min_10_exp
        else:
            likelihoods = Distribution.pdf(self, data)
        return likelihoods

    def loglikelihoods(self, data=None):
        if data is None:
            if hasattr(self, 'parent_Fit'):
                data = self.parent_Fit.data
        elif not self.discrete:
            if self.in_range():
                data = self.xmax or trim_to_range(data, xmin=(self.xmin), xmax=(self.xmax))
                from numpy import log
                loglikelihoods = log((data * self.Lambda) ** (self.beta - 1) * self.beta * self.Lambda) + (self.Lambda * self.xmin) ** self.beta - (self.Lambda * data) ** self.beta
                from sys import float_info
                from numpy import inf
                loglikelihoods[loglikelihoods == -inf] = log(10 ** float_info.min_10_exp)
        else:
            loglikelihoods = Distribution.loglikelihoods(self, data)
        return loglikelihoods

    def _generate_random_continuous(self, r):
        from numpy import log
        return 1 / self.Lambda * ((self.Lambda * self.xmin) ** self.beta - log(1 - r)) ** (1 / self.beta)


class Truncated_Power_Law(Distribution):

    def parameters(self, params):
        self.alpha = params[0]
        self.parameter1 = self.alpha
        self.parameter1_name = 'alpha'
        self.Lambda = params[1]
        self.parameter2 = self.Lambda
        self.parameter2_name = 'lambda'

    @property
    def name(self):
        return 'truncated_power_law'

    def _initial_parameters(self, data):
        from numpy import log, sum, mean
        alpha = 1 + len(data) / sum(log(data / self.xmin))
        Lambda = 1 / mean(data)
        return (
         alpha, Lambda)

    def _in_standard_parameter_range(self):
        return self.Lambda > 0 and self.alpha > 1

    def _cdf_base_function(self, x):
        from mpmath import gammainc
        from numpy import vectorize
        gammainc = vectorize(gammainc)
        CDF = gammainc(1 - self.alpha, self.Lambda * x).astype('float') / self.Lambda ** (1 - self.alpha)
        CDF = 1 - CDF
        return CDF

    def _pdf_base_function(self, x):
        from numpy import exp
        return x ** (-self.alpha) * exp(-self.Lambda * x)

    @property
    def _pdf_continuous_normalizer(self):
        from mpmath import gammainc
        C = self.Lambda ** (1 - self.alpha) / float(gammainc(1 - self.alpha, self.Lambda * self.xmin))
        return C

    @property
    def _pdf_discrete_normalizer(self):
        from mpmath import lerchphi
        from mpmath import exp
        C = float(exp(self.xmin * self.Lambda) / lerchphi(exp(-self.Lambda), self.alpha, self.xmin))
        if self.xmax:
            Cxmax = float(exp(self.xmax * self.Lambda) / lerchphi(exp(-self.Lambda), self.alpha, self.xmax))
            C = 1.0 / C - 1.0 / Cxmax
            C = 1.0 / C
        return C

    def pdf(self, data=None):
        if data is None:
            if hasattr(self, 'parent_Fit'):
                data = self.parent_Fit.data
        elif not self.discrete:
            if self.in_range() and False:
                data = trim_to_range(data, xmin=(self.xmin), xmax=(self.xmax))
                from numpy import exp
                from mpmath import gammainc
                likelihoods = self.Lambda ** (1 - self.alpha) / (data ** self.alpha * exp(self.Lambda * data) * gammainc(1 - self.alpha, self.Lambda * self.xmin)).astype(float)
                from sys import float_info
                likelihoods[likelihoods == 0] = 10 ** float_info.min_10_exp
        else:
            likelihoods = Distribution.pdf(self, data)
        return likelihoods

    def _generate_random_continuous(self, r):

        def helper(r):
            from numpy import log
            from numpy.random import rand
            while True:
                x = self.xmin - 1 / self.Lambda * log(1 - r)
                p = (x / self.xmin) ** (-self.alpha)
                if rand() < p:
                    return x
                r = rand()

        from numpy import array
        return array(list(map(helper, r)))


class Lognormal(Distribution):

    def parameters(self, params):
        self.mu = params[0]
        self.parameter1 = self.mu
        self.parameter1_name = 'mu'
        self.sigma = params[1]
        self.parameter2 = self.sigma
        self.parameter2_name = 'sigma'

    @property
    def name(self):
        return 'lognormal'

    def pdf(self, data=None):
        """
        Returns the probability density function (normalized histogram) of the
        theoretical distribution for the values in data within xmin and xmax,
        if present.

        Parameters
        ----------
        data : list or array, optional
            If not provided, attempts to use the data from the Fit object in
            which the Distribution object is contained.

        Returns
        -------
        probabilities : array
        """
        if data is None:
            if hasattr(self, 'parent_Fit'):
                data = self.parent_Fit.data
            else:
                data = trim_to_range(data, xmin=(self.xmin), xmax=(self.xmax))
                n = len(data)
                from sys import float_info
                from numpy import tile
                return self.in_range() or tile(10 ** float_info.min_10_exp, n)
            if not self.discrete:
                f = self._pdf_base_function(data)
                C = self._pdf_continuous_normalizer
                if C > 0:
                    likelihoods = f / C
                else:
                    likelihoods = tile(10 ** float_info.min_10_exp, n)
        elif self._pdf_discrete_normalizer:
            f = self._pdf_base_function(data)
            C = self._pdf_discrete_normalizer
            likelihoods = f * C
        elif self.discrete_approximation == 'round':
            likelihoods = self._round_discrete_approx(data)
        else:
            if self.discrete_approximation == 'xmax':
                upper_limit = self.xmax
            else:
                upper_limit = self.discrete_approximation
            from numpy import arange
            X = arange(self.xmin, upper_limit + 1)
            PDF = self._pdf_base_function(X)
            PDF = (PDF / sum(PDF)).astype(float)
            likelihoods = PDF[(data - self.xmin).astype(int)]
        likelihoods[likelihoods == 0] = 10 ** float_info.min_10_exp
        return likelihoods

    def _round_discrete_approx(self, data):
        """
        This function reformulates the calculation to avoid underflow errors
        with the erf function. As implemented, erf(x) quickly approaches 1
        while erfc(x) is more accurate. Since erfc(x) = 1 - erf(x),
        calculations can be written using erfc(x)
        """
        import numpy as np
        import scipy.special as ss
        lower_data = data - 0.5
        upper_data = data + 0.5
        self.xmin -= 0.5
        if self.xmax:
            self.xmax += 0.5
        else:
            arg1 = (np.log(lower_data) - self.mu) / (np.sqrt(2) * self.sigma)
            arg2 = (np.log(upper_data) - self.mu) / (np.sqrt(2) * self.sigma)
            likelihoods = 0.5 * (ss.erfc(arg1) - ss.erfc(arg2))
            if not self.xmax:
                norm = 0.5 * ss.erfc((np.log(self.xmin) - self.mu) / (np.sqrt(2) * self.sigma))
            else:
                norm = -self._cdf_xmin + self._cdf_base_function(self.xmax)
        self.xmin += 0.5
        if self.xmax:
            self.xmax -= 0.5
        return likelihoods / norm

    def cdf(self, data=None, survival=False):
        """
        The cumulative distribution function (CDF) of the lognormal
        distribution. Calculated for the values given in data within xmin and
        xmax, if present. Calculation was reformulated to avoid underflow
        errors

        Parameters
        ----------
        data : list or array, optional
            If not provided, attempts to use the data from the Fit object in
            which the Distribution object is contained.
        survival : bool, optional
            Whether to calculate a CDF (False) or CCDF (True).
            False by default.

        Returns
        -------
        X : array
            The sorted, unique values in the data.
        probabilities : array
            The portion of the data that is less than or equal to X.
        """
        from numpy import log, sqrt
        import scipy.special as ss
        if data is None:
            if hasattr(self, 'parent_Fit'):
                data = self.parent_Fit.data
        data = trim_to_range(data, xmin=(self.xmin), xmax=(self.xmax))
        n = len(data)
        from sys import float_info
        if not self.in_range():
            from numpy import tile
            return tile(10 ** float_info.min_10_exp, n)
        val_data = (log(data) - self.mu) / (sqrt(2) * self.sigma)
        val_xmin = (log(self.xmin) - self.mu) / (sqrt(2) * self.sigma)
        CDF = 0.5 * (ss.erfc(val_xmin) - ss.erfc(val_data))
        norm = 0.5 * ss.erfc(val_xmin)
        if self.xmax:
            norm = norm - (1 - self._cdf_base_function(self.xmax))
        CDF = CDF / norm
        if survival:
            CDF = 1 - CDF
        possible_numerical_error = False
        from numpy import isnan, min
        if isnan(min(CDF)):
            print("'nan' in fit cumulative distribution values.", file=(sys.stderr))
            possible_numerical_error = True
        if possible_numerical_error:
            print('Likely underflow or overflow error: the optimal fit for this distribution gives values that are so extreme that we lack the numerical precision to calculate them.', file=(sys.stderr))
        return CDF

    def _initial_parameters(self, data):
        from numpy import mean, std, log
        logdata = log(data)
        return (
         mean(logdata), std(logdata))

    def _in_standard_parameter_range(self):
        return self.sigma > 0

    def _cdf_base_function(self, x):
        from numpy import sqrt, log
        from scipy.special import erf
        return 0.5 + 0.5 * erf((log(x) - self.mu) / (sqrt(2) * self.sigma))

    def _pdf_base_function(self, x):
        from numpy import exp, log
        return 1.0 / x * exp(-(log(x) - self.mu) ** 2 / (2 * self.sigma ** 2))

    @property
    def _pdf_continuous_normalizer(self):
        from mpmath import erfc
        from scipy.constants import pi
        from numpy import sqrt, log
        C = erfc((log(self.xmin) - self.mu) / (sqrt(2) * self.sigma)) / sqrt(2 / (pi * self.sigma ** 2))
        return float(C)

    @property
    def _pdf_discrete_normalizer(self):
        return False

    def _generate_random_continuous(self, r):
        from numpy import exp, sqrt, log, frompyfunc
        from mpmath import erf, erfinv
        erfinv = frompyfunc(erfinv, 1, 1)
        Q = erf((log(self.xmin) - self.mu) / (sqrt(2) * self.sigma))
        Q = Q * r - r + 1.0
        Q = erfinv(Q).astype('float')
        return exp(self.mu + sqrt(2) * self.sigma * Q)


class Lognormal_Positive(Lognormal):

    @property
    def name(self):
        return 'lognormal_positive'

    def _in_standard_parameter_range(self):
        return self.sigma > 0 and self.mu > 0


def nested_loglikelihood_ratio(loglikelihoods1, loglikelihoods2, **kwargs):
    """
    Calculates a loglikelihood ratio and the p-value for testing which of two
    probability distributions is more likely to have created a set of
    observations. Assumes one of the probability distributions is a nested
    version of the other.

    Parameters
    ----------
    loglikelihoods1 : list or array
        The logarithms of the likelihoods of each observation, calculated from
        a particular probability distribution.
    loglikelihoods2 : list or array
        The logarithms of the likelihoods of each observation, calculated from
        a particular probability distribution.
    nested : bool, optional
        Whether one of the two probability distributions that generated the
        likelihoods is a nested version of the other. True by default.
    normalized_ratio : bool, optional
        Whether to return the loglikelihood ratio, R, or the normalized
        ratio R/sqrt(n*variance)

    Returns
    -------
    R : float
        The loglikelihood ratio of the two sets of likelihoods. If positive, 
        the first set of likelihoods is more likely (and so the probability
        distribution that produced them is a better fit to the data). If
        negative, the reverse is true.
    p : float
        The significance of the sign of R. If below a critical value
        (typically .05) the sign of R is taken to be significant. If above the
        critical value the sign of R is taken to be due to statistical
        fluctuations.
    """
    return loglikelihood_ratio(loglikelihoods1, loglikelihoods2, nested=True, **kwargs)


def loglikelihood_ratio(loglikelihoods1, loglikelihoods2, nested=False, normalized_ratio=False):
    """
    Calculates a loglikelihood ratio and the p-value for testing which of two
    probability distributions is more likely to have created a set of
    observations.

    Parameters
    ----------
    loglikelihoods1 : list or array
        The logarithms of the likelihoods of each observation, calculated from
        a particular probability distribution.
    loglikelihoods2 : list or array
        The logarithms of the likelihoods of each observation, calculated from
        a particular probability distribution.
    nested : bool, optional
        Whether one of the two probability distributions that generated the
        likelihoods is a nested version of the other. False by default.
    normalized_ratio : bool, optional
        Whether to return the loglikelihood ratio, R, or the normalized
        ratio R/sqrt(n*variance)

    Returns
    -------
    R : float
        The loglikelihood ratio of the two sets of likelihoods. If positive, 
        the first set of likelihoods is more likely (and so the probability
        distribution that produced them is a better fit to the data). If
        negative, the reverse is true.
    p : float
        The significance of the sign of R. If below a critical value
        (typically .05) the sign of R is taken to be significant. If above the
        critical value the sign of R is taken to be due to statistical
        fluctuations.
    """
    from numpy import sqrt
    from scipy.special import erfc
    n = float(len(loglikelihoods1))
    if n == 0:
        R = 0
        p = 1
        return (
         R, p)
    else:
        from numpy import asarray
        loglikelihoods1 = asarray(loglikelihoods1)
        loglikelihoods2 = asarray(loglikelihoods2)
        from numpy import inf, log
        from sys import float_info
        min_val = log(10 ** float_info.min_10_exp)
        loglikelihoods1[loglikelihoods1 == -inf] = min_val
        loglikelihoods2[loglikelihoods2 == -inf] = min_val
        R = sum(loglikelihoods1 - loglikelihoods2)
        from numpy import mean
        mean_diff = mean(loglikelihoods1) - mean(loglikelihoods2)
        variance = sum((loglikelihoods1 - loglikelihoods2 - mean_diff) ** 2) / n
        if nested:
            from scipy.stats import chi2
            p = 1 - chi2.cdf(abs(2 * R), 1)
        else:
            p = erfc(abs(R) / sqrt(2 * n * variance))
    if normalized_ratio:
        R = R / sqrt(n * variance)
    return (
     R, p)


def cdf(data, survival=False, **kwargs):
    """
    The cumulative distribution function (CDF) of the data.

    Parameters
    ----------
    data : list or array, optional
    survival : bool, optional
        Whether to calculate a CDF (False) or CCDF (True). False by default.

    Returns
    -------
    X : array
        The sorted, unique values in the data.
    probabilities : array
        The portion of the data that is less than or equal to X.
    """
    return cumulative_distribution_function(data, survival=survival, **kwargs)


def ccdf(data, survival=True, **kwargs):
    """
    The complementary cumulative distribution function (CCDF) of the data.

    Parameters
    ----------
    data : list or array, optional
    survival : bool, optional
        Whether to calculate a CDF (False) or CCDF (True). True by default.

    Returns
    -------
    X : array
        The sorted, unique values in the data.
    probabilities : array
        The portion of the data that is less than or equal to X.
    """
    return cumulative_distribution_function(data, survival=survival, **kwargs)


def cumulative_distribution_function(data, xmin=None, xmax=None, survival=False, **kwargs):
    """
    The cumulative distribution function (CDF) of the data.

    Parameters
    ----------
    data : list or array, optional
    survival : bool, optional
        Whether to calculate a CDF (False) or CCDF (True). False by default.
    xmin : int or float, optional
        The minimum data size to include. Values less than xmin are excluded.
    xmax : int or float, optional
        The maximum data size to include. Values greater than xmin are
        excluded.

    Returns
    -------
    X : array
        The sorted, unique values in the data.
    probabilities : array
        The portion of the data that is less than or equal to X.
    """
    from numpy import array
    data = array(data)
    if not data.any():
        from numpy import nan
        return (array([nan]), array([nan]))
    data = trim_to_range(data, xmin=xmin, xmax=xmax)
    n = float(len(data))
    from numpy import sort
    data = sort(data)
    all_unique = not any(data[:-1] == data[1:])
    if all_unique:
        from numpy import arange
        CDF = arange(n) / n
    else:
        from numpy import searchsorted, unique
        CDF = searchsorted(data, data, side='left') / n
        unique_data, unique_indices = unique(data, return_index=True)
        data = unique_data
        CDF = CDF[unique_indices]
    if survival:
        CDF = 1 - CDF
    return (data, CDF)


def is_discrete(data):
    """Checks if every element of the array is an integer."""
    from numpy import floor
    return (floor(data) == data.astype(float)).all()


def trim_to_range(data, xmin=None, xmax=None, **kwargs):
    """
    Removes elements of the data that are above xmin or below xmax (if present)
    """
    from numpy import asarray
    data = asarray(data)
    if xmin:
        data = data[(data >= xmin)]
    if xmax:
        data = data[(data <= xmax)]
    return data


def pdf(data, xmin=None, xmax=None, linear_bins=False, **kwargs):
    """
    Returns the probability density function (normalized histogram) of the
    data.

    Parameters
    ----------
    data : list or array
    xmin : float, optional
        Minimum value of the PDF. If None, uses the smallest value in the data.
    xmax : float, optional
        Maximum value of the PDF. If None, uses the largest value in the data.
    linear_bins : float, optional
        Whether to use linearly spaced bins, as opposed to logarithmically
        spaced bins (recommended for log-log plots).

    Returns
    -------
    bin_edges : array
        The edges of the bins of the probability density function.
    probabilities : array
        The portion of the data that is within the bin. Length 1 less than
        bin_edges, as it corresponds to the spaces between them.
    """
    from numpy import logspace, histogram, floor, unique
    from math import ceil, log10
    if not xmax:
        xmax = max(data)
    else:
        if not xmin:
            xmin = min(data)
        if linear_bins:
            bins = range(int(xmin), int(xmax))
        else:
            log_min_size = log10(xmin)
        log_max_size = log10(xmax)
        number_of_bins = ceil((log_max_size - log_min_size) * 10)
        bins = unique(floor(logspace(log_min_size,
          log_max_size, num=number_of_bins)))
    hist, edges = histogram(data, bins, density=True)
    return (
     edges, hist)


def checkunique(data):
    """Quickly checks if a sorted array is all unique elements."""
    for i in range(len(data) - 1):
        if data[i] == data[(i + 1)]:
            return False

    return True


def plot_ccdf(data, ax=None, survival=False, **kwargs):
    return plot_cdf(data, ax=ax, survival=True, **kwargs)


def plot_cdf(data, ax=None, survival=False, **kwargs):
    """
    Plots the cumulative distribution function (CDF) of the data to a new
    figure or to axis ax if provided.

    Parameters
    ----------
    data : list or array
    ax : matplotlib axis, optional
        The axis to which to plot. If None, a new figure is created.
    survival : bool, optional
        Whether to plot a CDF (False) or CCDF (True). False by default.

    Returns
    -------
    ax : matplotlib axis
        The axis to which the plot was made.
    """
    bins, CDF = cdf(data, survival=survival, **kwargs)
    if not ax:
        import matplotlib.pyplot as plt
        (plt.plot)(bins, CDF, **kwargs)
        ax = plt.gca()
    else:
        (ax.plot)(bins, CDF, **kwargs)
    ax.set_xscale('log')
    ax.set_yscale('log')
    return ax


def plot_pdf(data, ax=None, linear_bins=False, **kwargs):
    """
    Plots the probability density function (PDF) to a new figure or to axis ax
    if provided.

    Parameters
    ----------
    data : list or array
    ax : matplotlib axis, optional
        The axis to which to plot. If None, a new figure is created.
    linear_bins : bool, optional
        Whether to use linearly spaced bins (True) or logarithmically
        spaced bins (False). False by default.

    Returns
    -------
    ax : matplotlib axis
        The axis to which the plot was made.
    """
    edges, hist = pdf(data, linear_bins=linear_bins, **kwargs)
    bin_centers = (edges[1:] + edges[:-1]) / 2.0
    from numpy import nan
    hist[hist == 0] = nan
    if not ax:
        import matplotlib.pyplot as plt
        (plt.plot)(bin_centers, hist, **kwargs)
        ax = plt.gca()
    else:
        (ax.plot)(bin_centers, hist, **kwargs)
    ax.set_xscale('log')
    ax.set_yscale('log')
    return ax


def bisect_map(mn, mx, function, target):
    """
    Uses binary search to find the target solution to a function, searching in
    a given ordered sequence of integer values.

    Parameters
    ----------
    seq : list or array, monotonically increasing integers
    function : a function that takes a single integer input, which monotonically
        decreases over the range of seq.
    target : the target value of the function

    Returns
    -------
    value : the input value that yields the target solution. If there is no
    exact solution in the input sequence, finds the nearest value k such that 
    function(k) <= target < function(k+1). This is similar to the behavior of
    bisect_left in the bisect package. If even the first, leftmost value of seq
    does not satisfy this condition, -1 is returned.
    """
    if function([mn]) < target or function([mx]) > target:
        return -1
    while mx == mn + 1:
        return mn
        m = (mn + mx) / 2
        value = function([m])[0]
        if value > target:
            mn = m
        elif value < target:
            mx = m
        else:
            return m


class Distribution_Fit(object):

    def __init__(self, data, name, xmin, discrete=False, xmax=None, method='Likelihood', estimate_discrete=True):
        self.data = data
        self.discrete = discrete
        self.xmin = xmin
        self.xmax = xmax
        self.method = method
        self.name = name
        self.estimate_discrete = estimate_discrete

    def __getattr__(self, name):
        param_names = {'lognormal':('mu', 'sigma', None), 
         'exponential':('Lambda', None, None), 
         'truncated_power_law':('alpha', 'Lambda', None), 
         'power_law':('alpha', None, None), 
         'negative_binomial':('r', 'p', None), 
         'stretched_exponential':('Lambda', 'beta', None), 
         'gamma':('k', 'theta', None)}
        param_names = param_names[self.name]
        if name in param_names:
            if name == param_names[0]:
                setattr(self, name, self.parameter1)
            elif name == param_names[1]:
                setattr(self, name, self.parameter2)
            elif name == param_names[2]:
                setattr(self, name, self.parameter3)
            return getattr(self, name)
        if name in ('parameters', 'parameter1_name', 'parameter1', 'parameter2_name',
                    'parameter2', 'parameter3_name', 'parameter3', 'loglikelihood'):
            self.parameters, self.loglikelihood = distribution_fit((self.data), distribution=(self.name), discrete=(self.discrete), xmin=(self.xmin),
              xmax=(self.xmax),
              search_method=(self.method),
              estimate_discrete=(self.estimate_discrete))
            self.parameter1 = self.parameters[0]
            if len(self.parameters) < 2:
                self.parameter2 = None
            else:
                self.parameter2 = self.parameters[1]
            if len(self.parameters) < 3:
                self.parameter3 = None
            else:
                self.parameter3 = self.parameters[2]
            self.parameter1_name = param_names[0]
            self.parameter2_name = param_names[1]
            self.parameter3_name = param_names[2]
            if name == 'parameters':
                return self.parameters
            if name == 'parameter1_name':
                return self.parameter1_name
            if name == 'parameter2_name':
                return self.parameter2_name
            if name == 'parameter3_name':
                return self.parameter3_name
            if name == 'parameter1':
                return self.parameter1
            if name == 'parameter2':
                return self.parameter2
            if name == 'parameter3':
                return self.parameter3
            if name == 'loglikelihood':
                return self.loglikelihood
        if name == 'D':
            if self.name != 'power_law':
                self.D = None
            else:
                self.D = power_law_ks_distance((self.data), (self.parameter1), xmin=(self.xmin), xmax=(self.xmax), discrete=(self.discrete))
            return self.D
        if name == 'p':
            print('A p value outside of a loglihood ratio comparison to another candidate distribution is not currently supported.\n                     If your data set is particularly large and has any noise in it at all, using such statistical tools as the Monte Carlo method\n                    can lead to erroneous results anyway; the presence of the noise means the distribution will obviously not perfectly fit the\n                    candidate distribution, and the very large number of samples will make the Monte Carlo simulations very close to a perfect\n                    fit. As such, such a test will always fail, unless your candidate distribution perfectly describes all elements of the\n                    system, including the noise. A more helpful analysis is the comparison between multiple, specific candidate distributions\n                    (the loglikelihood ratio test), which tells you which is the best fit of these distributions.',
              file=(sys.stderr))
            self.p = None
            return self.p
        raise AttributeError(name)


def distribution_fit--- This code section failed: ---

 L.2211         0  LOAD_CONST               0
                2  LOAD_CONST               ('log',)
                4  IMPORT_NAME              numpy
                6  IMPORT_FROM              log
                8  STORE_DEREF              'log'
               10  POP_TOP          

 L.2213        12  LOAD_FAST                'distribution'
               14  LOAD_STR                 'negative_binomial'
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    66  'to 66'
               20  LOAD_GLOBAL              is_discrete
               22  LOAD_DEREF               'data'
               24  CALL_FUNCTION_1       1  ''
               26  POP_JUMP_IF_TRUE     66  'to 66'

 L.2214        28  LOAD_GLOBAL              print
               30  LOAD_STR                 'Rounding to integer values for negative binomial fit.'
               32  LOAD_GLOBAL              sys
               34  LOAD_ATTR                stderr
               36  LOAD_CONST               ('file',)
               38  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               40  POP_TOP          

 L.2215        42  LOAD_CONST               0
               44  LOAD_CONST               ('around',)
               46  IMPORT_NAME              numpy
               48  IMPORT_FROM              around
               50  STORE_FAST               'around'
               52  POP_TOP          

 L.2216        54  LOAD_FAST                'around'
               56  LOAD_DEREF               'data'
               58  CALL_FUNCTION_1       1  ''
               60  STORE_DEREF              'data'

 L.2217        62  LOAD_CONST               True
               64  STORE_FAST               'discrete'
             66_0  COME_FROM            26  '26'
             66_1  COME_FROM            18  '18'

 L.2220        66  LOAD_FAST                'xmin'
               68  LOAD_CONST               None
               70  COMPARE_OP               is
               72  POP_JUMP_IF_TRUE    106  'to 106'
               74  LOAD_FAST                'xmin'
               76  LOAD_STR                 'find'
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_TRUE    106  'to 106'
               82  LOAD_GLOBAL              type
               84  LOAD_FAST                'xmin'
               86  CALL_FUNCTION_1       1  ''
               88  LOAD_GLOBAL              tuple
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_TRUE    106  'to 106'
               94  LOAD_GLOBAL              type
               96  LOAD_FAST                'xmin'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_GLOBAL              list
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   174  'to 174'
            106_0  COME_FROM            92  '92'
            106_1  COME_FROM            80  '80'
            106_2  COME_FROM            72  '72'

 L.2221       106  LOAD_CONST               0
              108  LOAD_DEREF               'data'
              110  COMPARE_OP               in
              112  POP_JUMP_IF_FALSE   140  'to 140'

 L.2222       114  LOAD_GLOBAL              print
              116  LOAD_STR                 'Value 0 in data. Throwing out 0 values'
              118  LOAD_GLOBAL              sys
              120  LOAD_ATTR                stderr
              122  LOAD_CONST               ('file',)
              124  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              126  POP_TOP          

 L.2223       128  LOAD_DEREF               'data'
              130  LOAD_DEREF               'data'
              132  LOAD_CONST               0
              134  COMPARE_OP               !=
              136  BINARY_SUBSCR    
              138  STORE_DEREF              'data'
            140_0  COME_FROM           112  '112'

 L.2224       140  LOAD_GLOBAL              find_xmin
              142  LOAD_DEREF               'data'
              144  LOAD_FAST                'discrete'
              146  LOAD_FAST                'xmax'
              148  LOAD_FAST                'search_method'
              150  LOAD_FAST                'estimate_discrete'
              152  LOAD_FAST                'xmin'
              154  LOAD_CONST               ('discrete', 'xmax', 'search_method', 'estimate_discrete', 'xmin_range')
              156  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              158  UNPACK_SEQUENCE_6     6 
              160  STORE_FAST               'xmin'
              162  STORE_FAST               'D'
              164  STORE_FAST               'alpha'
              166  STORE_FAST               'loglikelihood'
              168  STORE_FAST               'n_tail'
              170  STORE_FAST               'noise_flag'
              172  JUMP_FORWARD        178  'to 178'
            174_0  COME_FROM           104  '104'

 L.2226       174  LOAD_CONST               None
              176  STORE_FAST               'alpha'
            178_0  COME_FROM           172  '172'

 L.2228       178  LOAD_FAST                'distribution'
              180  LOAD_STR                 'power_law'
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   200  'to 200'
              186  LOAD_FAST                'alpha'
              188  POP_JUMP_IF_FALSE   200  'to 200'

 L.2229       190  LOAD_FAST                'alpha'
              192  BUILD_LIST_1          1 
              194  LOAD_FAST                'loglikelihood'
              196  BUILD_TUPLE_2         2 
              198  RETURN_VALUE     
            200_0  COME_FROM           188  '188'
            200_1  COME_FROM           184  '184'

 L.2231       200  LOAD_GLOBAL              float
              202  LOAD_FAST                'xmin'
              204  CALL_FUNCTION_1       1  ''
              206  STORE_FAST               'xmin'

 L.2232       208  LOAD_DEREF               'data'
              210  LOAD_DEREF               'data'
              212  LOAD_FAST                'xmin'
              214  COMPARE_OP               >=
              216  BINARY_SUBSCR    
              218  STORE_DEREF              'data'

 L.2234       220  LOAD_FAST                'xmax'
              222  POP_JUMP_IF_FALSE   244  'to 244'

 L.2235       224  LOAD_GLOBAL              float
              226  LOAD_FAST                'xmax'
              228  CALL_FUNCTION_1       1  ''
              230  STORE_FAST               'xmax'

 L.2236       232  LOAD_DEREF               'data'
              234  LOAD_DEREF               'data'
              236  LOAD_FAST                'xmax'
              238  COMPARE_OP               <=
              240  BINARY_SUBSCR    
              242  STORE_DEREF              'data'
            244_0  COME_FROM           222  '222'

 L.2239       244  LOAD_FAST                'distribution'
              246  LOAD_STR                 'all'
              248  COMPARE_OP               ==
          250_252  POP_JUMP_IF_FALSE   634  'to 634'

 L.2240       254  LOAD_GLOBAL              print
              256  LOAD_STR                 'Analyzing all distributions'
              258  LOAD_GLOBAL              sys
              260  LOAD_ATTR                stderr
              262  LOAD_CONST               ('file',)
              264  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              266  POP_TOP          

 L.2241       268  LOAD_GLOBAL              print
              270  LOAD_STR                 'Calculating power law fit'
              272  LOAD_GLOBAL              sys
              274  LOAD_ATTR                stderr
              276  LOAD_CONST               ('file',)
              278  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              280  POP_TOP          

 L.2242       282  LOAD_FAST                'alpha'
          284_286  POP_JUMP_IF_FALSE   296  'to 296'

 L.2243       288  LOAD_FAST                'alpha'
              290  BUILD_LIST_1          1 
              292  STORE_FAST               'pl_parameters'
              294  JUMP_FORWARD        322  'to 322'
            296_0  COME_FROM           284  '284'

 L.2245       296  LOAD_GLOBAL              distribution_fit
              298  LOAD_DEREF               'data'
              300  LOAD_STR                 'power_law'
              302  LOAD_FAST                'discrete'
              304  LOAD_FAST                'xmin'
              306  LOAD_FAST                'xmax'
              308  LOAD_FAST                'search_method'
              310  LOAD_FAST                'estimate_discrete'
              312  LOAD_CONST               ('search_method', 'estimate_discrete')
              314  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              316  UNPACK_SEQUENCE_2     2 
              318  STORE_FAST               'pl_parameters'
              320  STORE_FAST               'loglikelihood'
            322_0  COME_FROM           294  '294'

 L.2246       322  BUILD_MAP_0           0 
              324  STORE_FAST               'results'

 L.2247       326  LOAD_FAST                'xmin'
              328  LOAD_FAST                'results'
              330  LOAD_STR                 'xmin'
              332  STORE_SUBSCR     

 L.2248       334  LOAD_FAST                'xmax'
              336  LOAD_FAST                'results'
              338  LOAD_STR                 'xmax'
              340  STORE_SUBSCR     

 L.2249       342  LOAD_FAST                'discrete'
              344  LOAD_FAST                'results'
              346  LOAD_STR                 'discrete'
              348  STORE_SUBSCR     

 L.2250       350  BUILD_MAP_0           0 
              352  LOAD_FAST                'results'
              354  LOAD_STR                 'fits'
              356  STORE_SUBSCR     

 L.2251       358  LOAD_FAST                'pl_parameters'
              360  LOAD_FAST                'loglikelihood'
              362  BUILD_TUPLE_2         2 
              364  LOAD_FAST                'results'
              366  LOAD_STR                 'fits'
              368  BINARY_SUBSCR    
              370  LOAD_STR                 'power_law'
              372  STORE_SUBSCR     

 L.2253       374  LOAD_GLOBAL              print
              376  LOAD_STR                 'Calculating truncated power law fit'
              378  LOAD_GLOBAL              sys
              380  LOAD_ATTR                stderr
              382  LOAD_CONST               ('file',)
              384  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              386  POP_TOP          

 L.2254       388  LOAD_GLOBAL              distribution_fit
              390  LOAD_DEREF               'data'
              392  LOAD_STR                 'truncated_power_law'
              394  LOAD_FAST                'discrete'
              396  LOAD_FAST                'xmin'
              398  LOAD_FAST                'xmax'
              400  LOAD_FAST                'pl_parameters'
              402  LOAD_CONST               0
              404  BINARY_SUBSCR    
              406  LOAD_FAST                'search_method'
              408  LOAD_FAST                'estimate_discrete'
              410  LOAD_CONST               ('comparison_alpha', 'search_method', 'estimate_discrete')
              412  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              414  UNPACK_SEQUENCE_4     4 
              416  STORE_FAST               'tpl_parameters'
              418  STORE_FAST               'loglikelihood'
              420  STORE_FAST               'R'
              422  STORE_FAST               'p'

 L.2255       424  LOAD_FAST                'tpl_parameters'
              426  LOAD_FAST                'loglikelihood'
              428  BUILD_TUPLE_2         2 
              430  LOAD_FAST                'results'
              432  LOAD_STR                 'fits'
              434  BINARY_SUBSCR    
              436  LOAD_STR                 'truncated_power_law'
              438  STORE_SUBSCR     

 L.2256       440  BUILD_MAP_0           0 
              442  LOAD_FAST                'results'
              444  LOAD_STR                 'power_law_comparison'
              446  STORE_SUBSCR     

 L.2257       448  LOAD_FAST                'R'
              450  LOAD_FAST                'p'
              452  BUILD_TUPLE_2         2 
              454  LOAD_FAST                'results'
              456  LOAD_STR                 'power_law_comparison'
              458  BINARY_SUBSCR    
              460  LOAD_STR                 'truncated_power_law'
              462  STORE_SUBSCR     

 L.2258       464  BUILD_MAP_0           0 
              466  LOAD_FAST                'results'
              468  LOAD_STR                 'truncated_power_law_comparison'
              470  STORE_SUBSCR     

 L.2260       472  LOAD_STR                 'exponential'
              474  LOAD_STR                 'lognormal'
              476  LOAD_STR                 'stretched_exponential'
              478  LOAD_STR                 'gamma'
              480  BUILD_LIST_4          4 
              482  STORE_FAST               'supported_distributions'

 L.2262       484  SETUP_LOOP          630  'to 630'
              486  LOAD_FAST                'supported_distributions'
              488  GET_ITER         
              490  FOR_ITER            628  'to 628'
              492  STORE_FAST               'i'

 L.2263       494  LOAD_GLOBAL              print
              496  LOAD_STR                 'Calculating %s fit'
              498  LOAD_FAST                'i'
              500  BUILD_TUPLE_1         1 
              502  BINARY_MODULO    
              504  LOAD_GLOBAL              sys
              506  LOAD_ATTR                stderr
              508  LOAD_CONST               ('file',)
              510  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              512  POP_TOP          

 L.2264       514  LOAD_GLOBAL              distribution_fit
              516  LOAD_DEREF               'data'
              518  LOAD_FAST                'i'
              520  LOAD_FAST                'discrete'
              522  LOAD_FAST                'xmin'
              524  LOAD_FAST                'xmax'
              526  LOAD_FAST                'pl_parameters'
              528  LOAD_CONST               0
              530  BINARY_SUBSCR    
              532  LOAD_FAST                'search_method'
              534  LOAD_FAST                'estimate_discrete'
              536  LOAD_CONST               ('comparison_alpha', 'search_method', 'estimate_discrete')
              538  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              540  UNPACK_SEQUENCE_4     4 
              542  STORE_FAST               'parameters'
              544  STORE_FAST               'loglikelihood'
              546  STORE_FAST               'R'
              548  STORE_FAST               'p'

 L.2265       550  LOAD_FAST                'parameters'
              552  LOAD_FAST                'loglikelihood'
              554  BUILD_TUPLE_2         2 
              556  LOAD_FAST                'results'
              558  LOAD_STR                 'fits'
              560  BINARY_SUBSCR    
              562  LOAD_FAST                'i'
              564  STORE_SUBSCR     

 L.2266       566  LOAD_FAST                'R'
              568  LOAD_FAST                'p'
              570  BUILD_TUPLE_2         2 
              572  LOAD_FAST                'results'
              574  LOAD_STR                 'power_law_comparison'
              576  BINARY_SUBSCR    
              578  LOAD_FAST                'i'
              580  STORE_SUBSCR     

 L.2268       582  LOAD_GLOBAL              distribution_compare
              584  LOAD_DEREF               'data'
              586  LOAD_STR                 'truncated_power_law'
              588  LOAD_FAST                'tpl_parameters'
              590  LOAD_FAST                'i'
              592  LOAD_FAST                'parameters'
              594  LOAD_FAST                'discrete'
              596  LOAD_FAST                'xmin'
              598  LOAD_FAST                'xmax'
              600  CALL_FUNCTION_8       8  ''
              602  UNPACK_SEQUENCE_2     2 
              604  STORE_FAST               'R'
              606  STORE_FAST               'p'

 L.2269       608  LOAD_FAST                'R'
              610  LOAD_FAST                'p'
              612  BUILD_TUPLE_2         2 
              614  LOAD_FAST                'results'
              616  LOAD_STR                 'truncated_power_law_comparison'
              618  BINARY_SUBSCR    
              620  LOAD_FAST                'i'
              622  STORE_SUBSCR     
          624_626  JUMP_BACK           490  'to 490'
              628  POP_BLOCK        
            630_0  COME_FROM_LOOP      484  '484'

 L.2270       630  LOAD_FAST                'results'
              632  RETURN_VALUE     
            634_0  COME_FROM           250  '250'

 L.2273       634  LOAD_CONST               False
              636  STORE_FAST               'no_data'

 L.2274       638  LOAD_FAST                'xmax'
          640_642  POP_JUMP_IF_FALSE   670  'to 670'
              644  LOAD_GLOBAL              all
              646  LOAD_DEREF               'data'
              648  LOAD_FAST                'xmax'
              650  COMPARE_OP               >
              652  LOAD_DEREF               'data'
              654  LOAD_FAST                'xmin'
              656  COMPARE_OP               <
              658  BINARY_ADD       
              660  CALL_FUNCTION_1       1  ''
          662_664  POP_JUMP_IF_FALSE   670  'to 670'

 L.2276       666  LOAD_CONST               True
              668  STORE_FAST               'no_data'
            670_0  COME_FROM           662  '662'
            670_1  COME_FROM           640  '640'

 L.2277       670  LOAD_GLOBAL              all
              672  LOAD_DEREF               'data'
              674  LOAD_FAST                'xmin'
              676  COMPARE_OP               <
              678  CALL_FUNCTION_1       1  ''
          680_682  POP_JUMP_IF_FALSE   688  'to 688'

 L.2278       684  LOAD_CONST               True
              686  STORE_FAST               'no_data'
            688_0  COME_FROM           680  '680'

 L.2279       688  LOAD_GLOBAL              len
              690  LOAD_DEREF               'data'
              692  CALL_FUNCTION_1       1  ''
              694  LOAD_CONST               2
              696  COMPARE_OP               <
          698_700  POP_JUMP_IF_FALSE   706  'to 706'

 L.2280       702  LOAD_CONST               True
              704  STORE_FAST               'no_data'
            706_0  COME_FROM           698  '698'

 L.2281       706  LOAD_FAST                'no_data'
          708_710  POP_JUMP_IF_FALSE   830  'to 830'

 L.2282       712  LOAD_CONST               0
              714  LOAD_CONST               ('array',)
              716  IMPORT_NAME              numpy
              718  IMPORT_FROM              array
              720  STORE_FAST               'array'
              722  POP_TOP          

 L.2283       724  LOAD_CONST               0
              726  LOAD_CONST               ('float_info',)
              728  IMPORT_NAME              sys
              730  IMPORT_FROM              float_info
              732  STORE_FAST               'float_info'
              734  POP_TOP          

 L.2284       736  LOAD_FAST                'array'
              738  LOAD_CONST               0
              740  LOAD_CONST               0
              742  LOAD_CONST               0
              744  BUILD_LIST_3          3 
              746  CALL_FUNCTION_1       1  ''
              748  STORE_FAST               'parameters'

 L.2285       750  LOAD_FAST                'search_method'
              752  LOAD_STR                 'Likelihood'
              754  COMPARE_OP               ==
          756_758  POP_JUMP_IF_FALSE   772  'to 772'

 L.2286       760  LOAD_CONST               10
              762  LOAD_FAST                'float_info'
              764  LOAD_ATTR                max_10_exp
              766  BINARY_POWER     
              768  UNARY_NEGATIVE   
              770  STORE_FAST               'loglikelihood'
            772_0  COME_FROM           756  '756'

 L.2287       772  LOAD_FAST                'search_method'
              774  LOAD_STR                 'KS'
              776  COMPARE_OP               ==
          778_780  POP_JUMP_IF_FALSE   786  'to 786'

 L.2288       782  LOAD_CONST               1
              784  STORE_FAST               'loglikelihood'
            786_0  COME_FROM           778  '778'

 L.2289       786  LOAD_FAST                'comparison_alpha'
              788  LOAD_CONST               None
              790  COMPARE_OP               is
          792_794  POP_JUMP_IF_FALSE   804  'to 804'

 L.2290       796  LOAD_FAST                'parameters'
              798  LOAD_FAST                'loglikelihood'
              800  BUILD_TUPLE_2         2 
              802  RETURN_VALUE     
            804_0  COME_FROM           792  '792'

 L.2291       804  LOAD_CONST               10
              806  LOAD_FAST                'float_info'
              808  LOAD_ATTR                max_10_exp
              810  BINARY_POWER     
              812  STORE_FAST               'R'

 L.2292       814  LOAD_CONST               1
              816  STORE_FAST               'p'

 L.2293       818  LOAD_FAST                'parameters'
              820  LOAD_FAST                'loglikelihood'
              822  LOAD_FAST                'R'
              824  LOAD_FAST                'p'
              826  BUILD_TUPLE_4         4 
              828  RETURN_VALUE     
            830_0  COME_FROM           708  '708'

 L.2295       830  LOAD_GLOBAL              float
              832  LOAD_GLOBAL              len
              834  LOAD_DEREF               'data'
              836  CALL_FUNCTION_1       1  ''
              838  CALL_FUNCTION_1       1  ''
              840  STORE_FAST               'n'

 L.2299       842  LOAD_FAST                'distribution'
              844  LOAD_STR                 'power_law'
              846  COMPARE_OP               ==
          848_850  POP_JUMP_IF_FALSE   888  'to 888'
              852  LOAD_FAST                'alpha'
          854_856  POP_JUMP_IF_TRUE    888  'to 888'

 L.2300       858  LOAD_CONST               1
              860  LOAD_FAST                'n'
              862  LOAD_GLOBAL              sum
              864  LOAD_DEREF               'log'
              866  LOAD_DEREF               'data'
              868  LOAD_FAST                'xmin'
              870  BINARY_TRUE_DIVIDE
              872  CALL_FUNCTION_1       1  ''
              874  CALL_FUNCTION_1       1  ''
              876  BINARY_TRUE_DIVIDE
              878  BINARY_ADD       
              880  BUILD_LIST_1          1 
              882  STORE_FAST               'initial_parameters'
          884_886  JUMP_FORWARD       1148  'to 1148'
            888_0  COME_FROM           854  '854'
            888_1  COME_FROM           848  '848'

 L.2301       888  LOAD_FAST                'distribution'
              890  LOAD_STR                 'exponential'
              892  COMPARE_OP               ==
          894_896  POP_JUMP_IF_FALSE   926  'to 926'

 L.2302       898  LOAD_CONST               0
              900  LOAD_CONST               ('mean',)
              902  IMPORT_NAME              numpy
              904  IMPORT_FROM              mean
              906  STORE_FAST               'mean'
              908  POP_TOP          

 L.2303       910  LOAD_CONST               1
              912  LOAD_FAST                'mean'
              914  LOAD_DEREF               'data'
              916  CALL_FUNCTION_1       1  ''
              918  BINARY_TRUE_DIVIDE
              920  BUILD_LIST_1          1 
              922  STORE_FAST               'initial_parameters'
              924  JUMP_FORWARD       1148  'to 1148'
            926_0  COME_FROM           894  '894'

 L.2304       926  LOAD_FAST                'distribution'
              928  LOAD_STR                 'stretched_exponential'
              930  COMPARE_OP               ==
          932_934  POP_JUMP_IF_FALSE   966  'to 966'

 L.2305       936  LOAD_CONST               0
              938  LOAD_CONST               ('mean',)
              940  IMPORT_NAME              numpy
              942  IMPORT_FROM              mean
              944  STORE_FAST               'mean'
              946  POP_TOP          

 L.2306       948  LOAD_CONST               1
              950  LOAD_FAST                'mean'
              952  LOAD_DEREF               'data'
              954  CALL_FUNCTION_1       1  ''
              956  BINARY_TRUE_DIVIDE
              958  LOAD_CONST               1
              960  BUILD_LIST_2          2 
              962  STORE_FAST               'initial_parameters'
              964  JUMP_FORWARD       1148  'to 1148'
            966_0  COME_FROM           932  '932'

 L.2307       966  LOAD_FAST                'distribution'
              968  LOAD_STR                 'truncated_power_law'
              970  COMPARE_OP               ==
          972_974  POP_JUMP_IF_FALSE  1026  'to 1026'

 L.2308       976  LOAD_CONST               0
              978  LOAD_CONST               ('mean',)
              980  IMPORT_NAME              numpy
              982  IMPORT_FROM              mean
              984  STORE_FAST               'mean'
              986  POP_TOP          

 L.2309       988  LOAD_CONST               1
              990  LOAD_FAST                'n'
              992  LOAD_GLOBAL              sum
              994  LOAD_DEREF               'log'
              996  LOAD_DEREF               'data'
              998  LOAD_FAST                'xmin'
             1000  BINARY_TRUE_DIVIDE
             1002  CALL_FUNCTION_1       1  ''
             1004  CALL_FUNCTION_1       1  ''
             1006  BINARY_TRUE_DIVIDE
             1008  BINARY_ADD       
             1010  LOAD_CONST               1
             1012  LOAD_FAST                'mean'
             1014  LOAD_DEREF               'data'
             1016  CALL_FUNCTION_1       1  ''
             1018  BINARY_TRUE_DIVIDE
             1020  BUILD_LIST_2          2 
             1022  STORE_FAST               'initial_parameters'
             1024  JUMP_FORWARD       1148  'to 1148'
           1026_0  COME_FROM           972  '972'

 L.2310      1026  LOAD_FAST                'distribution'
             1028  LOAD_STR                 'lognormal'
             1030  COMPARE_OP               ==
         1032_1034  POP_JUMP_IF_FALSE  1078  'to 1078'

 L.2311      1036  LOAD_CONST               0
             1038  LOAD_CONST               ('mean', 'std')
             1040  IMPORT_NAME              numpy
             1042  IMPORT_FROM              mean
             1044  STORE_FAST               'mean'
             1046  IMPORT_FROM              std
             1048  STORE_FAST               'std'
             1050  POP_TOP          

 L.2312      1052  LOAD_DEREF               'log'
             1054  LOAD_DEREF               'data'
             1056  CALL_FUNCTION_1       1  ''
             1058  STORE_FAST               'logdata'

 L.2313      1060  LOAD_FAST                'mean'
             1062  LOAD_FAST                'logdata'
             1064  CALL_FUNCTION_1       1  ''
             1066  LOAD_FAST                'std'
             1068  LOAD_FAST                'logdata'
             1070  CALL_FUNCTION_1       1  ''
             1072  BUILD_LIST_2          2 
             1074  STORE_FAST               'initial_parameters'
             1076  JUMP_FORWARD       1148  'to 1148'
           1078_0  COME_FROM          1032  '1032'

 L.2314      1078  LOAD_FAST                'distribution'
             1080  LOAD_STR                 'negative_binomial'
             1082  COMPARE_OP               ==
         1084_1086  POP_JUMP_IF_FALSE  1098  'to 1098'

 L.2315      1088  LOAD_CONST               1
             1090  LOAD_CONST               0.5
             1092  BUILD_LIST_2          2 
             1094  STORE_FAST               'initial_parameters'
             1096  JUMP_FORWARD       1148  'to 1148'
           1098_0  COME_FROM          1084  '1084'

 L.2316      1098  LOAD_FAST                'distribution'
             1100  LOAD_STR                 'gamma'
             1102  COMPARE_OP               ==
         1104_1106  POP_JUMP_IF_FALSE  1148  'to 1148'

 L.2317      1108  LOAD_CONST               0
             1110  LOAD_CONST               ('mean',)
             1112  IMPORT_NAME              numpy
             1114  IMPORT_FROM              mean
             1116  STORE_FAST               'mean'
             1118  POP_TOP          

 L.2318      1120  LOAD_FAST                'n'
             1122  LOAD_GLOBAL              sum
             1124  LOAD_DEREF               'log'
             1126  LOAD_DEREF               'data'
             1128  LOAD_FAST                'xmin'
             1130  BINARY_TRUE_DIVIDE
             1132  CALL_FUNCTION_1       1  ''
             1134  CALL_FUNCTION_1       1  ''
             1136  BINARY_TRUE_DIVIDE
             1138  LOAD_FAST                'mean'
             1140  LOAD_DEREF               'data'
             1142  CALL_FUNCTION_1       1  ''
             1144  BUILD_LIST_2          2 
             1146  STORE_FAST               'initial_parameters'
           1148_0  COME_FROM          1104  '1104'
           1148_1  COME_FROM          1096  '1096'
           1148_2  COME_FROM          1076  '1076'
           1148_3  COME_FROM          1024  '1024'
           1148_4  COME_FROM           964  '964'
           1148_5  COME_FROM           924  '924'
           1148_6  COME_FROM           884  '884'

 L.2320      1148  LOAD_FAST                'search_method'
             1150  LOAD_STR                 'Likelihood'
             1152  COMPARE_OP               ==
         1154_1156  POP_JUMP_IF_FALSE  1592  'to 1592'

 L.2323      1158  LOAD_FAST                'distribution'
             1160  LOAD_STR                 'power_law'
             1162  COMPARE_OP               ==
         1164_1166  POP_JUMP_IF_FALSE  1306  'to 1306'
             1168  LOAD_FAST                'discrete'
         1170_1172  POP_JUMP_IF_TRUE   1306  'to 1306'
             1174  LOAD_FAST                'xmax'
         1176_1178  POP_JUMP_IF_TRUE   1306  'to 1306'
             1180  LOAD_FAST                'alpha'
         1182_1184  POP_JUMP_IF_TRUE   1306  'to 1306'

 L.2324      1186  LOAD_CONST               0
             1188  LOAD_CONST               ('array', 'nan')
             1190  IMPORT_NAME              numpy
             1192  IMPORT_FROM              array
             1194  STORE_FAST               'array'
             1196  IMPORT_FROM              nan
             1198  STORE_FAST               'nan'
             1200  POP_TOP          

 L.2325      1202  LOAD_CONST               1
             1204  LOAD_FAST                'n'

 L.2326      1206  LOAD_GLOBAL              sum
             1208  LOAD_DEREF               'log'
             1210  LOAD_DEREF               'data'
             1212  LOAD_FAST                'xmin'
             1214  BINARY_TRUE_DIVIDE
             1216  CALL_FUNCTION_1       1  ''
             1218  CALL_FUNCTION_1       1  ''
             1220  BINARY_TRUE_DIVIDE
             1222  BINARY_ADD       
             1224  STORE_FAST               'alpha'

 L.2327      1226  LOAD_FAST                'n'
             1228  LOAD_DEREF               'log'
             1230  LOAD_FAST                'alpha'
             1232  LOAD_CONST               1.0
             1234  BINARY_SUBTRACT  
             1236  CALL_FUNCTION_1       1  ''
             1238  BINARY_MULTIPLY  
             1240  LOAD_FAST                'n'
             1242  LOAD_DEREF               'log'
             1244  LOAD_FAST                'xmin'
             1246  CALL_FUNCTION_1       1  ''
             1248  BINARY_MULTIPLY  
             1250  BINARY_SUBTRACT  
             1252  LOAD_FAST                'alpha'
             1254  LOAD_GLOBAL              sum
             1256  LOAD_DEREF               'log'
             1258  LOAD_DEREF               'data'
             1260  LOAD_FAST                'xmin'
             1262  BINARY_TRUE_DIVIDE
             1264  CALL_FUNCTION_1       1  ''
             1266  CALL_FUNCTION_1       1  ''
             1268  BINARY_MULTIPLY  
             1270  BINARY_SUBTRACT  
             1272  STORE_FAST               'loglikelihood'

 L.2328      1274  LOAD_FAST                'loglikelihood'
             1276  LOAD_FAST                'nan'
             1278  COMPARE_OP               ==
         1280_1282  POP_JUMP_IF_FALSE  1288  'to 1288'

 L.2329      1284  LOAD_CONST               0
             1286  STORE_FAST               'loglikelihood'
           1288_0  COME_FROM          1280  '1280'

 L.2330      1288  LOAD_FAST                'array'
             1290  LOAD_FAST                'alpha'
             1292  BUILD_LIST_1          1 
             1294  CALL_FUNCTION_1       1  ''
             1296  STORE_FAST               'parameters'

 L.2331      1298  LOAD_FAST                'parameters'
             1300  LOAD_FAST                'loglikelihood'
             1302  BUILD_TUPLE_2         2 
             1304  RETURN_VALUE     
           1306_0  COME_FROM          1182  '1182'
           1306_1  COME_FROM          1176  '1176'
           1306_2  COME_FROM          1170  '1170'
           1306_3  COME_FROM          1164  '1164'

 L.2332      1306  LOAD_FAST                'distribution'
             1308  LOAD_STR                 'power_law'
             1310  COMPARE_OP               ==
         1312_1314  POP_JUMP_IF_FALSE  1464  'to 1464'
             1316  LOAD_FAST                'discrete'
         1318_1320  POP_JUMP_IF_FALSE  1464  'to 1464'
             1322  LOAD_FAST                'xmax'
         1324_1326  POP_JUMP_IF_TRUE   1464  'to 1464'
             1328  LOAD_FAST                'alpha'
         1330_1332  POP_JUMP_IF_TRUE   1464  'to 1464'
             1334  LOAD_FAST                'estimate_discrete'
         1336_1338  POP_JUMP_IF_FALSE  1464  'to 1464'

 L.2333      1340  LOAD_CONST               0
             1342  LOAD_CONST               ('array', 'nan')
             1344  IMPORT_NAME              numpy
             1346  IMPORT_FROM              array
             1348  STORE_FAST               'array'
             1350  IMPORT_FROM              nan
             1352  STORE_FAST               'nan'
             1354  POP_TOP          

 L.2334      1356  LOAD_CONST               1
             1358  LOAD_FAST                'n'

 L.2335      1360  LOAD_GLOBAL              sum
             1362  LOAD_DEREF               'log'
             1364  LOAD_DEREF               'data'
             1366  LOAD_FAST                'xmin'
             1368  LOAD_CONST               0.5
             1370  BINARY_SUBTRACT  
             1372  BINARY_TRUE_DIVIDE
             1374  CALL_FUNCTION_1       1  ''
             1376  CALL_FUNCTION_1       1  ''
             1378  BINARY_TRUE_DIVIDE
             1380  BINARY_ADD       
             1382  STORE_FAST               'alpha'

 L.2336      1384  LOAD_FAST                'n'
             1386  LOAD_DEREF               'log'
             1388  LOAD_FAST                'alpha'
             1390  LOAD_CONST               1.0
             1392  BINARY_SUBTRACT  
             1394  CALL_FUNCTION_1       1  ''
             1396  BINARY_MULTIPLY  
             1398  LOAD_FAST                'n'
             1400  LOAD_DEREF               'log'
             1402  LOAD_FAST                'xmin'
             1404  CALL_FUNCTION_1       1  ''
             1406  BINARY_MULTIPLY  
             1408  BINARY_SUBTRACT  
             1410  LOAD_FAST                'alpha'
             1412  LOAD_GLOBAL              sum
             1414  LOAD_DEREF               'log'
             1416  LOAD_DEREF               'data'
             1418  LOAD_FAST                'xmin'
             1420  BINARY_TRUE_DIVIDE
             1422  CALL_FUNCTION_1       1  ''
             1424  CALL_FUNCTION_1       1  ''
             1426  BINARY_MULTIPLY  
             1428  BINARY_SUBTRACT  
             1430  STORE_FAST               'loglikelihood'

 L.2337      1432  LOAD_FAST                'loglikelihood'
             1434  LOAD_FAST                'nan'
             1436  COMPARE_OP               ==
         1438_1440  POP_JUMP_IF_FALSE  1446  'to 1446'

 L.2338      1442  LOAD_CONST               0
             1444  STORE_FAST               'loglikelihood'
           1446_0  COME_FROM          1438  '1438'

 L.2339      1446  LOAD_FAST                'array'
             1448  LOAD_FAST                'alpha'
             1450  BUILD_LIST_1          1 
             1452  CALL_FUNCTION_1       1  ''
             1454  STORE_FAST               'parameters'

 L.2340      1456  LOAD_FAST                'parameters'
             1458  LOAD_FAST                'loglikelihood'
             1460  BUILD_TUPLE_2         2 
             1462  RETURN_VALUE     
           1464_0  COME_FROM          1336  '1336'
           1464_1  COME_FROM          1330  '1330'
           1464_2  COME_FROM          1324  '1324'
           1464_3  COME_FROM          1318  '1318'
           1464_4  COME_FROM          1312  '1312'

 L.2343      1464  LOAD_GLOBAL              likelihood_function_generator
             1466  LOAD_FAST                'distribution'
             1468  LOAD_FAST                'discrete'
             1470  LOAD_FAST                'xmin'
             1472  LOAD_FAST                'xmax'
             1474  LOAD_CONST               ('discrete', 'xmin', 'xmax')
             1476  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1478  STORE_DEREF              'likelihood_function'

 L.2346      1480  LOAD_CONST               0
             1482  LOAD_CONST               ('fmin',)
             1484  IMPORT_NAME_ATTR         scipy.optimize
             1486  IMPORT_FROM              fmin
             1488  STORE_FAST               'fmin'
             1490  POP_TOP          

 L.2348      1492  LOAD_FAST                'fmin'

 L.2349      1494  LOAD_CLOSURE             'data'
             1496  LOAD_CLOSURE             'likelihood_function'
             1498  LOAD_CLOSURE             'log'
             1500  BUILD_TUPLE_3         3 
             1502  LOAD_LAMBDA              '<code_object <lambda>>'
             1504  LOAD_STR                 'distribution_fit.<locals>.<lambda>'
             1506  MAKE_FUNCTION_8          'closure'

 L.2350      1508  LOAD_FAST                'initial_parameters'
             1510  LOAD_CONST               1
             1512  LOAD_CONST               False
             1514  LOAD_CONST               ('full_output', 'disp')
             1516  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1518  UNPACK_SEQUENCE_5     5 
             1520  STORE_FAST               'parameters'
             1522  STORE_FAST               'negative_loglikelihood'
             1524  STORE_FAST               'iter'
             1526  STORE_FAST               'funcalls'
             1528  STORE_FAST               'warnflag'

 L.2351      1530  LOAD_FAST                'negative_loglikelihood'
             1532  UNARY_NEGATIVE   
             1534  STORE_FAST               'loglikelihood'

 L.2353      1536  LOAD_FAST                'comparison_alpha'
         1538_1540  POP_JUMP_IF_FALSE  1582  'to 1582'

 L.2354      1542  LOAD_GLOBAL              distribution_compare
             1544  LOAD_DEREF               'data'
             1546  LOAD_STR                 'power_law'
             1548  LOAD_FAST                'comparison_alpha'
             1550  BUILD_LIST_1          1 
             1552  LOAD_FAST                'distribution'
             1554  LOAD_FAST                'parameters'
             1556  LOAD_FAST                'discrete'
             1558  LOAD_FAST                'xmin'
             1560  LOAD_FAST                'xmax'
             1562  CALL_FUNCTION_8       8  ''
             1564  UNPACK_SEQUENCE_2     2 
             1566  STORE_FAST               'R'
             1568  STORE_FAST               'p'

 L.2355      1570  LOAD_FAST                'parameters'
             1572  LOAD_FAST                'loglikelihood'
             1574  LOAD_FAST                'R'
             1576  LOAD_FAST                'p'
             1578  BUILD_TUPLE_4         4 
             1580  RETURN_VALUE     
           1582_0  COME_FROM          1538  '1538'

 L.2357      1582  LOAD_FAST                'parameters'
             1584  LOAD_FAST                'loglikelihood'
             1586  BUILD_TUPLE_2         2 
             1588  RETURN_VALUE     
             1590  JUMP_FORWARD       1620  'to 1620'
           1592_0  COME_FROM          1154  '1154'

 L.2359      1592  LOAD_FAST                'search_method'
             1594  LOAD_STR                 'KS'
             1596  COMPARE_OP               ==
         1598_1600  POP_JUMP_IF_FALSE  1620  'to 1620'

 L.2360      1602  LOAD_GLOBAL              print
             1604  LOAD_STR                 'Not yet supported. Sorry.'
             1606  LOAD_GLOBAL              sys
             1608  LOAD_ATTR                stderr
             1610  LOAD_CONST               ('file',)
             1612  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1614  POP_TOP          

 L.2361      1616  LOAD_CONST               None
             1618  RETURN_VALUE     
           1620_0  COME_FROM          1598  '1598'
           1620_1  COME_FROM          1590  '1590'

Parse error at or near `JUMP_FORWARD' instruction at offset 172


def distribution_compare(data, distribution1, parameters1, distribution2, parameters2, discrete, xmin, xmax, nested=None, **kwargs):
    no_data = False
    if xmax:
        if all((data > xmax) + (data < xmin)):
            no_data = True
    if all(data < xmin):
        no_data = True
    if no_data:
        R = 0
        p = 1
        return (
         R, p)
    likelihood_function1 = likelihood_function_generator(distribution1, discrete, xmin, xmax)
    likelihood_function2 = likelihood_function_generator(distribution2, discrete, xmin, xmax)
    likelihoods1 = likelihood_function1(parameters1, data)
    likelihoods2 = likelihood_function2(parameters2, data)
    if (distribution1 in distribution2 or distribution2) in distribution1:
        if nested is None:
            print('Assuming nested distributions', file=(sys.stderr))
            nested = True
    from numpy import log
    R, p = loglikelihood_ratio(log(likelihoods1), log(likelihoods2), nested=nested, **kwargs)
    return (
     R, p)


def likelihood_function_generator(distribution_name, discrete=False, xmin=1, xmax=None):
    if distribution_name == 'power_law':
        likelihood_function = lambda parameters, data: power_law_likelihoods(data, parameters[0], xmin, xmax, discrete)
    elif distribution_name == 'exponential':
        likelihood_function = lambda parameters, data: exponential_likelihoods(data, parameters[0], xmin, xmax, discrete)
    elif distribution_name == 'stretched_exponential':
        likelihood_function = lambda parameters, data: stretched_exponential_likelihoods(data, parameters[0], parameters[1], xmin, xmax, discrete)
    elif distribution_name == 'truncated_power_law':
        likelihood_function = lambda parameters, data: truncated_power_law_likelihoods(data, parameters[0], parameters[1], xmin, xmax, discrete)
    elif distribution_name == 'lognormal':
        likelihood_function = lambda parameters, data: lognormal_likelihoods(data, parameters[0], parameters[1], xmin, xmax, discrete)
    elif distribution_name == 'negative_binomial':
        likelihood_function = lambda parameters, data: negative_binomial_likelihoods(data, parameters[0], parameters[1], xmin, xmax)
    elif distribution_name == 'gamma':
        likelihood_function = lambda parameters, data: gamma_likelihoods(data, parameters[0], parameters[1], xmin, xmax)
    return likelihood_function


def find_xmin(data, discrete=False, xmax=None, search_method='Likelihood', return_all=False, estimate_discrete=True, xmin_range=None):
    from numpy import sort, unique, asarray, argmin, vstack, arange, sqrt
    if 0 in data:
        print('Value 0 in data. Throwing out 0 values', file=(sys.stderr))
        data = data[(data != 0)]
    if xmax:
        data = data[(data <= xmax)]
    else:
        if not all((data[i] <= data[(i + 1)] for i in range(len(data) - 1))):
            data = sort(data)
        else:
            if xmin_range == 'find' or xmin_range is None:
                possible_xmins = data
            else:
                possible_xmins = data[(data <= max(xmin_range))]
                possible_xmins = possible_xmins[(possible_xmins >= min(xmin_range))]
            xmins, xmin_indices = unique(possible_xmins, return_index=True)
            xmins = xmins[:-1]
            if len(xmins) < 2:
                from sys import float_info
                xmin = 1
                D = 1
                alpha = 0
                loglikelihood = -10 ** float_info.max_10_exp
                n_tail = 1
                noise_flag = True
                Ds = 1
                alphas = 0
                sigmas = 1
                if not return_all:
                    return (xmin, D, alpha, loglikelihood, n_tail, noise_flag)
                return (
                 xmin, D, alpha, loglikelihood, n_tail, noise_flag, xmins, Ds, alphas, sigmas)
                xmin_indices = xmin_indices[:-1]
                if search_method == 'Likelihood':
                    alpha_MLE_function = lambda xmin: distribution_fit(data, 'power_law', xmin=xmin, xmax=xmax, discrete=discrete, search_method='Likelihood', estimate_discrete=estimate_discrete)
                    fits = asarray(list(map(alpha_MLE_function, xmins)))
            elif search_method == 'KS':
                alpha_KS_function = lambda xmin: distribution_fit(data, 'power_law', xmin=xmin, xmax=xmax, discrete=discrete, search_method='KS', estimate_discrete=estimate_discrete)[0]
                fits = asarray(list(map(alpha_KS_function, xmins)))
            params = fits[:, 0]
            alphas = vstack(params)[:, 0]
            loglikelihoods = fits[:, 1]
            ks_function = lambda index: power_law_ks_distance(data, (alphas[index]), (xmins[index]), xmax=xmax, discrete=discrete)
            Ds = asarray(list(map(ks_function, arange(len(xmins)))))
            sigmas = (alphas - 1) / sqrt(len(data) - xmin_indices + 1)
            good_values = sigmas < 0.1
            xmin_max = argmin(good_values)
            if good_values.all():
                min_D_index = argmin(Ds)
                noise_flag = False
            elif xmin_max > 0:
                min_D_index = argmin(Ds[:xmin_max])
                noise_flag = False
            else:
                min_D_index = argmin(Ds)
                noise_flag = True
        xmin = xmins[min_D_index]
        D = Ds[min_D_index]
        alpha = alphas[min_D_index]
        loglikelihood = loglikelihoods[min_D_index]
        n_tail = sum(data >= xmin)
        return return_all or (
         xmin, D, alpha, loglikelihood, n_tail, noise_flag)
    return (
     xmin, D, alpha, loglikelihood, n_tail, noise_flag, xmins, Ds, alphas, sigmas)


def power_law_ks_distance(data, alpha, xmin, xmax=None, discrete=False, kuiper=False):
    from numpy import arange, sort, mean
    data = data[(data >= xmin)]
    if xmax:
        data = data[(data <= xmax)]
    n = float(len(data))
    if n < 2:
        if kuiper:
            return (1, 1, 2)
        return 1
    if not all((data[i] <= data[(i + 1)] for i in arange(n - 1))):
        data = sort(data)
    if not discrete:
        Actual_CDF = arange(n) / n
        Theoretical_CDF = 1 - (data / xmin) ** (-alpha + 1)
    if discrete:
        from scipy.special import zeta
        if xmax:
            bins, Actual_CDF = cumulative_distribution_function(data, xmin=xmin, xmax=xmax)
            Theoretical_CDF = 1 - (zeta(alpha, bins) - zeta(alpha, xmax + 1)) / (zeta(alpha, xmin) - zeta(alpha, xmax + 1))
        if not xmax:
            bins, Actual_CDF = cumulative_distribution_function(data, xmin=xmin)
            Theoretical_CDF = 1 - zeta(alpha, bins) / zeta(alpha, xmin)
    D_plus = max(Theoretical_CDF - Actual_CDF)
    D_minus = max(Actual_CDF - Theoretical_CDF)
    Kappa = 1 + mean(Theoretical_CDF - Actual_CDF)
    if kuiper:
        return (D_plus, D_minus, Kappa)
    D = max(D_plus, D_minus)
    return D


def power_law_likelihoods(data, alpha, xmin, xmax=False, discrete=False):
    if alpha < 0:
        from numpy import tile
        from sys import float_info
        return tile(10 ** float_info.min_10_exp, len(data))
        xmin = float(xmin)
        data = data[(data >= xmin)]
        if xmax:
            data = data[(data <= xmax)]
    else:
        if not discrete:
            likelihoods = data ** (-alpha) * ((alpha - 1) * xmin ** (alpha - 1))
        if discrete:
            if alpha < 1:
                from numpy import tile
                from sys import float_info
                return tile(10 ** float_info.min_10_exp, len(data))
            if not xmax:
                from scipy.special import zeta
                likelihoods = data ** (-alpha) / zeta(alpha, xmin)
            if xmax:
                from scipy.special import zeta
                likelihoods = data ** (-alpha) / (zeta(alpha, xmin) - zeta(alpha, xmax + 1))
    from sys import float_info
    likelihoods[likelihoods == 0] = 10 ** float_info.min_10_exp
    return likelihoods


def negative_binomial_likelihoods(data, r, p, xmin=0, xmax=False):
    xmin = float(xmin)
    data = data[(data >= xmin)]
    if xmax:
        data = data[(data <= xmax)]
    from numpy import asarray
    from scipy.misc import comb
    pmf = lambda k: comb(k + r - 1, k) * (1 - p) ** r * p ** k
    likelihoods = asarray(list(map(pmf, data))).flatten()
    if xmin != 0 or xmax:
        xmax = max(data)
        from numpy import arange
        normalization_constant = sum(list(map(pmf, arange(xmin, xmax + 1))))
        likelihoods = likelihoods / normalization_constant
    from sys import float_info
    likelihoods[likelihoods == 0] = 10 ** float_info.min_10_exp
    return likelihoods


def exponential_likelihoods(data, Lambda, xmin, xmax=False, discrete=False):
    if Lambda < 0:
        from numpy import tile
        from sys import float_info
        return tile(10 ** float_info.min_10_exp, len(data))
        data = data[(data >= xmin)]
        if xmax:
            data = data[(data <= xmax)]
    else:
        from numpy import exp
        if not discrete:
            likelihoods = Lambda * exp(Lambda * (xmin - data))
        if discrete:
            if not xmax:
                likelihoods = exp(-Lambda * data) * (1 - exp(-Lambda)) * exp(Lambda * xmin)
            if xmax:
                likelihoods = exp(-Lambda * data) * (1 - exp(-Lambda)) / (exp(-Lambda * xmin) - exp(-Lambda * (xmax + 1)))
    from sys import float_info
    likelihoods[likelihoods == 0] = 10 ** float_info.min_10_exp
    return likelihoods


def stretched_exponential_likelihoods(data, Lambda, beta, xmin, xmax=False, discrete=False):
    if Lambda < 0:
        from numpy import tile
        from sys import float_info
        return tile(10 ** float_info.min_10_exp, len(data))
        data = data[(data >= xmin)]
        if xmax:
            data = data[(data <= xmax)]
    else:
        from numpy import exp
        if not discrete:
            likelihoods = data ** (beta - 1) * beta * Lambda * exp(Lambda * (xmin ** beta - data ** beta))
        if discrete:
            if not xmax:
                xmax = max(data)
            if xmax:
                from numpy import arange
                X = arange(xmin, xmax + 1)
                PDF = X ** (beta - 1) * beta * Lambda * exp(Lambda * (xmin ** beta - X ** beta))
                PDF = PDF / sum(PDF)
                likelihoods = PDF[(data - xmin).astype(int)]
    from sys import float_info
    likelihoods[likelihoods == 0] = 10 ** float_info.min_10_exp
    return likelihoods


def gamma_likelihoods(data, k, theta, xmin, xmax=False, discrete=False):
    if not k <= 0:
        if theta <= 0:
            from numpy import tile
            from sys import float_info
            return tile(10 ** float_info.min_10_exp, len(data))
        data = data[(data >= xmin)]
        if xmax:
            data = data[(data <= xmax)]
    else:
        from numpy import exp
        from mpmath import gammainc
        if not discrete:
            likelihoods = data ** (k - 1) / (exp(data / theta) * theta ** k * float(gammainc(k)))
            normalization_constant = 1 - float(gammainc(k, 0, (xmin / theta), regularized=True))
            likelihoods = likelihoods / normalization_constant
        if discrete:
            if not xmax:
                xmax = max(data)
            if xmax:
                from numpy import arange
                X = arange(xmin, xmax + 1)
                PDF = X ** (k - 1) / (exp(X / theta) * theta ** k * float(gammainc(k)))
                PDF = PDF / sum(PDF)
                likelihoods = PDF[(data - xmin).astype(int)]
    from sys import float_info
    likelihoods[likelihoods == 0] = 10 ** float_info.min_10_exp
    return likelihoods


def truncated_power_law_likelihoods(data, alpha, Lambda, xmin, xmax=False, discrete=False):
    if alpha < 0 or Lambda < 0:
        from numpy import tile
        from sys import float_info
        return tile(10 ** float_info.min_10_exp, len(data))
    else:
        data = data[(data >= xmin)]
        if xmax:
            data = data[(data <= xmax)]
        from numpy import exp
        if not discrete:
            from mpmath import gammainc
            likelihoods = Lambda ** (1 - alpha) / (data ** alpha * exp(Lambda * data) * gammainc(1 - alpha, Lambda * xmin)).astype(float)
        if discrete:
            if not xmax:
                xmax = max(data)
            if xmax:
                from numpy import arange
                X = arange(xmin, xmax + 1)
                PDF = X ** (-alpha) * exp(-Lambda * X)
                PDF = PDF / sum(PDF)
                likelihoods = PDF[(data - xmin).astype(int)]
    from sys import float_info
    likelihoods[likelihoods == 0] = 10 ** float_info.min_10_exp
    return likelihoods


def lognormal_likelihoods(data, mu, sigma, xmin, xmax=False, discrete=False):
    from numpy import log
    if sigma <= 0 or mu < log(xmin):
        from numpy import tile
        from sys import float_info
        return tile(10 ** float_info.min_10_exp, len(data))
    data = data[(data >= xmin)]
    if xmax:
        data = data[(data <= xmax)]
    if not discrete:
        from numpy import sqrt, exp
        from scipy.special import erfc
        from scipy.constants import pi
        likelihoods = 1.0 / data * exp(-(log(data) - mu) ** 2 / (2 * sigma ** 2)) * sqrt(2 / (pi * sigma ** 2)) / erfc((log(xmin) - mu) / (sqrt(2) * sigma))
    if discrete:
        if not xmax:
            xmax = max(data)
        if xmax:
            from numpy import arange, exp
            X = arange(xmin, xmax + 1)
            PDF = 1.0 / X * exp(-(log(X) - mu) ** 2 / (2 * sigma ** 2))
            PDF = (PDF / sum(PDF)).astype(float)
            likelihoods = PDF[(data - xmin).astype(int)]
    from sys import float_info
    likelihoods[likelihoods == 0] = 10 ** float_info.min_10_exp
    return likelihoods