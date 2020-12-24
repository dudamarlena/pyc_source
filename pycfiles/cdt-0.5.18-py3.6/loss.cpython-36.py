# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/utils/loss.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 9014 bytes
"""Pytorch implementation of Losses and tools.

.. MIT License
..
.. Copyright (c) 2018 Diviyan Kalainathan
..
.. Permission is hereby granted, free of charge, to any person obtaining a copy
.. of this software and associated documentation files (the "Software"), to deal
.. in the Software without restriction, including without limitation the rights
.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
.. copies of the Software, and to permit persons to whom the Software is
.. furnished to do so, subject to the following conditions:
..
.. The above copyright notice and this permission notice shall be included in all
.. copies or substantial portions of the Software.
..
.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
.. SOFTWARE.
"""
from .Settings import SETTINGS
import numpy as np
from scipy.stats import ttest_ind
import torch as th

class TTestCriterion(object):
    __doc__ = ' A loop criterion based on t-test to check significance of results.\n\n    Args:\n        max_iter (int): Maximum number of iterations authorized\n        runs_per_iter (int): Number of runs performed per iteration\n        threshold (float): p-value threshold, under which the loop is stopped.\n\n    Example:\n        >>> from cdt.utils.loss import TTestCriterion\n        >>> l = TTestCriterion(50,5)\n        >>> x, y = [], []\n        >>> while l.loop(x, y):\n            ...     # compute loop and update results in x, y\n        >>> x, y  # Two lists with significant difference in score\n    '

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
    __doc__ = '**[torch.nn.Module]** Maximum Mean Discrepancy Metric to compare\n    empirical distributions.\n\n    The MMD score is defined by:\n\n    .. math::\n        \\widehat{MMD_k}(\\mathcal{D}, \\widehat{\\mathcal{D}}) = \n        \\frac{1}{n^2} \\sum_{i, j = 1}^{n} k(x_i, x_j) + \\frac{1}{n^2}\n        \\sum_{i, j = 1}^{n} k(\\hat{x}_i, \\hat{x}_j) - \\frac{2}{n^2} \n        \\sum_{i,j = 1}^n k(x_i, \\hat{x}_j)\n\n    where :math:`\\mathcal{D} \\text{ and } \\widehat{\\mathcal{D}}` represent \n    respectively the observed and empirical distributions, :math:`k` represents\n    the RBF kernel and :math:`n` the batch size.\n\n    Args:\n        input_size (int): Fixed batch size.\n        bandwiths (list): List of bandwiths to take account of. Defaults at\n            [0.01, 0.1, 1, 10, 100]\n        device (str): PyTorch device on which the computation will be made.\n            Defaults at ``cdt.SETTINGS.default_device``.\n\n    Inputs: empirical, observed\n        Forward pass: Takes both the true samples and the generated sample in any order \n        and returns the MMD score between the two empirical distributions.\n\n        + **empirical** distribution of shape `(batch_size, features)`: torch.Tensor\n          containing the empirical distribution\n        + **observed** distribution of shape `(batch_size, features)`: torch.Tensor\n          containing the observed distribution.\n\n    Outputs: score\n        + **score** of shape `(1)`: Torch.Tensor containing the loss value.\n\n    .. note::\n        Ref: Gretton, A., Borgwardt, K. M., Rasch, M. J., Schölkopf, \n        B., & Smola, A. (2012). A kernel two-sample test.\n        Journal of Machine Learning Research, 13(Mar), 723-773.\n\n    Example:\n        >>> from cdt.utils.loss import MMDloss\n        >>> import torch as th\n        >>> x, y = th.randn(100,10), th.randn(100, 10)\n        >>> mmd = MMDloss(100)  # 100 is the batch size\n        >>> mmd(x, y)\n        0.0766\n    '

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
    __doc__ = '**[torch.nn.Module]** L2 Loss between k-moments between two\n    distributions, k being a parameter.\n\n    These moments are raw moments and not normalized.\n    The loss is an L2 loss between the moments:\n\n    .. math::\n        MML(X, Y) = \\sum_{m=1}^{m^*} \\left( \\frac{1}{n_x} \\sum_{i=1}^{n_x} {x_i}^m \n        - \\frac{1}{n_y} \\sum_{j=1}^{n_y} {y_j}^m \\right)^2\n\n    where :math:`m^*` represent the number of moments to compute.\n\n    Args:\n        n_moments (int): Number of moments to compute.\n\n    Input: (X, Y)\n        + **X** represents the first empirical distribution in a torch.Tensor of\n          shape `(?, features)`\n        + **Y** represents the second empirical distribution in a torch.Tensor of\n          shape `(?, features)`\n\n    Output: mml\n        + **mml** is the output of the forward pass and is differenciable. \n          torch.Tensor of shape `(1)`\n\n    Example:\n        >>> from cdt.utils.loss import MomentMatchingLoss\n        >>> import torch as th\n        >>> x, y = th.randn(100,10), th.randn(100, 10)\n        >>> mml = MomentMatchingLoss(4)\n        >>> mml(x, y)\n    '

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