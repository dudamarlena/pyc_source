# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: test_netbox.py
# Compiled at: 2018-02-21 16:35:35
from __future__ import absolute_import
import sys, json, yaml, pytest
from requests.models import Response
try:
    from netbox import netbox
except ImportError:
    sys.path.append('contrib/inventory/')
    import netbox

try:
    from unittest.mock import patch, MagicMock, mock_open
    builtin_open = 'builtins.open'
except ImportError:
    from mock import patch, MagicMock, mock_open
    builtin_open = '__builtin__.open'

netbox_config = '\nnetbox:\n    main:\n        api_url: \'http://localhost/api/dcim/devices/\'\n        api_token: \'1234567890987654321234567890987654321\'\n\n    # How servers will be grouped.\n    # If no group specified here, inventory script will return all servers.\n    group_by:\n        # Default section in Netbox.\n        default:\n            - device_role\n            - rack\n            - platform\n        # Custom sections (custom_fields) could be used.\n        #custom:\n        #    - env\n\n    # Use Netbox sections as host variables.\n    hosts_vars:\n        # Sections related to IPs e.g. "primary_ip" or "primary_ip4".\n        ip:\n            ansible_ssh_host: primary_ip\n        # Any other sections.\n        general:\n            rack_name: rack\n        # Custom sections (custom_fields) could be used as vars too.\n        #custom:\n        #    env: env\n'
netbox_config_invalid = 'invalid yaml syntax: ]['
netbox_config_data = yaml.safe_load(netbox_config)
netbox_api_output = json.loads('\n{\n  "count": 2,\n  "next": null,\n  "previous": null,\n  "results": [\n    {\n      "id": 1,\n      "name": "fake_host01",\n      "display_name": "Fake Host",\n      "device_type": {\n        "id": 1,\n        "manufacturer": {\n          "id": 8,\n          "name": "Fake Manufacturer",\n          "slug": "fake_manufacturer"\n        },\n        "model": "all",\n        "slug": "all"\n      },\n      "device_role": {\n        "id": 8,\n        "name": "Fake Server",\n        "slug": "fake_server"\n      },\n      "tenant": null,\n      "platform": null,\n      "serial": "",\n      "asset_tag": "fake_tag",\n      "rack": {\n        "id": 1,\n        "name": "fake_rack01",\n        "facility_id": null,\n        "display_name": "Fake Rack01"\n      },\n      "position": null,\n      "face": null,\n      "parent_device": null,\n      "status": true,\n      "primary_ip": {\n        "id": 1,\n        "family": 4,\n        "address": "192.168.0.2/32"\n      },\n      "primary_ip4": {\n        "id": 1,\n        "family": 4,\n        "address": "192.168.0.2/32"\n      },\n      "primary_ip6": null,\n      "comments": "",\n      "custom_fields": {\n        "label": "Web",\n        "env": {\n          "id": 1,\n          "value": "Prod"\n        }\n      }\n    },\n    {\n      "id": 2,\n      "name": "fake_host02",\n      "display_name": "fake_host02",\n      "device_type": {\n        "id": 1,\n        "manufacturer": {\n          "id": 8,\n          "name": "Super Micro",\n          "slug": "super-micro"\n        },\n        "model": "all",\n        "slug": "all"\n      },\n      "device_role": {\n        "id": 8,\n        "name": "Server",\n        "slug": "server"\n      },\n      "tenant": null,\n      "platform": null,\n      "serial": "",\n      "asset_tag": "xtag",\n      "rack": {\n        "id": 1,\n        "name": "fake_rack01",\n        "facility_id": null,\n        "display_name": "Fake Host 02"\n      },\n      "position": null,\n      "face": null,\n      "parent_device": null,\n      "status": true,\n      "primary_ip": null,\n      "primary_ip4": null,\n      "primary_ip6": null,\n      "comments": "",\n      "custom_fields": {\n        "label": "DB",\n        "env": {\n          "id": 1,\n          "value": "Prod"\n        }\n      }\n    }\n  ]\n}\n')

def mock_response(json_payload):
    response = Response()
    response.status_code = 200
    response.json = MagicMock(return_value=json_payload)
    return MagicMock(return_value=response)


