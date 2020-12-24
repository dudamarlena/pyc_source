# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fastsom/som/som.py
# Compiled at: 2020-04-24 11:45:18
# Size of source mod 2**32: 10933 bytes
"""
This module contains the base SOM module.
"""
import torch
from torch import Tensor
from fastai.torch_core import Module
from functools import partial
from typing import Tuple, Callable
from ..core import index_tensor, expanded_op, ifnone
__all__ = [
 'Som',
 'neigh_gauss',
 'neigh_square',
 'neigh_rhomb',
 'neigh_diff_standard',
 'neigh_diff_toroidal',
 'pnorm',
 'pdist',
 'pcosim',
 'manhattan_dist']
SomSize2D = Tuple[(int, int, int)]

def pcosim(a: Tensor, b: Tensor, p: int=2) -> Tensor:
    """
    Calculates the cosine similarity of order `p` between `a` and `b`.
    Assumes tensor shapes are compatible.

    Parameters
    ----------
    a : Tensor
        The first tensor
    b : Tensor
        The second tensor
    p : int default=2
        The order.
    """
    return (a * b).sum(-1) / pnorm(a, p=p) * pnorm(b, p=p)


def pnorm(a: Tensor, p: int=2) -> Tensor:
    """
    Calculates the norm of order `p` of tensor `a`.

    Parameters
    ----------
    a : Tensor
        The input tensor
    p : int default=2
        The order.
    """
    return a.abs().pow(p).sum(-1).pow(1 / p)


def pdist(a: Tensor, b: Tensor, p: int=2) -> Tensor:
    """
    Calculates the distance of order `p` between `a` and `b`.
    Assumes tensor shapes are compatible.

    Parameters
    ----------
    a : Tensor
        The first tensor
    b : Tensor
        The second tensor
    p : int default=2
        The order.
    """
    return pnorm((a - b), p=p)


def manhattan_dist(a: Tensor, b: Tensor) -> Tensor:
    """
    Calculates the Manhattan distance (order 1 p-distance) between `a` and `b`.
    Assumes tensor shapes are compatible.

    Parameters
    ----------
    a : Tensor
        The first tensor
    b : Tensor
        The second tensor
    p : int default=2
        The order.
    """
    return pdist(a, b, p=1)


def neigh_gauss(position_diff: Tensor, sigma: Tensor) -> Tensor:
    """
    Gaussian neighborhood scaling function based on center-wise         diff `position_diff` and radius `sigma`.

    Parameters
    ----------
    position_diff : Tensor
        The positional difference around some center.
    sigma : Tensor
        The scaling radius.
    """
    v = pnorm(position_diff, p=2)
    return torch.exp(torch.neg(v.pow(2) / sigma.pow(2)))


def neigh_rhomb(position_diff: Tensor, sigma: Tensor) -> Tensor:
    """
    Diamond-shaped neighborhood function based on center-wise diff `position_diff` and radius `sigma`.
    Note: Manhattan distance should be used with this function.

    Parameters
    ----------
    position_diff : Tensor
        The positional difference around some center.
    sigma : Tensor
        The scaling radius.
    """
    v = pnorm(position_diff, p=1)
    return torch.exp(torch.neg(torch.sqrt(v) / sigma))


def neigh_square(position_diff: Tensor, sigma: Tensor) -> Tensor:
    """
    Square-shaped neighborhood scaling function based on center-wise diff `position_diff` and radius `sigma`.

    Parameters
    ----------
    position_diff : Tensor
        The positional difference around some center.
    sigma : Tensor
        The scaling radius.
    """
    v = position_diff.abs().max(-1)[0]
    return torch.exp(torch.neg(v.sqrt() / sigma))


def neigh_diff_standard(bmus: Tensor, positions: Tensor) -> Tensor:
    """
    Positional difference function.
    Computes index difference between Best Matching Units (`bmus`) and `positions`, where `positions` 
    are indices of elements inside the SOM grid.

    Parameters
    ----------
    bmus : Tensor
        The list of Best Matching Units (2D indices)
    positions : Tensor
        The 2D tensor of grid element indices 
    """
    return bmus - positions


def neigh_diff_toroidal(bmus: Tensor, positions: Tensor, map_size: Tuple[(int, int)]=None) -> Tensor:
    """
    Positional difference function.
    Computes toroidal (wraparound) difference between Best Matching Units (`bmus`) and `positions`, where `positions` 
    are indices of elements inside the SOM grid.

    Parameters
    ----------
    bmus : Tensor
        The list of Best Matching Units (2D indices)
    positions : Tensor
        The 2D tensor of grid element indices
    map_size : Tuple[int, int] = None
        The SOM size. Used to pick shortest distance between indices.
    """
    ms = torch.tensor(map_size)
    dx = (bmus[(Ellipsis, 0)] - positions[(Ellipsis, 0)]).abs().unsqueeze(-1)
    dy = (bmus[(Ellipsis, 1)] - positions[(Ellipsis, 1)]).abs().unsqueeze(-1)
    dx = torch.cat([dx, ms[0] - dx], dim=(-1)).min(dim=(-1), keepdim=True)[0]
    dy = torch.cat([dy, ms[1] - dy], dim=(-1)).min(dim=(-1), keepdim=True)[0]
    return torch.cat([dx, dy], dim=(-1))


