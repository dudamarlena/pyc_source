# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/bird/tests/test_bird.py
# Compiled at: 2014-10-01 09:21:00
import numpy as np
from numpy.testing import assert_array_almost_equal
from bird import bird, s_bird
from scipy import linalg

def _make_doppler(N):
    x = np.linspace(0, 1, N)
    doppler = np.sqrt(x * (1 - x)) * np.sin(2.1 * np.pi / (x + 0.05))
    return doppler.reshape((1, N))


def test_bird():
    """ test bird calls """
    N = 1024
    scales = [32, 64, 128, 256]
    M = np.sum(np.array(scales) / 2) * N
    n_runs = 30
    verbose = False
    p_above = 1.0 / M
    rng = np.random.RandomState(42)
    target_snr = 5
    X = _make_doppler(N)
    X = X / linalg.norm(X)
    truth = X.copy()
    noise = rng.randn(*truth.shape)
    noise = 0.3 * np.exp(-float(target_snr) / 10.0) * noise / linalg.norm(noise)
    data = X + noise
    X_denoised = bird(data, scales, n_runs, p_above=p_above, random_state=42, n_jobs=1, verbose=verbose)
    assert_array_almost_equal(X_denoised, truth, decimal=2)
    X_denoised_again = bird(data, scales, n_runs, p_above=p_above, random_state=42, n_jobs=1, verbose=verbose)
    assert_array_almost_equal(X_denoised, X_denoised_again, decimal=8)


def test_sbird():
    """ test s-bird calls """
    N = 1024
    scales = [32, 64, 128, 256]
    M = np.sum(np.array(scales) / 2) * N
    n_runs = 10
    n_channels = 5
    verbose = False
    p_above = 1.0 / M
    rng = np.random.RandomState(42)
    target_snr = 5
    X = _make_doppler(N)
    X = X / linalg.norm(X)
    X = np.tile(X, [n_channels, 1])
    truth = X.copy()
    data = np.zeros_like(X)
    for chan in range(X.shape[0]):
        noise = rng.randn(*truth[chan, :].shape)
        noise = 0.3 * np.exp(-float(target_snr) / 10.0) * noise / linalg.norm(noise)
        data[chan, :] = X[chan, :] + noise

    X_denoised = s_bird(data, scales, n_runs, p_above=p_above, random_state=42, n_jobs=1, verbose=verbose)
    assert_array_almost_equal(X_denoised, truth, decimal=2)