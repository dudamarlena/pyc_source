# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_conf.py
# Compiled at: 2014-10-22 16:00:16
__author__ = 'Nicolas Baer <nicolas.baer@uzh.ch>'
import copy, ConfigParser, os, shutil, tempfile, unittest, sys, nose.tools
from voluptuous import Invalid, MultipleInvalid
from elasticluster.conf import ConfigReader, ConfigValidator, Configurator
from elasticluster.cluster import Node
from elasticluster.exceptions import ClusterNotFound
from elasticluster.providers.ansible_provider import AnsibleSetupProvider
from elasticluster.providers.ec2_boto import BotoCloudProvider

def minimal_configuration(valid_path):
    cfg = ConfigParser.ConfigParser()
    cfg.add_section('cloud/boto1')
    cfg.set('cloud/boto1', 'provider', 'ec2_boto')
    cfg.set('cloud/boto1', 'ec2_url', 'https://ec2.us-east-1.amazonaws.com')
    cfg.set('cloud/boto1', 'ec2_access_key', 'XXXXXX')
    cfg.set('cloud/boto1', 'ec2_secret_key', 'XXXXXX')
    cfg.set('cloud/boto1', 'ec2_region', 'us-east-1')
    cfg.add_section('cloud/google1')
    cfg.set('cloud/google1', 'provider', 'google')
    cfg.set('cloud/google1', 'gce_project_id', 'gc3-uzh')
    cfg.set('cloud/google1', 'gce_client_id', 'XXXXXX')
    cfg.set('cloud/google1', 'gce_client_secret', 'XXXXXX')
    cfg.add_section('cluster/c1')
    cfg.set('cluster/c1', 'cloud', 'boto1')
    cfg.set('cluster/c1', 'login', 'log1')
    cfg.set('cluster/c1', 'setup_provider', 'sp1')
    cfg.set('cluster/c1', 'login', 'log1')
    cfg.set('cluster/c1', 'image_id', 'i-12345')
    cfg.set('cluster/c1', 'flavor', 'm1.tiny')
    cfg.set('cluster/c1', 'misc_nodes', '10')
    cfg.set('cluster/c1', 'security_group', 'default')
    cfg.add_section('cluster/c2')
    cfg.set('cluster/c2', 'cloud', 'google1')
    cfg.set('cluster/c2', 'login', 'log1')
    cfg.set('cluster/c2', 'setup_provider', 'sp1')
    cfg.set('cluster/c2', 'login', 'log1')
    cfg.set('cluster/c2', 'image_id', 'i-12345')
    cfg.set('cluster/c2', 'flavor', 'm1.tiny')
    cfg.set('cluster/c2', 'misc_nodes', '10')
    cfg.set('cluster/c2', 'security_group', 'default')
    cfg.add_section('setup/sp1')
    cfg.set('setup/sp1', 'provider', 'ansible')
    cfg.add_section('login/log1')
    cfg.set('login/log1', 'image_user', 'ubuntu')
    cfg.set('login/log1', 'image_user_sudo', 'root')
    cfg.set('login/log1', 'image_sudo', 'False')
    cfg.set('login/log1', 'user_key_name', 'keyname')
    cfg.set('login/log1', 'user_key_private', valid_path)
    cfg.set('login/log1', 'user_key_public', valid_path)
    return cfg


class Configuration(object):

    def get_config(self, path):
        config = {'mycluster': {'setup': {'provider': 'ansible', 
                                   'playbook_path': '%(ansible_pb_dir)s/site.yml', 
                                   'frontend_groups': 'slurm_master', 
                                   'compute_groups': 'slurm_clients'}, 
                         'cloud': {'provider': 'ec2_boto', 
                                   'ec2_url': 'http://cloud.gc3.uzh.ch:8773/services/Cloud', 
                                   'ec2_access_key': '***fill in your data here***', 
                                   'ec2_secret_key': '***fill in your data here***', 
                                   'ec2_region': 'nova'}, 
                         'login': {'image_user': 'gc3-user', 
                                   'image_user_sudo': 'root', 
                                   'image_sudo': 'True', 
                                   'user_key_name': '***name of SSH keypair on Hobbes***', 
                                   'user_key_private': path, 
                                   'user_key_public': path}, 
                         'cluster': {'cloud': 'hobbes', 
                                     'login': 'gc3-user', 
                                     'setup_provider': 'my-slurm-cluster', 
                                     'frontend_nodes': '1', 
                                     'compute_nodes': '2'}, 
                         'nodes': {'frontend': {'security_group': 'default', 
                                                'flavor': 'm1.tiny', 
                                                'image_id': 'ami-00000048'}, 
                                   'compute': {'security_group': 'default', 
                                               'flavor': 'm1.large', 
                                               'image_id': 'ami-00000048'}}}}
        return config


