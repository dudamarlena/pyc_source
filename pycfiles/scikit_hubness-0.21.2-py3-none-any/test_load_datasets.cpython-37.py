# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/data/tests/test_load_datasets.py
# Compiled at: 2019-08-29 04:04:59
# Size of source mod 2**32: 337 bytes
from skhubness.data import load_dexter

def test_load_dexter():
    X, y = load_dexter()
    n_samples = 300
    n_features = 20000
    assert X.shape == (n_samples, n_features), f"Wrong shape: X.shape = {X.shape}, should be (300, 20_000)."
    assert y.shape == (n_samples,), f"Wrong shape: y.shape = {y.shape}, should be (300, )."