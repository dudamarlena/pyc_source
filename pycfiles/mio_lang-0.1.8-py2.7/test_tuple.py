# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/types/test_tuple.py
# Compiled at: 2013-11-11 04:41:49


def test_null(mio):
    assert tuple(iter(mio.eval('Tuple'))) == ()


def test_clone(mio):
    assert mio.eval('Tuple clone()') == ()


def test_repr(mio):
    assert repr(mio.eval('Tuple')) == '()'


def test_repr2(mio):
    mio.eval('xs = (1, 2, 3)')
    assert repr(mio.eval('xs')) == '(1, 2, 3)'


def test_at(mio):
    mio.eval('xs = (1, 2, 3)')
    assert mio.eval('xs') == (1, 2, 3)
    assert mio.eval('xs at(0)') == 1


def test_getitem(mio):
    mio.eval('xs = (1, 2, 3)')
    assert mio.eval('xs') == (1, 2, 3)
    assert mio.eval('xs __getitem__(0)') == 1


def test_len(mio):
    mio.eval('xs = (1, 2, 3)')
    assert mio.eval('xs') == (1, 2, 3)
    assert mio.eval('xs len') == 3


def test_len2(mio):
    mio.eval('xs = (1, 2, 3)')
    assert mio.eval('xs') == (1, 2, 3)
    assert mio.eval('xs __len__()') == 3


def test_len3(mio):
    xs = mio.eval('(1, 2, 3)')
    assert len(xs) == 3


def test_count(mio):
    mio.eval('xs = (1, 2, 3)')
    assert mio.eval('xs') == (1, 2, 3)
    assert mio.eval('xs count(1)') == 1


def test_reversed(mio):
    mio.eval('xs = (1, 2, 3)')
    assert mio.eval('xs') == (1, 2, 3)
    assert mio.eval('xs reversed()') == (3, 2, 1)


def test_sorted(mio):
    mio.eval('xs = (3, 1, 2)')
    assert mio.eval('xs') == (3, 1, 2)
    assert mio.eval('xs sorted()') == (1, 2, 3)