# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/datasets/tests/test_samples_generator.py
# Compiled at: 2019-12-09 07:12:30
# Size of source mod 2**32: 986 bytes
from getml.datasets import make_numerical, make_categorical, make_discrete

def test_make_numerical():
    population, peripheral = make_numerical(n_rows_population=10,
      n_rows_peripheral=40,
      random_state=2309)
    assert population.shape == (10, 4)
    assert peripheral.shape == (40, 3)
    assert population['targets'][0] == 1


def test_make_categorical():
    population, peripheral = make_categorical(n_rows_population=10,
      n_rows_peripheral=50,
      random_state=2309)
    assert population.shape == (10, 4)
    assert peripheral.shape == (50, 3)
    assert population['targets'][0] == 4


def test_make_discrete():
    population, peripheral = make_discrete(n_rows_population=10,
      n_rows_peripheral=50,
      random_state=2309)
    assert population.shape == (10, 4)
    assert peripheral.shape == (50, 3)
    assert population['targets'][0] == 1