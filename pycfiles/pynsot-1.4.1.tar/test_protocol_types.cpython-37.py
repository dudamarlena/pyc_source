# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryanh/src/pynsot/tests/app/test_protocol_types.py
# Compiled at: 2019-10-16 17:52:59
# Size of source mod 2**32: 6728 bytes
"""
Test Circuits in the CLI app.
"""
from __future__ import absolute_import, unicode_literals
import logging, pytest
from tests.fixtures import attribute, attributes, client, config, device, interface, network, site, site_client
from tests.fixtures.circuits import circuit
from tests.fixtures.protocol_types import protocol_type, protocol_types, protocol_attribute, protocol_attribute2
from tests.util import CliRunner, assert_output
log = logging.getLogger(__name__)

def test_protocol_types_add(site_client, protocol_attribute):
    """Test ``nsot protocol_types add``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run('protocol_types add -n bgp')
        assert result.exit_code == 0
        assert 'Added protocol_type!' in result.output
        result = runner.run('protocol_types list')
        assert result.exit_code == 0
        assert 'bgp' in result.output
        result = runner.run('protocol_types add -n bgp')
        expected_output = 'The fields site, name must make a unique set.'
        assert result.exit_code != 0
        assert expected_output in result.output
        result = runner.run("protocol_types add -n ospf -d 'OSPF is the best'")
        assert result.exit_code == 0
        assert 'Added protocol_type!' in result.output
        site_id = str(protocol_attribute['site_id'])
        result = runner.run('protocol_types list -i 2')
        assert result.exit_code == 0
        assert site_id in result.output
        assert 'OSPF is the best' in result.output
        result = runner.run('protocol_types add -n tcp -r %s' % protocol_attribute['name'])
        assert result.exit_code == 0
        assert 'Added protocol_type!' in result.output
        result = runner.run('protocol_types list -n tcp')
        assert result.exit_code == 0
        assert protocol_attribute['name'] in result.output


def test_protocol_types_list(site_client, protocol_type, protocol_attribute, protocol_attribute2):
    """Test ``nsot protocol_types list``"""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run('protocol_types list')
        assert result.exit_code == 0
        assert protocol_type['name'] in result.output
        result = runner.run('protocol_types list -d "%s"' % protocol_type['description'])
        assert result.exit_code == 0
        assert protocol_type['description'] in result.output
        result = runner.run('protocol_types list -n %s' % protocol_type['name'])
        assert result.exit_code == 0
        assert protocol_type['name'] in result.output
        result = runner.run('protocol_types list -s %s' % protocol_type['site'])
        assert result.exit_code == 0
        assert protocol_type['name'] in result.output
        result = runner.run('protocol_types list -i %s' % protocol_type['id'])
        assert result.exit_code == 0
        assert protocol_type['name'] in result.output


def test_protocol_types_list_limit(site_client, protocol_types):
    """
    If ``--limit 2`` is used, we should only see the first two Protocol objects
    """
    limit = 2
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run('protocol_types list -l {}'.format(limit))
        assert result.exit_code == 0
        expected_types = protocol_types[:limit]
        unexpected_types = protocol_types[limit:]
        for t in expected_types:
            assert t['name'] in result.output

        for t in unexpected_types:
            assert t['name'] not in result.output


def test_protocol_types_list_offset(site_client, protocol_types):
    """
    If ``--limit 2`` and ``--offset 2`` are used, we should only see the third
    and fourth Protocol objects that were created
    """
    limit = 2
    offset = 2
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run('protocol_types list -l {} -o {}'.format(limit, offset))
        assert result.exit_code == 0
        expected_types = protocol_types[offset:limit + offset]
        unexpected_types = protocol_types[limit + offset:]
        for t in expected_types:
            assert t['name'] in result.output

        for t in unexpected_types:
            assert t['name'] not in result.output


def test_protocol_types_update(site_client, protocol_type, protocol_attribute):
    """Test ``nsot protocol_types update``"""
    pt_id = protocol_type['id']
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run('protocol_types update -n Cake -i %s' % pt_id)
        assert result.exit_code == 0
        assert 'Updated protocol_type!' in result.output
        result = runner.run('protocol_types update -d Rise -i %s' % pt_id)
        assert result.exit_code == 0
        assert 'Updated protocol_type!' in result.output
        result = runner.run('protocol_types list -i %s' % pt_id)
        assert result.exit_code == 0
        assert 'Cake' in result.output
        assert 'Rise' in result.output
        result = runner.run('protocol_types update -r %s -i %s' % (
         protocol_attribute['name'],
         pt_id))
        assert result.exit_code == 0
        assert 'Updated protocol_type!' in result.output
        result = runner.run('protocol_types list -i %s' % pt_id)
        assert result.exit_code == 0
        assert protocol_attribute['name'] in result.output


def test_protocol_types_remove(site_client, protocol_type):
    """Test ``nsot protocol_types remove``"""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run('protocol_types remove -i %s' % protocol_type['id'])
        assert result.exit_code == 0
        assert 'Removed protocol_type!' in result.output