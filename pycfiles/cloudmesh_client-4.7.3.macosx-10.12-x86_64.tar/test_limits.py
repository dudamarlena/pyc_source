# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_cloud/test_limits.py
# Compiled at: 2017-04-23 10:30:41
""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_limits.py:Test_limits.test_001

nosetests -v --nocapture tests/test_limits.py

or

nosetests -v tests/test_limits.py

"""
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default

class Test_limits:
    """
        This class tests the LimitsCommand
    """
    data = dotdict({'cloud': Default.cloud, 
       'wrong_cloud': 'no_cloud', 
       'tenant': 'TBD', 
       'format': 'table'})
    config = ConfigDict('cloudmesh.yaml')
    credentials = config['cloudmesh']['clouds'][data.cloud]['credentials']
    data.tenant = credentials.get('OS_TENANT_NAME') or credentials.get('OS_TENANT_ID')

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c='-')
        print command
        parameter = command.split(' ')
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print result
        return result

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        HEADING('test limits list')
        result = self.run('cm limits list --cloud={cloud}')
        assert 'Name' in result

    def test_002(self):
        HEADING('test limits list with csv output')
        result = self.run('cm limits list --format={format}').split('\n')
        assert 'maxTotalFloatingIps' in str(result)

    def test_003(self):
        HEADING('test limits class where cloud doesnt exist')
        result = self.run('cm limits list --cloud={wrong_cloud}')
        assert 'ERROR' in str(result)