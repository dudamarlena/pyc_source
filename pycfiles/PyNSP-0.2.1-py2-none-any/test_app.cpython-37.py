# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ryanh/src/pynsot/tests/test_app.py
# Compiled at: 2019-10-16 17:52:59
# Size of source mod 2**32: 48322 bytes
__doc__ = '\nTest the CLI app.\n'
from __future__ import unicode_literals
import logging, pytest
from .fixtures import attribute, attributes, client, config, device, network, interface, site, site_client
from .util import CliRunner, assert_output
log = logging.getLogger(__name__)
__all__ = ('client', 'config', 'site', 'site_client', 'pytest', 'attribute', 'device',
           'interface', 'network')

def test_site_id(client):
    """Test ``nsot devices list`` without required site_id"""
    runner = CliRunner(client.config)
    with runner.isolated_filesystem():
        result = runner.run('devices list')
        expected_output = 'Error: Missing option "-s" / "--site-id".'
        assert result.exit_code == 2
        assert expected_output in result.output


def test_site_add(client):
    """Test ``nsot sites add``."""
    runner = CliRunner(client.config)
    with runner.isolated_filesystem():
        result = runner.run("sites add -n Foo -d 'Foo site.'")
        expected_output = '[SUCCESS] Added site!\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run("sites add -n Foo -d 'Foo site.'")
        expected_output = 'site with this name already exists.\n'
        assert result.exit_code == 1
        assert expected_output in result.output


def test_sites_list(client, site):
    """Test ``nsot sites list``."""
    runner = CliRunner(client.config)
    with runner.isolated_filesystem():
        result = runner.run('sites list')
        assert result.exit_code == 0
        assert site['name'] in result.output
        result = runner.run('sites list -i %s' % site['id'])
        assert result.exit_code == 0
        assert site['name'] in result.output
        result = runner.run('sites list -n %s' % site['name'])
        assert result.exit_code == 0
        assert site['name'] in result.output
        result = runner.run('sites list -N')
        assert result.exit_code == 0
        assert site['name'] == result.output.strip()


def test_sites_update(client, site):
    """Test ``nsot sites update``."""
    runner = CliRunner(client.config)
    with runner.isolated_filesystem():
        result = runner.run('sites update -n Bacon -i %s' % site['id'])
        assert result.exit_code == 0
        assert 'Updated site!' in result.output
        result = runner.run('sites update -d Sizzle -i %s' % site['id'])
        assert result.exit_code == 0
        assert 'Updated site!' in result.output
        result = runner.run('sites list -n Bacon')
        assert result.exit_code == 0
        assert 'Bacon' in result.output
        assert 'Sizzle' in result.output


def test_sites_remove(client, site):
    """Test ``nsot sites remove``."""
    runner = CliRunner(client.config)
    with runner.isolated_filesystem():
        result = runner.run('sites remove -i %s' % site['id'])
        assert result.exit_code == 0
        assert 'Removed site!' in result.output


def test_attributes_add(site_client):
    """Test ``nsot attributes add``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run('attributes add -n device_multi -r device --multi')
        assert_output(result, ['Added attribute!'])


def test_attributes_list(site_client):
    """Test ``nsot attributes list``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        runner.run('attributes add -n monitored -r device --allow-empty')
        result = runner.run('attributes list')
        assert result.exit_code == 0
        result = runner.run('attributes list -N')
        assert result.exit_code == 0
        assert 'Device:monitored\n' == result.output
        attr = site_client.attributes.get(name='monitored')[0]
        name_result = runner.run('attributes list -n monitored')
        expected = ('Constraints', 'monitored')
        assert result.exit_code == 0
        for e in expected:
            assert e in name_result.output

        id_result = runner.run('attributes list -i %s' % attr['id'])
        assert id_result.exit_code == 0
        assert id_result.output == name_result.output


