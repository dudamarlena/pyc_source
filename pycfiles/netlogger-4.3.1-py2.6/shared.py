# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/stress/shared.py
# Compiled at: 2010-03-22 23:48:32
"""
Shared classes and functions for stress tests
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: shared.py 24358 2010-03-23 03:48:32Z dang $'
import signal, sys

class ProgramException(Exception):
    pass


class ProgramAlreadyRunning(ProgramException):
    pass


class ProgramNotRunning(ProgramException):
    pass


class ProgramCannotRun(ProgramException):
    pass


class Report:
    """A simple tabular report.
    """
    COL_SEP = '\t'

    def __init__(self, title='Report', col_names=['Value'], col_formats=None, ostrm=sys.stderr):
        """Constructor.

        :Parameters:
          title - Title of report
          col_names - List of (string) column names
          col_formats - List of (string) column formats, default is
                        '%s', as many as col_names
          ostr - Output stream for printing
        """
        self.title, self.ostrm = title, ostrm
        if col_formats is None:
            self._formats = [
             '%s'] * col_names
        else:
            self._formats = col_formats
        self._names = col_names
        self._header()
        return

    def _header(self):
        self.ostrm.write('== %s ==\n' % self.title)
        self.ostrm.write(self.COL_SEP.join(self._names))
        self.ostrm.write('\n')

    def values(self, values):
        text = self.COL_SEP.join([ f % v for (v, f) in zip(values, self._formats)
                                 ])
        self.ostrm.write(text)
        self.ostrm.write('\n')


class Program:

    def __init__(self, path, args):
        self._full_path = path
        self._name = os.path.basename(path)
        self._args = list(args)
        self._running = False
        self._last_output = ''

    def run(self):
        """Run the program.
        """
        if self._running:
            raise ProgramAlreadyRunning()
        pargs = [
         self._full_path] + self._args
        try:
            self._process = Popen(pargs, stderr=STDOUT, stdout=PIPE)
        except OSError, E:
            raise ProgramCannotRun(str(E))

        self._running = True

    def stop(self, signo=signal.SIGTERM):
        """Stop the program and return its retcode.
        """
        if not self._running:
            raise ProgramNotRunning()
        log.debug('%s.stopping.start' % self._name)
        while 1:
            retcode = self._process.poll()
            if retcode is not None:
                break
            try:
                os.kill(self._process.pid, signo)
                if signo != signal.SIGKILL:
                    time.sleep(2)
                    retcode = self._process.poll()
                    if retcode is None:
                        os.kill(self._process.pid, signal.SIGKILL)
                self._process.wait()
            except OSError:
                continue

            time.sleep(1)

        self._last_output = self._getOutput()
        try:
            del self._process
        except AttributeError:
            pass

        self._running = False
        log.debug('%s.stopping.end' % self._name, status=retcode)
        return retcode

    def getOutput(self):
        """Return output of last (stopped) run.
        """
        return self._last_output

    def _getOutput(self):
        buf = ''
        while 1:
            data = self._process.stdout.read()
            if len(data) == 0:
                break
            buf = buf + data

        return buf