# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\test\test_pickle.py
# Compiled at: 2013-01-14 06:47:43
__doc__ = 'Tests for pickling Cellmlmodel objects.'
import pickle, numpy as np
from cgp.physmod.cellmlmodel import Cellmlmodel
from cgp.virtexp.elphys.paceable import Paceable
from nose.tools import raises

class Model(Cellmlmodel, Paceable):
    """Example model class."""


def test_pickle():
    """Pickling a Cellmlmodel mixing in Paceable."""
    old = Model(workspace='tentusscher_noble_noble_panfilov_2004', rename={'y': {'Na_i': 'Nai', 'Ca_i': 'Cai', 'K_i': 'Ki'}, 'p': {'IstimStart': 'stim_start', 
             'IstimEnd': 'stim_end', 
             'IstimAmplitude': 'stim_amplitude', 
             'IstimPeriod': 'stim_period', 
             'IstimPulseDuration': 'stim_duration'}}, use_cython=True)
    s = pickle.dumps(old)
    new = pickle.loads(s)
    for desired, actual in zip(old.integrate(), new.integrate()):
        np.testing.assert_array_equal(desired, actual)


@raises(pickle.PicklingError)
def test_pickle_nested():
    """Pickling a nested class doesn't work."""

    class Nested(Cellmlmodel, Paceable):
        """A nested class."""

    old = Nested(workspace='tentusscher_noble_noble_panfilov_2004', rename={'y': {'Na_i': 'Nai', 'Ca_i': 'Cai', 'K_i': 'Ki'}, 'p': {'IstimStart': 'stim_start', 
             'IstimEnd': 'stim_end', 
             'IstimAmplitude': 'stim_amplitude', 
             'IstimPeriod': 'stim_period', 
             'IstimPulseDuration': 'stim_duration'}}, use_cython=True)
    _ = pickle.dumps(old)