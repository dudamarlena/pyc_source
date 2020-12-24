# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/trainer/classifier_train_valid.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 505 bytes
import tensorflow as tf, numpy as np
from deephyper.search.nas.model.trainer.train_valid import TrainerTrainValid
import deephyper.search.nas.model.arch as a, deephyper.search.nas.model.train_utils as U
from deephyper.search import util
from deephyper.search.nas.utils._logging import JsonMessage as jm
logger = util.conf_logger('deephyper.model.trainer')

class TrainerClassifierTrainValid(TrainerTrainValid):

    def __init__(self, config, model):
        super().__init__(config, model)