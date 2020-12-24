# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/nlstatus.py
# Compiled at: 2009-12-08 17:43:30
"""
Function library to check the status of NetLogger components
"""
__rcsid__ = '$Id: nlstatus.py 23537 2009-02-13 05:00:17Z dang $'
__author__ = 'Dan Gunter <dkgunter@lbl.gov>'
import glob, os, re
from netlogger.nldate import parseISO, DateFormatError, guess

class StatusCheckerError(Exception):
    pass


class InitError(StatusCheckerError):
    pass


class ParameterError(InitError):

    def __init__(self, how, what, why='Cause unknown'):
        msg = "%s parameter '%s': %s" % (how, what, why)
        Exception.__init__(self, msg)


class Status:
    """Result of checking status.
    """
    (ERROR, FAIL, OK) = (-1, 0, 1)
    NAGIOS_STR = {ERROR: 'CRITICAL', FAIL: 'CRITICAL', OK: 'OK'}

    def __init__(self, code, msg=''):
        """Create new status with the given code and message (msg).
        """
        self.code = code
        self.msg = msg

    def nagiosString(self):
        """Format into a Nagios-style return value.
        Returns a string that Nagios should understand.
        """
        status = self.NAGIOS_STR.get(self.code, 'UNKNOWN')
        return '%s: %s' % (status, self.msg)


class Success(Status):
    """Syntactic sugar for creating a successful status."""

    def __init__(self, why):
        Status.__init__(self, Status.OK, msg=why)


class Failure(Status):

    def __init__(self, why):
        """Syntactic sugar for creating a failure status."""
        Status.__init__(self, Status.FAIL, msg=why)


class Abort(Status):
    """Syntactic sugar for creating an abort (error) status."""

    def __init__(self, why):
        Status.__init__(self, Status.ERROR, msg=why)


class StatusChecker:
    """Base class for something that checks the status
    of a component.
    """

    def __init__(self, since=0):
        """Set base class parameters:
        - since: time, as a string or float, which the
                 thing checked should be more recent than
        """
        if isinstance(since, float):
            self.since = since
        (_, self.since) = guess(since)

    def check(self):
        """Override in derived class to do the work.
        Will raise a subclass of StatusCheckerError if there
        is an unexpected error.
        Returns an instance of Status.
        """
        raise NotImplementedError()


class Syslogng(StatusChecker):
    """Check that the last dated entry in a syslog-ng log is
    recent enough.
    """
    DATE_RE = re.compile('\\d{4}-\\d{2}-\\d{2}T[012]\\d:\\d{2}:\\d{2}-\\d{2}:\\d{2}')

    def __init__(self, log_file=None, since=None):
        """Set parameters:
        - log_file: (string) Full path to log file to be searched.

        """
        if log_file is None:
            raise ParameterError('Missing', 'log_file')
        self._log = log_file
        StatusChecker.__init__(self, since=since)
        return

    def check(self):
        """Find last message that looks like this:

        2009-02-01T12:22:05-00:00 syslog_ng@pdsfgrid5.nersc.gov -- MARK --
        
        in the log. 
        """
        if not os.path.exists(self._log):
            return Abort("File '%s' not found" % self._log)
        try:
            f = file(self._log)
        except IOError, E:
            return Abort("Cannot open '%s': %s" % (
             self._log, E))

        try:
            f.seek(-2, 2)
            while 1:
                while f.read(1) != '\n':
                    f.seek(-2, 1)

                line = f.readline().strip()
                if self.DATE_RE.match(line):
                    date_str = line[:25]
                    mark_time = parseISO(date_str)
                    if mark_time >= self.since:
                        result = Success('last entry is %s' % date_str)
                    else:
                        result = Failure('no entry since %s' % date_str)
                    break

        except IOError, E:
            result = Abort('I/O Error: %s' % E)

        return result


class Rawlogs(StatusChecker):

    def __init__(self, log_dir=None, log_pat='*.log', since=None):
        """Set parameters:
        - log_dir: (string) Where log files should be found
        - log_pat: (string) Glob expression to find log files
        - since: see StatusChecker
        """
        if log_dir is None:
            raise ParameterError('Missing', 'log_dir')
        if not os.path.isdir(log_dir):
            raise ParameterError('Non-existent', 'log_dir')
        self._dir, self._pat = log_dir, log_pat
        StatusChecker.__init__(self, since=since)
        return

    def check(self):
        """Look at all files in directory matching the pattern,
        compare the modification time (mtime) to the desired date,
        and fail if any are too 'stale'.
        """
        save_dir = os.getcwd()
        try:
            os.chdir(self._dir)
        except IOError, E:
            return Abort("Cannot change to directory '%s': %s" % (
             self._dir, E))
        else:
            files = glob.glob(self._pat)
            stale_files = []
            for filename in files:
                try:
                    modified_time = os.stat(filename).st_mtime
                    if modified_time < self.since:
                        stale_files.append(filename)
                except OSError, E:
                    pass

            if not stale_files:
                result = Success('%d files' % len(files))
            result = Failure('%d out of %d files are stale: first=%s' % (
             len(stale_files), len(files), stale_files[0]))

        os.chdir(save_dir)
        return result