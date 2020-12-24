# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/cloudservers/tests/test_ipgroups.py
# Compiled at: 2010-08-16 13:56:53
from cloudservers import IPGroup
from fakeserver import FakeServer
from utils import assert_isinstance
from nose.tools import assert_equal
cs = FakeServer()

def test_list_ipgroups():
    ipl = cs.ipgroups.list()
    cs.assert_called('GET', '/shared_ip_groups/detail')
    [ assert_isinstance(ipg, IPGroup) for ipg in ipl ]


def test_get_ipgroup():
    ipg = cs.ipgroups.get(1)
    cs.assert_called('GET', '/shared_ip_groups/1')
    assert_isinstance(ipg, IPGroup)


def test_create_ipgroup():
    ipg = cs.ipgroups.create('My group', 1234)
    cs.assert_called('POST', '/shared_ip_groups')
    assert_isinstance(ipg, IPGroup)


def test_delete_ipgroup():
    ipg = cs.ipgroups.get(1)
    ipg.delete()
    cs.assert_called('DELETE', '/shared_ip_groups/1')
    cs.ipgroups.delete(ipg)
    cs.assert_called('DELETE', '/shared_ip_groups/1')
    cs.ipgroups.delete(1)
    cs.assert_called('DELETE', '/shared_ip_groups/1')


def test_find():
    ipg = cs.ipgroups.find(name='group1')
    cs.assert_called('GET', '/shared_ip_groups/detail')
    assert_equal(ipg.name, 'group1')
    ipgl = cs.ipgroups.findall(id=1)
    assert_equal(ipgl, [IPGroup(None, {'id': 1})])
    return