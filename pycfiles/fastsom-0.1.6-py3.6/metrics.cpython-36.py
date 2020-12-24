# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fastsom/interp/metrics.py
# Compiled at: 2020-04-24 11:45:18
# Size of source mod 2**32: 4388 bytes
"""
SOM statistics for various purpouses.
"""
import torch, numpy as np
from torch import Tensor
from typing import Tuple
from fastsom.som import Som, pdist
from ..core import expanded_op, idxs_2d_to_1d, idxs_1d_to_2d
__all__ = [
 'cluster_stats',
 'codebook_err',
 'mean_quantization_err',
 'topologic_err']

def cluster_stats(x: Tensor, som: Som) -> Tuple[float]:
    """Calculates cluster statistics for a Self-Organizing Map."""
    som.eval()
    preds = idxs_2d_to_1d(som.forward(x.cuda()), som.weights.shape[0]).cuda()
    w = som.weights.view(-1, som.weights.shape[(-1)]).cuda()
    uniques, inverse, counts = preds.unique(dim=0, return_inverse=True, return_counts=True)
    distances = (w[preds] - x.cuda()).pow(2).sum(-1).sqrt()
    max_distances = []
    for b in uniques:
        idxs = (inverse == b).nonzero()
        if idxs.nelement() > 0:
            cluster_max_dist = distances[preds[idxs.squeeze(-1)]].max()
            max_distances.append(cluster_max_dist.cpu().numpy())

    empty_clusters_count = w.shape[0] - len(uniques)
    return (counts.float().std().log().cpu().numpy(), np.mean(max_distances), float(empty_clusters_count))


def codebook_err(pred_b: Tensor, yb: Tensor, som: Som=None) -> Tensor:
    """Counts the number of records not belonging to each cluster that are closer than that cluster's furthest record."""
    xb = som._recorder['xb']
    w = som.weights.view(-1, xb.shape[(-1)])
    distances = expanded_op(xb, w.to(device=(xb.device)), pdist)
    row_sz = som.size[0]
    preds = idxs_2d_to_1d(pred_b, row_sz)
    n_classes = som.size[0] * som.size[1]
    batch_size = xb.shape[0]
    count = 0
    _, inverse = preds.unique(dim=0, return_inverse=True)
    for cluster_idx in range(n_classes):
        cluster_distances = distances[(inverse == cluster_idx).nonzero().view(-1)]
        if len(cluster_distances) > 0:
            max_cluster_distance = cluster_distances[:, cluster_idx].max()
            non_cluster_distances = distances[(inverse != cluster_idx).nonzero().view(-1)]
            count += (non_cluster_distances[:, cluster_idx] < max_cluster_distance).nonzero().shape[0]

    return torch.tensor(count / n_classes / batch_size).to(device=(xb.device))


def mean_quantization_err(pred_b: Tensor, yb: Tensor, som: Som=None) -> Tensor:
    """Mean distance of each record from its respective BMU."""
    xb = som._recorder['xb']
    w = som.weights.view(-1, xb.shape[(-1)]).to(device=(xb.device))
    row_sz = som.size[0]
    preds = idxs_2d_to_1d(pred_b, row_sz)
    return pdist(xb, (w[preds]), p=2).mean()


def topologic_err(pred_b: Tensor, yb: Tensor, som: Som=None, thresh: int=4) -> Tensor:
    """
    Min vec distance of each record with every class and checks if the second-to-min value belongs in the first-best neighborhood.
    If not, it gets added as an error.
    """
    xb = som._recorder['xb']
    distances = expanded_op(xb, som.weights.view(-1, xb.shape[(-1)]), pdist)
    _, closest_2_indices = distances.topk(2, largest=False, sorted=True, dim=(-1))
    col_sz = som.size[1]
    top_2_2d_idxs = idxs_1d_to_2d(closest_2_indices.cpu().numpy(), col_sz).float()
    map_distances = pdist((top_2_2d_idxs[:, 0]), (top_2_2d_idxs[:, 1]), p=2)
    return (map_distances >= thresh).int().float().sum(-1).to(device=(xb.device))