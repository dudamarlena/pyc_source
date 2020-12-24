# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_cloud/test_image.py
# Compiled at: 2017-04-23 10:30:41
__doc__ = ' run with\n\npython setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_image.py:Test_image.test_001\n\nnosetests -v --nocapture tests/test_image.py\n\nor\n\nnosetests -v tests/test_image.py\n\n'
from __future__ import print_function
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default
from cloudmesh_client.cloud.image import Image
from pprint import pprint

class Test_image:
    """
        This class tests the ImageCommand
    """
    data = dotdict({'cloud': Default.cloud, 
       'wrong_cloud': 'no_cloud', 
       'format': 'json'})

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c='-')
        print(command)
        parameter = command.split(' ')
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print(result)
        return result

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        HEADING('test image refresh')
        result = self.run('cm image refresh --cloud={cloud}')
        assert 'ok.' in result

    def test_002(self):
        HEADING('test image refresh fail')
        result = self.run('cm image refresh --cloud={wrong_cloud}')
        assert 'failed' in result

    def test_003(self):
        HEADING('test image list')
        result = self.run('cm image list --cloud={cloud}')
        assert 'description' in result

    def test_004(self):
        HEADING('test image list fail')
        result = self.run('cm image list --cloud={wrong_cloud}')
        assert 'failed' in result

    def test_005(self):
        HEADING('test image list ID')
        result = self.run('cm image list --cloud={cloud} --format={format}')
        assert 'Ubuntu' in result

    def test_006(self):
        HEADING('test image list ID fail')
        result = self.run('cm image list i --cloud={wrong_cloud}')
        assert 'failed' in result

    def test_007(self):
        HEADING('test image username guess')
        result = Image.guess_username('Ubuntu-image')
        print(result)
        assert result == 'ubuntu'
        result = Image.guess_username('wily-image')
        print(result)
        assert result == 'ubuntu'
        result = Image.guess_username('fedora-image')
        print(result)
        assert result == 'root'
        result = Image.guess_username('image', description='image with wily')
        print(result)
        assert result == 'ubuntu'

    def test_008(self):
        HEADING('test image get username')
        assert Default.cloud not in ('cm', 'chameleon') and True
        result = self.run('cm image list --refresh')
        Image.set_username(name='CC-Ubuntu14.04', cloud=Default.cloud, username='undefined')
        result = Image.get_username('CC-Ubuntu14.04', Default.cloud)
        print('Username:', result)
        assert 'undefined' in result
        Image.set_username(name='CC-Ubuntu14.04', cloud=Default.cloud, username=None)
        result = Image.get_username('CC-Ubuntu14.04', Default.cloud, guess=True)
        print('Username:', result)
        assert 'cc' in result
        return

    def test_009(self):
        HEADING('test image get username')
        assert Default.cloud not in ('cm', 'chameleon') and True
        login = Image.get_username('CC-Ubuntu14.04', Default.cloud, guess=True)
        print('LOGIN', login)
        Image.set_username(name='CC-Ubuntu14.04', cloud=Default.cloud, username=login)
        result = Image.get_username('CC-Ubuntu14.04', Default.cloud)
        print(result)