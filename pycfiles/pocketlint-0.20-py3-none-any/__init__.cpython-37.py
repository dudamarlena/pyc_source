# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jkonecny/Documents/RH/packager/git/pocketlint/build/lib/pocketlint/__init__.py
# Compiled at: 2019-08-30 04:21:13
# Size of source mod 2**32: 14382 bytes
from __future__ import print_function
import atexit, concurrent.futures, os, re, shutil, subprocess, sys, tempfile
from distutils.version import LooseVersion

class PocketLintConfig(object):
    __doc__ = 'Configuration object that a project should use to tell pylint how\n       to operate.  Instance attributes:\n\n       falsePositives    -- A list of FalsePositive objects for filtering\n                            incorrect pylint error messages.\n                            Default: []\n       loadAllExtensions -- Load all the extensions to the pylint. This will resolve\n                            I1101(c-extension-no-member) messages but it could be\n                            potentially dangerous. See man pylint --unsafe-load-any-extension\n                            Default: False\n    '

    def __init__(self):
        self.falsePositives = []
        self.loadAllExtensions = False

    @property
    def disabledOptions(self):
        """A list of warning and error codes that pylint should ignore
           when checking source code.  The base PocketLintConfig object
           comes with a pretty useful list, but subclasses can feel free
           to add or remove as desired.  This list should strive to be empty,
           though.
        """
        return [
         'W0110',
         'W0123',
         'W0141',
         'W0142',
         'W0212',
         'W0511',
         'W0603',
         'W0613',
         'W0614',
         'E0012',
         'I0011',
         'I0012',
         'I0013']

    @property
    def extraArgs(self):
        """Extra command line arguments that should be passed to pylint.  These
           arguments will be added after the default ones so they can override
           the base config, but may in turn also be overridden by arguments
           passed to the testing framework on the command line.
        """
        return []

    @property
    def initHook(self):
        """Python code to be run by pylint as part of an init hook.  Most
           projects will not need this.
        """
        return ''

    @property
    def pylintPlugins(self):
        """A list of plugins provided by PocketLint to be added to the set of
           pylink checkers.  Not all of these will be relevant to all projects,
           but they should still be able to run without error.  If necessary,
           projects can modify this list as needed.
        """
        return [
         'pocketlint.checkers.environ',
         'pocketlint.checkers.intl',
         'pocketlint.checkers.markup',
         'pocketlint.checkers.pointless-override',
         'pocketlint.checkers.preconf']

    @property
    def ignoreNames(self):
        """A set of names to skip when automatically determining the list of
           files to lint. The items in this set could be a particular filename
           to skip or a directory that the linter should not traverse into.
           The items should be just basenames, not paths.
        """
        return set()


class FalsePositive(object):
    __doc__ = 'An object used in filtering out incorrect results from pylint.  Pass in\n       a regular expression matching a pylint error message that should be\n       ignored.  This object can also be used to keep track of how often it is\n       used, for auditing that false positives are still useful.\n    '

    def __init__(self, regex):
        self.regex = regex
        self.used = 0


