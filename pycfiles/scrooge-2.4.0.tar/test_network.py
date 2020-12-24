# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/collect_plugins/test_network.py
# Compiled at: 2014-05-30 05:53:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from datetime import date
from mock import MagicMock, patch
from django.test import TestCase
from django.conf import settings
from ralph_pricing.models import UsageType, DailyUsage, Venture
from ralph_pricing.plugins.collects import network

class SshClientMock:

    def __init__(self, stdin=b'', stdout=b'', stderr=b''):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

    def exec_command(self, command):
        return (
         MagicMock(read=MagicMock(return_value=self.stdin)),
         MagicMock(read=MagicMock(return_value=self.stdout), readlines=MagicMock(return_value=self.stdout)),
         MagicMock(read=MagicMock(return_value=self.stderr)))


def get_ip_addresses_mock(only_public):
    return {b'10.10.10.10': 1, b'20.20.20.20': 1}


def get_ssh_client_mock(address, login, password):
    return SshClientMock(stdout=[
     b'',
     b'10.10.10.10 | 20.20.20.20 | 30',
     b'',
     b'',
     b'',
     b''])


class TestNetwork(TestCase):

    def setUp(self):
        settings.NFSEN_CLASS_ADDRESS = []
        settings.SSH_NFSEN_CREDENTIALS = {}
        settings.NFSEN_CHANNELS = []
        settings.NETWORK_UNKNOWN_VENTURE_SYMBOL = b''

    def test_get_names_of_data_files_when_executed_commend_return_error(self):
        self.assertRaises(network.RemoteServerError, network.get_names_of_data_files, ssh_client=SshClientMock(stderr=b'error'), channel=b'test-channel', date=b'2014-10-01')

    def test_get_names_of_data_files(self):
        self.assertEqual(network.get_names_of_data_files(SshClientMock(stdout=[b'1\n', b'2']), b'test-channel', b'2014-10-01'), [
         b'1', b'2'])

    def test_execute_nfdump(self):
        self.assertEqual(network.execute_nfdump(SshClientMock(stdout=[b'0', b'1', b'2', b'3', b'4', b'5', b'6']), b'test-channel', b'2014-10-01', [
         b'file1', b'file2'], b'scrip'), [
         b'1', b'2'])

    @patch.object(settings, b'NFSEN_CLASS_ADDRESS', [b'10.10.10.10'])
    def test_extract_ip_and_bytes_when_input_output_is_scrip(self):
        self.assertEqual(network.extract_ip_and_bytes(b'10.10.10.10 | 20.20.20.20 | 30', b'scrip'), ('10.10.10.10',
                                                                                                     30))

    @patch.object(settings, b'NFSEN_CLASS_ADDRESS', [b'20.20.20.20'])
    def test_extract_ip_and_bytes_when_input_output_is_dstip(self):
        self.assertEqual(network.extract_ip_and_bytes(b'10.10.10.10 | 20.20.20.20 | 30', b'dstip'), ('20.20.20.20',
                                                                                                     30))

    @patch.object(settings, b'NFSEN_CLASS_ADDRESS', [b'10.10.10.10'])
    def test_extract_ip_and_bytes_when_bytes_string_is_bytes_format(self):
        self.assertEqual(network.extract_ip_and_bytes(b'10.10.10.10 | 20.20.20.20 | 3000', b'scrip')[1], 3000)

    @patch.object(settings, b'NFSEN_CLASS_ADDRESS', [b'10.10.10.10'])
    def test_extract_ip_and_bytes_when_bytes_string_is_megabytes_format(self):
        self.assertEqual(network.extract_ip_and_bytes(b'10.10.10.10 | 20.20.20.20 | 1 M', b'scrip')[1], 1048576)

    @patch.object(settings, b'NFSEN_CLASS_ADDRESS', [b'10.10.10.10'])
    def test_extract_ip_and_bytes_when_bytes_string_is_gigabytes_format(self):
        self.assertEqual(network.extract_ip_and_bytes(b'10.10.10.10 | 20.20.20.20 | 1 G', b'scrip')[1], 1073741824)

    @patch.object(settings, b'NFSEN_CLASS_ADDRESS', [b'10.10.10.10'])
    def test_extract_ip_and_bytes_when_bytes_string_is_incorrect_format(self):
        self.assertRaises(network.UnknowDataFormatError, network.extract_ip_and_bytes, row=b'10.10.10.10 | 20.20.20.20 | 1 X', input_output=b'scrip')

    @patch.object(settings, b'NFSEN_CLASS_ADDRESS', [b'30.30.30.30'])
    def test_extract_ip_and_bytes_when_ip_is_not_in_class_address(self):
        self.assertEqual(network.extract_ip_and_bytes(b'10.10.10.10 | 20.20.20.20 | 30', b'scrip'), None)
        return

    def test_get_network_usage_when_ip_and_byte_is_none(self):
        self.assertEqual(network.get_network_usage(SshClientMock(stdout=[
         b'',
         b'10.10.10.10 | 20.20.20.20 | 30',
         b'',
         b'',
         b'',
         b'']), b'test-channel', b'2014-10-01', [
         b'file1', b'file2'], b'scrip'), {})

    @patch.object(settings, b'NFSEN_CLASS_ADDRESS', [b'10.10.10.10'])
    def test_get_network_usage(self):
        self.assertEqual(network.get_network_usage(SshClientMock(stdout=[
         b'',
         b'10.10.10.10 | 20.20.20.20 | 30',
         b'',
         b'',
         b'',
         b'']), b'test-channel', b'2014-10-01', [
         b'file1', b'file2'], b'scrip'), {b'10.10.10.10': 30})

    @patch.object(settings, b'NFSEN_CLASS_ADDRESS', [
     b'10.10.10.10', b'20.20.20.20'])
    @patch.object(settings, b'SSH_NFSEN_CREDENTIALS', {b'address': {b'login': b'login', 
                    b'password': b'password'}})
    @patch.object(network, b'get_ssh_client', get_ssh_client_mock)
    @patch.object(settings, b'NFSEN_CHANNELS', [b'test-channel'])
    def test_get_network_usages(self):
        self.assertEqual(network.get_network_usages(b'2014-10-01'), {b'20.20.20.20': 30, b'10.10.10.10': 30})

    def test_get_usages_type(self):
        self.assertEqual(network.get_usage_type(), UsageType.objects.get())

    def test_sort_per_venture_when_venture_is_none(self):
        self.assertEqual(network.sort_per_venture({b'10.10.10.10': 30}, {b'10.10.10.10': None, 
           b'0.0.0.0': 1}), {1: 30})
        return

    def test_sort_per_venture_when_there_is_no_ip(self):
        self.assertEqual(network.sort_per_venture({b'10.10.10.10': 30}, {b'20.20.20.20': 1, 
           b'0.0.0.0': 2}), {2: 30})

    def test_sort_per_venture(self):
        self.assertEqual(network.sort_per_venture({b'10.10.10.10': 30}, {b'10.10.10.10': 1}), {1: 30})

    def test_update_when_venture_is_not_found(self):
        self.assertEqual(self._update_daily_usage(), 0)

    def test_update(self):
        self.assertEqual(self._update_daily_usage(True), 1)

    @patch.object(settings, b'NFSEN_CLASS_ADDRESS', [
     b'10.10.10.10', b'20.20.20.20'])
    @patch.object(settings, b'SSH_NFSEN_CREDENTIALS', {b'address': {b'login': b'login', 
                    b'password': b'password'}})
    @patch.object(settings, b'NFSEN_CHANNELS', [b'test-channel'])
    @patch.object(network, b'get_ssh_client', get_ssh_client_mock)
    @patch.object(network, b'get_ip_addresses', get_ip_addresses_mock)
    def test_network(self):
        Venture.objects.create(venture_id=1)
        self.assertEqual(network.network(today=date(year=2014, month=1, day=1))[1], b'Create/Update 1 venture usages')
        self.assertEqual(DailyUsage.objects.get().value, 60)

    def _update_daily_usage(self, create_venture=False):
        if create_venture:
            Venture.objects.create(venture_id=1)
        network.update({b'10.10.10.10': 30}, {b'10.10.10.10': 1}, network.get_usage_type(), date(year=2014, month=1, day=1))
        return DailyUsage.objects.all().count()