def test_attributes_update(site_client):
    """Test ``nsot attributes update``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        runner.run('attributes add -r device -n tags --multi')
        attr = site_client.attributes.get(name='tags')[0]
        before_result = runner.run('attributes list -i %s' % attr['id'])
        assert_output(before_result, ['tags', 'Device'])
        result = runner.run('attributes update --no-multi -i %s' % attr['id'])
        assert_output(result, ['Updated attribute!'])
        after_result = runner.run('attributes list -i %s' % attr['id'])
        assert after_result.exit_code == 0
        assert before_result != after_result
        runner.run('attributes update -r device -n tags --allow-empty')
        result = runner.run('attributes list -r device -n tags')
        assert_output(result, ['allow_empty=True'])
        result = runner.run('attributes update -r device -n tags')
        assert_output(result, ['Error:'], exit_code=2)


def test_attributes_remove(site_client, attribute):
    """Test ``nsot attributes update``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run('attributes remove -i %s' % attribute['id'])
        assert result.exit_code == 0
        assert 'Removed attribute!' in result.output


def test_device_add(site_client):
    """Test ``nsot devices add``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run('devices add -H foo-bar1')
        expected_output = '[SUCCESS] Added device!\n'
        assert result.exit_code == 0
        assert result.output == expected_output


def test_devices_bulk_add(site_client):
    """Test ``nsot devices add -b /path/to/bulk_file``"""
    BULK_ADD = 'hostname:attributes\nfoo-bar1:owner=jathan\nfoo-bar2:owner=jathan\n'
    BULK_FAIL = 'hostname:attributes\nfoo-bar3:owner=jathan,bacon=delicious\nfoo-bar4:owner=jathan\n'
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        runner.run('attributes add -n owner -r device')
        with open('bulk_file', 'w') as (fh):
            fh.writelines(BULK_ADD)
        with open('bulk_fail', 'w') as (fh):
            fh.writelines(BULK_FAIL)
        result = runner.run('devices add -b bulk_file')
        expected_output = '[SUCCESS] Added device!\n[SUCCESS] Added device!\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('devices add -b bulk_fail')
        expected_output = 'Attribute name (bacon) does not exist'
        assert result.exit_code == 1
        assert expected_output in result.output


def test_devices_list(site_client):
    """Test ``nsot devices list``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        runner.run('attributes add -n owner -r device')
        runner.run('devices add -H foo-bar1 -a owner=jathan')
        runner.run('devices add -H foo-bar2 -a owner=jathan')
        result = runner.run('devices list')
        assert result.exit_code == 0
        expected = ('foo-bar1', 'foo-bar2')
        for e in expected:
            assert e in result.output

        result = runner.run('devices list -q owner=jathan')
        expected_output = 'foo-bar1\nfoo-bar2\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('devices list -N')
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('devices list -q owner=jathan -d')
        expected_output = 'foo-bar1,foo-bar2\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('devices list -l 1 -q owner=jathan')
        expected_output = 'foo-bar1\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('devices list -l 1 -o 1 -q owner=jathan')
        expected_output = 'foo-bar2\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('devices list -a owner=jathan -g')
        expected_output = 'foo-bar1 owner=jathan\nfoo-bar1 hostname=foo-bar1\nfoo-bar1 id=5\nfoo-bar1 site_id=11\nfoo-bar2 owner=jathan\nfoo-bar2 hostname=foo-bar2\nfoo-bar2 id=6\nfoo-bar2 site_id=11\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        runner.run('devices add -H foo-bar3 -a owner="Jathan McCollum"')
        result = runner.run('devices list -q \'owner="Jathan McCollum"\'')
        expected_output = 'foo-bar3\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('devices list -q "owner=Jathan\\ McCollum"')
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('devices list -q \'owner="Jathan McCollum\'')
        assert result.exit_code == 1
        assert 'No closing quotation' in result.output


