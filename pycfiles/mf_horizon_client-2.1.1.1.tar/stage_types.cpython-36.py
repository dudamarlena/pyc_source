# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stanley/PycharmProjects/horizon-python-client/src/mf_horizon_client/data_structures/configs/stage_types.py
# Compiled at: 2020-03-26 22:31:55
# Size of source mod 2**32: 369 bytes
import enum

class StageType(enum.Enum):
    __doc__ = ' A complete list of all stages available to use in a pipeline'
    feature_generation = 'feature_generation'
    filtering = 'filtering'
    problem_specification = 'problem_specification'
    stationarisation = 'stationarisation'
    backtest = 'backtest'
    refinement = 'refinement'
    prediction = 'prediction'