# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_basic/test_shell.py
# Compiled at: 2017-04-23 10:30:41
__doc__ = ' run with\n\npython setup.py install; nosetests -v --nocapture tests/cm_basic/test_shell.py:Test_shell.test_001\n\nnosetests -v --nocapture tests/cm_basic/test_shell.py\n\nor\n\nnosetests -v tests/cm_basic/test_shell.py\n\n'
from __future__ import print_function
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.util import HEADING

def run(command):
    parameter = command.split(' ')
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return str(result)


class Test_shell(object):
    """

    """

    def setup(self):
        pass

    def test_001(self):
        HEADING('check if we can run help:return: ')
        r = run('cm help')
        print(r)
        assert 'Documented commands' in r
        assert 'banner' in r
        assert 'help' in r
        assert 'EOF' in r
        assert 'q' in r
        assert 'quit' in r