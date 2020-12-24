# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Tests/CheetahWrapper.py
# Compiled at: 2019-09-22 10:12:27
__doc__ = "\nTests for the 'cheetah' command.\n\nBesides unittest usage, recognizes the following command-line options:\n    --list CheetahWrapper.py\n        List all scenarios that are tested.  The argument is the path\n        of this script.\n     --nodelete\n        Don't delete scratch directory at end.\n     --output\n        Show the output of each subcommand.  (Normally suppressed.)\n"
import os, os.path, re, shutil, sys, tempfile, unittest
from optparse import OptionParser
from Cheetah.CheetahWrapper import CheetahWrapper
try:
    from subprocess import Popen, PIPE, STDOUT

    class Popen4(Popen):

        def __init__(self, cmd, bufsize=-1, shell=True, close_fds=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, **kwargs):
            super(Popen4, self).__init__(cmd, bufsize=bufsize, shell=shell, close_fds=close_fds, stdin=stdin, stdout=stdout, stderr=stderr, **kwargs)
            self.tochild = self.stdin
            self.fromchild = self.stdout
            self.childerr = self.stderr


except ImportError:
    from popen2 import Popen4

DELETE = True
OUTPUT = False
BACKUP_SUFFIX = CheetahWrapper.BACKUP_SUFFIX

def warn(msg):
    sys.stderr.write(msg + '\n')


class CFBase(unittest.TestCase):
    """Base class for "cheetah compile" and "cheetah fill" unit tests.
    """
    srcDir = ''
    subdirs = ('child', 'child/grandkid')
    srcFiles = ('a.tmpl', 'child/a.tmpl', 'child/grandkid/a.tmpl')
    expectError = False

    def inform(self, message):
        if self.verbose:
            print message

    def setUp(self):
        """Create the top-level directories, subdirectories and .tmpl
           files.
        """
        self.cmd = self.locate_cheetah('cheetah')
        cwd = os.getcwd()
        if not os.environ.get('PYTHONPATH'):
            os.environ['PYTHONPATH'] = cwd
        else:
            pythonPath = os.environ['PYTHONPATH']
            if pythonPath != cwd and not pythonPath.endswith(':%s' % cwd):
                os.environ['PYTHONPATH'] = '%s:%s' % (pythonPath, cwd)
            self.scratchDir = scratchDir = tempfile.mkdtemp()
            self.origCwd = os.getcwd()
            os.chdir(scratchDir)
            if self.srcDir:
                os.mkdir(self.srcDir)
            for dir in self.subdirs:
                os.mkdir(dir)

            for fil in self.srcFiles:
                f = open(fil, 'w')
                f.write('Hello, world!\n')
                f.close()

    def tearDown(self):
        global DELETE
        os.chdir(self.origCwd)
        if DELETE:
            shutil.rmtree(self.scratchDir, True)
            if os.path.exists(self.scratchDir):
                warn('Warning: unable to delete scratch directory %s')
        else:
            warn('Warning: not deleting scratch directory %s' % self.scratchDir)

    def _checkDestFileHelper(self, path, expected, allowSurroundingText, errmsg):
        """Low-level helper to check a destination file.

           in : path, string, the destination path.
                expected, string, the expected contents.
                allowSurroundingtext, bool, allow the result to contain
                  additional text around the 'expected' substring?
                errmsg, string, the error message.  It may contain the
                  following "%"-operator keys: path, expected, result.
           out: None
        """
        path = os.path.abspath(path)
        exists = os.path.exists(path)
        msg = 'destination file missing: %s' % path
        self.assertTrue(exists, msg)
        f = open(path, 'r')
        result = f.read()
        f.close()
        if allowSurroundingText:
            success = result.find(expected) != -1
        else:
            success = result == expected
        msg = errmsg % locals()
        self.assertTrue(success, msg)

    def checkCompile(self, path):
        expected = 'Hello, world!'
        errmsg = "destination file %(path)s doesn't contain expected substring:\n%(expected)r"
        self._checkDestFileHelper(path, expected, True, errmsg)

    def checkFill(self, path):
        expected = 'Hello, world!\n'
        errmsg = 'destination file %(path)s contains wrong result.\nExpected %(expected)r\nFound %(result)r'
        self._checkDestFileHelper(path, expected, False, errmsg)

    def checkSubdirPyInit(self, path):
        """Verify a destination subdirectory exists and contains an
           __init__.py file.
        """
        exists = os.path.exists(path)
        msg = 'destination subdirectory %s misssing' % path
        self.assertTrue(exists, msg)
        initPath = os.path.join(path, '__init__.py')
        exists = os.path.exists(initPath)
        msg = 'destination init file missing: %s' % initPath
        self.assertTrue(exists, msg)

    def checkNoBackup(self, path):
        """Verify 'path' does not exist.  (To check --nobackup.)
        """
        exists = os.path.exists(path)
        msg = 'backup file exists in spite of --nobackup: %s' % path
        self.assertFalse(exists, msg)

    def locate_cheetah(self, cmd):
        paths = os.getenv('PATH')
        if not paths:
            return cmd
        paths = paths.split(':')
        for p in paths:
            p = os.path.join(p, cmd)
            p = os.path.abspath(p)
            if os.path.isfile(p):
                return p

        return cmd

    def assertWin32Subprocess(self, cmd):
        try:
            from subprocess import Popen, PIPE, STDOUT
        except ImportError:
            _in, _out = os.popen4(cmd)
            _in.close()
            output = _out.read()
            status = _out.close()
            if status is None:
                status = 0
        else:
            process = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
            process.stdin.close()
            output = process.stdout.read()
            status = process.wait()
            process.stdout.close()

        return (status, output)

    def assertPosixSubprocess(self, cmd):
        cmd = cmd.replace('cheetah', self.cmd)
        process = Popen4(cmd, env=os.environ)
        process.tochild.close()
        output = process.fromchild.read()
        status = process.wait()
        process.fromchild.close()
        return (
         status, output)

    def assertSubprocess(self, cmd, nonzero=False):
        status, output = (None, None)
        if sys.platform == 'win32':
            status, output = self.assertWin32Subprocess(cmd)
        else:
            status, output = self.assertPosixSubprocess(cmd)
        if not nonzero:
            self.assertEqual(status, 0, 'Subprocess exited with a non-zero status (%d)\n                            %s' % (status, output))
        else:
            self.assertNotEqual(status, 0, 'Subprocess exited with a zero status (%d)\n                            %s' % (status, output))
        return output

    def go(self, cmd, expectedStatus=0, expectedOutputSubstring=None):
        """Run a "cheetah compile" or "cheetah fill" subcommand.

           in : cmd, string, the command to run.
                expectedStatus, int, subcommand's expected output status.
                  0 if the subcommand is expected to succeed, 1-255 otherwise.
                expectedOutputSubstring, string, substring which much appear
                  in the standard output or standard error.  None to skip this
                  test.
           out: None.
        """
        output = self.assertSubprocess(cmd)
        if expectedOutputSubstring is not None:
            msg = 'substring %r not found in subcommand output: %s' % (
             expectedOutputSubstring, cmd)
            substringTest = output.find(expectedOutputSubstring) != -1
            self.assertTrue(substringTest, msg)
        return


