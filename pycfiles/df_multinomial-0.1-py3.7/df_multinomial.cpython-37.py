# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\df_multinomial\df_multinomial.py
# Compiled at: 2019-03-28 19:05:17
# Size of source mod 2**32: 6630 bytes
""" Multinomial proportion confidence interval for pandas dataframes

Created on Fri Mar 28 12:07:07 2019

Author: Marco Bellini
License: BSD-3
"""
import numpy as np
from scipy import stats
import pandas as pd

def gen_ci_label(columns, prefix):
    new_cols = [prefix + '_%g' % x for x in columns]
    return new_cols


def multinomial_proportions_confint_df(df_counts, alpha=0.05, return_mean=False, return_multiindex=False):
    """ Confidence intervals for multinomial proportions stored in pandas dataframe

    Parameters
    ----------
    :param df_counts: pandas DataFrame
        each row of the dataframe is an experiment and contains the number of observations in each category.
    :param alpha: float in (0, 1), optional
        Significance level, defaults to 0.05.
    :param: return_mean True/False, optional, False is default
        Add the mean of observations to the return dataframe

    Returns
    -------
    :return: confint : pandas DataFrame
        Array of ([mean],lower, upper) confidence levels for each category, such that
        overall coverage is (approximately) `1-alpha`.

    Raises
    ------

    Notes
    -----

    References
    ----------

    .. [1] Levin, Bruce, "A representation for multinomial cumulative
       distribution functions," The Annals of Statistics, Vol. 9, No. 5,
       1981, pp. 1123-1126.

    .. [2] Goodman, L.A., "On simultaneous confidence intervals for multinomial
           proportions," Technometrics, Vol. 7, No. 2, 1965, pp. 247-254.

    .. [3] Sison, Cristina P., and Joseph Glaz, "Simultaneous Confidence
           Intervals and Sample Size Determination for Multinomial
           Proportions," Journal of the American Statistical Association,
           Vol. 90, No. 429, 1995, pp. 366-369.

    .. [4] May, Warren L., and William D. Johnson, "A SAS® macro for
           constructing simultaneous confidence intervals  for multinomial
           proportions," Computer methods and programs in Biomedicine, Vol. 53,
           No. 3, 1997, pp. 153-162.

    """
    if not isinstance(df_counts, pd.DataFrame):
        raise TypeError('counts must be a pandas DataFrame')
    else:
        if alpha <= 0 or alpha >= 1:
            raise ValueError('alpha must be in (0, 1), bounds excluded')
        if (df_counts.values < 0).any():
            raise ValueError('counts must be >= 0')
        n_experiments = df_counts.sum(axis=1)
        k_values = df_counts.shape[1]
        row_counts = pd.concat(([n_experiments] * k_values), axis=1)
        row_counts.columns = df_counts.columns
        proportions = df_counts.divide(row_counts)
        chi2 = stats.chi2.ppf(1 - alpha / k_values, 1)
        chi2_m = df_counts * 0 + chi2
        delta_numerator = np.sqrt(chi2 ** 2 + 4 * df_counts * chi2 * (1 - proportions))
        n_m = pd.concat(([n_experiments] * k_values), axis=1)
        n_m.columns = df_counts.columns
        delta_divider = 2 * (chi2_m + n_m)
        numerator = 2 * df_counts + chi2_m
        num1 = numerator - delta_numerator
        confidence_lower = num1.divide(delta_divider)
        num2 = numerator + delta_numerator
        confidence_upper = num2.divide(delta_divider)
        if return_mean:
            df_mean = proportions
            if return_multiindex:
                multi_columns = {'mean':df_mean, 
                 'lb':confidence_lower,  'ub':confidence_upper}
                region = pd.concat((multi_columns.values()), axis=1, keys=(multi_columns.keys()))
            else:
                confidence_lower.columns = gen_ci_label(df_counts.columns, 'lb')
                confidence_upper.columns = gen_ci_label(df_counts.columns, 'ub')
                df_mean.columns = gen_ci_label(df_counts.columns, 'mean')
                region = pd.concat((df_mean, confidence_lower, confidence_upper), axis=1)
        else:
            if return_multiindex:
                multi_columns = {'lb':confidence_lower, 
                 'ub':confidence_upper}
                region = pd.concat((multi_columns.values()), axis=1, keys=(multi_columns.keys()))
            else:
                confidence_lower.columns = gen_ci_label(df_counts.columns, 'lb')
                confidence_upper.columns = gen_ci_label(df_counts.columns, 'ub')
                region = pd.concat((confidence_lower, confidence_upper), axis=1)
    return region


def mn_mean_ci(df, groupby_col, feature, alpha=0.05):
    """
    group DataFrame by column groupby_col and count the occurrences in feature
    then extact mean and ci using multinomial_proportions_confint_df

    :param df: DataFrame
    :param groupby_col: column or list of columns

    :param feature: columns
    :param alpha: float in (0, 1), optional
        Significance level, defaults to 0.05.
    :return: pandas DataFrame as in multinomial_proportions_confint_df
    """
    counts = df.groupby(by=groupby_col)[feature].value_counts().unstack(level=1).fillna(0)
    mean_ci = multinomial_proportions_confint_df(counts, alpha=alpha, return_mean=True, return_multiindex=True)
    return mean_ci


def mn_ci_plot(df, ax=None, label_prefix='', **kwargs):
    """
    plots the dataframe (output of mn_mean_ci) using a for loop on df.index

    :param df:
    :param ax: optional axis handle, default None
    :param kwargs: for plt.errorbar
    :return:
    """
    groups = list(df.index)
    xm = df.columns.levels[1]
    for ind in groups:
        ym = df.loc[ind]['mean']
        lb = df.loc[ind]['lb']
        ub = df.loc[ind]['ub']
        yerr_l = np.abs(lb - ym)
        yerr_u = np.abs(ub - ym)
        yerr = np.vstack((yerr_l, yerr_u))
        if isinstance(ind, (int, float, complex)):
            label = label_prefix + '%g' % ind
        else:
            if isinstance(ind, str):
                label = label_prefix + ind
        if ax is None:
            (plt.errorbar)(xm, ym, yerr=yerr, label=label, **kwargs)
        else:
            (ax.errorbar)(xm, ym, yerr=yerr, label=label, **kwargs)

    return ()