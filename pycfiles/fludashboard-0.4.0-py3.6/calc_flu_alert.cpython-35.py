# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marfcg/codes/FluVigilanciaBR/fludashboard/fludashboard/libs/calc_flu_alert.py
# Compiled at: 2017-10-17 15:31:35
# Size of source mod 2**32: 1091 bytes
"""

"""
import numpy as np, pandas as pd

def get_season_level(se):
    """

    :param se: pd.Series
    :return: int
    """
    _max = max([se.l3, se.l2, se.l1, se.l0])
    if np.isnan(_max):
        return 0
    if se.l0 == _max:
        return 1
    if se.l1 == _max:
        return 2
    if se.l2 == _max:
        return 3
    return 4


def calc_alert_rank_whole_year(se):
    """
    calculate the alert rank for the whole year

    :param se: pd.Series
    :return:
    """
    high_threshold = se.l3 + se.l2
    if high_threshold >= 5:
        return 4
    if high_threshold > 1:
        return 3
    if se.l1 >= 1:
        return 2
    return 1


def apply_filter_alert_by_epiweek(df: pd.DataFrame, epiweek: int=None):
    """

    :param df:
    :param epiweek:
    :return:
    """
    if epiweek is not None:
        mask = df.eval('epiweek=={}'.format(epiweek))
    else:
        mask = df.keys()
    df_alert = df[mask].copy().reset_index()
    alert_col = df_alert.T.apply(get_season_level)
    df_alert = df_alert.assign(alert=alert_col)
    return df_alert