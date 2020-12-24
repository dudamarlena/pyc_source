# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/guc.py
# Compiled at: 2010-05-03 17:56:20
"""
Parse globus-url-copy output

Sample input:
RANGE start: 0 b85667c4-e8ba-4818-96ad-07241c35a623 gsiftp://blatz.lbl.gov/etc/passwd -> gsiftp://blatz.lbl.gov/tmp/foo?b85667c4-e8ba-4818-96ad-07241c35a623

RANGE size: b85667c4-e8ba-4818-96ad-07241c35a623 6947
111 Range Marker 0-6947

RANGE range: b85667c4-e8ba-4818-96ad-07241c35a623 0-6947-6947
RANGE final range: b85667c4-e8ba-4818-96ad-07241c35a623 0-6947-6947
RANGE success: 6947 b85667c4-e8ba-4818-96ad-07241c35a623 gsiftp://blatz.lbl.gov/etc/passwd -> gsiftp://blatz.lbl.gov/tmp/foo?b85667c4-e8ba-4818-96ad-07241c35a623

Example error:

    ** File not found **

FAULT! globus_ftp_client: the server responded with an error
500 500-Command failed. : globus_l_gfs_file_open failed.
500-globus_xio: Unable to open file
/scratch/hadoop/hadoop-hadoop/dfs/data/current/subdir23/blk_5109228518806678365-nein
500-globus_xio: System error in open: No such file or directory
500-globus_xio: A system call failed: No such file or directory
500 End.

    ** Remote host not found **

FAULT! globus_xio: Unable to connect to not.a.server:2811
globus_xio: globus_libc_getaddrinfo failed.
globus_common: Name or service not known

"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: guc.py 24766 2010-05-03 21:56:20Z dang $'
from logging import DEBUG
import re, time
from netlogger.parsers.base import BaseParser, getGuid, parseDate
from netlogger.util import as_bool
EVENT_PREFIX = 'globus.guc.'

class Fault:
    """Accumulate info for an error, which is spread
    across input lines.
    """

    def __init__(self, module='', msg=''):
        self.module = module
        self.code = 0
        self.xio_errs = []
        self.common_errs = []
        if module == 'globus_xio':
            self.xio_errs.append(msg)
        else:
            self.common_errs.append(msg)

    def add_xio_error(self, msg):
        """Add an error from XIO.
        """
        self.xio_errs.append(msg)

    def add_error(self, msg):
        """Add a 'commonn', non-XIO, error
        """
        self.common_errs.append(msg)

    def get_event(self):
        return dict(event=EVENT_PREFIX + 'end', level='ERROR', status=-1, code=self.code, module=self.module, msg=(';;').join(self.common_errs), xio__msg=(';;').join(self.xio_errs))


class Parser(BaseParser):
    """Parse globus-url-copy output

    Parameters:
        - koa_mode {yes*,yes,no}: If 'yes', expect the output to match
          what is seen by datakoa
    """
    RANGE_RE = re.compile('^RANGE (?P<keyword>.*?): (?P<rest>.*)')
    RANGE_KWD_RE = {'start': '(?P<offset>\\d+)\\s+(?P<guid>\\S+)\\s+(?P<src>\\S+)\\s+->\\s+(?P<dst>[^?]+)', 
       'size': '(?P<guid>\\S+)\\s+(?P<bytes>\\d+)', 
       'range': '(?P<guid>\\S+)\\s+(?P<start>\\d+)-(?P<end>\\d+)-(?P<len>\\d+)', 
       'final_range': '(?P<guid>\\S+)\\s+(?P<start>\\d+)-(?P<end>\\d+)-(?P<len>\\d+)', 
       'success': '(?P<offset>\\d+)\\s+(?P<guid>\\S+)\\s+(?P<src>\\S+)\\s+->\\s+(?P<dst>[^?]+)'}
    for (key, value) in RANGE_KWD_RE.items():
        RANGE_KWD_RE[key] = re.compile(RANGE_KWD_RE[key])

    EVENT_MAP = {'success': 'end'}
    FAULT_RE = re.compile('^FAULT!\\s+(?P<module>\\S+?):\\s*(?P<msg>.*)')
    F_END_RE = re.compile('^[45]\\d\\d End\\.')
    F_XIO_RE = re.compile('^[45]\\d\\d-globus_xio:\\s*(?P<msg>.*)')
    F_COMMON_RE = re.compile('^(?P<type>\\w+):\\s*(?P<msg>.*)')
    (STATE_BASE, STATE_FAULT) = (0, 1)

    def __init__(self, f, koa_mode='yes', **kw):
        """Constructor.
        """
        BaseParser.__init__(self, f, fullname=__name__, **kw)
        self._debugging = self.log.isEnabledFor(DEBUG)
        self._koa = as_bool(koa_mode)
        self._state = self.STATE_BASE
        self._curfault = None
        return

    def process(self, line):
        """Process a line of output from GUC.
        """
        if self._debugging:
            self.log.debug('process.start')
        if self._state == self.STATE_BASE:
            result = self.process_base(line)
        elif self._state == self.STATE_FAULT:
            result = self.process_fault(line)
        else:
            result = ()
        if self._debugging:
            self.log.debug('process.end', state=self._state)
        return result

    def process_base(self, line):
        """Process a non-fault line
        """
        d = {}
        m = self.RANGE_RE.match(line)
        if m:
            d = {'ts': time.time()}
            kwd = m.groupdict()['keyword']
            event = kwd.replace('  ', ' ').replace(' ', '_')
            rest = m.groupdict()['rest']
            if self.RANGE_KWD_RE.has_key(event):
                m2 = self.RANGE_KWD_RE[event].match(rest)
                if not m2:
                    raise ValueError("Cannot parse '%s'" % event)
                d.update(m2.groupdict())
                d['event'] = EVENT_PREFIX + self.EVENT_MAP.get(event, event)
            else:
                d = {}
        else:
            m = self.FAULT_RE.match(line)
            if m:
                self._state = self.STATE_FAULT
                self._curfault = Fault(**m.groupdict())
        if d:
            return (d,)
        else:
            return ()

    def process_fault(self, line):
        """Process a line in 'fault' mode.
        """
        result = ()
        match = -1
        for (i, regex) in enumerate((
         self.F_END_RE,
         self.F_XIO_RE,
         self.F_COMMON_RE)):
            m = regex.match(line)
            if m:
                match = i
                d = m.groupdict()
                break

        if match == 0:
            self._state = self.STATE_BASE
            result = self.flush_fault()
        elif match == 1:
            self._curfault.add_xio_error(d['msg'])
            self._curfault.code = 500
        elif match == 2:
            if d['type'] == 'globus_xio':
                self._curfault.add_xio_error(d['msg'])
            else:
                self._curfault.add_error(d['msg'])
        return result

    def flush_fault(self):
        """At end of fault, return event and reset it.
        """
        result = (
         self._curfault.get_event(),)
        self._curfault = None
        return result

    def finalize(self):
        """Return pending fault if any
        """
        if self._curfault:
            return self.flush_fault()
        else:
            return ()