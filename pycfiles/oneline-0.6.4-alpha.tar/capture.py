# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cygdrive/c/Users/Nad/oneline/oneline/lib/lz4/nose-1.3.4-py2.7.egg/nose/plugins/capture.py
# Compiled at: 2014-09-06 21:58:19
"""
This plugin captures stdout during test execution. If the test fails
or raises an error, the captured output will be appended to the error
or failure output. It is enabled by default but can be disabled with
the options ``-s`` or ``--nocapture``.

:Options:
  ``--nocapture``
    Don't capture stdout (any stdout output will be printed immediately)

"""
import logging, os, sys
from nose.plugins.base import Plugin
from nose.pyversion import exc_to_unicode, force_unicode
from nose.util import ln
from StringIO import StringIO
log = logging.getLogger(__name__)

class Capture(Plugin):
    """
    Output capture plugin. Enabled by default. Disable with ``-s`` or
    ``--nocapture``. This plugin captures stdout during test execution,
    appending any output captured to the error or failure output,
    should the test fail or raise an error.
    """
    enabled = True
    env_opt = 'NOSE_NOCAPTURE'
    name = 'capture'
    score = 1600

    def __init__(self):
        self.stdout = []
        self._buf = None
        return

    def options(self, parser, env):
        """Register commandline options
        """
        parser.add_option('-s', '--nocapture', action='store_false', default=not env.get(self.env_opt), dest='capture', help="Don't capture stdout (any stdout output will be printed immediately) [NOSE_NOCAPTURE]")

    def configure(self, options, conf):
        """Configure plugin. Plugin is enabled by default.
        """
        self.conf = conf
        if not options.capture:
            self.enabled = False

    def afterTest(self, test):
        """Clear capture buffer.
        """
        self.end()
        self._buf = None
        return

    def begin(self):
        """Replace sys.stdout with capture buffer.
        """
        self.start()

    def beforeTest(self, test):
        """Flush capture buffer.
        """
        self.start()

    def formatError(self, test, err):
        """Add captured output to error report.
        """
        test.capturedOutput = output = self.buffer
        self._buf = None
        if not output:
            return err
        else:
            ec, ev, tb = err
            return (ec, self.addCaptureToErr(ev, output), tb)

    def formatFailure(self, test, err):
        """Add captured output to failure report.
        """
        return self.formatError(test, err)

    def addCaptureToErr(self, ev, output):
        ev = exc_to_unicode(ev)
        output = force_unicode(output)
        return ('\n').join([ev, ln('>> begin captured stdout <<'),
         output, ln('>> end captured stdout <<')])

    def start(self):
        self.stdout.append(sys.stdout)
        self._buf = StringIO()
        sys.stdout = self._buf

    def end(self):
        if self.stdout:
            sys.stdout = self.stdout.pop()

    def finalize(self, result):
        """Restore stdout.
        """
        while self.stdout:
            self.end()

    def _get_buffer(self):
        if self._buf is not None:
            return self._buf.getvalue()
        else:
            return

    buffer = property(_get_buffer, None, None, 'Captured stdout output.')