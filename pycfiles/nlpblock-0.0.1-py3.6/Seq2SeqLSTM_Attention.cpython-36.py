# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\nlpblock\model\Seq2SeqLSTM_Attention.py
# Compiled at: 2019-03-02 23:47:35
# Size of source mod 2**32: 1815 bytes
import torch, torch.nn as nn, nlpblock as nb

class Seq2SeqLSTM_Attention(nn.Module):

    def __init__(self, n_enc_vocab, n_dec_vocab, n_hidden, n_layers=1, bidirectional=False, linearTransform=True):
        super(Seq2SeqLSTM_Attention, self).__init__()
        self.n_hidden = n_hidden
        self.num_directions = 2 if bidirectional is True else 1
        self.encoder = nb.LSTM(input_size=n_enc_vocab, hidden_size=n_hidden, bidirectional=bidirectional)
        self.decoder = nb.LSTM(input_size=n_dec_vocab, hidden_size=n_hidden, bidirectional=bidirectional)
        self.attention = nb.AttentionTwo(n_dec_vocab, n_hidden, n_layers=n_layers,
          bidirectional=bidirectional,
          linearTransform=linearTransform)

    def hidden_init(self, enc_input):
        batch = enc_input.size(0)
        return torch.rand([self.num_directions, batch, self.n_hidden])

    def forward(self, enc_input, dec_input):
        init_hidden = self.hidden_init(enc_input)
        enc_output, final_enc_hidden = self.encoder(enc_input, (self.hidden_init(enc_input), self.hidden_init(enc_input)))
        dec_output, _ = self.decoder(dec_input, final_enc_hidden)
        output, attention = self.attention(enc_output, dec_output)
        return (output, attention)