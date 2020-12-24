# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/PyCausality/TransferEntropy.py
# Compiled at: 2018-12-23 18:29:16
# Size of source mod 2**32: 27253 bytes
import pandas as pd, statsmodels.api as sm, numpy as np
from copy import deepcopy
from dateutil.relativedelta import relativedelta
import warnings
from .Utils.Utils import *

class LaggedTimeSeries:
    """LaggedTimeSeries"""

    def __init__(self, df, lag=None, max_lag_only=True, window_size=None, window_stride=None):
        """
        Args:
            df              -   Pandas DataFrame object of N columns. Must be indexed as an increasing 
                                time series (i.e. past-to-future), with equal timesteps between each row
            lags            -   The number of steps to be included. Each increase in Lags will result 
                                in N additional columns, where N is the number of columns in the original 
                                dataframe. It will also remove the first N rows.
            max_lag_only    -   Defines whether the returned dataframe contains all lagged timeseries up to 
                                and including the defined lag, or only the time series equal to this lag value
            window_size     -   Dict containing key-value pairs only from within: {'YS':0,'MS':0,'D':0,'H':0,'min':0,'S':0,'ms':0}
                                Describes the desired size of each window, provided the data is indexed with datetime type. Leave as
                                None for no windowing. Units follow http://pandas.pydata.org/pandas-docs/stable/timeseries.html#timeseries-offset-aliases
            window_stride   -   Dict containing key-value pairs only from within: {'YS':0,'MS':0,'D':0,'H':0,'min':0,'S':0,'ms':0}
                                Describes the size of the step between consecutive windows, provided the data is indexed with datetime type. Leave as
                                None for no windowing. Units follow http://pandas.pydata.org/pandas-docs/stable/timeseries.html#timeseries-offset-aliases
                       
        Returns:    -   n/a
        """
        self.df = sanitise(df)
        self.axes = list(self.df.columns.values)
        self.max_lag_only = max_lag_only
        if lag is not None:
            self.t = lag
            self.df = self.__apply_lags__()
        elif window_size is not None and window_stride is not None:
            self.has_windows = True
            self.__apply_windows__(window_size, window_stride)
        else:
            self.has_windows = False

    def __apply_lags__(self):
        """
        Args:
            n/a
        Returns:
            new_df.iloc[self.t:]    -   This is a new dataframe containing the original columns and
                                        all lagged columns. Note that the first few rows (equal to self.lag) will
                                        be removed from the top, since lagged values are of coursenot available
                                        for these indexes.
        """
        new_df = self.df.copy(deep=True).dropna()
        col_names = self.df.columns.values.tolist()
        if self.max_lag_only == True:
            for col_name in col_names:
                new_df[col_name + '_lag' + str(self.t)] = self.df[col_name].shift(self.t)

        else:
            if self.max_lag_only == False:
                for col_name in col_names:
                    for t in range(1, self.t + 1):
                        new_df[col_name + '_lag' + str(t)] = self.df[col_name].shift(t)

            else:
                raise ValueError('Error')
        return new_df.iloc[self.t:]

    def __apply_windows__(self, window_size, window_stride):
        """
        Args:
            window_size      -   Dict passed from self.__init__
            window_stride    -   Dict passed from self.__init__
        Returns:    
            n/a              -   Sets the daterange for the self.windows property to iterate along
        """
        self.window_size = {'YS':0, 
         'MS':0,  'D':0,  'H':0,  'min':0,  'S':0,  'ms':0}
        self.window_stride = {'YS':0,  'MS':0,  'D':0,  'H':0,  'min':0,  'S':0,  'ms':0}
        self.window_stride.update(window_stride)
        self.window_size.update(window_size)
        freq = ''
        daterangefreq = freq.join([str(v) + str(k) for k, v in self.window_stride.items() if v != 0])
        self.daterange = pd.date_range((self.df.index.min()), (self.df.index.max()), freq=daterangefreq)

    def date_diff(self, window_size):
        """
        Args: 
            window_size     -    Dict passed from self.windows function
        Returns:
            start_date      -    The start date of the proposed window
            end_date        -    The end date of the proposed window    
        
        This function is TBC - proposed due to possible duplication of the relativedelta usage in self.windows and self.headstart
        """
        pass

    @property
    def windows(self):
        """
        Args: 
            n/a
        Returns:
            windows         -   Generator defining a pandas DataFrame for each window of the data. 
                                Usage like:   [window for window in LaggedTimeSeries.windows]
        """
        if self.has_windows == False:
            return self.df
        for i, dt in enumerate(self.daterange):
            if dt - relativedelta(years=(self.window_size['YS']), months=(self.window_size['MS']),
              days=(self.window_size['D']),
              hours=(self.window_size['H']),
              minutes=(self.window_size['min']),
              seconds=(self.window_size['S']),
              microseconds=(self.window_size['ms'])) >= self.df.index.min():
                yield self.df.loc[dt - relativedelta(years=(self.window_size['YS']), months=(self.window_size['MS']),
                  days=(self.window_size['D']),
                  hours=(self.window_size['H']),
                  minutes=(self.window_size['min']),
                  seconds=(self.window_size['S']),
                  microseconds=(self.window_size['ms'])):dt]

    @property
    def headstart(self):
        """
        Args: 
            n/a
        Returns:
            len(windows)    -   The number of windows which would have start dates before the desired date range. 
                                Used in TransferEntropy class to slice off incomplete windows.
            
        """
        windows = [i for i, dt in enumerate(self.daterange) if dt - relativedelta(years=(self.window_size['YS']), months=(self.window_size['MS']),
          days=(self.window_size['D']),
          hours=(self.window_size['H']),
          minutes=(self.window_size['min']),
          seconds=(self.window_size['S']),
          microseconds=(self.window_size['ms'])) < self.df.index.min()]
        return len(windows)