netbox_api_all_hosts = mock_response(netbox_api_output)
netbox_api_output['results'].pop(1)
netbox_api_single_host = mock_response(netbox_api_output)
fake_host = netbox_api_output

class Args(object):
    config_file = 'netbox.yml'
    host = None
    list = True


netbox_inventory = netbox.NetboxAsInventory(Args, netbox_config_data)
Args.list = False
netbox_inventory_default_args = netbox.NetboxAsInventory(Args, netbox_config_data)
Args.host = 'fake_host01'
netbox_inventory_single = netbox.NetboxAsInventory(Args, netbox_config_data)

class TestNetboxUtils(object):

    @pytest.mark.parametrize('source_dict, key_path', [
     ({'a_key': {'b_key': {'c_key': 'c_value'}}},
      [
       'a_key', 'b_key', 'c_key'])])
    def test_get_value_by_path_key_exists(self, source_dict, key_path):
        """
        Test get value by path with exists key.
        """
        reduced_path = netbox_inventory._get_value_by_path(source_dict, key_path)
        assert reduced_path == 'c_value'

    @pytest.mark.parametrize('source_dict, key_path', [
     ({'a_key': {'b_key': {'c_key': 'c_value'}}},
      [
       'a_key', 'b_key', 'any'])])
    def test_get_value_by_path_key_not_exists(self, source_dict, key_path):
        """
        Test get value by path with non-exists key.
        """
        with pytest.raises(SystemExit) as (key_not_exists):
            netbox_inventory._get_value_by_path(source_dict, key_path)
        assert key_not_exists

    @pytest.mark.parametrize('source_dict, key_path, ignore_key_error', [
     ({'a_key': {'b_key': {'c_key': 'c_value'}}},
      [
       'a_key', 'b_key', 'any'],
      True)])
    def test_get_value_by_path_key_not_exists_ignore_error(self, source_dict, key_path, ignore_key_error):
        """
        Test get value by path with exists key and not ignore error.
        """
        reduced_path = netbox_inventory._get_value_by_path(source_dict, key_path, ignore_key_error=ignore_key_error)
        assert reduced_path is None
        return

    @pytest.mark.parametrize('source_dict, key_path, default', [
     ({'a_key': {'b_key': {'c_key': 'c_value'}}},
      [
       'a_key', 'b_key', 'any'],
      'default_value')])
    def test_get_value_by_path_key_not_exists_with_default_value(self, source_dict, key_path, default):
        """
        Test get value by path with exists key and not ignore error.
        """
        reduced_path = netbox_inventory._get_value_by_path(source_dict, key_path, default=default)
        assert reduced_path is 'default_value'

    @pytest.mark.parametrize('yaml_file', [
     'netbox.yml'])
    def test_open_yaml_file_exists(self, yaml_file):
        """
        Test open exists yaml file.
        """
        with patch(builtin_open, new_callable=mock_open, read_data=netbox_config):
            config_output = netbox.open_yaml_file(yaml_file)
            assert config_output['netbox']
            assert config_output['netbox']['main']['api_url']

    @pytest.mark.parametrize('yaml_file', [
     'nonexists.yml'])
    def test_open_yaml_file_not_exists(self, yaml_file):
        """
        Test open non-exists yaml file.
        """
        with pytest.raises(SystemExit) as (file_not_exists):
            netbox.open_yaml_file(yaml_file)
        assert file_not_exists

    @pytest.mark.parametrize('yaml_file', [
     'netbox_invalid_syntax.yml'])
    def test_open_yaml_file_invalid(self, yaml_file):
        """
        Test open invalid yaml file.
        """
        with pytest.raises(SystemExit) as (invalid_yaml_syntax):
            with patch(builtin_open, new_callable=mock_open, read_data=netbox_config_invalid):
                netbox.open_yaml_file(yaml_file)
        assert invalid_yaml_syntax