class CFIdirBase(CFBase):
    """Subclass for tests with --idir.
    """
    srcDir = 'SRC'
    subdirs = ('SRC/child', 'SRC/child/grandkid')
    srcFiles = ('SRC/a.tmpl', 'SRC/child/a.tmpl', 'SRC/child/grandkid/a.tmpl')


class OneFile(CFBase):

    def testCompile(self):
        self.go('cheetah compile a.tmpl')
        self.checkCompile('a.py')

    def testFill(self):
        self.go('cheetah fill a.tmpl')
        self.checkFill('a.html')

    def testText(self):
        self.go('cheetah fill --oext txt a.tmpl')
        self.checkFill('a.txt')


class OneFileNoExtension(CFBase):

    def testCompile(self):
        self.go('cheetah compile a')
        self.checkCompile('a.py')

    def testFill(self):
        self.go('cheetah fill a')
        self.checkFill('a.html')

    def testText(self):
        self.go('cheetah fill --oext txt a')
        self.checkFill('a.txt')


class SplatTmpl(CFBase):

    def testCompile(self):
        self.go('cheetah compile *.tmpl')
        self.checkCompile('a.py')

    def testFill(self):
        self.go('cheetah fill *.tmpl')
        self.checkFill('a.html')

    def testText(self):
        self.go('cheetah fill --oext txt *.tmpl')
        self.checkFill('a.txt')


class ThreeFilesWithSubdirectories(CFBase):

    def testCompile(self):
        self.go('cheetah compile a.tmpl child/a.tmpl child/grandkid/a.tmpl')
        self.checkCompile('a.py')
        self.checkCompile('child/a.py')
        self.checkCompile('child/grandkid/a.py')

    def testFill(self):
        self.go('cheetah fill a.tmpl child/a.tmpl child/grandkid/a.tmpl')
        self.checkFill('a.html')
        self.checkFill('child/a.html')
        self.checkFill('child/grandkid/a.html')

    def testText(self):
        self.go('cheetah fill --oext txt a.tmpl child/a.tmpl child/grandkid/a.tmpl')
        self.checkFill('a.txt')
        self.checkFill('child/a.txt')
        self.checkFill('child/grandkid/a.txt')


