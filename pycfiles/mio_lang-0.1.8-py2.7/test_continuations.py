# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/core/test_continuations.py
# Compiled at: 2013-12-08 17:19:04


def test(mio):
    mio.eval('i = 0')
    assert mio.eval('x = Continuation current; i += 1')
    assert mio.eval('i == 1')
    mio.eval('x()')
    assert mio.eval('i == 2')


def test2(mio):
    x = mio.eval('x = Continuation current')
    assert mio.eval('x') == x