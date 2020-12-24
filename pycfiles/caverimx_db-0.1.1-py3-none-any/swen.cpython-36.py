# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caver/model/swen.py
# Compiled at: 2018-12-03 22:41:49
# Size of source mod 2**32: 1614 bytes
import torch
from torch import nn
from .base import BaseModule
from ..config import ConfigSWEN
from ..utils import update_config

class SWEN(BaseModule):
    """SWEN"""

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