class TestConfigurator(unittest.TestCase):

    def setUp(self):
        file, path = tempfile.mkstemp()
        self.path = path
        self.config = Configuration().get_config(self.path)

    def tearDown(self):
        os.unlink(self.path)

    def test_create_cloud_provider(self):
        configurator = Configurator(self.config)
        provider = configurator.create_cloud_provider('mycluster')
        url = self.config['mycluster']['cloud']['ec2_url']
        self.assertEqual(provider._url, url)
        access_key = self.config['mycluster']['cloud']['ec2_access_key']
        self.assertEqual(provider._access_key, access_key)
        secret_key = self.config['mycluster']['cloud']['ec2_secret_key']
        self.assertEqual(provider._secret_key, secret_key)
        region = self.config['mycluster']['cloud']['ec2_region']
        self.assertEqual(provider._region_name, region)

    def test_create_cluster(self):
        configurator = Configurator(self.config)
        cluster = configurator.create_cluster('mycluster')
        self.assertEqual(cluster.name, 'mycluster')
        self.assertTrue(type(cluster._cloud_provider) is BotoCloudProvider)
        self.assertTrue(type(cluster._setup_provider) is AnsibleSetupProvider)
        self.assertTrue('compute' in cluster.nodes)
        self.assertTrue('frontend' in cluster.nodes)
        self.assertTrue(len(cluster.nodes['compute']) == 2)
        self.assertTrue(len(cluster.nodes['frontend']) == 1)

    def test_load_cluster(self):
        storage_path = tempfile.mkdtemp()
        configurator = Configurator(self.config, storage_path=storage_path)
        self.assertRaises(ClusterNotFound, configurator.load_cluster, 'mycluster')
        shutil.rmtree(storage_path)

    def test_create_setup_provider(self):
        configurator = Configurator(self.config)
        provider = configurator.create_setup_provider('mycluster')
        self.assertTrue(type(provider) is AnsibleSetupProvider)
        conf = self.config['mycluster']['setup']
        groups = dict((k[:-7], v.split(',')) for k, v in conf.items() if k.endswith('_groups'))
        self.assertEqual(groups, provider.groups)
        playbook_path = os.path.join(sys.prefix, 'share/elasticluster/providers/ansible-playbooks', 'site.yml')
        self.assertEqual(playbook_path, provider._playbook_path)
        storage_path = configurator.general_conf['storage']
        self.assertEqual(provider._storage_path, storage_path)
        usr_sudo = self.config['mycluster']['login']['image_user_sudo']
        self.assertEqual(provider._sudo_user, usr_sudo)
        sudo = self.config['mycluster']['login']['image_sudo']
        self.assertEqual(provider._sudo, sudo)


class TestConfigValidator(unittest.TestCase):

    def setUp(self):
        file, path = tempfile.mkstemp()
        self.path = path
        self.config = Configuration().get_config(self.path)

    def tearDown(self):
        os.unlink(self.path)

    def test_gce_config(self):
        self.config['mycluster']['cloud'] = {'provider': 'google', 
           'gce_client_id': '***fill in your data here***', 
           'gce_client_secret': '***fill in your data here***', 
           'gce_project_id': 'test-id'}
        validator = ConfigValidator(self.config)
        validator.validate()

    def test_valid_config(self):
        """
        Valid configuration
        """
        validator = ConfigValidator(self.config)
        validator.validate()

    def test_invalid_config(self):
        """
        Invalid configuration
        """
        config = copy.deepcopy(self.config)
        config['mycluster']['login']['user_key_public'] = '/tmp/elastic-test'
        validator = ConfigValidator(config)
        self.assertRaises(Invalid, validator.validate)
        config = copy.deepcopy(config)
        config['mycluster']['setup']['ec2_host'] = 'www.elasticluster'
        validator = ConfigValidator(config)
        self.assertRaises(Invalid, validator.validate)
        optional = [
         'frontend_groups', 'compute_groups', 'frontend_nodes',
         'compute_nodes', 'security_group', 'flavor', 'image_id',
         'playbook_path', 'frontend', 'compute']
        config = copy.deepcopy(config)
        for cluster, sections in config.iteritems():
            for section, properties in sections.iteritems():
                for property, value in properties.iteritems():
                    if property not in optional:
                        config_tmp = copy.deepcopy(config)
                        del config_tmp[cluster][section][property]
                        validator = ConfigValidator(config_tmp)
                        self.assertRaises(Invalid, validator.validate)

        mandatory = [
         'flavor', 'image_id', 'security_group']
        config = copy.deepcopy(config)
        for node, properties in config['mycluster']['nodes'].iteritems():
            for property in properties.iterkeys():
                if property in mandatory:
                    config_tmp = copy.deepcopy(config)
                    del config_tmp['mycluster']['nodes'][node][property]
                    validator = ConfigValidator(config_tmp)
                    self.assertRaises(Invalid, validator.validate)


