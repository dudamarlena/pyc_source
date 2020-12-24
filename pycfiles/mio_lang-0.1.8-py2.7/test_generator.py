# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/core/test_generator.py
# Compiled at: 2013-12-08 17:19:04
from pytest import raises
from mio.errors import StopIteration

def test_generator(mio):
    mio.eval('foo = block(\n        yield 1\n        yield 2\n        yield 3\n    )')
    mio.eval('f = foo()')
    assert mio.eval('next(f)') == 1
    assert mio.eval('next(f)') == 2
    assert mio.eval('next(f)') == 3
    with raises(StopIteration):
        mio.eval('next(f)', reraise=True)