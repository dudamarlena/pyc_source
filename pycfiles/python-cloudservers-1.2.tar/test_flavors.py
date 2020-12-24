# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/cloudservers/tests/test_flavors.py
# Compiled at: 2010-08-16 13:12:03
from cloudservers import Flavor, NotFound
from fakeserver import FakeServer
from utils import assert_isinstance
from nose.tools import assert_raises, assert_equal
cs = FakeServer()

def test_list_flavors():
    fl = cs.flavors.list()
    cs.assert_called('GET', '/flavors/detail')
    [ assert_isinstance(f, Flavor) for f in fl ]


def test_get_flavor_details():
    f = cs.flavors.get(1)
    cs.assert_called('GET', '/flavors/1')
    assert_isinstance(f, Flavor)
    assert_equal(f.ram, 256)
    assert_equal(f.disk, 10)


def test_find():
    f = cs.flavors.find(ram=256)
    cs.assert_called('GET', '/flavors/detail')
    assert_equal(f.name, '256 MB Server')
    f = cs.flavors.find(disk=20)
    assert_equal(f.name, '512 MB Server')
    assert_raises(NotFound, cs.flavors.find, disk=12345)