class TransferEntropy:
    """TransferEntropy"""

    def __init__(self, DF, endog, exog, lag=None, window_size=None, window_stride=None):
        """
        Args:
            DF            -   (DataFrame) Time series data for X and Y (NOT including lagged variables)
            endog         -   (string)    Fieldname for endogenous (dependent) variable Y
            exog          -   (string)    Fieldname for exogenous (independent) variable X
            lag           -   (integer)   Number of periods (rows) by which to lag timeseries data
            window_size   -   (Dict)      Must contain key-value pairs only from within: {'YS':0,'MS':0,'D':0,'H':0,'min':0,'S':0,'ms':0}
                                          Describes the desired size of each window, provided the data is indexed with datetime type. Leave as
                                          None for no windowing. Units follow http://pandas.pydata.org/pandas-docs/stable/timeseries.html#timeseries-offset-aliases
            window_stride -   (Dict)      Must contain key-value pairs only from within: {'YS':0,'MS':0,'D':0,'H':0,'min':0,'S':0,'ms':0}
                                          Describes the size of the step between consecutive windows, provided the data is indexed with datetime type. Leave as
                                          None for no windowing. Units follow http://pandas.pydata.org/pandas-docs/stable/timeseries.html#timeseries-offset-aliases
        Returns:
            n/a
        """
        self.lts = LaggedTimeSeries(df=(sanitise(DF)), lag=lag,
          window_size=window_size,
          window_stride=window_stride)
        if self.lts.has_windows is True:
            self.df = self.lts.windows
            self.date_index = self.lts.daterange[self.lts.headstart:]
            self.results = pd.DataFrame(index=(self.date_index))
            self.results.index.name = 'windows_ending_on'
        else:
            self.df = [
             self.lts.df]
            self.results = pd.DataFrame(index=[0])
        self.max_lag_only = True
        self.endog = endog
        self.exog = exog
        self.lag = lag
        self.covars = [[], []]
        for i, (X, Y) in enumerate({self.exog: self.endog, self.endog: self.exog}.items()):
            X_lagged = X + '_lag' + str(self.lag)
            Y_lagged = Y + '_lag' + str(self.lag)
            self.covars[i] = [
             np.cov(self.lts.df[[Y, Y_lagged, X_lagged]].values.T),
             np.cov(self.lts.df[[X_lagged, Y_lagged]].values.T),
             np.cov(self.lts.df[[Y, Y_lagged]].values.T),
             np.ones(shape=(1, 1)) * self.lts.df[Y_lagged].std() ** 2]

    def linear_TE(self, df=None, n_shuffles=0):
        """
        Linear Transfer Entropy for directional causal inference

        Defined:            G-causality * 0.5, where G-causality described by the reduction in variance of the residuals
                            when considering side information.
        Calculated using:   log(var(e_joint)) - log(var(e_independent)) where e_joint and e_independent
                            represent the residuals from OLS fitting in the joint (X(t),Y(t)) and reduced (Y(t)) cases

        Arguments:
            n_shuffles  -   (integer)   Number of times to shuffle the dataframe, destroying the time series temporality, in order to 
                                        perform significance testing.
        Returns:
            transfer_entropies  -  (list) Directional Linear Transfer Entropies from X(t)->Y(t) and Y(t)->X(t) respectively
        """
        TEs = []
        shuffled_TEs = []
        p_values = []
        z_scores = []
        for i, df in enumerate(self.df):
            df = deepcopy(df)
            if self.lts.has_windows is True:
                print('Window ending: ', self.date_index[i])
            transfer_entropies = [
             0, 0]
            for i, (X, Y) in enumerate({self.exog: self.endog, self.endog: self.exog}.items()):
                X_lagged = X + '_lag' + str(self.lag)
                Y_lagged = Y + '_lag' + str(self.lag)
                joint_residuals = sm.OLS(df[Y], sm.add_constant(df[[Y_lagged, X_lagged]])).fit().resid
                independent_residuals = sm.OLS(df[Y], sm.add_constant(df[Y_lagged])).fit().resid
                granger_causality = np.log(np.var(independent_residuals) / np.var(joint_residuals))
                transfer_entropies[i] = granger_causality / 2

            TEs.append(transfer_entropies)
            if n_shuffles > 0:
                p, z, TE_mean = significance(df=df, TE=transfer_entropies,
                  endog=(self.endog),
                  exog=(self.exog),
                  lag=(self.lag),
                  n_shuffles=n_shuffles,
                  method='linear')
                shuffled_TEs.append(TE_mean)
                p_values.append(p)
                z_scores.append(z)

        self.add_results({'TE_linear_XY':np.array(TEs)[:, 0],  'TE_linear_YX':np.array(TEs)[:, 1], 
         'p_value_linear_XY':None, 
         'p_value_linear_YX':None, 
         'z_score_linear_XY':0, 
         'z_score_linear_YX':0})
        if n_shuffles > 0:
            self.add_results({'p_value_linear_XY':np.array(p_values)[:, 0],  'p_value_linear_YX':np.array(p_values)[:, 1], 
             'z_score_linear_XY':np.array(z_scores)[:, 0], 
             'z_score_linear_YX':np.array(z_scores)[:, 1], 
             'Ave_TE_linear_XY':np.array(shuffled_TEs)[:, 0], 
             'Ave_TE_linear_YX':np.array(shuffled_TEs)[:, 1]})
        return transfer_entropies

    def nonlinear_TE(self, df=None, pdf_estimator='histogram', bins=None, bandwidth=None, gridpoints=20, n_shuffles=0):
        """
        NonLinear Transfer Entropy for directional causal inference

        Defined:            TE = TE_XY - TE_YX      where TE_XY = H(Y|Y-t) - H(Y|Y-t,X-t)
        Calculated using:   H(Y|Y-t,X-t) = H(Y,Y-t,X-t) - H(Y,Y-t)  and finding joint entropy through density estimation

        Arguments:
            pdf_estimator   -   (string)    'Histogram' or 'kernel' Used to define which method is preferred for density estimation
                                            of the distribution - either histogram or KDE
            bins            -   (dict of lists) Optional parameter to provide hard-coded bin-edges. Dict keys 
                                            must contain names of variables - including lagged columns! Dict values must be lists
                                            containing bin-edge numerical values. 
            bandwidth       -   (float)     Optional parameter for custom bandwidth in KDE. This is a scalar multiplier to the covariance
                                            matrix used (see: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.covariance_factor.html)
            gridpoints      -   (integer)   Number of gridpoints (in each dimension) to discretise the probablity space when performing
                                            integration of the kernel density estimate. Increasing this gives more precision, but significantly
                                            increases execution time
            n_shuffles      -   (integer)   Number of times to shuffle the dataframe, destroying the time series temporality, in order to 
                                            perform significance testing.

        Returns:
            transfer_entropies  -  (list) Directional Transfer Entropies from X(t)->Y(t) and Y(t)->X(t) respectively
        
        (Also stores TE, Z-score and p-values in self.results - for each window if windows defined.)
        """
        self.bins = bins
        if self.bins is None:
            self.bins = {self.endog: None}
        TEs = []
        shuffled_TEs = []
        p_values = []
        z_scores = []
        for i, df in enumerate(self.df):
            df = deepcopy(df)
            if self.lts.has_windows is True:
                print('Window ending: ', self.date_index[i])
            transfer_entropies = [
             0, 0]
            for i, (X, Y) in enumerate({self.exog: self.endog, self.endog: self.exog}.items()):
                X_lagged = X + '_lag' + str(self.lag)
                Y_lagged = Y + '_lag' + str(self.lag)
                H1 = get_entropy(df=(df[[Y, Y_lagged, X_lagged]]), gridpoints=gridpoints,
                  bandwidth=bandwidth,
                  estimator=pdf_estimator,
                  bins={k:v for k, v in self.bins.items() if k in [Y, Y_lagged, X_lagged]},
                  covar=(self.covars[i][0]))
                H2 = get_entropy(df=(df[[X_lagged, Y_lagged]]), gridpoints=gridpoints,
                  bandwidth=bandwidth,
                  estimator=pdf_estimator,
                  bins={k:v for k, v in self.bins.items() if k in [X_lagged, Y_lagged]},
                  covar=(self.covars[i][1]))
                H3 = get_entropy(df=(df[[Y, Y_lagged]]), gridpoints=gridpoints,
                  bandwidth=bandwidth,
                  estimator=pdf_estimator,
                  bins={k:v for k, v in self.bins.items() if k in [Y, Y_lagged]},
                  covar=(self.covars[i][2]))
                H4 = get_entropy(df=(df[[Y_lagged]]), gridpoints=gridpoints,
                  bandwidth=bandwidth,
                  estimator=pdf_estimator,
                  bins={k:v for k, v in self.bins.items() if k in [Y_lagged]},
                  covar=(self.covars[i][3]))
                conditional_entropy_joint = H1 - H2
                conditional_entropy_independent = H3 - H4
                transfer_entropies[i] = conditional_entropy_independent - conditional_entropy_joint

            TEs.append(transfer_entropies)
            if n_shuffles > 0:
                p, z, TE_mean = significance(df=df, TE=transfer_entropies,
                  endog=(self.endog),
                  exog=(self.exog),
                  lag=(self.lag),
                  n_shuffles=n_shuffles,
                  pdf_estimator=pdf_estimator,
                  bins=(self.bins),
                  bandwidth=bandwidth,
                  method='nonlinear')
                shuffled_TEs.append(TE_mean)
                p_values.append(p)
                z_scores.append(z)

        self.add_results({'TE_XY':np.array(TEs)[:, 0],  'TE_YX':np.array(TEs)[:, 1], 
         'p_value_XY':None, 
         'p_value_YX':None, 
         'z_score_XY':0, 
         'z_score_YX':0})
        if n_shuffles > 0:
            self.add_results({'p_value_XY':np.array(p_values)[:, 0],  'p_value_YX':np.array(p_values)[:, 1], 
             'z_score_XY':np.array(z_scores)[:, 0], 
             'z_score_YX':np.array(z_scores)[:, 1], 
             'Ave_TE_XY':np.array(shuffled_TEs)[:, 0], 
             'Ave_TE_YX':np.array(shuffled_TEs)[:, 1]})
        return transfer_entropies

    def add_results(self, dict):
        """
        Args:
            dict    -   JSON-style data to store in existing self.results DataFrame
        Returns:
            n/a
        """
        for k, v in dict.items():
            self.results[str(k)] = v


