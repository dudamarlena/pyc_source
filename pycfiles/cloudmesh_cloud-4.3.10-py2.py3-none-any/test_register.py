# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_cloud/test_register.py
# Compiled at: 2017-04-23 10:30:41
__doc__ = ' run with\n\npython setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_register.py:Test_register.test_001\n\nnosetests -v --nocapture tests/test_register.py\n\nor\n\nnosetests -v tests/test_register.py\n'
from cloudmesh_client.common.util import banner
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.default import Default

class Test_register:
    """
    # tests
    # for india only
    """
    data = dotdict({'cloud': 'kilo', 
       'group': 'test', 
       'vm': 'testvm', 
       'flavor': 'TBD', 
       'image': 'TBD', 
       'wrong_cloud': 'no_cloud', 
       'cert': '~/.cloudmesh/clouds/india/{cloud}/cacert.pem', 
       'yaml': 'cloudmesh1.yaml'})
    data.image = Default.get_image()
    data.flavor = Default.get_flavor()

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
        HEADING(('cm register remote {cloud}').format(**self.data))
        result = self.run('cm register remote {cloud}')
        print result
        assert ('{cloud}').format(**self.data) in result
        assert 'OS_AUTH_URL' in result
        assert 'https://kilo.futuresystems.org:5000/v3' in result

    def test_002(self):
        HEADING('testing cm register random1')
        result = self.run('cm register remote doesnotexist')
        assert 'ERROR: executing' in result

    def test_003(self):
        HEADING('testing cm register list')
        result = self.run('cm register list')
        assert ('{cloud}').format(**self.data) in result

    def test_004(self):
        HEADING('testing cm register info')
        result = self.run('cm register info')
        assert 'exists' in result

    def test_005(self):
        HEADING('testing cm register cat')
        result = self.run('cm register cat')
        assert 'version:' in result

    def test_006(self):
        HEADING(('testing cm register cat --yaml={yaml}').format(**self.data))
        result = self.run('cm register cat --yaml={yaml}')
        assert 'ERROR: executing command' in result

    def test_007(self):
        HEADING('testing cm register edit --yaml=cloudmesh_doesnotexist.yaml')
        result = self.run('cm register edit --yaml=cloudmesh_doesnotexit.yaml')
        assert 'ERROR: executing command' in result

    def test_008(self):
        HEADING('testing cm register list ssh')
        result = self.run('cm register list ssh')
        assert '| host' in result

    def test_009(self):
        HEADING('testing cm register remote')
        result = self.run('cm register remote')
        assert 'Reading rc file from' in result

    def test_010(self):
        HEADING(('cm register json {cloud}').format(**self.data))
        result = self.run('cm register json {cloud}')
        assert 'openstack' in result

    def test_011(self):
        HEADING('testing cm register json hadoop')
        result = self.run('cm register json hadoop')
        assert 'Cloud hadoop is not described in cloudmesh.yaml' in result