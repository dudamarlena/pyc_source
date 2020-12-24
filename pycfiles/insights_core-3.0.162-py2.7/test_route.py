# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_route.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.route import Route
from insights.tests import context_wrap
ROUTE = '\nKernel IP routing table\nDestination     Gateway         Genmask         Flags Metric Ref    Use Iface\n10.66.208.0     0.0.0.0         255.255.255.0   U     0      0        0 eth0\n169.254.0.0     0.0.0.0         255.255.0.0     U     1002   0        0 eth0\n0.0.0.0         10.66.208.254   0.0.0.0         UG    0      0        0 eth0\n'

def test_route():
    route_info = Route(context_wrap(ROUTE))
    for route in route_info:
        assert route == {'Destination': '10.66.208.0', 'Gateway': '0.0.0.0', 
           'Genmask': '255.255.255.0', 
           'Flags': 'U', 
           'Metric': '0', 
           'Ref': '0', 
           'Use': '0', 
           'Iface': 'eth0'}
        break

    assert '169.254.0.0' in route_info