# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/easyexplore/utils.py
# Compiled at: 2020-05-10 17:13:08
# Size of source mod 2**32: 56851 bytes
import geojson, glob, itertools, logging, os, numpy as np, networkx as nx, pandas as pd, psutil, subprocess, zipfile
from .data_import_export import DataExporter, FileUtils
from datetime import datetime
from ipywidgets import FloatProgress
from IPython.display import display, HTML
from itertools import islice
from scipy.stats import anderson, chi2, chi2_contingency, f_oneway, friedmanchisquare, mannwhitneyu, normaltest, kendalltau, kruskal, kstest, pearsonr, powerlaw, shapiro, spearmanr, stats, ttest_ind, ttest_rel, wilcoxon
from statsmodels.stats.weightstats import ztest
from typing import Dict, List, Tuple
INVALID_VALUES: list = [
 'nan', 'NaN', 'NaT', np.nan, 'none', 'None', 'inf', '-inf', np.inf, -np.inf]
PERCENTILES = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
PERCENTILES: List[float]

class EasyExplore:
    __doc__ = '\n\n    Class for handling logging activities\n\n    '

    def __init__(self, log_path: str=None, show_msg: bool=True, show_header: bool=False, show_progress_bar: bool=False, show_ram_usage: bool=True):
        """
        :param log_path: str: Path of the log file
        :param show_msg: bool: Enable and disable message display
        :param show_header: bool: Enable and disable header display
        :param show_progress_bar: bool: Enable and disable progress bar display
        :param show_ram_usage: bool: Enable and disable ram usage display
        """
        self.display = True
        self.data_shape = tuple([None, None])
        self.header_title = ''
        self.show_msg = show_msg
        self.show_header = show_header
        self.show_pb = show_progress_bar
        self.show_ram = show_ram_usage
        self.header = dict(header=dict(id='easyexplore', color='olive',
          font_family='Courier',
          font_size='15px'),
          title=dict(id='easyexplore', color='grey',
          font_family='Courier',
          font_size='15px'))
        self.pb = FloatProgress(value=0.0, min=0,
          max=100.0,
          step=0.1,
          description='EasyExplore',
          bar_style='success',
          orientation='horizontal')
        self.pb_max = 100
        self.log = logging.getLogger(name=__name__)
        self.log.setLevel(level=(logging.DEBUG))
        if log_path is None:
            self.log_path = '{}/log/'.format(os.getcwd().replace('\\', '/'))
        else:
            self.log_path = log_path
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        self.invalid_values = [
         '', 'nan', 'NaN', 'NaT', np.nan, 'none', 'None', None, 'inf', '-inf', np.inf, -np.inf]
        self.perc = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
        self.timestamp_format = '%Y-%m-%d %H:%M:%S'
        self.formatter = {'dev':'%(asctime)s - %(levelname)s - %(message)s',  'stage':'%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s', 
         'prod':'%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'}

    def display_header(self, title: str, data_shape: Tuple[(str, str)]):
        """

        Display header

        :param str title:
        :param Tuple[str, str] data_shape:
        """
        _header = HTML('<p id="{}"><span style="font-size:{};color:{};font-family:{};"><i>EasyExplore</i></span></p>'.format(self.header['header'].get('id'), self.header['header'].get('color'), self.header['header'].get('font_family'), self.header['header'].get('font_size')))
        _title = HTML('<p id="{}"><span style="font-size:{};color:{};font-family:{};">{}</span><span style="font-size:15px;">Cases = {}  |  Features = {}</span></p>'.format(self.header['header'].get('id'), self.header['title'].get('color'), self.header['title'].get('font_family'), self.header['title'].get('font_size'), title, data_shape[0], data_shape[1]))
        display(_title)

    def display_pb(self):
        """

        Display progress bar

        """
        display((self.pb), include=None, exclude=None, metadata=None, transient=None, display_id=None)

    def display_msg(self, msg: str):
        """

        Display messages as HTML widget

        :param str msg: Message to display
        :return:
        """
        _msg = HTML('<p id="{}"><span style="font-size:{};color:{};font-family:{};"><b>{}</b></span></p>'.format(self.header['header'].get('id'), self.header['header'].get('color'), self.header['header'].get('font_family'), self.header['header'].get('font_size'), msg))
        display(_msg)

    def printer(self, msg: str):
        """

        Internal message printer

        """
        if self.show_msg:
            if self.show_ram:
                print('\n{}: RAM usage: {}%: {}\n'.format(datetime.now().strftime(self.timestamp_format), psutil.virtual_memory().percent, msg))
            else:
                print('\n{}: {}\n'.format(datetime.now().strftime(self.timestamp_format), msg))