def test_devices_subcommands(site_client, device):
    """Test ``nsot devices list ... interfaces`` sub-command."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        hostname = device['hostname']
        device_id = device['id']
        runner.run('interfaces add -D %s -n eth0' % device_id)
        runner.run('interfaces add -D %s -n eth1' % device_id)
        result = runner.run('devices list -H %s interfaces' % hostname)
        expected = ('eth0', 'eth1')
        assert result.exit_code == 0
        for e in expected:
            assert e in result.output

        result = runner.run('devices list -i %s interfaces' % device_id)
        assert result.exit_code == 0
        for e in expected:
            assert e in result.output

        result = runner.run('devices list -q foo=test_device interfaces')
        assert result.exit_code == 0
        for e in expected:
            assert e in result.output


def test_devices_update(site_client):
    """Test ``nsot devices update``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        runner.run('attributes add -n owner -r device')
        runner.run('attributes add -n monitored -r device --allow-empty')
        runner.run('devices add -H foo-bar1 -a owner=jathan')
        result = runner.run('devices update -H foo-bar1 -a monitored')
        expected_output = '[SUCCESS] Updated device!\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('devices list -H foo-bar1')
        assert result.exit_code == 0
        assert 'monitored=' in result.output
        result = runner.run('devices update -H foo-bar1 -a monitored --delete-attributes')
        assert result.exit_code == 0
        result = runner.run('devices list -H foo-bar1')
        assert result.exit_code == 0
        assert 'monitored=' not in result.output


def test_attribute_modify_multi(site_client):
    """Test modification of list-type attributes (multi=True)."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        runner.run('devices add -H foo-bar1')
        runner.run('attributes add -r device -n multi --multi')
        result = runner.run('devices update -H foo-bar1 -a multi=jathy -a multi=jilli --multi')
        assert result.exit_code == 0
        result = runner.run('devices list -H foo-bar1')
        expected = ('multi=', 'jathy', 'jilli')
        assert result.exit_code == 0
        for e in expected:
            assert e in result.output

        result = runner.run('devices update -H foo-bar1 -a multi=bob -a multi=alice --multi --replace-attributes')
        assert result.exit_code == 0
        result = runner.run('devices list -H foo-bar1')
        expected = ('multi=', 'bob', 'alice')
        assert result.exit_code == 0
        for e in expected:
            assert e in result.output

        result = runner.run('devices update -H foo-bar1 -a multi=bob --multi --delete-attributes')
        assert result.exit_code == 0
        result = runner.run('devices list -H foo-bar1')
        assert result.exit_code == 0
        assert 'bob' not in result.output
        result = runner.run('devices update -H foo-bar1 -a multi=alice --multi --delete-attributes')
        assert result.exit_code == 0
        result = runner.run('devices list -H foo-bar1')
        assert result.exit_code == 0
        assert 'multi=' not in result.output
        result = runner.run('devices update -H foo-bar1 -a multi=spam -a multi=eggs --multi')
        assert result.exit_code == 0
        result = runner.run('devices list -H foo-bar1')
        expected = ('multi=', 'eggs', 'spam')
        assert result.exit_code == 0
        for e in expected:
            assert e in result.output

        result = runner.run('devices update -H foo-bar1 -a multi --delete-attributes')
        assert result.exit_code == 0
        result = runner.run('devices list -H foo-bar1')
        assert result.exit_code == 0
        assert 'multi=' not in result.output


def test_devices_remove(site_client, device):
    """Test ``nsot devices remove``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run('devices remove -i %s' % device['id'])
        assert_output(result, ['Removed device!'])
        runner.run('devices add -H delete-me')
        result = runner.run('devices remove -i delete-me')
        assert_output(result, ['Removed device!'])
        runner.run('devices add -H delete-me')
        result = runner.run('devices remove -H delete-me')
        assert_output(result, ['Removed device!'])


