# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\nlpblock\layer\AttentionOne.py
# Compiled at: 2019-03-02 23:24:42
# Size of source mod 2**32: 2603 bytes
import torch, torch.nn as nn
from nlpblock.layer.Attention import Attention

class AttentionOne(Attention):
    __doc__ = '\n    Classes for only `ONE` time sequence Model such as RNN, LSTM, etc\n    When forward in this class, We make query from only RNN, LSTM outputs parameter(=All time steps of output in time sequence Model)\n    '

    def __init__(self, n_class, n_hidden, n_layers=1, bidirectional=False, linearTransform=True):
        super(AttentionOne, self).__init__(n_hidden, n_layers, bidirectional, linearTransform)
        self.n_class = n_class
        self.num_directions = 2 if bidirectional is True else 1
        self.classifier = nn.Linear((self.n_hidden), n_class, bias=False)

    def forward(self, outputs, first=0, last=-1):
        """
        In this function, query in Attention will be made from outputs matrix
        :param outputs: a matrix of all time steps of output in RNN ,LSTM, etc(=context),
                Shape : [batch, enc_seq_len, n_hidden * num_directions]
        :param first index in a matrix of all time steps of output in RNN ,LSTM, etc
        :param last index in a matrix of all time steps of output in RNN ,LSTM, etc
        :return: final output, Shape [batch, n_class] for classification
        """
        batch, seq_len, n_hidden = outputs.size(0), outputs.size(1), outputs.size(-1) // self.num_directions
        outputs = outputs.view(batch, seq_len, self.num_directions, n_hidden)
        query = torch.empty([batch, self.num_directions, n_hidden])
        if self.bidirectional is True:
            for i in range(batch):
                query[i][1] = outputs[i][first][(-1)]
                query[i][0] = outputs[i][last][0]

        else:
            for i in range(batch):
                query[i][0] = outputs[i][last][0]

        outputs = outputs.view(batch, seq_len, -1)
        query = query.view(batch, -1)
        attn_softmax_vector = self.get_attn_vector(outputs, query)
        context_vector = attn_softmax_vector.bmm(outputs).squeeze(1)
        return self.classifier(context_vector)