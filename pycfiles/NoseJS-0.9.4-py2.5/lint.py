# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/nosejs/lint.py
# Compiled at: 2009-03-06 12:32:54
import sys, unittest, subprocess, logging
log = logging.getLogger('nose.plugins.nosejs')

class JsLintError(Exception):
    """JavaScript Lint Error"""
    pass


class JsLintWarning(Exception):
    """JavaScript Lint Warning"""
    pass


class JsLintTestCase(unittest.TestCase):
    """A test case that runs a file through the jsl lint executable."""
    __test__ = False

    def __init__(self, filename, jsl_bin, jsl_options=None, stop_on_error=False):
        self.jsl_bin = jsl_bin
        self.jsl_options = jsl_options or []
        self.filename = filename
        self.stop_on_error = stop_on_error
        super(JsLintTestCase, self).__init__()

    def runTest(self):
        pass

    def run(self, result):
        cmd = [
         self.jsl_bin]
        cmd.extend(self.jsl_options)
        start = '=NJS=ST='
        sep = '=NJS=SEP='
        cmd.extend([
         '-output-format', start + '__FILE__' + sep + '__LINE__' + sep + '__ERROR__',
         '-nologo', '-nosummary', '-nofilelisting',
         '-process', self.filename])
        log.debug('jsl command: %s' % (' ').join(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.stdout.read()
        returncode = p.wait()
        try:
            if returncode != 0:
                msgs = output.split(start)
                for msg in msgs:
                    if msg.strip() == '':
                        continue
                    try:
                        (file, line, error) = msg.split(sep)
                    except:
                        log.debug('Could not split %s using markers' % msg)
                        raise

                    error = error.strip()
                    if error.startswith('lint warning:'):
                        etype = JsLintWarning
                    else:
                        etype = JsLintError
                    result.addError(self, (etype, '%s:%s %s' % (file, line, error), None))
                    if self.stop_on_error:
                        break

            else:
                result.addSuccess(self)
        finally:
            result.stopTest(self)

        return

    def address(self):
        return (
         self.id(), None, None)

    def id(self):
        return repr(self)

    def shortDescription(self):
        return repr(self)

    def __repr__(self):
        return 'javascript-lint: %s' % self.filename

    __str__ = __repr__