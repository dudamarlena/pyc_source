# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/allrank/models/losses/rankNet.py
# Compiled at: 2020-02-21 08:15:29
# Size of source mod 2**32: 3651 bytes
from itertools import product
import torch
from torch.nn import BCEWithLogitsLoss
from allrank.data.dataset_loading import PADDED_Y_VALUE

def rankNet_weightByGTDiff(y_pred, y_true, padded_value_indicator=PADDED_Y_VALUE):
    """
    Wrapper for RankNet employing weighing by the differences of ground truth values.
    :param y_pred: predictions from the model, shape [batch_size, slate_length]
    :param y_true: ground truth labels, shape [batch_size, slate_length]
    :param padded_value_indicator: an indicator of the y_true index containing a padded item, e.g. -1
    :return: loss value, a torch.Tensor
    """
    return rankNet(y_pred, y_true, padded_value_indicator, weight_by_diff=True)


def rankNet_weightByGTDiff_pow(y_pred, y_true, padded_value_indicator=PADDED_Y_VALUE):
    """
    Wrapper for RankNet employing weighing by the squared differences of ground truth values.
    :param y_pred: predictions from the model, shape [batch_size, slate_length]
    :param y_true: ground truth labels, shape [batch_size, slate_length]
    :param padded_value_indicator: an indicator of the y_true index containing a padded item, e.g. -1
    :return: loss value, a torch.Tensor
    """
    return rankNet(y_pred, y_true, padded_value_indicator, weight_by_diff=False, weight_by_diff_powed=True)


def rankNet(y_pred, y_true, padded_value_indicator=PADDED_Y_VALUE, weight_by_diff=False, weight_by_diff_powed=False):
    """
    RankNet loss introduced in "Learning to Rank using Gradient Descent".
    :param y_pred: predictions from the model, shape [batch_size, slate_length]
    :param y_true: ground truth labels, shape [batch_size, slate_length]
    :param weight_by_diff: flag indicating whether to weight the score differences by ground truth differences.
    :param weight_by_diff_powed: flag indicating whether to weight the score differences by the squared ground truth differences.
    :return: loss value, a torch.Tensor
    """
    y_pred = y_pred.clone()
    y_true = y_true.clone()
    mask = y_true == padded_value_indicator
    y_pred[mask] = float('-inf')
    y_true[mask] = float('-inf')
    document_pairs_candidates = list(product((range(y_true.shape[1])), repeat=2))
    pairs_true = y_true[:, document_pairs_candidates]
    selected_pred = y_pred[:, document_pairs_candidates]
    true_diffs = pairs_true[:, :, 0] - pairs_true[:, :, 1]
    pred_diffs = selected_pred[:, :, 0] - selected_pred[:, :, 1]
    the_mask = (true_diffs > 0) & ~torch.isinf(true_diffs)
    pred_diffs = pred_diffs[the_mask]
    weight = None
    if weight_by_diff:
        abs_diff = torch.abs(true_diffs)
        weight = abs_diff[the_mask]
    else:
        if weight_by_diff_powed:
            true_pow_diffs = torch.pow(pairs_true[:, :, 0], 2) - torch.pow(pairs_true[:, :, 1], 2)
            abs_diff = torch.abs(true_pow_diffs)
            weight = abs_diff[the_mask]
        true_diffs = (true_diffs > 0).type(torch.float32)
        true_diffs = true_diffs[the_mask]
        return BCEWithLogitsLoss(weight=weight)(pred_diffs, true_diffs)