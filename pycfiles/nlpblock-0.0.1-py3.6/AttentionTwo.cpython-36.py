# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\nlpblock\layer\AttentionTwo.py
# Compiled at: 2019-03-02 23:38:00
# Size of source mod 2**32: 2596 bytes
import torch, torch.nn as nn
from nlpblock.layer.Attention import Attention

class AttentionTwo(Attention):
    __doc__ = '\n    Classes for relationship-attention of `TWO` models such as Encoder between Decoder\n    Each Model should have same Type.\n    In general, I call first model as Encdoer, second model as Decoder\n    '

    def __init__(self, n_dec_vocab, n_hidden, n_layers=1, bidirectional=False, linearTransform=True):
        super(AttentionTwo, self).__init__(n_hidden, n_layers, bidirectional, linearTransform)
        self.n_dec_vocab = n_dec_vocab
        self.num_directions = 2 if bidirectional is True else 1
        self.classifier = nn.Linear((self.n_hidden * 2), n_dec_vocab, bias=False)

    def forward(self, enc_output, dec_output):
        """
        :param enc_output: a matrix of all time steps of output in encoder(=context), Shape : [batch, enc_seq_len, n_hidden * num_directions]
        :param dec_output: a matrix of all time steps of output in decoder(=query)  , Shape : [batch, dec_seq_len, n_hidden * num_directions]
        :return: concatenated dec_output and attention weight between encoder and decoder
                first return : mixed output between decoder output and context vector
                second return : softmax-nize attention vector
                , Shape : [batch, dec_seq_len, n_dec_vocab], [batch, dec_seq_len. enc_seq_len]
        """
        batch, dec_seq_len = dec_output.size(0), dec_output.size(1)
        enc_seq_len = enc_output.size(1)
        output = torch.empty([dec_seq_len, batch, self.n_dec_vocab])
        attention = torch.empty([dec_seq_len, batch, enc_seq_len])
        for i in range(dec_seq_len):
            F, query = enc_output, dec_output[:, i, :]
            attn_softmax_vector = self.get_attn_vector(F, query)
            attention[i] = attn_softmax_vector.squeeze(1)
            context_vector = attn_softmax_vector.bmm(enc_output)
            query = query.unsqueeze(1)
            output[i] = self.classifier(torch.cat((query, context_vector), dim=2)).squeeze(1)

        return (
         output.transpose(0, 1), attention.transpose(0, 1))