class Som(Module):
    __doc__ = '\n    Self-Organizing Map module.\n\n    Parameters\n    ----------\n    size: SomSize2D\n        The 2D map size: (rows, cols, n_features)\n    alpha : float default=0.3\n        The initial alpha hyperparameter. This is usually overwritten by a `SomTrainer`.\n    dist_fn: Callable = pdist\n        The distance function used to compute records-to-codebook distances.\n    neigh_fn: Callable = neigh_gauss\n        The neighbourhood scaling function.\n    neigh_diff_fn: Callable = neigh_diff_standard\n        The neighbourhood difference function. Can be standard or toroidal.\n    '

    def __init__(self, size: SomSize2D, alpha=0.3, dist_fn: Callable=pdist, neigh_fn: Callable=neigh_gauss, neigh_diff_fn: Callable=neigh_diff_standard) -> None:
        self.size = size
        self.lr = torch.tensor([1.0])
        self.alpha = torch.tensor([alpha])
        self.sigma = torch.tensor([max(size[:-1]) / 2.0])
        self.weights = torch.randn(size)
        self.dist_fn, self.neigh_fn, self.neigh_diff_fn = dist_fn, neigh_fn, neigh_diff_fn
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.indices = None
        self.after_weight_init()
        self._recorder = dict()
        if self.neigh_diff_fn.__name__ == 'neigh_diff_toroidal':
            self.neigh_diff_fn = partial((self.neigh_diff_fn), map_size=(self.size[:-1]))

    def forward(self, x: Tensor) -> Tensor:
        """Calculates distances between elements in `x` and `weights`; computes BMUs and returns them."""
        if x.device != self.device:
            x = self._to_device(x)
        else:
            if self.weights.device != self.device:
                self.weights = self._to_device(self.weights)
            distances = self.distance(x, self.weights.view(-1, x.shape[(-1)]))
            bmu_indices = self.find_bmus(distances)
            if self.training:
                self._recorder['diffs'] = self.diff(x, self.weights.view(-1, x.shape[(-1)])).view(x.shape[0], self.size[0], self.size[1], x.shape[(-1)])
                self._recorder['bmus'] = bmu_indices
        self._recorder['xb'] = x.clone()
        return bmu_indices

    def backward(self) -> None:
        """Updates weights based on BMUs and indices calculated in the forward"""
        bmu_indices = self._recorder['bmus']
        elementwise_diffs = self._recorder['diffs']
        batch_size = bmu_indices.shape[0]
        if self.indices is None:
            self.indices = self._to_device(index_tensor(self.size[:-1]).view(-1, 2))
        neigh_multipliers = self.neighborhood(bmu_indices, self.indices, self.sigma)
        delta = neigh_multipliers * self.alpha * elementwise_diffs
        self.weights += delta.sum(dim=0) / batch_size

    def find_bmus(self, distances: Tensor) -> Tensor:
        """
        Finds the BMUs for a batch of distances.

        Input:

        `distances`:  [B, rows*cols]

        

        Output:

        `bmus`:       [B, 2]
        """
        min_idx = distances.argmin(-1)
        bmus = torch.stack([min_idx / self.size[1], min_idx % self.size[1]], dim=1)
        return self._to_device(bmus)

    def distance(self, a: Tensor, b: Tensor) -> Tensor:
        """Calculates the distance between `a` and `b`, expanding their sizes."""
        return expanded_op(a, b, (self.dist_fn), device=(self.device))

    def diff(self, a: Tensor, b: Tensor) -> Tensor:
        """Calculates the difference between `a` and `b`, expanding their sizes."""
        return expanded_op(a, b, (lambda a, b: a - b), device=(self.device))

    def neighborhood(self, bmus: Tensor, indices: Tensor, sigma: Tensor) -> Tensor:
        """Calculates neighborhood multipliers using `neigh_fn`."""
        out_shape = (
         bmus.shape[0], self.size[0], self.size[1], 1)
        return expanded_op((bmus.float()), (indices.float()), (lambda a, b: self.neigh_fn(self.neigh_diff_fn(a, b), sigma)), device=(self.device)).view(out_shape)

    def get_prev_batch_output(self):
        """Retrieves the output of the previous batch in training"""
        if self._diffs is not None:
            if self._bmus is not None:
                return (
                 self._bmus, self._diffs)
        raise RuntimeError(f"`{self.__class__.__name__}.get_prev_batch_output` should only be called during training")

    def after_weight_init(self):
        self.to_device()

    def parameters(self, recurse=True):
        """Returns an iterator over module parameters."""
        return iter([self.alpha, self.sigma])

    def to_device(self, device: torch.device=None) -> None:
        """Moves params and weights to the appropriate device."""
        self.weights = self._to_device((self.weights), device=device)
        self.alpha = self._to_device((self.alpha), device=device)
        self.sigma = self._to_device((self.sigma), device=device)
        self.lr = self._to_device((self.lr), device=device)

    def _to_device(self, a: Tensor, device: torch.device=None) -> Tensor:
        """Moves a tensor to the appropriate device"""
        return a.to(device=(ifnone(device, self.device)))

    def __repr__(self):
        return f"{self.__class__.__name__}(\n            size={self.size[:-1]}, neuron_size={self.size[(-1)]}, alpha={self.alpha}, sigma={self.sigma}),\n            dist_fn={self.dist_fn.__name__}, neigh_fn={self.neigh_fn.__name__}, neigh_diff_fn={self.neigh_diff_fn})"