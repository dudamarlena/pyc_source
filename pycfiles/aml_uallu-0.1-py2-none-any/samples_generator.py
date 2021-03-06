# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/amltlearn/datasets/samples_generator.py
# Compiled at: 2016-09-20 11:24:51
__doc__ = '\n.. module:: samples_generator\n\nsamples_generator\n*************\n\n:Description: samples_generator\n\n    \n\n:Authors: bejar\n    \n\n:Version: \n\n:Created on: 21/01/2015 9:02 \n\n'
__author__ = 'bejar'
import numpy as np, numbers
from sklearn.utils import check_random_state, check_array

def make_blobs(n_samples=100, n_features=2, centers=3, cluster_std=1.0, center_box=(-10.0, 10.0), shuffle=True, random_state=None):
    """Generate isotropic Gaussian blobs for clustering.

    7/10/2015
    A fixed and more flexible version of the scikit-learn function

    Parameters
    ----------
    n_samples : int, or sequence of integers, optional (default=100)
        The total number of points equally divided among clusters.
        or a sequence of the number of examples of each cluster

    n_features : int, optional (default=2)
        The number of features for each sample.

    centers : int or array of shape [n_centers, n_features], optional
        (default=3)
        The number of centers to generate, or the fixed center locations.

    cluster_std: float or sequence of floats, optional (default=1.0)
        The standard deviation of the clusters.
        now works for the list of floats

    center_box: pair of floats (min, max), optional (default=(-10.0, 10.0))
        The bounding box for each cluster center when centers are
        generated at random.

    shuffle : boolean, optional (default=True)
        Shuffle the samples.

    random_state : int, RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.

    Returns
    -------
    X : array of shape [n_samples, n_features]
        The generated samples.

    y : array of shape [n_samples]
        The integer labels for cluster membership of each sample.

    Examples
    --------
    >>> from sklearn.datasets.samples_generator import make_blobs
    >>> X, y = make_blobs(n_samples=10, centers=3, n_features=2,
    ...                   random_state=0)
    >>> print(X.shape)
    (10, 2)
    >>> y
    array([0, 0, 1, 0, 2, 2, 2, 1, 1, 0])
    """
    generator = check_random_state(random_state)
    if isinstance(centers, numbers.Integral):
        centers = generator.uniform(center_box[0], center_box[1], size=(
         centers, n_features))
    else:
        centers = check_array(centers)
        n_features = centers.shape[1]
    X = []
    y = []
    n_centers = centers.shape[0]
    if not isinstance(n_samples, list):
        n_samples_per_center = [
         int(n_samples // n_centers)] * n_centers
        for i in range(n_samples % n_centers):
            n_samples_per_center[i] += 1

    else:
        if len(n_samples) != n_centers:
            raise NameError('List of number of examples per center doer not match number of centers')
        n_samples_per_center = n_samples
        n_samples = sum(n_samples)
    if not isinstance(cluster_std, list):
        std_list = [
         cluster_std] * centers.shape[0]
    else:
        if len(cluster_std) != n_centers:
            raise NameError('List of number of examples per center doer not match number of centers')
        std_list = cluster_std
    for i, (n, st) in enumerate(zip(n_samples_per_center, std_list)):
        X.append(centers[i] + generator.normal(scale=st, size=(
         n, n_features)))
        y += [i] * n

    X = np.concatenate(X)
    y = np.array(y)
    if shuffle:
        indices = np.arange(n_samples)
        generator.shuffle(indices)
        X = X[indices]
        y = y[indices]
    return (
     X, y)