class TestConfigReader(unittest.TestCase):

    def setUp(self):
        file, path = tempfile.mkstemp()
        self.path = path
        self.cfgfile = path

    def tearDown(self):
        os.unlink(self.cfgfile)

    def _check_read_config(self, config):
        with open(self.cfgfile, 'wb') as (fd):
            fd.write(config)
        return Configurator.fromConfig(self.cfgfile)

    def _check_read_config_object(self, cfgobj):
        with open(self.cfgfile, 'wb') as (fd):
            cfgobj.write(fd)
        ret = Configurator.fromConfig(self.cfgfile)
        return ret

    def test_read_valid_config(self):
        """
        Read valid config into dictionary
        """
        config = '\n[cloud/hobbes]\nprovider=ec2_boto\nec2_url=http://hobbes.gc3.uzh.ch:8773/services/Cloud\nec2_access_key=****REPLACE WITH YOUR ACCESS ID****\nec2_secret_key=****REPLACE WITH YOUR SECRET KEY****\nec2_region=nova\n\n[cloud/amazon-us-east-1]\nprovider=ec2_boto\nec2_url=https://ec2.us-east-1.amazonaws.com\nec2_access_key=****REPLACE WITH YOUR ACCESS ID****\nec2_secret_key=****REPLACE WITH YOUR SECRET KEY****\nec2_region=us-east-1\n\n[login/ubuntu]\nimage_user=ubuntu\nimage_user_sudo=root\nimage_sudo=True\nuser_key_name=elasticluster\nuser_key_private=' + self.path + '\nuser_key_public=' + self.path + '\n\n[login/gc3-user]\nimage_user=gc3-user\nimage_user_sudo=root\nimage_sudo=True\nuser_key_name=elasticluster\nuser_key_private=' + self.path + '\nuser_key_public=' + self.path + '\n\n[setup/ansible-slurm]\nprovider=ansible\nfrontend_groups=slurm_master\ncompute_groups=slurm_clients\n\n[setup/ansible-gridengine]\nprovider=ansible\nfrontend_groups=gridengine_master\ncompute_groups=gridengine_clients\n\n[setup/ansible-pbs]\nprovider=ansible\nfrontend_groups=pbs_master,maui_master\ncompute_groups=pbs_clients\n\n[setup/ansible_matlab]\nprovider=ansible\nfrontend_groups=mdce_master,mdce_worker,ganglia_monitor,ganglia_master\nworker_groups=mdce_worker,ganglia_monitor\n\n[cluster/slurm]\ncloud=hobbes\nlogin=gc3-user\nsetup_provider=ansible-slurm\nsecurity_group=default\nimage_id=ami-00000048\nflavor=m1.small\nfrontend_nodes=1\ncompute_nodes=2\nssh_to=frontend\n\n[cluster/torque]\ncloud=hobbes\nfrontend_nodes=1\ncompute_nodes=2\nssh_to=frontend\nsecurity_group=default\n# CentOS image\nimage_id=ami-0000004f\nflavor=m1.small\nlogin=gc3-user\nsetup_provider=ansible-pbs\n\n[cluster/aws-slurm]\ncloud=amazon-us-east-1\nlogin=ubuntu\nsetup_provider=ansible-slurm\nsecurity_group=default\n# ubuntu image\nimage_id=ami-90a21cf9\nflavor=m1.small\nfrontend_nodes=1\ncompute_nodes=2\n\n[cluster/matlab]\ncloud=hobbes\nlogin=gc3-user\nsetup_provider=ansible_matlab\nsecurity_group=default\nimage_id=ami-00000099\nflavor=m1.medium\nfrontend_nodes=1\nworker_nodes=10\nimage_userdata=\nssh_to=frontend\n\n[cluster/slurm/frontend]\nflavor=bigdisk\n            '
        config = self._check_read_config(config)
        cfg = config.cluster_conf
        self.assertTrue('matlab' in cfg)
        self.assertTrue('aws-slurm' in cfg)
        self.assertTrue('torque' in cfg)
        self.assertTrue('slurm' in cfg)
        self.assertTrue('frontend' in cfg['matlab']['nodes'])
        self.assertTrue('worker' in cfg['matlab']['nodes'])
        self.assertTrue(cfg['matlab']['cluster']['security_group'] == 'default')
        self.assertTrue(cfg['matlab']['login']['image_user'] == 'gc3-user')
        self.assertTrue(cfg['matlab']['setup']['provider'] == 'ansible')
        self.assertTrue(cfg['matlab']['cloud']['ec2_region'] == 'nova')
        self.assertTrue(cfg['slurm']['nodes']['frontend']['flavor'] == 'bigdisk')

    def test_read_missing_section_cluster(self):
        """
        Check if a configuration file with no `cluster` sections will
        raise an error.
        """
        cfg = minimal_configuration(self.path)
        cfg.remove_section('cluster/c1')
        cfg.remove_section('cluster/c2')
        self.assertRaises(Invalid, self._check_read_config_object, cfg)

    def test_read_missing_section_cloud(self):
        """
        Read config with missing section
        """
        cfg = minimal_configuration(self.path)
        cfg.remove_section('cloud/boto1')
        self.assertRaises(Invalid, self._check_read_config_object, cfg)

    def test_read_section_linking(self):
        """
        Read config with wrong section links
        """
        config = '\n[cloud/hobbes]\nprovider=ec2_boto\nec2_url=http://hobbes.gc3.uzh.ch:8773/services/Cloud\nec2_access_key=****REPLACE WITH YOUR ACCESS ID****\nec2_secret_key=****REPLACE WITH YOUR SECRET KEY****\nec2_region=nova\n\n[login/gc3-user]\nimage_user=gc3-user\nimage_user_sudo=root\nimage_sudo=True\nuser_key_name=elasticluster\nuser_key_private=~/.ssh/id_dsa.cloud\nuser_key_public=~/.ssh/id_dsa.cloud.pub\n\n[setup/ansible-slurm]\nprovider=ansible\nfrontend_groups=slurm_master\ncompute_groups=slurm_clients\n\n[cluster/slurm]\ncloud=hobbes-new\nlogin=gc3-user\nsetup_provider=ansible-slurm\nsecurity_group=default\n# Ubuntu image\nimage_id=ami-00000048\nflavor=m1.small\nfrontend_nodes=1\ncompute_nodes=2\nssh_to=frontend\n'
        self.assertRaises(Invalid, self._check_read_config, config)

    def test_missing_options(self):
        cfg = minimal_configuration(self.path)

        @nose.tools.raises(Invalid, MultipleInvalid)
        def missing_option(section, option):
            tmpcfg = minimal_configuration()
            _, cfgfile = tempfile.mkstemp()
            tmpcfg.remove_option(section, option)
            with open(cfgfile, 'w') as (fd):
                tmpcfg.write(fd)
            try:
                config = Configurator.fromConfig(cfgfile)
            finally:
                os.unlink(cfgfile)

        for section in cfg.sections():
            for option, value in cfg.items(section):
                yield (
                 missing_option, section, option)


