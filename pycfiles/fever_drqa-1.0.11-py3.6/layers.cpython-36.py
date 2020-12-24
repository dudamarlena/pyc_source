# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drqa/reader/layers.py
# Compiled at: 2019-08-29 06:03:42
# Size of source mod 2**32: 10280 bytes
"""Definitions of model layers/NN modules"""
import torch, torch.nn as nn, torch.nn.functional as F
from torch.autograd import Variable

class StackedBRNN(nn.Module):
    __doc__ = 'Stacked Bi-directional RNNs.\n\n    Differs from standard PyTorch library in that it has the option to save\n    and concat the hidden states between layers. (i.e. the output hidden size\n    for each sequence input is num_layers * hidden_size).\n    '

    def __init__(self, input_size, hidden_size, num_layers, dropout_rate=0, dropout_output=False, rnn_type=nn.LSTM, concat_layers=False, padding=False):
        super(StackedBRNN, self).__init__()
        self.padding = padding
        self.dropout_output = dropout_output
        self.dropout_rate = dropout_rate
        self.num_layers = num_layers
        self.concat_layers = concat_layers
        self.rnns = nn.ModuleList()
        for i in range(num_layers):
            input_size = input_size if i == 0 else 2 * hidden_size
            self.rnns.append(rnn_type(input_size, hidden_size, num_layers=1,
              bidirectional=True))

    def forward(self, x, x_mask):
        """Encode either padded or non-padded sequences.

        Can choose to either handle or ignore variable length sequences.
        Always handle padding in eval.

        Args:
            x: batch * len * hdim
            x_mask: batch * len (1 for padding, 0 for true)
        Output:
            x_encoded: batch * len * hdim_encoded
        """
        if x_mask.data.sum() == 0:
            output = self._forward_unpadded(x, x_mask)
        else:
            if self.padding or not self.training:
                output = self._forward_padded(x, x_mask)
            else:
                output = self._forward_unpadded(x, x_mask)
        return output.contiguous()

    def _forward_unpadded(self, x, x_mask):
        """Faster encoding that ignores any padding."""
        x = x.transpose(0, 1)
        outputs = [
         x]
        for i in range(self.num_layers):
            rnn_input = outputs[(-1)]
            if self.dropout_rate > 0:
                rnn_input = F.dropout(rnn_input, p=(self.dropout_rate),
                  training=(self.training))
            rnn_output = self.rnns[i](rnn_input)[0]
            outputs.append(rnn_output)

        if self.concat_layers:
            output = torch.cat(outputs[1:], 2)
        else:
            output = outputs[(-1)]
        output = output.transpose(0, 1)
        if self.dropout_output:
            if self.dropout_rate > 0:
                output = F.dropout(output, p=(self.dropout_rate),
                  training=(self.training))
        return output

    def _forward_padded(self, x, x_mask):
        """Slower (significantly), but more precise, encoding that handles
        padding.
        """
        lengths = x_mask.data.eq(0).long().sum(1).squeeze()
        _, idx_sort = torch.sort(lengths, dim=0, descending=True)
        _, idx_unsort = torch.sort(idx_sort, dim=0)
        lengths = list(lengths[idx_sort])
        idx_sort = Variable(idx_sort)
        idx_unsort = Variable(idx_unsort)
        x = x.index_select(0, idx_sort)
        x = x.transpose(0, 1)
        rnn_input = nn.utils.rnn.pack_padded_sequence(x, lengths)
        outputs = [
         rnn_input]
        for i in range(self.num_layers):
            rnn_input = outputs[(-1)]
            if self.dropout_rate > 0:
                dropout_input = F.dropout((rnn_input.data), p=(self.dropout_rate),
                  training=(self.training))
                rnn_input = nn.utils.rnn.PackedSequence(dropout_input, rnn_input.batch_sizes)
            outputs.append(self.rnns[i](rnn_input)[0])

        for i, o in enumerate(outputs[1:], 1):
            outputs[i] = nn.utils.rnn.pad_packed_sequence(o)[0]

        if self.concat_layers:
            output = torch.cat(outputs[1:], 2)
        else:
            output = outputs[(-1)]
        output = output.transpose(0, 1)
        output = output.index_select(0, idx_unsort)
        if output.size(1) != x_mask.size(1):
            padding = torch.zeros(output.size(0), x_mask.size(1) - output.size(1), output.size(2)).type(output.data.type())
            output = torch.cat([output, Variable(padding)], 1)
        if self.dropout_output:
            if self.dropout_rate > 0:
                output = F.dropout(output, p=(self.dropout_rate),
                  training=(self.training))
        return output


