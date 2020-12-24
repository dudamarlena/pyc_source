# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/tests/test_util.py
# Compiled at: 2019-03-29 13:46:33
# Size of source mod 2**32: 299 bytes


def sanity(x):
    return x + 1


def test_sanity():
    assert sanity(1) == 2