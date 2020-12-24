# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caver/model/han.py
# Compiled at: 2018-12-03 22:41:49
# Size of source mod 2**32: 2870 bytes
import torch
from torch import nn
from .base import BaseModule
from ..config import ConfigHAN
from ..utils import update_config

class HAN(BaseModule):
    """HAN"""

    def __init__(self, **kwargs):
        super().__init__()
        self.config = update_config((ConfigHAN()), **kwargs)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.embedding = nn.Embedding(self.config.vocab_size, self.config.embedding_dim)
        self.rnn = nn.GRU((self.config.embedding_dim),
          (self.config.hidden_dim),
          (self.config.layer_num),
          batch_first=True,
          bidirectional=(self.config.bidirectional))
        self.attention = Attention(self.config)
        self.mlp = nn.Linear(self.config.hidden_dim * (2 if self.config.bidirectional else 1), self.config.label_num)
        self.sigmoid = nn.Sigmoid()

    def init_hidden(self, batch_size):
        return torch.zeros(self.config.layer_num * (2 if self.config.bidirectional else 1), batch_size, self.config.hidden_dim).to(self.device)

    def forward(self, input_data):
        batch_size = input_data.size(0)
        hidden = self.init_hidden(batch_size)
        embedded = self.embedding(input_data)
        context, hidden = self.rnn(embedded, hidden)
        context = self.attention(context)
        return self.sigmoid(self.mlp(context))


class Attention(nn.Module):
    """Attention"""

    def __init__(self, config):
        super().__init__()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.config = config
        self.linear = nn.Linear(self.config.hidden_dim * 2, self.config.hidden_dim)
        self.tanh = nn.Tanh()
        self.softmax = nn.Softmax(dim=1)
        self.uw = torch.randn((self.config.hidden_dim), 1, requires_grad=True).to(self.device)

    def forward(self, context):
        batch_size = context.size(0)
        u = self.tanh(self.linear(context))
        weight = self.softmax(u.bmm(self.uw.unsqueeze(0).repeat(batch_size, 1, 1)))
        return weight.transpose(1, 2).bmm(context).view(batch_size, -1)