class ThreeFilesWithSubdirectoriesNoExtension(CFBase):

    def testCompile(self):
        self.go('cheetah compile a child/a child/grandkid/a')
        self.checkCompile('a.py')
        self.checkCompile('child/a.py')
        self.checkCompile('child/grandkid/a.py')

    def testFill(self):
        self.go('cheetah fill a child/a child/grandkid/a')
        self.checkFill('a.html')
        self.checkFill('child/a.html')
        self.checkFill('child/grandkid/a.html')

    def testText(self):
        self.go('cheetah fill --oext txt a child/a child/grandkid/a')
        self.checkFill('a.txt')
        self.checkFill('child/a.txt')
        self.checkFill('child/grandkid/a.txt')


class SplatTmplWithSubdirectories(CFBase):

    def testCompile(self):
        self.go('cheetah compile *.tmpl child/*.tmpl child/grandkid/*.tmpl')
        self.checkCompile('a.py')
        self.checkCompile('child/a.py')
        self.checkCompile('child/grandkid/a.py')

    def testFill(self):
        self.go('cheetah fill *.tmpl child/*.tmpl child/grandkid/*.tmpl')
        self.checkFill('a.html')
        self.checkFill('child/a.html')
        self.checkFill('child/grandkid/a.html')

    def testText(self):
        self.go('cheetah fill --oext txt *.tmpl child/*.tmpl child/grandkid/*.tmpl')
        self.checkFill('a.txt')
        self.checkFill('child/a.txt')
        self.checkFill('child/grandkid/a.txt')


class OneFileWithOdir(CFBase):

    def testCompile(self):
        self.go('cheetah compile --odir DEST a.tmpl')
        self.checkSubdirPyInit('DEST')
        self.checkCompile('DEST/a.py')

    def testFill(self):
        self.go('cheetah fill --odir DEST a.tmpl')
        self.checkFill('DEST/a.html')

    def testText(self):
        self.go('cheetah fill --odir DEST --oext txt a.tmpl')
        self.checkFill('DEST/a.txt')


class VarietyWithOdir(CFBase):

    def testCompile(self):
        self.go('cheetah compile --odir DEST a.tmpl child/a child/grandkid/*.tmpl')
        self.checkSubdirPyInit('DEST')
        self.checkSubdirPyInit('DEST/child')
        self.checkSubdirPyInit('DEST/child/grandkid')
        self.checkCompile('DEST/a.py')
        self.checkCompile('DEST/child/a.py')
        self.checkCompile('DEST/child/grandkid/a.py')

    def testFill(self):
        self.go('cheetah fill --odir DEST a.tmpl child/a child/grandkid/*.tmpl')
        self.checkFill('DEST/a.html')
        self.checkFill('DEST/child/a.html')
        self.checkFill('DEST/child/grandkid/a.html')

    def testText(self):
        self.go('cheetah fill --odir DEST --oext txt a.tmpl child/a child/grandkid/*.tmpl')
        self.checkFill('DEST/a.txt')
        self.checkFill('DEST/child/a.txt')
        self.checkFill('DEST/child/grandkid/a.txt')


class RecurseExplicit(CFBase):

    def testCompile(self):
        self.go('cheetah compile -R child')
        self.checkCompile('child/a.py')
        self.checkCompile('child/grandkid/a.py')

    def testFill(self):
        self.go('cheetah fill -R child')
        self.checkFill('child/a.html')
        self.checkFill('child/grandkid/a.html')

    def testText(self):
        self.go('cheetah fill -R --oext txt child')
        self.checkFill('child/a.txt')
        self.checkFill('child/grandkid/a.txt')


class RecurseImplicit(CFBase):

    def testCompile(self):
        self.go('cheetah compile -R')
        self.checkCompile('child/a.py')
        self.checkCompile('child/grandkid/a.py')

    def testFill(self):
        self.go('cheetah fill -R')
        self.checkFill('a.html')
        self.checkFill('child/a.html')
        self.checkFill('child/grandkid/a.html')

    def testText(self):
        self.go('cheetah fill -R --oext txt')
        self.checkFill('a.txt')
        self.checkFill('child/a.txt')
        self.checkFill('child/grandkid/a.txt')


class RecurseExplicitWIthOdir(CFBase):

    def testCompile(self):
        self.go('cheetah compile -R --odir DEST child')
        self.checkSubdirPyInit('DEST/child')
        self.checkSubdirPyInit('DEST/child/grandkid')
        self.checkCompile('DEST/child/a.py')
        self.checkCompile('DEST/child/grandkid/a.py')

    def testFill(self):
        self.go('cheetah fill -R --odir DEST child')
        self.checkFill('DEST/child/a.html')
        self.checkFill('DEST/child/grandkid/a.html')

    def testText(self):
        self.go('cheetah fill -R --odir DEST --oext txt child')
        self.checkFill('DEST/child/a.txt')
        self.checkFill('DEST/child/grandkid/a.txt')


