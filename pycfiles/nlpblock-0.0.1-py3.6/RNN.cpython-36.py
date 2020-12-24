# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\nlpblock\layer\RNN.py
# Compiled at: 2019-03-02 23:17:12
# Size of source mod 2**32: 936 bytes
import torch.nn as nn

class RNN(nn.Module):
    __doc__ = "\n        All parameter same torch.nn default setting\n        except, nonlinearity(='relu') batch_first(=True), bias(=False)\n        See more detail in here, https://pytorch.org/docs/stable/nn.html\n    "

    def __init__(self, input_size, hidden_size, nonlinearity='relu', bias=False, batch_first=True, num_layers=1, dropout=0, bidirectional=False):
        super(RNN, self).__init__()
        self.rnn = nn.RNN(input_size=input_size, hidden_size=hidden_size,
          nonlinearity=nonlinearity,
          bias=bias,
          batch_first=batch_first,
          num_layers=num_layers,
          dropout=dropout,
          bidirectional=bidirectional)

    def forward(self, input, h_0):
        return self.rnn(input, h_0)