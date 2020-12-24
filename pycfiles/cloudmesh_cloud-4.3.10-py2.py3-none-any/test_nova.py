# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_cloud/test_nova.py
# Compiled at: 2017-04-23 10:30:41
__doc__ = ' run with\n\npython setup.py install; nosetests -v --nocapture tests/cm_cloud/test_nova.py:Test_nova.test_001\n\nnosetests -v --nocapture tests/test_nova.py\n\nor\n\nnosetests -v tests/test_nova.py\n\n'
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default

class Test_nova:
    """tests nova command"""
    data = dotdict({'cloud': Default.cloud, 
       'group': 'mygroup', 
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

    def test_000(self):
        HEADING('set the default group')
        result = self.run('cm default group={group}')

    def test_001(self):
        HEADING('cm nova set <cloud>')
        result = self.run('cm nova set {cloud}')
        assert ('{cloud} is set').format(**self.data) in result

    def test_002(self):
        HEADING('cm nova info <cloud>')
        result = self.run('cm nova info {cloud}')
        assert 'OK.' in result

    def test_003(self):
        HEADING('cm nova list')
        result = self.run('cm nova list')
        assert '+' in result

    def test_004(self):
        HEADING('cm nova image-list')
        result = self.run('cm nova image-list')
        assert 'ACTIVE' in result