# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/utils/loss.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 9014 bytes
__doc__ = 'Pytorch implementation of Losses and tools.\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
from .Settings import SETTINGS
import numpy as np
from scipy.stats import ttest_ind
import torch as th

class TTestCriterion(object):
    """TTestCriterion"""

    def __init__(self, max_iter, runs_per_iter, threshold=0.01):
        super(TTestCriterion, self).__init__()
        self.threshold = threshold
        self.max_iter = max_iter
        self.runs_per_iter = runs_per_iter
        self.iter = 0
        self.p_value = np.inf

    def loop(self, xy, yx):
        """ Tests the loop condition based on the new results and the
        parameters.

        Args:
            xy (list): list containing all the results for one set of samples
            yx (list): list containing all the results for the other set.

        Returns:
            bool: True if the loop has to continue, False otherwise.
        """
        if self.iter < 2:
            self.iter += self.runs_per_iter
            return True
        else:
            t_test, self.p_value = ttest_ind(xy, yx, equal_var=False)
            if self.p_value > self.threshold:
                if self.iter < self.max_iter:
                    self.iter += self.runs_per_iter
                    return True
            return False


class MMDloss(th.nn.Module):
    """MMDloss"""

    def __init__(self, input_size, bandwidths=None):
        """Init the model."""
        super(MMDloss, self).__init__()
        if bandwidths is None:
            bandwidths = th.Tensor([0.01, 0.1, 1, 10, 100])
        else:
            bandwidths = bandwidths
        s = th.cat([th.ones([input_size, 1]) / input_size,
         th.ones([input_size, 1]) / -input_size], 0)
        self.register_buffer('bandwidths', bandwidths.unsqueeze(0).unsqueeze(0))
        self.register_buffer('S', s @ s.t())

    def forward(self, x, y):
        X = th.cat([x, y], 0)
        XX = X @ X.t()
        X2 = (X * X).sum(dim=1).unsqueeze(0)
        exponent = -2 * XX + X2.expand_as(XX) + X2.t().expand_as(XX)
        b = exponent.unsqueeze(2).expand(-1, -1, self.bandwidths.shape[2]) * -self.bandwidths
        lossMMD = th.sum(self.S.unsqueeze(2) * b.exp())
        return lossMMD


class MomentMatchingLoss(th.nn.Module):
    """MomentMatchingLoss"""

    def __init__(self, n_moments=1):
        """Initialize the loss model.

        :param n_moments: number of moments
        """
        super(MomentMatchingLoss, self).__init__()
        self.moments = n_moments

    def forward(self, pred, target):
        """Compute the loss model.

        :param pred: predicted Variable
        :param target: Target Variable
        :return: Loss
        """
        loss = th.FloatTensor([0])
        for i in range(1, self.moments):
            mk_pred = th.mean(th.pow(pred, i), 0)
            mk_tar = th.mean(th.pow(target, i), 0)
            loss.add_(th.mean((mk_pred - mk_tar) ** 2))

        return loss


def notears_constr(adj_m, max_pow=None):
    """No Tears constraint for binary adjacency matrixes. Represents a
    differenciable constraint to converge towards a DAG.

    .. warning::
       If adj_m is non binary: Feed adj_m * adj_m as input (Hadamard product).

    Args:
        adj_m (array-like): Adjacency matrix of the graph
        max_pow (int): maximum value to which the infinite sum is to be computed.
           defaults to the shape of the adjacency_matrix

    Returns:
        np.ndarray or torch.Tensor: Scalar value of the loss with the type
            depending on the input.

    .. note::
       Zheng, X., Aragam, B., Ravikumar, P. K., & Xing, E. P. (2018). DAGs with
       NO TEARS: Continuous Optimization for Structure Learning. In Advances in
       Neural Information Processing Systems (pp. 9472-9483).
    """
    m_exp = [
     adj_m]
    if max_pow is None:
        max_pow = adj_m.shape[1]
    while m_exp[(-1)].sum() > 0 and len(m_exp) < max_pow:
        m_exp.append(m_exp[(-1)] @ adj_m / len(m_exp))

    return sum([i.diag().sum() for idx, i in enumerate(m_exp)])