class PocketLinter(object):
    __doc__ = 'Main class that does the hard work of running pylint on a project.\n       Pass an instance of PocketLintConfig to a new instance of this class\n       and then call its run method.  This is all that should be necessary for\n       most projects:\n\n       from pocketlint import PocketLintConfig, PocketLinter\n\n       class FooLintConfig(PocketLintConfig):\n          ....\n\n       if __name__ == "__main__":\n           conf = FooLintConfig()\n           linter = PocketLinter(conf)\n           rc = linter.run()\n           os._exit(rc)\n    '

    def __init__(self, config):
        self._config = config
        self._pylint_log = False
        if 'top_srcdir' not in os.environ:
            self._pylint_log = True

    def _del_xdg_runtime_dir(self):
        shutil.rmtree(os.environ['XDG_RUNTIME_DIR'])

    @property
    def _files(self):
        retval = []
        srcdir = os.environ.get('top_srcdir', os.getcwd())
        for root, dirnames, files in os.walk(srcdir):
            for i in self._config.ignoreNames:
                if i in dirnames:
                    dirnames.remove(i)
                if i in files:
                    files.remove(i)

            for f in files:
                try:
                    with open(root + '/' + f) as (fo):
                        lines = fo.readlines()
                except UnicodeDecodeError:
                    continue

                if '# pylint: skip-file\n' in lines:
                    continue
                if not f.endswith('.py'):
                    if not lines or str(lines[0]).startswith('#!/usr/bin/python'):
                        retval.append(root + '/' + f)

        return retval

    @property
    def _pylint_args(self):
        args = ["--msg-template='{msg_id}({symbol}):{line:3d},{column}: {obj}: {msg}'",
         '-r', 'n',
         '--disable', 'C,R',
         '--rcfile', '/dev/null',
         '--dummy-variables-rgx', '_',
         '--ignored-classes', 'DefaultInstall,Popen,QueueFactory,TransactionSet',
         '--defining-attr-methods', '__init__,grabObjects,initialize,reset,start,setUp',
         '--load-plugins', ','.join(self._config.pylintPlugins),
         '--deprecated-modules', 'string,regsub,TERMIOS,Bastion,rexec',
         '--disable', ','.join(self._config.disabledOptions)]
        if self._config.initHook:
            args += ['--init-hook', self._config.initHook]
        if self._config.extraArgs:
            args += self._config.extraArgs
        if self._config.loadAllExtensions:
            args += ['--unsafe-load-any-extension=yes']
        if self._pylint_version >= LooseVersion('1.7.0'):
            args += ['-s', 'n']
        return args

    def _command_exists(self, exc):
        proc = subprocess.Popen(['which', exc], stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        _out, _err = proc.communicate()
        return proc.returncode == 0

    @property
    def _pylint_executable(self):
        return [sys.executable, '-m', 'pylint']

    @property
    def _pylint_version(self):
        exc = self._pylint_executable
        exc.append('--version')
        proc = subprocess.Popen(exc, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        stdout, _stderr = proc.communicate()
        pattern = re.compile('.+ (?P<version>[1-9.]+)')
        match = pattern.search(stdout.decode())
        if match:
            return LooseVersion(match.group('version'))
        return LooseVersion('0')

    def _parseArgs(self):
        args = []
        files = []
        if len(sys.argv) > 1:
            for arg in sys.argv[1:]:
                if arg.startswith('-'):
                    args.append(arg)
                else:
                    files.append(arg)

        return (
         args, files)

    def _setupEnvironment(self):
        builddir = os.environ.get('top_builddir', os.getcwd())
        if 'XDG_RUNTIME_DIR' not in os.environ:
            d = tempfile.mkdtemp()
            os.environ['XDG_RUNTIME_DIR'] = d
            atexit.register(self._del_xdg_runtime_dir)
        if 'TERM' in os.environ:
            os.environ.pop('TERM')
        os.environ['NO_AT_BRIDGE'] = '1'
        os.environ['GDK_BACKEND'] = 'x11'
        os.environ['PYLINTHOME'] = builddir + '/tests/pylint/.pylint.d'
        if not os.path.exists(os.environ['PYLINTHOME']):
            os.mkdir(os.environ['PYLINTHOME'])

    def _filterFalsePositives(self, filename, lines):
        if not self._config.falsePositives:
            return lines
        retval = []
        for line in lines:
            if not (line.startswith('*****') or line.startswith('Using config file') or line.strip()):
                continue
            else:
                validError = True
                for regex in self._config.falsePositives:
                    if re.search(regex.regex, line):
                        regex.used += 1
                        validError = False
                        break

            if validError:
                retval.append(line)

        if retval:
            retval.insert(0, '************* Module ' + filename)
        return retval

    def _run_one(self, filename, args):
        proc = subprocess.Popen((self._pylint_executable + self._pylint_args + args + [filename]), stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        stdout, stderr = proc.communicate()
        output = stdout + stderr
        lines = self._filterFalsePositives(filename, output.decode('utf-8').split('\n'))
        if lines:
            return (
             '\n'.join(lines), proc.returncode)
        return ('', 0)

    def _print(self, s, fo=None):
        print(s)
        sys.stdout.flush()
        if fo:
            print(s, file=fo)
            fo.flush()

    def run(self):
        retval = 0
        self._setupEnvironment()
        args, files = self._parseArgs()
        if not files:
            files = self._files
        elif self._pylint_log:
            fo = open('pylint-log', 'w')
        else:
            fo = None
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as (executor):
            jobs = []
            for f in files:
                jobs.append(executor.submit(self._run_one, f, args))

            for job in concurrent.futures.as_completed(jobs):
                result = job.result()
                output = result[0].strip()
                if output:
                    self._print(output, fo)
                if result[1] > retval:
                    retval = result[1]

        unusedFPs = []
        for fp in self._config.falsePositives:
            if fp.used == 0:
                unusedFPs.append(fp.regex)

        if unusedFPs:
            self._print('************* Unused False Positives Found:', fo)
            for fp in unusedFPs:
                self._print(fp, fo)

        return retval