# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/glespy/tools/test/test_tools.py
# Compiled at: 2013-09-14 10:33:36
__author__ = 'yarnaid'
import unittest, os, glespy.tools.tools as tools
NT_FLG = 'nt' == os.name

@unittest.skipIf(NT_FLG, 'GlespBinariesTest now is not for nt')
class GlespBinariesTest(unittest.TestCase):
    """
    Checking existence of glesp binaries
    """

    def test_binaries(self):
        for prog in tools.binaries.values():
            self.assertTrue(os.path.exists(prog))


class FunctionsTests(unittest.TestCase):

    @unittest.skipIf(NT_FLG, 'GlespBinariesTest now is not for nt')
    def test_run_cmd_mkdir(self):
        args = ['mkdir', '-p', 'my_dir']
        tools.run_cmd(args=args)
        self.assertTrue(os.path.exists('my_dir'))
        os.rmdir('my_dir')

    def test_run_cmd_stdout(self):
        """
        test stdout param of run_cmd
        """
        pass

    def test_run_cmd_stderr(self):
        """
        test stderr param of run_cmd
        """
        pass

    def test_get_out_name_with_name(self):
        """
        test for given 'name' param
        """
        n = 'my_name.tmp'
        nn = tools.get_out_name(n, delete=True)
        self.assertEqual(n, nn)

    def test_get_out_name_without_name(self):
        """
        should get name for tmp file and the file
        """
        n = tools.get_out_name(delete=False)
        self.assertTrue(os.path.exists(n))
        os.remove(n)

    def test_get_out_name_without_name_with_suffix(self):
        """
        test suffix in tmp file name
        """
        n = tools.get_out_name(suffix='suffix', delete=True)
        suffix = os.path.split(n)[(-1)].split('_')
        self.assertTrue('suffix' in suffix)


if __name__ == '__main__':
    unittest.main()