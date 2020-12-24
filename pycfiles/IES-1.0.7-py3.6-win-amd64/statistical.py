# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\factors\statistical.py
# Compiled at: 2018-01-16 04:37:02
# Size of source mod 2**32: 24373 bytes
import numpy as np
from numpy import broadcast_arrays
from scipy.stats import linregress, pearsonr, spearmanr
from strategycontainer.model import Equity
from strategycontainer.exception import IncompatibleTerms
from strategycontainer.tsp.factors import CustomFactor
from strategycontainer.tsp.filters import SingleAsset
from strategycontainer.tsp.mixins import SingleInputMixin, StandardOutputs
from strategycontainer.tsp.sentinels import NotSpecified
from strategycontainer.tsp.term import AssetExists
from strategycontainer.utils.input_validation import expect_bounded, expect_dtypes, expect_types
from strategycontainer.utils.math_utils import nanmean
from strategycontainer.utils.numpy_utils import float64_dtype, int64_dtype
from .basic import Returns
ALLOWED_DTYPES = (
 float64_dtype, int64_dtype)

class _RollingCorrelation(CustomFactor, SingleInputMixin):

    @expect_dtypes(base_factor=ALLOWED_DTYPES, target=ALLOWED_DTYPES)
    @expect_bounded(correlation_length=(2, None))
    def __new__(cls, base_factor, target, correlation_length, mask=NotSpecified):
        if target.ndim == 2:
            if base_factor.mask is not target.mask:
                raise IncompatibleTerms(term_1=base_factor, term_2=target)
        return super(_RollingCorrelation, cls).__new__(cls,
          inputs=[
         base_factor, target],
          window_length=correlation_length,
          mask=mask)


class RollingPearson(_RollingCorrelation):
    __doc__ = '\n    A Factor that computes pearson correlation coefficients between the columns\n    of a given Factor and either the columns of another Factor/BoundColumn or a\n    slice/single column of data.\n\n    Parameters\n    ----------\n    base_factor : zipline.pipeline.factors.Factor\n        The factor for which to compute correlations of each of its columns\n        with `target`.\n    target : zipline.pipeline.Term with a numeric dtype\n        The term with which to compute correlations against each column of data\n        produced by `base_factor`. This term may be a Factor, a BoundColumn or\n        a Slice. If `target` is two-dimensional, correlations are computed\n        asset-wise.\n    correlation_length : int\n        Length of the lookback window over which to compute each correlation\n        coefficient.\n    mask : zipline.pipeline.Filter, optional\n        A Filter describing which assets (columns) of `base_factor` should have\n        their correlation with `target` computed each day.\n\n    See Also\n    --------\n    :func:`scipy.stats.pearsonr`\n    :meth:`Factor.pearsonr`\n    :class:`zipline.pipeline.factors.RollingPearsonOfReturns`\n\n    Notes\n    -----\n    Most users should call Factor.pearsonr rather than directly construct an\n    instance of this class.\n    '
    window_safe = True

    def compute(self, today, assets, out, base_data, target_data):
        target_data = broadcast_arrays(target_data, base_data)[0]
        for i in range(len(out)):
            out[i] = pearsonr(base_data[:, i], target_data[:, i])[0]


