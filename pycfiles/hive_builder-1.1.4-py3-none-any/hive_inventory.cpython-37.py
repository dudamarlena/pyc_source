# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mitsuru/Projects/hive/hive/plugins/hive_inventory.py
# Compiled at: 2019-09-12 05:08:43
# Size of source mod 2**32: 12968 bytes
"""
hive inventory: dynamic inventory plugin for hive
"""
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleParserError
import ipaddress
DOCUMENTATION = '\n  name: hive_inventory\n  plugin_type: inventory\n  short_description: Returns Inventory for hive docker site\n  description:\n    - Generate vpcs, firewall, subnets, hosts resources\n\n  options:\n    plugin:\n      description: token that ensures this is a source file for the \'hive_inventory\' plugin.\n      required: True\n      choices: [\'hive_inventory\']\n    name:\n      description:\n      - name of hive\n      - all hosts can reffernce as hive_name\n      - domein name format(ex. pdns.example.com) is recommended\n      required: True\n    stages:\n      description: stage list\n      required: True\n      suboptions:\n        stage:\n          description: Name of the stage\n          required: true\n          choices: [\'private\', \'staging\', \'production\']\n        provider:\n          description: infrastructure provider\n          required: true\n          choices: [\'vagrant\', \'aws\', \'azure\', \'gcp\', \'openstack\']\n        separate_repository:\n          description: whether repository node is separated from swarm nodes\n          type: bool\n          default: true\n        cidr:\n          description: cidr of vpc\n          required: true\n        inbound_rules:\n          description: inbound rules\n          type: list\n          suboptions:\n            port:\n              description: port number\n              required: true\n              type: int\n            src:\n              description: network addresses to ristrict source ip\n              type: list\n              default: [\'0.0.0.0/0\']\n        number_of_hosts:\n          description: number of hosts\n          default: 4 if separate_repository else 3\n          type: int\n        subnets:\n          description: list of subnet\n          type: list\n          suboptions:\n            cidr:\n              description: cidr of subnet\n              required: true\n            name:\n              description: name of subnet\n              default: "{name of site}_subnet_{index of item}"\n            available_zone:\n              description: available zone of subnet\n              required: true\n        memory_size:\n          description: "memory size of hive hosts(only available when provider is \'vagrant\')"\n          type: int with unit(G,M,K)\n          default: VirtualBox default\n        cpus:\n          description: "number of cpu of hive hosts(only available when provider is \'vagrant\')"\n          type: int\n          default: VirtualBox default\n        instance_type:\n          description: "the instance type of hive hosts(availabe when provider is a IaaS)"\n        image_name:\n          description: "the source image of the hive host(availabe when provider is a IaaS)"\n        region:\n          description: "the region where hive hosts are located (availabe when provider is a IaaS)"\n        disk_size:\n          description: disk size of hive hosts\n          type: int with unit(G,M,K)\n          default: 20G\n        mirrored_disk_size:\n          description: disk size of hosts for drbd mirror disk, if not specified then hive does not provision mirrord disk\n          type: int (megabyte)\n        repository_memory_size:\n          description: "memory size of hosts(only available when provider is \'vagrant\')"\n          type: int with unit(G,M,K)\n          default: 512M\n        repository_instance_type:\n          description: "instance type of host(availabe when provider is a IaaS)"\n        repository_disk_size:\n          description: disk size of hosts\n          type: int with unit(G,M,K)\n          default: 40G\n'
EXAMPLES = '\nplugin: hive_inventory\nname: test.example.com\nstages:\n  private:\n    provider: vagrant\n    separate_repository: False\n    subnets:\n    - cidr: 192.168.0.96/29\n'

class InventoryModule(BaseInventoryPlugin):
    NAME = 'hive_inventory'

    def __init__(self):
        super(InventoryModule, self).__init__()
        self.sites = []

    def verify_file(self, path):
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('.yaml', '.yml')):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self._read_config_data(path)
        self.inventory.add_group('servers')
        self.inventory.add_group('hives')
        self.inventory.add_group('repository')
        self.inventory.add_group('first_hive')
        self.inventory.add_group('mother')
        self.inventory.add_child('servers', 'hives')
        self.inventory.add_child('servers', 'repository')
        self.name = self.get_option('name')
        self.inventory.set_variable('all', 'hive_name', self.name)
        stages = self.get_option('stages')
        for stage_name, option in stages.items():
            stage = Stage(self.name, stage_name, option, inventory)
            stage.set_provider()
            stage.add_stage_group()
            stage.set_subnets()
            stage.add_hives()


