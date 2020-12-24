# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/allrank/models/losses/approxNDCG.py
# Compiled at: 2020-02-21 08:15:29
# Size of source mod 2**32: 2625 bytes
import torch
from allrank.data.dataset_loading import PADDED_Y_VALUE
from allrank.models.losses import DEFAULT_EPS

def approxNDCGLoss(y_pred, y_true, eps=DEFAULT_EPS, padded_value_indicator=PADDED_Y_VALUE, alpha=1.0):
    """
    Loss based on approximate NDCG introduced in "A General Approximation Framework for Direct Optimization of
    Information Retrieval Measures". Please note that this method does not implement any kind of truncation.
    :param y_pred: predictions from the model, shape [batch_size, slate_length]
    :param y_true: ground truth labels, shape [batch_size, slate_length]
    :param eps: epsilon value, used for numerical stability
    :param padded_value_indicator: an indicator of the y_true index containing a padded item, e.g. -1
    :param alpha: score difference weight used in the sigmoid function
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
    padded_pairs_mask.diagonal(dim1=(-2), dim2=(-1)).zero_()
    true_sorted_by_preds.clamp_(min=0.0)
    y_true_sorted.clamp_(min=0.0)
    pos_idxs = torch.arange(1, y_pred.shape[1] + 1).to(device)
    D = torch.log2(1.0 + pos_idxs.float())[None, :]
    maxDCGs = torch.sum(((torch.pow(2, y_true_sorted) - 1) / D), dim=(-1)).clamp(min=eps)
    G = (torch.pow(2, true_sorted_by_preds) - 1) / maxDCGs[:, None]
    scores_diffs = y_pred_sorted[:, :, None] - y_pred_sorted[:, None, :]
    scores_diffs[~padded_pairs_mask] = 0.0
    approx_pos = 1.0 + torch.sum((padded_pairs_mask.float() * torch.sigmoid(-alpha * scores_diffs).clamp(min=eps)), dim=(-1))
    approx_D = torch.log2(1.0 + approx_pos)
    approx_NDCG = torch.sum((G / approx_D), dim=(-1))
    return -torch.mean(approx_NDCG)