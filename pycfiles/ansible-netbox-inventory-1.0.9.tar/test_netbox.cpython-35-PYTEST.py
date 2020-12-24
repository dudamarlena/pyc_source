# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aabouzaid/git/mine/netbox-as-ansible-inventory/tests/test_netbox.py
# Compiled at: 2017-12-05 17:11:17
# Size of source mod 2**32: 17121 bytes
from __future__ import absolute_import
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys, json, yaml, pytest
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
netbox_api_output = json.loads('\n[\n  {\n    "id": 1,\n    "name": "fake_host01",\n    "display_name": "Fake Host",\n    "device_type": {\n      "id": 1,\n      "manufacturer": {\n        "id": 8,\n        "name": "Fake Manufacturer",\n        "slug": "fake_manufacturer"\n      },\n      "model": "all",\n      "slug": "all"\n    },\n    "device_role": {\n      "id": 8,\n      "name": "Fake Server",\n      "slug": "fake_server"\n    },\n    "tenant": null,\n    "platform": null,\n    "serial": "",\n    "asset_tag": "fake_tag",\n    "rack": {\n      "id": 1,\n      "name": "fake_rack01",\n      "facility_id": null,\n      "display_name": "Fake Rack01"\n    },\n    "position": null,\n    "face": null,\n    "parent_device": null,\n    "status": true,\n    "primary_ip": {\n      "id": 1,\n      "family": 4,\n      "address": "192.168.0.2/32"\n    },\n    "primary_ip4": {\n      "id": 1,\n      "family": 4,\n      "address": "192.168.0.2/32"\n    },\n    "primary_ip6": null,\n    "comments": "",\n    "custom_fields": {\n      "label": "Web",\n      "env": {\n        "id": 1,\n        "value": "Prod"\n      }\n    }\n  },\n  {\n    "id": 2,\n    "name": "fake_host02",\n    "display_name": "fake_host02",\n    "device_type": {\n      "id": 1,\n      "manufacturer": {\n        "id": 8,\n        "name": "Super Micro",\n        "slug": "super-micro"\n      },\n      "model": "all",\n      "slug": "all"\n    },\n    "device_role": {\n      "id": 8,\n      "name": "Server",\n      "slug": "server"\n    },\n    "tenant": null,\n    "platform": null,\n    "serial": "",\n    "asset_tag": "xtag",\n    "rack": {\n      "id": 1,\n      "name": "fake_rack01",\n      "facility_id": null,\n      "display_name": "Fake Host 02"\n    },\n    "position": null,\n    "face": null,\n    "parent_device": null,\n    "status": true,\n    "primary_ip": null,\n    "primary_ip4": null,\n    "primary_ip6": null,\n    "comments": "",\n    "custom_fields": {\n      "label": "DB",\n      "env": {\n        "id": 1,\n        "value": "Prod"\n      }\n    }\n  }\n]\n')

def mock_response(json_payload):
    response = Response()
    response.status_code = 200
    response.json = MagicMock(return_value=json_payload)
    return MagicMock(return_value=response)


