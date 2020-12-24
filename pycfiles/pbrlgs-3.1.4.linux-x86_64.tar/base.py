# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/tests/base.py
# Compiled at: 2017-12-04 07:19:32
"""Common utilities used in testing"""
import os, shutil, subprocess, sys, fixtures, testresources, testtools
from testtools import content
from pbr import options

class DiveDir(fixtures.Fixture):
    """Dive into given directory and return back on cleanup.

    :ivar path: The target directory.
    """

    def __init__(self, path):
        self.path = path

    def setUp(self):
        super(DiveDir, self).setUp()
        self.addCleanup(os.chdir, os.getcwd())
        os.chdir(self.path)


class BaseTestCase(testtools.TestCase, testresources.ResourcedTestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        test_timeout = os.environ.get('OS_TEST_TIMEOUT', 30)
        try:
            test_timeout = int(test_timeout)
        except ValueError:
            print 'OS_TEST_TIMEOUT set to invalid value defaulting to no timeout'
            test_timeout = 0

        if test_timeout > 0:
            self.useFixture(fixtures.Timeout(test_timeout, gentle=True))
        if os.environ.get('OS_STDOUT_CAPTURE') in options.TRUE_VALUES:
            stdout = self.useFixture(fixtures.StringStream('stdout')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stdout', stdout))
        if os.environ.get('OS_STDERR_CAPTURE') in options.TRUE_VALUES:
            stderr = self.useFixture(fixtures.StringStream('stderr')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stderr', stderr))
        self.log_fixture = self.useFixture(fixtures.FakeLogger('pbr'))
        self.useFixture(fixtures.TempHomeDir())
        self.useFixture(fixtures.NestedTempfile())
        self.useFixture(fixtures.FakeLogger())
        self.useFixture(fixtures.EnvironmentVariable('PBR_VERSION', '0.0'))
        self.temp_dir = self.useFixture(fixtures.TempDir()).path
        self.package_dir = os.path.join(self.temp_dir, 'testpackage')
        shutil.copytree(os.path.join(os.path.dirname(__file__), 'testpackage'), self.package_dir)
        self.addCleanup(os.chdir, os.getcwd())
        os.chdir(self.package_dir)
        self.addCleanup(self._discard_testpackage)
        if not getattr(self, 'preversioned', True):
            self.useFixture(fixtures.EnvironmentVariable('PBR_VERSION'))
            setup_cfg_path = os.path.join(self.package_dir, 'setup.cfg')
            with open(setup_cfg_path, 'rt') as (cfg):
                content = cfg.read()
            content = content.replace('version = 0.1.dev', '')
            with open(setup_cfg_path, 'wt') as (cfg):
                cfg.write(content)

    def _discard_testpackage(self):
        for k in list(sys.modules):
            if k == 'pbr_testpackage' or k.startswith('pbr_testpackage.'):
                del sys.modules[k]

    def run_pbr(self, *args, **kwargs):
        return self._run_cmd('pbr', args, **kwargs)

    def run_setup(self, *args, **kwargs):
        return self._run_cmd(sys.executable, (('setup.py', ) + args), **kwargs)

    def _run_cmd(self, cmd, args=[], allow_fail=True, cwd=None):
        """Run a command in the root of the test working copy.

        Runs a command, with the given argument list, in the root of the test
        working copy--returns the stdout and stderr streams and the exit code
        from the subprocess.

        :param cwd: If falsy run within the test package dir, otherwise run
            within the named path.
        """
        cwd = cwd or self.package_dir
        result = _run_cmd([cmd] + list(args), cwd=cwd)
        if result[2] and not allow_fail:
            raise Exception('Command failed retcode=%s' % result[2])
        return result


class CapturedSubprocess(fixtures.Fixture):
    """Run a process and capture its output.

    :attr stdout: The output (a string).
    :attr stderr: The standard error (a string).
    :attr returncode: The return code of the process.

    Note that stdout and stderr are decoded from the bytestrings subprocess
    returns using error=replace.
    """

    def __init__(self, label, *args, **kwargs):
        """Create a CapturedSubprocess.

        :param label: A label for the subprocess in the test log. E.g. 'foo'.
        :param *args: The *args to pass to Popen.
        :param **kwargs: The **kwargs to pass to Popen.
        """
        super(CapturedSubprocess, self).__init__()
        self.label = label
        self.args = args
        self.kwargs = kwargs
        self.kwargs['stderr'] = subprocess.PIPE
        self.kwargs['stdin'] = subprocess.PIPE
        self.kwargs['stdout'] = subprocess.PIPE

    def setUp(self):
        super(CapturedSubprocess, self).setUp()
        proc = subprocess.Popen(*self.args, **self.kwargs)
        out, err = proc.communicate()
        self.out = out.decode('utf-8', 'replace')
        self.err = err.decode('utf-8', 'replace')
        self.addDetail(self.label + '-stdout', content.text_content(self.out))
        self.addDetail(self.label + '-stderr', content.text_content(self.err))
        self.returncode = proc.returncode
        if proc.returncode:
            raise AssertionError('Failed process %s' % proc.returncode)
        self.addCleanup(delattr, self, 'out')
        self.addCleanup(delattr, self, 'err')
        self.addCleanup(delattr, self, 'returncode')


def _run_cmd(args, cwd):
    """Run the command args in cwd.

    :param args: The command to run e.g. ['git', 'status']
    :param cwd: The directory to run the comamnd in.
    :return: ((stdout, stderr), returncode)
    """
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    streams = tuple(s.decode('latin1').strip() for s in p.communicate())
    for stream_content in streams:
        print stream_content

    return streams + (p.returncode,)


def _config_git():
    _run_cmd([
     'git', 'config', '--global', 'user.email', 'example@example.com'], None)
    _run_cmd([
     'git', 'config', '--global', 'user.name', 'OpenStack Developer'], None)
    _run_cmd([
     'git', 'config', '--global', 'user.signingkey',
     'example@example.com'], None)
    return