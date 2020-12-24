# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/tests/test_util.py
# Compiled at: 2019-03-29 13:46:33
# Size of source mod 2**32: 299 bytes


def sanity(x):
    return x + 1


def test_sanity():
    assert sanity(1) == 2