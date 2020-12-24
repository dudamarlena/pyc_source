# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/anaconda3/lib/python3.6/site-packages/vnlp/model/module.py
# Compiled at: 2018-06-22 03:31:12
# Size of source mod 2**32: 529 bytes
from torch import nn

class BaseModule(nn.Module):

    def __init__(self, args):
        super().__init__()
        self.args = args

    def featurize(self, batch, device=None):
        raise NotImplementedError()

    def compute_loss(self, out, batch):
        raise NotImplementedError()

    def extract_preds(self, out, batch):
        raise NotImplementedError()

    def graph(self, grapher, metrics, iteration):
        grapher.add_metrics(metrics, iteration=iteration)
        grapher.add_parameters(self, iteration)