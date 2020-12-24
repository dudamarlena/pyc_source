# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsr/examples/tests/test_kvpairs.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsr.examples.kvpairs import loads
DATA = '\n# this is a config file\na = 15\nb = a string\nvalueless\nd = 1.14\n\n# another section\n+valueless  # no value\ne = hello   # a value\n#\n'

def test_kvpairs():
    d = loads(DATA)
    assert d
    assert d['a'].value == 15
    assert d['b'].value == 'a string'
    assert d['valueless'].value is None
    assert d['d'].value == 1.14
    assert d['+valueless'].value is None
    assert d['e'].value == 'hello'
    return