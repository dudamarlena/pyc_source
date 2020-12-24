# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/vmstat.py
# Compiled at: 2010-04-29 16:01:18
"""
Parser for output of 'vmstat' UNIX utility.
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: vmstat.py 24755 2010-04-29 20:01:18Z dang $'
from itertools import izip
from logging import DEBUG
import re, time
from netlogger.parsers import base
from netlogger import nldate

class Parser(base.BaseParser):
    """Parser for output of 'vmstat' UNIX utility.

    Parameters:
       - start_time {yyyy-mm-ddThh:mm:ss (GMT),<now>*}: Time at which 
         netstat started, for generating timestamps.
       - interval {INT,1*}: Interval in seconds between reports, also for
         generating proper timestamps.
    """

    def __init__(self, f, start_time=None, interval='1', **kwargs):
        base.BaseParser.__init__(self, f, fullname=__name__, **kwargs)
        self._dbg = self.log.isEnabledFor(DEBUG)
        if start_time is None:
            self._t0 = time.time()
        else:
            try:
                t0 = nldate.parseISO(start_time + 'Z')
            except ValueError:
                raise ValueError("Bad start time '%s': must be in format 'yyyy-mm-ddThh:mm:ss', in GMT" % start_time)

            self._t0 = t0
        try:
            self._isec = int(interval)
        except ValueError:
            raise ValueError("Bad interval '%s': integer expected" % interval)

        self._nlines = 0
        return

    def process(self, line):
        """Process header or body line from vmstat.

        Sample:
        procs -----------memory---------- ---swap-- -----io---- --system-- -----cpu------
        r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
        0  0      0 5414724 245476 481588    0    0  4425  1225    4   10  2  8 90  0  0
        """
        if line.startswith('procs'):
            return ()
        else:
            fields = line.split()
            v0 = None
            try:
                v0 = int(fields[0])
            except:
                pass

            if v0 is None:
                self._field_names = fields
                return ()
            try:
                values = map(int, fields)
            except ValueError:
                raise

            self._nlines += 1
            ts = self._t0 + self._nlines * self._isec
            event = {base.TS_FIELD: ts, base.EVENT_FIELD: 'vmstat'}
            for (name, value) in izip(self._field_names, values):
                event[name] = value

            return (event,)