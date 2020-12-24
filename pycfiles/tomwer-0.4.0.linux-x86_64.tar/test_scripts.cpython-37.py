# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/test/test_scripts.py
# Compiled at: 2020-01-24 07:42:12
# Size of source mod 2**32: 4197 bytes
from __future__ import absolute_import, division, print_function
__authors__ = [
 'V.Valls', 'H.Payno']
__license__ = 'MIT'
__copyright__ = 'European Synchrotron Radiation Facility, Grenoble, France'
__date__ = '21/02/2018'
import sys, unittest, logging, subprocess
from tomwer.test.utils.utilstest import UtilsTest
_logger = logging.getLogger(__name__)

class TestScriptsHelp(unittest.TestCase):

    def executeCommandLine(self, command_line, env):
        """Execute a command line.

        Log output as debug in case of bad return code.
        """
        _logger.info('Execute: %s', ' '.join(command_line))
        p = subprocess.Popen(command_line, stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE),
          env=env)
        out, err = p.communicate()
        _logger.info('Return code: %d', p.returncode)
        try:
            out = out.decode('utf-8')
        except UnicodeError:
            pass

        try:
            err = err.decode('utf-8')
        except UnicodeError:
            pass

        if p.returncode != 0:
            _logger.info('stdout:')
            _logger.info('%s', out)
            _logger.info('stderr:')
            _logger.info('%s', err)
        else:
            _logger.debug('stdout:')
            _logger.debug('%s', out)
            _logger.debug('stderr:')
            _logger.debug('%s', err)
        self.assertEqual(p.returncode, 0)

    def executeAppHelp(self, script_name, module_name):
        script = UtilsTest.script_path(script_name, module_name)
        env = UtilsTest.get_test_env()
        if script.endswith('.exe'):
            command_line = [
             script]
        else:
            command_line = [
             sys.executable, script]
        command_line.append('--help')
        self.executeCommandLine(command_line, env)

    def testAxis(self):
        self.executeAppHelp('axis', 'tomwer.app.axis')

    def testDarkRef(self):
        self.executeAppHelp('darkref', 'tomwer.app.darkref')

    def testFtserie(self):
        self.executeAppHelp('ftserie', 'tomwer.app.ftseries')

    def testLamino(self):
        self.executeAppHelp('lamino', 'tomwer.app.lamino')

    def testRadioStack(self):
        self.executeAppHelp('radiostack', 'tomwer.app.radiostack')

    def testSampleMoved(self):
        self.executeAppHelp('samplemoved', 'tomwer.app.samplemoved')

    def testSliceStack(self):
        self.executeAppHelp('slicestack', 'tomwer.app.slicestack')

    def testRSync(self):
        self.executeAppHelp('rsync', 'tomwer.app.rsync')


def suite():
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loader(TestScriptsHelp))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())