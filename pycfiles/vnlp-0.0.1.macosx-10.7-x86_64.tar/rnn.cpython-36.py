# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/anaconda3/lib/python3.6/site-packages/vnlp/nn/rnn.py
# Compiled at: 2018-06-21 18:09:27
# Size of source mod 2**32: 1338 bytes
import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

class PackedRNN(nn.Module):

    def __init__(self, rnn):
        super().__init__()
        self.rnn = rnn

    @property
    def batch_first(self):
        return self.rnn.batch_first

    def forward(self, inputs, lengths, prev_state=None, total_length=None, pad_value=0):
        sorted_lens, sorted_indices = torch.sort(lengths, dim=0, descending=True)
        inputs = inputs[sorted_indices] if self.batch_first else inputs[:, sorted_indices]
        packed_inputs = pack_padded_sequence(inputs, lengths=sorted_lens, batch_first=(self.batch_first))
        packed_outputs, state = self.rnn(packed_inputs, prev_state)
        outputs, _ = pad_packed_sequence(packed_outputs, batch_first=(self.batch_first), padding_value=pad_value, total_length=(total_length or sorted_lens.max().item()))
        _, unsorted_indices = torch.sort(sorted_indices, 0)
        outputs = outputs[unsorted_indices] if self.batch_first else outputs[:, unsorted_indices]
        if isinstance(state, (tuple, list)):
            state = [s[:, unsorted_indices] for s in state]
        else:
            state = state[:, unsorted_indices]
        return (
         outputs, state)