netbox_api_all_hosts = mock_response(netbox_api_output)
netbox_api_single_host = mock_response(netbox_api_output[0])
fake_host = netbox_api_output[0]

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
     (
      {'a_key': {'b_key': {'c_key': 'c_value'}}},
      [
       'a_key', 'b_key', 'c_key'])])
    def test_get_value_by_path_key_exists(self, source_dict, key_path):
        """
        Test get value by path with exists key.
        """
        reduced_path = netbox_inventory._get_value_by_path(source_dict, key_path)
        @py_assert2 = 'c_value'
        @py_assert1 = reduced_path == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (reduced_path, @py_assert2)) % {'py0': @pytest_ar._saferepr(reduced_path) if 'reduced_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reduced_path) else 'reduced_path', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    @pytest.mark.parametrize('source_dict, key_path', [
     (
      {'a_key': {'b_key': {'c_key': 'c_value'}}},
      [
       'a_key', 'b_key', 'any'])])
    def test_get_value_by_path_key_not_exists(self, source_dict, key_path):
        """
        Test get value by path with non-exists key.
        """
        with pytest.raises(SystemExit) as (key_not_exists):
            netbox_inventory._get_value_by_path(source_dict, key_path)
        if not key_not_exists:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(key_not_exists) if 'key_not_exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(key_not_exists) else 'key_not_exists'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))

    @pytest.mark.parametrize('source_dict, key_path, ignore_key_error', [
     (
      {'a_key': {'b_key': {'c_key': 'c_value'}}},
      [
       'a_key', 'b_key', 'any'],
      True)])
    def test_get_value_by_path_key_not_exists_ignore_error(self, source_dict, key_path, ignore_key_error):
        """
        Test get value by path with exists key and not ignore error.
        """
        reduced_path = netbox_inventory._get_value_by_path(source_dict, key_path, ignore_key_error=ignore_key_error)
        @py_assert2 = None
        @py_assert1 = reduced_path is @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (reduced_path, @py_assert2)) % {'py0': @pytest_ar._saferepr(reduced_path) if 'reduced_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reduced_path) else 'reduced_path', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    @pytest.mark.parametrize('source_dict, key_path, default', [
     (
      {'a_key': {'b_key': {'c_key': 'c_value'}}},
      [
       'a_key', 'b_key', 'any'],
      'default_value')])
    def test_get_value_by_path_key_not_exists_with_default_value(self, source_dict, key_path, default):
        """
        Test get value by path with exists key and not ignore error.
        """
        reduced_path = netbox_inventory._get_value_by_path(source_dict, key_path, default=default)
        @py_assert2 = 'default_value'
        @py_assert1 = reduced_path is @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (reduced_path, @py_assert2)) % {'py0': @pytest_ar._saferepr(reduced_path) if 'reduced_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reduced_path) else 'reduced_path', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    @pytest.mark.parametrize('yaml_file', [
     'netbox.yml'])
    def test_open_yaml_file_exists(self, yaml_file):
        """
        Test open exists yaml file.
        """
        with patch(builtin_open, new_callable=mock_open, read_data=netbox_config):
            config_output = netbox.open_yaml_file(yaml_file)
            @py_assert0 = config_output['netbox']
            if not @py_assert0:
                @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format2))
            @py_assert0 = None
            @py_assert0 = config_output['netbox']['main']['api_url']
            if not @py_assert0:
                @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format2))
            @py_assert0 = None

    @pytest.mark.parametrize('yaml_file', [
     'nonexists.yml'])
    def test_open_yaml_file_not_exists(self, yaml_file):
        """
        Test open non-exists yaml file.
        """
        with pytest.raises(SystemExit) as (file_not_exists):
            netbox.open_yaml_file(yaml_file)
        if not file_not_exists:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(file_not_exists) if 'file_not_exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file_not_exists) else 'file_not_exists'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))

    @pytest.mark.parametrize('yaml_file', [
     'netbox_invalid_syntax.yml'])
    def test_open_yaml_file_invalid(self, yaml_file):
        """
        Test open invalid yaml file.
        """
        with pytest.raises(SystemExit) as (invalid_yaml_syntax):
            with patch(builtin_open, new_callable=mock_open, read_data=netbox_config_invalid):
                netbox.open_yaml_file(yaml_file)
        if not invalid_yaml_syntax:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(invalid_yaml_syntax) if 'invalid_yaml_syntax' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(invalid_yaml_syntax) else 'invalid_yaml_syntax'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))


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
        if not empty_config_error:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(empty_config_error) if 'empty_config_error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(empty_config_error) else 'empty_config_error'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))

    @pytest.mark.parametrize('api_url', [
     netbox_inventory.api_url])
    def test_get_hosts_list(self, api_url):
        """
        Test get hosts list from API without token and make sure it returns a list.
        """
        with patch('requests.get', netbox_api_all_hosts):
            hosts_list = netbox_inventory.get_hosts_list(api_url)
            @py_assert3 = isinstance(hosts_list, list)
            if not @py_assert3:
                @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(hosts_list) if 'hosts_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hosts_list) else 'hosts_list', 'py2': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format5))
            @py_assert3 = None

    @pytest.mark.parametrize('api_url, api_token', [
     (
      netbox_inventory.api_url, netbox_inventory.api_token)])
    def test_get_hosts_list_token(self, api_url, api_token):
        """
        Test get hosts list from API with token and make sure it returns a list.
        """
        with patch('requests.get', netbox_api_all_hosts):
            hosts_list = netbox_inventory.get_hosts_list(api_url, api_token)
            @py_assert3 = isinstance(hosts_list, list)
            if not @py_assert3:
                @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(hosts_list) if 'hosts_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hosts_list) else 'hosts_list', 'py2': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format5))
            @py_assert3 = None

    @pytest.mark.parametrize('api_url, api_token', [
     (None, None)])
    def test_get_hosts_list_none_url_value(self, api_url, api_token):
        """
        Test if Netbox URL is invalid.
        """
        with patch('requests.get', netbox_api_all_hosts):
            with pytest.raises(SystemExit) as (none_url_error):
                netbox_inventory.get_hosts_list(api_url, api_token)
            if not none_url_error:
                @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(none_url_error) if 'none_url_error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(none_url_error) else 'none_url_error'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format1))

    @pytest.mark.parametrize('api_url, api_token, host_name', [
     (
      netbox_inventory_single.api_url, netbox_inventory_single.api_token, netbox_inventory_single.host)])
    def test_get_hosts_list_single_host(self, api_url, api_token, host_name):
        """
        Test Netbox single host output.
        """
        with patch('requests.get', netbox_api_single_host):
            host_data = netbox_inventory_single.get_hosts_list(api_url, api_token, specific_host=host_name)
            @py_assert0 = host_data['name']
            @py_assert3 = 'fake_host01'
            @py_assert2 = @py_assert0 == @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None

    @pytest.mark.parametrize('server_name, group_value, inventory_dict', [
     (
      'fake_server', 'fake_group', {})])
    def test_add_host_to_group(self, server_name, group_value, inventory_dict):
        """
        Test add host to its group inside inventory dict.
        """
        netbox_inventory.add_host_to_group(server_name, group_value, inventory_dict)
        @py_assert2 = inventory_dict[group_value]
        @py_assert1 = server_name in @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py3)s', ), (server_name, @py_assert2)) % {'py0': @pytest_ar._saferepr(server_name) if 'server_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(server_name) else 'server_name', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    @pytest.mark.parametrize('groups_categories, inventory_dict, host_data', [
     (
      {'default': ['device_role', 'rack', 'platform']},
      {'_meta': {'hostvars': {}}},
      fake_host)])
    def test_add_host_to_inventory(self, groups_categories, inventory_dict, host_data):
        """
        Test add host to its group in inventory dict (grouping).
        """
        netbox_inventory.add_host_to_inventory(groups_categories, inventory_dict, host_data)
        @py_assert0 = 'hostvars'
        @py_assert3 = inventory_dict['_meta']
        @py_assert2 = @py_assert0 in @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = 'fake_rack01'
        @py_assert2 = @py_assert0 in inventory_dict
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, inventory_dict)) % {'py3': @pytest_ar._saferepr(inventory_dict) if 'inventory_dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inventory_dict) else 'inventory_dict', 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'fake_host01'
        @py_assert3 = inventory_dict['fake_rack01']
        @py_assert2 = @py_assert0 in @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    @pytest.mark.parametrize('groups_categories, inventory_dict, host_data', [
     (
      {'arbitrary_category_name': []},
      {'_meta': {'hostvars': {}}},
      fake_host)])
    def test_add_host_to_inventory_with_wrong_category(self, groups_categories, inventory_dict, host_data):
        """
        Test adding host to inventory with wrong category.
        """
        with pytest.raises(KeyError) as (wrong_category_error):
            netbox_inventory.add_host_to_inventory(groups_categories, inventory_dict, host_data)
        if not wrong_category_error:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(wrong_category_error) if 'wrong_category_error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(wrong_category_error) else 'wrong_category_error'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))

    @pytest.mark.parametrize('groups_categories, inventory_dict, host_data', [
     ({},
      {'_meta': {'hostvars': {}}},
      fake_host),
     ({},
      {'no_group': [], '_meta': {'hostvars': {}}},
      fake_host)])
    def test_add_host_to_inventory_with_no_group(self, groups_categories, inventory_dict, host_data):
        """
        Test adding host to inventory with no group.
        """
        netbox_inventory.add_host_to_inventory(groups_categories, inventory_dict, host_data)
        @py_assert0 = 'fake_host01'
        @py_assert3 = inventory_dict['no_group']
        @py_assert2 = @py_assert0 in @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    @pytest.mark.parametrize('groups_categories, inventory_dict, host_data', [
     (
      {'default': ['arbitrary_group_name']},
      {'_meta': {'hostvars': {}}},
      fake_host)])
    def test_add_host_to_inventory_with_wrong_group(self, groups_categories, inventory_dict, host_data):
        """
        Test add host to inventory with wrong group.
        """
        with pytest.raises(SystemExit) as (no_group_error):
            netbox_inventory.add_host_to_inventory(groups_categories, inventory_dict, host_data)
        if not no_group_error:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(no_group_error) if 'no_group_error' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(no_group_error) else 'no_group_error'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))

    @pytest.mark.parametrize('host_data, host_vars', [
     (
      fake_host,
      {'ip': {'ansible_ssh_host': 'primary_ip'}, 'general': {'rack_name': 'rack'}})])
    def test_get_host_vars(self, host_data, host_vars):
        """
        Test get host vars based on specific tags
        (which come from inventory script config file).
        """
        host_vars = netbox_inventory.get_host_vars(host_data, host_vars)
        @py_assert0 = host_vars['ansible_ssh_host']
        @py_assert3 = '192.168.0.2'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = host_vars['rack_name']
        @py_assert3 = 'fake_rack01'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    @pytest.mark.parametrize('inventory_dict, host_name, host_vars', [
     (
      {'_meta': {'hostvars': {}}},
      'fake_host01',
      {'rack_name': 'fake_rack01'})])
    def test_update_host_meta_vars(self, inventory_dict, host_name, host_vars):
        """
        Test update host vars in inventory dict.
        """
        netbox_inventory.update_host_meta_vars(inventory_dict, host_name, host_vars)
        @py_assert0 = inventory_dict['_meta']['hostvars']['fake_host01']['rack_name']
        @py_assert3 = 'fake_rack01'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    @pytest.mark.parametrize('inventory_dict, host_name, host_vars', [
     (
      {'_meta': {'hostvars': {}}},
      'fake_host01',
      {'rack_name': 'fake_rack01'})])
    def test_update_host_meta_vars_single_host(self, inventory_dict, host_name, host_vars):
        """
        Test update host vars in inventory dict.
        """
        netbox_inventory_single.update_host_meta_vars(inventory_dict, host_name, host_vars)
        @py_assert0 = inventory_dict['fake_host01']['rack_name']
        @py_assert3 = 'fake_rack01'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_generate_inventory(self):
        """
        Test generateing final Ansible inventory before convert it to JSON.
        """
        with patch('requests.get', netbox_api_all_hosts):
            ansible_inventory = netbox_inventory.generate_inventory()
            @py_assert0 = 'fake_host01'
            @py_assert3 = ansible_inventory['_meta']['hostvars']
            @py_assert2 = @py_assert0 in @py_assert3
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None
            @py_assert1 = ansible_inventory['_meta']['hostvars']['fake_host02']
            @py_assert4 = isinstance(@py_assert1, dict)
            if not @py_assert4:
                @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py3': @pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dict) else 'dict', 'py2': @pytest_ar._saferepr(@py_assert1)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert4 = None

    @pytest.mark.parametrize('inventory_dict', [
     {'fake_rack01': ['fake_host01', 'fake_host02'], 
      'Fake Server': ['fake_host01'], 
      'Server': ['fake_host02'], 
      '_meta': {'hostvars': {'fake_host02': {'rack_name': 'fake_rack01'}, 
                             'fake_host01': {'ansible_ssh_host': '192.168.0.2', 'rack_name': 'fake_rack01'}}}}])
    def test_print_inventory_json(self, capsys, inventory_dict):
        """
        Test printing final Ansible inventory in JSON format.
        """
        netbox_inventory.print_inventory_json(inventory_dict)
        function_stdout, function_stderr = capsys.readouterr()
        @py_assert1 = not function_stderr
        if not @py_assert1:
            @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(function_stderr) if 'function_stderr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(function_stderr) else 'function_stderr'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert1 = None
        @py_assert1 = json.loads
        @py_assert4 = @py_assert1(function_stdout)
        @py_assert6 = @py_assert4 == inventory_dict
        if not @py_assert6:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.loads\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, inventory_dict)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(inventory_dict) if 'inventory_dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inventory_dict) else 'inventory_dict', 'py0': @pytest_ar._saferepr(json) if 'json' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(json) else 'json', 'py3': @pytest_ar._saferepr(function_stdout) if 'function_stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(function_stdout) else 'function_stdout', 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert4 = @py_assert6 = None

    @pytest.mark.parametrize('inventory_dict', [
     {'fake_host01': {'ansible_ssh_host': '192.168.0.2', 
                      'rack_name': 'fake_rack01'}}])
    def test_print_inventory_json_single_host(self, capsys, inventory_dict):
        """
        Test printing final Ansible inventory in JSON format for single host.
        """
        netbox_inventory_single.print_inventory_json(inventory_dict)
        function_stdout, function_stderr = capsys.readouterr()
        @py_assert1 = not function_stderr
        if not @py_assert1:
            @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(function_stderr) if 'function_stderr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(function_stderr) else 'function_stderr'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert1 = None
        @py_assert1 = json.loads
        @py_assert4 = @py_assert1(function_stdout)
        @py_assert7 = inventory_dict['fake_host01']
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.loads\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(json) if 'json' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(json) else 'json', 'py3': @pytest_ar._saferepr(function_stdout) if 'function_stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(function_stdout) else 'function_stdout', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    @pytest.mark.parametrize('inventory_dict', [
     {'fake_rack01': ['fake_host01'], 
      '_meta': {'hostvars': {'fake_host01': {'ansible_ssh_host': '192.168.0.2', 'rack_name': 'fake_rack01'}}}}])
    def test_print_inventory_json_no_list_arg(self, capsys, inventory_dict):
        """
        Test printing final Ansible inventory in JSON format without --list argument.
        """
        netbox_inventory_default_args.print_inventory_json(inventory_dict)
        function_stdout, function_stderr = capsys.readouterr()
        @py_assert1 = not function_stderr
        if not @py_assert1:
            @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(function_stderr) if 'function_stderr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(function_stderr) else 'function_stderr'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert1 = None
        @py_assert1 = json.loads
        @py_assert4 = @py_assert1(function_stdout)
        @py_assert7 = {}
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.loads\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(json) if 'json' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(json) else 'json', 'py3': @pytest_ar._saferepr(function_stdout) if 'function_stdout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(function_stdout) else 'function_stdout', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None