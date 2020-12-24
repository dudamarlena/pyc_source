# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_ifcfg_static_route.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.sysconfig import IfCFGStaticRoute
from insights.tests import context_wrap
import pytest
CONTEXT_PATH_DEVICE_1 = 'etc/sysconfig/network-scripts/route-test-net'
STATIC_ROUTE_1 = ('\nADDRESS0=10.65.223.0\nNETMASK0=255.255.254.0\nGATEWAY0=10.65.223.1\n').strip()
CONTEXT_PATH_DEVICE_2 = 'etc/sysconfig/network-scripts/route-test-net-11'
STATIC_ROUTE_2 = ('\nADDRESS0=\nNETMASK0=255.255.254.0\nGATEWAY0=10.65.223.1\n').strip()
CONTEXT_PATH_DEVICE_3 = 'etc/sysconfig/network-scripts/ifcfg-eth0'

def test_static_route_connection_1():
    context = context_wrap(STATIC_ROUTE_1, path=CONTEXT_PATH_DEVICE_1)
    r = IfCFGStaticRoute(context)
    assert r.static_route_name == 'test-net'
    assert r.data == {'ADDRESS0': '10.65.223.0', 'NETMASK0': '255.255.254.0', 'GATEWAY0': '10.65.223.1'}


def test_static_route_connection_2():
    context = context_wrap(STATIC_ROUTE_1, CONTEXT_PATH_DEVICE_2)
    r = IfCFGStaticRoute(context)
    assert r.static_route_name == 'test-net-11'
    assert r.data == {'ADDRESS0': '10.65.223.0', 'NETMASK0': '255.255.254.0', 'GATEWAY0': '10.65.223.1'}


def test_missing_index():
    with pytest.raises(IndexError):
        context = context_wrap(STATIC_ROUTE_2, CONTEXT_PATH_DEVICE_3)
        r = IfCFGStaticRoute(context)
        assert r.static_route_name == 'eth0'