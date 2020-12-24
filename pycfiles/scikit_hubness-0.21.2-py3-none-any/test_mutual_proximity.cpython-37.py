# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/reduction/tests/test_mutual_proximity.py
# Compiled at: 2019-09-20 05:21:31
# Size of source mod 2**32: 3619 bytes
import pytest, numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.utils.testing import assert_raises
from skhubness.reduction import MutualProximity
from skhubness.neighbors import NearestNeighbors
METHODS = [
 'normal', 'exact']
ALLOWED_METHODS = [
 'exact', 'empiric', 'normal', 'gaussi']

def test_correct_mp_empiric():
    X, y = make_classification(n_samples=120, n_features=10, random_state=1234)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=20)
    nn = NearestNeighbors(n_neighbors=20)
    nn.fit(X_train, y_train)
    neigh_dist_train, neigh_ind_train = nn.kneighbors()
    neigh_dist_test, neigh_ind_test = nn.kneighbors(X_test)
    mp = MutualProximity(method='empiric')
    mp.fit(neigh_dist_train, neigh_ind_train, X=None, assume_sorted=True)
    mp_dist_test, mp_ind_test = mp.transform(neigh_dist_test, neigh_ind_test, X=None, assume_sorted=True)
    mp_dist_test_correct = np.empty_like(neigh_dist_test, dtype=float)
    mp_ind_test_correct = np.empty_like(neigh_ind_test, dtype=int)
    n_test, n_train = neigh_ind_test.shape
    for x in range(n_test):
        for y in range(n_train):
            idx = neigh_ind_test[(x, y)]
            d_xy = neigh_dist_test[(x, y)]
            set1 = set()
            set2 = set()
            for j, d_xj in zip(neigh_ind_test[x, :], neigh_dist_test[x, :]):
                if d_xj > d_xy:
                    set1.add(j)

            for j in neigh_ind_test[x, :]:
                k = np.argwhere(neigh_ind_train[idx] == j).ravel()
                d_yj = neigh_dist_train[(idx, k)] if k.size else neigh_dist_train[(idx, -1)] + 1e-06
                if d_yj > d_xy:
                    set2.add(j)

            mp_dist_test_correct[(x, y)] = 1 - len(set1.intersection(set2)) / n_train
            mp_ind_test_correct[(x, y)] = idx

    np.testing.assert_array_almost_equal(mp_dist_test, mp_dist_test_correct)
    np.testing.assert_array_equal(mp_ind_test, mp_ind_test_correct)


@pytest.mark.parametrize('method', METHODS)
@pytest.mark.parametrize('verbose', [0, 1])
def test_mp_runs_without_error(method, verbose):
    X, y = make_classification(n_samples=20, n_features=10)
    nn = NearestNeighbors()
    nn.fit(X, y)
    neigh_dist, neigh_ind = nn.kneighbors()
    mp = MutualProximity(method=method, verbose=verbose)
    _ = mp.fit(neigh_dist, neigh_ind, X, assume_sorted=True).transform(neigh_dist,
      neigh_ind, X, assume_sorted=True)


@pytest.mark.parametrize('method', ['invalid', None])
def test_invalid_method(method):
    X, y = make_classification(n_samples=10)
    nn = NearestNeighbors()
    nn.fit(X, y)
    neigh_dist, neigh_ind = nn.kneighbors()
    mp = MutualProximity(method=method)
    with assert_raises(ValueError):
        mp.fit(neigh_dist, neigh_ind, X, assume_sorted=True)