class RollingSpearman(_RollingCorrelation):
    __doc__ = '\n    A Factor that computes spearman rank correlation coefficients between the\n    columns of a given Factor and either the columns of another\n    Factor/BoundColumn or a slice/single column of data.\n\n    Parameters\n    ----------\n    base_factor : zipline.pipeline.factors.Factor\n        The factor for which to compute correlations of each of its columns\n        with `target`.\n    target : zipline.pipeline.Term with a numeric dtype\n        The term with which to compute correlations against each column of data\n        produced by `base_factor`. This term may be a Factor, a BoundColumn or\n        a Slice. If `target` is two-dimensional, correlations are computed\n        asset-wise.\n    correlation_length : int\n        Length of the lookback window over which to compute each correlation\n        coefficient.\n    mask : zipline.pipeline.Filter, optional\n        A Filter describing which assets (columns) of `base_factor` should have\n        their correlation with `target` computed each day.\n\n    See Also\n    --------\n    :func:`scipy.stats.spearmanr`\n    :meth:`Factor.spearmanr`\n    :class:`zipline.pipeline.factors.RollingSpearmanOfReturns`\n\n    Notes\n    -----\n    Most users should call Factor.spearmanr rather than directly construct an\n    instance of this class.\n    '
    window_safe = True

    def compute(self, today, assets, out, base_data, target_data):
        target_data = broadcast_arrays(target_data, base_data)[0]
        for i in range(len(out)):
            out[i] = spearmanr(base_data[:, i], target_data[:, i])[0]


class RollingLinearRegression(CustomFactor, SingleInputMixin):
    __doc__ = '\n    A Factor that performs an ordinary least-squares regression predicting the\n    columns of a given Factor from either the columns of another\n    Factor/BoundColumn or a slice/single column of data.\n\n    Parameters\n    ----------\n    dependent : zipline.pipeline.factors.Factor\n        The factor whose columns are the predicted/dependent variable of each\n        regression with `independent`.\n    independent : zipline.pipeline.slice.Slice or zipline.pipeline.Factor\n        The factor/slice whose columns are the predictor/independent variable\n        of each regression with `dependent`. If `independent` is a Factor,\n        regressions are computed asset-wise.\n    regression_length : int\n        Length of the lookback window over which to compute each regression.\n    mask : zipline.pipeline.Filter, optional\n        A Filter describing which assets (columns) of `dependent` should be\n        regressed against `independent` each day.\n\n    See Also\n    --------\n    :func:`scipy.stats.linregress`\n    :meth:`Factor.linear_regression`\n    :class:`zipline.pipeline.factors.RollingLinearRegressionOfReturns`\n\n    Notes\n    -----\n    Most users should call Factor.linear_regression rather than directly\n    construct an instance of this class.\n    '
    outputs = ['alpha', 'beta', 'r_value', 'p_value', 'stderr']

    @expect_dtypes(dependent=ALLOWED_DTYPES, independent=ALLOWED_DTYPES)
    @expect_bounded(regression_length=(2, None))
    def __new__(cls, dependent, independent, regression_length, mask=NotSpecified):
        if independent.ndim == 2:
            if dependent.mask is not independent.mask:
                raise IncompatibleTerms(term_1=dependent, term_2=independent)
        return super(RollingLinearRegression, cls).__new__(cls,
          inputs=[
         dependent, independent],
          window_length=regression_length,
          mask=mask)

    def compute(self, today, assets, out, dependent, independent):
        alpha = out.alpha
        beta = out.beta
        r_value = out.r_value
        p_value = out.p_value
        stderr = out.stderr

        def regress(y, x):
            regr_results = linregress(y=y, x=x)
            alpha[i] = regr_results[1]
            beta[i] = regr_results[0]
            r_value[i] = regr_results[2]
            p_value[i] = regr_results[3]
            stderr[i] = regr_results[4]

        independent = broadcast_arrays(independent, dependent)[0]
        for i in range(len(out)):
            regress(y=(dependent[:, i]), x=(independent[:, i]))


