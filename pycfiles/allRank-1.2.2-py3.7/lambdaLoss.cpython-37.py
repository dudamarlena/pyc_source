# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/allrank/models/losses/lambdaLoss.py
# Compiled at: 2020-02-21 08:15:29
# Size of source mod 2**32: 5057 bytes
import torch
from allrank.data.dataset_loading import PADDED_Y_VALUE
from allrank.models.losses import DEFAULT_EPS

def lambdaLoss(y_pred, y_true, eps=DEFAULT_EPS, padded_value_indicator=PADDED_Y_VALUE, weighing_scheme=None, k=None, sigma=1.0, mu=10.0, reduction='sum', reduction_log='binary'):
    """
    LambdaLoss framework for LTR losses implementations, introduced in "The LambdaLoss Framework for Ranking Metric Optimization".
    Contains implementations of different weighing schemes corresponding to e.g. LambdaRank or RankNet.
    :param y_pred: predictions from the model, shape [batch_size, slate_length]
    :param y_true: ground truth labels, shape [batch_size, slate_length]
    :param eps: epsilon value, used for numerical stability
    :param padded_value_indicator: an indicator of the y_true index containing a padded item, e.g. -1
    :param weighing_scheme: a string corresponding to a name of one of the weighing schemes
    :param k: rank at which the loss is truncated
    :param sigma: score difference weight used in the sigmoid function
    :param mu: optional weight used in NDCGLoss2++ weighing scheme
    :param reduction: losses reduction method, could be either a sum or a mean
    :param reduction_log: logarithm variant used prior to masking and loss reduction, either binary or natural
    :return: loss value, a torch.Tensor
    """
    device = y_pred.device
    y_pred = y_pred.clone()
    y_true = y_true.clone()
    padded_mask = y_true == padded_value_indicator
    y_pred[padded_mask] = float('-inf')
    y_true[padded_mask] = float('-inf')
    y_pred_sorted, indices_pred = y_pred.sort(descending=True, dim=(-1))
    y_true_sorted, _ = y_true.sort(descending=True, dim=(-1))
    true_sorted_by_preds = torch.gather(y_true, dim=1, index=indices_pred)
    true_diffs = true_sorted_by_preds[:, :, None] - true_sorted_by_preds[:, None, :]
    padded_pairs_mask = torch.isfinite(true_diffs)
    if weighing_scheme != 'ndcgLoss1_scheme':
        padded_pairs_mask = padded_pairs_mask & (true_diffs > 0)
    else:
        ndcg_at_k_mask = torch.zeros((y_pred.shape[1], y_pred.shape[1]), dtype=(torch.bool), device=device)
        ndcg_at_k_mask[:k, :k] = 1
        true_sorted_by_preds.clamp_(min=0.0)
        y_true_sorted.clamp_(min=0.0)
        pos_idxs = torch.arange(1, y_pred.shape[1] + 1).to(device)
        D = torch.log2(1.0 + pos_idxs.float())[None, :]
        maxDCGs = torch.sum((((torch.pow(2, y_true_sorted) - 1) / D)[:, :k]), dim=(-1)).clamp(min=eps)
        G = (torch.pow(2, true_sorted_by_preds) - 1) / maxDCGs[:, None]
        if weighing_scheme is None:
            weights = 1.0
        else:
            weights = globals()[weighing_scheme](G, D, mu, true_sorted_by_preds)
        scores_diffs = (y_pred_sorted[:, :, None] - y_pred_sorted[:, None, :]).clamp(min=(-100000000.0), max=100000000.0)
        scores_diffs[torch.isnan(scores_diffs)] = 0.0
        weighted_probas = (torch.sigmoid(sigma * scores_diffs).clamp(min=eps) ** weights).clamp(min=eps)
        if reduction_log == 'natural':
            losses = torch.log(weighted_probas)
        else:
            if reduction_log == 'binary':
                losses = torch.log2(weighted_probas)
            else:
                raise ValueError('Reduction logarithm base can be either natural or binary')
        masked_losses = losses[(padded_pairs_mask & ndcg_at_k_mask)]
        if reduction == 'sum':
            loss = -torch.sum(masked_losses)
        else:
            if reduction == 'mean':
                loss = -torch.mean(masked_losses)
            else:
                raise ValueError('Reduction method can be either sum or mean')
    return loss


def ndcgLoss1_scheme(G, D, *args):
    return (G / D)[:, :, None]


def ndcgLoss2_scheme(G, D, *args):
    pos_idxs = torch.arange(1, (G.shape[1] + 1), device=(G.device))
    delta_idxs = torch.abs(pos_idxs[:, None] - pos_idxs[None, :])
    deltas = torch.abs(torch.pow(torch.abs(D[(0, delta_idxs - 1)]), -1.0) - torch.pow(torch.abs(D[(0, delta_idxs)]), -1.0))
    deltas.diagonal().zero_()
    return deltas[None, :, :] * torch.abs(G[:, :, None] - G[:, None, :])


def lamdbaRank_scheme(G, D, *args):
    return torch.abs(torch.pow(D[:, :, None], -1.0) - torch.pow(D[:, None, :], -1.0)) * torch.abs(G[:, :, None] - G[:, None, :])


def ndcgLoss2PP_scheme(G, D, *args):
    return args[0] * ndcgLoss2_scheme(G, D) + lamdbaRank_scheme(G, D)


def rankNet_scheme(G, D, *args):
    return 1.0


def rankNetWeightedByGTDiff_scheme(G, D, *args):
    return torch.abs(args[1][:, :, None] - args[1][:, None, :])


def rankNetWeightedByGTDiffPowed_scheme(G, D, *args):
    return torch.abs(torch.pow(args[1][:, :, None], 2) - torch.pow(args[1][:, None, :], 2))