def test_networks_add(site_client):
    """Test ``nsot networks add``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run('networks add -c 10.0.0.0/8')
        expected_output = '[SUCCESS] Added network!\n'
        assert result.exit_code == 0
        assert result.output == expected_output


def test_networks_bulk_add(site_client):
    """Test ``nsot networks add -b /path/to/bulk_file``."""
    BULK_ADD = 'cidr:attributes\n10.0.0.0/8:owner=jathan\n10.0.0.0/24:owner=jathan\n'
    BULK_FAIL = 'cidr:attributes\n10.10.0.0/24:owner=jathan,bacon=delicious\n10.11.0.0/24:owner=jathan\n'
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        runner.run('attributes add -n owner -r network')
        with open('bulk_file', 'w') as (fh):
            fh.writelines(BULK_ADD)
        with open('bulk_fail', 'w') as (fh):
            fh.writelines(BULK_FAIL)
        result = runner.run('networks add -b bulk_file')
        expected_output = '[SUCCESS] Added network!\n[SUCCESS] Added network!\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('networks add -b bulk_fail')
        expected_output = 'Attribute name (bacon) does not exist'
        assert result.exit_code == 1
        assert expected_output in result.output


def test_networks_list(site_client):
    """Test ``nsot networks list``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        runner.run('attributes add -n owner -r network')
        runner.run('networks add -c 10.0.0.0/8 -a owner=jathan')
        runner.run('networks add -c 10.0.0.0/24 -a owner=jathan')
        result = runner.run('networks list')
        assert result.output.count('10.0.0.0') == 3
        assert result.exit_code == 0
        result = runner.run('networks list -q owner=jathan')
        expected_output = '10.0.0.0/8\n10.0.0.0/24\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('networks list -N')
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('networks list -l 1 -q owner=jathan')
        expected_output = '10.0.0.0/8\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('networks list -l 1 -o 1 -q owner=jathan')
        expected_output = '10.0.0.0/24\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('networks list -q owner=jathan -d')
        expected_output = '10.0.0.0/8,10.0.0.0/24\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('networks list -a owner=jathan -g')
        expected_output = '10.0.0.0/8 owner=jathan\n10.0.0.0/8 cidr=10.0.0.0/8\n10.0.0.0/8 id=5\n10.0.0.0/8 ip_version=4\n10.0.0.0/8 is_ip=False\n10.0.0.0/8 network_address=10.0.0.0\n10.0.0.0/8 parent=None\n10.0.0.0/8 parent_id=None\n10.0.0.0/8 prefix_length=8\n10.0.0.0/8 site_id=18\n10.0.0.0/8 state=allocated\n10.0.0.0/24 owner=jathan\n10.0.0.0/24 cidr=10.0.0.0/24\n10.0.0.0/24 id=6\n10.0.0.0/24 ip_version=4\n10.0.0.0/24 is_ip=False\n10.0.0.0/24 network_address=10.0.0.0\n10.0.0.0/24 parent=10.0.0.0/8\n10.0.0.0/24 parent_id=5\n10.0.0.0/24 prefix_length=24\n10.0.0.0/24 site_id=18\n10.0.0.0/24 state=allocated\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        runner.run('networks add -c 10.0.0.0/16 -a owner="Jathan McCollum"')
        result = runner.run('networks list -q \'owner="Jathan McCollum"\'')
        expected_output = '10.0.0.0/16\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('networks list -q "owner=Jathan\\ McCollum"')
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('networks list -q \'owner="Jathan McCollum\'')
        assert result.exit_code == 1
        assert 'No closing quotation' in result.output


