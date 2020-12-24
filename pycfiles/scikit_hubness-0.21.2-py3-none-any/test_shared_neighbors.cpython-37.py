# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/reduction/tests/test_shared_neighbors.py
# Compiled at: 2019-08-29 04:04:58
# Size of source mod 2**32: 782 bytes
import pytest
from sklearn.datasets import make_classification
from sklearn.exceptions import NotFittedError
from sklearn.utils.testing import assert_raises
from skhubness.reduction.shared_neighbors import SharedNearestNeighbors, SimhubIn
from skhubness.neighbors import NearestNeighbors

@pytest.mark.parametrize('method', [SharedNearestNeighbors, SimhubIn])
def test_snn(method):
    X, y = make_classification()
    nn = NearestNeighbors()
    nn.fit(X, y)
    neigh_dist, neigh_ind = nn.kneighbors()
    snn = method()
    with assert_raises(NotImplementedError):
        snn.fit(neigh_dist, neigh_ind, X, assume_sorted=True)
    with assert_raises(NotFittedError):
        snn.transform(neigh_dist, neigh_ind, X, assume_sorted=True)