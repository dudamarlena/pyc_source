# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/examples/tests/test_kvpairs.py
# Compiled at: 2019-05-28 16:55:28
# Size of source mod 2**32: 457 bytes
from parsr.examples.kvpairs import loads
DATA = '\n# this is a config file\na = 15\nb = a string\nvalueless\nd = 1.14\n\n# another section\n+valueless  # no value\ne = hello   # a value\n#\n'

def test_kvpairs():
    d = loads(DATA)
    if not d:
        raise AssertionError
    else:
        if not d['a'].value == 15:
            raise AssertionError
        else:
            if not d['b'].value == 'a string':
                raise AssertionError
            else:
                assert d['valueless'].value is None
                assert d['d'].value == 1.14
            assert d['+valueless'].value is None
        assert d['e'].value == 'hello'