def test_networks_subcommands(site_client, network):
    """Test ``nsot networks list ... <subcommand>``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        runner.run('attributes add -n owner -r network')
        runner.run('networks add -c 10.0.0.0/8 -a owner=jathan')
        runner.run('networks add -c 10.0.0.0/24 -a owner=jathan')
        result = runner.run('networks list -c 10.0.0.0/8 subnets')
        assert_output(result, ['10.0.0.0', '24'])
        result = runner.run('networks list -c 10.0.0.0/24 supernets')
        assert_output(result, ['10.0.0.0', '8'])
        runner.run('networks add -c 10.10.10.0/24')
        runner.run('networks add -c 10.10.10.1/32')
        runner.run('networks add -c 10.10.10.2/32')
        runner.run('networks add -c 10.10.10.3/32')
        result = runner.run('networks list -c 10.10.10.1/32 parent')
        assert_output(result, ['10.10.10.0', '24'])
        result = runner.run('networks list -c 10.10.10.1/32 ancestors')
        assert_output(result, ['10.10.10.0', '24'])
        assert_output(result, ['10.0.0.0', '8'])
        result = runner.run('networks list -c 10.10.10.0/24 children')
        assert_output(result, ['10.10.10.1', '32'])
        assert_output(result, ['10.10.10.2', '32'])
        assert_output(result, ['10.10.10.3', '32'])
        result = runner.run('networks list -c 10.0.0.0/8 descendants')
        assert_output(result, ['10.0.0.0', '24'])
        assert_output(result, ['10.10.10.0', '24'])
        assert_output(result, ['10.10.10.1', '32'])
        assert_output(result, ['10.10.10.2', '32'])
        assert_output(result, ['10.10.10.3', '32'])
        result2 = runner.run('networks list -c 10.0.0.0/8 descendents')
        assert_output(result2, ['[WARNING]'])
        assert result.output.splitlines() == result2.output.splitlines()[1:]
        result = runner.run('networks list -c 10.10.10.1/32 root')
        assert_output(result, ['10.0.0.0', '8'])
        result = runner.run('networks list -c 10.10.10.2/32 siblings')
        assert_output(result, ['10.10.10.1', '32'])
        assert_output(result, ['10.10.10.3', '32'])
        result = runner.run('networks list -c 10.10.10.2/32 siblings --include-self')
        assert_output(result, ['10.10.10.1', '32'])
        assert_output(result, ['10.10.10.2', '32'])
        assert_output(result, ['10.10.10.3', '32'])
        result = runner.run('networks list -c 10.10.10.104/32 closest_parent')
        assert_output(result, ['10.10.10.0', '24'])
        result = runner.run('networks list -c 1.2.3.4/32 closest_parent')
        assert_output(result, ['No such Network found'], exit_code=1)
        result = runner.run('networks list -q foo=test_network parent')
        assert result.exit_code == 0
        result = runner.run('networks list -q owner=jathan parent')
        assert result.exit_code == 1


def test_networks_allocation(site_client, device, network, interface):
    """Test network allocation-related subcommands."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run('networks list -c 10.20.30.1/32 assignments')
        assert_output(result, ['foo-bar1', 'eth0'])
        runner.run('networks add -c 10.20.30.104/32 --state reserved')
        result = runner.run('networks list reserved')
        assert_output(result, ['10.20.30.104', '32'])
        result = runner.run('networks list -c 10.20.30.0/24 next_network -n 2 -p 28')
        assert_output(result, ['10.20.30.16', '28'])
        assert_output(result, ['10.20.30.32', '28'])
        runner.run('networks add -c 10.20.30.3/32')
        result = runner.run('networks list -c 10.20.30.0/24 next_address -n 3')
        assert_output(result, ['10.20.30.2', '32'])
        assert_output(result, ['10.20.30.4', '32'])
        assert_output(result, ['10.20.30.5', '32'])
        runner.run('networks add -c 10.2.1.0/24')
        runner.run('networks add -c 10.2.1.0/25')
        result = runner.run('networks list -c 10.2.1.0/24 next_network -p 28 -n 3 -s')
        assert_output(result, ['10.2.1.128', '28'])
        assert_output(result, ['10.2.1.144', '28'])
        assert_output(result, ['10.2.1.160', '28'])
        result = runner.run('networks list -c 10.2.1.0/24 next_address -n 3 -s')
        assert_output(result, ['10.2.1.128', '32'])
        assert_output(result, ['10.2.1.129', '32'])
        assert_output(result, ['10.2.1.130', '32'])


