# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/test_collection.py
# Compiled at: 2007-05-18 21:14:46
from mkcode import collector, registry

def test_distutils_collection():
    distutils_ns = collector.collect_from_distutils()
    assert isinstance(distutils_ns, registry.Namespace)
    assert distutils_ns.install
    assert distutils_ns.test