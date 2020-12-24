# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_basic/test_var.py
# Compiled at: 2017-04-23 10:30:41
__doc__ = ' run with\n\npython setup.py install; nosetests -v --nocapture tests/cm_basic/test_var.py\npython setup.py install; nosetests -v --nocapture tests/cm_basic/test_var.py:Test_var.test_001\n\nnosetests -v --nocapture tests/cm_basic/test_var.py\n\nor\n\nnosetests -v tests/cm_basic/test_var.py\n\n'
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.var import Var

def run(command):
    print command
    parameter = command.split(' ')
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    print result
    return result


class Test_var(object):
    """

    """

    def setup(self):
        pass

    def test_001(self):
        HEADING(' delete defaults')
        Var.clear()
        print Var.list()
        assert Var.list() is None
        return

    def _check(self, content):
        result = Var.list()
        print result
        assert content in str(result)

    def test_002(self):
        HEADING('set default variable')
        name = 'myvar'
        value = 'myvalue'
        Var.set(name, value)
        print Var.list()
        self._check(value)

    def test_003(self):
        HEADING('delete default variable')
        Var.clear()
        name = 'deleteme'
        value = 'myvalue'
        Var.set(name, value)
        print Var.list()
        Var.delete(name)
        print Var.list()
        self._check('None')

    def test_004(self):
        HEADING('assign a variable')
        command = 'cm var myvar=myvalue'
        result = run(command)
        result = run('cm var list')
        assert 'myvalue' in result

    def test_005(self):
        HEADING('print a variable')
        command = 'cm banner $myvar'
        result = run(command)
        assert 'myvalue' in result
        assert 'myvar' in result

    def test_999(self):
        HEADING('clear the defaults')
        Var.clear()
        result = Var.list()
        print result
        assert result is None
        return