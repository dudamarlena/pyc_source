# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/hwlib/test_iproute2.py
# Compiled at: 2018-01-10 00:48:14
# Size of source mod 2**32: 3364 bytes
"""Module to unit test mercury.common.misc.iproute2"""
import mock, pytest, mercury_agent.inspector.hwlib.iproute2 as ipr2
from tests.unit.base import MercuryAgentUnitTest
IPROUTE2_EXAMPLE_OUTPUT_LINES = [
 'default via 192.168.1.1 dev br0  proto static  metric 425',
 '192.168.1.0/24 dev br0  proto kernel  scope link  src 192.168.1.175  metric 425',
 '192.168.122.0/24 dev virbr0  proto kernel  scope link  src 192.168.122.1 linkdown']
EXPECTED_EXAMPLE_ENTRIES = [
 {'via':'192.168.1.1', 
  'dev':'br0', 
  'destination':'default', 
  'proto':'static', 
  'metric':'425'},
 {'src':'192.168.1.175', 
  'destination':'192.168.1.0/24', 
  'dev':'br0', 
  'proto':'kernel', 
  'scope':'link', 
  'metric':'425'},
 {'src':'192.168.122.1', 
  'destination':'192.168.122.0/24', 
  'dev':'virbr0', 
  'proto':'kernel', 
  'scope':'link', 
  'linkdown':True}]

def construct_ipr2_with_fake_output(ipr_output, ip_path='/usr/sbin/ip'):
    """Get an IPRoute2 object with faked ip route output."""
    with mock.patch('mercury.common.helpers.cli.find_in_path') as (find_in_path_mock):
        find_in_path_mock.return_value = ip_path
        with mock.patch('mercury.common.helpers.cli.run') as (run_mock):
            run_mock.return_value = ipr_output
            return ipr2.IPRoute2()


class MercuryHwlibIPRoute2UnitTests(MercuryAgentUnitTest):
    __doc__ = 'Unit tests for mercury.common.misc.iproute2'

    def test_example_output_parsing(self):
        """Test if IPRoute2 parsed the example output correctly."""
        ipr = construct_ipr2_with_fake_output('\n'.join(IPROUTE2_EXAMPLE_OUTPUT_LINES))
        result_table = ipr.table
        if not isinstance(result_table, list):
            raise AssertionError
        elif not len(result_table) == 3:
            raise AssertionError
        for index in range(0, len(result_table)):
            assert result_table[index] == EXPECTED_EXAMPLE_ENTRIES[index]

    def test_modified_example_parsing(self):
        """Test another case of IPRoute2 parsing."""
        new_test_output = '\n'.join(IPROUTE2_EXAMPLE_OUTPUT_LINES[0:2])
        ipr = construct_ipr2_with_fake_output(new_test_output)
        result_table = ipr.table
        if not isinstance(result_table, list):
            raise AssertionError
        elif not len(result_table) == 2:
            raise AssertionError
        for index in range(0, 2):
            assert result_table[index] == EXPECTED_EXAMPLE_ENTRIES[index]

    def test_ipr_output_is_malformed(self):
        """Test what happens if `ip route` output is malformed."""
        test_output = 'this is not good ip route output :('
        with pytest.raises(Exception):
            construct_ipr2_with_fake_output(test_output)