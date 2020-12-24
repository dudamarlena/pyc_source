# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/utils/torch.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 14459 bytes
__doc__ = 'PyTorch utilities for models.\n\nAuthor: Diviyan Kalainathan, Olivier Goudet\nDate: 09/3/2018\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
import math, torch as th
from torch.nn import Parameter
from torch.nn.modules.batchnorm import _BatchNorm

def _sample_gumbel(shape, eps=1e-10, out=None):
    """
    Implementation of pytorch.
    (https://github.com/pytorch/pytorch/blob/e4eee7c2cf43f4edba7a14687ad59d3ed61d9833/torch/nn/functional.py)
    Sample from Gumbel(0, 1)
    based on
    https://github.com/ericjang/gumbel-softmax/blob/3c8584924603869e90ca74ac20a6a03d99a91ef9/Categorical%20VAE.ipynb ,
    (MIT license)
    """
    U = out.resize_(shape).uniform_() if out is not None else th.rand(shape)
    return -th.log(eps - th.log(U + eps))


def _gumbel_softmax_sample(logits, tau=1, eps=1e-10):
    """
    Implementation of pytorch.
    (https://github.com/pytorch/pytorch/blob/e4eee7c2cf43f4edba7a14687ad59d3ed61d9833/torch/nn/functional.py)
    Draw a sample from the Gumbel-Softmax distribution
    based on
    https://github.com/ericjang/gumbel-softmax/blob/3c8584924603869e90ca74ac20a6a03d99a91ef9/Categorical%20VAE.ipynb
    (MIT license)
    """
    dims = logits.dim()
    gumbel_noise = _sample_gumbel((logits.size()), eps=eps, out=(logits.data.new()))
    y = logits + gumbel_noise
    return th.softmax(y / tau, dims - 1)


def gumbel_softmax(logits, tau=1, hard=False, eps=1e-10):
    """
    Implementation of pytorch.
    (https://github.com/pytorch/pytorch/blob/e4eee7c2cf43f4edba7a14687ad59d3ed61d9833/torch/nn/functional.py)
    Sample from the Gumbel-Softmax distribution and optionally discretize.
    Args:
      logits: `[batch_size, n_class]` unnormalized log-probs
      tau: non-negative scalar temperature
      hard: if ``True``, take `argmax`, but differentiate w.r.t. soft sample y
    Returns:
      [batch_size, n_class] sample from the Gumbel-Softmax distribution.
      If hard=True, then the returned sample will be one-hot, otherwise it will
      be a probability distribution that sums to 1 across classes
    Constraints:
    - this implementation only works on batch_size x num_features tensor for now
    based on
    https://github.com/ericjang/gumbel-softmax/blob/3c8584924603869e90ca74ac20a6a03d99a91ef9/Categorical%20VAE.ipynb ,
    (MIT license)
    """
    shape = logits.size()
    if not len(shape) == 2:
        raise AssertionError
    else:
        y_soft = _gumbel_softmax_sample(logits, tau=tau, eps=eps)
        if hard:
            _, k = y_soft.data.max(-1)
            y_hard = (logits.data.new)(*shape).zero_().scatter_(-1, k.view(-1, 1), 1.0)
            y = y_hard - y_soft.data + y_soft
        else:
            y = y_soft
    return y


def _sample_logistic(shape, out=None):
    U = out.resize_(shape).uniform_() if out is not None else th.rand(shape)
    return th.log(U) - th.log(1 - U)


def _sigmoid_sample(logits, tau=1):
    """
    Implementation of Bernouilli reparametrization based on Maddison et al. 2017
    """
    dims = logits.dim()
    logistic_noise = _sample_logistic((logits.size()), out=(logits.data.new()))
    y = logits + logistic_noise
    return th.sigmoid(y / tau)


def gumbel_sigmoid(logits, ones_tensor, zeros_tensor, tau=1, hard=False):
    shape = logits.size()
    y_soft = _sigmoid_sample(logits, tau=tau)
    if hard:
        y_hard = th.where(y_soft > 0.5, ones_tensor, zeros_tensor)
        y = y_hard.data - y_soft.data + y_soft
    else:
        y = y_soft
    return y


