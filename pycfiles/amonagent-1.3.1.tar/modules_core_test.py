# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/martin/amonagent/tests/modules_core_test.py
# Compiled at: 2014-05-20 04:17:01
import sys, re, socket
from amonagent.modules.core import get_uptime, get_memory_info, get_cpu_utilization, get_load_average, get_disk_usage, get_network_traffic, get_ip_address, get_cpu_info

class TestSystemCheck(object):

    def test_uptime(self):
        uptime = get_uptime()
        assert isinstance(uptime, str)

    def test_ip_address(self):
        ip_address = get_ip_address()
        valid_ip = False
        try:
            socket.inet_pton(socket.AF_INET, ip_address)
            valid_ip = True
        except AttributeError:
            try:
                socket.inet_aton(ip_address)
                valid_ip = True
            except socket.error:
                pass

        except socket.error:
            pass

        assert valid_ip

    def test_memory(self):
        memory_dict = get_memory_info()
        assert 'free_mb' in memory_dict
        assert 'total_mb' in memory_dict
        assert 'used_mb' in memory_dict
        assert 'used_percent' in memory_dict
        assert 'swap_free_mb' in memory_dict
        assert 'swap_used_mb' in memory_dict
        assert 'swap_used_percent' in memory_dict
        assert 'swap_total_mb' in memory_dict
        for v in memory_dict.values():
            assert isinstance(v, int)

    def test_disk(self):
        disk = get_disk_usage()
        for k in disk:
            _dict = disk[k]
            assert 'used' in _dict
            assert 'percent' in _dict
            assert 'free' in _dict
            assert 'volume' in _dict
            assert 'total' in _dict

    def test_cpu(self):
        cpu = get_cpu_utilization()
        assert 'idle' in cpu
        assert 'user' in cpu
        assert 'system' in cpu
        for v in cpu.values():
            assert len(v) == 4 or len(v) == 5 or len(v) == 6
            value_regex = re.compile('\\d+[\\.]\\d+')
            assert re.match(value_regex, v)

    def test_loadavg(self):
        loadavg = get_load_average()
        assert 'minute' in loadavg
        assert 'five_minutes' in loadavg
        assert 'fifteen_minutes' in loadavg
        assert 'cores' in loadavg
        assert isinstance(loadavg['cores'], int)
        assert isinstance(loadavg['minute'], str)
        assert isinstance(loadavg['five_minutes'], str)
        assert isinstance(loadavg['fifteen_minutes'], str)
        value_regex = re.compile('\\d+[\\.]\\d+')
        assert re.match(value_regex, loadavg['minute'])
        assert re.match(value_regex, loadavg['five_minutes'])
        assert re.match(value_regex, loadavg['fifteen_minutes'])

    def test_network(self):
        network_data = get_network_traffic()
        value_regex = re.compile('\\d+[\\.]\\d+')
        assert isinstance(network_data, dict)
        for key, value in network_data.iteritems():
            assert key not in ('lo', 'IFACE')
            for k in value.keys():
                assert k in ('inbound', 'outbound')

            for k, v in value.items():
                assert re.match(value_regex, v)