def significance(df, TE, endog, exog, lag, n_shuffles, method, pdf_estimator=None, bins=None, bandwidth=None, both=True):
    """
        Perform significance analysis on the hypothesis test of statistical causality, for both X(t)->Y(t)
        and Y(t)->X(t) directions
   
        Calculated using:  Assuming stationarity, we shuffle the time series to provide the null hypothesis. 
                           The proportion of tests where TE > TE_shuffled gives the p-value significance level.
                           The amount by which the calculated TE is greater than the average shuffled TE, divided
                           by the standard deviation of the results, is the z-score significance level.

        Arguments:
            TE              -      (list)    Contains the transfer entropy in each direction, i.e. [TE_XY, TE_YX]
            endog           -      (string)  The endogenous variable in the TE analysis being significance tested (i.e. X or Y) 
            exog            -      (string)  The exogenous variable in the TE analysis being significance tested (i.e. X or Y) 
            pdf_estimator   -      (string)  The pdf_estimator used in the original TE analysis
            bins            -      (Dict of lists)  The bins used in the original TE analysis

            n_shuffles      -      (float) Number of times to shuffle the dataframe, destroyig temporality
            both            -      (Bool) Whether to shuffle both endog and exog variables (z-score) or just exog                                  variables (giving z*-score)  
        Returns:
            p_value         -      Probablity of observing the result given the null hypothesis
            z_score         -      Number of Standard Deviations result is from mean (normalised)
        """
    shuffled_TEs = np.zeros(shape=(2, n_shuffles))
    if both is True:
        pass
    for i in range(n_shuffles):
        df = shuffle_series(df)
        shuffled_causality = TransferEntropy(DF=df, endog=endog,
          exog=exog,
          lag=lag)
        if method == 'linear':
            TE_shuffled = shuffled_causality.linear_TE(df, n_shuffles=0)
        else:
            TE_shuffled = shuffled_causality.nonlinear_TE(df, pdf_estimator, bins, bandwidth, n_shuffles=0)
        shuffled_TEs[:, i] = TE_shuffled

    p_values = (
     np.count_nonzero(TE[0] < shuffled_TEs[0, :]) / n_shuffles,
     np.count_nonzero(TE[1] < shuffled_TEs[1, :]) / n_shuffles)
    z_scores = (
     (TE[0] - np.mean(shuffled_TEs[0, :])) / np.std(shuffled_TEs[0, :]),
     (TE[1] - np.mean(shuffled_TEs[1, :])) / np.std(shuffled_TEs[1, :]))
    TE_mean = (
     np.mean(shuffled_TEs[0, :]),
     np.mean(shuffled_TEs[1, :]))
    return (
     p_values, z_scores, TE_mean)