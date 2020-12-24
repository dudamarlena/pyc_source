# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_lib/test/test_lib.py
# Compiled at: 2017-05-10 17:49:05


def test_flatten():
    from toil_lib import flatten
    x = [
     (1, 2), (3, 4, (5, 6))]
    y = (1, (2, (3, 4, 5)))
    assert flatten(x) == [1, 2, 3, 4, 5, 6]
    assert flatten(y) == [1, 2, 3, 4, 5]


def test_partitions():
    from toil_lib import partitions
    x = [ z for z in xrange(100) ]
    assert len(list(partitions(x, 10))) == 10
    assert len(list(partitions(x, 20))) == 5
    assert len(list(partitions(x, 100))) == 1
    assert list(partitions([], 10)) == []