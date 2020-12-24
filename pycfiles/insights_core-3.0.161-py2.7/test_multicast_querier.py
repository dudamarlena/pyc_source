# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_multicast_querier.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.multicast_querier import MulticastQuerier
MULTICAST_QUERIER = '\n/sys/devices/virtual/net/br0/bridge/multicast_querier\n0\n/sys/devices/virtual/net/br1/bridge/multicast_querier\n1\n/sys/devices/virtual/net/br2/bridge/multicast_querier\n0\n'

def test_mcast_queri():
    result = MulticastQuerier(context_wrap(MULTICAST_QUERIER))
    assert result.bri_val == {'br0': 0, 'br1': 1, 'br2': 0}
    assert result.bri_val['br1'] == 1
    assert len(result.bri_val) == 3