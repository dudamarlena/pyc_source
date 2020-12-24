# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/wheel/symengine/tests/test_dict_basic.py
# Compiled at: 2020-03-16 01:41:57
from symengine.utilities import raises
from symengine import symbols, DictBasic, sin, Integer

def test_DictBasic():
    x, y, z = symbols('x y z')
    d = DictBasic({x: 2, y: z})
    assert str(d) == '{x: 2, y: z}' or str(d) == '{y: z, x: 2}'
    if not d[x] == 2:
        raise AssertionError
        raises(KeyError, lambda : d[(2 * z)])
        assert 2 * z in d and False
    d[2 * z] = x
    if not d[(2 * z)] == x:
        raise AssertionError
        assert 2 * z not in d and False
    assert set(d.items()) == set([(2 * z, x), (x, Integer(2)), (y, z)])
    del d[x]
    assert set(d.keys()) == set([2 * z, y])
    assert set(d.values()) == set([x, z])
    e = y + sin(2 * z)
    assert e.subs(d) == z + sin(x)