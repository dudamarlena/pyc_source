# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_clouds/test_kilo.py
# Compiled at: 2017-04-23 10:30:41
""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_clouds/test_chameleon.py:Test_chameleon.test_001

nosetests -v --nocapture tests/test_image.py

or

nosetests -v tests/test_chameleon.py

"""
import os
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner

class Test_chameleon:
    """
        This class tests the ImageCommand
    """
    data = dotdict({'cloud': 'kilo'})

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
        """
        test image refresh
        :return:
        """
        HEADING()
        result = self.run('make db')
        assert 'ok.' in result

    def test_002(self):
        """
        test image refresh
        :return:
        """
        HEADING()
        result = self.run('cm default cloud={cloud}')
        assert 'ok.' in result

    def test_003(self):
        """
        test image refresh
        :return:
        """
        HEADING()
        os.system('py.test tests/cm_cloud')
        assert True