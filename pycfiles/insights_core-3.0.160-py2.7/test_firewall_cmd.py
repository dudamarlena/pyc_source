# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_firewall_cmd.py
# Compiled at: 2020-04-16 14:56:28
import doctest, pytest
from insights.parsers import firewall_cmd
from insights.parsers.firewall_cmd import FirewallCmdListALLZones
from insights.tests import context_wrap
from insights.parsers import ParseException
from insights.core.plugins import ContentException
FIREWALL_LIST_ZONES_1 = ('\nFirewallD is not running\n').strip()
FIREWALL_LIST_ZONES_2 = ('\n-bash: firewall-cmd: command not found\n').strip()
FIREWALL_LIST_ZONES_3 = ('\nblock\n  target: %%REJECT%%\n  icmp-block-inversion: no\n  interfaces:\n  sources:\n  services:\n  ports:\n  protocols:\n  masquerade: no\n  forward-ports:\n  source-ports:\n  icmp-blocks:\n  rich rules:\n\n\ndmz\n  target: default\n  icmp-block-inversion: no\n  interfaces:\n  sources:\n  services: ssh\n  ports:\n  protocols:\n  masquerade: no\n  forward-ports:\n  source-ports:\n  icmp-blocks:\n  rich rules:\n\n\npublic (active, default)\n  target: default\n  icmp-block-inversion: no\n  interfaces: eno1\n  sources:\n  services: dhcpv6-client ssh\n  ports:\n  protocols:\n  masquerade: no\n  forward-ports: port=80:proto=tcp:toport=12345:toaddr=\n        port=81:proto=tcp:toport=1234:toaddr=\n        port=83:proto=tcp:toport=456:toaddr=10.72.47.45\n  source-ports:\n  icmp-blocks:\n  rich rules:\n        rule family="ipv4" source address="10.0.0.0/24" destination address="192.168.0.10/32" port port="8080-8090" protocol="tcp" accept\n        rule family="ipv4" source address="10.0.0.0/24" destination address="192.168.0.10/32" port port="443" protocol="tcp" reject\n        rule family="ipv4" source address="192.168.0.10/24" reject\n        rule family="ipv6" source address="1:2:3:4:6::" forward-port port="4011" protocol="tcp" to-port="4012" to-addr="1::2:3:4:7"\n\n\ntrusted\n  target: ACCEPT\n  icmp-block-inversion: yes\n  interfaces:\n  sources:\n  services:\n  ports:\n  protocols:\n  masquerade: no\n  forward-ports:\n  source-ports:\n  icmp-blocks:\n  rich rules:\n').strip()
FIREWALL_LIST_ZONES_4 = ('\npublic (active)\n    target: default\n    icmp-block-inversion: no\n    interfaces: eno1\n    sources:\n    services: dhcpv6-client ssh\n    ports:\n    protocols:\n    masquerade: no\n    forward-ports:\n    source-ports\n    icmp-blocks\n    rich rules\n').strip()

def test_docs():
    env = {'zones': FirewallCmdListALLZones(context_wrap(FIREWALL_LIST_ZONES_3))}
    failed, total = doctest.testmod(firewall_cmd, globs=env)
    assert failed == 0


def test_empty_content():
    with pytest.raises(ContentException):
        FirewallCmdListALLZones(context_wrap(FIREWALL_LIST_ZONES_1))
    with pytest.raises(ContentException):
        FirewallCmdListALLZones(context_wrap(FIREWALL_LIST_ZONES_2))
    with pytest.raises(ParseException):
        FirewallCmdListALLZones(context_wrap(FIREWALL_LIST_ZONES_4))


def test_firewall_info():
    zones = FirewallCmdListALLZones(context_wrap(FIREWALL_LIST_ZONES_3))
    assert 'trusted' not in zones.active_zones
    assert zones.zones['public']['services'] == ['dhcpv6-client ssh']
    assert zones.zones['public']['icmp-block-inversion'] == ['no']
    assert zones.zones['trusted']['services'] == []
    assert zones.zones['trusted']['icmp-block-inversion'] == ['yes']
    zone_info = ['target', 'icmp-block-inversion', 'interfaces', 'sources', 'services',
     'ports', 'protocols', 'masquerade', 'forward-ports', 'source-ports',
     'icmp-blocks', 'rich rules']
    assert all(key in zones.zones['public'] for key in zone_info)
    assert 'port=80:proto=tcp:toport=12345:toaddr=' in zones.zones['public']['forward-ports']
    assert 'port=83:proto=tcp:toport=456:toaddr=10.72.47.45' in zones.zones['public']['forward-ports']
    assert len(zones.zones['public']['forward-ports']) == 3
    assert len(zones.zones['public']['rich rules']) == 4
    assert 'active' in zones.zones['public']['_attributes']
    assert 'default' in zones.zones['public']['_attributes']
    assert 'rule family="ipv4" source address="10.0.0.0/24" destination address="192.168.0.10/32" port port="8080-8090" protocol="tcp" accept' in zones.zones['public']['rich rules']
    assert 'rule family="ipv4" source address="192.168.0.10/24" reject' in zones.zones['public']['rich rules']