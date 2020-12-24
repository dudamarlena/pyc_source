# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stanley/PycharmProjects/horizon-python-client/src/mf_horizon_client/data_structures/configs/stage_config_enums.py
# Compiled at: 2020-04-13 11:00:26
# Size of source mod 2**32: 814 bytes
from enum import Enum

class CorrelationMethod(Enum):
    mutual_info = 'mutual_info'
    spearman = 'spearman'
    pearson = 'pearson'
    kendall = 'kendall'


class StationarisationStrategy(Enum):
    keep_fail = 'keep_fail'
    discard_fail = 'discard_fail'
    none = 'none'


class TargetTransformType(Enum):
    DoNothing = 'DoNothingTargetTransform'
    HorizonLagDiff = 'HorizonDiff'
    HorizonLagDiffRatio = 'HorizonDiffRatio'


class FeatureGeneratorType(Enum):
    autolag = 'autolag'
    ewma = 'ewma'
    logarithm = 'logarithm'
    lag = 'lag'
    rolling_average = 'rolling_average'
    perc_change = 'perc_change'


class RegressorType(Enum):
    RandomForest = 'RandomForest'
    Martingale = 'Martingale'
    VBLinReg = 'VBLinReg'
    MondrianForest = 'MondrianForest'
    XGBoost = 'XGBoost'