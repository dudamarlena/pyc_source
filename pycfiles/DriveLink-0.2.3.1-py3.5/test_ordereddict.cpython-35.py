# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_ordereddict.py
# Compiled at: 2017-09-12 20:30:59
# Size of source mod 2**32: 2770 bytes
from drivelink import OrderedDict
import pytest, os

def test_dict():
    dct = OrderedDict('testOrderedDict')
    for i in range(10):
        dct[i] = i

    for i in range(10):
        if not dct[i] == i:
            raise AssertionError


def test_init():
    with pytest.raises(ValueError) as (excinfo):
        OrderedDict('testOrderedDictInit', 0)
    excinfo.match('.* per page.*')
    with pytest.raises(ValueError) as (excinfo):
        OrderedDict('testOrderedDictInit', 1, 0)
    excinfo.match('.* in RAM.*')
    with pytest.raises(IOError) as (excinfo):
        OrderedDict('', 1, 1, '/')
    if not excinfo.value.errno == 13:
        assert excinfo.value[0][0] == 13
    with OrderedDict('testOrderedDictInit', 1, 1):
        pass
    OrderedDict('testOrderedDictInit', 1, 1)


def test_change_settings():
    with OrderedDict('testOrderedDictChangeSettings', 1, 1) as (d):
        d[0] = 1
        d[1] = 'c'
        d[2] = 3.4
    with OrderedDict('testOrderedDictChangeSettings', 2, 2) as (d):
        assert d[0] == 1
        assert d[1] == 'c'
        assert d[2] == 3.4
    with OrderedDict('testOrderedDictChangeSettings', 1, 1) as (d):
        assert d[0] == 1
        assert d[1] == 'c'
        assert d[2] == 3.4


def test_guarantee_page():
    with OrderedDict('testOrderedDictGuaranteePage', 1, 1) as (d):
        d[0] = 1
        d[1] = 'c'
        d[2] = 3.4
        assert d[0] == 1
        assert d[1] == 'c'
        assert d[2] == 3.4


def test_string_funcs():
    d = OrderedDict('testOrderedDictStringFuncs')
    assert str(d).startswith('Dictionary')
    assert str(d).endswith('testOrderedDictStringFuncs')
    assert repr(d).startswith('OrderedDict(')
    assert repr(d).endswith(".DriveLink')")


def test_save():
    d = OrderedDict('testOrderedDictSave', 1, 1)
    d[0] = 1
    d[1] = 'c'
    d[2] = 3.4
    d.close()
    with OrderedDict('testOrderedDictSave', 1, 1) as (d):
        assert d[0] == 1
        assert d[1] == 'c'
        assert d[2] == 3.4


def test_contains():
    with OrderedDict('testOrderedDictContains', 1, 1) as (d):
        d[0] = 1
        d[1] = 'c'
        d[2] = 3.4
        assert 0 in d
        assert 1 in d
        assert 2 in d
        assert 3 not in d
        assert 4 not in d
        assert 5 not in d


def test_save_page():
    with OrderedDict('testOrderedDictSavePage', 1, 1) as (d):
        d[0] = 1
        d[1] = 'c'
        d[2] = 3.4
        assert d[0] == 1
        assert os.path.exists(d._file_base + '0')
        os.remove(d._file_base + '0')
        assert d[1] == 'c'
        assert not os.path.exists(d._file_base + '0')
        with pytest.raises(IOError):
            assert d[0] != 1


if __name__ == '__main__':
    freeze_support()
    ut.main()