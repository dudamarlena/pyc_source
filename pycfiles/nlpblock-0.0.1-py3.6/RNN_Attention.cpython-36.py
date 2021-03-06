# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\nlpblock\model\RNN_Attention.py
# Compiled at: 2019-03-02 23:35:49
# Size of source mod 2**32: 1210 bytes
import torch, torch.nn as nn, nlpblock as nb

class RNN_Attention(nn.Module):

    def __init__(self, emb_dim, n_class, n_hidden, n_layers=1, bidirectional=False, linearTransform=True):
        super(RNN_Attention, self).__init__()
        self.n_hidden = n_hidden
        self.num_directions = 2 if bidirectional is True else 1
        self.rnn = nb.RNN(emb_dim, n_hidden, bidirectional=bidirectional)
        self.attention = nb.AttentionOne(n_class, n_hidden, n_layers=n_layers,
          bidirectional=bidirectional,
          linearTransform=linearTransform)

    def hidden_init(self, input):
        batch = input.size(0)
        return torch.rand([self.num_directions, batch, self.n_hidden])

    def forward(self, input):
        outputs, _ = self.rnn(input, self.hidden_init(input))
        return (outputs, self.attention(outputs))