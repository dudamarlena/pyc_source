# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/vm.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.common.Error import Error
from uuid import UUID
from cloudmesh_client.common.dotdict import dotdict
from builtins import input
from pprint import pprint
from cloudmesh_client.cloud.network import Network
from cloudmesh_client.default import Names, Default
import traceback

class Vm(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def generate_vm_name(cls, prefix=None, fill=3):
        return Default.generate_name(Names.VM_COUNTER, display_name=Default.user, prefix=prefix, fill=fill)

    @classmethod
    def uuid(cls, name, category=None):
        vm = cls.get(name, category=category)
        if vm is None:
            return
        else:
            return vm.uuid

    @classmethod
    def get(cls, key, category=None):
        """
        returns the value of the first objects matching the key
        with the given category.

        :param key: The dictionary key
        :param category: The category
        :return:
        """
        if category is None:
            o = cls.cm.find(kind='vm', output='dict', scope='first', name=key)
        else:
            o = cls.cm.find(category=category, kind='vm', output='dict', scope='first', name=key)
        return o

    @classmethod
    def construct_ip_dict(cls, ip_addr, name=None):
        if name is None:
            Console.error('cloud name not set')
            return
        else:
            try:
                d = ConfigDict('cloudmesh.yaml')
                cloud_details = d['cloudmesh']['clouds'][name]
                if cloud_details['cm_type'] == 'openstack':
                    ipaddr = {}
                    for network in ip_addr:
                        index = 0
                        for ip in ip_addr[network]:
                            ipaddr[index] = {}
                            ipaddr[index]['network'] = network
                            ipaddr[index]['version'] = ip['version']
                            ipaddr[index]['addr'] = ip['addr']
                            index += 1

                    return ipaddr
                if cloud_details['cm_type'] == 'ec2':
                    index = 0
                    ipaddr = {}
                    ipaddr[index] = {}
                    ipaddr[index]['addr'] = ip_addr
                    return ipaddr
                if cloud_details['cm_type'] == 'azure':
                    index = 0
                    ipaddr = {}
                    for ip in ip_addr:
                        ipaddr[index] = {}
                        ipaddr[index]['network'] = ip
                        ipaddr[index]['version'] = 'ipv4'
                        ipaddr[index]['addr'] = ip
                        index += 1

                    return ipaddr
            except Exception as e:
                Console.error('error in vm construct dict %s' % e, traceflag=True)

            return

    @classmethod
    def isUuid(cls, name):
        try:
            UUID(name, version=4)
            return True
        except ValueError:
            return False

    @classmethod
    def boot(cls, **kwargs):
        arg = dotdict(kwargs)
        for a in ['key', 'name', 'image', 'flavor']:
            if a not in kwargs:
                raise ValueError(a + ' not in arguments to vm boot')

        conf = ConfigDict('cloudmesh.yaml')
        arg.user = arg.user or conf['cloudmesh']['profile']['user']
        arg.group = arg.group or Default.group
        cloud_provider = CloudProvider(arg.cloud).provider
        if 'nics' in arg:
            nics = arg.nics
        else:
            nics = None
        basic_dict = {'cloud': arg.cloud, 
           'name': arg.name, 
           'image': arg.image, 
           'flavor': arg.flavor, 
           'key': arg.key, 
           'secgroup': [
                      arg.secgroup], 
           'nics': nics, 
           'meta': {'kind': 'cloudmesh', 
                    'group': arg.group, 
                    'cluster': arg.get('cluster', None), 
                    'image': arg.image, 
                    'flavor': arg.flavor, 
                    'key': arg.key, 
                    'category': arg.cloud}}
        if arg.cloud == 'azure':
            kwargs = dict()
            kwargs['kind'] = 'key_azure'
            db_result = cls.cm.find(**kwargs)
            key_result = None
            try:
                for key in db_result:
                    if key['name'] == arg.key:
                        pprint('Found the key')
                        key_result = key
                        break

                if key_result is not None:
                    new_dict_items = dict()
                    new_dict_items['cert_thumbprint'] = key_result['fingerprint']
                    new_dict_items['pub_key_path'] = key_result['key_path']
                    new_dict_items['cert_path'] = key_result['certificate']
                    new_dict_items['pfx_path'] = key_result['pfx_path']
                    basic_dict.update(new_dict_items)
                else:
                    pprint('None found in DB')
            except:
                traceback.print_exc()
                pprint('Exception while processing azure boot arguments')

        d = dotdict(basic_dict)
        Console.ok(('Machine {name} is being booted on cloud {cloud} ...').format(**arg))
        print(Printer.attribute(d))
        vm = cloud_provider.boot_vm(**d)
        if vm is not None:
            cls.refresh(cloud=arg.cloud)
            try:
                cls.cm.set(d.name, 'key', d.key, scope='first', kind='vm')
                cls.cm.set(d.name, 'image', d.image, scope='first', kind='vm')
                cls.cm.set(d.name, 'flavor', d.flavor, scope='first', kind='vm')
                cls.cm.set(d.name, 'group', arg.group, scope='first', kind='vm')
                cls.cm.set(d.name, 'user', arg.user, scope='first', kind='vm')
                cls.cm.set(d.name, 'username', arg.username, scope='first', kind='vm')
                cls.cm.set(d.name, 'cluster', arg.cluster, scope='first', kind='vm')
            except:
                import sys
                Console.warning('cls.cm.set error: %s' % sys.exc_info()[0])

        return vm

    @classmethod
    def start(cls, **kwargs):
        arg = dotdict(kwargs)
        cloud_provider = CloudProvider(arg.cloud).provider
        for server in kwargs['servers']:
            cloud_provider.start_vm(server)
            Console.ok(('Machine {:} is being started on {:} Cloud...').format(server, cloud_provider.cloud))

    @classmethod
    def stop(cls, **kwargs):
        arg = dotdict(kwargs)
        cloud_provider = CloudProvider(arg.cloud).provider
        for server in kwargs['servers']:
            cloud_provider.stop_vm(server)
            Console.ok(('Machine {:} is being stopped on {:} Cloud...').format(server, cloud_provider.cloud))

    @classmethod
    def delete(cls, **kwargs):
        arg = dotdict(kwargs)
        force = kwargs.get('force', Default.purge)
        if 'cloud' in arg:
            cloud_provider = CloudProvider(arg.cloud).provider
            for server in kwargs['servers']:
                vm = cls.cm.find(name=server, kind='vm', cloud=arg.cloud, scope='first')
                if vm:
                    provider = vm['provider']
                    cloud = vm['category']
                    server_dict = Network.get_instance_dict(cloudname=arg.cloud, instance_id=server)
                    floating_ip = server_dict['floating_ip']
                    if floating_ip is not None:
                        Network.disassociate_floating_ip(cloudname=arg.cloud, instance_name=server, floating_ip=floating_ip)
                    cloud_provider.delete_vm(server)
                    if force:
                        cls.cm.delete(kind='vm', provider=provider, category=cloud, name=server)
                        Console.ok(('VM record {:} is being deleted from the local database...').format(server))
                    else:
                        cls.cm.set(server, 'status', 'deleted', kind='vm', scope='first')
                else:
                    Console.error(('VM {:} can not be found.').format(server), traceflag=False)

        else:
            clouds = set()
            for server in arg.servers:
                vm = cls.cm.find(kind='vm', name=server, scope='first')
                if vm:
                    cloud = vm['category']
                    provider = vm['provider']
                    cloud_provider = CloudProvider(cloud).provider
                    clouds.add(cloud)
                    cloud_provider.delete_vm(server)
                    if force:
                        cls.cm.delete(kind='vm', provider=provider, category=cloud, name=server)
                        Console.ok(('VM record {:} is being deleted from the local database...').format(server))
                    else:
                        cls.cm.set(server, 'status', 'deleted', kind='vm', scope='first')
                else:
                    Console.error(('VM {:} can not be found.').format(server), traceflag=False)

        return

    @classmethod
    def get_vms_by_name(cls, name, cloud):
        vm_data = cls.cm.find(kind='vm', name=name, category=cloud)
        if vm_data is None or len(vm_data) == 0:
            raise RuntimeError('VM data not found in database.')
        return vm_data

    @classmethod
    def get_vms_by_group(cls, name):
        group = cls.cm.find(kind='group', name=name)
        return group

    @classmethod
    def get_vm(cls, name):
        vm = cls.cm.find(kind='vm', name=name)
        return vm

    @classmethod
    def rename(cls, **kwargs):
        arg = dotdict(kwargs)
        cloud_provider = CloudProvider(kwargs['cloud']).provider
        vms = cls.get_vms_by_name(name=arg.oldname, cloud=arg.cloud)
        if len(vms) > 1:
            users_choice = 'y'
            if not arg.force:
                print(('More than 1 vms found with the same name as {}.').format(server))
                users_choice = input('Would you like to auto-order the new names? (y/n): ')
            if users_choice.strip() == 'y':
                count = 1
                for index in vms:
                    count_new_name = ('{0}{1}').format(arg.newname, count)
                    cloud_provider.rename_vm(vms[index]['uuid'], count_new_name)
                    print(('Machine {0} with UUID {1} renamed to {2} on {3} cloud').format(vms[index]['name'], vms[index]['uuid'], count_new_name, cloud_provider.cloud))
                    count += 1

            elif users_choice.strip() == 'n':
                cloud_provider.rename_vm(arg.oldname, arg.newname)
                print(('Machine {0} renamed to {1} on {2} Cloud...').format(arg.oldname, arg.newname, cloud_provider.cloud))
            else:
                Console.error('Invalid Choice.')
                return
        else:
            cloud_provider.rename_vm(arg.oldname, arg.newname)
            print(('Machine {0} renamed to {1} on {2} Cloud...').format(arg.oldname, arg.newname, cloud_provider.cloud))
        cls.refresh(cloud=arg.cloud)

    @classmethod
    def info(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def list(cls, **kwargs):
        """
        This method lists all VMs of the cloud
        """
        arg = dotdict(kwargs)
        if 'name' in arg:
            arg.name = arg.name
        arg.output = arg.output or 'table'

        def vm_groups(vm):
            """

            :param vm: name of the vm
            :return: a list of groups the vm is in
            """
            try:
                query = {'kind': 'group', 
                   'provider': 'general', 
                   'species': 'vm', 
                   'member': vm, 
                   'scope': 'all', 
                   'output': 'dict'}
                d = cls.cm.find(**query)
                groups_vm = set()
                if d is not None and len(d) > 0:
                    for vm in d:
                        groups_vm.add(vm['name'])

                return list(groups_vm)
            except Exception as ex:
                Console.error(ex.message)

            return []

        try:
            if 'name' in arg and arg.name is not None:
                if cls.isUuid(arg.name):
                    elements = cls.cm.find(kind='vm', category=arg.category, uuid=arg.name)
                else:
                    elements = cls.cm.find(kind='vm', category=arg.category, label=arg.name)
            else:
                elements = cls.cm.find(kind='vm', category=arg.category)
            if elements is None or len(elements) == 0:
                return
            for elem in elements:
                element = elem
                name = element['name']
                groups = vm_groups(name)
                element['group'] = (',').join(groups)

            order, header = CloudProvider(arg.category).get_attributes('vm')
            if 'name' in arg and arg.name is not None:
                return Printer.attribute(elements[0], output=arg.output)
            return Printer.write(elements, order=order, output=arg.output)
        except Exception as ex:
            Console.error(ex.message)

        return

    @classmethod
    def clear(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def refresh(cls, **kwargs):
        refreshed = cls.cm.refresh('vm', kwargs['cloud'])
        vms = cls.cm.find(kind='vm')
        me = Default.user
        for vm in vms:
            name = vm['name']
            if not name.startswith(me):
                continue
            number = name.split('-')[(-1)]
            try:
                new_counter = int(number) + 1
            except ValueError:
                continue

            old_counter = Default.get_counter(Names.VM_COUNTER)
            counter = max(new_counter, old_counter)
            Default.set_counter(Names.VM_COUNTER, counter)

        Console.debug_msg('Set counter ' + Names.VM_COUNTER + ' to ' + str(Default.get_counter(Names.VM_COUNTER)))
        return refreshed

    @classmethod
    def status_from_cloud(cls, **kwargs):
        cloud_provider = CloudProvider(kwargs['cloud']).provider
        vm = cloud_provider.get_vm(name=kwargs['name'])
        return vm['status']

    @classmethod
    def set_login_user(cls, name=None, cloud=None, username=None):
        vm = Vm.get(name, category=cloud)
        if vm is None:
            Console.error('VM could not be found', traceflag=False)
            return
        else:
            cls.cm.update(kind='vm', provider=vm['provider'], filter={'name': name}, update={'username': username})
            return

    @classmethod
    def get_login_user(cls, name, cloud):
        print(name, cloud)
        Console.error('this method is wrong implemented')

    @classmethod
    def get_vm_public_ip(cls, vm_name, cloud):
        """

        :param vm_name: Name of the VM instance whose Public IP has to be retrieved from the DB
        :param cloud: Libcloud supported Cloud provider name
        :return: Public IP as a list
        """
        public_ip_list = []
        vms = cls.get_vms_by_name(vm_name, cloud)
        keys = vms.keys()
        if keys is not None and len(keys) > 0:
            public_ip = vms[keys[0]]['public_ips']
            if public_ip is not None and public_ip != '':
                public_ip_list.append(public_ip)
        return public_ip_list