class TestConfigurationFile(unittest.TestCase):

    def setUp(self):
        file, path = tempfile.mkstemp()
        self.cfgfile = path

    def tearDown(self):
        os.unlink(self.cfgfile)

    def test_valid_minimal_configuration(self):
        cfg = minimal_configuration(self.cfgfile)
        with open(self.cfgfile, 'w') as (fd):
            cfg.write(fd)
        config = Configurator.fromConfig(self.cfgfile)

    def test_parsing_of_multiple_ansible_groups(self):
        """Fix regression causing multiple ansible groups to be incorrectly parsed

        The bug caused this configuration snippet:

        [setup/ansible]
        frontend_groups=slurm_master,ganglia_frontend

        to lead to the following inventory file:

        [slurm_master,ganglia_frontend]
        frontend001 ...
        """
        cfg = minimal_configuration(self.cfgfile)
        cfg.set('setup/sp1', 'misc_groups', 'misc_master,misc_client')
        with open(self.cfgfile, 'w') as (fd):
            cfg.write(fd)
        config = Configurator.fromConfig(self.cfgfile)
        setup = config.create_setup_provider('c1')
        self.assertEqual(setup.groups['misc'], ['misc_master', 'misc_client'])


if __name__ == '__main__':
    import nose
    nose.runmodule()