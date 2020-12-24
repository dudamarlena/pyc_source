# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aeolus/tests/test_const.py
# Compiled at: 2019-11-04 07:32:32
# Size of source mod 2**32: 2261 bytes
"""Test calc submodule."""
from pathlib import Path
from aeolus import const
from aeolus.exceptions import ArgumentError, LoadError
import iris
import numpy.testing as npt
import pytest
TST_DATA = Path(__file__).parent / 'data'
CONST_FILE = 'dummy'

def test_init_const_general():
    """Test init_const function w/o arguments."""
    cnsts = const.init_const()
    assert str(cnsts).startswith('GeneralConstants')
    assert isinstance(cnsts, const.const.ConstContainer)
    for key in cnsts.__dataclass_fields__.keys():
        attr = getattr(cnsts, key)
        assert isinstance(attr, const.const.ScalarCube)
        assert attr.ndim == 0
    else:
        key = 'stefan_boltzmann'
        assert key in cnsts.__dataclass_fields__
        cube = getattr(cnsts, key)
        assert cube.units == 'W m-2 K-4'
        npt.assert_allclose(cube.data, 5.670367e-08)


def test_loaderror():
    """Test raising LoadError."""
    with pytest.raises(LoadError):
        const.init_const(CONST_FILE)
    with pytest.raises(LoadError):
        const.init_const(CONST_FILE, directory=(TST_DATA / 'nonexistent_directory'))


def test_argumenterror():
    """Test raising ArgumentError."""
    with pytest.raises(ArgumentError):
        const.init_const(CONST_FILE, directory=(str(TST_DATA)))


def test_init_const_custom():
    """Test init_const function with a custom JSON file."""
    cnsts = const.init_const(CONST_FILE, directory=TST_DATA)
    assert str(cnsts).startswith('DummyConstants')
    assert isinstance(cnsts, const.const.ConstContainer)
    for key in cnsts.__dataclass_fields__.keys():
        attr = getattr(cnsts, key)
        assert isinstance(attr, iris.cube.Cube)
        assert attr.ndim == 0
    else:
        key = 'my_constant'
        assert key in cnsts.__dataclass_fields__
        cube = getattr(cnsts, key)
        assert cube.units == 'm s-1'
        npt.assert_allclose(cube.data, 123)


def test_scalarcube():
    """Test ScalarCube."""
    name = 'physical_constant'
    cube = iris.cube.Cube(data=(-123.456), units='m', long_name=name)
    scube = const.const.ScalarCube.from_cube(cube)
    assert isinstance(scube.asc, iris.coords.AuxCoord)
    npt.assert_allclose(scube.data, scube.asc.points.squeeze())
    assert scube.asc.long_name == name