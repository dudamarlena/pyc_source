# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caver/model/swen.py
# Compiled at: 2018-12-03 22:41:49
# Size of source mod 2**32: 1614 bytes
import torch
from torch import nn
from .base import BaseModule
from ..config import ConfigSWEN
from ..utils import update_config

class SWEN(BaseModule):
    __doc__ = '\n    :param window: avg_pool window\n    :type window: int\n\n    This model is the implementation of SWEN-hier from `swen_paper`_:\n    Shen, Dinghan, et al. "Baseline Needs More Love: On Simple Word-Embedding-Based Models and Associated Pooling Mechanisms."\n\n    .. _swen_paper: https://arxiv.org/abs/1805.09843\n\n    text -> embedding -> avg_pool -> max_pool -> mlp -> sigmoid\n    '

    def __init__(self, **kwargs):
        super().__init__()
        self.config = update_config((ConfigSWEN()), **kwargs)
        self.embedding = nn.Embedding(self.config.vocab_size, self.config.embedding_dim, self.config.sentence_length)
        self.embedding_dropout = nn.Dropout(self.config.embedding_drop)
        self.avg_pool = nn.AvgPool1d(self.config.window)
        self.max_pool = nn.MaxPool1d((self.config.sentence_length - self.config.window) // 3 - 1)
        self.dropout = nn.Dropout(self.config.drop)
        self.mlp = nn.Linear(self.config.embedding_dim, self.config.label_num)
        self.sigmoid = nn.Sigmoid()

    def forward(self, input_data):
        embedded = self.embedding(input_data).transpose(1, 2)
        hidden = self.embedding_dropout(embedded)
        hidden = self.avg_pool(hidden)
        hidden = self.max_pool(hidden)
        hidden = hidden.view(-1, self.config.embedding_dim)
        return self.sigmoid(self.mlp(self.dropout(hidden)))