# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/anaconda3/lib/python3.6/site-packages/vnlp/nn/functional.py
# Compiled at: 2018-06-21 18:29:18
# Size of source mod 2**32: 1220 bytes
import torch, numpy as np

def pad(seqs, pad_value=0, device=None):
    """
    pads a list of variable-lengthed lists and returns a padded tensor and a lengths tensor.
    """
    lens = [len(s) for s in seqs]
    max_len = max(lens)
    return (torch.tensor([s + [pad_value] * (max_len - l) for s, l in zip(seqs, lens)], device=device), torch.tensor(lens, device=device))


def mask(lens, invert=False, device=None, total_length=None):
    """
    return a boolean mask of valid positions corresponding to the given lengths.
    """
    max_len = total_length if total_length else lens.max().item()
    valid = False if invert else True
    return torch.tensor([[valid] * l + [not valid] * (max_len - l) for l in lens.tolist()], device=device)


def mask_invalid_scores(scores, lens):
    """
    returns a differentiable version of scores whose invalid positions are masked with `-np.inf`.
    """
    valid = mask(lens, device=(scores.device), total_length=(scores.size(1)))
    while scores.dim() > valid.dim():
        valid = valid.unsqueeze(valid.dim()).expand_as(scores)

    neg = torch.zeros_like(valid, device=(scores.device)).float()
    neg.masked_fill_(1 - valid, -np.inf)
    return scores * valid.float() + neg