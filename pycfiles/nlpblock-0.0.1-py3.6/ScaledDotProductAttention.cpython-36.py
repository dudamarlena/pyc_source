# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\nlpblock\layer\ScaledDotProductAttention.py
# Compiled at: 2019-03-01 09:11:31
# Size of source mod 2**32: 768 bytes
import torch, numpy as np, torch.nn as nn

class ScaledDotProductAttention(nn.Module):

    def __init__(self, d_model, d_k, d_v, n_heads):
        super(ScaledDotProductAttention, self).__init__()
        self.d_model = d_model
        self.d_k = d_k
        self.d_v = d_v
        self.n_heads = n_heads
        self.softmax = nn.Softmax(dim=(-1))

    def forward(self, Q, K, V, attn_mask=None):
        attn_vector = torch.matmul(Q, K.transpose(-1, -2)) / np.sqrt(self.d_k)
        if attn_mask is not None:
            attn_vector.masked_fill_(attn_mask, -1000000000.0)
        attn_softmax_vector = self.softmax(attn_vector)
        context_vector = torch.matmul(attn_softmax_vector, V)
        return (
         context_vector, attn_softmax_vector)