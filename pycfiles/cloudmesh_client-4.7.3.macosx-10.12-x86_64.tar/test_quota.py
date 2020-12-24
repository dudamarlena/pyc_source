# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_cloud/test_quota.py
# Compiled at: 2017-04-23 10:30:41
""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_quota.py:Test_quota.test_001

nosetests -v --nocapture tests/test_quota.py

or

nosetests -v tests/test_quota.py

"""
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default

class Test_quota:
    """
        This class tests the QuotaCommand
    """
    data = dotdict({'cloud': Default.cloud, 
       'format': 'csv', 
       'wrong_cloud': 'no_cloud'})

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
        HEADING('test quota list')
        result = self.run('cm quota list')
        assert 'Quota' in result

    def test_002(self):
        HEADING('test quota list with csv output')
        result = self.run('cm quota list --cloud={cloud} --format={format}')
        assert 'ram' in result

    def test_003(self):
        HEADING('test quota class where cloud doesnt exist')
        result = self.run('cm quota list --cloud={wrong_cloud}')
        assert 'is not defined in the yaml file' in result