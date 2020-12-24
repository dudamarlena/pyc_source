# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/types/test_boolean.py
# Compiled at: 2013-11-18 07:03:57


def test_boolean(mio):
    assert mio.eval('Boolean').value is None
    assert mio.eval('True')
    assert not mio.eval('False')
    assert mio.eval('None').value is None
    return


def test_init(mio):
    assert mio.eval('Boolean clone() is Boolean')
    assert mio.eval('True clone() is True')
    assert mio.eval('False clone() is False')
    assert mio.eval('None clone() is None')


def test_repr(mio):
    assert mio.eval('Boolean __repr__()') == repr(None)
    assert mio.eval('True __repr__()') == repr(True)
    assert mio.eval('False __repr__()') == repr(False)
    assert mio.eval('None __repr__()') == repr(None)
    return