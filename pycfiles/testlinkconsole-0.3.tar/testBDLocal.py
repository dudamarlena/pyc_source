# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbrun/Projets/Perso/projets/dev/testlinkconsole/testlinkconsole/tests/plugins/testBDLocal.py
# Compiled at: 2014-07-08 03:37:19
import unittest, mock
from plugins.bdlocal import BDLocalPlugin

class TestBDLocalPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = BDLocalPlugin()

    def test_activate(self):
        self.assertEquals(self.plugin.activate(), 'BDLocal plugin actif')

    def test_deactivate(self):
        self.assertEquals(self.plugin.deactivate(), 'BDLocal plugin inactif')

    @mock.patch('__builtin__.print')
    def test_run(self, mock_print):
        mock_print.assert_has_calls([])
        self.assertEquals(self.plugin.run('profile', 'script'), None)
        return

    @unittest.skip('TODO')
    def test_listProjects(self):
        pass

    @unittest.skip('TODO')
    def test_listTestPlans(self):
        pass

    @unittest.skip('TODO')
    def test_listTestCases(self):
        pass

    @unittest.skip('TODO')
    def test_getInfoProject(self):
        pass

    @unittest.skip('TODO')
    def test_getInfoTestPlan(self):
        pass

    @unittest.skip('TODO')
    def test_getInfoTestCase(self):
        pass

    @unittest.skip('TODO')
    def test_runTestPlan(self):
        pass

    @unittest.skip('TODO')
    def test_runTestCase(self):
        pass


if __name__ == '__main__':
    unittest.main()