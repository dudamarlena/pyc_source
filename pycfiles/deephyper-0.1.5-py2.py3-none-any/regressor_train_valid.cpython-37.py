# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/trainer/regressor_train_valid.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 580 bytes
import tensorflow as tf, numpy as np, math, traceback
from sklearn.metrics import mean_squared_error
import deephyper.search.nas.model.arch as a
import deephyper.search.nas.model.train_utils as U
from deephyper.search import util
import deephyper.search.nas.utils._logging as jm
from deephyper.search.nas.model.trainer.train_valid import TrainerTrainValid
logger = util.conf_logger('deephyper.model.trainer')

class TrainerRegressorTrainValid(TrainerTrainValid):

    def __init__(self, config, model):
        super().__init__(config, model)