# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\nlpblock\model\Transformer.py
# Compiled at: 2019-03-01 09:26:31
# Size of source mod 2**32: 531 bytes
import torch, torch.nn as nn, nlpblock as nb

class Transofmer(nn.Module):

    def __init__(self, n_enc_vocab, n_dec_vocab):
        super(Transofmer, self).__init__()
        self.n_enc_vocab = n_enc_vocab
        self.n_dec_vocab = n_dec_vocab

    def forward(self, *input):
        return 1


model = Transofmer(n_enc_vocab=20, n_dec_vocab=30)
output, attention = model(torch.rand([3, 5, 20]), torch.rand([3, 7, 30]))