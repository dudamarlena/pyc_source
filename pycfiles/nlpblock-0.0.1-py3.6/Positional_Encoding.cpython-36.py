# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\nlpblock\layer\Positional_Encoding.py
# Compiled at: 2019-03-02 23:50:02
# Size of source mod 2**32: 219 bytes
import torch.nn as nn

class Positional_Encoding(nn.Module):

    def __init__(self, d_model, d_k, d_v, n_heads):
        super(Positional_Encoding, self).__init__()

    def forward(self, input):
        return 1