# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/predict_param.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 1513 bytes
from arch.api.utils import log_utils
from federatedml.param.base_param import BaseParam
LOGGER = log_utils.getLogger()

class PredictParam(BaseParam):
    __doc__ = '\n    Define the predict method of HomoLR, HeteroLR, SecureBoosting\n\n    Parameters\n    ----------\n\n    threshold: float or int, The threshold use to separate positive and negative class. Normally, it should be (0,1)\n    '

    def __init__(self, threshold=0.5):
        self.threshold = threshold

    def check(self):
        if type(self.threshold).__name__ not in ('float', 'int'):
            raise ValueError("predict param's predict_param {} not supported, should be float or int".format(self.threshold))
        LOGGER.debug('Finish predict parameter check!')
        return True