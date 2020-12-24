# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fastsom/learn/initializers.py
# Compiled at: 2020-04-24 11:45:18
# Size of source mod 2**32: 2098 bytes
"""
Initializers are used to define
initial map weights for Self-Organizing Maps.
"""
from torch import Tensor
from kmeans_pytorch import kmeans as _kmeans
import torch
__all__ = [
 'som_initializers',
 'WeightsInitializer',
 'KMeansInitializer',
 'RandomInitializer']

class WeightsInitializer:
    __doc__ = 'Weight initializer base class.'

    def __call__(self, x: Tensor, k: int, **kwargs) -> Tensor:
        raise NotImplementedError


class KMeansInitializer(WeightsInitializer):
    __doc__ = "\n    Initializes weights using K-Means.\n\n    Parameters\n    ----------\n    distance : str default='euclidean'\n        The type of distance function to be used. Can be `euclidean` or `cosine`.\n    "

    def __init__(self, distance: str='euclidean'):
        self.distance = distance
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    def __call__(self, x: Tensor, k: int, **kwargs) -> Tensor:
        """
        Calculates K-Means on `x` and returns the centroids.

        Parameters
        ----------
        x : Tensor
            The input data.
        k: int
            The number of weights to be returned.
        """
        _, cluster_centers = _kmeans(X=x, num_clusters=k, distance=(self.distance), device=(self.device))
        return cluster_centers


class RandomInitializer(WeightsInitializer):
    __doc__ = '\n    Initializes weights randomly.\n    '

    def __call__(self, x: Tensor, k: int, **kwargs) -> Tensor:
        """
        Uniform random  weight initialization.

        Parameters
        ----------
        x: Tensor
            The input data.
        k: int
            The number of weights to be returned.
        """
        x_min = x.min(dim=0)[0]
        x_max = x.max(dim=0)[0]
        return (x_max - x_min) * torch.zeros(k, x.shape[(-1)]).uniform_(0, 1) - x_min


som_initializers = {'random':RandomInitializer(), 
 'kmeans':KMeansInitializer(), 
 'kmeans_cosine':KMeansInitializer(distance='cosine')}