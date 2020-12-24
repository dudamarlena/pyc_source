# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_dict.py
# Compiled at: 2017-09-12 20:37:07
# Size of source mod 2**32: 2567 bytes
from drivelink import Dict
import pytest, os

def test_dict():
    dct = Dict('testDict')
    for i in range(10):
        dct[i] = i

    for i in range(10):
        if not dct[i] == i:
            raise AssertionError


def test_init():
    with pytest.raises(ValueError) as (excinfo):
        Dict('testDictInit', 0)
    excinfo.match('.* per page.*')
    with pytest.raises(ValueError) as (excinfo):
        Dict('testDictInit', 1, 0)
    excinfo.match('.* in RAM.*')
    with pytest.raises(OSError) as (excinfo):
        Dict('', 1, 1, '/New/')
    if not excinfo.value.errno == 13:
        assert excinfo.value[0][0] == 13
    with Dict('testDictInit', 1, 1):
        pass
    Dict('testDictInit', 1, 1)


def test_change_settings():
    with Dict('testDictChangeSettings', 1, 1) as (d):
        d[0] = 1
        d[1] = 'c'
        d[2] = 3.4
    with Dict('testDictChangeSettings', 2, 2) as (d):
        assert d[0] == 1
        assert d[1] == 'c'
        assert d[2] == 3.4
    with Dict('testDictChangeSettings', 1, 1) as (d):
        assert d[0] == 1
        assert d[1] == 'c'
        assert d[2] == 3.4


def test_guarantee_page():
    with Dict('testDictGuaranteePage', 1, 1) as (d):
        d[0] = 1
        d[1] = 'c'
        d[2] = 3.4
        assert d[0] == 1
        assert d[1] == 'c'
        assert d[2] == 3.4


def test_save():
    d = Dict('testDictSave', 1, 1)
    d[0] = 1
    d[1] = 'c'
    d[2] = 3.4
    d.close()
    with Dict('testDictSave', 1, 1) as (d):
        assert d[0] == 1
        assert d[1] == 'c'
        assert d[2] == 3.4


def test_string_funcs():
    d = Dict('testDictStringFuncs')
    assert str(d).startswith('Dictionary')
    assert str(d).endswith('testDictStringFuncs')
    assert repr(d).startswith('Dict(')
    assert repr(d).endswith(".DriveLink')")


def test_change_compression():
    d = Dict('testChangeCompression', 1, 1, compression_ratio=0)
    d[0] = 1
    d[1] = 'c'
    d[2] = 3.4
    d.close()
    with Dict('testChangeCompression', 1, 1, compression_ratio=-1) as (d):
        assert d[0] == 1
        assert d[1] == 'c'
        assert d[2] == 3.4
    with Dict('testChangeCompression', 1, 1, compression_ratio=9) as (d):
        assert d[0] == 1
        assert d[1] == 'c'
        assert d[2] == 3.4


def test_contains():
    with Dict('testDictContains', 1, 1) as (d):
        d[0] = 1
        d[1] = 'c'
        d[2] = 3.4
        assert 0 in d
        assert 1 in d
        assert 2 in d
        assert 3 not in d
        assert 4 not in d
        assert 5 not in d


if __name__ == '__main__':
    freeze_support()
    ut.main()