class RollingPearsonOfReturns(RollingPearson):
    __doc__ = '\n    Calculates the Pearson product-moment correlation coefficient of the\n    returns of the given asset with the returns of all other assets.\n\n    Pearson correlation is what most people mean when they say "correlation\n    coefficient" or "R-value".\n\n    Parameters\n    ----------\n    target : zipline.assets.Asset\n        The asset to correlate with all other assets.\n    returns_length : int >= 2\n        Length of the lookback window over which to compute returns. Daily\n        returns require a window length of 2.\n    correlation_length : int >= 1\n        Length of the lookback window over which to compute each correlation\n        coefficient.\n    mask : zipline.pipeline.Filter, optional\n        A Filter describing which assets should have their correlation with the\n        target asset computed each day.\n\n    Notes\n    -----\n    Computing this factor over many assets can be time consuming. It is\n    recommended that a mask be used in order to limit the number of assets over\n    which correlations are computed.\n\n    Examples\n    --------\n    Let the following be example 10-day returns for three different assets::\n\n                       SPY    MSFT     FB\n        2017-03-13    -.03     .03    .04\n        2017-03-14    -.02    -.03    .02\n        2017-03-15    -.01     .02    .01\n        2017-03-16       0    -.02    .01\n        2017-03-17     .01     .04   -.01\n        2017-03-20     .02    -.03   -.02\n        2017-03-21     .03     .01   -.02\n        2017-03-22     .04    -.02   -.02\n\n    Suppose we are interested in SPY\'s rolling returns correlation with each\n    stock from 2017-03-17 to 2017-03-22, using a 5-day look back window (that\n    is, we calculate each correlation coefficient over 5 days of data). We can\n    achieve this by doing::\n\n        rolling_correlations = RollingPearsonOfReturns(\n            target=sid(8554),\n            returns_length=10,\n            correlation_length=5,\n        )\n\n    The result of computing ``rolling_correlations`` from 2017-03-17 to\n    2017-03-22 gives::\n\n                       SPY   MSFT     FB\n        2017-03-17       1    .15   -.96\n        2017-03-20       1    .10   -.96\n        2017-03-21       1   -.16   -.94\n        2017-03-22       1   -.16   -.85\n\n    Note that the column for SPY is all 1\'s, as the correlation of any data\n    series with itself is always 1. To understand how each of the other values\n    were calculated, take for example the .15 in MSFT\'s column. This is the\n    correlation coefficient between SPY\'s returns looking back from 2017-03-17\n    (-.03, -.02, -.01, 0, .01) and MSFT\'s returns (.03, -.03, .02, -.02, .04).\n\n    See Also\n    --------\n    :class:`zipline.pipeline.factors.RollingSpearmanOfReturns`\n    :class:`zipline.pipeline.factors.RollingLinearRegressionOfReturns`\n    '

    def __new__(cls, target, returns_length, correlation_length, mask=NotSpecified):
        returns = Returns(window_length=returns_length,
          mask=(AssetExists() | SingleAsset(asset=target)))
        return super(RollingPearsonOfReturns, cls).__new__(cls,
          base_factor=returns,
          target=(returns[target]),
          correlation_length=correlation_length,
          mask=mask)


class RollingSpearmanOfReturns(RollingSpearman):
    __doc__ = '\n    Calculates the Spearman rank correlation coefficient of the returns of the\n    given asset with the returns of all other assets.\n\n    Parameters\n    ----------\n    target : zipline.assets.Asset\n        The asset to correlate with all other assets.\n    returns_length : int >= 2\n        Length of the lookback window over which to compute returns. Daily\n        returns require a window length of 2.\n    correlation_length : int >= 1\n        Length of the lookback window over which to compute each correlation\n        coefficient.\n    mask : zipline.pipeline.Filter, optional\n        A Filter describing which assets should have their correlation with the\n        target asset computed each day.\n\n    Notes\n    -----\n    Computing this factor over many assets can be time consuming. It is\n    recommended that a mask be used in order to limit the number of assets over\n    which correlations are computed.\n\n    See Also\n    --------\n    :class:`zipline.pipeline.factors.RollingPearsonOfReturns`\n    :class:`zipline.pipeline.factors.RollingLinearRegressionOfReturns`\n    '

    def __new__(cls, target, returns_length, correlation_length, mask=NotSpecified):
        returns = Returns(window_length=returns_length,
          mask=(AssetExists() | SingleAsset(asset=target)))
        return super(RollingSpearmanOfReturns, cls).__new__(cls,
          base_factor=returns,
          target=(returns[target]),
          correlation_length=correlation_length,
          mask=mask)