def test_networks_update(site_client):
    """Test ``nsot networks update``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        runner.run('attributes add -n owner -r network')
        runner.run('networks add -c 10.0.0.0/8 -a owner=jathan')
        runner.run('attributes add -n foo -r network')
        result = runner.run('networks update -c 10.0.0.0/8 -a foo=bar')
        expected_output = '[SUCCESS] Updated network!\n'
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('networks list -c 10.0.0.0/8')
        assert result.exit_code == 0
        assert 'foo=bar' in result.output
        result = runner.run('networks update -c 10.0.0.0/8 -a foo --delete-attributes')
        assert result.exit_code == 0
        assert 'foo=bar' not in result.output


def test_networks_remove(site_client, network):
    """Test ``nsot networks remove``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run('networks remove -i %s' % network['id'])
        assert_output(result, ['Removed network!'])
        runner.run('networks add -c 10.20.30.0/24')
        result = runner.run('networks remove -i 10.20.30.0/24')
        assert_output(result, ['Removed network!'])
        runner.run('networks add -c 10.20.30.0/24')
        result = runner.run('networks remove -c 10.20.30.0/24')
        assert_output(result, ['Removed network!'])
        runner.run('networks add -c 10.20.30.0/24')
        runner.run('networks add -c 10.20.30.5/32')
        runner.run('networks add -c 10.20.0.0/17')
        result = runner.run('networks remove -c 10.20.30.0/24')
        result.exit_code == 1
        assert "Cannot delete some instances of model 'Network'" in result.output
        result = runner.run('networks remove -c 10.20.30.0/24 -f')
        assert_output(result, ['Removed network!'])
        result = runner.run('networks remove -c 10.20.0.0/17 --force-delete')
        result.exit_code == 1
        assert 'cannot forcefully delete a network that does not have a parent' in result.output


def test_interfaces_add(site_client, device):
    """Test ``nsot interfaces add``."""
    device_id = device['id']
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run("interfaces add -D %s -n eth0 -e 'this is eth0'" % device_id)
        assert result.exit_code == 0
        assert 'Added interface!' in result.output
        result = runner.run('interfaces list -D %s' % device_id)
        assert result.exit_code == 0
        assert 'eth0' in result.output
        runner.run('networks add -c 10.10.10.0/24')
        add_result = runner.run('interfaces add -D %s -n eth1 -c 10.10.10.1/32' % device_id)
        assert add_result.exit_code == 0
        result = runner.run('interfaces list -D %s' % device_id)
        assert result.exit_code == 0
        expected = ('eth0', '10.10.10.1/32')
        for e in expected:
            assert e in result.output

        add_result = runner.run('interfaces add -D %s -n eth2 -c 10.10.10.2/32 -c 10.10.10.3/32' % device_id)
        assert add_result.exit_code == 0
        result = runner.run('interfaces list -D %s -n eth2' % device_id)
        assert result.exit_code == 0
        expected = ('10.10.10.2/32', '10.10.10.3/32')
        for e in expected:
            assert e in result.output

        parent_ifc = site_client.interfaces.get(name='eth0')[0]
        parent_id = parent_ifc['id']
        result = runner.run('interfaces add -D %s -n eth0:1 -p %s' % (device_id, parent_id))
        assert result.exit_code == 0
        assert 'Added interface!' in result.output


