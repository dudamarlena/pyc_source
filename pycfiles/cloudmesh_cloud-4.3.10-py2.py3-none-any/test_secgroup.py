# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_cloud/test_secgroup.py
# Compiled at: 2017-04-23 10:30:41
__doc__ = ' run with\n\npython setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_secgroup.py:Test_secgroup.test_001\n\nnosetests -v --nocapture tests/test_secgroup.py\n\nor\n\nnosetests -v tests/test_secgroup.py\n\n'
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from pprint import pprint
from cloudmesh_client.shell.console import Console
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase

class Test_secgroup:
    data = dotdict({'dgroup': ('{}-default').format(Default.user), 
       'cloud': Default.cloud, 
       'group': ('cm-{}-test').format(Default.user), 
       'wrong_cloud': 'no_cloud', 
       'rules': {'rule_http': '80 80 tcp  0.0.0.0/0', 
                 'rule_https': '443 443 tcp  0.0.0.0/0', 
                 'rule_ssh': '22 22 tcp  0.0.0.0/0'}, 
       'image': Default.get_image(category=Default.cloud), 
       'flavor': Default.get_flavor(category=Default.cloud), 
       'vm': ('{}_testsecgroup').format(Default.user)})
    for rule in data.rules:
        data[rule] = data.rules[rule]

    data.tenant = ConfigDict('cloudmesh.yaml')['cloudmesh.clouds'][data.cloud]['credentials']['OS_TENANT_NAME']

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c='-')
        print command
        parameter = command.split(' ')
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print result
        return str(result)

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        HEADING('cm secgroup add ...')
        for rule in self.data.rules:
            command = ('cm secgroup add  {} {} {}').format(self.data.group, rule, self.data['rules'][rule])
            result = self.run(command)

        command = 'cm secgroup list'
        result = self.run(command)
        for rule in self.data.rules:
            assert rule in result

    def test_002(self):
        HEADING('cm secgroup delete ...')
        command = ('cm secgroup delete {group}').format(**self.data)
        result = self.run(command)
        result = self.run('cm secgroup list')
        assert self.data.group not in result

    def test_003(self):
        HEADING('secgroup api')
        data = dotdict({'cloud': 'cm', 
           'groupname': 'gvonlasz-default'})
        provider = CloudProvider(data.cloud).provider
        groups = None
        rules = provider.list_secgroup(data.cloud)
        return

    def test_004(self):
        """
        A through test of deleting/updating secgroups.
        It creates in the db a testing group with 3 rules;
        Uploading the secgroup to cloud;
        booting a vm with this newly created group;
        deleting the secgroup (should fail as being used);
        updating rules for the secgroup
        (should succeed - updating rules, but not creating duplicated group);
        cleaning up...
            delete the testing vm
            deleting the testing secgroup
        """
        HEADING('creating testing group in db and populate with rules')
        for rule in self.data.rules:
            command = ('cm secgroup add  {} {} {}').format(self.data.group, rule, self.data['rules'][rule])
            result = self.run(command)

        HEADING('uploading the newly created secgroup to default cloud')
        command = ('cm secgroup upload {} --cloud={}').format(self.data.group, self.data.cloud)
        result = self.run(command)
        HEADING('listing secgroup in default cloud')
        command = ('cm secgroup list --cloud={}').format(self.data.cloud)
        result = self.run(command)
        assert '80' in result and self.data.group in result
        HEADING('booting a vm with the test secgroup')
        command = 'cm vm boot --name={vm} --cloud={cloud} --image={image}' + ' --flavor={flavor} --secgroup={group}'
        result = self.run(command)
        assert 'OK.' in result
        HEADING('cm secgroup delete ... Deleting a secgroup that is being used')
        command = ('cm secgroup delete {} --cloud={}').format(self.data.group, self.data.cloud)
        result = self.run(command)
        assert 'ERROR' in result and 'in use' in result
        HEADING('adding new rule to the test secgroup (change in db)')
        command = ('cm secgroup add {} ssh 8765 8765 tcp 0.0.0.0/0').format(self.data.group)
        result = self.run(command)
        HEADING('updating the teseting secgroup in the default cloud (upload to cloud)')
        command = ('cm secgroup upload {} --cloud={}').format(self.data.group, self.data.cloud)
        result = self.run(command)
        HEADING(('cm secgroup list --cloud={}').format(self.data.cloud))
        command = ('cm secgroup list --cloud={}').format(self.data.cloud)
        result = self.run(command)
        assert '8765' in result
        HEADING('Cleaning up......')
        HEADING('deleting the test vm and the test secgroup')
        command = ('cm vm delete {}').format(self.data.vm)
        result = self.run(command)
        command = ('cm secgroup delete {} --cloud={}').format(self.data.group, self.data.cloud)
        result = self.run(command)
        command = ('cm secgroup list --cloud={}').format(self.data.cloud)
        result = self.run(command)
        assert self.data.group not in result