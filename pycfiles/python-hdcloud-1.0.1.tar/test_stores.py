# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/python-hdcloud/tests/test_stores.py
# Compiled at: 2010-04-14 14:13:59
from __future__ import absolute_import
from hdcloud import Store
from .fakeserver import FakeHDCloud
from .utils import assert_isinstance
hdcloud = FakeHDCloud()

def test_all_stores():
    stores = hdcloud.stores.all()
    hdcloud.assert_called('GET', '/stores.json')
    [ assert_isinstance(s, Store) for s in stores ]


def test_get_store():
    store = hdcloud.stores.get(id=1)
    hdcloud.assert_called('GET', '/stores/1.json')
    assert store.name == 'Example Store'