def test_interfaces_list(site_client, device):
    """Test ``nsot interfaces list``."""
    device_id = device['id']
    hostname = device['hostname']
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        runner.run('attributes add -r interface -n vlan')
        runner.run('networks add -c 10.10.10.0/24')
        i1 = runner.run('interfaces add -D %s -n eth0 -a vlan=100 -m 00:00:00:00:00:01 -S 10000 -c 10.10.10.1/32' % device_id)
        assert i1.exit_code == 0
        i2 = runner.run('interfaces add -D %s -n eth1 -a vlan=100 -m 00:00:00:00:00:02 -S 20000 -c 10.10.10.2/32 -t 24' % device_id)
        assert i2.exit_code == 0
        result = runner.run('interfaces list')
        assert result.exit_code == 0
        expected = ('eth0', 'eth1')
        for e in expected:
            assert e in result.output

        result = runner.run('interfaces list -q vlan=100')
        expected_output = '{0}:eth0\n{0}:eth1\n'.format(hostname)
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('interfaces list -a vlan=100 -N')
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('interfaces list -q vlan=100 -d')
        expected_output = '{0}:eth0,{0}:eth1\n'.format(hostname)
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('interfaces list -l1 -q vlan=100')
        expected_output = '{0}:eth0\n'.format(hostname)
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('interfaces list -l1 -o1 -q vlan=100')
        expected_output = '{0}:eth1\n'.format(hostname)
        assert result.exit_code == 0
        assert result.output == expected_output
        result = runner.run('interfaces list -a vlan=100 -g')
        expected_output = "{0}:eth0 vlan=100\n{0}:eth0 addresses=[u'10.10.10.1/32']\n{0}:eth0 description=\n{0}:eth0 device=16\n{0}:eth0 device_hostname=foo-bar1\n{0}:eth0 id=8\n{0}:eth0 mac_address=00:00:00:00:00:01\n{0}:eth0 name=eth0\n{0}:eth0 name_slug=foo-bar1:eth0\n{0}:eth0 networks=[u'10.10.10.0/24']\n{0}:eth0 parent=None\n{0}:eth0 parent_id=None\n{0}:eth0 speed=10000\n{0}:eth0 type=6\n{0}:eth1 vlan=100\n{0}:eth1 addresses=[u'10.10.10.2/32']\n{0}:eth1 description=\n{0}:eth1 device=16\n{0}:eth1 device_hostname=foo-bar1\n{0}:eth1 id=9\n{0}:eth1 mac_address=00:00:00:00:00:02\n{0}:eth1 name=eth1\n{0}:eth1 name_slug=foo-bar1:eth1\n{0}:eth1 networks=[u'10.10.10.0/24']\n{0}:eth1 parent=None\n{0}:eth1 parent_id=None\n{0}:eth1 speed=20000\n{0}:eth1 type=24\n".format(hostname)
        assert result.exit_code == 0
        assert result.output == expected_output
        natural_key = '{0}:eth1'.format(hostname)
        result = runner.run('interfaces list -i {}'.format(natural_key))
        assert natural_key in result.output
        assert result.exit_code == 0
        result = runner.run('interfaces list -D %s' % device_id)
        expected = ('eth0', 'eth1')
        assert result.exit_code == 0
        for e in expected:
            assert e in result.output

        result = runner.run('interfaces list -D %s' % hostname)
        assert result.exit_code == 0
        for e in expected:
            assert e in result.output

        result = runner.run('interfaces list -D %s -n eth1' % hostname)
        assert result.exit_code == 0
        assert 'eth1' in result.output
        assert 'eth0' not in result.output
        result = runner.run('interfaces list -D %s -S 10000' % hostname)
        assert result.exit_code == 0
        assert 'eth0' in result.output
        assert 'eth1' not in result.output
        result = runner.run('interfaces list -D %s -t 24' % hostname)
        assert result.exit_code == 0
        assert 'eth1' in result.output
        assert 'eth0' not in result.output
        result = runner.run('interfaces list -D %s -m 2' % hostname)
        assert result.exit_code == 0
        assert 'eth1' in result.output
        assert 'eth0' not in result.output


def test_interfaces_subcommands(site_client, device):
    """Test ``nsot interfaces list ... {subcommand}``."""
    device_id = device['id']
    device_hostname = device['hostname']
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        runner.run('attributes add -r interface -n vlan')
        runner.run('networks add -c 10.10.10.0/24')
        i1 = runner.run('interfaces add -D %s -n eth0 -a vlan=100 -m 00:00:00:00:00:01 -S 10000 -c 10.10.10.1/32 -c 10.10.10.2/32' % device_id)
        assert i1.exit_code == 0
        cmds = [
         'interfaces list -D %s -n eth0 -N addresses' % device_id,
         'interfaces list -i %s:eth0 -N addresses' % device_hostname,
         'interfaces list -q vlan=100 -N addresses']
        for cmd in cmds:
            result = runner.run(cmd)
            assert result.exit_code == 0
            assert result.output == '10.10.10.1/32\n10.10.10.2/32\n'

        cmds = [
         'interfaces list -D %s -n eth0 -N networks' % device_id,
         'interfaces list -i %s:eth0 -N networks' % device_hostname,
         'interfaces list -q vlan=100 -N networks']
        for cmd in cmds:
            result = runner.run(cmd)
            assert result.exit_code == 0
            assert result.output == '10.10.10.0/24\n'

        cmds = [
         'interfaces list -D %s -n eth0 -N assignments' % device_id,
         'interfaces list -i %s:eth0 -N assignments' % device_hostname,
         'interfaces list -q vlan=100 -N assignments']
        for cmd in cmds:
            result = runner.run(cmd)
            expected_output = 'foo-bar1:eth0:10.10.10.1/32\nfoo-bar1:eth0:10.10.10.2/32\n'
            assert result.exit_code == 0
            assert result.output == expected_output