class ChannelBatchNorm1d(_BatchNorm):
    """ChannelBatchNorm1d"""

    def __init__(self, num_channels, num_features, *args, **kwargs):
        (super(ChannelBatchNorm1d, self).__init__)(num_channels * num_features, *args, **kwargs)
        self.num_channels = num_channels
        self.num_features = num_features

    def _check_input_dim(self, input):
        if input.dim() != 2:
            if input.dim() != 3:
                raise ValueError('expected 2D or 3D input (got {}D input)'.format(input.dim()))

    def forward(self, input):
        _input = input.contiguous().view(-1, self.num_channels * self.num_features)
        output = super(ChannelBatchNorm1d, self).forward(_input)
        return output.view(-1, self.num_channels, self.num_features)


class MatrixSampler(th.nn.Module):
    """MatrixSampler"""

    def __init__(self, graph_size, mask=None, gumbel=False):
        super(MatrixSampler, self).__init__()
        if not isinstance(graph_size, (list, tuple)):
            self.graph_size = (
             graph_size, graph_size)
        else:
            self.graph_size = graph_size
        self.weights = th.nn.Parameter((th.FloatTensor)(*self.graph_size))
        self.weights.data.zero_()
        if mask is None:
            mask = 1 - (th.eye)(*self.graph_size)
        if not (type(mask) == bool and not mask):
            self.register_buffer('mask', mask)
        self.gumble = gumbel
        ones_tensor = (th.ones)(*self.graph_size)
        self.register_buffer('ones_tensor', ones_tensor)
        zeros_tensor = (th.zeros)(*self.graph_size)
        self.register_buffer('zeros_tensor', zeros_tensor)

    def forward(self, tau=1, drawhard=True):
        """Return a sampled graph."""
        if self.gumble:
            drawn_proba = (gumbel_softmax((th.stack([self.weights.view(-1), -self.weights.view(-1)], 1)), tau=tau,
              hard=drawhard)[:, 0].view)(*self.graph_size)
        else:
            drawn_proba = gumbel_sigmoid((2 * self.weights), (self.ones_tensor), (self.zeros_tensor), tau=tau, hard=drawhard)
        if hasattr(self, 'mask'):
            return self.mask * drawn_proba
        else:
            return drawn_proba

    def get_proba(self):
        if hasattr(self, 'mask'):
            return th.sigmoid(2 * self.weights) * self.mask
        else:
            return th.sigmoid(2 * self.weights)

    def set_skeleton(self, mask):
        self.register_buffer('mask', mask)


def functional_linear3d(input, weight, bias=None):
    r"""
    Apply a linear transformation to the incoming data: :math:`y = xA^T + b`.
    Shape:
        - Input: :math:`(N, *, in\_features)` where `*` means any number of
          additional dimensions
        - Weight: :math:`(out\_features, in\_features)`
        - Bias: :math:`(out\_features)`
        - Output: :math:`(N, *, out\_features)`
    """
    output = input.transpose(0, 1).matmul(weight)
    if bias is not None:
        output += bias.unsqueeze(1)
    return output.transpose(0, 1)


class Linear3D(th.nn.Module):
    """Linear3D"""

    def __init__(self, sizes, bias=True):
        super(Linear3D, self).__init__()
        self.in_features = sizes[1]
        self.out_features = sizes[2]
        self.channels = sizes[0]
        self.weight = Parameter(th.Tensor(self.channels, self.in_features, self.out_features))
        if bias:
            self.bias = Parameter(th.Tensor(self.channels, self.out_features))
        else:
            self.register_parameter('bias', None)
        self.reset_parameters()

    def reset_parameters(self):
        stdv = 1.0 / math.sqrt(self.weight.size(1))
        self.weight.data.uniform_(-stdv, stdv)
        if self.bias is not None:
            self.bias.data.uniform_(-stdv, stdv)

    def forward(self, input, noise=None, adj_matrix=None):
        if input.dim() == 2:
            if noise is None:
                input = input.unsqueeze(1).expand([input.shape[0], self.channels, self.in_features])
            else:
                input = th.cat([
                 input.unsqueeze(1).expand([input.shape[0],
                  self.channels,
                  self.in_features - 1]),
                 noise.unsqueeze(2)], 2)
        if adj_matrix is not None:
            input = input * adj_matrix.t().unsqueeze(0)
        return functional_linear3d(input, self.weight, self.bias)

    def extra_repr(self):
        return 'in_features={}, out_features={}, bias={}'.format(self.in_features, self.out_features, self.bias is not None)