class Flat(CFBase):

    def testCompile(self):
        self.go('cheetah compile --flat child/a.tmpl')
        self.checkCompile('a.py')

    def testFill(self):
        self.go('cheetah fill --flat child/a.tmpl')
        self.checkFill('a.html')

    def testText(self):
        self.go('cheetah fill --flat --oext txt child/a.tmpl')
        self.checkFill('a.txt')


class FlatRecurseCollision(CFBase):
    expectError = True

    def testCompile(self):
        self.assertSubprocess('cheetah compile -R --flat', nonzero=True)

    def testFill(self):
        self.assertSubprocess('cheetah fill -R --flat', nonzero=True)

    def testText(self):
        self.assertSubprocess('cheetah fill -R --flat', nonzero=True)


class IdirRecurse(CFIdirBase):

    def testCompile(self):
        self.go('cheetah compile -R --idir SRC child')
        self.checkSubdirPyInit('child')
        self.checkSubdirPyInit('child/grandkid')
        self.checkCompile('child/a.py')
        self.checkCompile('child/grandkid/a.py')

    def testFill(self):
        self.go('cheetah fill -R --idir SRC child')
        self.checkFill('child/a.html')
        self.checkFill('child/grandkid/a.html')

    def testText(self):
        self.go('cheetah fill -R --idir SRC --oext txt child')
        self.checkFill('child/a.txt')
        self.checkFill('child/grandkid/a.txt')


class IdirOdirRecurse(CFIdirBase):

    def testCompile(self):
        self.go('cheetah compile -R --idir SRC --odir DEST child')
        self.checkSubdirPyInit('DEST/child')
        self.checkSubdirPyInit('DEST/child/grandkid')
        self.checkCompile('DEST/child/a.py')
        self.checkCompile('DEST/child/grandkid/a.py')

    def testFill(self):
        self.go('cheetah fill -R --idir SRC --odir DEST child')
        self.checkFill('DEST/child/a.html')
        self.checkFill('DEST/child/grandkid/a.html')

    def testText(self):
        self.go('cheetah fill -R --idir SRC --odir DEST --oext txt child')
        self.checkFill('DEST/child/a.txt')
        self.checkFill('DEST/child/grandkid/a.txt')


class IdirFlatRecurseCollision(CFIdirBase):
    expectError = True

    def testCompile(self):
        self.assertSubprocess('cheetah compile -R --flat --idir SRC', nonzero=True)

    def testFill(self):
        self.assertSubprocess('cheetah fill -R --flat --idir SRC', nonzero=True)

    def testText(self):
        self.assertSubprocess('cheetah fill -R --flat --idir SRC --oext txt', nonzero=True)


class NoBackup(CFBase):
    """Run the command twice each time and verify a backup file is
       *not* created.
    """

    def testCompile(self):
        self.go('cheetah compile --nobackup a.tmpl')
        self.go('cheetah compile --nobackup a.tmpl')
        self.checkNoBackup('a.py' + BACKUP_SUFFIX)

    def testFill(self):
        self.go('cheetah fill --nobackup a.tmpl')
        self.go('cheetah fill --nobackup a.tmpl')
        self.checkNoBackup('a.html' + BACKUP_SUFFIX)

    def testText(self):
        self.go('cheetah fill --nobackup --oext txt a.tmpl')
        self.go('cheetah fill --nobackup --oext txt a.tmpl')
        self.checkNoBackup('a.txt' + BACKUP_SUFFIX)


def listTests(cheetahWrapperFile):
    """cheetahWrapperFile, string, path of this script.

       XXX TODO: don't print test where expectError is true.
    """
    rx = re.compile('self\\.go\\("(.*?)"\\)')
    f = open(cheetahWrapperFile)
    while True:
        lin = f.readline()
        if not lin:
            break
        m = rx.search(lin)
        if m:
            print m.group(1)

    f.close()


def main():
    global DELETE
    global OUTPUT
    parser = OptionParser()
    parser.add_option('--list', action='store', dest='listTests')
    parser.add_option('--nodelete', action='store_true')
    parser.add_option('--output', action='store_true')
    parser.add_option('-e', '--explain', action='store_true')
    parser.add_option('-v', '--verbose', action='store_true')
    parser.add_option('-q', '--quiet', action='store_true')
    opts, files = parser.parse_args()
    if opts.nodelete:
        DELETE = False
    if opts.output:
        OUTPUT = True
    if opts.listTests:
        listTests(opts.listTests)
    else:
        del sys.argv[1:]
        for opt in ('explain', 'verbose', 'quiet'):
            if getattr(opts, opt):
                sys.argv.append('--' + opt)

        sys.argv.extend(files)
        unittest.main()


if __name__ == '__main__':
    main()