def test_interfaces_update(site_client, device):
    """Test ``nsot interfaces update``."""
    device_id = device['id']
    hostname = device['hostname']
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        runner.run('attributes add -n vlan -r interface')
        runner.run('attributes add -n metro -r interface')
        runner.run('networks add -c 10.10.10.0/24')
        runner.run("interfaces add -D %s -n eth0 -a vlan=100 -a metro=lax -m 1 -S 40000 -e 'this is my eth0' -t 24 -c 10.10.10.1/32" % device_id)
        parent_ifc = site_client.interfaces.get(name='eth0')[0]
        parent_id = parent_ifc['id']
        runner.run('interfaces add -D %s -n eth0:1 -c 10.10.10.2/32' % device_id)
        child_ifc = site_client.interfaces.get(name='eth0:1')[0]
        child_id = child_ifc['id']
        cases = [
         [
          200, parent_id],
         [
          300, '%s:%s' % (hostname, parent_ifc['name'])]]
        for vlan, identifier in cases:
            result = runner.run('interfaces update -i %s -a vlan=%d' % (identifier, vlan))
            assert result.exit_code == 0
            assert 'Updated interface!' in result.output
            result = runner.run('interfaces list -i %s' % identifier)
            assert result.exit_code == 0
            assert 'vlan=%d' % vlan in result.output

        result = runner.run('interfaces update -i %s -p %s' % (child_id, parent_id))
        assert result.exit_code == 0
        result = runner.run('interfaces list -p %s' % parent_id)
        assert result.exit_code == 0
        assert 'eth0:1' in result.output
        result = runner.run('interfaces update -i %s -n child -m 3 -t 161 -S 12345678' % child_id)
        assert result.exit_code == 0
        result = runner.run('interfaces list -n child')
        assert result.exit_code == 0
        expected = ('161', '12345678', '00:00:00:00:00:03')
        for e in expected:
            assert e in result.output

        result = runner.run('interfaces list -i %s' % parent_id)
        assert result.exit_code == 0
        assert '10.10.10.1/32' not in result.output
        runner.run('interfaces update -i %s -c 10.10.10.1/32' % parent_id)
        result = runner.run('interfaces list -i %s' % parent_id)
        assert result.exit_code == 0
        assert '10.10.10.1/32' in result.output
        result = runner.run("interfaces update -i %s -e 'description'" % child_id)
        assert result.exit_code == 0


def test_interfaces_remove(site_client, device, interface):
    """Test ``nsot interfaces remove``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run('interfaces remove -i %s' % interface['id'])
        assert result.exit_code == 0
        assert 'Removed interface!' in result.output


def test_interfaces_remove_by_natural_key(site_client, device, interface):
    """Test ``nsot interfaces remove`` via the natural key."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        identifier = '%s:%s' % (device['hostname'], interface['name'])
        result = runner.run('interfaces remove -i %s' % identifier)
        assert result.exit_code == 0
        assert 'Removed interface!' in result.output


def test_values_list(site_client):
    """Test ``nsot values list``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        runner.run('attributes add -n owner -r device')
        runner.run('devices add -H foo-bar1 -a owner=jathan')
        result = runner.run('values list')
        assert result.exit_code == 2
        assert 'Error: Missing option "-n"' in result.output
        result = runner.run('values list -n owner -r device')
        assert result.exit_code == 0
        assert result.output == 'jathan\n'


def test_changes_list(site_client):
    """Test ``nsot changes list``."""
    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run('changes list')
        assert result.exit_code == 0