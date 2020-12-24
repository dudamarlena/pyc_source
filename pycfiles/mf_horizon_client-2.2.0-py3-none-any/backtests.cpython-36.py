# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stanley/IdeaProjects/horizon-python-client/src/mf_horizon_client/post_processing/backtests.py
# Compiled at: 2020-05-09 19:22:18
# Size of source mod 2**32: 543 bytes
import pandas as pd, numpy as np
from sklearn.metrics import classification_report

def binary_backtests_returns(backtests: pd.DataFrame) -> pd.DataFrame:
    """
    Converts a Horizon backtest data frame into a binary backtests of directions
    """
    return backtests.diff().apply(np.sign).dropna()


def calculate_metrics(y_pred: pd.Series, y_true: pd.Series):
    """
    Takes a Horizon binary backtest data frame and calculate metrics.
    """
    return classification_report(y_true=y_true, y_pred=y_pred, output_dict=True)