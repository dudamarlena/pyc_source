# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_cloud/test_scripts.py
# Compiled at: 2017-04-23 10:30:41
__doc__ = ' run with\n\npython setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_scripts.py\n\nnosetests -v --nocapture tests/test_scripts.py\n\nor\n\nnosetests -v tests/test_scripts.py\n\n'
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default

class Test_script:
    """tests script command"""
    data = dotdict({'cloud': Default.cloud, 
       'group': 'mygroup'})

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
        self.scripts = [
         ('bash.cm', 'README.rst'),
         ('comment.cm', '/* test'),
         ('var.cm', 'username'),
         ('py.cm', '2'),
         ('terminal.cm', ''),
         ('key.cm', ''),
         ('reservedemo.cm', 'cloudnauts')]

    def tearDown(self):
        pass

    def test_001(self):
        HEADING('cm script set india')
        for self.data['script'], self.data['check'] in self.scripts:
            result = self.run('cm scripts/{script}')
            assert self.data['check'] in result