class SeqAttnMatch(nn.Module):
    __doc__ = 'Given sequences X and Y, match sequence Y to each element in X.\n\n    * o_i = sum(alpha_j * y_j) for i in X\n    * alpha_j = softmax(y_j * x_i)\n    '

    def __init__(self, input_size, identity=False):
        super(SeqAttnMatch, self).__init__()
        if not identity:
            self.linear = nn.Linear(input_size, input_size)
        else:
            self.linear = None

    def forward(self, x, y, y_mask):
        """
        Args:
            x: batch * len1 * hdim
            y: batch * len2 * hdim
            y_mask: batch * len2 (1 for padding, 0 for true)
        Output:
            matched_seq: batch * len1 * hdim
        """
        if self.linear:
            x_proj = self.linear(x.view(-1, x.size(2))).view(x.size())
            x_proj = F.relu(x_proj)
            y_proj = self.linear(y.view(-1, y.size(2))).view(y.size())
            y_proj = F.relu(y_proj)
        else:
            x_proj = x
            y_proj = y
        scores = x_proj.bmm(y_proj.transpose(2, 1))
        y_mask = y_mask.unsqueeze(1).expand(scores.size())
        scores.data.masked_fill_(y_mask.data, -float('inf'))
        alpha_flat = F.softmax(scores.view(-1, y.size(1)))
        alpha = alpha_flat.view(-1, x.size(1), y.size(1))
        matched_seq = alpha.bmm(y)
        return matched_seq


class BilinearSeqAttn(nn.Module):
    __doc__ = "A bilinear attention layer over a sequence X w.r.t y:\n\n    * o_i = softmax(x_i'Wy) for x_i in X.\n\n    Optionally don't normalize output weights.\n    "

    def __init__(self, x_size, y_size, identity=False, normalize=True):
        super(BilinearSeqAttn, self).__init__()
        self.normalize = normalize
        if not identity:
            self.linear = nn.Linear(y_size, x_size)
        else:
            self.linear = None

    def forward(self, x, y, x_mask):
        """
        Args:
            x: batch * len * hdim1
            y: batch * hdim2
            x_mask: batch * len (1 for padding, 0 for true)
        Output:
            alpha = batch * len
        """
        Wy = self.linear(y) if self.linear is not None else y
        xWy = x.bmm(Wy.unsqueeze(2)).squeeze(2)
        xWy.data.masked_fill_(x_mask.data, -float('inf'))
        if self.normalize:
            if self.training:
                alpha = F.log_softmax(xWy)
            else:
                alpha = F.softmax(xWy)
        else:
            alpha = xWy.exp()
        return alpha


class LinearSeqAttn(nn.Module):
    __doc__ = 'Self attention over a sequence:\n\n    * o_i = softmax(Wx_i) for x_i in X.\n    '

    def __init__(self, input_size):
        super(LinearSeqAttn, self).__init__()
        self.linear = nn.Linear(input_size, 1)

    def forward(self, x, x_mask):
        """
        Args:
            x: batch * len * hdim
            x_mask: batch * len (1 for padding, 0 for true)
        Output:
            alpha: batch * len
        """
        x_flat = x.view(-1, x.size(-1))
        scores = self.linear(x_flat).view(x.size(0), x.size(1))
        scores.data.masked_fill_(x_mask.data, -float('inf'))
        alpha = F.softmax(scores)
        return alpha


def uniform_weights(x, x_mask):
    """Return uniform weights over non-masked x (a sequence of vectors).

    Args:
        x: batch * len * hdim
        x_mask: batch * len (1 for padding, 0 for true)
    Output:
        x_avg: batch * hdim
    """
    alpha = Variable(torch.ones(x.size(0), x.size(1)))
    if x.data.is_cuda:
        alpha = alpha.cuda()
    alpha = alpha * x_mask.eq(0).float()
    alpha = alpha / alpha.sum(1).expand(alpha.size())
    return alpha


def weighted_avg(x, weights):
    """Return a weighted average of x (a sequence of vectors).

    Args:
        x: batch * len * hdim
        weights: batch * len, sum(dim = 1) = 1
    Output:
        x_avg: batch * hdim
    """
    return weights.unsqueeze(1).bmm(x).squeeze(1)