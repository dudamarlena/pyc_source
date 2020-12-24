# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x/code/OONI/ooni-probe/ooni/nettests/third_party/netalyzr.py
# Compiled at: 2016-06-26 06:48:30
import time, os, distutils.spawn
from twisted.python import usage
from twisted.internet import reactor, threads
from ooni.templates import process
from ooni.utils import log

class JavaNotInstalled(Exception):
    pass


class CouldNotFindNetalyzrCli(Exception):
    pass


class UsageOptions(usage.Options):
    optParameters = [
     [
      'clipath', 'p', None, 'Specify the path to NetalyzrCLI.jar (can be downloaded from http://netalyzr.icsi.berkeley.edu/NetalyzrCLI.jar).']]


class NetalyzrWrapperTest(process.ProcessTest):
    name = 'NetalyzrWrapper'
    description = 'A wrapper around the Netalyzr java command line client.'
    author = 'Jacob Appelbaum <jacob@appelbaum.net>'
    requiredOptions = [
     'clipath']
    usageOptions = UsageOptions
    requiresRoot = False
    requiresTor = False
    timeout = 300

    def requirements(self):
        if not distutils.spawn.find_executable('java'):
            raise JavaNotInstalled('Java is not installed.')

    def setUp(self):
        if not os.path.exists(self.localOptions['clipath']):
            raise CouldNotFindNetalyzrCli(('Could not find NetalyzrCLI.jar at {}').format(self.localOptions['clipath']))
        self.command = [
         distutils.spawn.find_executable('java'),
         '-jar',
         ('{}').format(self.localOptions['clipath']),
         '-d']

    def test_run_netalyzr(self):
        """
        This test simply wraps netalyzr and runs it from command line
        """
        log.msg('Running NetalyzrWrapper (this will take some time, be patient)')
        log.debug("with command '%s'" % self.command)
        self.d = self.run(self.command, env=os.environ, usePTY=1)
        return self.d