class Stage:

    def __init__(self, name, stage_name, option, inventory):
        self.stage_name = stage_name
        self.name = name
        self.stage = option
        self.inventory = inventory
        if self.stage_name not in ('private', 'staging', 'production'):
            raise AnsibleParserError(f'stage must be one of "private", "staging", "production", but specified {self.stage_name}')
        self.stage_prefix = 'p-' if self.stage_name == 'private' else 's-' if self.stage_name == 'staging' else ''

    def set_provider(self):
        if 'provider' not in self.stage:
            raise AnsibleParserError('provider must be specified')
        else:
            self.provider = self.stage['provider']
            if self.provider not in ('vagrant', 'aws', 'azure', 'gcp', 'openstack'):
                raise AnsibleParserError(f'provider must be one of "vagrant", "aws", "azure", "gcp", "openstack", but specified {self.provider}')
            if self.provider == 'vagrant':
                if 'instance_type' in self.stage:
                    raise AnsibleParserError('instance_type cannot be specified when provider is vagrant')
                if 'region' in self.stage:
                    raise AnsibleParserError('region cannot be specified when provider is vagrant')
                if 'memory_size' in self.stage:
                    self.memory_size = self.stage['memory_size']
                if 'repository_memory_size' in self.stage:
                    self.repository_memory_size = self.stage['repository_memory_size']
                if 'cpus' in self.stage:
                    self.cpus = self.stage['cpus']
                if 'repository_cpus' in self.stage:
                    self.repository_cpus = self.stage['repository_cpus']
                if 'disk_size' in self.stage:
                    self.disk_size = self.stage['disk_size']
                if 'repository_disk_size' in self.stage:
                    self.repository_disk_size = self.stage['repository_disk_size']
            else:
                if 'memory_size' in self.stage:
                    raise AnsibleParserError('memory_size cannot be specified when provider is IaaS')
                if 'repository_memory_size' in self.stage:
                    raise AnsibleParserError('repository_memory_size cannot be specified when provider is IaaS')
                if 'instance_type' in self.stage:
                    self.instance_type = self.stage['instance_type']
                if 'repository_instance_type' in self.stage:
                    self.repository_instance_type = self.stage['repository_instance_type']

    def add_stage_group(self):
        self.inventory.add_group(self.stage_name)
        self.inventory.set_variable(self.stage_name, 'hive_provider', self.provider)

    def set_subnets(self):
        self.subnets = []
        if 'cidr' not in self.stage:
            raise AnsibleParserError('cidr must be specified')
        else:
            mother_name = f"{self.stage_prefix}mother.{self.name}"
            self.inventory.add_host(mother_name, group='mother')
            self.inventory.add_host(mother_name, group=(self.stage_name))
            self.inventory.set_variable(mother_name, 'hive_cidr', self.stage['cidr'])
            if 'region' in self.stage:
                self.inventory.set_variable(mother_name, 'hive_region', self.stage['region'])
            if 'subnets' not in self.stage:
                try:
                    net = ipaddress.ip_network(self.stage['cidr'])
                except ValueError as e:
                    try:
                        raise AnsibleParserError(str(e))
                    finally:
                        e = None
                        del e

                hosts = net.hosts()
                next(hosts)
                self.subnets.append({'ip_list':map(str, hosts),  'netmask':str(net.netmask)})
            else:
                var_subnets = []
                for idx, s in enumerate(self.stage['subnets']):
                    subnet = s.copy()
                    var_subnets.append(s)
                    if 'name' not in subnet:
                        subnet['name'] = f"{self.stage_prefix}subnet{idx}"
                    if 'cidr' not in subnet:
                        raise AnsibleParserError('cidr in subnet must be specified')
                    try:
                        net = ipaddress.ip_network(subnet['cidr'])
                    except ValueError as e:
                        try:
                            raise AnsibleParserError(str(e))
                        finally:
                            e = None
                            del e

                    hosts = net.hosts()
                    next(hosts)
                    next(hosts)
                    next(hosts)
                    next(hosts)
                    subnet['ip_list'] = map(str, hosts)
                    subnet['netmask'] = str(net.netmask)
                    self.subnets.append(subnet)

                self.inventory.set_variable(mother_name, 'hive_subnets', var_subnets)

    def add_hives(self):
        separate_repository = self.stage['separate_repository'] if 'separate_repository' in self.stage else True
        number_of_hosts = self.stage.get('number_of_hosts', 4 if separate_repository else 3)
        for idx in range(number_of_hosts):
            host_name = f"{self.stage_prefix}hive{idx}.{self.name}"
            self.inventory.add_host(host_name, group=(self.stage_name))
            if idx == number_of_hosts - 1 and not separate_repository:
                self.inventory.add_host(host_name, group='hives')
                if hasattr(self, 'memory_size'):
                    self.inventory.set_variable(host_name, 'hive_memory_size', self.memory_size)
                if hasattr(self, 'cpus'):
                    self.inventory.set_variable(host_name, 'hive_cpus', self.memory_size)
                if hasattr(self, 'disk_size'):
                    self.inventory.set_variable(host_name, 'hive_disk_size', self.disk_size)
                if hasattr(self, 'instance_type'):
                    self.inventory.set_variable(host_name, 'hive_instance_type', self.instance_type)
                if 'mirrored_disk_size' in self.stage:
                    self.inventory.set_variable(host_name, 'hive_mirrored_disk_size', self.stage['mirrored_disk_size'])
                self.inventory.add_host(host_name, group='repository')
                if hasattr(self, 'repository_memory_size'):
                    self.inventory.set_variable(host_name, 'hive_memory_size', self.repository_memory_size)
                if hasattr(self, 'repository_cpus'):
                    self.inventory.set_variable(host_name, 'hive_cpus', self.repository_memory_size)
                if hasattr(self, 'repository_disk_size'):
                    self.inventory.set_variable(host_name, 'hive_disk_size', self.repository_disk_size)
                if hasattr(self, 'repository_instance_type'):
                    self.inventory.set_variable(host_name, 'hive_instance_type', self.repository_instance_type)
                else:
                    self.inventory.add_host(host_name, group='hives')
                    if hasattr(self, 'memory_size'):
                        self.inventory.set_variable(host_name, 'hive_memory_size', self.memory_size)
                    if hasattr(self, 'cpus'):
                        self.inventory.set_variable(host_name, 'hive_cpus', self.memory_size)
                    if hasattr(self, 'disk_size'):
                        self.inventory.set_variable(host_name, 'hive_disk_size', self.disk_size)
                    if hasattr(self, 'instance_type'):
                        self.inventory.set_variable(host_name, 'hive_instance_type', self.instance_type)
                    if 'mirrored_disk_size' in self.stage:
                        self.inventory.set_variable(host_name, 'hive_mirrored_disk_size', self.stage['mirrored_disk_size'])
                    if 'image_name' in self.stage:
                        self.inventory.set_variable(host_name, 'hive_image_name', self.stage['image_name'])
                    subnet = self.subnets[(idx % len(self.subnets))]
                    if 'name' in subnet:
                        self.inventory.set_variable(host_name, 'hive_subnet', subnet['name'])
                    if 'available_zone' in subnet:
                        self.inventory.set_variable(host_name, 'hive_available_zone', subnet['available_zone'])
                    self.inventory.set_variable(host_name, 'hive_private_ip', next(subnet['ip_list']))
                    self.inventory.set_variable(host_name, 'hive_netmask', subnet['netmask'])

        self.inventory.set_variable('hives', 'hive_swarm_master', f"{self.stage_prefix}hive0.{self.name}")
        self.inventory.add_host(f"{self.stage_prefix}hive0.{self.name}", group='first_hive')


class providerBase:

    def __init__(self, name):
        self.name = name