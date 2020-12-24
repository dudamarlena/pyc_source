# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/allrank/models/transformer.py
# Compiled at: 2020-02-21 08:15:29
# Size of source mod 2**32: 9291 bytes
__doc__ = '\nCode in this file was adapted from "The Annotated Transformer" by Harvard NLP.\nhttp://nlp.seas.harvard.edu/2018/04/03/attention.html\n'
import copy, math
from typing import Optional
import torch
import torch.nn as nn
import torch.nn.functional as F
from allrank.config import PositionalEncoding
from allrank.models.positional import _make_positional_encoding

def clones(module, N):
    """
    Creation of N identical layers.
    :param module: module to clone
    :param N: number of copies
    :return: nn.ModuleList of module copies
    """
    return nn.ModuleList([copy.deepcopy(module) for _ in range(N)])


class Encoder(nn.Module):
    """Encoder"""

    def __init__(self, layer, N, position):
        super(Encoder, self).__init__()
        self.layers = clones(layer, N)
        self.norm = LayerNorm(layer.size)
        self.position = position

    def forward(self, x, mask, indices):
        """
        Forward pass through each block of the Transformer.
        :param x: input of shape [batch_size, slate_length, input_dim]
        :param mask: padding mask of shape [batch_size, slate_length]
        :param indices: original item ranks used in positional encoding, shape [batch_size, slate_length]
        :return: output of shape [batch_size, slate_length, output_dim]
        """
        if self.position:
            x = self.position(x, mask, indices)
        mask = mask.unsqueeze(-2)
        for layer in self.layers:
            x = layer(x, mask)

        return self.norm(x)


class LayerNorm(nn.Module):
    """LayerNorm"""

    def __init__(self, features, eps=1e-06):
        """
        :param features: shape of normalized features
        :param eps: epsilon used for standard deviation
        """
        super(LayerNorm, self).__init__()
        self.a_2 = nn.Parameter(torch.ones(features))
        self.b_2 = nn.Parameter(torch.zeros(features))
        self.eps = eps

    def forward(self, x):
        """
        Forward pass through the layer normalization.
        :param x: input of shape [batch_size, slate_length, input_dim]
        :return: normalized input of shape [batch_size, slate_length, output_dim]
        """
        mean = x.mean((-1), keepdim=True)
        std = x.std((-1), keepdim=True)
        return self.a_2 * (x - mean) / (std + self.eps) + self.b_2


class SublayerConnection(nn.Module):
    """SublayerConnection"""

    def __init__(self, size, dropout):
        super(SublayerConnection, self).__init__()
        self.norm = LayerNorm(size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, sublayer):
        """
        Forward pass through the sublayer connection module, applying the residual connection to any sublayer with the same size.
        :param x: input of shape [batch_size, slate_length, input_dim]
        :param sublayer: layer through which to pass the input prior to applying the sum
        :return: output of shape [batch_size, slate_length, output_dim]
        """
        return x + self.dropout(sublayer(self.norm(x)))


class EncoderLayer(nn.Module):
    """EncoderLayer"""

    def __init__(self, size, self_attn, feed_forward, dropout):
        super(EncoderLayer, self).__init__()
        self.self_attn = self_attn
        self.feed_forward = feed_forward
        self.sublayer = clones(SublayerConnection(size, dropout), 2)
        self.size = size

    def forward(self, x, mask):
        """
        Forward pass through the encoder block.
        :param x: input of shape [batch_size, slate_length, self.size]
        :param mask: padding mask of shape [batch_size, slate_length]
        :return: output of shape [batch_size, slate_length, self.size]
        """
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, mask))
        return self.sublayer[1](x, self.feed_forward)


def attention(query, key, value, mask=None, dropout=None):
    """
    Basic function for "Scaled Dot Product Attention" computation.
    :param query: query set of shape [batch_size, slate_size, n_attention_heads, attention_dim]
    :param key: key set of shape [batch_size, slate_size, n_attention_heads, attention_dim]
    :param value: value set of shape [batch_size, slate_size, n_attention_heads, attention_dim]
    :param mask: padding mask of shape [batch_size, slate_length]
    :param dropout: dropout probability
    :return: attention scores of shape [batch_size, slate_size, n_attention_heads, attention_dim]
    """
    d_k = query.size(-1)
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 1, float('-inf'))
    p_attn = F.softmax(scores, dim=(-1))
    if dropout is not None:
        p_attn = dropout(p_attn)
    return (torch.matmul(p_attn, value), p_attn)


class MultiHeadedAttention(nn.Module):
    """MultiHeadedAttention"""

    def __init__(self, h, d_model, dropout=0.1):
        """
        :param h: number of attention heads
        :param d_model: input/output dimensionality
        :param dropout: dropout probability
        """
        super(MultiHeadedAttention, self).__init__()
        assert d_model % h == 0
        self.d_k = d_model // h
        self.h = h
        self.linears = clones(nn.Linear(d_model, d_model), 4)
        self.attn = None
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, query, key, value, mask=None):
        """
        Forward pass through the multi-head attention block.
        :param query: query set of shape [batch_size, slate_size, self.d_model]
        :param key: key set of shape [batch_size, slate_size, self.d_model]
        :param value: value set of shape [batch_size, slate_size, self.d_model]
        :param mask: padding mask of shape [batch_size, slate_length]
        :return: output of shape [batch_size, slate_size, self.d_model]
        """
        if mask is not None:
            mask = mask.unsqueeze(1)
        nbatches = query.size(0)
        query, key, value = [l(x).view(nbatches, -1, self.h, self.d_k).transpose(1, 2) for l, x in zip(self.linears, (query, key, value))]
        x, self.attn = attention(query, key, value, mask=mask, dropout=(self.dropout))
        x = x.transpose(1, 2).contiguous().view(nbatches, -1, self.h * self.d_k)
        return self.linears[(-1)](x)


class PositionwiseFeedForward(nn.Module):
    """PositionwiseFeedForward"""

    def __init__(self, d_model, d_ff, dropout=0.1):
        """
        :param d_model: input/output dimensionality
        :param d_ff: hidden dimensionality
        :param dropout: dropout probability
        """
        super(PositionwiseFeedForward, self).__init__()
        self.w_1 = nn.Linear(d_model, d_ff)
        self.w_2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        """
        Forward pass through the feed-forward block.
        :param x: input of shape [batch_size, slate_size, self.d_model]
        :return: output of shape [batch_size, slate_size, self.d_model]
        """
        return self.w_2(self.dropout(F.relu(self.w_1(x))))


def make_transformer(N=6, d_ff=2048, h=8, dropout=0.1, n_features=136, positional_encoding: Optional[PositionalEncoding]=None):
    """
    Helper function for instantiating Transformer-based Encoder.
    :param N: number of Transformer blocks
    :param d_ff: hidden dimensionality of the feed-forward layer in the Transformer block
    :param h: number of attention heads
    :param dropout: dropout probability
    :param n_features: number of input/output features of the feed-forward layer
    :param positional_encoding: config.PositionalEncoding object containing PE config
    :return: Transformer-based Encoder with given hyperparameters
    """
    c = copy.deepcopy
    attn = MultiHeadedAttention(h, n_features, dropout)
    ff = PositionwiseFeedForward(n_features, d_ff, dropout)
    position = _make_positional_encoding(n_features, positional_encoding)
    return Encoder(EncoderLayer(n_features, c(attn), c(ff), dropout), N, position)