class TestNetboxAsInventory(object):

    @pytest.mark.parametrize('args, config', [
     (
      Args, {})])
    def test_empty_config_dict(self, args, config):
        """
        Test if Netbox config file is empty.
        """
        with pytest.raises(SystemExit) as (empty_config_error):
            netbox.NetboxAsInventory(args, config)
        assert empty_config_error

    @pytest.mark.parametrize('api_url', [
     netbox_inventory.api_url])
    def test_get_hosts_list(self, api_url):
        """
        Test get hosts list from API without token and make sure it returns a list.
        """
        with patch('requests.get', netbox_api_all_hosts):
            hosts_list = netbox_inventory.get_hosts_list(api_url)
            assert isinstance(hosts_list, list)

    @pytest.mark.parametrize('api_url, api_token', [
     (
      netbox_inventory.api_url, netbox_inventory.api_token)])
    def test_get_hosts_list_token(self, api_url, api_token):
        """
        Test get hosts list from API with token and make sure it returns a list.
        """
        with patch('requests.get', netbox_api_all_hosts):
            hosts_list = netbox_inventory.get_hosts_list(api_url, api_token)
            assert isinstance(hosts_list, list)

    @pytest.mark.parametrize('api_url, api_token', [
     (None, None)])
    def test_get_hosts_list_none_url_value(self, api_url, api_token):
        """
        Test if Netbox URL is invalid.
        """
        with patch('requests.get', netbox_api_all_hosts):
            with pytest.raises(SystemExit) as (none_url_error):
                netbox_inventory.get_hosts_list(api_url, api_token)
            assert none_url_error

    @pytest.mark.parametrize('api_url, api_token, host_name', [
     (
      netbox_inventory_single.api_url, netbox_inventory_single.api_token, netbox_inventory_single.host)])
    def test_get_hosts_list_single_host(self, api_url, api_token, host_name):
        """
        Test Netbox single host output.
        """
        with patch('requests.get', netbox_api_single_host):
            host_data = netbox_inventory_single.get_hosts_list(api_url, api_token, specific_host=host_name)
            print host_data
            assert host_data['name'] == 'fake_host01'

    @pytest.mark.parametrize('server_name, group_value, inventory_dict', [
     (
      'fake_server', 'fake_group', {})])
    def test_add_host_to_group(self, server_name, group_value, inventory_dict):
        """
        Test add host to its group inside inventory dict.
        """
        netbox_inventory.add_host_to_group(server_name, group_value, inventory_dict)
        assert server_name in inventory_dict[group_value]

    @pytest.mark.parametrize('groups_categories, inventory_dict, host_data', [
     ({'default': ['device_role', 'rack', 'platform']}, {'_meta': {'hostvars': {}}},
      fake_host)])
    def test_add_host_to_inventory(self, groups_categories, inventory_dict, host_data):
        """
        Test add host to its group in inventory dict (grouping).
        """
        netbox_inventory.add_host_to_inventory(groups_categories, inventory_dict, host_data)
        assert 'hostvars' in inventory_dict['_meta']
        assert 'fake_rack01' in inventory_dict
        assert 'fake_host01' in inventory_dict['fake_rack01']

    @pytest.mark.parametrize('groups_categories, inventory_dict, host_data', [
     ({'arbitrary_category_name': []}, {'_meta': {'hostvars': {}}},
      fake_host)])
    def test_add_host_to_inventory_with_wrong_category(self, groups_categories, inventory_dict, host_data):
        """
        Test adding host to inventory with wrong category.
        """
        with pytest.raises(KeyError) as (wrong_category_error):
            netbox_inventory.add_host_to_inventory(groups_categories, inventory_dict, host_data)
        assert wrong_category_error

    @pytest.mark.parametrize('groups_categories, inventory_dict, host_data', [
     ({}, {'_meta': {'hostvars': {}}},
      fake_host),
     ({}, {'no_group': [], '_meta': {'hostvars': {}}},
      fake_host)])
    def test_add_host_to_inventory_with_no_group(self, groups_categories, inventory_dict, host_data):
        """
        Test adding host to inventory with no group.
        """
        netbox_inventory.add_host_to_inventory(groups_categories, inventory_dict, host_data)
        assert 'fake_host01' in inventory_dict['no_group']

    @pytest.mark.parametrize('groups_categories, inventory_dict, host_data', [
     ({'default': ['arbitrary_group_name']}, {'_meta': {'hostvars': {}}},
      fake_host)])
    def test_add_host_to_inventory_with_wrong_group(self, groups_categories, inventory_dict, host_data):
        """
        Test add host to inventory with wrong group.
        """
        with pytest.raises(SystemExit) as (no_group_error):
            netbox_inventory.add_host_to_inventory(groups_categories, inventory_dict, host_data)
        assert no_group_error

    @pytest.mark.parametrize('host_data, host_vars', [
     (
      fake_host, {'ip': {'ansible_ssh_host': 'primary_ip'}, 'general': {'rack_name': 'rack'}})])
    def test_get_host_vars(self, host_data, host_vars):
        """
        Test get host vars based on specific tags
        (which come from inventory script config file).
        """
        host_vars = netbox_inventory.get_host_vars(host_data, host_vars)
        assert host_vars['ansible_ssh_host'] == '192.168.0.2'
        assert host_vars['rack_name'] == 'fake_rack01'

    @pytest.mark.parametrize('inventory_dict, host_name, host_vars', [
     ({'_meta': {'hostvars': {}}},
      'fake_host01', {'rack_name': 'fake_rack01'})])
    def test_update_host_meta_vars(self, inventory_dict, host_name, host_vars):
        """
        Test update host vars in inventory dict.
        """
        netbox_inventory.update_host_meta_vars(inventory_dict, host_name, host_vars)
        assert inventory_dict['_meta']['hostvars']['fake_host01']['rack_name'] == 'fake_rack01'

    @pytest.mark.parametrize('inventory_dict, host_name, host_vars', [
     ({'_meta': {'hostvars': {}}},
      'fake_host01', {'rack_name': 'fake_rack01'})])
    def test_update_host_meta_vars_single_host(self, inventory_dict, host_name, host_vars):
        """
        Test update host vars in inventory dict.
        """
        netbox_inventory_single.update_host_meta_vars(inventory_dict, host_name, host_vars)
        assert inventory_dict['fake_host01']['rack_name'] == 'fake_rack01'

    def test_generate_inventory(self):
        """
        Test generateing final Ansible inventory before convert it to JSON.
        """
        with patch('requests.get', netbox_api_all_hosts):
            ansible_inventory = netbox_inventory.generate_inventory()
            assert 'fake_host01' in ansible_inventory['_meta']['hostvars']
            assert isinstance(ansible_inventory['_meta']['hostvars']['fake_host02'], dict)

    @pytest.mark.parametrize('inventory_dict', [
     {'fake_rack01': [
                      'fake_host01', 'fake_host02'], 
        'Fake Server': [
                      'fake_host01'], 
        'Server': [
                 'fake_host02'], 
        '_meta': {'hostvars': {'fake_host02': {'rack_name': 'fake_rack01'}, 'fake_host01': {'ansible_ssh_host': '192.168.0.2', 'rack_name': 'fake_rack01'}}}}])
    def test_print_inventory_json(self, capsys, inventory_dict):
        """
        Test printing final Ansible inventory in JSON format.
        """
        netbox_inventory.print_inventory_json(inventory_dict)
        function_stdout, function_stderr = capsys.readouterr()
        assert not function_stderr
        assert json.loads(function_stdout) == inventory_dict

    @pytest.mark.parametrize('inventory_dict', [
     {'fake_host01': {'ansible_ssh_host': '192.168.0.2', 
                        'rack_name': 'fake_rack01'}}])
    def test_print_inventory_json_single_host(self, capsys, inventory_dict):
        """
        Test printing final Ansible inventory in JSON format for single host.
        """
        netbox_inventory_single.print_inventory_json(inventory_dict)
        function_stdout, function_stderr = capsys.readouterr()
        assert not function_stderr
        assert json.loads(function_stdout) == inventory_dict['fake_host01']

    @pytest.mark.parametrize('inventory_dict', [
     {'fake_rack01': [
                      'fake_host01'], 
        '_meta': {'hostvars': {'fake_host01': {'ansible_ssh_host': '192.168.0.2', 'rack_name': 'fake_rack01'}}}}])
    def test_print_inventory_json_no_list_arg(self, capsys, inventory_dict):
        """
        Test printing final Ansible inventory in JSON format without --list argument.
        """
        netbox_inventory_default_args.print_inventory_json(inventory_dict)
        function_stdout, function_stderr = capsys.readouterr()
        assert not function_stderr
        assert json.loads(function_stdout) == {}