class RollingLinearRegressionOfReturns(RollingLinearRegression):
    __doc__ = "\n    Perform an ordinary least-squares regression predicting the returns of all\n    other assets on the given asset.\n\n    Parameters\n    ----------\n    target : zipline.assets.Asset\n        The asset to regress against all other assets.\n    returns_length : int >= 2\n        Length of the lookback window over which to compute returns. Daily\n        returns require a window length of 2.\n    regression_length : int >= 1\n        Length of the lookback window over which to compute each regression.\n    mask : zipline.pipeline.Filter, optional\n        A Filter describing which assets should be regressed against the target\n        asset each day.\n\n    Notes\n    -----\n    Computing this factor over many assets can be time consuming. It is\n    recommended that a mask be used in order to limit the number of assets over\n    which regressions are computed.\n\n    This factor is designed to return five outputs:\n\n    - alpha, a factor that computes the intercepts of each regression.\n    - beta, a factor that computes the slopes of each regression.\n    - r_value, a factor that computes the correlation coefficient of each\n      regression.\n    - p_value, a factor that computes, for each regression, the two-sided\n      p-value for a hypothesis test whose null hypothesis is that the slope is\n      zero.\n    - stderr, a factor that computes the standard error of the estimate of each\n      regression.\n\n    For more help on factors with multiple outputs, see\n    :class:`zipline.pipeline.factors.CustomFactor`.\n\n    Examples\n    --------\n    Let the following be example 10-day returns for three different assets::\n\n                       SPY    MSFT     FB\n        2017-03-13    -.03     .03    .04\n        2017-03-14    -.02    -.03    .02\n        2017-03-15    -.01     .02    .01\n        2017-03-16       0    -.02    .01\n        2017-03-17     .01     .04   -.01\n        2017-03-20     .02    -.03   -.02\n        2017-03-21     .03     .01   -.02\n        2017-03-22     .04    -.02   -.02\n\n    Suppose we are interested in predicting each stock's returns from SPY's\n    over rolling 5-day look back windows. We can compute rolling regression\n    coefficients (alpha and beta) from 2017-03-17 to 2017-03-22 by doing::\n\n        regression_factor = RollingRegressionOfReturns(\n            target=sid(8554),\n            returns_length=10,\n            regression_length=5,\n        )\n        alpha = regression_factor.alpha\n        beta = regression_factor.beta\n\n    The result of computing ``alpha`` from 2017-03-17 to 2017-03-22 gives::\n\n                       SPY    MSFT     FB\n        2017-03-17       0    .011   .003\n        2017-03-20       0   -.004   .004\n        2017-03-21       0    .007   .006\n        2017-03-22       0    .002   .008\n\n    And the result of computing ``beta`` from 2017-03-17 to 2017-03-22 gives::\n\n                       SPY    MSFT     FB\n        2017-03-17       1      .3   -1.1\n        2017-03-20       1      .2     -1\n        2017-03-21       1     -.3     -1\n        2017-03-22       1     -.3    -.9\n\n    Note that SPY's column for alpha is all 0's and for beta is all 1's, as the\n    regression line of SPY with itself is simply the function y = x.\n\n    To understand how each of the other values were calculated, take for\n    example MSFT's ``alpha`` and ``beta`` values on 2017-03-17 (.011 and .3,\n    respectively). These values are the result of running a linear regression\n    predicting MSFT's returns from SPY's returns, using values starting at\n    2017-03-17 and looking back 5 days. That is, the regression was run with\n    x = [-.03, -.02, -.01, 0, .01] and y = [.03, -.03, .02, -.02, .04], and it\n    produced a slope of .3 and an intercept of .011.\n\n    See Also\n    --------\n    :class:`zipline.pipeline.factors.RollingPearsonOfReturns`\n    :class:`zipline.pipeline.factors.RollingSpearmanOfReturns`\n    "
    window_safe = True

    def __new__(cls, target, returns_length, regression_length, mask=NotSpecified):
        returns = Returns(window_length=returns_length,
          mask=(AssetExists() | SingleAsset(asset=target)))
        return super(RollingLinearRegressionOfReturns, cls).__new__(cls,
          dependent=returns,
          independent=(returns[target]),
          regression_length=regression_length,
          mask=mask)


