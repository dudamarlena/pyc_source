# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/min_max_test.py
# Compiled at: 2020-03-28 00:57:59
# Size of source mod 2**32: 214 bytes
import dosk.algo as algo

def test_min():
    values = (2, 3, 1, 4, 6)
    val = algo.min(values)
    assert val == 1


def test_max():
    values = (2, 3, 1, 4, 6)
    val = algo.max(values)
    assert val == 6