# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caver/model/fasttext.py
# Compiled at: 2018-12-18 00:48:32
# Size of source mod 2**32: 1042 bytes
import torch, torch.nn as nn, torch.nn.functional as F
from .base import BaseModule

class FastText(BaseModule):
    __doc__ = '\n    Original FastText re-implementaion\n    '

    def __init__(self, vocab_size=1000, embedding_dim=100, label_num=100):
        super().__init__()
        self._vocab_size = vocab_size
        self._embedding_dim = embedding_dim
        self._label_num = label_num
        self.embedding = nn.Embedding(self._vocab_size, self._embedding_dim)
        self.predictor = nn.Linear(self._embedding_dim, self._label_num)

    def forward(self, sentence):
        embedded = self.embedding(sentence)
        pooled = F.avg_pool2d(embedded, (embedded.shape[1], 1)).squeeze(1)
        preds = self.predictor(pooled)
        return preds