# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/makism/Github/dyconnmap-public-master/tests/test_clustering.py
# Compiled at: 2020-01-23 04:24:20
# Size of source mod 2**32: 3349 bytes
"""
Test the synchronization time series as computed from classes PhaseSync and XFreqCoupling.
Also, from the all tests the Time Varying Functional Connectivity Graphs are also computed.

- two tests using the class PhaseSync (two channels, PLV)
- two tests using the class XFreqCoupling (multiple channels, PAC, PLV)
- two tests using the class XFreqCoupling (multiple channels, multiple high frequency bands, PAC, PLV)

"""
import nose
from nose import tools
import scipy as sp
from scipy import io
import numpy as np
from numpy import testing
import sklearn
from sklearn import datasets
import dyconnmap
from dyconnmap import cluster
rng = None
data = None

def initialize():
    global data
    global rng
    rng = np.random.RandomState(seed=0)
    data, _ = sklearn.datasets.make_moons(n_samples=1024, noise=0.125, random_state=rng)


@nose.tools.with_setup(initialize)
def test_clustering_ng():
    ng = dyconnmap.cluster.NeuralGas(rng=rng).fit(data)
    protos = ng.protos
    _, symbols = ng.encode(data)
    result_protos = np.load('data/test_clustering_ng_protos.npy')
    np.testing.assert_array_almost_equal(protos, result_protos)
    result_symbols = np.load('data/test_clustering_ng_symbols.npy')
    np.testing.assert_array_almost_equal(symbols, result_symbols)


@nose.tools.with_setup(initialize)
def test_clustering_rng():
    reng = dyconnmap.cluster.RelationalNeuralGas(n_protos=10,
      iterations=100,
      rng=rng).fit(data)
    protos = reng.protos
    _, symbols = reng.encode(data)
    result_protos = np.load('data/test_clustering_rng_protos.npy')
    np.testing.assert_array_almost_equal(protos, result_protos)
    result_symbols = np.load('data/test_clustering_rng_symbols.npy')
    np.testing.assert_array_almost_equal(symbols, result_symbols)


@nose.tools.with_setup(initialize)
def test_clustering_mng():
    protos = dyconnmap.cluster.MergeNeuralGas(rng=rng).fit(data).protos
    result_protos = np.load('data/test_clustering_mng_protos.npy')
    np.testing.assert_array_almost_equal(protos, result_protos)


@nose.tools.with_setup(initialize)
def test_clustering_gng():
    gng = dyconnmap.cluster.GrowingNeuralGas(rng=rng)
    gng.fit(data)
    protos = gng.protos
    encoding, symbols = gng.encode(data)
    result_protos = np.load('data/test_clustering_gng_protos.npy')
    np.testing.assert_array_almost_equal(protos, result_protos)
    result_symbols = np.load('data/test_clustering_gng_symbols.npy')
    np.testing.assert_array_almost_equal(symbols, result_symbols)


@nose.tools.with_setup(initialize)
def test_clustering_som():
    protos = dyconnmap.cluster.SOM(grid=(8, 4), rng=rng).fit(data).weights
    result_protos = np.load('data/test_clustering_som_protos.npy')
    np.testing.assert_array_almost_equal(protos, result_protos)


@nose.tools.with_setup(initialize)
def test_clustering_som_umatrix():
    protos = dyconnmap.cluster.SOM(grid=(8, 4), rng=rng).fit(data).weights
    umatrix = dyconnmap.cluster.umatrix(protos)
    result_umatrix = np.load('data/test_clustering_som_umatrix.npy')
    np.testing.assert_array_equal(umatrix, result_umatrix)