class Log:
    __doc__ = '\n\n    Class for handling logging\n\n    '

    def __init__(self, write: bool=False, level: str='info', env: str='dev', logger_file_path: str=None, log_ram_usage: bool=True, log_cpu_usage: bool=True):
        """
        :param write: bool
            Write logging file or not

        :param level: str
            Name of the logging level of the messge
                -> info: Logs any information
                -> warn: Logs warnings
                -> error: Logs errors including critical messages

        :param env: str
            Name of the logging environment to use
                -> dev: Development - Logs any information
                -> stage: Staging - Logs only warnings and errors including critical messages
                -> prod: Production - Logs only errors including critical messages

        :param logger_file_path: str
            Complete file path of the logger file

        :param log_ram_usage: bool
            Log RAM usage (in percent) or not

        :param log_cpu_usage: bool
            Log CPU usage (in percent) or not
        """
        self.write = write
        self.timestamp_format = '%Y-%m-%d %H:%M:%S'
        if log_ram_usage:
            self.ram = ' -> RAM {}%'.format(psutil.virtual_memory().percent)
        else:
            self.ram = ''
        if log_cpu_usage:
            self.cpu = ' -> CPU {}%'.format(psutil.cpu_percent(percpu=False))
        else:
            self.cpu = ''
        self.msg = '{}{}{} | '.format(datetime.now().strftime(self.timestamp_format), self.ram, self.cpu)
        if write:
            if logger_file_path is None:
                self.log_file_path = os.path.join(os.getcwd(), 'log.txt')
            else:
                self.log_file_path = logger_file_path
            FileUtils(file_path=(self.log_file_path), create_dir=True).make_dir()
        else:
            self.log_file_path = None
        self.levels = [
         'info', 'warn', 'error']
        _env = dict(dev=0, stage=1, prod=2)
        if env in _env.keys():
            self.env = _env.get(env)
        else:
            self.env = _env.get('dev')
        if level in self.levels:
            self.level = self.levels.index(level)
        else:
            self.level = 0

    def _write(self):
        """
        Write log file

        """
        with open(file=(self.log_file_path), mode='a', encoding='utf-8') as (_log):
            _log.write('{}\n'.format(self.msg))

    def log(self, msg: str):
        """
        Log message

        :param msg: str
            Message to log
        """
        if self.level >= self.env:
            if self.level == 0:
                _level_description = ''
            else:
                if self.level == 1:
                    _level_description = 'WARNING: '
                else:
                    if self.level == 2:
                        _level_description = 'ERROR: '
                self.msg = '{}{}'.format(self.msg, msg)
                if self.write:
                    self._write()
                else:
                    print(self.msg)


