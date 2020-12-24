# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_basic/test_cloud_model.py
# Compiled at: 2017-04-23 10:30:41
__doc__ = ' run with\n\npython setup.py install; nosetests -v --nocapture tests/cm_basic/test_model.py:Test_model.test_001\n\nnosetests -v --nocapture tests/cm_basic/test_model.py\n\nor\n\nnosetests -v tests/cm_basic/test_model.py\n\n'
from __future__ import print_function
from pprint import pprint
from cloudmesh_client.common.FlatDict import FlatDict
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.db import VM_OPENSTACK, VM_LIBCLOUD
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.default import Default
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.util import banner

class Test_cloud_model(object):
    cm = CloudmeshDatabase()
    data = dotdict({'cloud': Default.cloud})

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c='-')
        print(command)
        parameter = command.split(' ')
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print(result)
        return str(result)

    def setup(self):
        self.d = {'name': 'vm1', 
           'cloud': 'india', 
           'update': '2015-06-18 22:11:48 UTC', 
           'user': 'gregor', 
           'extra': {'created': '2015-05-21T20:37:10Z', 'metadata': {'base_image_ref': '398746398798372493287', 'description': None, 
                                  'image_location': 'snapshot', 
                                  'image_state': 'available', 
                                  'image_type': 'snapshot', 
                                  'instance_type_ephemeral_gb': '0', 
                                  'instance_type_flavorid': '3', 
                                  'instance_type_id': '1', 
                                  'instance_type_memory_mb': '4096', 
                                  'instance_type_name': 'm1.medium', 
                                  'instance_type_root_gb': '40', 
                                  'instance_type_rxtx_factor': '1.0', 
                                  'instance_type_swap': '0', 
                                  'instance_type_vcpus': '2', 
                                  'instance_uuid': '386473678463876387', 
                                  'kernel_id': None, 
                                  'network_allocated': 'True', 
                                  'owner_id': '36487264932876984723649', 
                                  'ramdisk_id': None, 
                                  'user_id': '762387463827463278649837'}, 
                     'minDisk': 40, 
                     'minRam': 0, 
                     'progress': 100, 
                     'serverId': 'yiuksajhlkjahl', 
                     'status': 'ACTIVE', 
                     'updated': '2015-05-27T02:11:48Z'}, 
           'id': '39276498376478936247832687', 
           'name': 'VM with Cloudmesh Configured Completely'}
        self.vm = {'extra': {'access_ip': '', 'availability_zone': 'nova', 
                     'config_drive': '', 
                     'created': '2015-06-19T00:06:58Z', 
                     'disk_config': 'MANUAL', 
                     'flavorId': '1', 
                     'hostId': '', 
                     'imageId': 'abcd', 
                     'key_name': None, 
                     'metadata': {}, 'password': '********', 
                     'tenantId': '1234', 
                     'updated': '2015-06-19T00:06:58Z', 
                     'uri': 'http://i5r.idp.iu.futuregrid.org/v2/1234/servers/abcd'}, 
           'id': '67f6bsf67a6b', 
           'image': None, 
           'name': 'vm2', 
           'private_ips': [], 'public_ips': [], 'size': None, 
           'state': 3}
        self.d = FlatDict(self.vm)
        return

    def tearDown(self):
        pass

    def test_000(self):
        result = self.run('cm refresh off')
        print

    def test_001(self):
        HEADING('check the model')
        self.cm.clean()
        d = self.d
        banner('VM Data', c='-')
        pprint(d.__dict__)
        assert d['extra__imageId'] == 'abcd'
        banner('Add VM', c='-')
        name = 'vm1'
        uuid = d.id
        vm = VM_OPENSTACK(name=name, user='test', category=self.data.cloud, **d)
        print(vm)
        banner('VM added', c='-')
        self.cm.add(vm)
        banner('Add VM', c='-')
        name = 'vm2'
        uuid = d.id
        vm = VM_OPENSTACK(name=name, user='test', category=self.data.cloud, **d)
        print(vm)
        banner('VM added', c='-')
        self.cm.add(vm)
        banner('Get VM from Database', c='-')
        vms = self.cm.find(kind='vm', name=name, output='dict')
        pprint(vms)
        assert len(vms) == 1
        assert vms[0]['name'] == name

    def test_002(self):
        HEADING('VM DB test')
        self.cm.clean()
        print('ADD TO OS ')
        d = {'user': 'test', 
           'category': self.data.cloud}
        for index in range(1, 6):
            name = 'vm_' + str(index).zfill(3)
            banner(name)
            print('ADD', name)
            try:
                d['name'] = name
                d['uuid'] = 'uuid_' + str(index)
                vm = VM_OPENSTACK(**d)
                pprint(vm.__dict__)
            except Exception as e:
                Console.error('issue adding vm', traceflag=True)

            self.cm.add(vm)
            print('VM added. ok')

        print('ADD TO LIBCLOUD ')
        for index in range(6, 11):
            name = 'vm_' + str(index).zfill(3)
            banner(name)
            print('ADD', name)
            d['name'] = name
            d['uuid'] = 'uuid_' + str(index)
            vm = VM_LIBCLOUD(**d)
            print('VM', vm.__dict__)
            self.cm.add(vm)

        self.cm.save()
        result = self.run('cm refresh off')
        print(result)
        vms = self.cm.find(kind='vm', scope='all', output='dict')
        pprint(vms)
        print(len(vms))
        assert len(vms) == 10

    def test_003(self):
        HEADING('find vm tables')
        print('---------')
        all_tables = self.cm.tables
        for t in all_tables:
            print(t.__tablename__, t.__kind__)

        print(all_tables)
        assert 'DEFAULT' in str(all_tables)

    def test_004(self):
        HEADING('find vm tables')
        print('-------------')
        vm = self.cm.find(kind='vm', name='vm_001', scope='first')
        pprint(vm)
        assert vm.name == 'vm_001'
        print('-------------')
        vm = self.cm.find(kind='vm', name='vm_006', scope='first')
        pprint(vm)
        assert vm.name == 'vm_006'
        print('-------------')
        vms = self.cm.find(kind='vm', scope='all')
        pprint(vms)
        print(len(vms))
        assert len(vms) == 10