class SimpleBeta(CustomFactor, StandardOutputs):
    __doc__ = '\n    Factor producing the slope of a regression line between each asset\'s daily\n    returns to the daily returns of a single "target" asset.\n\n    Parameters\n    ----------\n    target : zipline.Asset\n        Asset against which other assets should be regressed.\n    regression_length : int\n        Number of days of daily returns to use for the regression.\n    allowed_missing_percentage : float, optional\n        Percentage of returns observations (between 0 and 1) that are allowed\n        to be missing when calculating betas. Assets with more than this\n        percentage of returns observations missing will produce values of\n        NaN. Default behavior is that 25% of inputs can be missing.\n    '
    window_safe = True
    dtype = float64_dtype
    params = ('allowed_missing_count', )

    @expect_types(target=Equity,
      regression_length=int,
      allowed_missing_percentage=(
     int, float),
      __funcname='SimpleBeta')
    @expect_bounded(regression_length=(3, None),
      allowed_missing_percentage=(0.0, 1.0),
      __funcname='SimpleBeta')
    def __new__(cls, target, regression_length, allowed_missing_percentage=0.25):
        daily_returns = Returns(window_length=2,
          mask=(AssetExists() | SingleAsset(asset=target)))
        allowed_missing_count = int(allowed_missing_percentage * regression_length)
        return super(SimpleBeta, cls).__new__(cls,
          inputs=[
         daily_returns, daily_returns[target]],
          window_length=regression_length,
          allowed_missing_count=allowed_missing_count)

    def compute(self, today, assets, out, all_returns, target_returns, allowed_missing_count):
        vectorized_beta(dependents=all_returns,
          independent=target_returns,
          allowed_missing=allowed_missing_count,
          out=out)

    def short_repr(self):
        return '{}({!r}, {}, {})'.format(type(self).__name__, str(self.target.symbol), self.window_length, self.params['allowed_missing_count'])

    @property
    def target(self):
        """Get the target of the beta calculation.
        """
        return self.inputs[1].asset

    def __repr__(self):
        return '{}({}, length={}, allowed_missing={})'.format(type(self).__name__, self.target, self.window_length, self.params['allowed_missing_count'])


def vectorized_beta(dependents, independent, allowed_missing, out=None):
    """
    Compute slopes of linear regressions between columns of ``dependents`` and
    ``independent``.

    Parameters
    ----------
    dependents : np.array[N, M]
        Array with columns of data to be regressed against ``independent``.
    independent : np.array[N, 1]
        Independent variable of the regression
    allowed_missing : int
        Number of allowed missing (NaN) observations per column. Columns with
        more than this many non-nan observations in both ``dependents`` and
        ``independents`` will output NaN as the regression coefficient.

    Returns
    -------
    slopes : np.array[M]
        Linear regression coefficients for each column of ``dependents``.
    """
    nan = np.nan
    isnan = np.isnan
    N, M = dependents.shape
    if out is None:
        out = np.full(M, nan)
    independent = np.where(isnan(dependents), nan, independent)
    ind_residual = independent - nanmean(independent, axis=0)
    covariances = nanmean((ind_residual * dependents), axis=0)
    independent_variances = nanmean((ind_residual ** 2), axis=0)
    np.divide(covariances, independent_variances, out=out)
    nanlocs = isnan(independent).sum(axis=0) > allowed_missing
    out[nanlocs] = nan
    return out