class StatsUtils:
    __doc__ = '\n\n    Class for calculating univariate and multivariate statistics\n\n    '

    def __init__(self, data: pd.DataFrame, features: List[str]):
        """
        :param data:
        :param features:
        """
        self.data_set = data
        self.features = features
        self.nan_policy = 'omit'

    def _anderson_darling_test(self, feature: str, sig_level: float=0.05) -> float:
        """

        Anderson-Darling test for normality tests

        :param feature:
        :param sig_level:
        :return: float: Probability describing significance level
        """
        _stat = anderson(x=(self.data_set[feature]), dist='norm')
        try:
            _i = _stat.significance_level.tolist().index(100 * sig_level)
            p = _stat.critical_values[_i]
        except ValueError:
            p = _stat.critical_values[2]

        return p

    def _bartlette_sphericity_test(self) -> dict:
        """

        Bartlette's test for sphericity

        """
        _n_cases, _n_features = self.data_set.shape
        _cor = self.data_set[self.features].corr('pearson')
        _cor_det = np.linalg.det(_cor.values)
        _statistic = -np.log(_cor_det) * (_n_cases - 1 - (2 * _n_features + 5) / 6)
        _dof = _n_features * (_n_features - 1) / 2
        return dict(statistic=_statistic, p=(chi2.pdf(_statistic, _dof)))

    def _dagostino_k2_test(self, feature: str) -> float:
        """

        D'Agostino K² test for normality

        :param feature: String containing the name of the feature
        :return: Float indicating the statistical probability value (p-value)
        """
        stat, p = normaltest(a=(self.data_set[feature]), axis=0, nan_policy='propagate')
        return p

    def _kaiser_meyer_olkin_test(self) -> dict:
        """

        Kaiser-Meyer-Olkin test for unobserved features

        """
        _cor = self.correlation(meth='pearson').values
        _partial_cor = self.correlation(meth='partial').values
        np.fill_diagonal(_cor, 0)
        np.fill_diagonal(_partial_cor, 0)
        _cor = _cor ** 2
        _partial_cor = _partial_cor ** 2
        _cor_sum = np.sum(_cor)
        _partial_cor_sum = np.sum(_partial_cor)
        _cor_sum_feature = np.sum(_cor, axis=0)
        _partial_cor_sum_feature = np.sum(_partial_cor, axis=0)
        return dict(kmo=(_cor_sum / (_cor_sum + _partial_cor_sum)), kmo_per_feature=(_cor_sum_feature / (_cor_sum_feature + _partial_cor_sum_feature)))

    def _shapiro_wilk_test(self, feature: str) -> float:
        """

        Shapiro-Wilk test for normality tests

        :param feature: String containing the name of the feature
        :return: Float indicating the statistical probability value (p-value)
        """
        return shapiro(x=(self.data_set[feature]))

    def curtosis_test(self) -> List[str]:
        """

        Test whether a distribution is tailed or not

        :return: List of strings containing the names of the tailed features
        """
        raise UtilsException('Method not supported yet')

    def correlation(self, meth: str='pearson', min_obs: int=1) -> pd.DataFrame:
        """

        Calculate correlation coefficients

        :param meth: String containing the method to be used as correlation coefficient
                        -> pearson: Marginal Correlation based on Pearson's r
                        -> kendall: Rank Correlation based on Kendall
                        -> spearman: Rank Correlation based on Spearman
                        -> partial: Partial Correlation
        :param min_obs: Integer indicating the minimum amount of valid observations
        :return: Pandas DataFrame containing the correlation matrix
        """
        if meth in ('pearson', 'kendall', 'spearman'):
            _cor = self.data_set[self.features].corr(method=meth, min_periods=min_obs)
        else:
            if meth == 'partial':
                if self.data_set.shape[0] - self.data_set.isnull().astype(dtype=int).sum().sum() > 0:
                    _cov = np.cov(m=(self.data_set[self.features].dropna()))
                    try:
                        assert np.linalg.det(_cov) > np.finfo(np.float32).eps
                        _inv_var_cov = np.linalg.inv(_cov)
                    except AssertionError:
                        _inv_var_cov = np.linalg.pinv(_cov)

                    _std = np.sqrt(np.diag(_inv_var_cov))
                    _cov2cor = _inv_var_cov / np.outer(_std, _std)
                    _cor = pd.DataFrame(data=(np.nan_to_num(x=_cov2cor, copy=True) * -1), columns=(self.features),
                      index=(self.features))
                else:
                    _cor = pd.DataFrame()
                    Log(write=False, level='info').log(msg='Can not calculate coefficients for partial correlation because of the high missing data rate')
            else:
                raise UtilsException('Method for calculating correlation coefficient ({}) not supported'.format(meth))
        return _cor

    def correlation_test(self, x: str, y: str, meth: str='pearson', freq_table: List[float]=None, yates_correction: bool=True, power_divergence: str='cressie_read') -> dict:
        """
        :param x:
        :param y:
        :param meth: String defining the hypothesis test method for correlation
                        -> pearson:
                        -> spearman:
                        -> kendall:
                        -> chi-squared:
        :param freq_table:
        :param yates_correction:
        :param power_divergence: String defining the power divergence test method used in chi-squared independent test
                                    -> pearson: Pearson's chi-squared statistic
                                    -> log-likelihood: Log-Likelihood ratio (G-test)
                                    -> freeman-tukey: Freeman-tukey statistic
                                    -> mod-log-likelihood: Modified log-likelihood ratio
                                    -> neyman: Neyman's statistic
                                    -> cressie-read: Cressie-Read power divergence test statistic
        :return:
        """
        _reject = None
        if meth == 'pearson':
            _correlation_test = pearsonr(x=(self.data_set[x]), y=(self.data_set[y]))
        else:
            if meth == 'spearman':
                _correlation_test = spearmanr(a=(self.data_set[x]), b=(self.data_set[y]), axis=0, nan_policy=(self.nan_policy))
            else:
                if meth == 'kendall':
                    _correlation_test = kendalltau(x=(self.data_set[x]), y=(self.data_set[y]), nan_policy=(self.nan_policy))
                else:
                    if meth == 'chi-squared':
                        _correlation_test = chi2_contingency(observed=freq_table, correction=yates_correction, lambda_=power_divergence)
                    else:
                        raise UtilsException('Method for correlation test not supported')
            if _correlation_test[1] <= self.p:
                _reject = False
            else:
                _reject = True
        return {'feature':''.join(self.data_set.keys()), 
         'cases':len(self.data_set.values), 
         'test_statistic':_correlation_test[0], 
         'p_value':_correlation_test[1], 
         'reject':_reject}

    def factoriability_test(self, meth: str='kmo') -> dict:
        """

        Test whether a data set contains unobserved features required for factor analysis

        :param meth: String containing the name of the used method
                        -> kmo: Kaiser-Meyer-Olkin Criterion
                        -> bartlette: Bartlette's test of sphericity
        """
        _fac = {}
        if meth == 'kmo':
            pass
        else:
            if meth == 'bartlette':
                pass
            else:
                raise UtilsException('Method for testing "factoriability" ({}) not supported'.format(meth))
            return {}

    def non_parametric_test(self, x: str, y: str, meth: str='kruskal-wallis', continuity_correction: bool=True, alternative: str='two-sided', zero_meth: str='pratt', *args):
        """
        :param x:
        :param y:
        :param meth: String defining the hypothesis test method for non-parametric tests
                        -> kruskal-wallis: Kruskal-Wallis H test to test whether the distributions of two or more
                                           independent samples are equal or not
                        -> mann-whitney: Mann-Whitney U test to test whether the distributions of two independent
                                         samples are equal or not
                        -> wilcoxon: Wilcoxon Signed-Rank test for test whether the distributions of two paired samples
                                     are equal or not
                        -> friedman: Friedman test for test whether the distributions of two or more paired samples
                                     are equal or not
        :param continuity_correction:
        :param alternative: String defining the type of hypothesis test
                            -> two-sided:
                            -> less:
                            -> greater:
        :param zero_meth: String defining the method to handle zero differences in the ranking process (Wilcoxon test)
                            -> pratt: Pratt treatment that includes zero-differences (more conservative)
                            -> wilcox: Wilcox tratment that discards all zero-differences
                            -> zsplit: Zero rank split, just like Pratt, but spliting the zero rank between positive
                                       and negative ones
        :param args:
        :return:
        """
        _reject = None
        if meth == 'kruskal-wallis':
            _non_parametric_test = kruskal(args, self.nan_policy)
        else:
            if meth == 'mann-whitney':
                _non_parametric_test = mannwhitneyu(x=(self.data_set[x]), y=(self.data_set[y]),
                  use_continuity=continuity_correction,
                  alternative=alternative)
            else:
                if meth == 'wilcoxon':
                    _non_parametric_test = wilcoxon(x=(self.data_set[x]), y=(self.data_set[y]),
                      zero_method=zero_meth,
                      correction=continuity_correction)
                else:
                    if meth == 'friedman':
                        _non_parametric_test = friedmanchisquare(args)
                    else:
                        raise ValueError('No non-parametric test found !')
            if _non_parametric_test[1] <= self.p:
                _reject = False
            else:
                _reject = True
        return {'feature':''.join(self.data_set.keys()), 
         'cases':len(self.data_set.values), 
         'test_statistic':_non_parametric_test[0], 
         'p_value':_non_parametric_test[1], 
         'reject':_reject}

    def normality_test(self, alpha: float=0.05, meth: str='shapiro-wilk') -> dict:
        """

        Test whether a distribution is normal distributed or not

        :param alpha: Float indicating the threshold that indicates whether a hypothesis can be rejected or not
        :param meth: String containing the method to test normality
                        -> shapiro-wilk:
                        -> anderson-darling:
                        -> dagostino:
        :return: dict: Results of normality test (statistic, p-value, p > alpha)
        """
        _alpha = alpha
        _normality = {}
        for feature in self.features:
            if meth == 'shapiro-wilk':
                _stat, _p = self._shapiro_wilk_test(feature=feature)
            else:
                if meth == 'anderson-darling':
                    _stat, _p = self._anderson_darling_test(feature=feature, sig_level=alpha)
                else:
                    if meth == 'dagostino':
                        _stat, _p = self._dagostino_k2_test(feature=feature)
                    else:
                        raise UtilsException('Method ({}) for testing normality not supported'.format(meth))
            _normality.update({feature: dict(stat=_stat, p=_p, normality=(_p > _alpha))})

        return _normality

    def parametric_test(self, x: str, y: str, meth: str='t-test', welch_t_test: bool=True, *args):
        """
        :param x:
        :param y:
        :param meth: String defining the hypothesis test method for parametric tests
                        -> z-test:
                        -> t-test:
                        -> t-test-paired:
                        -> anova:
        :param welch_t_test:
        :param args: Arguments containing samples from two or more groups for anova test
        :return:
        """
        _reject = None
        if meth == 't-test':
            _parametric_test = ttest_ind(a=(self.data_set[x]), b=(self.data_set[y]), axis=0,
              equal_var=(not welch_t_test),
              nan_policy=(self.nan_policy))
        else:
            if meth == 't-test-paired':
                _parametric_test = ttest_rel(a=(self.data_set[x]), b=(self.data_set[y]), axis=0, nan_policy=(self.nan_policy))
            else:
                if meth == 'anova':
                    _parametric_test = f_oneway(args)
                else:
                    if meth == 'z-test':
                        _parametric_test = ztest(x1=x, x2=y, value=0, alternative='two-sided', usevar='pooled', ddof=1)
                    else:
                        raise ValueError('No parametric test found !')
            if _parametric_test[1] <= self.p:
                _reject = False
            else:
                _reject = True
        return {'feature':''.join(self.data_set.keys()), 
         'cases':len(self.data_set.values), 
         'test_statistic':_parametric_test[0], 
         'p_value':_parametric_test[1], 
         'reject':_reject}

    def power_law_test(self, tail_prob: List[float]=None, shape_params: List[float]=None, location_params: List[float]=None, size: Tuple[int]=None, moments: str='mvsk'):
        """
        :param tail_prob:
        :param shape_params:
        :param location_params:
        :param size:
        :param moments:
        :return:
        """
        raise UtilsException('Method not implemented yet :-(')

    def skewness_test(self, axis: str='col', threshold_interval: Tuple[(float, float)]=(-0.5, 0.5)) -> dict:
        """

        Test whether a distribution is skewed or not

        :param axis: String containing the name of the axis of the data frame to use
                        -> col: Test skewness of feature
                        -> row: test skewness of cases
        :param threshold_interval: Tuple of floats indicating the threshold interval for testing
        :return: List of strings containing the name of the skewed features
        """
        if axis == 'col':
            _axis = 0
        else:
            if axis == 'row':
                _axis = 1
            else:
                raise UtilsException('Axis ({}) not supported'.format(axis))
        return self.data_set[self.features].skew(axis=_axis).to_dict()


class UtilsException(Exception):
    __doc__ = '\n\n    Class for setting up exceptions for class Utils\n\n    '


class Utils:
    __doc__ = '\n\n    Class for applying general utility methods\n\n    '

    def __init__(self):
        """
        """
        pass

    @staticmethod
    def check_dtypes(df: pd.DataFrame, date_edges: Tuple[(str, str)]=None) -> dict:
        """
        Check if data types of Pandas DataFrame match with the analytical measurement of data

        Parameters
        ----------
        df: pd.DataFrame
            Data set

        date_edges: Tuple[str, str]

        Returns
        -------
        dict: Data type conversion recommendation
        """
        _typing = dict(meta={}, conversion={})
        _features = list(df.keys())
        _dtypes = [str(dt) for dt in df.dtypes.tolist()]
        _feature_types = Utils().get_feature_types(df=df, features=_features,
          dtypes=(df.dtypes.tolist()),
          date_edges=date_edges)
        _table = {'feature_type':[],  'data_type':[],  'rec':[]}
        for i in range(0, len(_features), 1):
            if any(df[_features[i]].isnull()):
                if len(df[_features[i]].unique()) == 1:
                    _typing['meta'].update({_features[i]: dict(data_type='unknown', feature_type='float',
                                     rec='Drop feature (no valid data)')})
                    continue
            if str(_dtypes[i]).find('bool') >= 0:
                _typing['meta'].update({_features[i]: dict(data_type='categorical', feature_type='bool',
                                 rec='Convert to integer')})
                _typing['conversion'].update({_features[i]: 'int'})
            elif str(_dtypes[i]).find('float') >= 0:
                if _features[i] in _feature_types.get('date'):
                    _typing['meta'].update({_features[i]: dict(data_type='date', feature_type='float',
                                     rec='Convert to datetime')})
                    _typing['conversion'].update({_features[i]: 'date'})
                else:
                    if _features[i] in _feature_types.get('ordinal'):
                        _typing['meta'].update({_features[i]: dict(data_type='categorical', feature_type='float',
                                         rec='Convert to integer')})
                        _typing['conversion'].update({_features[i]: 'int'})
                    else:
                        if _features[i] in _feature_types.get('continuous'):
                            if any(df[_features[i]].isnull()):
                                _typing['meta'].update({_features[i]: dict(data_type='continuous', feature_type='float',
                                                 rec='Handle missing data')})
                        else:
                            _typing['meta'].update({_features[i]: dict(data_type='categorical', feature_type='float')})
                            _typing['conversion'].update({_features[i]: 'int'})
                            if _features[i] in _feature_types.get('categorical'):
                                if any(df[_features[i]].isnull()):
                                    _typing['meta'][_features[i]].update({'rec': 'Handle missing data and convert to integer'})
                                else:
                                    _typing['meta'][_features[i]].update({'rec': 'Convert to integer'})
            elif str(_dtypes[i]).find('int') >= 0:
                if _features[i] not in _feature_types.get('categorical'):
                    _typing['meta'][_features[i]].update({_features[i]: dict(feature_type='int')})
                    if _features[i] in _feature_types.get('ordinal'):
                        continue
                    else:
                        if _features[i] in _feature_types.get('date'):
                            _typing['meta'].update({_features[i]: dict(data_type='date', rec='Convert to datetime')})
                            _typing['conversion'].update({_features[i]: 'date'})
                        elif _features[i] in _feature_types.get('text'):
                            pass
                        _typing['meta'].update({_features[i]: dict(data_type='text', rec='Convert to string')})
                        _typing['conversion'].update({_features[i]: 'str'})
            else:
                if str(_dtypes[i]).find('object') >= 0:
                    if _features[i] in _feature_types.get('date'):
                        _typing['meta'].update({_features[i]: dict(data_type='date', feature_type='text',
                                         rec='Convert to datetime')})
                        _typing['conversion'].update({_features[i]: 'date'})
                    else:
                        if _features[i] in _feature_types.get('continuous'):
                            _typing['meta'].update({_features[i]: dict(data_type='continuous', feature_type='text')})
                            _typing['conversion'].update({_features[i]: 'float'})
                            if any(df[_features[i]].isnull()):
                                _typing['meta'][_features[i]].update({'rec': 'Handle missing data and convert to float'})
                            else:
                                _typing['meta'][_features[i]].update({'rec': 'Convert to float'})
                        elif _features[i] in _feature_types.get('categorical') or _features[i] in _feature_types.get('ordinal'):
                            _typing['meta'].update({_features[i]: dict(data_type='categorical', feature_type='text')})
                            _typing['conversion'].update({_features[i]: 'int'})
                            if any(df[_features[i]].isnull()):
                                _typing['meta'][_features[i]].update({'rec': 'Handle missing data and convert to integer by label encoding'})
                            else:
                                _typing['meta'][_features[i]].update({'rec': 'Convert to integer by label encoding'})

        return _typing

    @staticmethod
    def convert_jupyter(notebook_name: str, to: str='html'):
        """

        Convert Jupyter Notebook into several formats

        :param notebook_name: str: Name of the jupyter notebook
        :param to: str: Output format
                        -> html: HTML
                        -> pdf: PDF
                        -> latex: Latex
                        -> markdown: Markdown
                        -> rst: reStructuredText
                        -> script: Python / Julia / R script (depending on kernel settings of ipynb file)
        """
        subprocess.run('jupyter nbconvert "{}" --to {}'.format(notebook_name, to))

    @staticmethod
    def extract_tuple_el_in_list(list_of_tuples: List[tuple], tuple_pos: int) -> list:
        """

        Extract specific tuple elements from list of tuples

        :param list_of_tuples: List[tuple]: List of tuples
        :param tuple_pos: int: Position of element in tuples to extract
        :return: list: List of elements of tuple
        """
        if tuple_pos < 0:
            raise UtilsException('Position of element in tuple cannot be negative ({})'.format(tuple_pos))
        return next(islice(zip(*list_of_tuples), tuple_pos, None))

    @staticmethod
    def freedman_diaconis_bins(data_points: np.array) -> int:
        """

        Calculate the width of each bin by using Freedmann-Diaconis rule

        :param data_points: Numpy array containing the data point to plot
        :return: Integer indicating the amount of bins to compute
        """
        data = np.asarray(data_points, dtype=(np.float_))
        iqr = stats.iqr(data, rng=(25, 75), scale='raw', nan_policy='omit')
        rng = data.max() - data.min()
        return int(rng / (2 * iqr / np.power(data.size, 0.3333333333333333)) + 1)

    @staticmethod
    def freedman_diaconis_width(data_points: np.array) -> float:
        """

        Calculate the width of each bin by using Freedmann-Diaconis rule

        :param data_points: Numpy array containing the data point to plot
        :return: Float indicating the width of each bin
        """
        data = np.asarray(data_points, dtype=(np.float_))
        iqr = stats.iqr(data, rng=(25, 75), scale='raw', nan_policy='omit')
        return 2 * iqr / np.power(data.size, 0.3333333333333333)

    @staticmethod
    def generate_git_ignore(file_path: str, exclude_files: List[str]=None, exclude_default: bool=True):
        """

        Generate .gitignore file

        :param file_path:
        :param exclude_files: List[str]: Names of files or objects to be ignored
        :param exclude_default: bool: Exclude default files and objects
        """
        _gitignore = ''
        _default = '#########\n# misc: ##########\n.git\n.idea\n.DS_Store\n\n########### python: ###########\nvenv\n**/.cache\n**/__pycache__\n.pytest_cache\n\n###################### jupyter notebook: ######################\n.ipynb_checkpoints\n\n################## data sources: ##################\n*.db\n*.txt\n'
        if exclude_default:
            _gitignore = _default
        if exclude_files is not None:
            if len(exclude_files) > 0:
                for f in exclude_files:
                    _gitignore = _gitignore + f

        DataExporter(obj=_gitignore, file_path=file_path, create_dir=True, overwrite=False).file()

    @staticmethod
    def generate_network(df: pd.DataFrame, node_feature: str, edge_feature: str, kind: str='undirected', **kwargs) -> nx:
        """
        Generate network graph

        Parameters
        ----------
        df: pd.DataFrame
            Data set

        node_feature: str
            Name of the feature used to generate nodes from

        edge_feature: str
            Name of the feature used to generate edges from

        kind: str
            Network type
                -> directed: Bayes network
                -> undirected: Markov Network
                -> geometric: Geometric Network based on x, y scale

        Returns
        -------
        nx: Preconfigured Networkx network graph object
        """
        if kind == 'directed':
            _graph = nx.DiGraph()
        else:
            if kind == 'undirected':
                _graph = nx.Graph()
            else:
                if kind == 'geometric':
                    _graph = nx.random_geometric_graph(n=(kwargs.get('n')), radius=(kwargs.get('radius')),
                      dim=(2 if kwargs.get('dim') is None else kwargs.get('dim')),
                      pos=(kwargs.get('pos')),
                      p=(2 if kwargs.get('p') is None else kwargs.get('p')),
                      seed=None)
                else:
                    raise UtilsException('Network graph type ({}) not supported'.format(kind))
            if node_feature not in df.keys():
                raise UtilsException('Node feature ({}) not found'.format(node_feature))
            if edge_feature not in df.keys():
                raise UtilsException('Edge feature ({}) not found'.format(edge_feature))
        _group_by = df.groupby(by=edge_feature).aggregate({node_feature: 'count'})[1:]
        _nodes = df[node_feature].unique().tolist()
        _graph.add_nodes_from(nodes_for_adding=_nodes)
        _node_val = _group_by.index.values.tolist()
        _edge_val = _group_by[node_feature].values.tolist()
        for i in range(0, _group_by.shape[0], 1):
            if i in _nodes:
                _graph.add_edge(u_of_edge=(_node_val[i]), v_of_edge=(_edge_val[i]))
            else:
                _graph.add_edge(u_of_edge=i, v_of_edge=0)

        return _graph

    @staticmethod
    def get_duplicates(df: pd.DataFrame, cases: bool=True, features: bool=True) -> Dict[(str, list)]:
        """
        Get duplicate cases and / or features

        Parameters
        ----------
        df: pd.DataFrame
            Data set

        cases: bool
            Check whether cases are duplicated or not

        features: bool
            Check whether features are duplicated or not

        Returns
        -------
        Dict[str, list]: List of duplicated cases and / or features
        """
        _duplicates = dict(cases=[], features=[])
        if cases:
            _duplicates['cases'] = df.loc[df.duplicated(), :].index.values.tolist()
        if features:
            _duplicates['features'] = df.loc[:, df.transpose().duplicated()].keys().tolist()
        return _duplicates

    @staticmethod
    def get_feature_types(df: pd.DataFrame, features: List[str], dtypes: List[np.dtype], continuous: List[str]=None, categorical: List[str]=None, ordinal: List[str]=None, date: List[str]=None, text: List[str]=None, max_cats: int=500, date_edges: Tuple[(str, str)]=None) -> Dict[(str, List[str])]:
        """

        Get feature types

        :param df:
        :param features:
        :param dtypes:
        :param continuous:
        :param categorical:
        :param ordinal:
        :param date:
        :param text: List[str]
        :param max_cats:
        :param date_edges:
        :return:
        """
        _num = []
        _cat = []
        _str = []
        _date = []
        _ordinal = []
        _max_cats = max_cats if max_cats > 0 else 500
        if date_edges is None:
            _date_edges = None
        else:
            try:
                if not pd.to_datetime(date_edges[0]):
                    raise AssertionError
                elif not pd.to_datetime(date_edges[1]):
                    raise AssertionError
                _date_edges = tuple([pd.to_datetime(date_edges[0]), pd.to_datetime(date_edges[1])])
            except Exception as e:
                _date_edges = None
                Log(write=False, level='warning').log(msg=('Date edges ({}) cannot be converted into datetime\nError: {}'.format(date_edges, e)))

        for i, feature in enumerate(features):
            if date is not None:
                if feature in date:
                    _date.append(feature)
                    continue
                if ordinal is not None:
                    if feature in ordinal:
                        _ordinal.append(feature)
                        continue
                if continuous is not None:
                    if feature in continuous:
                        _num.append(feature)
                        continue
            else:
                if categorical is not None:
                    if feature in categorical:
                        _cat.append(feature)
                        continue
                if text is not None:
                    if feature in text:
                        _str.append(feature)
                        continue
            if str(dtypes[i]).find('float') >= 0:
                _unique = df[feature].unique()
                if any(df[feature].isnull()):
                    if any(_unique[(~pd.isnull(_unique))] % 1) != 0:
                        _num.append(feature)
                    elif len(str(df[feature].min()).split('.')[0]) >= 4:
                        try:
                            if not pd.to_datetime(df[feature]):
                                raise AssertionError
                            else:
                                if _date_edges is None:
                                    _date.append(feature)
                                else:
                                    if _date_edges[0] < pd.to_datetime(_unique.min()) or _date_edges[1] > pd.to_datetime(_unique.max()):
                                        _str.append(feature)
                                    else:
                                        _date.append(feature)
                        except (TypeError, ValueError):
                            _str.append(feature)

                    else:
                        _cat.append(feature)
                else:
                    if any(_unique % 1) != 0:
                        _num.append(feature)
                    elif len(str(df[feature].min()).split('.')[0]) >= 4:
                        try:
                            if not pd.to_datetime(df[feature]):
                                raise AssertionError
                            else:
                                if _date_edges is None:
                                    _date.append(feature)
                                else:
                                    if _date_edges[0] < pd.to_datetime(_unique.min()) or _date_edges[1] > pd.to_datetime(_unique.max()):
                                        _str.append(feature)
                                    else:
                                        _date.append(feature)
                        except (TypeError, ValueError):
                            _str.append(feature)

                    else:
                        _cat.append(feature)
            elif str(dtypes[i]).find('int') >= 0:
                if len(str(df[feature].min())) >= 4:
                    try:
                        assert pd.to_datetime(df[feature])
                        _date.append(feature)
                    except (TypeError, ValueError):
                        _cat.append(feature)

                else:
                    if df.shape[0] == len(df[feature].unique()):
                        _str.append(feature)
                    else:
                        _cat.append(feature)
            elif str(dtypes[i]).find('object') >= 0:
                _unique = df[feature].unique()
                _digits = 0
                _dot = False
                for text in _unique:
                    if text.find('.'):
                        _dot = True
                    if text.replace('.', '').isdigit():
                        _digits += 1

                if _digits == len(_unique):
                    if _dot:
                        if any(_unique[(~pd.isnull(_unique))] % 1) != 0:
                            _num.append(feature)
                        else:
                            if df.shape[0] == len(df[feature].unique()):
                                _str.append(feature)
                            else:
                                if len(str(df[feature].min()).split('.')[0]) >= 4:
                                    _str.append(feature)
                                else:
                                    _cat.append(feature)
                    else:
                        _cat.append(feature)
                else:
                    try:
                        _date_time = pd.to_datetime(df[feature])
                        if _date_edges is None:
                            _date.append(feature)
                        else:
                            if _date_edges[0] < pd.to_datetime(_unique.min()) or _date_edges[1] > pd.to_datetime(_unique.max()):
                                _str.append(feature)
                            else:
                                _date.append(feature)
                    except (TypeError, ValueError):
                        if df.shape[0] == len(df[feature].unique()):
                            _str.append(feature)
                        else:
                            if len(_unique) > _max_cats:
                                _str.append(feature)
                            else:
                                _cat.append(feature)

            else:
                if str(dtypes[i]).find('date') >= 0:
                    _date.append(feature)
                else:
                    if str(dtypes[i]).find('bool') >= 0:
                        _cat.append(feature)

        return dict(continuous=_num, categorical=_cat, ordinal=_ordinal, date=_date, text=_str)

    @staticmethod
    def get_geojson(df: pd.DataFrame, lat: np.array, lon: np.array, features: List[str], fig: str='polygon', save: bool=False) -> dict:
        """

        Generate geojson dictionary from pandas data frame

        :param df:
        :param lat:
        :param lon:
        :param features:
        :param fig:
        :param save:
        :return: dict: Geojson
        """
        features = []
        insert_features = lambda X: features.append(geojson.Feature(geometry=(geojson.Polygon((X['long'],
         X['lat']))),
          properties=dict(name=(X['name']), description=(X['description']))))
        df.apply(insert_features, axis=1)
        if save:
            with open('/Users/balistrerig/PycharmProjects/data_science/src/data_science/test/data/test.geojson', 'w', encoding='utf8') as (fp):
                geojson.dump((geojson.FeatureCollection(features)), fp, sort_keys=True, ensure_ascii=False)
        return dict

    @staticmethod
    def get_list_of_files(file_path: str) -> List[str]:
        """

        Get list of file in given directory or zip file

        :param file_path: str: Complete file path
        :return: List[str]: Name of detected files
        """
        if os.path.exists(file_path):
            if file_path.split('.')[(-1)] is 'zip':
                return zipfile.ZipFile(file_path).namelist()
            else:
                return [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
        else:
            raise UtilsException('File path not found ({})'.format(file_path))

    @staticmethod
    def get_list_of_objects(file_path: str) -> List[str]:
        """

        Get list of objects in given directory and subdirectories

        :param file_path: str: Complete file path
        :return: List[str]: List of object names detected in directory
        """
        return [obj for obj in os.listdir(file_path)]

    @staticmethod
    def get_invariant_features(df: pd.DataFrame) -> List[str]:
        """
        Get invariant features of data set

        Parameters
        ----------
        df: pd.DataFrame
            Data set

        Returns
        -------
        List[str]: Names of invariant features
        """
        _invariant_features = []
        for ft in df.keys():
            _unique_values = df[ft].unique()
            if len(_unique_values) <= 2:
                if len(_unique_values) == 1:
                    _invariant_features.append(ft)
                elif any(df[ft].isnull()):
                    _invariant_features.append(ft)

        return _invariant_features

    @staticmethod
    def get_pairs(features: List[str], max_features_each_pair: int=2) -> List[tuple]:
        """

        Get pairs of feature list

        :param List[str] features: Features to pair
        :param int max_features_each_pair: Maximum number of features for each pair
        :return: List[tuple]: List of features pairs
        """
        return [pair for pair in itertools.combinations(iterable=(list(set(features))), r=max_features_each_pair)]

    @staticmethod
    def get_group_by_percentile(data: pd.DataFrame, group_by: str, aggregate_by: List[str], aggregation: str='median', percentiles: int=10, duplicates: str='drop', include_group: bool=True) -> pd.DataFrame:
        """

        Generate percentile evaluation of of grouped features

        :param data: pd.DataFrame: Data set to calculate percentiles from
        :param group_by: str: Grouping features
        :param aggregate_by: List[str]: Features to aggregate
        :param aggregation: str: Aggregation method
        :param percentiles: int: Number of percentiles to generate
        :param duplicates: str: Handle duplicates
                                -> raise: Raise exception
                                -> drop: Drop
        :param include_group: bool: Include grouping feature inbto aggregation process
        :return: pd.DataFrame: Aggregated data set
        """
        _aggre = []
        _df = pd.DataFrame()
        if group_by in data.keys():
            _df[group_by] = data[group_by]
            if len(aggregate_by) == 0:
                raise UtilsException('No features for aggregation found')
            for agg in aggregate_by:
                if agg in data.keys():
                    _aggre.append(agg)
                    _df[agg] = data[agg]

        else:
            raise UtilsException('No feature for grouping found')
        if include_group:
            _aggre.append(group_by)
        _q = pd.qcut((_df[group_by]), q=percentiles, retbins=True, duplicates='drop')
        _perc_labels = _q[0].unique()
        _perc_edges = _q[1].tolist()
        _df['perc'] = pd.qcut(x=(_df[group_by]), q=percentiles,
          labels=_perc_labels,
          retbins=False,
          precision=4,
          duplicates=duplicates)
        _df_perc = _df.groupby(by=['perc']).agg({a:aggregation for a in _aggre})
        return _df_perc

    @staticmethod
    def get_perc_eval(pred: list, obs: list, aggregation: str='median', percentiles: int=10) -> pd.DataFrame:
        """

        Generate percentile evaluation of predictions and observation

        :param pred: list: List of predictions
        :param obs: list: List of observations
        :param aggregation: str: Aggregation method
                                -> min: Minimum
                                -> max: Maximum
                                -> median: Median
                                -> mean: Mean
        :param percentiles: int: Number of percentiles to calculate
        :return: pd.DataFrame: Percentile evaluation of prediction and observation
        """
        _df = pd.DataFrame({'obs':obs,  'preds':pred})
        _df['pred_perc'] = pd.qcut(x=(_df['obs']), q=percentiles, labels=(np.arange(1, percentiles + 1)), retbins=False, precision=4, duplicates='drop')
        _df_perc = _df.groupby(by=['pred_perc']).agg({'preds':aggregation,  'obs':aggregation})
        _df_perc['abs_diff'] = _df_perc['preds'] - _df_perc['obs']
        _df_perc['rel_diff'] = (_df_perc['preds'] - _df_perc['obs']) / _df_perc['obs']
        return _df_perc

    @staticmethod
    def search_for_file(key_word: str, starting_dir: str) -> List[str]:
        """

        Search for files with similar name patterns as key word input

        :param key_word: str: Searched key word
        :param starting_dir: str: Directory to start searching in
        :return: List[str]: Names of the files found under given key word
        """
        return glob.glob(pathname=key_word)